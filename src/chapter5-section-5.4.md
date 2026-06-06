# 5.4 生成树相关问题

> **学习目标**：掌握 Kruskal 与 Prim 的适用场景判断、次小生成树的非树边枚举方法以及有向图最小树形图的缩环算法——让生成树从"基础算法"升级为"灵活应用"。

## 理论基础

### 为什么需要学这个？

最小生成树（MST）大概是图论里最容易学的算法了——Kruskal 不就是给边排序然后并查集连起来吗？五分钟就能背下来。可到了题目里，你发现要的不是"最小"而是"次小"；不是"无向图"而是"有向图"；不是"一棵树"而是"在最小生成树的基础上去掉某条边、加上某条边后第二小的树"。

这时候你才意识到：MST 本身不是考点，**对 MST 结构的深入理解**才是。你需要知道 MST 的唯一性条件、知道路径最大边权怎么用、知道 Kruskal 和 Prim 什么时候选哪个。更进阶的——在有向图中求"从根出发的最小树形图"，Kruskal 和 Prim 全都失效了，你需要一个全新的算法。

本节从 MST 的选择策略开始，逐步深入到次小生成树（MST 的灵活延伸）和最小树形图（有向图的 MST 对应物）。学完你会发现，生成树问题不是只有一种题型。

### 核心概念

#### 1. Kruskal 与 Prim —— 两种思想，两种主场

| | Kruskal（加边法） | Prim（加点法） |
|------|-----------|----------|
| 核心操作 | 按边权排序→逐一尝试加入 | 从一个点开始→每次选最近的未加入点 |
| 数据结构 | 并查集 | 优先队列 |
| 复杂度 | O(m log m)，边排序是瓶颈 | O(m log n) |
| 优势场景 | 稀疏图（m 小）、需要路径最大边权 | 稠密图（m 大）、完全图 |

> **选择的直觉**：m 接近 n 时用 Kruskal（排序 O(n log n) 很轻松），m 接近 n² 时用 Prim（排序 O(n² log n) 还不如堆优化 Prim 的 O(n²)）。Kruskal 的另一大优势是"加边过程中可以逐步激活并查集"，非常适合处理动态加边、次小生成树等需要枚举非树边的问题。

> **Kruskal 正确性的切分性质证明**：Kruskal 算法的正确性来源于 MST 的**切分性质（Cut Property）**：对于图中任意一个割（将顶点分成两个集合），连接这两个集合的最小权值边一定属于某棵 MST。证明：假设割的最小权边 e 不在某棵 MST T 中，将 e 加入 T 会形成一个环。在这个环上，必然还有另一条边 e' 也跨越同一个割。由于 e 是最小割边，w(e) ≤ w(e')。用 e 替换 e'，新树的权和 ≤ T 的权和，且仍是生成树。因此存在一棵包含 e 的 MST。Kruskal 算法每步考虑的边恰好是"连接两个不同连通块的当前最小边"——这正是切分性质描述的割边——所以逐条加边构造的树必然是最优的。

#### 2. 次小生成树 —— "换一条边"的思想

**核心策略**：次小生成树与 MST 只有**一条边**不同（这是 MST 的次模性质保证的）。所以方法很简单——枚举每条不在 MST 中的边 `(u,v,w)`，将它加入 MST 会形成环，在环上删去一条最大的 MST 边 `max_edge(u,v)`，得到一棵新生成树。所有权重变化 `w_total - max_edge(u,v) + w` 中取最小值即可。

```
// 预处理 maxcost[u][v]：MST 中 u-v 路径上的最大边权
// 做法：对 MST 做 DFS，每访问一个节点，更新它到所有已访问节点的 maxcost
// 复杂度 O(n²)（对每个起点 DFS 一次）

// 枚举非树边求次小生成树
ans = INF;
for each 非树边 (u, v, w):
    ans = min(ans, mst_total - maxcost[u][v] + w);
```

> **直觉**：加入一条非树边后，环上删去最大边得到的是"代价最小的一棵新树"。所有这样的候选树中取最小的就是次小生成树。

> **严格与非严格次小生成树的区别**：**非严格次小生成树**允许权值和等于 MST（即如果存在另一棵不同的 MST，它也视为次小生成树），实现时只需维护路径上的**最大边权**，当 `MST_total - maxcost[u][v] + w > MST_total` 时更新答案（必须严格大于 MST 才记录）。**严格次小生成树**要求权值和严格大于 MST。问题在于：如果删除的最大边权恰好等于加入的非树边权（即 `maxcost[u][v] == w`），替换后权值和不变，这不是严格次小。处理方法：除了维护路径最大边权外，还要维护**路径次大边权**。当 `max == w` 时，用次大边替换，`MST_total - secondmax + w` 必然严格大于 MST_total。次大边的维护可以通过在 DFS 预处理 maxcost 时同时传递次大值来实现。

#### 3. 最小树形图（朱-刘算法）—— 有向图的"MST"

有向图中，从根节点出发能找到的"所有点可达"的最小边权和的有向树，叫最小树形图。Kruskal/Prim 在这种图上**完全失效**——因为边有方向，你不能随便连。

**缩环算法思想**：
1. 为每个点（除根外）选一条权值最小的入边
2. 如果选的边不形成环，这就是最优解
3. 如果形成环，把这个环缩成一个新点，环上边的权值不变，但**进入环的边权要减去对应点在环上入边的权值**（因为那条入边已经被选过了）
4. 递归上述过程

> **直觉**："缩环"相当于把一个"承诺"——"我先选这个环上的所有入边，之后再决定哪个外部点连过来"——编码到了图的结构上。减去权值的操作确保了最终解不重复计算。

> **朱刘算法缩环的正确性解释**：当为每个非根结点贪心选定最小入边后形成环 C 时，这个环上的点互为入边形成闭环。原问题的合法解必然要"打破"这个环——即舍弃环上某条入边，改选一条从环外点进入的边。缩环操作将环 C 收缩为新点 v_C，并对每条从环外 i 指向环内 j 的边做权值调整 `w'[i][v_C] = w[i][j] - iw[j]`（iw[j] 是 j 当前的最小入边权值）。这个减法的含义是：如果我们决定从 i 连入环来替代 j 的原入边，那么**实际承担的额外代价**只是 `w[i][j] - iw[j]`——因为 j 的原入边 iw[j] 本来就是要"支付"的（它已经在 ans 中被累加），现在只是多付差额。缩环后在新图上递归求解，等价于在原图上做出"打破环的哪条入边"的选择。这个减权操作保证了递归求解的最优性等价于原问题的最优性。

### 知识脉络

```
MST（无向图最小生成树）
    │
    ├──→ Kruskal（边排序 + 并查集）── 稀疏图首选
    │       └──→ 适合后续"枚举非树边"场景
    │
    ├──→ Prim（点扩展 + 优先队列）── 稠密图首选
    │
    ├──→ 次小生成树
    │       └──→ 核心：预处理 MST 路径最大边权
    │
    └──→ 有向图 → 最小树形图（朱-刘算法）
            └──→ 核心：贪心选最小入边 + 缩环
```

从无向到有向、从最优到次优，生成树问题的复杂度逐级递增，但核心思想始终是**贪心 + 对"MST 结构"的性质利用**。

> **跨章关联**：Kruskal算法的并查集实现在**3.1节**有全面展开，包括路径压缩和按秩合并；**3.9节**的树上莫队算法需要先对树进行分块——这与本节例题"邦德"中LCA倍增预处理一脉相承，都是基于DFS序在树上做区间化；**6.2节**的分块思想与本节次小生成树"枚举非树边"的替换策略共享同一个核心直觉——只改变一条边就能得到次优解。

### 快速上手模板

```cpp
// 【Kruskal】稀疏图首选
int fa[maxn];
int find(int x) { return fa[x] == x ? x : fa[x] = find(fa[x]); }

int kruskal(vector<Edge>& edges, int n) {
    sort(edges.begin(), edges.end(), [](auto& a, auto& b) {
        return a.w < b.w;
    });
    for (int i = 1; i <= n; i++) fa[i] = i;
    int cnt = 0, total = 0;
    for (auto [u, v, w] : edges) {
        int fu = find(u), fv = find(v);
        if (fu != fv) {
            fa[fu] = fv;
            total += w;
            mst_edges.push_back({u, v, w});  // 记录 MST 边
            if (++cnt == n - 1) break;
        }
    }
    return cnt == n - 1 ? total : -1;  // -1 表示不连通
}

// 【Prim】稠密图 / 完全图首选
int prim(int n, int g[][maxn]) {
    vector<int> dist(n+1, INF);
    vector<bool> vis(n+1, false);
    dist[1] = 0; int total = 0;
    for (int i = 1; i <= n; i++) {
        int u = -1;
        for (int j = 1; j <= n; j++)
            if (!vis[j] && (u == -1 || dist[j] < dist[u])) u = j;
        if (dist[u] == INF) return -1;  // 不连通
        vis[u] = true; total += dist[u];
        for (int v = 1; v <= n; v++)
            if (!vis[v] && g[u][v] < dist[v])
                dist[v] = g[u][v];
    }
    return total;
}

// 【次小生成树】预处理 MST 树上路径最大边权
void dfs_maxcost(int u, int fa, int w, int root) {
    for (int i = 1; i <= n; i++)
        if (used[i])  // used: 当前 DFS 路径上已访问的点
            maxcost[u][i] = maxcost[i][u] = max(maxcost[fa][i], w);
    used[u] = true;
    for (auto [v, w2] : mst_G[u])
        if (v != fa) dfs_maxcost(v, u, w2, root);
    used[u] = false;
}
```

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
