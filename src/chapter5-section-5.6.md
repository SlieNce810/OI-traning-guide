# 5.6 网络流问题

## 例题32  足球联赛（The K-league, 大田 2002, LA 2531/UVa1306

```cpp
// 例题32  足球联赛（The K-league, 大田 2002, LA 2531/UVa1306
// Rujia Liu
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <numeric>
#include <queue>
#include <vector>
using namespace std;

const int maxn = 700, INF = 1e9;

struct Edge {
  int from, to, cap, flow;
};
bool operator<(const Edge &a, const Edge &b) {
  return a.from < b.from || (a.from == b.from && a.to < b.to);
}
struct Dinic {
  int n, m, s, t;
  vector<Edge> edges; // 边数的两倍
  vector<int> G[maxn]; // 邻接表，G[i][j]表示结点i的第j条边在e数组中的序号
  bool vis[maxn]; // BFS使用
  int d[maxn];    // 从起点到i的距离
  int cur[maxn];  // 当前弧指针

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++)
      G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int cap) {
    edges.push_back((Edge){from, to, cap, 0});
    edges.push_back((Edge){to, from, 0, 0});
    m = edges.size();
    G[from].push_back(m - 2), G[to].push_back(m - 1);
  }

  bool BFS() {
    fill_n(vis, n + 1, false);
    queue<int> Q;
    Q.push(s), vis[s] = true, d[s] = 0;
    while (!Q.empty()) {
      int x = Q.front();
      Q.pop();
      for (size_t i = 0; i < G[x].size(); i++) {
        Edge &e = edges[G[x][i]];
        if (!vis[e.to] && e.cap > e.flow)
          vis[e.to] = true, d[e.to] = d[x] + 1, Q.push(e.to);
      }
    }
    return vis[t];
  }

  int DFS(int x, int a) {
    if (x == t || a == 0)
      return a;
    int flow = 0, f;
    for (int &i = cur[x]; i < G[x].size(); i++) {
      Edge &e = edges[G[x][i]];
      if (d[x] + 1 == d[e.to] && (f = DFS(e.to, min(a, e.cap - e.flow))) > 0) {
        e.flow += f, edges[G[x][i] ^ 1].flow -= f, flow += f, a -= f;
        if (a == 0)
          break;
      }
    }
    return flow;
  }

  int Maxflow(int s, int t) {
    this->s = s, this->t = t;
    int flow = 0;
    while (BFS())
      fill_n(cur, n + 1, 0), flow += DFS(s, INF);
    return flow;
  }
};
Dinic g;
const int maxt = 25 + 5;
int n, w[maxt], d[maxt], a[maxt][maxt];
inline int ID(int u, int v) { return u * n + v + 1; }
inline int ID(int u) { return n * n + u + 1; }
bool canWin(int team) { // 计算team全胜后的总胜利场数
  int total = w[team] + accumulate(a[team], a[team] + n, 0);
  for (int i = 0; i < n; i++) // 全胜又如何?
    if (w[i] > total)         // 有人已经胜的更多了
      return false;

  // 构图。s=0, 结点(u,v)的编号为u*n+v+1, 结点u的编号为n^2+u+1, t=n^2+n+1
  g.init(n * n + n + 2);
  int full = 0, s = 0, t = n * n + n + 1;
  for (int u = 0; u < n; u++) {
    for (int v = u + 1; v < n; v++) {
      if (a[u][v] > 0)
        g.AddEdge(s, ID(u, v), a[u][v]); // S到(u,v)的弧, 容量是剩余的场次
      full += a[u][v]; // (u,v)到u,v的弧，流量表示胜利属于?
      g.AddEdge(ID(u, v), ID(u), INF), g.AddEdge(ID(u, v), ID(v), INF);
    }
    if (w[u] < total)
      g.AddEdge(ID(u), t, total - w[u]); // u到T的弧，u的只能再胜total-w[u]局
  }
  return g.Maxflow(s, t) == full;
}

int main() {
  int T;
  scanf("%d", &T);
  while (T--) {
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
      scanf("%d%d", &w[i], &d[i]);
    for (int i = 0; i < n; i++)
      for (int j = 0; j < n; j++)
        scanf("%d", &a[i][j]);

    for (int i = 0, first = 1; i < n; i++)
      if (canWin(i)) {
        printf("%s", first ? "" : " "), first = 0;
        printf("%d", i+1);
      }
    printf("\n");
  }
  return 0;
}
// 25878256	10779	Collectors Problem	Accepted	C++	0.000	2020-12-23 08:44:16
```

## 例题31  运送超级计算机（Bring Them There, NEERC 2003,LA2957/UVa1324

```cpp
// 例题31  运送超级计算机（Bring Them There, NEERC 2003,LA2957/UVa1324
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<queue>
#include<vector>
#include<algorithm>
using namespace std;

const int maxn = 5000 + 10;
const int INF = 1000000000;

struct Edge {
  int from, to, cap, flow;
};

bool operator < (const Edge& a, const Edge& b) {
  return a.from < b.from || (a.from == b.from && a.to < b.to);
}

struct Dinic {
  int n, m, s, t;
  vector<Edge> edges;    // 边数的两倍
  vector<int> G[maxn];   // 邻接表，G[i][j]表示结点i的第j条边在e数组中的序号
  bool vis[maxn];        // BFS使用
  int d[maxn];           // 从起点到i的距离
  int cur[maxn];         // 当前弧指针

  void init() { edges.clear(); }

  void clearNodes(int a, int b) {
    for(int i = a; i <= b; i++) G[i].clear();
  }

  void AddEdge(int from, int to, int cap) {
    edges.push_back((Edge){from, to, cap, 0});
    edges.push_back((Edge){to, from, 0, 0});
    m = edges.size();
    G[from].push_back(m-2);
    G[to].push_back(m-1);
  }

  bool BFS() {
    memset(vis, 0, sizeof(vis));
    queue<int> Q;
    Q.push(s);
    vis[s] = 1;
    d[s] = 0;
    while(!Q.empty()) {
      int x = Q.front(); Q.pop();
      for(int i = 0; i < G[x].size(); i++) {
        Edge& e = edges[G[x][i]];
        if(!vis[e.to] && e.cap > e.flow) {
          vis[e.to] = 1;
          d[e.to] = d[x] + 1;
          Q.push(e.to);
        }
      }
    }
    return vis[t];
  }

  int DFS(int x, int a) {
    if(x == t || a == 0) return a;
    int flow = 0, f;
    for(int& i = cur[x]; i < G[x].size(); i++) {
      Edge& e = edges[G[x][i]];
      if(d[x] + 1 == d[e.to] && (f = DFS(e.to, min(a, e.cap-e.flow))) > 0) {
        e.flow += f;
        edges[G[x][i]^1].flow -= f;
        flow += f;
        a -= f;
        if(a == 0) break;
      }
    }
    return flow;
  }

  // 求s-t最大流。如果最大流超过limit，则只找一个流量为limit的流
  int Maxflow(int s, int t, int limit) {
    this->s = s; this->t = t;
    int flow = 0;
    while(BFS()) {
      memset(cur, 0, sizeof(cur));
      flow += DFS(s, limit - flow);
      if(flow == limit) break; // 达到流量限制，直接退出
    }
    return flow;
  }
};

Dinic g;

const int maxm = 200 + 10;
int main() {
  int n, m, k, S, T;
  int u[maxm], v[maxm]; // 输入边
  while(scanf("%d%d%d%d%d", &n, &m, &k, &S, &T) == 5) {
    for(int i = 0; i < m; i++) scanf("%d%d", &u[i], &v[i]);
    g.init();
    int day = 1;
    g.clearNodes(0, n-1); // 第一层结点编号为0~n-1。第day层(day>=1)结点编号为day*n~day*n+n-1
    int flow = 0;
    for(;;) {
      // 判断day天是否有解
      // 一架飞船最多需要n-1天到达目的地，沿着这一路线最多需要n+k-2天就可以运完所有飞船，总结点数不超过(n+k-1)n
      g.clearNodes(day*n, day*n+n-1);
      for(int i = 0; i < n; i++) g.AddEdge((day-1)*n+i, day*n+i, INF); // 原地不动
      for(int i = 0; i < m; i++) {
        g.AddEdge((day-1)*n+u[i]-1, day*n+v[i]-1, 1); // u[i]->v[i]
        g.AddEdge((day-1)*n+v[i]-1, day*n+u[i]-1, 1); // v[i]->u[i]
      }
      flow += g.Maxflow(S-1, day*n+T-1, k - flow);
      if(flow == k) break;
      day++;
    }

    // 输出解
    printf("%d\n", day);
    int idx = 0;
    vector<int> location(k, S); // 每架飞船的当前位置
    for(int d = 1; d <= day; d++) {
      idx += n*2;
      vector<int> moved(k, 0); // 第d天有没有移动飞船i
      vector<int> a, b;        // 第d天有一架飞船从a[i]到b[i]
      for(int i = 0; i < m; i++) {
        int f1 = g.edges[idx].flow; idx += 2;
        int f2 = g.edges[idx].flow; idx += 2;
        if(f1 == 1 && f2 == 0) { a.push_back(u[i]); b.push_back(v[i]); }
        if(f1 == 0 && f2 == 1) { a.push_back(v[i]); b.push_back(u[i]); }
      }
      printf("%d", a.size());
      for(int i = 0; i < a.size(); i++) {
        // 查找是哪架飞船从a[i]移动到了b[i]
        for(int j = 0; j < k; j++)
          if(!moved[j] && location[j] == a[i]) {
            printf(" %d %d", j+1, b[i]);
            moved[j] = 1;
            location[j] = b[i];
            break;
          }
      }
      printf("\n");
    }
  }
  return 0;
}
// 25878251	1324	Bring Them There	Accepted	C++	0.030	2020-12-23 08:43:47
```

## 例题33  收集者的难题（Collectors Problem, UVa 10779）

```cpp
// 例题33  收集者的难题（Collectors Problem, UVa 10779）
// Rujia Liu
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>
using namespace std;
const int maxn = 100 + 10, INF = 1e9;
struct Edge {
  int from, to, cap, flow;
};
bool operator<(const Edge &a, const Edge &b) {
  return a.from < b.from || (a.from == b.from && a.to < b.to);
}
struct Dinic {
  int n, m, s, t;
  vector<Edge> edges; // 边数的两倍
  vector<int> G[maxn]; // 邻接表，G[i][j]表示结点i的第j条边在e数组中的序号
  bool vis[maxn]; // BFS使用
  int d[maxn];    // 从起点到i的距离
  int cur[maxn];  // 当前弧指针
  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++)
      G[i].clear();
    edges.clear();
  }
  void ClearFlow() {
    for (size_t i = 0; i < edges.size(); i++)
      edges[i].flow = 0;
  }
  void AddEdge(int from, int to, int cap) {
    edges.push_back((Edge){from, to, cap, 0});
    edges.push_back((Edge){to, from, 0, 0});
    m = edges.size(), G[from].push_back(m - 2), G[to].push_back(m - 1);
  }
  bool BFS() {
    fill_n(vis, n + 1, false);
    queue<int> Q;
    Q.push(s), vis[s] = true, d[s] = 0;
    while (!Q.empty()) {
      int x = Q.front();
      Q.pop();
      for (size_t i = 0; i < G[x].size(); i++) {
        Edge &e = edges[G[x][i]];
        if (!vis[e.to] && e.cap > e.flow)
          vis[e.to] = true, d[e.to] = d[x] + 1, Q.push(e.to);
      }
    }
    return vis[t];
  }
  int DFS(int x, int a) {
    if (x == t || a == 0)
      return a;
    int flow = 0, f;
    for (int &i = cur[x]; i < G[x].size(); i++) {
      Edge &e = edges[G[x][i]];
      if (d[x] + 1 == d[e.to] && (f = DFS(e.to, min(a, e.cap - e.flow))) > 0) {
        e.flow += f, edges[G[x][i] ^ 1].flow -= f, flow += f, a -= f;
        if (a == 0)
          break;
      }
    }
    return flow;
  }
  int Maxflow(int s, int t) {
    this->s = s, this->t = t;
    int flow = 0;
    while (BFS())
      fill_n(cur, n + 1, 0), flow += DFS(s, INF);
    return flow;
  }
};
Dinic g;
int main() {
  int T; scanf("%d", &T);
  for (int kase = 1, n, m; kase <= T; kase++) {
    scanf("%d%d", &n, &m);
    g.init(n + m + 1); // s=0, 物品为点1~m, 除Bob外的人为m+1~m+n-1，t=m+n
    for (int i = 0, k; i < n; i++) {
      scanf("%d", &k);
      vector<int> cnt(m + 1, 0);
      for (int j = 0, kind; j < k; j++) scanf("%d", &kind), cnt[kind]++;
      if (i == 0) { // Bob
        for (int j = 1; j <= m; j++)
          if (cnt[j] >= 1) g.AddEdge(0, j, cnt[j]); // s连边到物品
      } else {                       // 其他人
        for (int j = 1; j <= m; j++) {
          if (cnt[j] >= 2) g.AddEdge(m + i, j, cnt[j] - 1); // 此人可以给出cnt[j]-1个物品j
          else if (cnt[j] == 0) g.AddEdge(j, m + i, 1); // 此人可以接受1个物品j
        }
      }
    }
    for (int i = 1; i <= m; i++) g.AddEdge(i, m + n, 1);
    printf("Case #%d: %d\n", kase, g.Maxflow(0, m+n));
  }
  return 0;
}
// 26481868 10779 Collectors Problem  Accepted  C++ 0.000 2021-06-13 11:55:19
```

## 例题30  UVa11248 Frequency Hopping：使用ISAP算法，加优化

```cpp
// 例题30  UVa11248 Frequency Hopping：使用ISAP算法，加优化
// 刘汝佳
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>
using namespace std;

const int NN = 100 + 10, INF = 1e9;
struct Edge {
  int from, to, cap, flow;
};
bool operator<(const Edge &a, const Edge &b) {
  return a.from < b.from || (a.from == b.from && a.to < b.to);
}
struct ISAP {
  int n, m, s, t;
  vector<Edge> edges;
  vector<int> G[NN]; // 邻接表，G[i][j]表示结点i的第j条边在e数组中的序号
  bool vis[NN]; // BFS使用
  int d[NN];    // 从起点到i的距离
  int cur[NN];  // 当前弧指针
  int p[NN];    // 可增广路上的上一条弧
  int num[NN];  // 距离标号计数

  void AddEdge(int from, int to, int cap) {
    edges.push_back((Edge){from, to, cap, 0});
    edges.push_back((Edge){to, from, 0, 0});
    m = edges.size();
    G[from].push_back(m - 2), G[to].push_back(m - 1);
  }

  bool BFS() {
    fill_n(vis, n + 1, false);
    queue<int> Q;
    Q.push(t), vis[t] = 1, d[t] = 0;
    while (!Q.empty()) {
      int x = Q.front();
      Q.pop();
      for (size_t i = 0; i < G[x].size(); i++) {
        Edge &e = edges[G[x][i] ^ 1];
        if (!vis[e.from] && e.cap > e.flow)
          vis[e.from] = 1, d[e.from] = d[x] + 1, Q.push(e.from);
      }
    }
    return vis[s];
  }

  void ClearAll(int n) {
    this->n = n;
    for (int i = 0; i < n; i++)
      G[i].clear();
    edges.clear();
  }

  void ClearFlow() {
    for (size_t i = 0; i < edges.size(); i++)
      edges[i].flow = 0;
  }

  int Augment() {
    int x = t, a = INF;
    while (x != s) {
      Edge &e = edges[p[x]];
      a = min(a, e.cap - e.flow), x = edges[p[x]].from;
    }
    x = t;
    while (x != s)
      edges[p[x]].flow += a, edges[p[x] ^ 1].flow -= a, x = edges[p[x]].from;
    return a;
  }

  int Maxflow(int s, int t, int need) {
    this->s = s, this->t = t;
    int flow = 0;
    BFS();
    fill_n(num, n + 1, 0);
    for (int i = 0; i < n; i++)
      num[d[i]]++;
    int x = s;
    fill_n(cur, n + 1, 0);
    while (d[s] < n) {
      if (x == t) {
        flow += Augment();
        if (flow >= need)
          return flow;
        x = s;
      }
      int ok = 0;
      for (size_t i = cur[x]; i < G[x].size(); i++) {
        Edge &e = edges[G[x][i]];
        if (e.cap > e.flow && d[x] == d[e.to] + 1) { // Advance
          ok = 1, p[e.to] = G[x][i], cur[x] = i;     // 注意
          x = e.to;
          break;
        }
      }
      if (!ok) {       // Retreat
        int m = n - 1; // 初值注意
        for (size_t i = 0; i < G[x].size(); i++) {
          Edge &e = edges[G[x][i]];
          if (e.cap > e.flow)
            m = min(m, d[e.to]);
        }
        if (--num[d[x]] == 0)
          break;
        num[d[x] = m + 1]++, cur[x] = 0; // 注意
        if (x != s)
          x = edges[p[x]].from;
      }
    }
    return flow;
  }

  vector<int> Mincut() { // call this after maxflow
    BFS();
    vector<int> ans;
    for (size_t i = 0; i < edges.size(); i++) {
      Edge &e = edges[i];
      if (!vis[e.from] && vis[e.to] && e.cap > 0)
        ans.push_back(i);
    }
    return ans;
  }

  void Reduce() {
    for (size_t i = 0; i < edges.size(); i++)
      edges[i].cap -= edges[i].flow;
  }

  void print() {
    printf("Graph:\n");
    for (size_t i = 0; i < edges.size(); i++) {
      const Edge &e = edges[i];
      printf("%d->%d, %d, %d\n", e.from, e.to, e.cap, e.flow);
    }
  }
};

ISAP g;
void solve(int n, int c) {
  int flow = g.Maxflow(0, n - 1, INF);
  if (flow >= c) {
    puts("possible");
    return;
  }
  vector<int> cut = g.Mincut();
  g.Reduce(); // 保留以前的流量
  vector<Edge> ans;
  for (size_t i = 0; i < cut.size(); i++) {
    Edge &e = g.edges[cut[i]];
    e.cap = c, g.ClearFlow();
    if (flow + g.Maxflow(0, n - 1, c) >= c) ans.push_back(e);
    e.cap = 0;
  }
  if (ans.empty()) {
    puts("not possible");
    return;
  }
  sort(ans.begin(), ans.end());
  printf("possible option:(%d,%d)", ans[0].from + 1, ans[0].to + 1);
  for (size_t i = 1; i < ans.size(); i++)
    printf(",(%d,%d)", ans[i].from + 1, ans[i].to + 1);
  puts("");
}

int main() {
  for (int n, e, c, kase = 1; scanf("%d%d%d", &n, &e, &c) == 3 && n; kase++) {
    g.ClearAll(n);
    for (int i = 0, b1, b2, fp; i < e; i++)
      scanf("%d%d%d", &b1, &b2, &fp), g.AddEdge(b1 - 1, b2 - 1, fp);
    printf("Case %d: ", kase);
    solve(n, c);
  }
  return 0;
}
// Accepted 360ms 4250 C++ 5.3.0 2020-12-1418:43:39 25846863
```

## 例题34  生产销售规划（Acme Corporation, UVa 11613）

```cpp
// 例题34  生产销售规划（Acme Corporation, UVa 11613）
// 陈锋
#include <algorithm>
#include <cassert>
#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>
using namespace std;
const int maxn = 202 + 10, INF = 1e9;
typedef long long LL;
struct Edge {
  int from, to, cap, flow, cost;
};

struct MCMF {
  int n, m, s, t;
  vector<Edge> edges;
  vector<int> G[maxn];
  int inq[maxn];  // 是否在队列中
  int d[maxn];    // Bellman-Ford
  int p[maxn];    // 上一条弧
  int a[maxn];    // 可改进量

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int cap, int cost) {
    edges.push_back((Edge){from, to, cap, 0, cost});
    edges.push_back((Edge){to, from, 0, 0, -cost});
    m = edges.size();
    G[from].push_back(m - 2);
    G[to].push_back(m - 1);
  }

  bool BellmanFord(int s, int t, LL& ans) {
    for (int i = 0; i < n; i++) d[i] = INF;
    memset(inq, 0, sizeof(inq));
    d[s] = 0, inq[s] = 1, p[s] = 0, a[s] = INF;

    queue<int> Q;
    Q.push(s);
    while (!Q.empty()) {
      int u = Q.front();
      Q.pop();
      inq[u] = 0;
      for (int i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if (e.cap > e.flow && d[e.to] > d[u] + e.cost) {
          d[e.to] = d[u] + e.cost, p[e.to] = G[u][i];
          a[e.to] = min(a[u], e.cap - e.flow);
          if (!inq[e.to]) Q.push(e.to), inq[e.to] = 1;
        }
      }
    }
    if (d[t] > 0) return false;
    ans += (LL)d[t] * (LL)a[t];
    int u = t;
    while (u != s) {
      edges[p[u]].flow += a[t], edges[p[u] ^ 1].flow -= a[t];
      u = edges[p[u]].from;
    }
    return true;
  }

  // 需要保证初始网络中没有负权圈
  LL Mincost(int s, int t) {
    LL cost = 0;
    while (BellmanFord(s, t, cost))
      ;
    return cost;
  }
};

MCMF g;

int main() {
  int T;
  scanf("%d", &T);
  for (int kase = 1, M, store_cost; kase <= T; kase++) {
    scanf("%d%d", &M, &store_cost);
    g.init(2 * M + 2);
    int source = 0, sink = 2 * M + 1;
    for (int i = 1, make_cost, make_limit, price, sell_limit, max_store; i <= M; i++) {
      scanf("%d%d%d%d%d", &make_cost, &make_limit, &price, &sell_limit, &max_store);
      g.AddEdge(source, i, make_limit, make_cost);
      g.AddEdge(M + i, sink, sell_limit, -price);  // 收益是负费用
      for (int j = 0; j <= max_store; j++)
        if (i + j <= M) g.AddEdge(i, M + i + j, INF, store_cost * j);  // 存j个月以后卖
    }
    printf("Case %d: %lld\n", kase, -g.Mincost(source, sink));
  }
  return 0;
}
// Accepted 120ms 2480 C++5.3.0 2020-12-1418:56:06 25846919
```
