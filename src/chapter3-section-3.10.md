# 3.10 kd-Tree

> **学习目标**：理解 kd-Tree 空间划分的"方差最大维优先"原则、KNN 搜索的剪枝条件物理含义、以及 kd-Tree 作为"维度诅咒"受害者在高维下的性能退化事实。

## 理论基础

### 为什么需要学这个？

如果你需要快速找到平面上距离某一点最近的 K 个点，朴素的 O(N) 扫描在大数据面前就是龟速。kd-Tree 就是为解决"多维空间中的范围查询和近邻搜索"而生的。它的思路非常朴素：把空间像切西瓜一样反复切成两半，每次切的时候都用"当前数据最散的那一维"作为刀口。这个简单的策略在低维（2D/3D）下平均效果非常好——每次查询只需 O(log N)。但 kd-Tree 有一个容易被忽略的真相：**维度一上去，性能直接崩盘**。如果你试图用它解决十维甚至二十维的问题，它可能比暴力扫描还慢。这一节，我们从"怎么切"讲到"为什么在高维会退化"，让你知己知彼。

### 核心概念

#### 1. 方差选择原则：为什么选"最散的那一维"？

**一句话定义**：在构建 kd-Tree 的每一层，计算所有数据点在每个维度上的方差，选择方差最大的维度作为划分维度，取中位数作为分割点。

**本质理解**：方差大 = 数据在这一维上分布得比较开。如果你选一个"所有数据值都差不多"的维度来切，切出来的左右子空间差别不大——树就"白切了"。方差最大意味着这一维能提供**最大的信息增益**，切完两边数据密度有明显差异，树更平衡、搜索更快。

**最小示例**：如果所有点都在 x 轴附近排成一行，y 坐标几乎不变。选 x 维度切可以有效划分空间；选 y 维度切可能所有点都落在一侧。

#### 2. KNN 搜索的剪枝条件：点到区域的最短距离

**一句话定义**：正在搜索最近邻时，当前最优距离为 best。查询点到"另一侧子空间"的最小距离如果在划分维度上的投影的平方 > best，就安全地剪掉那一侧。

**本质理解**：这本质上是一个 **bounding box** 的修剪。想象每个 kd-Tree 节点代表一个矩形区域（节点存储的 `xyMin/xyMax` 就是这个矩形）。查询点到这个矩形的最短距离 = max(0, 查询点坐标 - 矩形右边界) 在每个维度上的平方和。如果这个距离已经大于你当前找到的最近距离，那这个矩形里不可能有更近的点，直接跳过。这就是为什么 kd-Tree 能比暴力快——**绝大多数空间区域根本不用进入**。

#### 3. 高维退化问题

**一句话定义**：当维度 d 较大时（通常 > 10），kd-Tree 的剪枝效果急剧下降，最坏情况下每个节点都可能被访问，退化为 O(N)。

**本质理解**：高维空间有一个反直觉的性质——点的分布变得"稀疏而均匀"。在高维中，任何查询点到大多数 kd-Tree 节点的最小距离都非常接近，剪枝条件 `dist > best` 几乎永远不成立。而且最坏情况下，查询需要访问的节点数以指数方式依赖于 d。这是"维度诅咒"的典型体现。实用建议：**d ≤ 5 大胆用 kd-Tree，d ≥ 20 换用 LSH 或其他近似算法**。

#### 4. KNN 搜索最近邻的剪枝三条件详解

**条件一（主条件）：划分维度上的投影距离剪枝。** 设当前节点的划分维度为 dim，查询点 q 在该维度上和当前节点 p 的距离 delta = |q[dim] - p[dim]|。如果 delta² ≥ best（当前最优距离），则另一侧子空间完全不可能有更近的点——因为任何点到 q 的距离至少是 delta（在 dim 上的投影距离，其他维度的距离非负）。此时安全剪掉另一侧。Python 伪代码：`if delta * delta >= best: 跳过另一侧`。

**条件二（优先搜索近侧）：先搜索查询点所在的子空间。** 如果 q 在当前节点的划分维度上小于节点值（q[dim] < p[dim]），q 更接近左子空间，先递归左子树。这是因为近侧更可能包含最近邻，先搜索近侧可以更快地收紧 best，从而更早剪掉远侧。

**条件三（Bounding Box 整体剪枝）：基于节点矩形区域的全局判断。** 更通用的实现为每个节点维护 xyMin/xyMax（子树中所有点在每个维度上的最小值和最大值，即轴对齐包围盒 AABB）。查询点到节点矩形区域的最小距离定义为：若 q[dim] 在 [xyMin[dim], xyMax[dim]] 内则该维度贡献 0，否则该维贡献 = min(|q[dim]-xyMin[dim]|, |q[dim]-xyMax[dim]|)²。各维度平方和即查询点到子树区域的最短距离。若此距离 ≥ best，整个子树可以安全跳过。**条件一实际上就是条件三在单维度上的特例。**

### 知识脉络

```
多维空间查询
    │
    ├── kd-Tree (d ≤ 5)
    │   ├── 构建: 方差选维 + 中位数分割
    │   ├── 查询: bounding box + 距离剪枝
    │   └── 陷阱: 高维退化 (d > 10 效果变差)
    │
    └── 替代方案 (d > 20)
        ├── LSH (局部敏感哈希)
        └── 近似最近邻(ANN)
```

**本书跨章节连接**：kd-Tree 的最近邻搜索与第 4.3 节的**旋转卡壳**形成"动态 vs 静态"的二维近邻处理方案——前者支持动态点集的 KNN 查询，后者对固定凸包有 O(N) 的直径计算。kd-Tree 还可在莫队算法（3.9 节）中充当空间查询加速器——用矩形范围查询替代逐点扫描。如果在第 4.1 节的"狗的距离"问题中引入 kd-Tree，则可以将每次更新从 O(1) 变为 O(log N) 的近邻查询。

### 快速上手模板

```cpp
// kd-Tree 核心结构
struct Point { LL x, y; };
bool Div[N];  // 每层的划分维度

void build(int l, int r) {
    if (l > r) return;
    int m = (l + r) / 2;
    // 选择方差大的维度
    auto [xmin, xmax] = minmax_element(ps+l, ps+r+1, cmpx);
    auto [ymin, ymax] = minmax_element(ps+l, ps+r+1, cmpy);
    Div[m] = (xmax->x - xmin->x) >= (ymax->y - ymin->y); // x方差较大则按x划分
    nth_element(ps+l, ps+m, ps+r+1, Div[m] ? cmpx : cmpy); // 中位数居中
    build(l, m-1), build(m+1, r);
}

// KNN搜索（最近邻）
void nearest(int l, int r, const Point& q, LL& best, int& id) {
    if (l > r) return;
    int m = (l + r) / 2;
    LL d = dist(q, ps[m]);
    if (/* 满足筛选条件 */ d < best) best = d, id = m;
    LL delta = Div[m] ? (q.x - ps[m].x) : (q.y - ps[m].y); // 投影距离
    if (delta <= 0) {
        nearest(l, m-1, q, best, id);           // 先搜索近侧
        if (delta * delta < best) nearest(m+1, r, q, best, id); // 剪枝判远侧
    } else {
        nearest(m+1, r, q, best, id);
        if (delta * delta < best) nearest(l, m-1, q, best, id);
    }
}
```

## 例题51  寻找酒店（Finding Hotels, ACM/ICPC 青岛 2016, LA7744/HDU5992）

### 题目描述
平面上有N家酒店，每家酒店有坐标(x,y)和价格c。有M个查询，每次给出查询坐标(x,y)和预算上限C，需要找到**距离查询点最近**且**价格不超过C**的酒店，输出其坐标和价格。如有多个距离相同，选编号最小的。

- **输入格式**：T组数据。每组：N M，N行每行x y c（酒店），M行每行x y C（查询）。
- **约束**：N, M ≤ 2×10^5, x, y ≤ 10^9。

### 解题思路
使用**KD-Tree + 最近邻搜索**：
1. **KD-Tree构建**：交替按x/y维度划分空间，选择方差较大的维度划分，每个节点为中位数（nth_element）。记录每层划分维度Div。
2. **最近邻查询**：递归搜索KD-Tree。先遍历查询点所在的子空间，记录当前最优距离。检查另一侧时，若划分维度上的距离平方已超过最优距离，则剪枝（不可能有更近的点）。
3. **价格条件**：只有价格≤查询预算的点才参与比较。

### 算法方法
**KD-Tree（K维树）**：二维空间划分数据结构。交替维度划分实现O(log N)平均查询。nth_element选择中位数保证树平衡。剪枝策略在最近邻搜索中利用"当前最优距离 > 划分维距离"的条件避免无效搜索。

### 复杂度分析
- **时间复杂度**：构建O(N log N)，每次查询平均O(log N)，最坏O(N)。
- **空间复杂度**：O(N)，存储所有点。

```cpp
// 例题51  寻找酒店（Finding Hotels, LA7744/HDU5992）
// 陈锋
// 题目：平面上找距离最近且价格不超过预算的酒店
// 算法：KD-Tree + 最近邻搜索（带剪枝）
#include <bits/stdc++.h>
typedef long long LL;
using namespace std;
const int NN = 2E5 + 8;
struct Point { LL x, y; int c, id; } Ps[NN];
istream& operator>>(istream& is, Point& p) { return is >> p.x >> p.y >> p.c; }
bool cmpx(const Point& p1, const Point& p2) { return p1.x < p2.x; }
bool cmpy(const Point& p1, const Point& p2) { return p1.y < p2.y; }
LL dist(const Point& a, const Point& b) { return (a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y); }

bool Div[NN];  // 记录每层的划分维度
void build(int l, int r) {  // 递归构建KD-Tree
  if (l > r) return;
  int m = (l + r) / 2; Point *pl = Ps + l, *pr = Ps + r + 1;
  // 选择跨度较大的维度作为划分维度
  pair<Point*, Point*> px = minmax_element(pl, pr, cmpx), py = minmax_element(pl, pr, cmpy);
  Div[m] = px.second->x - px.first->x >= py.second->y - py.first->y;  // 方差大的维度
  nth_element(pl, Ps + m, pr, Div[m] ? cmpx : cmpy);  // 中位数
  build(l, m - 1), build(m + 1, r);
}

void nearest(int l, int r, const Point& p, LL& min_d, int& id) {  // 最近邻搜索
  if (l > r) return;
  int m = (l + r) / 2; const Point& pm = Ps[m]; LL d = dist(p, pm);
  if (pm.c <= p.c) {  // 价格满足条件
    if (d < min_d) min_d = d, id = m;
    else if (d == min_d && pm.id < Ps[id].id) id = m;
  }
  d = Div[m] ? (p.x - pm.x) : (p.y - pm.y);  // 查询点与中位数点在划分维度上的距离
  if (d <= 0) {  // 查询点在左侧
    nearest(l, m - 1, p, min_d, id);
    if (d * d < min_d) nearest(m + 1, r, p, min_d, id);  // 右侧可能有更近的点
  } else {
    nearest(m + 1, r, p, min_d, id);
    if (d * d < min_d) nearest(l, m - 1, p, min_d, id);
  }
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int id, n, m, T; cin >> T;
  while (T--) {
    cin >> n >> m;
    for (int i = 1; i <= n; i++) cin >> Ps[i], Ps[i].id = i;
    build(1, n);
    Point p;
    while (m--) { cin >> p; LL min_d = 1LL << 60; nearest(1, n, p, min_d, id); printf("%lld %lld %d\n", Ps[id].x, Ps[id].y, Ps[id].c); }
  }
  return 0;
}
// 32942274 2020-04-02 18:03:46 Accepted  5992  358MS 6344K 1962 B  G++ chenwz
```

## 例题52  保持健康（Keep Fit! UVa12939）

### 题目描述
有N个人在平面上运动（坐标(x,y)），两人"接触"当且仅当曼哈顿距离≤D。有M个查询[L,R]，问在时间区间[L,R]内，接触对的总数。

- **约束**：N ≤ 2×10^5, M ≤ 10^4, D ≤ 10^8。

### 解题思路
使用 **KD-Tree + 莫队算法**：
1. **坐标变换**：将曼哈顿距离转切比雪夫距离：`(x',y') = (x+y, x-y)`。则原问题转化为二维矩形范围内的点数统计。
2. **KD-Tree**：维护所有点的坐标，支持矩形范围查询（query函数），统计节点子树内有多少个点在当前莫队区间内（cntSum）。
3. **莫队算法**：离线处理查询，按(BLOCK, r)排序。移动左右端点时更新当前答案。addPos: 查询KD-Tree中与点i距离≤D（变换后为矩形范围）的点数 + 将点i标记为"在区间内"；delPos: 撤销标记。
4. 注意曼哈顿距离转换后：`|x1-x2|+|y1-y2| ≤ D` 等价于变换后的切比雪夫距离 `max(|x1'-x2'|, |y1'-y2'|) ≤ D`。

### 算法方法
**KD-Tree + 莫队算法（Mo's Algorithm）**：KD-Tree用于快速矩形范围查询（维护子树内的活跃点计数cntSum），莫队算法处理离线区间查询。坐标变换将曼哈顿距离条件下的计数转化为矩形范围查询。

### 复杂度分析
- **时间复杂度**：O((N+M√N)log N)，每次add/del O(log N)。
- **空间复杂度**：O(N+M)，存储KD-Tree节点和查询。

```cpp
// 例题52  保持健康（Keep Fit! UVa12939）
// 陈锋
// 题目：查询时间区间[L,R]内曼哈顿距离≤D的点对总数
// 算法：曼哈顿→切比雪夫变换 + KD-Tree矩形查询 + 莫队算法
#include <bits/stdc++.h>
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)
using namespace std;
typedef long long LL;

const int NN = 200010, MM = 10010;
int N, M, D, NodeId[NN], root, cmp_dim, BLOCK;
struct Point { int x, y; } PS[NN];
struct Query { int l, r, id;  // 莫队查询
  bool operator<(const Query& q) const { if (l / BLOCK != q.l / BLOCK) return l / BLOCK < q.l / BLOCK; return r < q.r; }
} QS[MM];
LL Ans[MM];

inline bool inRange(int x, int l, int r) { return l <= x && x <= r; }

struct KDTree {
  int xy[2], xyMax[2], xyMin[2], CH[2], cnt, cntSum, fa;  // cnt:当前点是否在区间内, cntSum:子树内点数
  bool operator<(const KDTree& k) const { return xy[cmp_dim] < k.xy[cmp_dim]; }
  // 查询子树中在矩形[x1,x2]×[y1,y2]内的点数
  inline int query(int x1, int x2, int y1, int y2) {
    int k = 0;
    if (xyMin[0] > x2 || xyMax[0] < x1 || xyMin[1] > y2 || xyMax[1] < y1 || 0 == cntSum) return 0;
    if (x1 <= xyMin[0] && xyMax[0] <= x2 && y1 <= xyMin[1] && xyMax[1] <= y2) return cntSum;
    if (inRange(xy[0], x1, x2) && inRange(xy[1], y1, y2)) k += cnt;
    _for(i, 0, 2) if (CH[i]) k += Tree[CH[i]].query(x1, x2, y1, y2);
    return k;
  }
  inline void update() { _for(i, 0, 2) if (CH[i]) _for(j, 0, 2) { xyMax[j] = max(xyMax[j], Tree[CH[i]].xyMax[j]); xyMin[j] = min(xyMin[j], Tree[CH[i]].xyMin[j]); } }
  inline void init(int i) { NodeId[fa] = i; _for(j, 0, 2) xyMax[j] = xyMin[j] = xy[j]; cnt = cntSum = 0; CH[0] = CH[1] = 0; }
} Tree[NN];

int build(int l, int r, int dim, int fa) {  // KD-Tree构建
  int mid = (l + r) / 2; cmp_dim = dim, nth_element(Tree + l + 1, Tree + mid + 1, Tree + r + 1);
  KDTree& n = Tree[mid]; n.init(mid), NodeId[n.fa] = mid, n.fa = fa;
  if (l < mid) n.CH[0] = build(l, mid - 1, !dim, mid);
  if (r > mid) n.CH[1] = build(mid + 1, r, !dim, mid);
  n.update(); return mid;
}

LL curAns;
inline void addPos(int i) {  // 莫队添加点i
  curAns += Tree[root].query(PS[i].x - D, PS[i].x + D, PS[i].y - D, PS[i].y + D);
  int ti = NodeId[i]; Tree[ti].cnt = 1;
  while (ti) Tree[ti].cntSum++, ti = Tree[ti].fa;
}
inline void delPos(int i) {  // 莫队删除点i
  int ti = NodeId[i]; Tree[ti].cnt = 0;
  while (ti) Tree[ti].cntSum--, ti = Tree[ti].fa;
  curAns -= Tree[root].query(PS[i].x - D, PS[i].x + D, PS[i].y - D, PS[i].y + D);
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  for (int t = 1, x, y; cin >> N >> D >> M; t++) {
    printf("Case %d:\n", t); BLOCK = (int)sqrt(N + 0.5);
    _rep(i, 1, N) { KDTree &nd = Tree[i]; cin >> x >> y; nd.xy[0] = PS[i].x = x + y, nd.xy[1] = PS[i].y = x - y; Tree[i].fa = i; }  // 坐标变换
    root = build(1, N, 0, 0);
    _rep(i, 1, M) cin >> QS[i].l >> QS[i].r, QS[i].id = i;
    sort(QS + 1, QS + M + 1);  // 莫队排序
    int curL = 1, curR = 0; curAns = 0;
    _rep(i, 1, M) {  // 莫队移动区间
      while (curR < QS[i].r) addPos(++curR);
      while (curR > QS[i].r) delPos(curR--);
      while (curL < QS[i].l) delPos(curL++);
      while (curL > QS[i].l) addPos(--curL);
      Ans[QS[i].id] = curAns;
    }
    _rep(i, 1, M) printf("%lld\n", Ans[i]);
  }
  return 0;
}
// 23613445 12939 Keep Fit! Accepted  C++11 3.630 2019-07-18 00:30:00
```
