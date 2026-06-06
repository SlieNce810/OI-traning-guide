# 5.4 生成树相关问题

## 例题20  秦始皇修路（Qin Shi Huang's National Road System, 北京 2011, LA5713/UVa1494）

### 题目描述
有 `n` 个城市，每个城市的位置 `(x, y)` 和人口 `p` 已知。秦始皇要修路（国家道路系统），他想要 `(A + B)` 最大化，其中：
- `A` 是某个魔法道路两端城市的人口之和
- `B` 是除去这条魔法道路后，剩下的最小生成树（MST）的总长度

即秦始皇可以先免费修一条路（用魔法），然后剩下的路按最小生成树修建。求 `(pop_u + pop_v) / (MST - maxcost(u,v))` 的最大值，其中 `maxcost(u,v)` 是 MST 中 u 和 v 路径上的最大边权。

**输入格式**：第一行为测试数据组数 `T`。每组数据第一行 `n`，接下来 `n` 行每行 `x y p`。`n ≤ 1000`。**输出格式**：对每组数据，输出最大 `A/B` 值（保留两位小数）。

### 解题思路
**MST + 次小生成树 / 路径最大边权**：免费修一条路等价于在 MST 中加入一条新边并删除 MST 中该边端点间路径上的最大边权（以减少总代价）。

**算法步骤**：
1. 对所有城市对计算欧几里得距离，构建完全图。使用 **Kruskal 算法** 构造 MST，同时记录 MST 的树结构。
2. 在 MST 树上进行 **DFS**，预处理任意两点间的路径最大边权 `maxcost[u][v]`：
   - DFS 遍历 MST 树，维护从根到当前结点的路径上经过的所有结点。
   - 对于新访问的结点 `u`（父结点 `fa`，边权 `facost`），`maxcost[u][x] = max(maxcost[fa][x], facost)`（对已访问的结点 x）。
3. 枚举免费边 `(i, j)`：`A = p[i] + p[j]`，`B = MST_total - maxcost[i][j]`。取最大值。

**核心思想**：`maxcost[i][j]` 是在 MST 中 i 到 j 路径上的最大边权，删除它可以最大化节省。

### 算法方法
- **Kruskal 最小生成树（MST）**：基于并查集，按边权排序。
- **DFS 树遍历**：在 MST 树上预处理任意两点间的最大边权。

### 复杂度分析
- **时间复杂度**：`O(n² log n + n²)`。Kruskal 对完全图 O(n² log n)，DFS 预处理 O(n²)。
- **空间复杂度**：`O(n²)`。存储 `maxcost` 矩阵和所有边。

```cpp
// 例题20  秦始皇修路（Qin Shi Huang's National Road System, 北京 2011, LA5713/UVa1494）
// 解题思路：MST + 路径最大边权预处理——枚举免费魔法道路，最大化 (pop_sum) / (MST-maxcost)
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

vector<int> G[maxn];     // MST 树的邻接表（存储邻接顶点）
vector<double> C[maxn];  // 对应的边权

struct Edge {
  int x, y;
  double d;
  bool operator < (const Edge& rhs) const {
    return d < rhs.d;      // 按边权升序排序，用于 Kruskal
  }
};

Edge e[maxn*maxn];           // 完全图的所有边

double maxcost[maxn][maxn];  // maxcost[u][v]: MST中u到v路径上的最大边权
vector<int> nodes;           // DFS过程中已访问的结点列表

// DFS预处理maxcost：遍历MST树，计算当前结点u到所有已访问结点的最大边权
void dfs(int u, int fa, double facost) {
  for(int i = 0; i < nodes.size(); i++) {
    int x = nodes[i];
    // u 到 x 的最大边权 = max(fa到x的最大边权, u-fa的边权)
    maxcost[u][x] = maxcost[x][u] = max(maxcost[x][fa], facost);
  }
  nodes.push_back(u);                    // 将u加入已访问列表
  for(int i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    if(v != fa) dfs(v, u, C[u][i]);      // 递归处理子结点
  }
}

// Kruskal 算法构建 MST，返回 MST 总长度
double MST() {
  m = 0;
  // 构造完全图：计算所有城市之间的欧几里得距离
  for(int i = 0; i < n; i++)
    for(int j = i+1; j < n; j++)
      e[m++] = (Edge) { i, j, sqrt((x[i]-x[j])*(x[i]-x[j]) + (y[i] - y[j])*(y[i] - y[j])) };
  sort(e, e+m);                         // 按边权排序
  for(int i = 0; i < n; i++) { pa[i] = i; G[i].clear(); C[i].clear(); } // 初始化并查集和MST树
  int cnt = 0;
  double ans = 0;
  for(int i = 0; i < m; i++) {          // Kruskal主循环
    int x = e[i].x, y = e[i].y, u = findset(x), v = findset(y);
    double d = e[i].d;
    if(u != v) {                         // 不形成环
      pa[u] = v;                         // 合并并查集
      G[x].push_back(y); C[x].push_back(d); // 在MST树中添加边
      G[y].push_back(x); C[y].push_back(d);
      ans += d;                          // 累加MST总长
      if(++cnt == n-1) break;            // MST完成
    }
  }
  return ans;
}

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    scanf("%d", &n);
    for(int i = 0; i < n; i++) scanf("%d%d%d", &x[i], &y[i], &p[i]); // 读入城市坐标和人口
    double tot = MST();                       // 计算MST总长度
    memset(maxcost, 0, sizeof(maxcost));
    nodes.clear();
    dfs(0, -1, 0);                            // DFS预处理maxcost
    double ans = -1;
    // 枚举免费魔法道路(i,j)，计算比值
    for(int i = 0; i < n; i++)
      for(int j = i+1; j < n; j++) {
        ans = max(ans, (p[i] + p[j]) / (tot - maxcost[i][j])); // A/B最大化
      }
   printf("%.2lf\n", ans);
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

### 题目描述
有 `N` 个城市和 `M` 条无向道路，每条道路有一个危险系数。邦德要从城市 `s` 到城市 `t` 完成多次任务。对于每次任务，他可以选择一条路径，该路径的危险程度定义为路径上所有道路危险系数的最大值。邦德希望最小化这个最大危险系数。求每次任务的最小危险程度。`N ≤ 50000`, `M ≤ 100000`，查询次数 `Q` 多。

**输入格式**：多组数据。每组第一行 `N M`，接下来 `M` 行 `u v w`，然后 `Q`，接下来 `Q` 行 `s t`。**输出格式**：对每个查询输出最小最大危险系数。

### 解题思路
**MST + LCA 倍增**：最小化路径上的最大边权等价于在 **最小生成树（MST）** 上行走（MST 保证任意路径上的最大边权最小）。

**算法步骤**：
1. 使用 **Kruskal 算法** 构建原图的 MST（最小生成树）。
2. 在 MST 树上进行 **LCA（最近公共祖先）倍增预处理**，同时维护每个结点向上 `2^k` 步路径上的最大边权 `MaxW[u][k]`。
3. 对于每个查询 `(s, t)`：
   - 先求 `s` 和 `t` 的 LCA `l`。
   - 答案是 `max(maxW(l→s), maxW(l→t))`，即 s 到 l 路径上的最大边权和 t 到 l 路径上的最大边权中的较大值。

**关键性质**：在 MST 中，任意两个顶点之间的唯一路径就是"最小瓶颈路径"（路径上最大边权最小）。

### 算法方法
- **Kruskal 最小生成树（MST）**：基于并查集构建。
- **LCA 倍增法（Binary Lifting LCA）**：在 MST 树上预处理 UP 和 MaxW 数组，支持 O(log N) 查询路径最大边权。

### 复杂度分析
- **时间复杂度**：`O(M log M + N log N + Q log N)`。Kruskal O(M log M)，LCA 预处理 O(N log N)，每次查询 O(log N)。
- **空间复杂度**：`O(N log N)`。UP 和 MaxW 数组大小为 O(N log N)。

```cpp
// 例题21  邦德（Bond, UVa 11354）
// 解题思路：MST+LCA倍增——最小瓶颈路径=MST上的唯一路径，LCA维护路径最大边权
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
vector<Edge> G[MAXN]; // MST Tree的邻接表
int L, Tin[MAXN], Tout[MAXN], UP[MAXN][20], MaxW[MAXN][20], timer;
// L: log2(N) 倍增最大层数
// Tin/Tout: DFS进出时间戳，用于O(1)判断祖先关系
// UP[u][i]: u向上2^i步的祖先
// MaxW[u][i]: u向上2^i步路径上的最大边权

bool isAncestor(int u, int v) { return Tin[u] <= Tin[v] && Tout[u] >= Tout[v]; }

// DFS预处理LCA倍增表和路径最大边权
void dfs(int u, int fa, int w) {
  Tin[u] = ++timer, UP[u][0] = fa, MaxW[u][0] = w;    // 初始化第0层
  for (int i = 1; i <= L; i++) {                        // 倍增预处理
    int ui = UP[u][i - 1];
    UP[u][i] = UP[ui][i - 1];                           // 2^i祖先=2^(i-1)的2^(i-1)
    MaxW[u][i] = max(MaxW[u][i - 1], MaxW[ui][i - 1]); // 路径最大边权=max(两段)
  }
  _for(i, 0, G[u].size()) {
    const Edge& e = G[u][i];
    if (e.v != fa) dfs(e.v, u, e.w);                   // 遍历子结点
  }
  Tout[u] = ++timer;
}

// 求u和v的LCA
int LCA(int u, int v) {
  if (isAncestor(u, v)) return u;                      // u是v的祖先
  if (isAncestor(v, u)) return v;                      // v是u的祖先
  for (int i = L; i >= 0; --i)
    if (!isAncestor(UP[u][i], v)) u = UP[u][i];        // 把u跳到LCA下方
  return UP[u][0];                                      // 父结点就是LCA
}

// 求v到祖先u路径上的最大边权（u必须是v的祖先）
int find_maxw(int u, int v) {
  if (u == v) return 0;
  assert(isAncestor(u, v));
  int w = 0;
  for (int i = L; i >= 0; --i) {
    if (!isAncestor(UP[v][i], u) && UP[v][i] != u) {  // 保证u是v的祖先且u≠v
      w = max(w, MaxW[v][i]);                          // 累加最大边权
      v = UP[v][i];                                     // 跳到更高的祖先
    }
  }
  assert(UP[v][0] == u);
  return max(w, MaxW[v][0]);                           // 最后一步
}

int PA[MAXN]; // 并查集
int find_pa(int i) { return PA[i] == i ? i : (PA[i] = find_pa(PA[i])); }

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  vector<Edge> es;
  for (int kase = 0, Q; cin >> N >> M; kase++) {
    L = ceil(log2(N));                                  // 倍增需要的层数
    if (kase) puts("");
    es.clear();
    Edge e;
    _for(i, 0, M) cin >> e.u >> e.v >> e.w, es.push_back(e); // 读入所有边
    sort(es.begin(), es.end());                         // Kruskal: 按边权排序
    _rep(i, 1, N) PA[i] = i;                           // 初始化并查集
    _rep(i, 0, N) G[i].clear();
    _for(i, 0, es.size()) {                            // Kruskal主循环
      const Edge& e = es[i];
      int u = e.u, v = e.v, pu = find_pa(u), pv = find_pa(v);
      if (pu != pv) {                                   // 不形成环
        PA[pv] = pu;                                    // 合并并查集
        G[u].push_back(Edge(u, v, e.w)), G[v].push_back(Edge(v, u, e.w)); // 构建MST树
      }
    }
    timer = 0, dfs(1, 1, 0);                           // LCA倍增预处理
    cin >> Q;
    for (int i = 0, s, t; i < Q; i++) {
      cin >> s >> t;
      int l = LCA(s, t);                               // 求LCA
      assert(s != t);
      printf("%d\n", max(find_maxw(l, s), find_maxw(l, t))); // s→l和t→l路径上的最大边权中的较大值
    }
  }
  return 0;
}
// Accepted 70ms 2400 C++11 5.3.0 2020-01-31 11:54:07 24489014
```

## 例题22  比赛网络（Stream My Contest, UVa 11865）

### 题目描述
有一个比赛网络，要从源结点 0 直播到 `N` 个其他结点。有 `M` 条可能的网络连接，每条连接 `(u, v, b, c)` 有带宽 `b` 和费用 `c`。你有一个总预算 `C`，需要选择一部分有向边，构建一棵以 0 为根的有向生成树（树形图/最小树形图），使得总费用不超过 `C`。带宽瓶颈定义为树中的最小带宽。求在满足预算的前提下，带宽瓶颈最大可以是多少。`N ≤ 60`, `M ≤ 10000`。

**输入格式**：第一行为测试数据组数 `T`。每组数据第一行 `N M C`，接下来 `M` 行 `u v b c`。**输出格式**：对每组数据输出最大带宽瓶颈，若无可行方案输出 "streaming not possible."。

### 解题思路
**二分答案 + 最小树形图（Minimum Arborescence）**：最大化最小带宽是典型的二分答案问题。

**二分框架**：对于猜测的带宽值 `X`，只考虑带宽 ≥ X 的边，检查是否存在一棵总费用 ≤ C 的以 0 为根的最小树形图。

**算法步骤**：
1. 将所有边按带宽降序排序。
2. 二分带宽值 `X`：选取带宽前 `k` 大的边，构建图。
3. 对该图计算最小树形图（使用 **固定根最小树形图算法**，即朱-刘算法 / Edmonds' algorithm）。
4. 如果最小树形图的总费用 ≤ C，说明 `X` 可行，尝试更大的 `X`；否则尝试更小的 `X`。

**最小树形图算法（MDST）**：
- 初始化：每个非根结点选择一条最小入边。
- 缩圈：如果选择的边形成了圈，将整个圈缩为一个新结点，并调整进入/离开圈的边的权值。
- 重复直到无圈，将缩圈时记录的边权和作为结果。

### 算法方法
- **二分答案（Binary Search）**：二分最小带宽瓶颈。
- **最小树形图（Minimum Arborescence）/ Edmonds' Algorithm**：以 0 为根的固定根最小树形图。

### 复杂度分析
- **时间复杂度**：`O(log M × N³)`。二分 `O(log M)` 次，每次最小树形图 O(N³)（邻接矩阵实现，N ≤ 60）。
- **空间复杂度**：`O(N²)`。邻接矩阵存储边权。

```cpp
// 例题22  比赛网络（Stream My Contest, UVa 11865）
// 解题思路：二分答案+最小树形图(MDST)——选带宽≥X的边，判断能否构造成本≤C的树形图
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
