# 5.3 最短路问题

> **学习目标**：理解 Dijkstra、Bellman-Ford、Floyd 三种算法的本质差异与正确性条件，并掌握状态图最短路建模——做到"不是记模板，而是选对算法"。

## 理论基础

### 为什么需要学这个？

最短路大概是你学图论时接触的第一个"有名字的算法"。Dijkstra 就那么几行代码，背下来就跑——SPFA 被卡了？换成堆优化的 Dijkstra 就行了——你是不是也这么想的？

但真实竞赛里最短路从来不是"给我图求距离"这么简单。真正的坑在于：
- 题目不告诉你"这是最短路题"，你得自己看出"这东西可以转化成图上求最短路径"；
- 三个算法看起来都能求最短路，但**用错一个就全盘皆输**——Dijkstra 碰到负边会死循环，Bellman-Ford 在稀疏图上太慢，Floyd 对大图根本跑不动；
- 最隐蔽的陷阱是**状态图上的最短路**——图不是题目给的，是你自己"构造"出来的。

这一节就是要帮你打通这三道关：算法的**正确性边界**（什么情况下用哪个）、**状态图建模**（怎么把题目转化成图）、以及**选算法的判断力**（看一眼数据范围就知道该用哪个）。

### 核心概念

#### 1. 松弛操作——三个算法的唯一共同点

```cpp
// 松弛：尝试用 u 的距离更新 v
if (dist[u] + w(u,v) < dist[v])
    dist[v] = dist[u] + w(u,v);
```

整个最短路问题的所有算法，本质上只是在回答一个问题：**按什么顺序执行松弛操作？**

| 算法 | 松弛顺序 | 复杂度 | 条件 |
|------|----------|--------|------|
| Dijkstra | 按 dist 递增（贪心） | O(m log n) | 边权非负 |
| Bellman-Ford | 暴力 n-1 轮全边松弛 | O(nm) | 任意边权 |
| Floyd | 三层循环、枚举中间点 | O(n³) | 全源 |

#### 2. Dijkstra——为什么边权非负是硬要求

Dijkstra 的核心操作是：每次选一个**未确定的、dist 最小**的点 u，并标记它"已确定"——它的最短距离不会再更新了。当边权非负时，没有任何未确定的点能通过 u "迂回"得到更短的距离（因为 w(u,v) ≥ 0，只会增加不会减少）。

> **反例**：如果存在负边 `w(u,v) = -5`，那 dist[v] 可能 = dist[u] - 5 < dist[u]，但我们刚才已经把 u 标记为"已确定"了——这就是 Dijkstra 在负边图上失效的原因。

> **Dijkstra 正确性的归纳证明（N 步骤）**：设 S 为"已确定最短距离"的点集。归纳假设：每次从优先队列中取出点 u 时，dist[u] 已经是 u 的真实最短距离。**归纳基础**：S = ∅ 时，源点 s 的 dist[s] = 0，显然正确。**归纳步骤**：假设当前 S 中所有点的距离都已确定。从优先队列取出 dist 最小的未入 S 点 u。考虑任何从 s 到 u 的实际最短路径 P，P 上必然存在第一个不在 S 中的点 w。设 w 在 P 上的前驱为 v（v ∈ S）。则 dist[w] ≤ dist[v] + w(v,w) = w 的真实最短距离（v 已确定）。又因为 u 是优先队列中 dist 最小的点，所以 dist[u] ≤ dist[w] ≤ w 的真实最短距离 ≤ u 的真实最短距离（P 经过 w，多走不会更短）。而 dist[u] 本身是从 s 到 u 的某条路径长度，不可能小于真实最短距离。因此 dist[u] 就等于真实最短距离。证毕。

#### 3. Bellman-Ford —— 负环是唯一的"无解"情况

Bellman-Ford 不挑边权，每轮对所有边松弛一次，重复 n-1 轮（最短路最多经过 n-1 条边）。第 n 轮如果还能松弛，说明存在**负环**——你可以在负环上无限绕圈，让距离趋向负无穷。

> **直觉**：松弛操作的物理意义是"试图用更多边来获得更短距离"。每轮松弛相当于允许路径多用一条边。n 轮后还能优化，说明有一条用了 n 条边还能更短的路径——那必然是兜圈子了。

> **SPFA 为什么会被卡？网格图的最坏情况分析**：SPFA 是 Bellman-Ford 的队列优化版——只有被松弛成功的点才会入队重试。在随机图上，SPFA 期望 O(km)（k 为小常数），但在**刻意构造的网格图**上，SPFA 的复杂度可以退化到 O(nm)。构造方法：将网格的每行每列都连成"V 字形"边权序列（例如 1, 2, 4, 8, ...），使得每个点的松弛会引发连锁反应——点 A 被更新后入队，出队时更新 B，B 入队后更新 C，...，最后 C 又反过来更新 A，形成指数级复发入队。更直观的理解：网格图上最短路径的层级关系复杂，BFS 分层失效，SPFA 失去了"每次松弛即确定一层"的性质，退化为穷举式不断修正。

#### 4. Floyd —— k 为什么必须在最外层

Floyd 的三重循环顺序是 `for k: for i: for j`，不能调换。原因在于动态规划定义：`dist[k][i][j]` 表示"只经过编号 ≤ k 的中间点，从 i 到 j 的最短距离"。每次增加 k 时，相当于允许经过一个新中间点。如果把 k 放在内层，就会在中间点集合还没确定时就使用它来松弛——违背了 DP 的阶段顺序。

> **深入解释**：Floyd 的状态定义为 `d[k][i][j]`，其中 k 是**阶段**，i 和 j 是**状态**。状态转移方程是 `d[k][i][j] = min(d[k-1][i][j], d[k-1][i][k] + d[k-1][k][j])`。这个转移要求 k-1 阶段的所有 (i,j) 对都已计算完毕，才能推出 k 阶段的值。因此 k 必须是最外层循环。如果将 k 放在内层（如 `for i: for j: for k`），则在计算 (i,j) 时使用的 `d[i][k]` 可能已经被当前阶段更新过——它本应代表"用 ≤k-1 号中间点从 i 到 k 的最短路径"，但实际可能已经用了当前 k 值（即用了更大编号的中间点）。这种"提前使用未来信息"的错误会导致结果不正确。正确的滚动数组实现只需要将 k 放在最外层，内层 i 和 j 的顺序可以互换。

#### 5. 状态图最短路——图是"造"出来的

有些问题输入不直接给图，而是给一组**状态转移规则**。比如："当前位置 cur，已访问集合 S，求完成所有任务的最短时间"。这时**状态本身是图的结点**，状态间的转移是边，边权是转移代价。

> **核心思想**：把题目中的"当前局面"抽象成结点，把"一步操作"抽象成边。图的规模等于状态总数（可能很大），这是隐式图问题——不显式建图，而是在 Dijkstra 中"即用即算"。

### 知识脉络

```
松弛操作（核心操作）
    │
    ├──→ 边权非负 ──→ Dijkstra（贪心，最快）
    │                    └──→ 状态图最短路（隐式图 + 堆优化）
    │
    ├──→ 边权任意 ──→ Bellman-Ford / SPFA
    │                    └──→ 负环检测（第 n 轮判断）
    │                    └──→ 差分约束（看成最短路的约束表达）
    │
    └──→ 全源需求 ──→ Floyd（O(n³)，n ≤ 300 可用）
                         └──→ k 在最外层是 DP 顺序要求
```

选算法的决策树：先看 n 的大小（n ≤ 300 直接用 Floyd），再看边权是否非负（非负用 Dijkstra），最后看是否需要负环检测（用 Bellman-Ford）。

> **跨章关联**：最短路算法在全书多个场景中作为建模工具出现——**2.7节**中矩阵乘法用于求解"经过恰好k条边的最短路"，这本质上是Floyd的矩阵形式推广；**3.2节**线段树优化建图将稀疏图上的最短路加速到 O(log² n)；**5.1节**的差分约束系统和**5.6节**的费用流都把最短路作为底层引擎；**6.4节**几何专题中"二分答案+最短路判断"是状态图最短路建模的经典模式。

### 快速上手模板

```cpp
// 【Dijkstra】边权非负 + 路径记录
typedef pair<int,int> pii;
void dijkstra(int s) {
    priority_queue<pii, vector<pii>, greater<pii>> pq;
    fill(dist, dist+n+1, INF);
    dist[s] = 0; pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;  // 过时数据
        for (auto [v, w] : G[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pre[v] = u;           // 记录路径
                pq.push({dist[v], v});
            }
        }
    }
}

// 【Bellman-Ford】任意边权 + 负环检测
bool bellman_ford(int s) {
    fill(dist, dist+n+1, INF);
    dist[s] = 0;
    for (int i = 1; i < n; i++)      // n-1 轮松弛
        for (auto [u, v, w] : edges)
            if (dist[u] != INF && dist[u] + w < dist[v])
                dist[v] = dist[u] + w;
    for (auto [u, v, w] : edges)     // 第 n 轮：检测负环
        if (dist[u] != INF && dist[u] + w < dist[v])
            return false;             // 存在负环
    return true;
}

// 【Floyd】全源最短路（n ≤ 300）
for (k = 1; k <= n; k++)             // k 必须在最外层！
    for (i = 1; i <= n; i++)
        for (j = 1; j <= n; j++)
            if (d[i][k] + d[k][j] < d[i][j])
                d[i][j] = d[i][k] + d[k][j];
```

## 例题18  低价空中旅行（Low Cost Air Travel, World Finals 2006, LA3561/UVa1048）

### 题目描述
Bob 需要完成若干次旅行（Trip）。他手中有一些联票（Ticket），每张联票有固定的价格，包含一序列的城市（航段），可以按顺序使用但不能跳段使用。每次旅行有一个必须按顺序访问的城市序列。Bob 可以为一次旅行购买多张联票，但他总是希望对每次旅行花费最少。如果使用一张联票时经过了旅行序列中的下一个城市，就视为访问了该城市（可以跳过不需要的城市）。求每次旅行的最小花费及所使用的联票方案。

**输入格式**：多组数据。第一行 `NT`（联票数），接下来 `NT` 行每行：价格 `cost`、城市数 `len`、`len` 个城市编号。然后 `NI`（旅行数），接下来 `NI` 组：每行城市数 `len`、`len` 个城市编号。`NT ≤ 20`，城市数总计 ≤ 4000。**输出格式**：对每次旅行，输出 `Case X, Trip Y: Cost = Z` 及使用的联票列表。

### 解题思路
**状态图上的最短路**：本题需要在已访问的城市和当前所在城市这两个维度上建立状态空间。

**状态定义**：`ID(visited, cur)` 表示已经访问了旅行序列的前 `visited` 个城市（第 `visited` 个是最后一个已访问的），当前位于城市 `cur`。

**状态转移**：对于每张联票 `ticket`（价格 `cost`）和每个状态 `(visited, cur)`：
- 从联票的第 1 个城市开始使用（必须是当前所在的城市 `cur`）。
- 依次遍历联票的后续航段，如果经过旅行序列中的下一个城市，则 `visited` 递增。
- 每使用一段联票，可以到达一个新的状态：`(visited', cities[ticket][leg])`，代价为联票价格。

**Dijkstra 最短路**：由于每条边的代价是联票价格（正数），使用 Dijkstra 求从 `(1, iti[0])` 到 `(len, iti[len-1])` 的最短路。

### 算法方法
- **Dijkstra 最短路算法**：带权最短路径，使用优先队列优化。

### 复杂度分析
- **时间复杂度**：`O(NT × len × leg × log(States))`。每次旅行需要构造状态图并跑 Dijkstra。状态数 ≈ `len × n_cities`，每条联票可产生最多 O(leg) 条转移边。
- **空间复杂度**：`O(len × n_cities + NT × max(leg))`。

```cpp
// 例题18  低价空中旅行（Low Cost Air Travel, World Finals 2006, LA3561/UVa1048）
// 解题思路：状态图建模——状态(已访问城市数,当前城市)→Dijkstra最短路
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<queue>
#include<algorithm>
using namespace std;

const int INF = 1000000000;
const int maxn = 4000 + 10;

struct Edge {
  int from, to, dist, val;  // dist:价格(边权), val:联票编号
};

struct HeapNode {
  int d, u;
  bool operator < (const HeapNode& rhs) const {
    return d > rhs.d;       // 小顶堆
  }
};

struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[maxn];
  bool done[maxn];    // 永久标号标记
  int d[maxn];        // 最短距离
  int p[maxn];        // 最短路树中的父边

  void init(int n) {
    this->n = n;
    for(int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int dist, int val) {
    edges.push_back((Edge){from, to, dist, val});
    m = edges.size();
    G[from].push_back(m-1);  // 记录边在edges中的索引
  }

  void dijkstra(int s) {
    priority_queue<HeapNode> Q;
    for(int i = 0; i < n; i++) d[i] = INF;
    d[s] = 0;
    memset(done, 0, sizeof(done));
    Q.push((HeapNode){0, s});
    while(!Q.empty()) {
      HeapNode x = Q.top(); Q.pop();
      int u = x.u;
      if(done[u]) continue;              // 已永久标号，跳过
      done[u] = true;
      for(int i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if(d[e.to] > d[u] + e.dist) {    // 松弛操作
          d[e.to] = d[u] + e.dist;
          p[e.to] = G[u][i];              // 记录前驱边
          Q.push((HeapNode){d[e.to], e.to});
        }
      }
    }
  }

  vector<int> GetShortestPath(int s, int t) {
    vector<int> path;
    while(t != s) {
      path.push_back(edges[p[t]].val);   // 回溯收集联票编号
      t = edges[p[t]].from;
    }
    reverse(path.begin(), path.end());
    return path;
  }
};

//////// 题目相关
#include<map>

int n_cities;
map<int,int> city_id;

int ID(int city) {
  if(city_id.count(city)) return city_id[city];
  city_id[city] = n_cities++;
  return n_cities-1;
}

// 状态编号：ID(visited, cur) = (visited-1) * n_cities + cur
int ID(int visited, int cur) { return (visited-1) * n_cities + cur; }

const int maxnt = 100;
int cost[maxnt];                  // cost[ticket]: 联票价格
vector<int> cities[maxnt], iti;   // cities[t]: 联票t经过的城市, iti: 旅行路线

Dijkstra solver;

int main() {
  int NT, NI, x, len, kase = 0;
  while(scanf("%d", &NT) == 1 && NT) {
    n_cities = 0;
    city_id.clear();
    for(int i = 0; i < NT; i++) {
      cities[i].clear();
      scanf("%d%d", &cost[i], &len);
      while(len--) { scanf("%d", &x); cities[i].push_back(ID(x)); } // 读联票
    }
    scanf("%d", &NI);
    kase++;
    for(int trip = 1; trip <= NI; trip++) {
      iti.clear();
      scanf("%d", &len);
      for(int i = 0; i < len; i++) { scanf("%d", &x); iti.push_back(ID(x)); } // 读旅行路线

      solver.init(n_cities * len);
      // 对每张联票和每个已访问城市数，构造状态转移
      for(int ticket = 0; ticket < NT; ticket++)
        for(int visited = 1; visited < len; visited++) {
          int cur = cities[ticket][0];       // 当前状态: (visited, cur)
          int next = visited;                // 下一个需要访问的城市在iti中的下标
          for(int leg = 1; leg < cities[ticket].size(); leg++) {
            if(cities[ticket][leg] == iti[next]) next++; // 经过了旅程中的下一个城市
            solver.AddEdge(ID(visited, cur), ID(next, cities[ticket][leg]),
                          cost[ticket], ticket+1);       // 添加转移边：使用联票ticket
            if(next == len) break;                       // 旅行已完成
          }
        }
      int src = ID(1, iti[0]), dest = ID(len, iti[len-1]); // 起点和终点状态
      solver.dijkstra(src);
      printf("Case %d, Trip %d: Cost = %d\n", kase, trip, solver.d[dest]);
      printf("  Tickets used:");
      vector<int> path = solver.GetShortestPath(src, dest); // 回溯路径
      for(int i = 0; i < path.size(); i++) printf(" %d", path[i]);
      printf("\n");
    }
  }
  return 0;
}
// 25878128	1048	Low Cost Air Travel	Accepted	C++	0.000	2020-12-23 08:11:36
```

## 例题19  动物园大逃亡（Animal Run, 北京 2006, UVa1376 LA 3661）

### 题目描述
有一个 `n × m` 的网格，动物要从左下角逃到右上角。网格中每个小方格被一条对角线分为两个三角形（左下和右上）。相邻三角形之间有边界（上下、左右、对角），每个边界通过需要消耗一定的代价（动物的体力）。求从最左下角到最右上角的最小消耗。

**输入格式**：多组数据。每组数据第一行 `n m`。接下来读入网格边的代价（横线、竖线、斜线各 `(n-1)*(m-1)` 左右的量）。n=m=0 时结束。**输出格式**：对每组数据输出 `Case X: Minimum = Y`。

### 解题思路
**对偶图 + Dijkstra 最短路**：该问题的本质是在一个平面网格图上求 s-t 最小割的容量。根据 **平面图最小割定理**，最小割等于对偶图上的最短路。每个被对角线分割的三角形作为对偶图的一个顶点，相邻三角形之间的边界作为边（权值为原消耗代价），求从下/左边界到上/右边界的对偶图最短路即可。

**图建模**：
- 将每个格子的两个三角形编号为 `half=0`（左下）和 `half=1`（右上）。
- `ID(r, c, half)` 返回三角形 `(r,c,half)` 的结点编号。
- 相邻三角形之间的穿过代价作为对偶图中的边权。

**建边细节**：
- 左下三角形（half=0）：可向左边三角形、下方三角形、本格右上三角形连边。
- 右上三角形（half=1）：可向右边三角形、上方三角形、本格左下三角形连边。
- 添加超级源点 0 连接左/下边界，超级汇点 `2*n*m+1` 连接右/上边界。

在构造的对偶图上运行 Dijkstra 求源点到汇点的最短路。

### 算法方法
- **对偶图转化（Planar Graph Dual）**：平面图的最小割转化为对偶图的最短路。
- **Dijkstra 最短路**：优先队列优化的 Dijkstra 算法。

### 复杂度分析
- **时间复杂度**：`O(nm log(nm))`。对偶图的顶点数 `O(nm)`，边数 `O(nm)`。Dijkstra 在优先队列下的复杂度。
- **空间复杂度**：`O(nm)`。存储对偶图的邻接表。

```cpp
// 例题19  动物园大逃亡（Animal Run, 北京 2006, UVa1376 LA 3661）
// 解题思路：平面图最小割→对偶图最短路。每个三角形=对偶图顶点，最小割容量=最短路长度
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<queue>
#include<algorithm>
using namespace std;

const int INF = 1000000000;
const int maxn = 2000000 + 10;

struct Edge {
  int from, to, dist;
};

struct HeapNode {
  int d, u;
  bool operator < (const HeapNode& rhs) const {
    return d > rhs.d;       // 小顶堆
  }
};

struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[maxn];
  bool done[maxn];    // 永久标号标记
  int d[maxn];        // 最短距离
  int p[maxn];        // 前驱边

  void init(int n) {
    this->n = n;
    for(int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int dist) {
    edges.push_back((Edge){from, to, dist});
    m = edges.size();
    G[from].push_back(m-1);
  }

  void dijkstra(int s) {
    priority_queue<HeapNode> Q;
    for(int i = 0; i < n; i++) d[i] = INF;
    d[s] = 0;
    memset(done, 0, sizeof(done));
    Q.push((HeapNode){0, s});
    while(!Q.empty()) {
      HeapNode x = Q.top(); Q.pop();
      int u = x.u;
      if(done[u]) continue;
      done[u] = true;
      for(int i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if(d[e.to] > d[u] + e.dist) {
          d[e.to] = d[u] + e.dist;
          p[e.to] = G[u][i];
          Q.push((HeapNode){d[e.to], e.to});
        }
      }
    }
  }
};

//////// 题目相关
#define REP(i,n) for(int i = 0; i < (n); ++i)

int n, m;
// 对偶图结点编号：half=0为左下三角形, half=1为右上三角形
int ID(int r, int c, int half) { return half * n * m + r * m + c + 1; }

const int maxsize = 1000;
int cost[maxsize][maxsize][3];  // cost[][][0]:横线, [1]:竖线, [2]:斜线

Dijkstra solver;

int main() {
  int kase = 0;
  while(scanf("%d%d", &n, &m) == 2 && n && m) {
    REP(i,n) REP(j,m-1) scanf("%d", &cost[i][j][0]); // 读入横线代价
    REP(i,n-1) REP(j,m) scanf("%d", &cost[i][j][1]); // 读入竖线代价
    REP(i,n-1) REP(j,m-1) scanf("%d", &cost[i][j][2]); // 读入斜线代价
    solver.init(2*n*m+2);  // 初始化对偶图

    // 对偶图内部建边：左下三角形和右上三角形之间
    REP(i,n-1) REP(j,m-1) {
      // 左下三角形 (half=0)
      int id1 = ID(i, j, 0);
      if(j > 0) solver.AddEdge(id1, ID(i, j-1, 1), cost[i][j][1]);    // 连左边
      if(i < n-1) solver.AddEdge(id1, ID(i+1, j, 1), cost[i+1][j][0]); // 连下边

      // 右上三角形 (half=1)
      int id2 = ID(i, j, 1);
      if(j < m-1) solver.AddEdge(id2, ID(i, j+1, 0), cost[i][j+1][1]); // 连右边
      if(i > 0) solver.AddEdge(id2, ID(i-1, j, 0), cost[i][j][0]);      // 连上边

      solver.AddEdge(id1, id2, cost[i][j][2]);  // 左下→右上（斜线双向）
      solver.AddEdge(id2, id1, cost[i][j][2]);  // 右上→左下
    }

    // 超级源点0连向左/下边界
    REP(i, n-1) solver.AddEdge(0, ID(i, 0, 0), cost[i][0][1]);       // 左边界
    REP(i, m-1) solver.AddEdge(0, ID(n-2, i, 0), cost[n-1][i][0]);   // 下边界

    // 右/上边界连向超级汇点
    REP(i, n-1) solver.AddEdge(ID(i, m-2, 1), 2*n*m+1, cost[i][m-1][1]); // 右边界
    REP(i, m-1) solver.AddEdge(ID(0, i, 1), 2*n*m+1, cost[0][i][0]);     // 上边界

    solver.dijkstra(0);  // 在构造好的对偶图上求最短路
    printf("Case %d: Minimum = %d\n", ++kase, solver.d[2*n*m+1]); // 输出最小割=最短路
  }
  return 0;
}
// 25878139	1376	Animal Run	Accepted	C++	1.110	2020-12-23 08:13:32
```

## 例题13  战争和物流（Warfare and Logistics, LA4080/UVa1416）

### 题目描述
给定一个 `N` 个城市 `M` 条边的无向图，每条边有一个传输代价。如果城市之间不连通，则代价为 `L`（人为设定的大值）。定义 `C(s,t)` 为从 `s` 到 `t` 的最短路径代价。现在有一个敌人可以破坏一条边（即删除一条边）。你需要计算：
1. 原始网络中所有起点-终点对的最短路径代价之和 `c`。
2. 敌人删除某条边后，新的最短路径代价之和的最大值 `c2`（即敌人选择删除哪条边能使总代价最大）。

`N ≤ 100`, `M ≤ 1000`, `L ≤ 10^8`。

**输入格式**：多组数据，每组第一行 `N M L`，接下来 `M` 行每行三个整数 `a b s`（城市编号和边权）。**输出格式**：对每组数据输出 `c c2`。

### 解题思路
**Dijkstra + 最短路径树分析**：原始 `c` 的计算很直接——以每个点为源点跑一次 Dijkstra，累加所有 `d[i]`（用 `L` 代替 `INF`）。关键是计算 `c2`。

**删除边的枚举优化**：暴力枚举每条边、每次重新计算所有源点的 Dijkstra 是 `O(M × N × (M + N log N))`，不可行。但注意到：对于给定的源点 `src`，最短路径树（Shortest Path Tree）中只有 `N-1` 条边。不在最短路径树中的边被删除时，根本不改变任何最短路径！只有删除在最短路径树中的边才需要重新计算。

**算法步骤**：
1. 预处理：以每个点为源点跑 Dijkstra，记录最短路径树（标记哪些边在树中 `used[src][a][b]`），并计算 `sum_single[src]`。
2. 计算原始 `c = Σ sum_single[src]`。
3. 枚举每对 `(i,j)`（每条原始边），删除该边后：
   - 如果对于某个源点 `src`，该边不在 `src` 的最短路径树中，则贡献 `sum_single[src]`。
   - 如果在，则需要对 `src` 重新跑一次 Dijkstra。
4. 取所有删除情况中的最大值作为 `c2`。

注意原图可能有多重边，取最短的前两条做备选。

### 算法方法
- **Dijkstra 最短路**：优先队列优化版本。
- **最短路径树（SPT）**：标记每条边是否属于某个源点的最短路径树。

### 复杂度分析
- **时间复杂度**：`O(N × (M log N) + M × N × (M log N))`。最坏情况每条边都在某个最短路径树中，但实际上 SPT 树边只有 N-1 条，大部分边不在树中。实际运行中 `O(N·M log N + N²·M)`。
- **空间复杂度**：`O(N³ + M)`。存储 `used[N][N][N]` 的布尔标记。

```cpp
// 例题13  战争和物流（Warfare and Logistics, LA4080/UVa1416）
// 解题思路：Dijkstra+最短路径树(SPT)——优化删除边枚举，只在删除SPT中边时重算
// 陈锋
#include<cstdio>
#include<cstring>
#include<vector>
#include<algorithm>
#include<queue>
using namespace std;

const int INF = 1e9, NN = 100 + 8;
struct Edge { int from, to, dist; };
struct HeapNode {
  int d, u;
  bool operator < (const HeapNode& rhs) const {
    return d > rhs.d;       // 小顶堆
  }
};

template<size_t SZ>
struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[SZ];
  bool done[SZ];    // 已永久标号
  int d[SZ];        // 最短距离
  int p[SZ];        // 前驱边

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int dist) {
    edges.push_back((Edge) {from, to, dist});
    m = edges.size();
    G[from].push_back(m - 1);
  }

  void dijkstra(int s) {
    priority_queue<HeapNode> Q;
    for (int i = 0; i < n; i++) d[i] = INF;
    d[s] = 0;
    memset(done, 0, sizeof(done));
    Q.push((HeapNode) {0, s});
    while (!Q.empty()) {
      HeapNode x = Q.top(); Q.pop();
      int u = x.u;
      if (done[u]) continue;
      done[u] = true;
      for (size_t i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        // dist=-1的边已被"删除"，跳过
        if (e.dist > 0 && d[e.to] > d[u] + e.dist) {
          d[e.to] = d[u] + e.dist;
          p[e.to] = G[u][i];
          Q.push((HeapNode) {d[e.to], e.to});
        }
      }
    }
  }
};

Dijkstra<NN> solver;
int N, M, L;
vector<int> gr[NN][NN];    // 两点之间的所有原始边权（处理重边）
int used[NN][NN][NN];      // used[src][a][b]=1 表示src的最短路径树包含边a→b
int idx[NN][NN];           // idx[u][v] 为边u→v在solver中的编号
int sum_single[NN];        // sum_single[src]: 源点为src的最短路树的总代价

// 计算原始网络的c值
int compute_c() {
  int ans = 0;
  memset(used, 0, sizeof(used));
  for (int src = 0; src < N; src++) {
    solver.dijkstra(src);
    sum_single[src] = 0;
    for (int i = 0; i < N; i++) {
      if (i != src) {
        int fa = solver.edges[solver.p[i]].from;    // i在SPT上的父结点
        used[src][fa][i] = used[src][i][fa] = 1;     // 标记SPT边
      }
      sum_single[src] += (solver.d[i] == INF ? L : solver.d[i]); // 不连通用L代替
    }
    ans += sum_single[src];
  }
  return ans;
}

// 计算删除边(a,b)后的总代价
int compute_newc(int a, int b) {
  int ans = 0;
  for (int src = 0; src < N; src++)
    if (!used[src][a][b]) ans += sum_single[src];  // 不在SPT中，无需重算
    else {
      solver.dijkstra(src);                         // 在SPT中，重新计算
      for (int i = 0; i < N; i++)
        ans += (solver.d[i] == INF ? L : solver.d[i]);
    }
  return ans;
}

int main() {
  while (scanf("%d%d%d", &N, &M, &L) == 3) {
    solver.init(N);
    for (int i = 0; i < N; i++)
      for (int j = 0; j < N; j++) gr[i][j].clear();

    for (int i = 0, a, b, s; i < M; i++) {
      scanf("%d%d%d", &a, &b, &s), a--, b--;
      gr[a][b].push_back(s), gr[b][a].push_back(s);  // 处理重边
    }

    // 构造初始网络：取最小的边权
    for (int i = 0; i < N; i++)
      for (int j = i + 1; j < N; j++) if (!gr[i][j].empty()) {
          sort(gr[i][j].begin(), gr[i][j].end());     // 排序，取最小
          solver.AddEdge(i, j, gr[i][j][0]);
          idx[i][j] = solver.m - 1;                    // 记录边编号
          solver.AddEdge(j, i, gr[i][j][0]);
          idx[j][i] = solver.m - 1;
        }

    int c = compute_c(), c2 = -1;
    for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++)
        if (!gr[i][j].empty()) {
          int& e1 = solver.edges[idx[i][j]].dist;
          int& e2 = solver.edges[idx[j][i]].dist;
          // 模拟删除这条边：若有多重边则用次短边替代，否则用-1标记"删除"
          if (gr[i][j].size() == 1) e1 = e2 = -1;
          else e1 = e2 = gr[i][j][1];  // 用次短边
          c2 = max(c2, compute_newc(i, j));
          e1 = e2 = gr[i][j][0];       // 恢复
        }

    printf("%d %d\n", c, c2);
  }
  return 0;
}
// Accepted 230ms 3538 C++ 5.3.0 2020-12-14 17:00:37 25846446
```

## 例题17  蒸汽式压路机（Steam Roller, LA 4128/UVa1078）

### 题目描述
一辆蒸汽压路机在一个 `R × C` 的网格道路上行驶，每条边有一个通过代价。压路机有两种状态：行驶中（沿着某个方向）或停止（停在十字路口可以改变方向）。从行驶到停止或从停止重新出发都需要付出额外的代价（等于边的代价）。起点和终点都是停止状态。求从起点到终点的最小代价。`R, C ≤ 100`。

**输入格式**：多组数据。每组数据第一行 `R C r1 c1 r2 c2`（起终点坐标），然后读入竖向和横向边的权值。`R=0` 时结束。**输出格式**：对每组数据输出 `Case X: Y`，如果不可达输出 `Impossible`。

### 解题思路
**状态图上的 Dijkstra**：压路机不能原地转方向（只能在路口停止后重新选择方向），因此状态需要同时包含位置和方向。

**状态定义**：`ID(r, c, dir)`，其中 `dir` 可以取 0~3（四个方向）或 4（停止状态）。

**状态转移**：
1. 从行驶状态 `(r,c,dir)`：
   - 可以停下来（到 `(r,c,4)`），代价 = 进入格子的边权。
   - 可以继续向前走（到 `(r+dr[dir], c+dc[dir], dir)`），代价 = 当前边的权值。
2. 从停止状态 `(r,c,4)`：
   - 可以选择任一方向出发（到 `(r+dr[dir], c+dc[dir], dir)`），代价 = 边权 × 2（出发+通过）。
   - 也可以只走一步就停下（到 `(r+dr[dir], c+dc[dir], 4)`），代价 = 边权 × 2。

**Dijkstra 最短路**：状态图是一个带正权边的有向图，使用 Dijkstra 求从源点（停止在起点）到终点（停止在终点）的最短路。

### 算法方法
- **状态图建模 + Dijkstra 最短路**：将行驶方向和停止状态编码为图中的不同顶点。

### 复杂度分析
- **时间复杂度**：`O(RC × log(RC))`。状态数 `5RC`，每个状态最多 4 条出边。
- **空间复杂度**：`O(RC)`。

```cpp
// 例题17  蒸汽式压路机（Steam Roller, LA 4128/UVa1078）
// 解题思路：状态图Dijkstra——状态(r,c,dir/停止), 前进/停下/重新出发各有不同代价
// 刘汝佳
#include <cstdio>
#include <cstring>
#include <iostream>
#include <queue>
using namespace std;
const int INF = 1e9, maxn = 50000 + 10;
struct Edge {
  int from, to, dist;
};
struct HeapNode {
  int d, u;
  bool operator<(const HeapNode& rhs) const { return d > rhs.d; }
};
struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[maxn];
  bool done[maxn];  // 永久标号
  int d[maxn];      // 最短距离
  int p[maxn];      // 前驱边

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int dist) {
    edges.push_back((Edge){from, to, dist});
    m = edges.size();
    G[from].push_back(m - 1);
  }

  void dijkstra(int s) {
    priority_queue<HeapNode> Q;
    for (int i = 0; i < n; i++) d[i] = INF;
    d[s] = 0;
    memset(done, 0, sizeof(done));
    Q.push((HeapNode){0, s});
    while (!Q.empty()) {
      HeapNode x = Q.top();
      Q.pop();
      int u = x.u;
      if (done[u]) continue;
      done[u] = true;
      for (int i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if (d[e.to] > d[u] + e.dist) {
          d[e.to] = d[u] + e.dist, p[e.to] = G[u][i];
          Q.push((HeapNode){d[e.to], e.to});
        }
      }
    }
  }
};

//////// 题目相关

const int UP = 0, LEFT = 1, DOWN = 2, RIGHT = 3;  // 方向编码
const int inv[] = {2, 3, 0, 1};                    // 反方向：上↔下, 左↔右
const int dr[] = {-1, 0, 1, 0};                    // 方向偏移：上左下右
const int dc[] = {0, -1, 0, 1};
const int maxr = 100, maxc = 100;
int grid[maxr][maxc][4];  // grid[r][c][dir]: 从(r,c)向dir方向走的边权
int n, id[maxr][maxc][5]; // id[r][c][dir]: 状态(r,c,dir)的结点编号, dir=4表示停止
int R, C;

// 获取或分配结点编号（从1开始）
int ID(int r, int c, int dir) {
  int& x = id[r][c][dir];
  if (x == 0) x = ++n;
  return x;
}
bool cango(int r, int c, int dir) {
  if (r < 0 || r >= R || c < 0 || c >= C) return false; // 越界
  return grid[r][c][dir] > 0;                            // 此方向有路
}

Dijkstra solver;

int main() {
  int r1, c1, r2, c2, kase = 0;
  while (cin >> R >> C >> r1 >> c1 >> r2 >> c2 && R) {
    r1--, c1--, r2--, c2--;
    // 读入边权（输入格式：先水平线后竖线）
    for (int r = 0; r < R; r++) {
      for (int c = 0; c < C - 1; c++) {
        cin >> grid[r][c + 1][LEFT];
        grid[r][c][RIGHT] = grid[r][c + 1][LEFT];  // 两个方向共线
      }
      if (r != R - 1)
        for (int c = 0; c < C; c++) {
          cin >> grid[r + 1][c][UP];
          grid[r][c][DOWN] = grid[r + 1][c][UP];    // 两个方向共线
        }
    }
    solver.init(R * C * 5 + 1);
    n = 0, memset(id, 0, sizeof(id));

    // 源点出发：可以选择任意方向
    for (int dir = 0; dir < 4; dir++)
      if (cango(r1, c1, dir)) {
        solver.AddEdge(0, ID(r1 + dr[dir], c1 + dc[dir], dir),
                       grid[r1][c1][dir] * 2);  // 开始走：代价×2
        solver.AddEdge(0, ID(r1 + dr[dir], c1 + dc[dir], 4),
                       grid[r1][c1][dir] * 2);  // 走一步就停：代价×2
      }

    // 计算每个状态的后继状态
    for (int r = 0; r < R; r++)
      for (int c = 0; c < C; c++) {
        // 从行驶状态出发的转移
        for (int dir = 0; dir < 4; dir++)
          if (cango(r, c, inv[dir])) {   // 能到达(r,c)（即能从反方向进入）
            // 停下来
            solver.AddEdge(ID(r, c, dir), ID(r, c, 4),
                           grid[r][c][inv[dir]]);
            // 继续直行
            if (cango(r, c, dir))
              solver.AddEdge(ID(r, c, dir), ID(r + dr[dir], c + dc[dir], dir),
                             grid[r][c][dir]);
          }
        // 从停止状态出发的转移
        for (int dir = 0; dir < 4; dir++)
          if (cango(r, c, dir)) {
            // 重新开始走：代价×2
            solver.AddEdge(ID(r, c, 4), ID(r + dr[dir], c + dc[dir], dir),
                           grid[r][c][dir] * 2);
            // 走一步停下：代价×2
            solver.AddEdge(ID(r, c, 4), ID(r + dr[dir], c + dc[dir], 4),
                           grid[r][c][dir] * 2);
          }
      }

    solver.dijkstra(0);
    int ans = solver.d[ID(r2, c2, 4)];  // 终点必须是停止状态
    printf("Case %d: ", ++kase);
    if (ans == INF) printf("Impossible\n");
    else printf("%d\n", ans);
  }
  return 0;
}
// 25878161	1078	Steam Roller	Accepted	C++	0.070	2020-12-23 08:17:38
```
// 例题17  蒸汽式压路机（Steam Roller, LA 4128/UVa1078）
// 刘汝佳
#include <cstdio>
#include <cstring>
#include <iostream>
#include <queue>
using namespace std;
const int INF = 1e9, maxn = 50000 + 10;
struct Edge {
  int from, to, dist;
};
struct HeapNode {
  int d, u;
  bool operator<(const HeapNode& rhs) const { return d > rhs.d; }
};
struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[maxn];
  bool done[maxn];  // 是否已永久标号
  int d[maxn];      // s到各个点的距离
  int p[maxn];      // 最短路中的上一条弧

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int dist) {
    edges.push_back((Edge){from, to, dist});
    m = edges.size();
    G[from].push_back(m - 1);
  }

  void dijkstra(int s) {
    priority_queue<HeapNode> Q;
    for (int i = 0; i < n; i++) d[i] = INF;
    d[s] = 0;
    memset(done, 0, sizeof(done));
    Q.push((HeapNode){0, s});
    while (!Q.empty()) {
      HeapNode x = Q.top();
      Q.pop();
      int u = x.u;
      if (done[u]) continue;
      done[u] = true;
      for (int i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if (d[e.to] > d[u] + e.dist) {
          d[e.to] = d[u] + e.dist, p[e.to] = G[u][i];
          Q.push((HeapNode){d[e.to], e.to});
        }
      }
    }
  }
};

//////// 题目相关

const int UP = 0, LEFT = 1, DOWN = 2, RIGHT = 3;

const int inv[] = {2, 3, 0, 1};
const int dr[] = {-1, 0, 1, 0};  // 上左下右
const int dc[] = {0, -1, 0, 1};
const int maxr = 100, maxc = 100;
int grid[maxr][maxc][4], n, id[maxr][maxc][5], R, C;
int ID(int r, int c, int dir) {
  int& x = id[r][c][dir];
  if (x == 0) x = ++n;  // 从1开始编号
  return x;
}
bool cango(int r, int c, int dir) {
  if (r < 0 || r >= R || c < 0 || c >= C) return false;  // 走出网格
  return grid[r][c][dir] > 0;                            // 此路不通？
}

Dijkstra solver;

int main() {
  int r1, c1, r2, c2, kase = 0;
  while (cin >> R >> C >> r1 >> c1 >> r2 >> c2 && R) {
    r1--, c1--, r2--, c2--;
    for (int r = 0; r < R; r++) {
      for (int c = 0; c < C - 1; c++) {
        cin >> grid[r][c + 1][LEFT];
        grid[r][c][RIGHT] = grid[r][c + 1][LEFT];
      }
      if (r != R - 1)
        for (int c = 0; c < C; c++) {
          cin >> grid[r + 1][c][UP];
          grid[r][c][DOWN] = grid[r + 1][c][UP];
        }
    }
    solver.init(R * C * 5 + 1);
    n = 0, memset(id, 0, sizeof(id));
    // 源点出发的边
    for (int dir = 0; dir < 4; dir++)
      if (cango(r1, c1, dir)) {
        solver.AddEdge(0, ID(r1 + dr[dir], c1 + dc[dir], dir),
                       grid[r1][c1][dir] * 2);  // 开始走下去
        solver.AddEdge(0, ID(r1 + dr[dir], c1 + dc[dir], 4),
                       grid[r1][c1][dir] * 2);  // 走一步停下来
      }

    // 计算每个状态(r,c,dir)的后继状态
    for (int r = 0; r < R; r++)
      for (int c = 0; c < C; c++) {
        for (int dir = 0; dir < 4; dir++)
          if (cango(r, c, inv[dir])) {
            solver.AddEdge(ID(r, c, dir), ID(r, c, 4),
                           grid[r][c][inv[dir]]);  // 停下来！
            if (cango(r, c, dir))
              solver.AddEdge(ID(r, c, dir), ID(r + dr[dir], c + dc[dir], dir),
                             grid[r][c][dir]);  // 继续走
          }
        for (int dir = 0; dir < 4; dir++)
          if (cango(r, c, dir)) {
            solver.AddEdge(ID(r, c, 4), ID(r + dr[dir], c + dc[dir], dir),
                           grid[r][c][dir] * 2);  // 重新开始走
            solver.AddEdge(ID(r, c, 4), ID(r + dr[dir], c + dc[dir], 4),
                           grid[r][c][dir] * 2);  // 走一步停下来
          }
      }

    solver.dijkstra(0);
    int ans = solver.d[ID(r2, c2, 4)];  // 找最优解
    printf("Case %d: ", ++kase);
    if (ans == INF)
      printf("Impossible\n");
    else
      printf("%d\n", ans);
  }
  return 0;
}
// 25878161	1078	Steam Roller	Accepted	C++	0.070	2020-12-23 08:17:38
```

## 例题14  过路费（加强版）（The Toll! Revisited, UVa 10537）

### 题目描述
有一个国家，共有 52 个城市（26 个大写字母城镇 + 26 个小写字母村子）。道路连接在部分城市之间，形成一个无向图。旅行者每经过一个村子需要上交 1 个单位的货物作为过路费；每经过一个城镇需要上交当前所持货物的 1/20（向上取整）。给定起点和终点，以及你需要最终携带 `P` 个单位的货物到达终点，问你从起点最少需要携带多少货物（以保证路上交完过路费后还能剩 P 个）。

**输入格式**：多组数据。每组数据第一行 `N`（道路数，-1 结束）。接下来 `N` 行每行两个字符表示道路连接的城市。然后一行整数 `P`，再一行两个字符 `S E`（起点终点）。**输出格式**：对每组数据输出最少初始货物数以及具体路径。

### 解题思路
**逆向 Dijkstra**：从终点出发，逆向推导每个城市需要的最少货物数。

**状态定义**：`D[u]` 表示从城市 `u` 出发（已经交过 `u` 的税）时，至少要带多少货物才能保证最终到达终点时还剩 `P`。

**递推公式**：
- 如果是村子（小写字母）：交税后剩 `k-1`，即 `forward(k, u) = k-1`。反向推导：`back(u) = D[u] + 1`。
- 如果是城镇（大写字母）：交税后剩 `k - ceil(k/20)`，即 `forward(k, u) = k - (k+19)/20`。反向推导：从 `D[u]` 反推初始 k，公式为 `k = D[u] * 20 / 19`，然后微调直到满足 `forward(k, u) >= D[u]`。

**Dijkstra 过程**：从终点开始，初始 `D[Ed] = P`。然后反复选择未访问的 `D[u]` 最小的城市 `u`，标记已访问，并更新其所有邻居。

**路径输出**：从起点沿着 `D` 值最小的路线走（贪心选择能到达且满足 `forward(k, next) >= D[next]` 的最小字典序的下一个城市）。

### 算法方法
- **逆向 Dijkstra**：从终点向起点方向推导最少初始货物数。使用类似 Dijkstra 的贪心标记策略。

### 复杂度分析
- **时间复杂度**：`O(V²)`。52 个顶点，每次选最小 D 需要 O(V)，共 V 轮。
- **空间复杂度**：`O(V²)`。邻接矩阵存储 52×52 的道路网络。

```cpp
// 例题14  过路费（加强版）（The Toll! Revisited, UVa 10537）
// 解题思路：逆向Dijkstra——从终点出发，反向推导每个城市所需的最少初始货物
// 陈锋
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<cctype>
using namespace std;

const int NN = 52 + 10;
const long long INF = 1LL << 60;
typedef long long LL;

int N, G[NN][NN], St, Ed, P, Vis[NN]; // G:道路邻接矩阵, Vis:是否已找到D的最优值
LL D[NN];     // D[i]表示从点i出发（已经交过点i的税了）时至少要带多少东西，到Ed时还能剩p个东西

// 读入城市编号：大写字母对应0~25，小写字母对应26~51
int read_node() {
  char s[9];
  scanf("%s", s);
  if (isupper(s[0])) return s[0] - 'A';     // 城镇：下标0-25
  return s[0] - 'a' + 26;                    // 村子：下标26-51
}
char node_label(int u) { return u < 26 ? 'A' + u : 'a' + (u - 26); }

// 正向计算：拿着k个货物来到城市u，交税后还剩多少货物
LL forward(LL k, int u) {
  if (u < 26) return k - (k + 19) / 20;     // 城镇：上交1/20（向上取整）
  return k - 1;                              // 村子：上交1个
}

// 反向计算：到达结点u并交税后需要剩D[u]个货物，则到达前至少需要多少货物
LL back(int u) {
  if (u >= 26) return D[u] + 1;             // 村子：交税1个，所以需要D[u]+1
  LL X = D[u] * 20 / 19;                    // 城镇：粗略估计（税费约1/20）
  while (forward(X, u) < D[u]) X++;         // 微调直到满足
  return X;
}

void solve() {
  N = 52; // 总是有52个结点（26城镇 + 26村子）
  fill_n(Vis, N + 1, 0), fill_n(D, N, INF);
  D[Ed] = P, Vis[Ed] = 1;                   // 终点：到达时还剩P个货物
  // 初始化：与终点相邻的城市，计算到达它们的最少货物数
  for (int i = 0; i < N; i++)
    if (i != Ed && G[i][Ed]) D[i] = back(Ed);

  while (!Vis[St]) {                        // 逆向Dijkstra主过程
    int minu = -1;                          // 找未访问的D值最小的城市
    for (int i = 0; i < N; i++)
      if (!Vis[i] && (minu < 0 || D[i] < D[minu])) minu = i;
    Vis[minu] = 1;                          // 标记为已找到最优值
    for (int i = 0; i < N; i++)
      if (!Vis[i] && G[i][minu]) D[i] = min(D[i], back(minu)); // 尝试更新邻居的D值
  }
  printf("%lld\n%c", D[St], node_label(St)); // 输出最少货物数+起点
  // 按最小字典序输出路径
  LL k = D[St];                             // 当前携带货物数
  for (int u = St, next; u != Ed; u = next) {
    for (next = 0; next < N; next++)        // 贪心找第一个可行的下一个城市
      if (G[u][next] && forward(k, next) >= D[next]) break;
    k = D[next];                            // 更新携带数
    printf("-%c", node_label(next));        // 输出路径
    u = next;
  }
  puts("");
}

int main() {
  for (int kase = 1; scanf("%d", &N) == 1 && N >= 0; kase++) {
    memset(G, 0, sizeof(G));
    for (int i = 0; i < N; i++) {
      int u = read_node(), v = read_node(); // 读入道路
      if (u != v) G[u][v] = G[v][u] = 1;    // 无向图
    }
    scanf("%d", &P);                        // 目标剩余货物
    St = read_node(), Ed = read_node();     // 起点和终点
    printf("Case %d:\n", kase);
    solve();
  }
  return 0;
}
// 25878179	10537	The Toll! Revisited	Accepted	C++	0.000	2020-12-23 08:23:15
```

## 例题12  林中漫步（A Walk Through the Forest, UVa 10917）

### 题目描述
Jimmy 在办公室（编号 1）工作，家在顶点 2。城市中有一些双向道路连接各个地点。Jimmy 下班后希望沿着"越来越接近家"的路线步行回家。具体来说，从当前顶点 `u` 走到下一个顶点 `v` 的前提是：从 `v` 到家的最短距离严格小于从 `u` 到家的最短距离。问 Jimmy 从办公室到家有多少条不同的合法路径。`n ≤ 1000`, `m` 条边。

**输入格式**：多组数据，每组第一行 `n`（顶点数），若 `n=0` 则结束；否则第二行 `m`（边数），接下来 `m` 行每行 `a b c`（无向边和距离）。**输出格式**：对每组数据输出合法路径数量。

### 解题思路
**Dijkstra + DAG 上的 DP**：

**第一步 - 计算到家的距离**：以家（顶点 2，代码中用 1）为源点跑一次 Dijkstra，得到每个顶点到家（+办公室）的最短距离 `solver.d[i]`。

**第二步 - 构建 DAG**：根据"只能往更接近家的方向走"规则，如果从 `u` 到 `v` 有一条边且 `solver.d[v] < solver.d[u]`，则在有向 DAG 中存在一条 `u → v` 的边。

**第三步 - DAG 上 DP 计数**：`dp(u)` 表示从 `u` 到家的路径数量。递推公式：`dp(u) = Σ dp(v)`，其中 `v` 满足 `solver.d[v] < solver.d[u]`。边界：`dp(1) = 1`。

求 `dp(0)`（Jimmy 办公室到家）。

**记忆化搜索**：由于 DAG 中路径是单向的（总是向距离减小的方向），使用递归记忆化搜索即可。

### 算法方法
- **Dijkstra 最短路**：计算从家到所有顶点的最短距离。
- **DAG 上的动态规划**：记忆化搜索统计路径数。

### 复杂度分析
- **时间复杂度**：`O(m log n + m)`。Dijkstra O(m log n)，DP O(m)。
- **空间复杂度**：`O(n + m)`。

```cpp
// 例题12  林中漫步（A Walk Through the Forest, UVa 10917）
// 解题思路：Dijkstra计算到家距离 + DAG上DP统计路径数——只走"越来越近"的路线
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<queue>
using namespace std;

const int INF = 1000000000;
const int maxn = 1000 + 10;

struct Edge {
  int from, to, dist;
};

struct HeapNode {
  int d, u;
  bool operator < (const HeapNode& rhs) const {
    return d > rhs.d;
  }
};

struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[maxn];
  bool done[maxn];    // 是否已永久标号
  int d[maxn];        // s到各个点的距离
  int p[maxn];        // 最短路中的上一条弧

  void init(int n) {
    this->n = n;
    for(int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int dist) {
    edges.push_back((Edge){from, to, dist});
    m = edges.size();
    G[from].push_back(m-1);
  }

  void dijkstra(int s) {
    priority_queue<HeapNode> Q;
    for(int i = 0; i < n; i++) d[i] = INF;
    d[s] = 0;
    memset(done, 0, sizeof(done));
    Q.push((HeapNode){0, s});
    while(!Q.empty()) {
      HeapNode x = Q.top(); Q.pop();
      int u = x.u;
      if(done[u]) continue;
      done[u] = true;
      for(int i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if(d[e.to] > d[u] + e.dist) {
          d[e.to] = d[u] + e.dist;
          p[e.to] = G[u][i];
          Q.push((HeapNode){d[e.to], e.to});
        }
      }
    }
  }
};

//////// 题目相关
Dijkstra solver;
int d[maxn]; // DP记忆化数组：d[u]表示从u到家的合法路径数（也复用了n的范围）

// DP记忆化搜索：从u走到家（顶点1）的合法路径数
int dp(int u) {
  if(u == 1) return 1; // 边界条件：已经到家，只有1种方式（原地不动）

  int& ans = d[u];
  if(ans >= 0) return ans; // 已经计算过，直接返回

  ans = 0;
  for(int i = 0; i < solver.G[u].size(); i++) {
    int v = solver.edges[solver.G[u][i]].to;     // 枚举邻居v
    if(solver.d[v] < solver.d[u]) ans += dp(v);   // 只有更接近家的方向才算
  }
  return ans;
}

int main() {
  int n, m;
  while(scanf("%d%d", &n, &m) == 2) {
    solver.init(n);
    for(int i = 0; i < m; i++) {
      int a, b, c;
      scanf("%d%d%d", &a, &b, &c); a--; b--;
      solver.AddEdge(a, b, c);    // 无向图建两条边
      solver.AddEdge(b, a, c);
    }

    solver.dijkstra(1); // 以家（顶点编号1，即原编号2）为源点求最短路
    memset(d, -1, sizeof(d)); // 初始化DP数组（-1表示未计算）
    printf("%d\n", dp(0));    // 办公室（编号0）到家的路径条数
  }
  return 0;
}
// 25878181	10917	Walk Through the Forest	Accepted	C++	0.010	2020-12-23 08:23:48
```

## 例题15  在环中（Going in Cycle!!, UVa 11090）

### 题目描述
给定一个 `n` 个顶点 `m` 条边的有向带权图，边权为正整数。求图中的一个环（圈），使得环上所有边的平均权值（总权和 / 边数）最小。输出这个最小平均值（保留两位小数）。如果图中不存在环，输出 "No cycle found."。`n ≤ 50`。

**输入格式**：第一行为测试数据组数 `T`。每组数据第一行 `n m`，接下来 `m` 行每行 `u v w`（有向边 u→v 权值 w）。**输出格式**：对每组数据输出 `Case #X: Y`（Y 为最小的平均边权，保留两位小数）或无环的提示。

### 解题思路
**二分答案 + 负环检测**：最小平均环问题可以转化为判定是否存在一个环的平均权值 ≤ x。

**转换原理**：对于猜测的平均值 `x`，将每条边的权值 `w` 修改为 `w - x`。则：
- 原图中存在一个平均权值 ≤ x 的环，等价于新图中存在一个**负权环**（环上权和 < 0）。
- 因为：`Σ(w_i) / k ≤ x` ⇔ `Σ(w_i - x) ≤ 0` ⇔ `Σ(w'_i) ≤ 0`，其中 `w'_i = w_i - x`。

**算法步骤**：
1. 二分查找最小值 `x`，范围 `[0, max_weight+1]`。
2. 对每个 `x`，使用 **Bellman-Ford 算法（SPFA 实现）** 检测图中是否存在负环。
3. 如果存在负环（说明平均权值 ≤ x），则减小 `R`；否则增大 `L`。
4. 如果 `x = max_weight + 1` 时仍无负环，说明原图无环。

**Bellman-Ford 负环检测（SPFA）**：所有顶点入队，初始距离=0。如果一个顶点入队超过 `n` 次，则存在负环。

### 算法方法
- **二分答案（Binary Search）**：枚举最小平均值。
- **Bellman-Ford / SPFA 负环检测**：将边权减去 x 后检测负环。

### 复杂度分析
- **时间复杂度**：`O(log(Range) × (n + m))`。二分约 `log(ub/eps)` ≈ 25 次，每次 SPFA O(n+m)。
- **空间复杂度**：`O(n + m)`。

```cpp
// 例题15  在环中（Going in Cycle!!, UVa 11090）
// 解题思路：二分答案+Bellman-Ford负环检测——最小平均环问题，边权减去x后检测负环
// 陈锋
#include<cstdio>
#include<cstring>
#include<queue>
using namespace std;

const int INF = 1e9, NN = 1000;

struct Edge {
  int from, to;
  double dist;
};

struct BellmanFord {
  int n, m;
  vector<Edge> edges;
  vector<int> G[NN];
  bool inq[NN];     // 是否在队列中
  double d[NN];     // 从起点到各点的距离（SPFA）
  int p[NN];        // 最短路中的前驱边
  int cnt[NN];      // 各顶点的入队次数（用于检测负环）

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, double dist) {
    edges.push_back((Edge) {from, to, dist});
    m = edges.size();
    G[from].push_back(m - 1);
  }

  // SPFA检测负环：所有顶点初始距离=0，同时入队
  bool negativeCycle() {
    queue<int> Q;
    memset(inq, 0, sizeof(inq));
    memset(cnt, 0, sizeof(cnt));
    for (int i = 0; i < n; i++) { d[i] = 0; inq[0] = true; Q.push(i); } // 所有顶点入队

    while (!Q.empty()) {
      int u = Q.front(); Q.pop();
      inq[u] = false;
      for (int i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if (d[e.to] > d[u] + e.dist) {           // 松弛操作
          d[e.to] = d[u] + e.dist;
          p[e.to] = G[u][i];
          if (!inq[e.to]) { Q.push(e.to); inq[e.to] = true;
            if (++cnt[e.to] > n) return true;     // 入队>n次→存在负环
          }
        }
      }
    }
    return false;
  }
};

BellmanFord solver;
// 二分判定：将所有边权减去x后，检测是否存在负环
bool test(double x) {
  for (int i = 0; i < solver.m; i++)
    solver.edges[i].dist -= x;                   // 边权减去x
  bool ret = solver.negativeCycle();             // 检测负环
  for (int i = 0; i < solver.m; i++)
    solver.edges[i].dist += x;                   // 恢复原权值
  return ret;
}

int main() {
  int T; scanf("%d", &T);
  for (int kase = 1, n, m; scanf("%d%d", &n, &m), kase <= T; kase++) {
    solver.init(n);
    int ub = 0;                                  // 记录最大边权作为二分上界
    for (int i = 0, u, v, w; i < m; i++) {
      scanf("%d%d%d", &u, &v, &w), u--, v--, ub = max(ub, w);
      solver.AddEdge(u, v, w);
    }
    printf("Case #%d: ", kase);
    if (!test(ub + 1)) printf("No cycle found.\n"); // ub+1时都没负环→原图无环
    else {
      double L = 0, R = ub;
      while (R - L > 1e-3) {                     // 二分精度1e-3
        double M = L + (R - L) / 2;
        if (test(M)) R = M; else L = M;          // 有负环→平均值可更小
      }
      printf("%.2lf\n", L);                       // 输出保留两位小数
    }
  }
  return 0;
}
// Accepted 50ms 2056 C++11 5.3.0 2020-01-31 17:59:48 24490896
```

## 例题11  机场快线（Airport Express, UVa 11374）

### 题目描述
某城市有 `N` 个火车站和一个机场。有 `M` 条经济特快线路（Economy-Xpress）连接部分车站（无向边带权）。另外有 `K` 条商务特快线路（Business-Xpress），也是无向边带权。Bob 要从起点 `S` 到终点 `E`，Bob 可以乘坐任意段经济特快，但最多只能乘坐一段商务特快。求最短路径以及所使用的商务特快线路（如果有的话）。`N ≤ 500`, `M ≤ 1000`, `K ≤ 1000`。

**输入格式**：多组数据。每组第一行 `N S E`，第二行 `M`，接下来 `M` 行 `u v d`（经济线路），然后一行 `K`，接下来 `K` 行 `u v d`（商务线路）。**输出格式**：对每组数据，第一行输出最短路径上的顶点序列，第二行输出使用的商务线路起点编号（未使用则 "Ticket Not Used"），第三行输出最短距离。

### 解题思路
**双源 Dijkstra**：由于最多使用一段商务特快，一个自然的思路是分别从起点 `S` 和终点 `E` 出发计算到所有点的最短距离。

**算法步骤**：
1. 在经济特快构成的图上，分别以 `S` 和 `E` 为源点跑两次 Dijkstra，得到 `SD.d[i]`（S 到 i 的最短距离）和 `ED.d[i]`（E 到 i 的最短距离）。
2. **不使用商务特快的答案**：`SD.d[E]`。
3. **使用商务特快 `(u, v, d)` 的答案**：`SD.d[u] + d + ED.d[v]` 或 `SD.d[v] + d + ED.d[u]`（取决于方向）。
4. 取所有情况的最小值作为最终答案。

**路径输出**：分别从 `S` 到 `u` 和从 `E` 到 `v` 回溯路径，拼接起来得到完整路径。

### 算法方法
- **双源 Dijkstra**：分别从 S 和 E 运行 Dijkstra，预处理所有点到起点和终点的最短距离。

### 复杂度分析
- **时间复杂度**：`O((M + K) log N)`。两次 Dijkstra O(M log N)，枚举商务线路 O(K)。
- **空间复杂度**：`O(N + M + K)`。

```cpp
// 例题11  机场快线（Airport Express, UVa 11374）
// 解题思路：双源Dijkstra——分别从S和E预计算最短距离，枚举最多一段商务特快
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
struct Edge {
  int u, v, d;
  bool operator<(const Edge& e) const { return d < e.d; }
};

struct HeapNode {
  int u, d;
  bool operator<(const HeapNode& rhs) const { return d > rhs.d; }
};

template <int SZV, int INF>  // |V|
struct Dijkstra {
  int n;
  vector<Edge> edges;
  vector<int> G[SZV];
  bool done[SZV];
  int d[SZV], p[SZV];

  void init(int n) {
    assert(n < SZV);
    this->n = n;
    edges.clear();
    _for(i, 0, n) G[i].clear();
  }

  void addEdge(int u, int v, int d) {  // u-v,d
    G[u].push_back(edges.size()), edges.push_back({u, v, d});
  }

  void dijkstra(int s) {
    priority_queue<HeapNode> Q;
    fill_n(done, n, false), fill_n(d, n, INF);
    d[s] = 0, Q.push({s, 0});
    while (!Q.empty()) {
      HeapNode x = Q.top();
      Q.pop();
      int u = x.u;  // select a node nearest to the current node set
      if (done[u]) continue;
      done[u] = true;

      for (size_t ei = 0; ei < G[u].size(); ei++) {
        const auto& e = edges[G[u][ei]];
        int v = e.v;
        if (d[v] > d[u] + e.d)
          d[v] = d[u] + e.d, p[v] = G[u][ei], Q.push({v, d[v]});
      }
    }
  }

  // path of s->e
  void getPath(int s, int e, deque<int>& path, bool rev = false) {
    assert(d[s] == 0), assert(d[e] != INF);
    int x = e;
    if (rev) path.push_back(x);
    else path.push_front(x);
    while (x != s) {
      x = edges[p[x]].u;
      if (rev) path.push_back(x);
      else path.push_front(x);
    }
  }
};

const int MAXN = 500 + 4, INF = 1e9;
int main() {
  Dijkstra<MAXN, INF> SD, ED;  // SD: 从起点S计算, ED: 从终点E计算（反向）
  for (int t = 0, N, S, E, M, K, u, v, d; scanf("%d%d%d", &N, &S, &E) == 3; t++) {
    if (t) puts("");
    SD.init(N + 1), ED.init(N + 1);
    scanf("%d", &M);
    for (int i = 0; i < M; i++) {  // Economy-Xpress: 读入经济线路
      scanf("%d%d%d", &u, &v, &d);
      SD.addEdge(u, v, d), SD.addEdge(v, u, d);  // 两个求解器都建相同的图
      ED.addEdge(u, v, d), ED.addEdge(v, u, d);
    }
    SD.dijkstra(S), ED.dijkstra(E);              // 分别从S和E跑Dijkstra
    int cu = -1, ans = INF;                      // cu: 使用的商务线路起点
    deque<int> path;
    if (SD.d[E] < ans) ans = SD.d[E], SD.getPath(S, E, path); // 不使用商务特快的方案

    // Lambda: 尝试使用商务特快 S → u → v → E
    auto update = [&](int u, int v, int d) {
      if (SD.d[u] < ans && ED.d[v] < ans && SD.d[u] + d + ED.d[v] < ans) {
        ans = SD.d[u] + d + ED.d[v], cu = u, path.clear();
        SD.getPath(S, u, path), ED.getPath(E, v, path, true); // 拼接路径
      }
    };

    scanf("%d", &K);
    _for(i, 0, K)
      scanf("%d%d%d", &u, &v, &d), update(u, v, d), update(v, u, d); // 双方向尝试
    _for(i, 0, path.size()) {                    // 输出路径
      if (i) printf(" ");
      printf("%d", path[i]);
    }
    puts("");
    if (cu == -1) puts("Ticket Not Used");       // 未使用商务特快
    else printf("%d\n", cu);                     // 使用的商务线路起点
    printf("%d\n", ans);                         // 最短距离
  }
  return 0;
}
// 18869546 11374 Airport Express Accepted C++11 0.000 2017-03-01 03:10:33
```

## 例题16  Halum操作（Halum, UVa 11478）

### 题目描述
在一个有向带权图中，你可以多次执行 "Halum" 操作：选择一个顶点 `v` 和一个整数 `d`，将所有以 `v` 为终点的边的权值增加 `d`，同时将所有以 `v` 为起点的边的权值减少 `d`。问通过若干次 Halum 操作，最小边权最大可以是多少（即最大化图中最小边的权值）。如果最小边权可以任意大，输出 "Infinite"；如果所有操作都无法使每条边 ≥ 1，输出 "No Solution"。`n ≤ 500`, `m ≤ 2700`。

**输入格式**：多组数据，每组第一行 `n m`，接下来 `m` 行每行 `u v d`（有向边 u→v 权值 d）。**输出格式**：对每组数据输出最大可能的最小边权，或 "Infinite"/"No Solution"。

### 解题思路
**差分约束系统 + 二分答案**：Halum 操作的本质是每个顶点的"势能"调整。

**数学建模**：设对顶点 `i` 执行 Halum 操作的总调整量为 `x[i]`（所有操作的 `d` 值之和）。则边 `(u, v, w)` 的新权值变为：`w' = w - x[u] + x[v]`。目标是最大化 `min(w')`。

**二分转化**：假设目标最小值 ≥ `X`，即对所有边 `(u, v, w)`：`w - x[u] + x[v] ≥ X`，整理得：`x[v] - x[u] ≥ X - w`，即 `x[u] - x[v] ≤ w - X`。

这恰好是 **差分约束系统** 的形式：`x[u] ≤ x[v] + (w - X)`（等价于 `v` 到 `u` 有一条权值为 `w - X` 的边）。

**判据**：差分约束系统有解 ⇔ 对应的图中不存在 **负环**。

**特殊情况**：
- 若 `X = max_weight + 1` 时仍有解 → 可无限增大（"Infinite"）。
- 若 `X = 1` 时已无解 → 无法达到要求（"No Solution"）。
- 否则二分查找最大 `X`。

### 算法方法
- **二分答案（Binary Search）**：二分最小边权目标值 X。
- **Bellman-Ford / SPFA 负环检测**：用于判断差分约束系统是否有解。

### 复杂度分析
- **时间复杂度**：`O(log(Range) × (n + m))`。二分约 `log(max_weight)` 次，每次 SPFA O(n+m)。
- **空间复杂度**：`O(n + m)`。

```cpp
// 例题16  Halum操作（Halum, UVa 11478）
// 解题思路：差分约束+二分答案——Halum操作≡顶点势能调整，边权约束转为差分约束
// 陈锋
// 陈锋
#include <cstdio>
#include <cstring>
#include <queue>
using namespace std;

const int INF = 1e9, NN = 500 + 10, MM = 2700 + 10;
struct Edge {
  int to, dist;
};

// 邻接表写法
struct BellmanFord {
  int n, m, head[NN], next[MM];
  Edge edges[MM];
  bool inq[NN];  // 是否在队列中
  int d[NN];     // s到各个点的距离
  int cnt[NN];   // 进队次数

  void init(int n) {
    this->n = n;
    m = 0, memset(head, -1, sizeof(head));
  }

  void AddEdge(int from, int to, int dist) {
    next[m] = head[from], head[from] = m, edges[m++] = (Edge){to, dist};
  }

  bool negativeCycle() {
    queue<int> Q;
    memset(inq, 0, sizeof(inq)), memset(cnt, 0, sizeof(cnt));
    for (int i = 0; i < n; i++) d[i] = 0, Q.push(i);
    while (!Q.empty()) {
      int u = Q.front();
      Q.pop();
      inq[u] = false;
      for (int i = head[u]; i != -1; i = next[i]) {
        Edge& e = edges[i];
        if (d[e.to] > d[u] + e.dist) {
          d[e.to] = d[u] + e.dist;
          if (!inq[e.to]) {
            Q.push(e.to), inq[e.to] = true;
            if (++cnt[e.to] > n) return true;
          }
        }
      }
    }
    return false;
  }
};

BellmanFord solver;

// 判定目标最小边权≥x是否有解：将每条边的权值减去x，检测差分约束系统
// 差分约束: x[v] - x[u] ≤ w - X → 边 v → u 权值为 w - X
// 无负环↔有解
bool test(int x) {
  for (int i = 0; i < solver.m; i++) solver.edges[i].dist -= x;   // 边权减去x
  bool ret = solver.negativeCycle();                                // 检测负环
  for (int i = 0; i < solver.m; i++) solver.edges[i].dist += x;    // 恢复原权值
  return !ret;  // 无负环才是有解（差分约束系统有解↔无负环）
}

int main() {
  for (int n, m; scanf("%d%d", &n, &m) == 2;) {
    solver.init(n);
    int ub = 0;                                     // 最大边权作为二分上界
    for (int i = 0, u, v, d; i < m; i++) {
      scanf("%d%d%d", &u, &v, &d);
      ub = max(ub, d);                              // 更新最大边权
      solver.AddEdge(u - 1, v - 1, d);              // 建差分约束边
    }
    if (test(ub + 1))                               // 如果每条边都能超过最大值→可无限增大
      puts("Infinite");
    else if (!test(1))                              // 如果连≥1都达不到→无解
      puts("No Solution");
    else {
      int L = 2, R = ub, ans = 1;                  // 二分找最大可行值
      while (L <= R) {
        int M = L + (R - L) / 2;
        if (test(M)) ans = M, L = M + 1;            // M可行→尝试更大
        else R = M - 1;                              // M不可行→必须减小
      }
      printf("%d\n", ans);
    }
  }
  return 0;
}
// Accepted 820ms 2089 C++5.3.0 2020-12-1417:56:15 25846657
```
