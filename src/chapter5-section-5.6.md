# 5.6 网络流问题

> **学习目标**：理解残量网络与增广路的核心机制、Dinic 的分层图优化、最小割最大流定理的直观含义，并触达费用流和上下界网络流的构造方法——掌握图论建模的终极工具。

## 理论基础

### 为什么需要学这个？

你有没有过这样的体验：一个题目，你绞尽脑汁想贪心、想 DP、想二分图，都不对，结果一看题解——"跑一个最大流就行了"。那种"我怎么就没想到"的感觉，几乎每个竞赛选手都体会过。网络流在竞赛中的地位很特殊：它不只是一个算法，而是一种**建模语言**——你可以用流来编码"分配"、"匹配"、"选择"、"决策"等几乎所有的组合优化问题。

但网络流的学习门槛也很高。最大流有那么多算法（EK、Dinic、ISAP），你什么时候该用哪个？最小割和最大流是什么关系，怎么用来建模？费用流和上下界又是怎么一回事？这一节就是要帮你串起这条从"基础流"到"带费用、带上下界的通用流"的学习线。

更关键的是，学完网络流之后，你的建模工具箱里会多出一个**万能武器**。很多之前觉得"这也能用图做？"的问题，现在你都能说一句：跑个最大流就行了。

### 核心概念

#### 1. 残量网络与增广路 —— 一切流算法的根基

- **残量网络**：对每条原边 `(u,v,cap)` 创建一条容量为 `cap - flow` 的正向边和一条容量为 `flow` 的反向边。反向边的物理意义是"我可以撤销已经流过去的流量"。
- **增广路**：残量网络中从源点到汇点、所有边容量 > 0 的路径。沿增广路 `P` 推进 `min_cap(P)` 的流量，总流增加。

```
// 给边 (u,v) 添加 cap 的容量时，同时添加反向边
add_edge(u, v, cap);
add_edge(v, u, 0);   // 反向边初始容量为 0
```

> **为什么反向边是网络流的灵魂？** 因为流没有"方向记忆"。假设你从 u 往 v 推了 3 个单位的流，后来发现从 v 往 u 推 2 个单位能让整体更优——残量网络中 `edge(v→u).cap = 3`（当初流的量），你推过去，这两个流就抵消了。反向边让贪心的增广过程具有了**后悔和重选**的能力。

#### 2. Dinic 算法 —— BFS 分层 + DFS 多路增广

Dinic 的两个核心优化：
1. **BFS 分层**：给每个点标记 `level = 到源点的最短距离`。增广时只能从 level 小的往 level 大的方向流，杜绝绕圈
2. **DFS 多路增广 + 当前弧优化**：一次 DFS 尽可能多地增广，用 `cur[u]` 记录 u 当前处理到哪条出边，避免重复扫描

```
BFS(分层) → DFS(多路增广) → 重复直到 BFS 无法到达汇点
```

> **直觉**：BFS 保证每次增广走的都是最短路径，DFS 负责在最短路径图上尽量多推流。一轮 BFS+DFS 就叫一个"阶段"，每阶段至少让最短路径长度 +1，因此最多 n 个阶段。

> **当前弧优化的原理与实现**：在 Dinic 的 DFS 增广过程中，`cur[u]` 数组记录结点 u 当前处理到哪条出边。关键观察：在一次 BFS 构建的分层图中，如果一条边 `(u, v)` 在某次 DFS 中被尝试增广但 `v` 已无法向汇点推送更多流（即递归返回 0），那么在当前分层图下，后续的增广中这条边也绝无可能再有贡献——因为层级关系不变，`v` 的容量瓶颈依然存在。因此 `cur[u]` 可以**永久跳过**这些已经"榨干"的边，每次 DFS 不用从 G[u][0] 开始扫描。实现方式：将 DFS 中的 `for(int i = 0; ...)` 改为 `for(int &i = cur[u]; ...)`（引用传递），cur[u] 在外层 while 循环中通过 `memset(cur, 0, ...)` 在每个新分层阶段开始时重置。这个优化将 Dinic 在分层图上的 DFS 部分从每轮 O(E) 拉低到每条边只被遍历常数次，是多路增广高效的关键。

#### 3. 最小割最大流定理 —— 切割与流量的对偶

- **割**：将图分成两组（S 组含源点，T 组含汇点），割的容量 = 从 S 组指向 T 组的所有边的容量之和
- **定理**：最大流的值 = 最小割的容量

> **直观理解**：把图的边想象成水管，从源点到汇点的总水量受限于"最窄的瓶颈"——而最小割就是全局的那个"最窄瓶颈"。因为流必须穿过割才能从 S 到 T，所有流的量都不会超过割的容量；而最大流的残余网络上，从源点可达的结点集合恰好构成了一个容量等于最大流的割——上界 = 下界。

**建模技巧**：很多"选择 / 冲突 / 分割"问题都对应最小割——S 侧表示"选"，T 侧表示"不选"；切割边的容量表示"代价"。

> **最小割的三种经典建模范式**：
> 
> **1. 二者选一（Binary Choice）**：每个元素必须选择属于集合 A 或集合 B，不同选择有不同的收益/代价。建模：源点 S 连向元素 i（容量 = 选 B 的代价），元素 i 连向汇点 T（容量 = 选 A 的代价）。割断 S→i 表示 i 归入 T 侧（选 A），割断 i→T 表示 i 归入 S 侧（选 B）。元素间如有冲突（例如 i 和 j 选不同集合有额外代价），则添加 i↔j 的双向边（容量 = 冲突代价）。
> 
> **2. 集合划分（Set Partition）**：将顶点划分为两个集合，最小化划分代价。建模同上，额外收益可转化为"负代价"处理（通过预加总收益再减去割的容量）。
> 
> **3. 最大权闭合子图（Maximum Weight Closure）**：选一个点就必须选它的所有后继。建模：S 连向正权点（容量 = 权值），负权点连向 T（容量 = -权值），原图的边容量为 INF。最小割将图分为 S 可达与不可达两部分，S 可达的正权点构成闭合子图。答案 = 正权总和 - 最小割容量。

#### 4. 费用流 —— 每条边不仅有容量，还有单价

在残量网络上跑**最短路**而不是随便找增广路。SPFA（或带势的 Dijkstra）每次找到**单位费用最小**的增广路，沿其增广。

> **为什么不直接用 Dijkstra？** 因为残量网络里有反向边（费用是正向边的相反数），可能有负边权。解决方法是维护**势能（potential）**，用 Johnson 最短路的思想消除负边：`h[v]` 记录上次的最短距离，用 `cost' = cost + h[u] - h[v]` 保证所有边非负，然后就能用 Dijkstra。

> **反向边费用为 -cost 的直觉解释——取消流量 = 返还费用**。在费用流中，每条正向边 `(u, v)` 的费用为 `cost`，其反向边 `(v, u)` 的费用设为 `-cost`。这不仅是数学上的对称处理，更有清晰的物理含义：如果在某次增广中，我们先沿着 `u→v` 推送了 f 个单位的流，支付了 `f * cost` 的费用；后来发现这个推送是不明智的（或者需要重新分配流量），就可以沿着反向边 `v→u` 推送流量。沿着反向边推送 f 个单位会获得 `f * (-cost) = -f * cost` 的"费用"——这恰好等于**退还**之前支付的费用。换句话说，残量网络中的反向边提供了"后悔"机制：取消之前的决策不仅恢复容量，还返还已付费用。这种对称设计保证了费用流算法（最短增广路）能正确找到全局最小费用的最大流。

#### 5. 上下界网络流 —— 每条边必须流过 [lower, upper]

普通流只要求"流量不超过容量"，上下界流要求每条边流量必须在 `[lower, upper]` 之间。

**构造方法**（无源汇可行流）：
1. 发送 `lower` 的流量到每条边，此时每个点的流入流出可能不平衡
2. 设 `A[u] = 总流入 - 总流出`（只算 lower 部分）
3. 新建超级源点 SS 和超级汇点 TT
4. 如果 `A[u] > 0`：SS → u，容量 = A[u]（需要补流入）
5. 如果 `A[u] < 0`：u → TT，容量 = -A[u]（需要泻出流）
6. 原边容量变为 `upper - lower`（剩余可流空间）
7. 从 SS 到 TT 跑最大流，满流则存在可行流

> **直觉**：先把每条边的"保底流量" lower 提前分配好，此时各点进出不平衡。用 SS/TT 来"配平"这些不平衡——缺流量的向 SS 借，多流量的排到 TT。配平成功意味着存在一种方案，在原图的 `[lower, upper]` 限制下实现流的平衡。

### 知识脉络

```
残量网络 + 增广路（根基）
    │
    ├──→ 最大流（最大流 / 最小割定理）
    │       ├──→ Dinic（BFS分层 + DFS多路 + 当前弧）
    │       └──→ 建模：分配、匹配、判定可行性
    │
    ├──→ 最小割（= 最大流）
    │       └──→ 建模：选择、冲突、分割代价
    │
    ├──→ 费用流（最短路 + 增广）
    │       └──→ 势能 Dijkstra 消除负边
    │
    └──→ 上下界网络流（强制流量区间）
            └──→ 构造 SS/TT 配平进出流量
```

每上升一层，流的模型就更灵活、表达能力更强。从"容量是上限"到"容量是区间"，从"流量不花钱"到"流量按单位计费"——这整套体系构成了竞赛中处理约束分配问题的最强工具链。

> **跨章关联**：网络流是全书建模能力的顶点，与多个章节形成闭环——**2.1节**中组合计数问题（用最大流判定方案存在性）与本节例题"足球联赛"共享判定型建模范式；**3.2节**线段树可以用于优化流网络的建图规模（将 O(n²) 条边降为 O(n log n)），处理网络流的大数据版本；**5.3节**最短路是费用流的底层引擎（SPFA/Potential Dijkstra）；**5.5节**二分图最大匹配是网络流的特例（所有边容量为1）；**6.2节**分块可以替代网络流处理某些区间分配问题，当 n 很大无法建图时退化为分块暴力。掌握网络流之后，从**匹配**到**分配**再到**选择代价**，几乎所有组合优化问题都可以用同一种语言描述。

### 快速上手模板

```cpp
// 【Dinic 最大流】BFS分层 + DFS多路增广 + 当前弧优化
struct Dinic {
    struct Edge { int to, cap, rev; };
    vector<Edge> G[maxn];
    int level[maxn], cur[maxn];

    void add_edge(int u, int v, int cap) {
        G[u].push_back({v, cap, (int)G[v].size()});
        G[v].push_back({u, 0, (int)G[u].size() - 1});
    }

    bool bfs(int s, int t) {
        memset(level, -1, sizeof(level));
        queue<int> q;
        level[s] = 0; q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (auto& e : G[u]) {
                if (e.cap > 0 && level[e.to] < 0) {
                    level[e.to] = level[u] + 1;
                    q.push(e.to);
                }
            }
        }
        return level[t] >= 0;
    }

    int dfs(int u, int t, int f) {
        if (u == t) return f;
        for (int& i = cur[u]; i < G[u].size(); i++) {
            auto& e = G[u][i];
            if (e.cap > 0 && level[u] < level[e.to]) {
                int d = dfs(e.to, t, min(f, e.cap));
                if (d > 0) {
                    e.cap -= d;
                    G[e.to][e.rev].cap += d;
                    return d;
                }
            }
        }
        return 0;
    }

    int maxflow(int s, int t) {
        int flow = 0;
        while (bfs(s, t)) {
            memset(cur, 0, sizeof(cur));
            int f;
            while ((f = dfs(s, t, INF)) > 0) flow += f;
        }
        return flow;
    }
};

// 【费用流】SPFA找最短路 + 增广
// add_edge(u, v, cap, cost) 同最大流，Edge 增加 cost 字段
// 每次用 SPFA 找 s→t 的单位费用最小路
// 沿最短路增广 min_cap，累加费用 += min_cap * dist[t]
```

## 例题32  足球联赛（The K-league, 大田 2002, LA 2531/UVa1306）

### 题目描述
一个足球联赛有 `n` 支球队。已知当前每支球队的胜场数 `w[i]` 和剩余的比赛安排 `a[i][j]`（i 和 j 之间的剩余比赛场数）。每个球队之间最多进行一次比赛，比赛不会有平局（一队胜、一队负）。问哪些球队在假设剩余比赛全部按有利于该球队的方式进行的情况下，有可能成为冠军（胜场数最多，可以并列）。`n ≤ 25`。

**输入格式**：第一行为测试数据组数 `T`。每组数据第一行 `n`，接下来 `n` 行每行 `w[i] d[i]`（胜场和无关数据），再 `n` 行 `n` 列比赛矩阵 `a[i][j]`。**输出格式**：对每组数据，输出可能成为冠军的球队编号（升序）。

### 解题思路
**最大流判定**：对于每支球队 `team`，假设它赢得所有剩余比赛，最大可能胜场为 `total = w[team] + Σ a[team][j]`。如果存在另一支球队胜场已超过 `total`，则 `team` 不可能夺冠。

**网络流建模**（对于候选球队 team）：
- 源点 `S` 连向每对球队 `(u,v)`（比赛），容量为 `a[u][v]`（剩余场数）。
- 每对 `(u,v)` 各连向 u 和 v，容量为 INF。
- 每支球队 `u` 连向汇点 `T`，容量为 `total - w[u]`（u 最多还能胜的场数）。
- 若最大流 = 所有剩余比赛总数，则 team 可能夺冠。

**流的含义**：源点到比赛的流量表示"分配胜利"，流经 u 的流量表示"给 u 的胜场"，汇点限制确保 no other team exceeds team 的最终胜场。

### 算法方法
- **Dinic 最大流算法**：BFS 分层 + DFS 增广，带当前弧优化。

### 复杂度分析
- **时间复杂度**：`O(n × V²√E)` 或 `O(n × V²E)`。每个 n 次判定，V = O(n²)，E = O(n²)，Dinic 在此类图中高效。
- **空间复杂度**：`O(n²)`。网络流图的边数 O(n²)。

```cpp
// 例题32  足球联赛（The K-league, 大田 2002, LA 2531/UVa1306）
// 解题思路：最大流判定——每支球队全赢，构建比赛分配网络，判断能否使该队冠军
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

## 例题31  运送超级计算机（Bring Them There, NEERC 2003,LA2957/UVa1324）

### 题目描述
有 `n` 个空间站和 `m` 条双向太空通道。每天每条通道只能通过一艘飞船（单向或双向但容量为 1）。有 `k` 艘飞船在空间站 `S`，需要运送到目标站 `T`。问最少需要多少天才能将所有飞船运送到目标，并输出每天的运输方案。`n ≤ 50`, `m ≤ 200`, `k ≤ 50`。

**输入格式**：多组数据。每组第一行 `n m k S T`，接下来 `m` 行 `u v`（通道连接的空间站编号）。**输出格式**：对每组数据输出天数 `d`，然后每天输出运输方案（飞船编号和目的地）。

### 解题思路
**分层图 + 最大流**：将每一天作为一层，在时间维度展开。

**分层图构造**：
- 第 `day` 层的结点编号为 `day*n` 到 `day*n+n-1`。
- 来源边（第 day-1 层到第 day 层）：
  1. 原地不动边：`(day-1)*n + i → day*n + i`，容量 INF。
  2. 通道边：`(day-1)*n + u → day*n + v`，容量 1（每天每条通道限 1 艘）。
  3. 反向通道边：`(day-1)*n + v → day*n + u`，容量 1。

**迭代求解**：第 1 天开始时（day=1），检查能否达到总流量 k。若不能，则增加一天（day++），在图中添加新一层的结点和边，继续增广。

**边界分析**：最多需要 `n + k - 2` 天（最坏情况：一艘飞船走 n-1 天，且每天只能运一艘）。总结点数 ≤ `(n + k - 1) × n`。

**方案输出**：回溯每条边的流量，找出每天哪些飞船移动了。

### 算法方法
- **Dinic 最大流算法**：分层图上的增量式最大流。

### 复杂度分析
- **时间复杂度**：`O((n+k) × n × m)`。最多 (n+k) 天，每天添加 O(m) 条边，Dinic 增广。
- **空间复杂度**：`O((n+k) × n × m)`。

```cpp
// 例题31  运送超级计算机（Bring Them There, NEERC 2003,LA2957/UVa1324）
// 解题思路：分层图最大流——每天一层，原地不动(INF边)+通道移动(容量1边)，迭代增加天数
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

### 题目描述
有 `n` 个人（包括 Bob）和 `m` 种贴纸。Bob 希望收集尽可能多不同种类的贴纸。每人最初有一些贴纸。他们可以相互交换贴纸，但每个人在交换中遵循以下规则：每个人最多可以给出每种贴纸中他持有的"重复"贴纸（即如果持有 ≥2 张同种贴纸，可以给出 cnt-1 张）；每个人最多可以接受 1 张他没有的贴纸。Bob 希望最大化他获得的不同贴纸种类数。`n ≤ 10`, `m ≤ 25`。

**输入格式**：第一行为测试数据组数 `T`。每组数据第一行 `n m`，接下来 `n` 行每行一个整数 `k` 表示该人持有的贴纸数量，然后 `k` 个整数（贴纸编号）。**输出格式**：对每组数据输出 Bob 最多能收集的不同贴纸种类数。

### 解题思路
**最大流建模**：将交换过程建模为网络流。

**结点设计**：
- 源点 `S = 0`，连接 Bob 拥有的贴纸种类（容量为 Bob 持有的每种的张数）。
- 每种贴纸作为一个结点（1~m）。
- 除 Bob 外的每个人作为一个结点（m+1 ~ m+n-1）。
- 汇点 `T = m + n`。

**边的含义**：
- `S → 贴纸 j`（容量 = Bob 持有数）：Bob 可以给出重复贴纸交换。
- `贴纸 j → 人 i`（容量 1）：人 i 可以接受 1 张他没有的贴纸 j。
- `人 i → 贴纸 j`（容量 cnt[j]-1）：人 i 可以给出 cnt[j]-1 张他的重复贴纸 j。
- `贴纸 j → T`（容量 1）：每种贴纸最终最多收集 1 张。

**答案**：从 S 到 T 的最大流量 = Bob 能获得的最大不同贴纸种类数。

### 算法方法
- **Dinic 最大流算法**：网络流建模，求最大流。

### 复杂度分析
- **时间复杂度**：`O(T × V²E)`。V = n + m ≤ 35，E = O(n × m)。
- **空间复杂度**：`O(V + E)`。

```cpp
// 例题33  收集者的难题（Collectors Problem, UVa 10779）
// 解题思路：最大流建模——S→Bob的贴纸→其他人与贴纸间交换→每种贴纸→T(容量1)
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

### 题目描述
给定一个有向带权网络（`n` 个结点，`m` 条边），以及目标流量 `C`。你可以选择至多修改一条边的容量（将其增加到任意值），问能否使源点 `1` 到汇点 `n` 的最大流至少为 `C`。如果已经 ≥ C，输出 "possible"；如果不能通过修改一条边达成，输出 "not possible"；如果可以，输出所有可能的修改方案 `(u, v)`（修改后能使最大流 ≥ C 的边）。`n ≤ 100`, `m ≤ 1000`。

**输入格式**：多组数据。每组第一行 `n e c`，接下来 `e` 行 `u v capacity`。n=e=c=0 结束。**输出格式**：对每组数据输出判定结果。

### 解题思路
**最大流 + 最小割分析**：

**第一步**：运行最大流算法，如果流量 ≥ C → "possible"。

**第二步**：如果流量不足，计算当前网络的最小割（使用 ISAP 算法求最大流后的残留网络 BFS）。候选修改边只能是**最小割中的边**（容量被完全使用且从 S-可达集指向 S-不可达集的边）。因为修改非最小割中的边不会改变最大流值。

**第三步**：对于每条在最小割中的边：
1. 临时将该边的容量设为 C（足够大）。
2. 在不重新计算全图的情况下（使用 `Reduce` 保留已增广的流），重新求最大流。
3. 如果新流量 ≥ C，则该边是一个可行方案。
4. 恢复边的容量。

**ISAP 算法**：使用距离标号优化（Improved Shortest Augmenting Path），比 Dinic 效率更高。包含 `Reduce()` 操作保留历史流量。

### 算法方法
- **ISAP 最大流算法**：带距离标号优化的增广路算法。
- **最小割分析**：限制候选边为最小割中的边。

### 复杂度分析
- **时间复杂度**：`O(n²m + |cut| × n²m)`。首次最大流 O(n²m)，每次候选边重算最大流 O(n²m)。
- **空间复杂度**：`O(n + m)`。

```cpp
// 例题30  UVa11248 Frequency Hopping：使用ISAP算法，加优化
// 解题思路：ISAP最大流+最小割分析——修改容量只能选最小割中的边，Reduce保留历史流
// 刘汝佳
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

### 题目描述
Acme 公司计划未来 `M` 个月的生产和销售。每个月 i 有：
- 生产成本 `make_cost[i]`（每件）
- 最大产量 `make_limit[i]`
- 售价 `price[i]`（每件）
- 最大销量 `sell_limit[i]`
- 产品最长可存储 `max_store[i]` 个月（当月生产的产品最晚在第 i+max_store[i] 月前必须售出）
- 存储成本 `store_cost`（每件每月，全局统一）

求最大利润（总收入 - 总生产成本 - 总存储成本）。`M ≤ 200`。

**输入格式**：第一行为测试数据组数 `T`。每组数据第一行 `M store_cost`，接下来 `M` 行每行 `make_cost make_limit price sell_limit max_store`。**输出格式**：对每组数据输出最大利润。

### 解题思路
**最小费用最大流（MCMF）**：将每个月"生产"和"销售"拆分为两个结点。

**网络流建模**：
- 源点 `S = 0`。
- 生产结点（1~M）：第 i 个月的生产。
- 销售结点（M+1~2M）：第 i 个月的销售。
- 汇点 `T = 2M + 1`。

**边的构建**：
- `S → 生产结点 i`（容量 `make_limit[i]`，费用 `make_cost[i]`）：在 i 月生产。
- `生产结点 i → 销售结点 i+j`（容量 INF，费用 `store_cost × j`）：产品存储 j 个月后售出（j=0 表示当月生产当月卖）。
- `销售结点 i → T`（容量 `sell_limit[i]`，费用 `-price[i]`）：在第 i 月销售（收益为负费用）。

**求解**：在网络上运行最小费用最大流（MCMF）。由于边的费用有正有负，且收益为负费用。当费用和变成正数时停止（后续增广只会减少利润）。

**答案**：`-总费用`（因为收益表示为负费用）。

### 算法方法
- **最小费用最大流（MCMF / Min-Cost Max-Flow）**：使用 Bellman-Ford + SPFA 的连续最短路增广算法。

### 复杂度分析
- **时间复杂度**：`O(F × V × E)`，其中 F 是最大流量。V = 2M+2，E = O(M²)（每个月的产品可以存到之后的任意月）。
- **空间复杂度**：`O(V + E) = O(M²)`。

```cpp
// 例题34  生产销售规划（Acme Corporation, UVa 11613）
// 解题思路：最小费用最大流(MCMF)——每月拆为生产和销售两点，收入为负费用，最小费用流求最大利润
// 陈锋
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
