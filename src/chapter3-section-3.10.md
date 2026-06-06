# 3.10 kd-Tree

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
#include <bits/stdc++.h>
typedef long long LL;
using namespace std;
const int NN = 2E5 + 8;
struct Point {
  LL x, y;
  int c, id;
} Ps[NN];
istream& operator>>(istream& is, Point& p) { return is >> p.x >> p.y >> p.c; }
bool cmpx(const Point& p1, const Point& p2) { return p1.x < p2.x; }
bool cmpy(const Point& p1, const Point& p2) { return p1.y < p2.y; }
LL dist(const Point& a, const Point& b) {
  return (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y);
}
bool Div[NN];  // 每一层的划分方式
void build(int l, int r) {
  if (l > r) return;
  int m = (l + r) / 2;
  Point *pl = Ps + l, *pr = Ps + r + 1;
  pair<Point*, Point*> px = minmax_element(pl, pr, cmpx),
                       py = minmax_element(pl, pr, cmpy);
  Div[m] = px.second->x - px.first->x >= py.second->y - py.first->y;
  nth_element(pl, Ps + m, pr, Div[m] ? cmpx : cmpy);
  build(l, m - 1), build(m + 1, r);
}
// Ps[L,r]中距离p最小的点->id，最小距离min_d。且要求Ps[id].c<p.c
void nearest(int l, int r, const Point& p, LL& min_d, int& id) {
  if (l > r) return;
  int m = (l + r) / 2;
  const Point& pm = Ps[m];
  LL d = dist(p, pm);
  if (pm.c <= p.c) {
    if (d < min_d) min_d = d, id = m;
    else if (d == min_d && pm.id < Ps[id].id) id = m;
  }
  d = Div[m] ? (p.x - pm.x) : (p.y - pm.y);
  if (d <= 0) {
    nearest(l, m - 1, p, min_d, id);
    if (d * d < min_d) nearest(m + 1, r, p, min_d, id);
  } else {
    nearest(m + 1, r, p, min_d, id);
    if (d * d < min_d) nearest(l, m - 1, p, min_d, id);
  }
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int id, n, m, T;
  cin >> T;
  while (T--) {
    cin >> n >> m;
    for (int i = 1; i <= n; i++) cin >> Ps[i], Ps[i].id = i;
    build(1, n);
    Point p;
    while (m--) {
      cin >> p;
      LL min_d = 1LL << 60;
      nearest(1, n, p, min_d, id);
      printf("%lld %lld %d\n", Ps[id].x, Ps[id].y, Ps[id].c);
    }
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
#include <bits/stdc++.h>

#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)
using namespace std;
typedef long long LL;

const int NN = 200010, MM = 10010;
int N, M, D, NodeId[NN], root, cmp_dim, BLOCK;
struct Point { int x, y; } PS[NN];
struct Query {
  int l, r, id;
  bool operator<(const Query& q) const {
    if (l / BLOCK != q.l / BLOCK) return l / BLOCK < q.l / BLOCK;
    return r < q.r;
  }
} QS[MM];
LL Ans[MM];

// if l ≤ x ≤ r
inline bool inRange(int x, int l, int r) { return l <= x && x <= r; }

struct KDTree {
  int xy[2], xyMax[2], xyMin[2], CH[2], cnt, cntSum, fa;
  bool operator<(const KDTree& k) const { return xy[cmp_dim] < k.xy[cmp_dim]; }
  inline int query(int x1, int x2, int y1, int y2);
  inline void update();
  inline void init(int i);
} Tree[NN];

// 查询整棵树中在[x1,x1], [y1,y2]中的节点个数
inline int KDTree::query(int x1, int x2, int y1, int y2) {
  int k = 0;
  if (xyMin[0] > x2 || xyMax[0] < x1 || xyMin[1] > y2 || xyMax[1] < y1 || 0 == cntSum)
    return 0; // 整棵树都不在[x1, x2], [y1, y2]中
  if (x1 <= xyMin[0] && xyMax[0] <= x2 && y1 <= xyMin[1] && xyMax[1] <= y2)
    return cntSum; // 整棵树都在其中
  if (inRange(xy[0], x1, x2) && inRange(xy[1], y1, y2))
    k += cnt; // 当前点在其中
  _for(i, 0, 2) if (CH[i])
    k += Tree[CH[i]].query(x1, x2, y1, y2); // 左右节点查询
  return k;
}

// 更新当前整棵树的x,y的Min,Max值
inline void KDTree::update() { // 更新整棵树的x,y坐标的Max, Min
  _for(i, 0, 2) if (CH[i]) _for(j, 0, 2) {
    xyMax[j] = max(xyMax[j], Tree[CH[i]].xyMax[j]);
    xyMin[j] = min(xyMin[j], Tree[CH[i]].xyMin[j]);
  }
}

// 初始化KDTree节点
inline void KDTree::init(int i) { // 初始化节点信息
  NodeId[fa] = i; // 一开始fa记录的是TreeNodeId对应的PointId
  _for(j, 0, 2) xyMax[j] = xyMin[j] = xy[j]; // 两个维度坐标的最大值
  cnt = cntSum = 0; // 是否在莫队当前区间中，树中在莫队当前区间中的点个数，初始都是0
  CH[0] = CH[1] = 0; // 左右子树初始化
}

// 将Ps[l, r]构建成一棵树
int build(int l, int r, int dim, int fa) {
  int mid = (l + r) / 2; // 区间分成两半
  // 取出按照cmp_dim维度对l,r点进行比较，并且将点mid放在中间
  cmp_dim = dim, nth_element(Tree + l + 1, Tree + mid + 1, Tree + r + 1);
  KDTree& n = Tree[mid]; // 本树根节点
  n.init(mid), NodeId[n.fa] = mid, n.fa = fa;
  if (l < mid) n.CH[0] = build(l, mid - 1, !dim, mid); // 递归构建左子树
  if (r > mid) n.CH[1] = build(mid + 1, r, !dim, mid); // 递归构建右子树
  n.update();
  return mid;
}

LL curAns;
inline void addPos(int i) { // 查找所有与Ps[i]距离≤D的点的个数
  curAns += Tree[root].query(PS[i].x - D, PS[i].x + D, PS[i].y - D, PS[i].y + D);
  int ti = NodeId[i]; // 点i对应的KDTree节点
  Tree[ti].cnt = 1; // 将点i记录下来，并且更新其所有祖先的计数
  while (ti) Tree[ti].cntSum++, ti = Tree[ti].fa;
}

inline void delPos(int i) {
  int ti = NodeId[i];
  Tree[ti].cnt = 0;
  // 将点i从莫队区间中去除，更新所有父节点的计数
  while (ti) Tree[ti].cntSum--, ti = Tree[ti].fa;
  // 去掉跟点i距离不大于D的点的个数
  curAns -= Tree[root].query(PS[i].x - D, PS[i].x + D, PS[i].y - D, PS[i].y + D);
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  for (int t = 1, x, y; cin >> N >> D >> M; t++) {
    printf("Case %d:\n", t);
    BLOCK = (int)sqrt(N + 0.5);
    _rep(i, 1, N) {
      KDTree &nd = Tree[i];
      cin >> x >> y;
      nd.xy[0] = PS[i].x = x + y, nd.xy[1] = PS[i].y = x - y, Tree[i].fa = i;
    }
    root = build(1, N, 0, 0);
    _rep(i, 1, M) cin >> QS[i].l >> QS[i].r, QS[i].id = i;
    sort(QS + 1, QS + M + 1);
    int curL = 1, curR = 0;
    curAns = 0;
    _rep(i, 1, M) { // 维护莫队当前的区间
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
