# 3.2 区间信息的维护与查询

> **学习目标**：掌握树状数组的 lowbit 本质和线段树的区间合并+惰性标记机制，建立"用二叉树管理区间"的思维框架。

## 理论基础

### 为什么需要学这个？

你肯定遇过这种场景：数组要支持单点修改和区间求和，暴力 O(N) 每次查询，被大数据卡爆。这时有人告诉你"用树状数组"，于是你背下了 `x += lowbit(x)` 的代码，但始终觉得 `lowbit` 是什么黑魔法。同样地，线段树的 `pushdown` 什么时候调、`maintain` 什么时候调，写错了就是"调三小时，删一行 bug"。这一节我们不走"背代码"的老路，而是从**二进制分解**和**区间结合律**两个底层原理出发，帮你真正理解：树状数组为什么能用一棵"缺胳膊少腿的树"做到前缀和，以及线段树的惰性标记为什么必须在下传时才生效。

### 核心概念

#### 1. lowbit = 二进制表示中的最低位 1

**一句话定义**：`lowbit(x) = x & -x`，它取出 x 的二进制表示中最低位的 1 对应的数值。

**本质理解**：树状数组 `C[i]` 管辖着 `[i - lowbit(i) + 1, i]` 这个区间的和。前进一步 `i += lowbit(i)` 是去"覆盖范围更大的那个区间"，后退一步 `i -= lowbit(i)` 是跳到"下一个不重叠区间"。整个 BIT 的结构就是将数组按二进制位切分而成的**不完全二叉树**——它之所以省空间，正是因为它只保留了每个最低位 1 对应的"汇总节点"。

**与朴素对比**：朴素前缀和修改 O(N)，查询 O(1)；树状数组两点 O(log N)。朴素线段树每个节点拆成两半，BIT 则按二进制位拆——BIT 的区间不是"严格的左右子树"，而是"2 的幂次大小"的压缩块。

#### 2. 线段树的区间合并需要结合律

**一句话定义**：线段树每个节点维护的值，必须能从左右子区间的值合并而来，且合并运算必须满足结合律。

**本质理解**：线段树的灵魂在于——我把大区间拆成两部分，分别维护好各自的信息后，就能在 O(1) 时间内"拼"出整个大区间的信息。这意味着**你维护的信息必须具有区间可合并性**。比如 sum 满足结合律（可以加），max 也满足；但求众数就不满足——你不能光从左右子区间的众数推出整个区间的众数。这就是为什么线段树的"节点信息结构性"比代码本身更重要。

#### 3. Lazy 标记：什么时候下传、什么顺序

**一句话定义**：Lazy 标记是对"暂缓的区间修改"的记录，只有在必须访问子节点时才下推。

**本质理解**：惰性标记设计的黄金法则——**"在读取或修改子节点之前必须 pushdown"**。加法标记和赋值标记同时存在时，赋值优先（因为赋值会覆盖加法）。pushdown 的顺序必须是：先传赋值标记，再传加法标记。另一个关键问题：**标记是什么语义？** 有的是"该区间被整体加了一个值"（add），有的是"该区间被整体覆盖为一个值"（set）。弄混语义是 bug 的首要来源。

#### 4. 树状数组 vs 线段树：选择决策树

**决策逻辑**：当遇到区间问题需要选择数据结构时，依次回答以下问题：

1. **是否只需要前缀和/单点修改？** → 树状数组（BIT），常数小、代码短。
2. **是否需要区间修改？** → 若只需要差分区间加+单点查询，BIT 仍可行（差分 BIT）；若需要区间修改+区间查询，优先用 BIT 维护两个差分数组（常数更优，但只适合加法）。
3. **是否需要维护 max/min/gcd 等不可减信息？** → 必须用线段树。BIT 的前缀相减要求信息可逆（如加法），max/min 不可逆。
4. **是否有多重标记（add+set 同时存在）？** → 线段树。BIT 无法优雅处理多重惰性标记。
5. **空间极度紧张+N 较小？** → BIT 用更少数组。线段树通常需要 4N 空间，BIT 只需 N。
6. **是否需要非递归实现以压常数？** → BIT 天然非递归；线段树的 zkw/非递归变体也可用但代码复杂度增加。

**一句话总结**：BIT 是"有损压缩"的线段树——它只保留了前缀和的信息能力，以此换取更简单的实现和更小的常数。能用 BIT 就不用线段树，但当你需要维护不可减信息或复杂标记时，线段树是唯一选择。

#### 5. Lazy 标记下传时机的严格讨论

**核心结论**：pushdown 在下述两种情况下必须调用——(1) **更新前**：当前节点的子节点即将被递归修改；(2) **查询前**：当前节点的子节点即将被访问以获取准确信息。具体代码模式：在 `update` 函数中，判断"不完全覆盖"后、递归子节点前调用 pushdown；在 `query` 函数中，判断"不完全覆盖"后、递归子节点前调用 pushdown。常见错误是只在 update 中 pushdown 而忘记 query 中也 pushdown——这会导致查询结果漏掉未下推的标记。另一个微妙之处：在 maintain（或 pushup）时，如果当前节点有标记，标记的效果应该已经在当前节点的 sumv 等值中体现了；pushdown 只是把这些标记传递给子节点，不改变当前节点的聚合值。

#### 6. 线段树实现方式对比：数组下标 vs 指针

**数组下标（堆式存储）**：根节点下标 1，节点 o 的左子为 2o、右子为 2o+1。优点：代码简单、不需要动态内存分配、缓存友好（连续内存）、不会出现内存泄漏。缺点：空间需要 4N 保证安全（最坏 2^(ceil(log₂ N)+1)），N 极大（如 10^9 且操作稀疏）时不可用。

**动态开点指针**：每个节点是 new 出来的对象，左右子为指针。优点：空间与操作次数成正比，N 很大但操作少时（如 N=10^9, Q=10^5）非常高效（动态开点线段树典型应用）。缺点：指针跳转增加缓存缺失、需要手动管理内存释放、代码稍复杂。

**选择建议**：静态问题（N 已知且不超过约 2×10^5）用数组下标；N 极大但操作稀疏时用动态开点指针。

### 知识脉络

```
单点修改+前缀和 ──→ 树状数组(lowbit驱动) ──→ 任意区间求和(差分)
                                          │
                    ┌──────────────────────┘
区间修改+区间查询 ──┤
                    └──→ 线段树
                          ├── 单惰性标记(add/set)
                          ├── 双重标记(add+set, 注意优先级)
                          └── 区间合并信息(sum/min/max组合)
```

**本书跨章节连接**：线段树是整本书的"瑞士军刀"——在第 1.4 节（DP）中，线段树用于优化 DP 转移（以区间最值加速递推）；在第 3.7 节（树算法）中，**树链剖分**将树上路径映射为线段树的连续区间；在第 3.11 节（可持久化）中，线段树的可持久化版本（主席树）支持历史版本查询和区间第 K 小。BIT 的 **lowbit 二进制分解**与第 1.3 节中"将整数拆成二进制位"的思路一脉相承。

### 快速上手模板

```cpp
// 树状数组核心
inline int lowbit(int x) { return x & -x; }
void add(int x, int v) {
    while (x <= N) C[x] += v, x += lowbit(x);
}
int sum(int x) {
    int s = 0;
    while (x > 0) s += C[x], x -= lowbit(x);
    return s;
}

// 线段树核心（pushdown模式）
void pushdown(int o, int L, int R) {
    if (addv[o] == 0) return;  // 无标记
    int M = (L + R) / 2;
    addv[o<<1] += addv[o], sumv[o<<1] += addv[o] * (M - L + 1);
    addv[o<<1|1] += addv[o], sumv[o<<1|1] += addv[o] * (R - M);
    addv[o] = 0;  // 标记清零
}
void update(int o, int L, int R, int qL, int qR, int v) {
    if (qL <= L && R <= qR) { addv[o] += v; sumv[o] += v * (R - L + 1); return; }
    pushdown(o, L, R);  // ★ 递归前必须下推
    int M = (L + R) / 2;
    if (qL <= M) update(o<<1, L, M, qL, qR, v);
    if (qR > M)  update(o<<1|1, M+1, R, qL, qR, v);
    sumv[o] = sumv[o<<1] + sumv[o<<1|1];
}
```

## 例题7  乒乓比赛（Ping pong, Beijing 2008, LA4329）

### 题目描述
一条街上有N个乒乓球爱好者，每个人有一个能力值a[i]（互不相同）。要选出三个人组成一场比赛：一个裁判和两个选手。裁判必须站在两个选手之间（位置i满足 `left < i < right`，left和right分别为两个选手的位置），且裁判的能力值必须介于两个选手的能力值之间（`min(a[left], a[right]) < a[i] < max(a[left], a[right])`）。求**有多少种不同的比赛组合方案**（选手和裁判的人选与位置均不同即视为不同方案）。

- **输入格式**：第一行为T（测试组数）。每组数据第一行为N（人数），第二行N个整数表示各人的能力值。
- **输出格式**：每组一行，输出方案总数。
- **约束**：N ≤ 20000，能力值 ≤ 100000。

### 解题思路
枚举每个位置i作为裁判，问题转化为：
1. **计算C[i]**：位置i左边有多少人能力值小于a[i]（则左边大于a[i]的人数 = i-1-C[i]）
2. **计算D[i]**：位置i右边有多少人能力值小于a[i]（则右边大于a[i]的人数 = N-i-D[i]）
3. **组合计数**：以i为裁判的方案数 = `C[i] * (N-i-D[i]) + (i-1-C[i]) * D[i]`。含义：左边选一个小的+右边选一个大的 + 左边选一个大的+右边选一个小的。
4. **使用树状数组**：能力值范围有限（≤100000），可用BIT作为"出现次数计数器"。
   - 正向扫描计算C[i]：对于位置i，查询BIT中能力值小于a[i]的元素个数（`sum(a[i]-1)`），然后 `add(a[i], 1)` 标记a[i]出现
   - 反向扫描计算D[i]：同理，从N到1遍历
5. 最后对每个非边界位置i（1<i<N），累加方案数。

### 算法方法
**树状数组（Binary Indexed Tree / Fenwick Tree）**：支持单点增加和前缀和查询，用于动态统计能力值的出现次数。时间复杂度O(log MAXA)每次操作。利用BIT统计"左边/右边有多少个元素值小于当前元素"的经典计数技巧。

### 复杂度分析
- **时间复杂度**：O(N log MAXA)，每个位置进行一次BIT查询和一次BIT更新，log(1e5) ≈ 17。
- **空间复杂度**：O(MAXA + N)，BIT数组大小约1e5+4，A、C、D数组各N+4。

```cpp
// 例题7  乒乓比赛（Ping pong, Beijing 2008, LA4329）
// 陈锋
// 题目：选3人（裁判在中间，能力介于两选手之间），求方案数
// 算法：枚举裁判，树状数组统计左右两边小于当前能力值的人数
#include <cassert>
#include <iostream>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
typedef long long LL;

// 树状数组模板：支持单点增加 add(i,v) 和前缀和查询 sum(i)
template <typename T, size_t SZ>
struct BIT {
  T C[SZ];       // 树状数组内部存储
  size_t N;      // 数组有效大小
  inline void init(size_t sz) {
    N = sz;
    assert(N + 1 < SZ);
    fill_n(C, N + 1, 0);  // 清零所有位置
  }
  inline int lowbit(int x) { return x & -x; }  // 取最低位1：x & (-x)
  // 查询前缀和：Σ(k=1→i) C[k]
  inline T sum(size_t i) {
    T ans = 0;
    while (i > 0) ans += C[i], i -= lowbit(i);
    return ans;
  }
  // 单点增加：在位置i加上v
  inline void add(size_t i, const T& v) {
    while (i <= N) C[i] += v, i += lowbit(i);
  }
};

const int MAXN = 20000 + 4, MAXA = 1e5;
int A[MAXN], C[MAXN], D[MAXN];  // A: 能力值, C[i]: 左侧小于A[i]的个数, D[i]: 右侧小于A[i]的个数
/*
  枚举i为裁判时：
  - 左边有 C[i] 个能力值小于 a[i]，(i-1)-C[i] 个大于 a[i]
  - 右边有 D[i] 个能力值小于 a[i]，(N-i)-D[i] 个大于 a[i]
  - 方案数 = 左小 × 右大 + 左大 × 右小
            = C[i]*(N-i-D[i]) + (i-1-C[i])*D[i]
*/
int main() {
  int T, N;
  ios::sync_with_stdio(false), cin.tie(0);
  cin >> T;
  BIT<int, MAXA + 4> X;  // 树状数组，值为出现次数
  while (T--) {
    cin >> N, fill_n(C, N + 1, 0);
    X.init(MAXA);  // 初始化树状数组（能力值范围为1~MAXA）
    // 正向扫描：计算每个位置左边有多少个能力值小于A[i]的
    _rep(i, 1, N) {
      cin >> A[i];
      C[i] = X.sum(A[i] - 1);  // 查询当前已出现的、小于A[i]的元素个数
      X.add(A[i], 1);           // 标记A[i]已出现（计数+1）
    }
    X.init(MAXA);  // 重新初始化，准备反向扫描
    LL ans = 0;
    // 反向扫描：计算每个位置右边有多少个能力值小于A[i]的，同时累加方案数
    for (int i = N; i >= 1; i--) {
      int d = X.sum(A[i] - 1);  // 查询右侧已出现的、小于A[i]的元素个数
      X.add(A[i], 1);            // 标记A[i]已出现
      if (i < N && i > 1)  // 裁判不能是边界位置（左右都必须有选手）
        ans += C[i] * (N - i - d) + (i - 1 - C[i]) * d;
    }
    cout << ans << endl;
  }
  return 0;
}
// Accepted 719ms 1184kB 1504 G++2020-12-13 20:47:28 22208011
```

## 例题11  山脉（Mountains, IOI05, SPOJ NKMOU）

### 题目描述
给定N座山排成一列，每座山有一个初始高度。需要支持两种操作：
- **I a b d**：将区间 [a, b] 内所有山的高度**增加** d（d 可正可负，正表示抬升，负表示降低/侵蚀）
- **Q h**：查询从左到右扫描时，前缀和（累计高度变化）**首次超过 h** 的最右位置。即找到最大的r使得前缀和 `sum[1..r] ≤ h`，返回这个r。

- **输入格式**：第一行为N（山的数量）。接下来若干行，每行一个操作（I或Q），以 `E` 结束。
- **输出格式**：对每个Q操作，输出一行结果。
- **约束**：N及操作数在合理范围，高度变化值可正可负。

### 解题思路
这是一个**带区间修改的线段树+特殊查询**问题。核心挑战在于将区间增加操作和"前缀和不超过h的最长前缀"查询结合起来。

1. **线段树节点维护两个关键信息**：
   - `sum`：区间内所有元素的和（即区间总高度增量）
   - `maxp`：该区间内所有**前缀（从区间左端点开始）的最大非负值**。这个值用于快速判断"前缀和是否超过h"

2. **区间修改**：使用惰性标记（lazy propagation）。当某个区间被整体设为相同值v时（set操作），不需要递归到叶子节点，直接在节点上设置标记并删除子节点。

3. **maxp的维护（maintain）**：对于节点p，`p.maxp = max(left.maxp, left.sum + right.maxp)`。含义：最大非负前缀要么完全在左子区间内，要么跨越左右（左区间全取 + 右区间的前缀）。

4. **查询query(h)**：从根节点开始，判断h与当前节点maxp的关系：
   - 若 `h ≥ p.maxp`：整个区间的前缀和都不超过h，返回整个区间的右端点R
   - 若p是叶子节点（所有元素等值v）：返回 `L + (h/v) - 1`（按比例计算能覆盖到哪）
   - 否则判断左侧：若 `h ≥ left.maxp`，说明能越过左边，递归到右子树；否则只能在左子区间内

5. **动态分配节点**：使用指针实现的线段树，每个节点通过 `new Node()` 动态分配，`isleaf()` 判断是否为叶子节点（没有左右孩子的节点代表整个区间值相同）。

### 算法方法
**线段树（Segment Tree）**：动态开点 + 惰性标记（区间设置/赋值）。节点维护区间和 `sum` 和最大非负前缀 `maxp`。通过 `maxp` 实现对"前缀和不超过h的最长位置"的O(log N)查询。区间修改时使用 `setval` 统一设置区间值并惰性删除子树。

### 复杂度分析
- **时间复杂度**：每次修改 O(log N)，每次查询 O(log N)（在树上二分查找最长前缀）。
- **空间复杂度**：O(N)，线段树节点数与操作中的修改区间数成正比，接近O(N log N)级别。

```cpp
// 例题11  山脉（Mountains, IOI05, SPOJ NKMOU）
// 陈锋
// 题目：区间增加高度（可正可负），查询前缀和首次超过h的位置
// 算法：线段树维护区间和与最大非负前缀，支持区间赋值和树上二分查询
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;
struct Node {
  LL sum, maxp;       // 区间和, 该区间内最大非负前缀和
  Node *left, *right; // 左右子节点指针（动态分配）
  int val;            // 惰性标记值（该区间所有元素设置为此值）
  // 判断是否为叶子节点：没有子节点的节点代表整个区间值相同
  inline bool isleaf() { return !left && !right; }
  inline void init() { memset(this, 0, sizeof(Node));}
  // 删除子节点并释放内存
  inline void delchildren() {
    if (left) delete left;
    if (right) delete right;
    left = right = nullptr;
  }
  ~Node() { delchildren(); } // 析构函数：delete时自动清理子节点
};
typedef Node* PN;
int N;
PN root;

// 维护节点信息：从子节点的sum和maxp计算当前节点
void maintain(Node& p) {
  p.sum = p.left->sum + p.right->sum;
  // 最大非负前缀 = max(仅左子区间的最大非负前缀, 左子区间全部 + 右子区间的最大非负前缀)
  p.maxp = max(p.left->maxp, p.left->sum + p.right->maxp);
}

// 区间[L,R]全部设置为值v，同时删除子树（惰性标记）
void setval(Node& p, int v, int L, int R) {
  assert(L <= R);
  p.sum = (LL)(p.val = v) * (R - L + 1);  // 区间和 = v × 区间长度
  p.maxp = max(0LL, p.sum);               // 最大非负前缀 = max(0, 区间和)
  p.delchildren();  // 设置标记后删除子节点（此后该节点视为叶子）
}

// 惰性标记下推：创建左右子节点并设置其值
void pushdown(Node& p, int L, int R) {
  int M = (L + R) / 2;
  p.left = new Node(), p.right = new Node();
  setval(*(p.left), p.val, L, M), setval(*(p.right), p.val, M + 1, R);
}

// 区间修改：将[l,r]内所有元素设置为v
void modify(int l, int r, int v, Node& p = *root, int nL = 1, int nR = N) {
  int M = (nL + nR) / 2;
  if (l <= nL && nR <= r) {  // 当前区间完全被覆盖 → 直接设置标记
    setval(p, v, nL, nR);
    return;
  }
  if (p.isleaf()) pushdown(p, nL, nR);  // 当前区间内值相同 → 先下推再修改
  if (l <= M) modify(l, r, v, *(p.left), nL, M);  // 递归左子区间
  if (r > M) modify(l, r, v, *(p.right), M + 1, nR);  // 递归右子区间
  maintain(p);  // 回溯时维护节点信息
}

// 查询前缀和<=h的最长前缀的右端点位置（树上二分查找）
int query(LL h, Node& p = *root, int L = 1, int R = N) {
  if (h >= p.maxp) return R;  // 整个区间的最大非负前缀都不超过h → 全部可取
  if (p.isleaf())             // 叶子节点：区间内值都相同(=p.val)
    return L + (h / p.val) - 1;  // 按比例计算能取到几个元素
  int M = (L + R) / 2;
  Node& pl = *(p.left);
  // 判断h是否大于等于左子区间的最大非负前缀
  return h >= pl.maxp
    ? query(h - pl.sum, *(p.right), M + 1, R)  // 能越过左边 → 递归右边继续找
    : query(h, pl, L, M);                        // 左边不够 → 只能在左子区间内
}

void dbgprint(Node& p = *root, int L = 1, int R = N) { // 打印数组，调试用
  if (p.isleaf()) {
    for (int i = L; i <= R; i++) printf("%d ", p.val);
    return;
  }
  int M = (L + R) / 2;
  dbgprint(*(p.left), L, M), dbgprint(*(p.right), M + 1, R);
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  cin >> N;
  string s;
  root = new Node();  // 创建根节点
  for (int a, b, d, h; cin >> s && s[0] != 'E'; ) {
    if (s[0] == 'I') cin >> a >> b >> d, modify(a, b, d);  // 区间增加
    else cin >> h, cout << query(h) << endl;                // 查询前缀和<=h的最长前缀
  }
  delete root;  // 释放根节点（析构函数递归释放所有子节点）
  return 0;
}
// 25407608 2020-02-16 07:12:57 Feng Chen IOI05 Mountains 100 2.62 169M CPP14
```

## 例题8  频繁出现的数值（Frequent Values, UVa 11235）

### 题目描述
给定一个长度为n的**非递减排列**的整数数组。有q个查询，每个查询给出区间[L, R]（1-based），求该区间内**出现次数最多的数值的出现次数**（即最高频次）。

- **输入格式**：多组测试数据。每组第一行为 n 和 q（n=0时结束），第二行为n个整数（非递减），接下来q行每行L, R。
- **输出格式**：每个查询输出一行结果。
- **约束**：n, q ≤ 100000，数组元素值在 int 范围内且非降序排列。

### 解题思路
数组的非递减性质意味着相同数值一定在连续的段中。利用**分段 + RMQ**解决：

1. **预处理分段**：将数组按相同数值划分为连续的"段"。每段记录其长度（即该数值的出现次数）。对于每个位置i，记录：
   - `num[i]`：位置i所属的段编号
   - `left[i]`：该段的最左位置（段起点）
   - `right[i]`：该段的最右位置（段终点）

2. **RMQ建立**：对段长度数组建立Sparse Table，支持O(1)查询任意段编号区间内的最大长度。

3. **查询处理**（[L,R]区间内最高频次数）：
   - 若L和R在同一段内（`num[L] == num[R]`）：整个区间内数值相同，答案为 `R-L+1`
   - 否则分为三部分：
     - **左边不完整段**：L到其段终点，长度 = `right[L] - L + 1`
     - **右边不完整段**：其段起点到R，长度 = `R - left[R] + 1`
     - **中间完整段**：段编号区间 `[num[L]+1, num[R]-1]`，用RMQ查最大段长度
   - 答案 = max(左边长度, 右边长度, 中间RMQ最大值)

### 算法方法
**分段预处理 + RMQ（Sparse Table / ST表）**：先利用非递减特性将数组分成连续相同值的段，将问题转化为对段长度的RMQ查询。Sparse Table是静态RMQ的经典方法，预处理O(N log N)，查询O(1)。

### 复杂度分析
- **时间复杂度**：预处理 O(N log N)（分段O(N) + RMQ构建O(N log N)），每次查询O(1)。
- **空间复杂度**：O(N log N)，RMQ表需要N×logN的空间（100000 × 17 ≈ 1.7M个int）。

```cpp
// 例题8  频繁出现的数值（Frequent Values, UVa 11235）
// Rujia Liu
// 题目：非递减数组中查询区间内出现最频繁的数值的出现次数
// 算法：将相同值分段，转化为对段长度的RMQ（区间最大值）查询
#include<cstdio>
#include<algorithm>
#include<vector>
using namespace std;

const int maxn = 100000 + 5;
const int maxlog = 20;  // log2(100000) ≈ 17

// Sparse Table：查询区间最大值
struct RMQ {
  int d[maxn][maxlog];  // d[i][j] 表示以i为起点、长度为2^j的区间内的最大值
  // 初始化Sparse Table
  void init(const vector<int>& A) {
    int n = A.size();
    // 长度为1的区间（2^0）：就是A[i]本身
    for(int i = 0; i < n; i++) d[i][0] = A[i];
    // 倍增构建：长度为2^j的区间分成两个长度为2^(j-1)的区间
    for(int j = 1; (1<<j) <= n; j++)
      for(int i = 0; i + (1<<j) - 1 < n; i++)
        d[i][j] = max(d[i][j-1], d[i + (1<<(j-1))][j-1]);
  }

  // 查询区间[L,R]的最大值（0-based）
  int query(int L, int R) {
    int k = 0;
    // 找到最大的k使得 2^k ≤ R-L+1
    while((1<<(k+1)) <= R-L+1) k++;
    // 用两个长度为2^k的区间覆盖整个查询区间
    return max(d[L][k], d[R-(1<<k)+1][k]);
  }
};

int a[maxn];       // 原始数组（非递减）
int num[maxn];     // num[i]：位置i所属的段编号
int left[maxn];    // left[i]：位置i所在段的最左位置
int right[maxn];   // right[i]：位置i所在段的最右位置
RMQ rmq;

int main() {
  int n, q;
  while(scanf("%d%d", &n, &q) == 2) {
    for(int i = 0; i < n; i++) scanf("%d", &a[i]);
    a[n] = a[n-1] + 1; // 哨兵：保证最后一个元素与前面不同，触发最后一段的结束
    int start = -1;
    vector<int> count;  // 存储每段的长度
    // 扫描数组，划分连续相同值的段
    for(int i = 0; i <= n; i++) {
      if(i == 0 || a[i] > a[i-1]) {  // 新段开始（利用非递减性质：变化代表新段）
        if(i > 0) {
          count.push_back(i - start);  // 上一段的长度
          for(int j = start; j < i; j++) {
            num[j] = count.size() - 1;  // 段编号
            left[j] = start;            // 段左边界
            right[j] = i-1;             // 段右边界
          }
        }
        start = i;  // 新段的起始位置
      }
    }
    rmq.init(count);  // 对段长度建立RMQ
    while(q--) {
      int L, R, ans;
      scanf("%d%d", &L, &R); L--; R--;  // 转为0-based
      if(num[L] == num[R]) ans = R - L + 1;  // 同一段内 → 整个区间都是同一个值
      else {
        // 左边不完整段 + 右边不完整段
        ans = max(R - left[R] + 1, right[L] - L + 1);
        // 中间完整段：用RMQ查最大段长度
        if(num[L] + 1 < num[R])
          ans = max(ans, rmq.query(num[L] + 1, num[R] - 1));
      }
      printf("%d\n", ans);
    }
  }
  return 0;
}
// 25877221  11235  Frequent values  Accepted  C++  0.090  2020-12-23 03:51:01
```

## 例题10  快速矩阵操作（Fast Matrix Operations, UVa 11992）

### 题目描述
给定一个 r 行 c 列的矩阵，初始所有元素为 0。需要支持 m 个操作，操作类型有 3 种：
1. **1 x1 y1 x2 y2 v**（ADD）：将子矩阵 [(x1,y1), (x2,y2)] 内所有元素**加上** v
2. **2 x1 y1 x2 y2 v**（SET）：将子矩阵 [(x1,y1), (x2,y2)] 内所有元素**设置为** v
3. **3 x1 y1 x2 y2**（QUERY）：查询子矩阵 [(x1,y1), (x2,y2)] 的**总和**、**最小值**和**最大值**

- **输入格式**：多组测试数据。每组第一行 r, c, m，接下来 m 行操作。
- **输出格式**：对每个类型 3 操作，输出一行三个整数：`sum min max`。
- **约束**：r ≤ 20，c ≤ 10^6，操作数很大，v 在合理范围内。

### 解题思路
关键观察：**行数 r ≤ 20（很小），列数 c 可达 10^6**。因此可以对每一行建立独立的线段树。

1. **每行一个线段树**：共 r 棵线段树，每棵维护一行的 c 个元素。矩阵操作转化为逐行的线段树操作。

2. **线段树节点维护三种信息**（NodeInfo）：
   - `minv`：区间最小值
   - `maxv`：区间最大值
   - `sumv`：区间总和

3. **双重惰性标记**：
   - `addv[o]`：加法标记（区间所有元素加上该值）
   - `setv[o]`：赋值标记（区间所有元素设置为该值）
   - `isSet[o]`：标记节点是否有赋值操作（SET 优先于 ADD，因为赋值覆盖了之前的累加）

4. **maintain 维护**：将子节点信息合并（通过 `operator+`），然后应用当前节点的加法和赋值标记。注意：赋值标记和加法标记不会同时生效 —— 有了赋值标记后，加法标记被清除。

5. **pushdown 下推**：将父节点的标记传递给左右子节点。SET 标记优先传递，ADD 标记累积。

6. **update 更新**：根据 op 类型（1=add, 2=set），递归更新覆盖区间内的节点。

7. **query 查询**：递归查询，返回区间段的信息（sum, min, max），通过 `operator+` 合并。

### 算法方法
**线段树（Segment Tree）**：支持区间加法和区间赋值两种操作的线段树。使用双重惰性标记（addv + setv），维护区间和/最小值/最大值。每行独立建树，行间用循环串联。`isSet` 标记用于区分"是否进行了赋值操作"，因为赋值操作优先级高于加法操作。

### 复杂度分析
- **时间复杂度**：O(m × r × log c)，每个操作需要在 r 行上各执行一次线段树操作，每次 O(log c)。
- **空间复杂度**：O(r × c)，r 棵线段树，每棵约 2c 个节点（但代码使用了大约 r × 2c 的数组）。

```cpp
// 例题10  快速矩阵操作（Fast Matrix Operations, UVa 11992）
// 陈锋
// 题目：矩阵支持子矩阵加法、赋值、查询总和/最小值/最大值
// 算法：每行一棵线段树，支持区间加法和区间赋值双重操作
#include <bits/stdc++.h>

using namespace std;

const int MAXC = 1e6 + 4, INF = 1e9;

// 线段树节点信息：区间的最小值、最大值、总和
struct NodeInfo {
  int minv, maxv, sumv;
};
// 两个节点信息合并（用于查询结果的合并）
NodeInfo operator+(const NodeInfo &n1, const NodeInfo &n2) {
  return {min(n1.minv, n2.minv), max(n1.maxv, n2.maxv), n1.sumv + n2.sumv};
}

// 线段树：支持区间加法和区间赋值
struct IntervalTree {
  NodeInfo nodes[MAXC];  // 节点数组（线段树用数组实现，根节点为1）
  int setv[MAXC], addv[MAXC], qL, qR;  // setv: 赋值标记, addv: 加法标记, qL/qR: 查询区间
  bitset<MAXC> isSet;  // 标记每个节点是否有赋值操作

  // 对节点o设置赋值标记（同时清除加法标记）
  inline void setFlag(int o, int v) { setv[o] = v, isSet.set(o), addv[o] = 0; }

  void init(int n) {
    int sz = n * 2 + 2;  // 线段树节点数（完全二叉树约2n）
    fill_n(addv, sz, 0);
    isSet.reset();
    isSet.set(1);  // 根节点初始被设置为0（通过isSet标记）
    memset(nodes, 0, sizeof(NodeInfo) * sz);
  }

  // 维护节点o的信息：合并左右子节点 + 应用当前节点的标记
  inline void maintain(int o, int L, int R) {
    int lc = o * 2, rc = o * 2 + 1, a = addv[o], s = setv[o];
    NodeInfo &nd = nodes[o], &li = nodes[lc], &ri = nodes[rc];
    if (R > L) nd = li + ri;  // 非叶子节点：合并左右子节点信息
    if (isSet[o]) nd = {s, s, s * (R - L + 1)};  // 有赋值标记：覆盖为s
    if (a) nd.minv += a, nd.maxv += a, nd.sumv += a * (R - L + 1);  // 有加法标记：整体增加a
  }

  // 下推标记：将当前节点的标记推给左右子节点
  inline void pushdown(int o) {
    int lc = o * 2, rc = o * 2 + 1;
    if (isSet[o])
      setFlag(lc, setv[o]), setFlag(rc, setv[o]), isSet.reset(o);  // 赋值标记下传
    if (addv[o])
      addv[lc] += addv[o], addv[rc] += addv[o], addv[o] = 0;  // 加法标记下传（累加）
  }

  // 区间更新：op=1 加v, op=2 赋值为v
  void update(int o, int L, int R, int op, int v) {
    int lc = o * 2, rc = o * 2 + 1, M = L + (R - L) / 2;
    if (qL <= L && qR >= R) {  // 当前区间完全覆盖
      if (op == 1) addv[o] += v;  // 加法：累加标记
      else setFlag(o, v);          // 赋值：设置标记
    } else {
      pushdown(o);  // 先下推标记再递归
      if (qL <= M) update(lc, L, M, op, v);
      else maintain(lc, L, M);  // 不需要更新的子节点也要维护
      if (qR > M) update(rc, M + 1, R, op, v);
      else maintain(rc, M + 1, R);
    }
    maintain(o, L, R);  // 回溯时维护当前节点
  }

  // 区间查询：返回区间信息（sum, min, max）
  NodeInfo query(int o, int L, int R) {
    int lc = o * 2, rc = o * 2 + 1, M = L + (R - L) / 2;
    maintain(o, L, R);  // 先确保当前节点信息准确
    if (qL <= L && qR >= R) return nodes[o];  // 完全覆盖

    pushdown(o);  // 否则下推标记
    NodeInfo li = {INF, -INF, 0}, ri = {INF, -INF, 0};
    if (qL <= M) li = query(lc, L, M);
    else maintain(lc, L, M);
    if (qR > M) ri = query(rc, M + 1, R);
    else maintain(rc, M + 1, R);
    return li + ri;  // 合并左右查询结果
  }
};

const int maxr = 20 + 5;
IntervalTree tree[maxr];  // 每行一棵线段树（r ≤ 20）

int main() {
  for (int r, c, m; scanf("%d%d%d", &r, &c, &m) == 3;) {
    // 初始化每行的线段树
    for (int x = 1; x <= r; x++) tree[x].init(c);
    for (int i = 0, op, x1, y1, x2, y2, v; i < m; i++) {
      scanf("%d%d%d%d%d", &op, &x1, &y1, &x2, &y2);
      if (op < 3) {  // ADD 或 SET 操作
        scanf("%d", &v);
        for (int x = x1; x <= x2; x++) {  // 逐行更新
          IntervalTree &tx = tree[x];
          tx.qL = y1, tx.qR = y2;
          tx.update(1, 1, c, op, v);  // op=1: add, op=2: set
        }
      } else {  // QUERY 操作
        NodeInfo gi = {INF, -INF, 0};  // 初始化累加结果
        for (int x = x1; x <= x2; x++) {  // 逐行查询
          IntervalTree &tx = tree[x];
          tx.qL = y1, tx.qR = y2;
          gi = gi + tx.query(1, 1, c);  // 合并每行的查询结果
        }
        printf("%d %d %d\n", gi.sumv, gi.minv, gi.maxv);
      }
    }
  }
  return 0;
}
// Accepted 550ms 2968 C++5.3.02020-12-1321:05:39 25843628
```

## 例题12  堆内存管理器（Heap Manager, UVa12419）

### 题目描述
模拟一个内存分配系统的运作。内存共有N个连续的块（0到N-1），初始全部空闲。系统处理进程的内存请求，每个进程有三个参数：到达时间t、所需内存大小m、使用时长p。规则如下：
- 新进程到达时，如果当前空闲内存中存在连续的、长度≥m的空闲区间，则**立即分配**（分配最靠左的满足条件的区间），该内存在使用时长p后自动释放
- 如果无法立即分配，进程进入**等待队列**。当有内存被释放时，检查等待队列中是否有进程可以被分配
- 需要输出每次分配的时间和位置，以及最终等待队列中进程的总数
- 输入以 `0 0 0` 标记结束

- **输入格式**：第一行N和b（b=1时输出每次分配详情，b=0时不输出）。接下来每行 t m p 表示进程。
- **输出格式**：两行，第一行为最后一个释放事件的时间，第二行为进入过等待队列的进程总数。
- **约束**：N可达10^9级别，但进程数有限（内存按时间分配/释放）。

### 解题思路
本题是**内存分配器模拟**，核心数据结构为**支持区间赋值+最长连续0区间查询的线段树**。由于N可能很大（10^9），但操作次数有限，使用**动态开点线段树**（指针实现）。

1. **线段树节点维护**：
   - `lz`：该区间从前缀开始的最长连续0的长度
   - `rz`：该区间从后缀开始的最长连续0的长度
   - `mz`：该区间内任意位置的最长连续0的长度
   - `setv`：惰性标记，0表示空闲，1表示占用，-1表示无标记

2. **关键操作**：
   - `set([l,r], v)`：区间赋值（0=释放，1=分配）
   - `query(len)`：查询最靠左的长度≥len的连续0区间的起始位置

3. **query实现**（寻找最左满足条件的空闲区间）：
   - 若 `lz ≥ len`：返回当前区间的左端点
   - 否则检查左子区间：若 `left.mz ≥ len`，递归左子区间
   - 否则检查中间跨区间段：若 `left.rz + right.lz ≥ len`，返回 `m - left.rz + 1`
   - 否则递归右子区间

4. **事件驱动模拟**：
   - 使用优先队列 `EQ` 维护释放事件（按时间排序）
   - 当有新进程到达时，先处理所有时间≤t的释放事件
   - 每次释放后尝试从等待队列 `Q` 中分配内存
   - 无法立即分配的进程放入等待队列

### 算法方法
**线段树（动态开点 Segment Tree） + 事件驱动模拟**：线段树维护连续0区间信息（经典的最大连续0子段和），支持区间赋值和二分查找。配合优先队列（释放事件）和队列（等待列表）实现内存分配器的时序模拟。

### 复杂度分析
- **时间复杂度**：O(P log N)，P为进程数。每次线段树操作O(log N)（动态开点保证只创建必要的节点）。
- **空间复杂度**：O(P log N)，线段树节点数量与操作涉及的区间数成正比。

```cpp
// 例题12  堆内存管理器（Heap Manager, UVa12419）
// 陈锋
// 题目：模拟内存分配系统，支持请求分配和定时释放
// 算法：动态开点线段树维护最大连续0区间，事件驱动模拟释放
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)
typedef long long LL;
const LL INF = 1ll << 60;

// 线段树节点（指针实现，动态开点）
struct IntTreeNode {
  IntTreeNode *lc, *rc;   // 左右子节点
  int setv;               // 惰性标记：0=空闲, 1=占用, -1=无标记
  int lz, rz, mz;         // 左端连续0长度, 右端连续0长度, 区间内最长连续0长度
  IntTreeNode() : lc(nullptr), rc(nullptr) { }
  inline void delchildren() {
    if (lc) delete lc;
    if (rc) delete rc;
    lc = rc = nullptr;
  }
  ~IntTreeNode() { delchildren(); }

  // 对整个区间[l,r]设置值v（0=空闲，1=占用）
  void mark(int l, int r, int v) {
    lz = rz = mz = (v == 0 ? r - l + 1 : 0);  // 空闲则全为0长度，占用则0长度为0
    setv = v;
    delchildren();  // 设置标记后删除子节点（惰性）
  }

  // 对子节点p设置标记（若p不存在则先创建）
  void mark(IntTreeNode* &p, int l, int r, int v) {
    if (!p) p = new IntTreeNode();
    p->mark(l, r, v);
  }

  // 标记下推：将setv标记推给左右子节点
  void pushdown(int l, int r) {
    int m = l + (r - l) / 2;
    if (setv == -1) return;  // 无标记，无需下推
    mark(lc, l, m, setv);
    mark(rc, m + 1, r, setv);
    setv = -1;  // 清除当前节点标记
  }

  // 区间赋值：将[ql,qr]区间设置为v
  void set(int l, int r, int ql, int qr, int v) {
    if (ql <= l && r <= qr) { mark(l, r, v); return; }  // 完全覆盖
    pushdown(l, r);
    int m = l + (r - l) / 2;
    IntTreeNode &ld = *(lc), &rd = *(rc);
    if (ql <= m) ld.set(l, m, ql, qr, v);    // 递归左子区间
    if (qr > m) rd.set(m + 1, r, ql, qr, v); // 递归右子区间
    // 回溯维护：合并左右子区间的信息
    lz = (ld.lz == m - l + 1) ? ld.lz + rd.lz : ld.lz;
    rz = (rd.rz == r - m) ? rd.rz + ld.rz : rd.rz;
    mz = max(max(ld.mz, rd.mz), ld.rz + rd.lz);  // 左子后缀 + 右子前缀
  }

  // 查询区间[l,r]中最靠左的长度≥len的连续0区间的起始位置
  int query(int l, int r, int len) {
    if (lz >= len) return l;  // 前缀满足条件 → 直接返回左端点
    pushdown(l, r);
    IntTreeNode &ld = *lc, &rd = *rc;
    int m = l + (r - l) / 2;
    if (ld.mz >= len) return ld.query(l, m, len);              // 完全在左子区间
    if (ld.rz + rd.lz >= len) return m - ld.rz + 1;            // 跨左右子区间
    return rd.query(m + 1, r, len);                             // 完全在右子区间
  }
};

// 释放事件：在时间t释放区间[l,r]的内存
struct Event {
  LL t;
  int l, r;
  bool operator<(const Event& a) const { return t > a.t; }  // 小顶堆：时间早的优先
};

// 等待中的进程：所需内存len, 使用时长t, 进程编号id
struct Process { int len, t, id; };

priority_queue<Event> EQ;  // 释放事件队列（优先队列）
queue<Process> Q;          // 等待队列
IntTreeNode A;             // 线段树根节点

// 在当前时间cur为进程p分配内存
void allocate(int N, int b, LL cur, const Process& p) {
  int l = A.query(0, N - 1, p.len);               // 查找最靠左的满足条件的空闲区间
  A.set(0, N - 1, l, l + p.len - 1, 1);           // 标记为已占用
  EQ.push(Event{cur + p.t, l, l + p.len - 1});     // 登记释放事件
  if (b) printf("%lld %d %d\n", cur, p.id, l);     // 输出分配详情
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int N, b, pcnt, m, p;
  for (LL t, ans = 0; cin >> N >> b;) {
    pcnt = 0;
    A.mark(0, N - 1, 0);  // 初始化：全部空闲
    for (int i = 1;; i++) {
      cin >> t >> m >> p;  // 到达时间, 所需大小, 使用时长
      if (t == 0 && m == 0 && p == 0) t = INF;  // 输入结束标记
      // 处理所有时间≤t的释放事件
      while (!EQ.empty() && EQ.top().t <= t) {
        LL cur = EQ.top().t;
        while (!EQ.empty() && EQ.top().t == cur) {  // 同一时刻可能有多个释放
          const auto& e = EQ.top();
          ans = e.t;
          A.set(0, N - 1, e.l, e.r, 0);  // 释放内存
          EQ.pop();
        }
        // 释放后尝试从等待队列中分配
        while (!Q.empty() && Q.front().len <= A.mz)
          allocate(N, b, cur, Q.front()), Q.pop();
      }
      if (t == INF) break;  // 所有进程处理完毕
      // 当前进程的内存请求
      if (A.mz >= m) allocate(N, b, t, Process{m, p, i});  // 可以立即分配
      else Q.push(Process{m, p, i}), pcnt++;  // 加入等待队列
    }
    printf("%lld\n%d\n\n", ans, pcnt);  // 输出：最后释放时间，等待过的进程数
  }
  return 0;
}
// 24887303  12419   Heap Manager  Accepted  C++11   0.610   2020-04-17 02:50:01
```

## 例题9  动态最大连续和（Ray, Pass me the Dishes, UVa1400）

### 题目描述
给定一个长度为N的整数序列（可能有负数）。有M个查询，每个查询给出区间[L, R]，需要找出该区间内**和最大的连续子区间**。如果有多个子区间和相同且最大，选择**字典序最小**的那一个（即左端点最小的，若左端点相同则右端点最小）。

- **输入格式**：多组测试数据。每组第一行为N和M，第二行为N个整数（序列），接下来M行每行L R。
- **输出格式**：每个查询输出一行：所选的子区间左端点和右端点。
- **约束**：N, M ≤ 500000，序列元素可为负数。

### 解题思路
这是一个**静态序列的区间最大连续子段和查询**问题，使用线段树在O(log N)时间内回答每个查询。

1. **线段树节点维护三类信息**（MaxVal）：
   - `sub`：该区间内的最优子区间（和最大且字典序最小）
   - `pfx`：该区间内最优前缀的右端点（从L开始、和最大的前缀的终点位置）
   - `sfx`：该区间内最优后缀的左端点（以R结束、和最大的后缀的起点位置）

2. **build构建**：
   - 叶子节点：`sub = {i, i}`, `pfx = sfx = i`
   - 非叶子节点的合并：
     - `pfx`：取 `sum(L, left.pfx)` 和 `sum(L, right.pfx)` 中较大的（从L开始）
     - `sfx`：取 `sum(left.sfx, R)` 和 `sum(right.sfx, R)` 中较大的（从R结束）
     - `sub`：max of（左子区间sub、右子区间sub、跨越中间的 `{left.sfx, right.pfx}`），用字典序规则比较

3. **前缀和优化**：使用前缀和数组 `SD[i] = ΣA[1..i]`，区间和 `sum(L,R) = SD[R] - SD[L-1]` 可以在O(1)时间内计算。

4. **查询 query(l, r)**：
   - 如果查询区间完全在一个子区间内，递归该子区间
   - 如果跨越左右子区间，需要同时获取左子区间的 `sfx` 和右子区间的 `pfx`，加上各自子区间的 `sub`，取三者中最优的

5. **字典序规则**：当两个子区间和相等时，选择 `min(i1, i2)`（std::pair的默认比较就满足字典序要求）。

### 算法方法
**线段树（Segment Tree）**：静态维护每个区间的最优前缀/后缀/子区间信息。这是经典的最大子段和（Maximum Subarray Sum）问题的区间查询版本。结合前缀和数组实现O(1)的区间和查询，使线段树每个节点的信息合并在O(1)时间内完成。

### 复杂度分析
- **时间复杂度**：构建O(N)，每次查询O(log N)（需要递归到O(log N)个节点）。
- **空间复杂度**：O(N)，线段树约2N个节点，前缀和数组N+1个元素。

```cpp
// 例题9  动态最大连续和（Ray, Pass me the Dishes, UVa1400）
// 陈锋
// 题目：查询区间内和最大的连续子区间，要求字典序最小
// 算法：线段树维护每个区间的最优子区间/前缀/后缀信息
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
typedef long long LL;
typedef pair<int, int> Interval;
const int MAXN = 5e5 + 4;
LL SD[MAXN];  // 前缀和数组：SD[i] = A[1]+...+A[i]

// O(1)计算区间和 [L,R]
inline LL sum(int L, int R) {
  return SD[R] - SD[L - 1];
}
inline LL sum(const Interval& i) { return sum(i.first, i.second); }

// 比较两个子区间，返回字典序更小（或和更大）的那个
inline Interval maxI(const Interval& i1, const Interval& i2) {
  LL s1 = sum(i1), s2 = sum(i2);
  if (s1 != s2) return s1 > s2 ? i1 : i2;  // 和不同，取和大的
  return min(i1, i2);                        // 和相同，取字典序小的
}

// 线段树节点存储的信息
struct MaxVal {
  int pfx;       // 该区间的最优前缀右端点
  int sfx;       // 该区间的最优后缀左端点
  Interval sub;  // 该区间的最优子区间
};

struct IntervalTree {
  MaxVal Nodes[MAXN * 2];  // 线段树节点数组（堆式存储）
  int qL, qR, N;

  void build(int N) {
    this->N = N;
    build(1, N, 1);  // 从根节点1开始构建，覆盖[1,N]
  }

  void build(int L, int R, int O) {
    assert(L <= R);
    assert(O > 0);
    if (L == R) {  // 叶子节点：单元素区间
      Nodes[O] = {L, L, make_pair(L, L)};
      return;
    }
    int M = (L + R) / 2, lc = 2 * O, rc = 2 * O + 1;
    build(L, M, lc), build(M + 1, R, rc);
    const MaxVal &nl = Nodes[lc], &nr = Nodes[rc];
    MaxVal &no = Nodes[O];
    // 最优前缀：比较从L到左子区间前缀终点 和 从L到右子区间前缀终点的和
    no.pfx = sum(L, nl.pfx) >= sum(L, nr.pfx) ? nl.pfx : nr.pfx;
    // 最优后缀：比较从左子区间后缀起点到R 和 从右子区间后缀起点到R的和
    no.sfx = sum(nl.sfx, R) >= sum(nr.sfx, R) ? nl.sfx : nr.sfx;
    // 最优子区间：取 左子最优、右子最优、跨越中间 三者中最好的
    no.sub = maxI(nl.sub, nr.sub);
    no.sub = maxI(no.sub, make_pair(nl.sfx, nr.pfx));
  }

  // 公开查询接口：[l,r]的最优子区间
  Interval query(int l, int r) {
    assert(l <= r);
    qL = l, qR = r;
    return _query(1, N, 1);
  }

  // 递归查询
  Interval _query(const int L, const int R, const int O) {
    if (qL <= L && R <= qR) return Nodes[O].sub;  // 完全覆盖
    int M = (L + R) / 2, lc = O * 2, rc = 2 * O + 1;
    if (qR <= M) return _query(L, M, lc);          // 完全在左子区间
    if (qL > M) return _query(M + 1, R, rc);        // 完全在右子区间
    // 跨越左右子区间：合并结果
    Interval ans = make_pair(_querySfx(L, M, lc), _queryPfx(M + 1, R, rc));
    ans = maxI(ans, maxI(_query(L, M, lc), _query(M + 1, R, rc)));
    return ans;
  }

  // 查询区间内与[L,R]的指定子区间相关的最优前缀右端点
  int _queryPfx(const int L, const int R, const int O) {
    if (qL <= L && R <= qR) return Nodes[O].pfx;
    int M = (L + R) / 2, lc = 2 * O, rc = 2 * O + 1;
    if (qR <= M) return _queryPfx(L, M, lc);
    if (qL > M) return _queryPfx(M + 1, R, rc);
    int m1 = _queryPfx(L, M, lc), m2 = _queryPfx(M + 1, R, rc);
    return sum(L, m1) >= sum(L, m2) ? m1 : m2;
  }

  // 查询区间内与[L,R]的指定子区间相关的最优后缀左端点
  int _querySfx(const int L, const int R, const int O) {
    if (qL <= L && R <= qR) return Nodes[O].sfx;
    int M = (L + R) / 2, lc = O * 2, rc = 2 * O + 1;
    if (qR <= M) return _querySfx(L, M, lc);
    if (qL > M) return _querySfx(M + 1, R, rc);
    int m1 = _querySfx(L, M, lc), m2 = _querySfx(M + 1, R, rc);
    return sum(m1, R) >= sum(m2, R) ? m1 : m2;
  }
};
IntervalTree tree;

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  SD[0] = 0;
  for (int t = 1, d, a, b, N, M; cin >> N >> M; t++) {
    _rep(i, 1, N) cin >> d, SD[i] = SD[i - 1] + d;  // 构建前缀和数组
    tree.build(N);  // 构建线段树
    printf("Case %d:\n", t);
    _rep(i, 1, M) {
      cin >> a >> b;
      Interval ans = tree.query(a, b);
      printf("%d %d\n", ans.first, ans.second);
    }
  }
  return 0;
}
// Accepted 160ms 3130 C++ 5.3.0 2020-12-13 20:58:55 25843597
```
