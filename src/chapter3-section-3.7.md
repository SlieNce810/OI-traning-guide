# 3.7 树的经典问题与方法

## 例题34  Rikka与路径的交集（Rikka with Intersection of Paths, ACM/ICPC徐州2018, CodeforceGym 102012G）

### 题目描述
给定一棵N个节点的树和M条简单路径。在所有路径中选择恰好K条，求所有方案中K条路径的交集非空的方案数，结果对1000000007取模。两条路径的交集是指它们公共节点的集合。N, M ≤ 3×10^5, K ≤ M。

### 解题思路
1. **问题转化**：选择K条路径使得它们有公共交点，等价于存在一个点u，使这K条路径都经过u。我们需要对每个点统计经过该点的路径数量。
2. **树上差分统计**：对每条路径(u, v)，在路径端点u和v处+1，在LCA节点d处-1，在d的父亲处-1（如果d不是根）。DFS后序遍历合并差分值，P[u] = 穿过节点u的路径总数。
3. **容斥去重**：如果直接计算C(P[u], K)会有重复——多条路径的交可能包含多个点。正确做法是在"最低公共祖先"处计数。设A[u] = 以u为LCA的路径数，则u对答案的贡献为 C(P[u], K) - C(P[u] - A[u], K)。即从所有经过u的K条路径组合中，排除所有路径都不以u为LCA的情况。
4. **组合数计算**：预处理阶乘和逆元，用公式C(n, k) = n! / (k! * (n-k)!)快速计算。

### 算法方法
**树上差分 + 倍增LCA + 组合数学/容斥原理**：用树上差分维护每条路径对节点的覆盖计数；倍增LCA在O(log N)内求路径端点最近公共祖先并记录A[u]；容斥原理确保每条路径的交集在"最低位置"只被统计一次。

### 复杂度分析
- **时间复杂度**：O((N+M) log N)。每条路径求LCA需O(log N)，树上差分合并O(N)，组合数预处理O(N)。
- **空间复杂度**：O(N log N)，主要存储倍增数组和图的邻接表。

```cpp
// 例题34  Rikka与路径的交集（Rikka with Intersection of Paths, ACM/ICPC徐州2018, CodeforceGym 102012G）
// 陈锋
#include <bits/stdc++.h>
const int NN = 3e5 + 8, MOD = 1000000007, HH = ceil(log2(NN));
using namespace std;
typedef long long LL;
#define _for(i,a,b) for( int i=(a); i<(int)(b); ++i)
#define _rep(i,a,b) for( int i=(a); i<=(int)(b); ++i)

void gcd(LL a, LL b, LL& d, LL& x, LL& y) {
  if (!b) d = a, x = 1, y = 0;
  else gcd(b, a % b, d, y, x), y -= x * (a / b);
}
LL inv(LL a, LL n) { // solve ax≡1 mod n
  LL d, x, y;
  gcd(a, n, d, x, y);
  return d == 1 ? (x + n) % n : -1;
}

LL Fact[NN]; // i!
inline LL C(int a, int b) { // C(a, b)
  if (a < 0 || b < 0 || a < b) return 0;
  return 1LL * (Fact[a] * inv(Fact[a - b], MOD) % MOD)
         * inv(Fact[b], MOD) % MOD;
}

vector<int> G[NN];
int Fa[NN][HH + 1], D[NN], P[NN], A[NN];
inline void dfs(int u, int fa, int d) {
  Fa[u][0] = fa, D[u] = d;
  _rep(i, 1, HH) Fa[u][i] = Fa[Fa[u][i - 1]][i - 1];
  for (auto v : G[u]) if (v != fa) dfs(v, u, d + 1);
}

int lca(int u, int v) {
  if (D[u] < D[v]) swap(u, v);
  int diff = D[u] - D[v];
  _rep(h, 0, HH) if (diff & (1 << h)) u = Fa[u][h];
  if (u == v) return u;
  for (int h = HH; h >= 0; h--)
    if (Fa[u][h] != Fa[v][h]) u = Fa[u][h], v = Fa[v][h];
  return Fa[u][0];
}

inline void differ(int u, int fa) { // 树上差分
  for (auto v : G[u])
    if (v != fa) differ(v, u), P[u] += P[v];
}

int main() {
  Fact[0] = 1;
  _for(i, 1, NN) Fact[i] = 1LL * Fact[i - 1] * i % MOD;
  ios::sync_with_stdio(false), cin.tie(0);
  int T; cin >> T;
  for (int t = 0, N, m, k, u, v; t < T; ++t) {
    cin >> N >> m >> k;
    fill_n(P, N + 1, 0), fill_n(A, N + 1, 0);
    _rep(i, 0, N) G[i].clear();
    _for(i, 1, N) cin >> u >> v, G[u].push_back(v), G[v].push_back(u);
    dfs(1, 0, 1);
    for (int i = 1, d; i <= m; ++i) {
      cin >> u >> v, d = lca(u, v);
      ++A[d], ++P[u], ++P[v], --P[d]; // d多计算一次
      if (d != 1) --P[Fa[d][0]]; // Fa[d]-root多计算两次
    } // P[u]: u→根节点路径上点为端点的简单路径条数之和, A[u]: u是几条路径的LCA?
    differ(1, 0); // 树上差分合并之后：P[u]: 有多少条路径经过u
    LL ans = 0; // 对于两条路径的交点，我们只统计是某直线端点LCA的那个，不是LCA的不算
    _rep(i, 1, N) (ans += C(P[i], k) - C(P[i] - A[i], k) + MOD) %= MOD;
    printf("%lld\n", ans);
  }
  return 0;
}
// 72027006 Feb/28/2020 G - Rikka with Intersections of Paths GNU C++11 Accepted  5677 ms 46000 KB
```

## 例题33  村庄有多远（How far away, HDU 2586） ECJTU 2009 Spring Contest

### 题目描述
给定一棵N个节点的无向带权树和M个查询，每次查询给出两个节点编号u和v，输出节点u到v在树上的最短路径长度。N ≤ 40000, M ≤ 200。

### 解题思路
1. **树上距离公式**：树上任意两点(u, v)间的距离为 `dist(u,v) = Dist[u] + Dist[v] - 2 * Dist[w]`，其中w = LCA(u, v)，Dist[x]表示根节点到x的距离。
2. **DFS预处理**：从根节点（取节点0）开始DFS，记录每个节点的深度D[u]、到根节点的距离Dist[u]，以及进入/离开时间戳Tin[u]、Tout[u]。时间戳用于O(1)判断祖先关系。
3. **倍增法LCA**：用UP[u][i]表示节点u的2^i级祖先。预处理时从小到大递推：`UP[u][i] = UP[UP[u][i-1]][i-1]`。查询时先将深度较深的节点提升到与较浅节点同深度，然后从高位到低位二分跳跃直到两个节点的祖先相同。
4. **祖先关系判**：如果u的Tin[v] ≤ Tin[u] ≤ Tout[v]，则v是u的祖先。

### 算法方法
**倍增法LCA（Binary Lifting）+ DFS + 时间戳**。用倍增数组实现O(log N)的LCA查询，用欧拉序时间戳O(1)判断祖先关系以优化跳跃过程。

### 复杂度分析
- **时间复杂度**：O((N+M) log N)。DFS预处理O(N log N)，每次查询LCA O(log N)，距离计算O(1)。
- **空间复杂度**：O(N log N)，存储UP倍增数组。

```cpp
// 例题33  村庄有多远（How far away, HDU 2586） ECJTU 2009 Spring Contest
// 陈锋
#include <bits/stdc++.h>

using namespace std;
const int MAXN = 40000 + 4;
int N, L, Tin[MAXN], Tout[MAXN], UP[MAXN][18], timer;
struct Edge {
  int v, k;
  Edge(int _v, int _k) : v(_v), k(_k) {}
};
vector<Edge> G[MAXN];
int Dist[MAXN], D[MAXN]; // 到root的距离，深度

// LCA预处理
void dfs(int u, int fa) {
  Tin[u] = ++timer, UP[u][0] = fa;
  if (u) D[u] = D[fa] + 1;
  for (int i = 1; i < L; i++)
    UP[u][i] = UP[UP[u][i - 1]][i - 1];
  for (size_t i = 0; i < G[u].size(); i++) {
    const Edge& e = G[u][i];
    if (e.v != fa) Dist[e.v] = Dist[u] + e.k, dfs(e.v, u);
  }
  Tout[u] = ++timer;
}

bool isAncestor(int u, int v) { return Tin[u] <= Tin[v] && Tout[u] >= Tout[v]; }

int LCA(int u, int v) {
  if (D[u] > D[v]) return LCA(v, u); // 保证u的深度<v的深度
  if (isAncestor(u, v)) return u; // u是v的祖先
  for (int i = L; i >= 0; --i) if (!isAncestor(UP[u][i], v)) u = UP[u][i];
  return UP[u][0];
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T, M, u, v, k;
  L = ceil(log2(N));
  cin >> T;
  while (T--) {
    cin >> N >> M;
    for (int i = 0; i < N; i++) G[i].clear();
    for (int i = 0; i < N - 1; i++)  {
      cin >> u >> v >> k, u--, v--;
      G[u].push_back(Edge(v, k)), G[v].push_back(Edge(u, k));
    }
    memset(UP, 0, sizeof(UP));
    Dist[0] = 0, D[0] = 0;
    dfs(0, 0);

    for (int i = 0; i < M; i++) {
      cin >> u >> v, u--, v--;
      int w = LCA(u, v);
      cout << Dist[u] + Dist[v] - 2 * Dist[w] << endl;
    }
  }
  return 0;
}
// Accepted 46ms 10220kB 1526 G++2020-01-30 11:30:51
```

## 例题37  竞赛（Race, IOI 2011，牛客NC51143）

### 题目描述
给定一棵N个节点的带权树，边的权值可以很大。求一条简单路径（至少包含一条边），满足路径上所有边的权值之和恰好等于K，且路径包含的边数最少。如果不存在这样的路径，输出-1。N ≤ 2×10^5, K ≤ 10^6。

### 解题思路
1. **点分治框架**：在树的递归分解过程中，对于每个重心u，考虑所有经过u的路径。
2. **桶优化**：维护一个全局桶数组F[w] = 权值和为w的"从重心到之前子树中某点"的路径所包含的最少边数。遍历u的每棵子树v，先收集子树v中所有点到根（即u在子树中的子节点）的路径信息{权值和sw, 边数ec}。
3. **组合统计**：对子树v中的每条路径(sw, ec)，检查F[K - sw]是否存在，若存在则用 ec + F[K - sw] 更新答案。
4. **更新桶**：将子树v中的所有路径信息用最小边数更新到F中，供后续子树使用。处理完u的所有子树后，清空本次使用的桶位置。
5. **递归分解**：标记u为已访问，对每个未被访问的子子树继续找重心递归处理。

### 算法方法
**点分治（Centroid Decomposition）+ 桶数组**：利用重心将树分解为大小不超过一半的子树，在每个重心处统计经过该重心的路径；用桶数组（大小为K）记录权值和对应的最小边数，实现O(子树大小)的组合匹配。

### 复杂度分析
- **时间复杂度**：O(N log N)。点分治递归深度O(log N)，每个节点在其祖先重心处被处理一次，每次桶操作O(1)。
- **空间复杂度**：O(N + K)，邻接表O(N)，桶数组F和访问标记Vis各O(K+N)。

```cpp
// 例题37  竞赛（Race, IOI 2011，牛客NC51143）
// 求一条简单路径，权值和等于K，且边数最小。
// 陈锋
#include<bits/stdc++.h>
using namespace std;

const int NN = 2e5 + 8, KK = 1e6 + 8, INF = 1 << 30;
int N, K, MaxSub[NN], SZ[NN], F[KK];
// MaxSub[i]: 去除节点i后得到的森林中节点数最多的树的节点
// SZ：保存子树的节点数
// F[i]权值和为i的路径包含的最小边数
bool Vis[NN];
struct Edge { int v, w; };
struct Path { int w, ec; }; // 路径权值之和，边数
vector<Edge> G[NN];

// 获取子树u的重心, treesz为整个子树大小，重心用来更新center
void find_center(int u, int fa, const int treesz, int& center) {
  int &s = SZ[u], &m = MaxSub[u];
  s = 1, m = 0;
  for (const auto &e : G[u]) {
    if (e.v == fa || Vis[e.v]) continue;
    find_center(e.v, u, treesz, center);
    s += SZ[e.v], m = max(m, SZ[e.v]);
  }
  m = max(m, treesz - s);
  if (m < MaxSub[center]) center = u;
}
// 收集子树u中每个点到根节点的路径的{权值和sw,边数ec}，只考虑权值和<=K的
void collect_path(int u, int fa, int sw, int ec, vector<Path> &S) {
  if (sw > K) return;
  S.push_back({sw, ec});
  for (const Edge &e : G[u])
    if (e.v != fa && !Vis[e.v]) collect_path(e.v, u, sw + e.w, ec + 1, S);
}
// 子树u中所有经过u且权值和=K的路径，这些路径长度(边数)的最小值→min_ec
void solve(int u, int& min_ec) {
  vector<int> q;
  for (const auto & e : G[u]) {
    if (Vis[e.v]) continue;
    vector<Path> S;
    collect_path(e.v, u, e.w, 1, S);
    for (auto& it : S) min_ec = min(min_ec, it.ec + F[K - it.w]); // 当前路径和之前子树路径的组合
    for (auto& it : S) q.push_back(it.w), F[it.w] = min(F[it.w], it.ec); // 更新这条路径对应的F值，让后来的子树用
  }
  for (int i : q) F[i] = INF;
}
void dfs(int u, int& min_ec) { // 递归求解子树u
  Vis[u] = true, F[0] = 0;
  solve(u, min_ec); //
  for (const auto & e : G[u]) {
    if (Vis[e.v]) continue;
    int center = 0; // 找子树v的中心，然后递归求解子树v
    find_center(e.v, u, SZ[e.v], center), dfs(center, min_ec);
  }
}

int main() {
  int N;
  scanf("%d%d", &N, &K);
  for (int i = 1, u, v, w; i < N; ++i) {
    scanf("%d%d%d", &u, &v, &w), ++u, ++v;
    G[u].push_back({v, w}), G[v].push_back({u, w});
  }
  fill_n(F, K + 1, INF);
  MaxSub[0] = INF;
  int min_ec = INF, center = 0;
  find_center(1, 0, N, center), dfs(center, min_ec);
  printf("%d\n", min_ec == INF ? -1 : min_ec);
  return 0;
}
// 46224368 Race Accepted 100 643 31840 2091 C++ 2020-12-23 14:23:18
```

## 例题40 要有彩虹（Let there be rainbows!, IPSC 2009 Problem L）

### 题目描述
给定一棵N个节点的树（节点编号0到N-1），初始所有边无色。有Q个操作，每个操作将路径(x, y)上的所有边涂成某种颜色（共7种颜色：红、橙、黄、绿、蓝、靛、紫）。对于每种颜色c，统计在所有操作中，之前不是颜色c的边因为当前操作被涂成颜色c的边的数量之和。N ≤ 10^6, Q ≤ 10^5。

### 解题思路
1. **树链剖分**：将树进行轻重链剖分（HLD），使得每条重链上的节点在DFS序中连续，可以用线段树维护。
2. **每条重链一棵线段树**：每棵线段树维护区间内每种颜色的出现次数。由于颜色只有7种，可以用位运算（bitmask）表示颜色集合。
3. **路径处理**：对查询路径(x, y)，不断处理x到y之间的重链片段。对于每个片段[l, r]，需要统计该区间内之前不是颜色c但被涂成c的边数 = 区间长度 - 原来已经是颜色c的边数。
4. **重链跳跃**：在两条链的连接处，需要二分查找LCA位置来确定x到y路径上某条重链的终止点。
5. **线段树下推**：使用懒惰标记（setv）进行区间染色。

### 算法方法
**树链剖分（HLD）+ 线段树**。树链剖分将树映射为线性序列，每条重链独立维护一棵线段树；线段树每个节点存储8种颜色的计数（7种颜色+无色）。

### 复杂度分析
- **时间复杂度**：O(N + Q log N)。树链剖分O(N)，每条查询路径上最多涉及O(log N)条重链，每段重链上的线段树操作O(log N)。
- **空间复杂度**：O(N)，线段树和树结构存储线性空间。

```cpp
// 例题40 要有彩虹（Let there be rainbows!, IPSC 2009 Problem L）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i,a,b) for( int i=(a); i<(int)(b); ++i)
#define _rep(i,a,b) for( int i=(a); i<=(int)(b); ++i)
typedef long long LL;
struct IntTree { // 每颗重链对应的线段树，IPSC不卡内存，如果其它OJ，可以考虑动态开点
  struct Node {
    int color, sum[8]; // color:区间颜色:0无颜色, sum:颜色的个数
    void setc(int c, int len) {
      color = c;
      fill_n(sum, 8, 0), sum[c] = len;
    }
    Node() { setc(0, 0); }
  };
  int L;
  vector<Node> data;
  IntTree(int N) { L = 1 << (int)(ceil(log2(N + 2))), data.resize(2 * L); }
  void insert(int l, int r, int clr, int o, int L, int len) {
    if (r <= L || l >= L + len) return; // [L, L+len] ∩ [l,r] = Φ
    Node& d = data[o], &ld = data[2 * o], &rd = data[2 * o + 1];
    if (l <= L && L + len <= r) { // [L, L+len) ∈ (l, r)
      d.setc(clr, len);
      return;
    }
    if (d.color != 0) ld.setc(d.color, len / 2), rd.setc(d.color, len / 2);
    d.setc(0, 0);
    insert(l, r, clr, 2 * o, L, len / 2);
    insert(l, r, clr, 2 * o + 1, L + len / 2, len / 2);
    _for(i, 0, 8) d.sum[i] += ld.sum[i] + rd.sum[i];
  }
  int count(int l, int r, int clr, int o, int L, int len) {
    if (r <= L || l >= L + len) return 0; // [L, L+len] ∩ [l,r] = Φ
    Node& d = data[o], &ld = data[2 * o], &rd = data[2 * o + 1];
    if (l <= L && L + len <= r) return d.sum[clr]; // [L, L+len) ∈ (l, r)
    if (d.color != 0) ld.setc(d.color, len / 2), rd.setc(d.color, len / 2);
    return count(l, r, clr, 2 * o, L, len / 2)
           + count(l, r, clr, 2 * o + 1, L + len / 2, len / 2);
  }
  void insert(int l, int r, int clr) { insert(l, r, clr, 1, 0, L); }
  int count(int l, int r, int clr) { return count(l, r, clr, 1, 0, L); }
};
const int NN = 1e6 + 8;
typedef vector<int> IVec;
IVec G[NN], CH[NN]; // 图的结构
int N, Fa[NN], Tin[NN], Tout[NN], Tsz[NN]; // 父节点，时间戳，子树大小
bool Vis[NN];
int PathId[NN], PathOffset[NN]; // 每个点所在的重链以及在其中的位置
vector<IVec> Paths; // 所有重链独立存放
vector<IntTree> ST; // 每个重链对应一颗线段树

void hld() {
  fill_n(Vis, N + 1, false), fill_n(Tsz, N + 1, 0);
  _rep(i, 0, N) CH[i].clear();
  Paths.clear();

  vector<int> walk; // 后序遍历的DFS序（子节点在父节点之前处理完）
  int time = 0;
  Vis[0] = true, Tin[0] = time, Fa[0] = 0;
  stack<int> sv, se; // sv:当前节点栈, se:当前处理的子节点索引栈（模拟递归）
  sv.push(0), se.push(0);
  while (!sv.empty()) { // 迭代版DFS：模拟递归后序遍历
    ++time;
    int u = sv.top(); sv.pop();
    int e = se.top(); se.pop(); // 当前要处理的子树v的编号
    if (e == (int)G[u].size()) { // u的所有子树都已处理完
      walk.push_back(u), Tout[u] = time, Tsz[u] = 1;
      for (auto v : CH[u]) Tsz[u] += Tsz[v]; // 累加子树体积
    } else {
      sv.push(u), se.push(e + 1); // 继续处理u的下一个子节点
      int v = G[u][e]; // u的子节点v
      if (!Vis[v]) {
        Vis[v] = true, Tin[v] = time, Fa[v] = u, CH[u].push_back(v);
        sv.push(v), se.push(0); // 递归进入v
      }
    }
  }

  fill_n(Vis, N + 1, false);
  Vis[0] = true; // 根节点已处理
  for (auto w : walk) { // 按后序遍历处理：自底向上构建重链
    if (Vis[w]) continue;
    IVec p{w}; // 当前重链，从w开始
    while (true) {
      bool heavy = (2 * Tsz[w] >= Tsz[Fa[w]]); // 判断是否是重儿子
      Vis[w] = true, w = Fa[w], p.push_back(w);
      if (!heavy || Vis[w]) break; // 遇到轻边或已处理节点则停止
    }
    Paths.push_back(p); // 保存这条重链
  }

  PathId[0] = -1; // 根不在任何链上
  _for(i, 0, Paths.size()) _for(j, 0, Paths[i].size() - 1) {
    PathId[Paths[i][j]] = i;      // 节点属于哪条重链
    PathOffset[Paths[i][j]] = j;  // 节点在重链中的偏移位置
  }
  ST.clear();
  for (const auto& p : Paths) ST.emplace_back(p.size() - 1); // 每条链建一棵线段树
}

inline bool is_ancestor(int x, int y) { // x is an ancestor of y ?
  return (Tin[y] >= Tin[x] && Tout[y] <= Tout[x]);
}

// 统计[x-y]路径上过去不是颜色c的，这次被涂成c的边数
// 返回值 = 本次操作新增涂成颜色c的边数
int query(int x, int y, int c) {
  if (x == y) return 0;
  if (is_ancestor(x, y)) return query(y, x, c); // 保证x深度≥y
  int pi = PathId[x], l = PathOffset[x], r = Paths[pi].size() - 1;
  const auto& pt = Paths[pi];
  if (is_ancestor(pt[r], y)) { // y在当前重链中的某处
    while (r - l > 1) { // 二分查找LCA在重链上的位置
      int m = (r + l) / 2;
      if (is_ancestor(pt[m], y)) r = m; else l = m;
    }
    l = PathOffset[x]; // x到r-1是要处理的区间
  }
  int ans = r - l - ST[pi].count(l, r, c); // 区间长度 - 已有颜色c的边数 = 新增颜色c的边数
  ST[pi].insert(l, r, c); // 将该区间涂成颜色c
  return ans + query(pt[r], y, c); // 加上从LCA(x,y)到y路径上的部分
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  string color[] = {"", "red", "orange", "yellow", "green", "blue", "indigo", "violet"};
  map<string, int> CI;
  _rep(i, 1, 7) CI[color[i]] = i;
  int T, Q; cin >> T;
  while (T--) {
    cin >> N;
    _rep(i, 0, N) G[i].clear();
    for (int i = 0, x, y; i < N - 1; ++i)
      cin >> x >> y, G[x].push_back(y), G[y].push_back(x);
    hld();
    cin >> Q;
    vector<LL> ans(8, 0);
    string c;
    for (int i = 0, x, y; i < Q; i++) {
      cin >> x >> y >> c;
      ans[CI[c]] += query(x, y, CI[c]);
    }
    _rep(i, 1, 7) cout << color[i] << " " << ans[i] << endl;
  }
  return 0;
}
```

## 例题39 软件包管理器（NOI 2015）牛客NC 17882）

### 题目描述
给定一棵以1为根的树，每个节点代表一个软件包。节点之间有依赖关系（子节点依赖父节点）。支持两种操作：
- `install x`：安装软件包x及其所有祖先（即1到x路径上的所有软件包），输出本次操作新安装的软件包数。
- `uninstall x`：卸载软件包x及其所有子孙（即x子树中的所有软件包），输出本次操作被卸载的软件包数。
初始所有软件包均未安装。N, Q ≤ 10^5。

### 解题思路
1. **模型分析**：安装操作影响的是从根到x的一条路径，卸载操作影响的是以x为根的子树。维护每个节点的"已安装"状态（0/1）。
2. **树链剖分**：将树进行轻重链剖分，使得每条重链上的节点在线段树中连续。子树在DFS序中也连续。
3. **安装操作**：将1到x路径上所有节点设为1。通过重链跳跃，每次将一条重链的一段区间设为1。安装前先查询该路径上已有多少个1，安装后减去即可得到新安装数量。
4. **卸载操作**：将x子树区间设为0。卸载前查询子树中的1的个数即为被卸载数量。
5. **线段树**：使用带有懒惰set标记的线段树，支持区间赋值和区间求和。

### 算法方法
**树链剖分（HLD）+ 线段树**。重链剖分后通过重链头跳跃处理路径更新；子树区间在DFS序中天然连续，直接在线段树上操作。

### 复杂度分析
- **时间复杂度**：O(N + Q log² N)。树链剖分预处理O(N)，每次安装操作涉及O(log N)条重链，每条重链上线段树操作O(log N)，总共O(log² N)；卸载操作只需一次线段树区间操作O(log N)。
- **空间复杂度**：O(N)，线段树4N空间，树结构线性空间。

```cpp
// 例题39 软件包管理器（NOI 2015）牛客NC 17882）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

typedef long long LL;

template <typename T, int SZ>
struct SegTree {
  struct Node {
    T sumv, setv;
    bool hasSet;
    void setVal(const T& val, int L, int R) {
      setv = val, hasSet = true, sumv = (R - L + 1) * setv;
    }
  };  // sumv: 最新的和；setv: 最新的set标记(子孙不受影响)
  Node NS[SZ];
  int N;
  void init(int _n) {
    N = _n;
    assert((1 << ((int)ceil(log2(N)))) < SZ);
  }

  void pushdown(int o, int L, int R) {
    Node& nd = NS[o];
    if (!nd.hasSet) return;
    int lc = 2 * o, rc = 2 * o + 1, M = (L + R) / 2;
    NS[lc].setVal(nd.setv, L, M), NS[rc].setVal(nd.setv, M + 1, R);
    nd.hasSet = false;
  }

  void setV(int l, int r, const T& v) { update(1, 1, N, v, l, r); }
  void update(int o, int L, int R, const T& v, int qL, int qR) {
    if (qL <= L && qR >= R) {
      NS[o].setVal(v, L, R);
      return;
    }
    int lc = 2 * o, rc = 2 * o + 1, M = (L + R) / 2;
    pushdown(o, L, R);
    if (qL <= M) update(lc, L, M, v, qL, qR);
    if (qR > M) update(rc, M + 1, R, v, qL, qR);
    NS[o].sumv = NS[lc].sumv + NS[rc].sumv;
  }
  T querysum(int l, int r) { return query(1, 1, N, l, r); }
  T query(int o, int L, int R, int qL, int qR) {
    if (qL <= L && qR >= R) return NS[o].sumv;
    pushdown(o, L, R);
    int lc = 2 * o, rc = 2 * o + 1, M = (L + R) / 2;
    T s = 0;
    if (qL <= M) s += query(lc, L, M, qL, qR);
    if (qR > M) s += query(rc, M + 1, R, qL, qR);
    return s;
  }
};

template <int SZ = 1004>
struct HLD {  //树链剖分
  int N, Fa[SZ], HcHead[SZ], Dep[SZ], HcTail[SZ], HSon[SZ], Usz[SZ];
  int ID[SZ], segSz;
  vector<int> G[SZ];
  void init(int _n) {
    segSz = 0;
    N = _n;
    assert(_n < SZ);
  }
  int dfs(int u, int fa) {  //返回子树体积
    int &h = HSon[u], &sz = Usz[u];
    sz = 1, Fa[u] = fa, h = 0, Dep[u] = Dep[fa] + 1;
    for (size_t i = 0; i < G[u].size(); i++) {
      int v = G[u][i];
      if (v == fa) continue;
      sz += dfs(v, u);
      if (Usz[v] > Usz[h]) h = v;  //体积最大的子树
    }
    return sz;  // dfs得到重儿子，深度，父节点
  }
  void hld(int u, int fa, int head) {  //轻重剖分
    ID[u] = ++segSz, HcHead[u] = head;
    if (HSon[u]) {
      hld(HSon[u], u, head);  //重链向下扩展
      for (size_t i = 0; i < G[u].size(); i++) {
        int v = G[u][i];  //轻儿子新开重链
        if (v != fa && v != HSon[u]) hld(v, u, v);
      }
      return;
    }
    HcTail[head] = u;
  }
  void addEdge(int u, int v) { G[u].push_back(v); }
  void build(int root = 1) { dfs(root, 0), hld(root, 0, root); }
};

const int NN = 1e5 + 8;
SegTree<int, NN * 3> St;
HLD<NN> H;
const int Root = 1;
int queryRootPathSum(int u) {  //查询u到树根路径上所有点的权值之和
  int ans = 0;
  while (true) {
    int hu = H.HcHead[u];
    ans += St.querysum(H.ID[hu], H.ID[u]);
    if (hu == Root) break;
    u = H.Fa[hu];
  }
  return ans;
}
void setRootPath(int u) {  //设置u到树根路径上所有点的权值为1
  while (true) {
    int hu = H.HcHead[u];
    St.setV(H.ID[hu], H.ID[u], 1);
    if (hu == Root) break;
    u = H.Fa[hu];
  }
}
int querySubTreeSum(int u) {  //子树u的所有点权之和，所有点在DFS序中是连续的
  return St.querysum(H.ID[u], H.ID[u] + H.Usz[u] - 1);
}
void clearSubTree(int u) {  //设置子树u的所有点权为0
  St.setV(H.ID[u], H.ID[u] + H.Usz[u] - 1, 0);
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int N, Q;
  cin >> N, H.init(N + 1), St.init(N + 1);
  for (int u = 2, p; u <= N; u++) cin >> p, H.addEdge(p + 1, u);
  H.build(Root), cin >> Q;
  string s;
  for (int i = 0, x; i < Q; i++) {
    cin >> s >> x, ++x;
    if (s[0] == 'i') {  //安装 x
      int s0 = queryRootPathSum(x);
      setRootPath(x);
      cout << queryRootPathSum(x) - s0 << endl;
    } else {  //卸载 x
      int s0 = querySubTreeSum(x);
      clearSubTree(x);
      cout << s0 << endl;
    }
  }
  return 0;
}
// 46047267 软件包管理器 答案正确 100 392 12212 3644 C++ 2020-12-13 22:29:46
```

## 例题35  路径统计（Tree, POJ1741）

### 题目描述
给定一棵N个节点的带权树，边的权值均为正整数。统计树上有多少对不同的节点(u, v)，使得u到v的路径上所有边的权值之和不超过K。N ≤ 10000, K ≤ 10^7。

### 解题思路
1. **点分治框架**：在树中递归地找到重心，所有经过重心的路径可以由重心分解为两条"半路径"。
2. **重心选择**：对当前子树，找到删除后剩余连通块大小不超过原树一半的节点作为重心。重心保证每次递归处理的子树规模至少减半。
3. **路径收集**：从重心开始，DFS收集每棵子树中所有点到重心的路径长度。对于每条路径，只保留长度≤K的。
4. **双指针计数**：将所有路径长度排序，用双指针法统计长度之和≤K的路径对数量。这计数了所有经过重心的路径。
5. **去重**：上述计数包含了来自同一棵子树的两条路径组合的情况（这种路径其实不经过重心）。需要减去每棵子树内部的重复计数。
6. **递归**：标记重心为已访问，对每棵子子树递归进行同样过程。

### 算法方法
**点分治（Centroid Decomposition）+ 排序+双指针**。找到重心后，收集所有经过重心的路径长度，排序后用双指针O(N)统计和为≤K的点对数，再减去同一子树内部的重复计数。

### 复杂度分析
- **时间复杂度**：O(N log² N)。每层递归对所有节点进行一次收集和排序，排序O(N log N)，递归深度O(log N)。
- **空间复杂度**：O(N)，存储邻接表和路径数组。

```cpp
// 例题35  路径统计（Tree, POJ1741）
// 陈锋
#include<cstdio>
#include<cassert>
#include<vector>
#include<algorithm>
#include<iterator>

using namespace std;
const int INF = 2147483647, MAXN = 10000 + 4;

struct Edge {
  int v, w;
  Edge(int _v, int _w): v(_v), w(_w) {}
};
int N, K;
vector<Edge> G[MAXN];
bool VIS[MAXN];

int get_size(int u, int fa) { // 子树u的体积
  assert(!VIS[u]);
  int ans = 1;
  for (size_t i = 0; i < G[u].size(); i++) {
    int v = G[u][i].v;
    if (v == fa || VIS[v]) continue;
    ans += get_size(v, u);
  }
  return ans;
}

// 给出子树u的大小，找出其重心
int find_centroid(int u, int fa, int usz, int &ch_sz, int &ct) {
  assert(!VIS[u]);
  int sz = 1, max_ch = -INF;
  for (size_t i = 0; i < G[u].size(); i++) {
    int v = G[u][i].v;
    if (v == fa || VIS[v]) continue;
    int chsz = find_centroid(v, u, usz, ch_sz, ct);
    sz += chsz, max_ch = max(max_ch, chsz);
  }
  max_ch = max(max_ch, usz - sz);
  if (max_ch < ch_sz) ch_sz = max_ch, ct = u;
  return sz;
}

int find_centroid(int u) { // 子树u的重心
  int ch_sz = INF, ct = -1, sz = get_size(u, -1);
  find_centroid(u, -1, sz, ch_sz, ct);
  assert(ct != -1 && ch_sz <= sz / 2);
  return ct;
}

// 收集子树u中所有到u的≤K的路径长度
void get_paths(int u, int fa, int plen, vector<int>& paths) {
  if (plen > K) return;
  paths.push_back(plen);
  for (size_t i = 0; i < G[u].size(); i++) {
    const Edge &e = G[u][i];
    if (e.v != fa && !VIS[e.v])
      get_paths(e.v, u, plen + e.w, paths);
  }
}

// 统计P中两个元素之和<=K的pair个数
inline int count_pairs(vector<int>& P) {
  sort(P.begin(), P.end());
  int ans = 0;
  for (int l = 0, r = P.size() - 1; ; l++) {
    while (r > l && P[r] + P[l] > K) r--;
    if (r <= l) break; // 双指针扫描法
    ans += r - l; // 减去同一颗子树v中的路径
  }
  return ans;
}

int solve(int u) { // 对子树u递归求解
  int ans = 0;
  vector<int> lens; // 所有合法的路径长度
  for (size_t i = 0; i < G[u].size(); i++) {
    const Edge &e = G[u][i];
    if (VIS[e.v]) continue;
    vector<int> ps; // u→子树v中点的所有路径
    get_paths(e.v, u, e.w, ps), ans -= count_pairs(ps);
    copy(ps.begin(), ps.end(), back_inserter(lens));
  }
  ans += count_pairs(lens) + lens.size(); // 从u出发的路径
  VIS[u] = true;
  for (size_t i = 0; i < G[u].size(); i++) {
    const Edge &e = G[u][i];
    if (!VIS[e.v]) ans += solve(find_centroid(e.v));
  }
  return ans;
}

int main() {
  while (scanf("%d%d", &N, &K) == 2 && (N || K)) {
    for (int i = 0; i <= N; i++) G[i].clear(), VIS[i] = false;
    for (int i = 0, u, v, w; i < N - 1; i++) {
      scanf("%d%d%d", &u, &v, &w), u--, v--;
      G[u].push_back(Edge(v, w)), G[v].push_back(Edge(u, w));
    }
    printf("%d\n", solve(find_centroid(0)));
  }
  return 0;
}
// Accepted 547ms 2004kB 2671 G++2020-01-3011:32:29
```

## 例题36  铁人比赛（Ironman Race in Treeland, ACM/ICPC Kuala Lumpur 2008, UVa12161）

### 题目描述
给定一棵N个节点的树，每条边有两个属性：损坏程度d（cost）和长度l（length）。要求选择一条简单路径，使得路径上所有边的损坏程度之和不超过M，且路径长度之和尽可能大。输出最大路径长度。N ≤ 30000, M ≤ 10^8。

### 解题思路
1. **点分治框架**：在重心处考虑所有经过该重心的路径。每条路径由两条从重心出发的半路径组合而成。
2. **维护费用-长度映射**：对于已处理过的子树，维护一个map：费用 -> 最大长度，且保证费用和长度都递增（用upper_bound剔除被支配的元素）。
3. **子树处理**：对于当前重心的每棵子树v，先收集子树v中所有点到子树根节点的路径信息{损坏Cost[u], 长度Dep[u]}。
4. **组合匹配**：对于子树v中的每条路径(cost, len)，在已处理子树的map中找到满足费用 ≤ M - cost 的最大长度，用 len + found_len 更新答案。
5. **插入维护**：将子树v中的所有路径插入map中，保持费用递增、长度递增的性质（删除被支配的项）。
6. **递归处理**：标记重心为已访问，对每个子子树找重心递归处理。

### 算法方法
**点分治（Centroid Decomposition）+ 有序映射（map）**。用map维护费用递增且长度递增的点对，通过upper_bound快速找到满足费用约束的最大长度。

### 复杂度分析
- **时间复杂度**：O(N log² N)。每层递归中map操作O(log N)，每个节点在每层被处理一次，递归深度O(log N)。
- **空间复杂度**：O(N)，存储邻接表和map。

```cpp
// 例题36  铁人比赛（Ironman Race in Treeland, ACM/ICPC Kuala Lumpur 2008, UVa12161）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;
struct Edge { int v, d, l; };
const int INF = 0x3f3f3f3f, MAXN = 3e4 + 10;
typedef map<int, int>::iterator MIT;

int N, M, MaxSub[MAXN], SZ[MAXN], VIS[MAXN], Dep[MAXN], Cost[MAXN];
// MaxSub[i]: 去除节点i后得到的森林中节点数最多的树的节点, SZ[u]：子树u的体积,
// Dep:长度，Cost: 路径的费用
vector<Edge> G[MAXN];
void find_center(int u, int fa, const int tree_sz, int& center) {  //找重心
  int &szu = SZ[u], &msu = MaxSub[u];
  szu = 1, msu = 0;
  for (const Edge& e : G[u]) {
    if (e.v == fa || VIS[e.v]) continue;
    find_center(e.v, u, tree_sz, center);
    szu += SZ[e.v], msu = max(msu, SZ[e.v]);
  }
  msu = max(msu, tree_sz - SZ[u]);
  if (MaxSub[center] > msu) center = u;
}

void insert_cd(map<int, int>& ps, int c, int d) {
  if (c > M) return;
  MIT it = ps.upper_bound(c);
  if (it == ps.begin() || (--it)->second < d) {  // 保证ps里面{费用:长度}同时递增
    ps[c] = d;               // (it-1)->c≤c，要求d>(it-1)->d才插入c:d
    it = ps.upper_bound(c);  // 对于所有的 it(it->c>c)，要求it->d>d，否则删除
    while (it != ps.end() && it->second <= d) ps.erase(it++);
  }
}

void collect_deps(int u, int fa, map<int, int>& ps) {  // 子树u节点路径的花费:长度
  SZ[u] = 1;
  insert_cd(ps, Cost[u], Dep[u]);
  for (const Edge& e : G[u]) {
    if (e.v == fa || VIS[e.v]) continue;
    Dep[e.v] = Dep[u] + e.l, Cost[e.v] = Cost[u] + e.d;
    collect_deps(e.v, u, ps), SZ[u] += SZ[e.v];
  }
}

void count(int u, int& max_len) {  // 计算经过子树u根结点的路径数
  map<int, int> ps, vps;           // u子树, v子树中的 费用:长度
  ps[0] = 0;
  for (const Edge& e : G[u]) {
    if (VIS[e.v]) continue;
    Dep[e.v] = e.l, Cost[e.v] = e.d;
    vps.clear(), collect_deps(e.v, u, vps);
    for (const pair<int, int>& p : vps) {
      MIT it = ps.upper_bound(M - p.first);
      if (it != ps.begin()) max_len = max(max_len, p.second + (--it)->second);
    }
    for (const pair<int, int>& p : vps) insert_cd(ps, p.first, p.second);
  }
}

void solve(int u, int& max_len) {
  count(u, max_len), VIS[u] = true;
  for (const Edge& e : G[u]) {
    if (VIS[e.v]) continue;
    int center = 0;
    find_center(e.v, u, SZ[e.v], center), solve(center, max_len);
  }
}

int main() {
  int T;
  scanf("%d", &T);
  for (int kase = 1; kase <= T; kase++) {
    scanf("%d%d", &N, &M);
    fill_n(VIS, N + 1, 0), MaxSub[0] = N;
    for (int i = 1; i <= N; i++) G[i].clear();
    for (int i = 1, u, v, d, l; i < N; i++) {
      scanf("%d%d%d%d", &u, &v, &d, &l);
      G[u].push_back({v, d, l}), G[v].push_back({u, d, l});
    }
    int center = 0, max_len = 0;
    find_center(1, -1, N, center);  // 找到初始的重心
    solve(center, max_len);         // 递归求解
    printf("Case %d: %d\n", kase, max_len);
  }
  return 0;
}
// Accepted 210ms 2797 C++ 5.3.0 2020-12-13 22:11:33 25843886
```

## 例题38 闪电的能量（Lightning Energy Report, ACM/ICPC Jakarta2010, UVa1674）

### 题目描述
（树链剖分版本）给定一棵N个节点的树，有Q条闪电从节点u经过最短路径击到节点v，每条闪电携带能量w。每条闪电为路径(u, v)上所有节点增加w的能量。对于每个节点，输出它最终的总能量。N, Q ≤ 50000。

### 解题思路（树链剖分版本）
1. **问题**：需要在树上做路径加法，最后查询每个点的值。
2. **树链剖分**：将树进行轻重链剖分，每条重链上的节点在线段树中连续排列。
3. **路径加法**：对于路径(u, v)，不断将较深重链头到当前节点的区间加上w，然后跳到重链头的父节点，直到两点在同一重链上，最后对它们之间的区间加上w。
4. **线段树**：使用加法懒标记（addv）的线段树，支持区间加法和单点查询（沿树遍历累加所有路径上的懒标记）。

### 算法方法
**树链剖分 + 线段树**（区间加法标记）。在线处理每条闪电，支持动态更新和查询。

### 复杂度分析
- **时间复杂度**：O(N + Q log² N)。每条闪电路径上经过O(log N)条重链，每条重链上线段树操作O(log N)。
- **空间复杂度**：O(N)，线段树4N和邻接表。

```cpp
// 例题38 闪电的能量（Lightning Energy Report, ACM/ICPC Jakarta2010, UVa1674）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)
typedef long long LL;

const int MAXN = 65536;
struct SegTree {
  int addv[MAXN * 4], N;
  void update(int o, int L, int R, int qL, int qR, int val) {
    if (qL <= L && R <= qR) {
      addv[o] += val;  //区间加上val
      return;
    }
    int M = (L + R) / 2;
    if (qL <= M) update(o << 1, L, M, qL, qR, val);         //覆盖左区间
    if (M < qR) update(o << 1 | 1, M + 1, R, qL, qR, val);  //覆盖右区间
  }

  void add(int qL, int qR, int val) { update(1, 1, N, qL, qR, val); }

  void init(int o, int L, int R) {  //初始化线段树
    addv[o] = 0;
    if (L == R) return;
    int M = (L + R) / 2;
    init(o << 1, L, M), init(o << 1 | 1, M + 1, R);
  }

  int query(int o, int L, int R, int qv, int val) {
    if (L == R) return val + addv[o];  //找到答案并且将答案返回
    int M = (L + R) >> 1;
    if (qv <= M) return query(o << 1, L, M, qv, val + addv[o]);  //答案在左区间
    return query(o << 1 | 1, M + 1, R, qv, val + addv[o]);  //答案在右区间
  }
};
// Fa[i]为i的父节点,HcHead[i]为i所在重链头,HSon[i]:i重儿子,SZ[i]:子树体积,ID[i]:i在线段树中序号
int Fa[MAXN], HcHead[MAXN], Depth[MAXN], HSon[MAXN], SZ[MAXN], ID[MAXN], intSz;

SegTree ST;
vector<int> G[MAXN];  //存储图
int dfs(int u, int fa) {  //第一次dfs, 得到每个节点的重儿子, 深度, 和父节点
  SZ[u] = 1, Fa[u] = fa, HSon[u] = 0, Depth[u] = Depth[fa] + 1;
  for (auto v : G[u]) {
    if (v == fa) continue;
    SZ[u] += dfs(v, u);
    if (SZ[v] > SZ[HSon[u]]) HSon[u] = v;  //重儿子为体积最大的子树
  }
  return SZ[u];
}
void hld(int u, int fa, int x) {  // 得到节点在线段树中标号及重链的标号
  ID[u] = ++intSz, HcHead[u] = x;  // 重链的标号为该重链最顶端的节点
  if (HSon[u])  // 先处理重链，保证剖分完之后每条重链中的标号是连续的
    hld(HSon[u], u, x);
  for (auto v : G[u])
    if (v != fa && v != HSon[u]) hld(v, u, v);
}

void addPath(int u, int v, int w) {
  while (true) {
    int hu = HcHead[u], hv = HcHead[v];
    if (hu == hv) break;  // 直到两点位于同一条重链才停止
    if (Depth[hu] < Depth[hv]) swap(u, v), swap(hu, hv);  // 更新h→head()
    ST.add(ID[hu], ID[u], w), u = Fa[hu];
  }
  if (Depth[u] < Depth[v]) swap(u, v);
  ST.add(ID[v], ID[u], w);  // 更新u->v
}
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T;
  cin >> T;
  for (int kase = 1, Q, N; kase <= T; kase++) {
    cin >> N;
    assert(N < MAXN);
    ST.N = N, ST.init(1, 1, N);  // 初始化线段树
    for (int i = 1; i <= N; i++) G[i].clear();
    SZ[0] = 0, Depth[1] = 0;
    for (int i = 1, u, v; i < N; i++) {
      cin >> u >> v, u++, v++;  // 输入节点从0开始，转为1开始
      G[u].push_back(v), G[v].push_back(u);
    }
    dfs(1, 1);  // 第一遍DFS：计算重儿子、深度、父节点
    intSz = 0;
    hld(1, 1, 1);  // 第二遍DFS：轻重链剖分，分配DFS序
    cin >> Q;
    for (int i = 0, u, v, w; i < Q; i++) {
      cin >> u >> v >> w, u++, v++;
      addPath(u, v, w);  // 路径(u,v)上所有点增加w能量
    }
    printf("Case #%d:\n", kase);
    for (int i = 1; i <= N; i++) printf("%d\n", ST.query(1, 1, N, ID[i], 0));  // 查询每个点累积的能量
  }
  return 0;
}
// Accepted 140ms 2976 C++5.3.02020-12-1322:18:36 25843914
```

## 例题38 闪电的能量（Lightning Energy Report, ACM/ICPC Jakarta2010, UVa1674）（LCA+差分版本）

### 题目描述
（LCA+树上差分版本）同上题。N, Q ≤ 50000。

### 解题思路（LCA+树上差分版本）
1. **离线处理**：将所有闪电操作一次性读入，用树上差分处理。
2. **树上差分原理**：对于路径(x, y)增加权值c，执行 `mark[x] += c, mark[y] += c, mark[lca(x,y)] -= c, mark[pa(lca)] -= c`（lca的父亲也减一次）。
3. **DFS合并**：后序遍历树，对于每个节点u，`ans[u] = mark[u] + sum(ans[child])`。最终ans[u]就是节点u被所有路径覆盖的总权值。
4. **正确性**：从x到LCA之间的节点（含LCA）都会累加到c；当df累加经过LCA后，mark[lca] -= c抵消了来自x和y方向的重复计数，pa(lca) -= c确保再往上的节点不受影响。

### 算法方法
**LCA（倍增法）+ 树上差分**。离线批量处理所有查询，用差分标记和DFS后序累加实现O(N)的最终答案计算。

### 复杂度分析
- **时间复杂度**：O(N + Q log N)。每条闪电求一次LCA O(log N)，差分标记O(1)，DFS合并O(N)。
- **空间复杂度**：O(N)，倍增数组和邻接表。

```cpp
// 例题38 闪电的能量（Lightning Energy Report, ACM/ICPC Jakarta2010, UVa1674）
// 基于LCA的树上差分解法, 陈锋
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 50000 + 4;

template <int SZ>
struct LCA {
  vector<int> G[MAXN];
  int N, L, Tin[MAXN], Tout[MAXN], UP[MAXN][18], timer;  // LCA相关
  void init(int _n) {
    N = _n, L = ceil(log2(N)), timer = 0;
    for (int i = 0; i <= N; i++) G[i].clear();
  }
  void addEdge(int u, int v) { G[u].push_back(v), G[v].push_back(u); }
  void dfs(int u, int fa = 0) {
    Tin[u] = ++timer, UP[u][0] = fa;
    for (int i = 1; i <= L; i++) UP[u][i] = UP[UP[u][i - 1]][i - 1];
    for (size_t i = 0; i < G[u].size(); i++)
      if (G[u][i] != fa) dfs(G[u][i], u);
    Tout[u] = ++timer;
  }

  bool isAncestor(int u, int v) { return Tin[u] < Tin[v] && Tout[v] < Tout[u]; }

  int lca(int u, int v) {
    if (u == v) return u;
    if (isAncestor(u, v)) return u;
    if (isAncestor(v, u)) return v;
    for (int i = L; i >= 0; --i)
      if (!isAncestor(UP[u][i], v)) u = UP[u][i];
    return UP[u][0];
  }
};

LCA<MAXN> lca;
int mark[MAXN], ans[MAXN];

int dfs_mark(int u, int fa) {
  int &a = ans[u];
  a = mark[u];
  for (size_t i = 0; i < lca.G[u].size(); i++) {
    int v = lca.G[u][i];
    if (v == fa) continue;
    a += dfs_mark(v, u);
  }
  return a;
}

int main() {
  int T;
  cin >> T;
  for (int kase = 1, N, Q, x, y; kase <= T; kase++) {
    cin >> N, lca.init(N);
    for (int i = 1; i < N; i++) cin >> x >> y, lca.addEdge(x, y);
    lca.dfs(0);
    cin >> Q;
    fill_n(mark, N + 1, 0);
    for (int i = 0, c; i < Q; i++) {
      cin >> x >> y >> c;
      int d = lca.lca(x, y), pd = lca.UP[d][0];
      mark[x] += c, mark[y] += c, mark[d] -= c;
      if (pd != d) mark[pd] -= c;
    }
    dfs_mark(0, 0);
    printf("Case #%d:\n", kase);
    for (int i = 0; i < N; i++) printf("%d\n", ans[i]);
  }
}
// Accepted 130ms 1932 C++5.3.0 2020-12-13 22:25:38 25843936
```
