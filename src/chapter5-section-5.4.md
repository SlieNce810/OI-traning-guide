# 5.4 生成树相关问题

## 例题20  秦始皇修路（Qin Shi Huang’s National Road System, 北京 2011, LA5713/UVa1494）

```cpp
// 例题20  秦始皇修路（Qin Shi Huang’s National Road System, 北京 2011, LA5713/UVa1494）
// Rujia Liu
#include<cstdio>
#include<cmath>
#include<cstring>
#include<vector>
#include<algorithm>
using namespace std;

const int maxn = 1000 + 10;
int n, m, x[maxn], y[maxn], p[maxn];

int pa[maxn];
int findset(int x) { return pa[x] != x ? pa[x] = findset(pa[x]) : x; } 

vector<int> G[maxn];
vector<double> C[maxn];

struct Edge {
  int x, y;
  double d;
  bool operator < (const Edge& rhs) const {
    return d < rhs.d;
  }
};

Edge e[maxn*maxn];

double maxcost[maxn][maxn];
vector<int> nodes;

void dfs(int u, int fa, double facost) {
  for(int i = 0; i < nodes.size(); i++) {
    int x = nodes[i];
    maxcost[u][x] = maxcost[x][u] = max(maxcost[x][fa], facost);
  }
  nodes.push_back(u);
  for(int i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    if(v != fa) dfs(v, u, C[u][i]);
  }
}

double MST() {
  m = 0;
  for(int i = 0; i < n; i++)
    for(int j = i+1; j < n; j++)
      e[m++] = (Edge) { i, j, sqrt((x[i]-x[j])*(x[i]-x[j]) + (y[i] - y[j])*(y[i] - y[j])) };
  sort(e, e+m);
  for(int i = 0; i < n; i++) { pa[i] = i; G[i].clear(); C[i].clear(); }
  int cnt = 0;
  double ans = 0;
  for(int i = 0; i < m; i++) {
    int x = e[i].x, y = e[i].y, u = findset(x), v = findset(y);
    double d = e[i].d;
    if(u != v) {
      pa[u] = v;
      G[x].push_back(y); C[x].push_back(d);
      G[y].push_back(x); C[y].push_back(d);
      ans += d;
      if(++cnt == n-1) break;
    }
  }
  return ans;
}

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    scanf("%d", &n);
    for(int i = 0; i < n; i++) scanf("%d%d%d", &x[i], &y[i], &p[i]);
    double tot = MST();
    memset(maxcost, 0, sizeof(maxcost));
    nodes.clear();
    dfs(0, -1, 0);
    double ans = -1;
    for(int i = 0; i < n; i++)
      for(int j = i+1; j < n; j++) {
        ans = max(ans, (p[i] + p[j]) / (tot - maxcost[i][j]));
      }
   printf("%.2lf\n", ans);
  }
  return 0;
}
// 25878195	1494	Qin Shi Huang's National Road System	Accepted	C++	0.090	2020-12-23 08:29:32
```

## 例题21  邦德（Bond, UVa 11354）

```cpp
// 例题21  邦德（Bond, UVa 11354）
// 陈锋
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)

const int MAXN = 50000 + 4;
struct Edge {
  int u, v, w;
  Edge(int _u = 0, int _v = 0, int _w = 0) : u(_u), v(_v), w(_w) {}
  bool operator<(const Edge& e) const {
    return w < e.w;
  }
};

int N, M;
vector<Edge> G[MAXN]; // MST Tree
int L, Tin[MAXN], Tout[MAXN], UP[MAXN][20], MaxW[MAXN][20], timer;

bool isAncestor(int u, int v) { return Tin[u] <= Tin[v] && Tout[u] >= Tout[v]; }

void dfs(int u, int fa, int w) {
  Tin[u] = ++timer, UP[u][0] = fa, MaxW[u][0] = w;
  for (int i = 1; i <= L; i++) {
    int ui = UP[u][i - 1];
    UP[u][i] = UP[ui][i - 1];
    MaxW[u][i] = max(MaxW[u][i - 1], MaxW[ui][i - 1]);
  }
  _for(i, 0, G[u].size()) {
    const Edge& e = G[u][i];
    if (e.v != fa) dfs(e.v, u, e.w);
  }
  Tout[u] = ++timer;
}

int LCA(int u, int v) {
  if (isAncestor(u, v)) return u;
  if (isAncestor(v, u)) return v;
  for (int i = L; i >= 0; --i) if (!isAncestor(UP[u][i], v)) u = UP[u][i];
  return UP[u][0];
}

int find_maxw(int u, int v) { // max w of v → u, u = Ancestor(v)
  if (u == v) return 0;
  assert(isAncestor(u, v));
  int w = 0;
  for (int i = L; i >= 0; --i) {
    if (!isAncestor(UP[v][i], u) && UP[v][i] != u) { // 保证u是v的祖先，且u != v
      w = max(w, MaxW[v][i]);
      v = UP[v][i];
    }
  }
  assert(UP[v][0] == u);
  return max(w, MaxW[v][0]);
}

int PA[MAXN]; // Union-Set
int find_pa(int i) { return PA[i] == i ? i : (PA[i] = find_pa(PA[i])); }

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  vector<Edge> es;
  for (int kase = 0, Q; cin >> N >> M; kase++) {
    L = ceil(log2(N));
    if (kase) puts("");
    es.clear();
    Edge e;
    _for(i, 0, M) cin >> e.u >> e.v >> e.w, es.push_back(e);
    sort(es.begin(), es.end());
    _rep(i, 1, N) PA[i] = i;
    _rep(i, 0, N) G[i].clear();
    _for(i, 0, es.size()) {
      const Edge& e = es[i];
      int u = e.u, v = e.v, pu = find_pa(u), pv = find_pa(v);
      if (pu != pv) {
        PA[pv] = pu;
        G[u].push_back(Edge(u, v, e.w)), G[v].push_back(Edge(v, u, e.w));
      }
    }
    timer = 0, dfs(1, 1, 0); // MST LCA
    cin >> Q;
    for (int i = 0, s, t; i < Q; i++) {
      cin >> s >> t;
      int l = LCA(s, t);
      assert(s != t);
      printf("%d\n", max(find_maxw(l, s), find_maxw(l, t)));
    }
  }
  return 0;
}
// Accepted 70ms 2400 C++11 5.3.0 2020-01-31 11:54:07 24489014
```

## 例题22  比赛网络（Stream My Contest, UVa 11865）

```cpp
// 例题22  比赛网络（Stream My Contest, UVa 11865）
// 刘汝佳
#include <bits/stdc++.h>
using namespace std;
const int INF = 1e9, maxn = 100 + 10;

// 固定根的最小树型图，邻接矩阵写法
struct MDST {
  int n;
  int w[maxn][maxn]; // 边权
  int vis[maxn];     // 访问标记，仅用来判断无解
  int ans;           // 计算答案
  int removed[maxn]; // 每个点是否被删除
  int cid[maxn];     // 所在圈编号
  int pre[maxn];     // 最小入边的起点
  int iw[maxn];      // 最小入边的权值
  int max_cid;       // 最大圈编号

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++)
      for (int j = 0; j < n; j++) w[i][j] = INF;
  }

  void AddEdge(int u, int v, int cost) {
    w[u][v] = min(w[u][v], cost); // 重边取权最小的
  }

  // 从s出发能到达多少个结点
  int dfs(int s) {
    vis[s] = 1;
    int ans = 1;
    for (int i = 0; i < n; i++)
      if (!vis[i] && w[s][i] < INF) ans += dfs(i);
    return ans;
  }

  // 从u出发沿着pre指针找圈
  bool cycle(int u) {
    max_cid++;
    int v = u;
    while (cid[v] != max_cid) { cid[v] = max_cid; v = pre[v]; }
    return v == u;
  }

  // 计算u的最小入弧，入弧起点不得在圈c中
  void update(int u) {
    iw[u] = INF;
    for (int i = 0; i < n; i++)
      if (!removed[i] && w[i][u] < iw[u]) {
        iw[u] = w[i][u];
        pre[u] = i;
      }
  }

  // 根结点为s，如果失败则返回false
  bool solve(int s) {
    memset(vis, 0, sizeof(vis));
    if (dfs(s) != n) return false;

    memset(removed, 0, sizeof(removed));
    memset(cid, 0, sizeof(cid));
    for (int u = 0; u < n; u++) update(u);
    pre[s] = s; iw[s] = 0; // 根结点特殊处理
    ans = max_cid = 0;
    for (;;) {
      bool have_cycle = false;
      for (int u = 0; u < n; u++) if (u != s && !removed[u] && cycle(u)) {
          have_cycle = true;
          // 以下代码缩圈，圈上除了u之外的结点均删除
          int v = u;
          do {
            if (v != u) removed[v] = 1;
            ans += iw[v];
            // 对于圈外点i，把边i->v改成i->u（并调整权值）；v->i改为u->i
            // 注意圈上可能还有一个v'使得i->v'或者v'->i存在，因此只保留权值最小的i->u和u->i
            for (int i = 0; i < n; i++) if (cid[i] != cid[u] && !removed[i]) {
                if (w[i][v] < INF) w[i][u] = min(w[i][u], w[i][v] - iw[v]);
                w[u][i] = min(w[u][i], w[v][i]);
                if (pre[i] == v) pre[i] = u;
              }
            v = pre[v];
          } while (v != u);
          update(u);
          break;
        }
      if (!have_cycle) break;
    }
    for (int i = 0; i < n; i++)
      if (!removed[i]) ans += iw[i];
    return true;
  }
};

//////// 题目相关
MDST solver;
struct Edge {
  int u, v, b, c;
  bool operator < (const Edge& rhs) const {
    return b > rhs.b;
  }
};

const int maxm = 10000 + 10;
int N, M, C;
Edge edges[maxm];

// 取b前cnt大的边构造网络，判断最小树型图的边权和是否小于C
bool check(int cnt) {
  solver.init(N);
  for (int i = 0; i < cnt; i++)
    solver.AddEdge(edges[i].u, edges[i].v, edges[i].c);
  if (!solver.solve(0)) return false;
  return solver.ans <= C;
}

int main() {
  int T;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%d%d", &N, &M, &C);
    for (int i = 0; i < M; i++) {
      scanf("%d%d%d%d", &edges[i].u, &edges[i].v, &edges[i].b, &edges[i].c);
    }
    sort(edges, edges + M);
    int l = 1, r = M, ans = -1;
    while (l <= r) {
      int m = l + (r - l) / 2;
      if (check(m)) ans = edges[m - 1].b, r = m - 1;
      else l = m + 1;
    }
    if (ans < 0) printf("streaming not possible.\n");
    else printf("%d kbps\n", ans);
  }
  return 0;
}
// Accepted 10ms 3277 C++11 5.3.0 2020-01-3111:54:45 24489015
```
