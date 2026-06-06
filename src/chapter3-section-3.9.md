# 3.9 离线算法

> **学习目标**：掌握三大离线算法框架的底层逻辑——莫队算法的分块排序复杂度分析、CDQ 分治的"时间维归并"思想、整体二分的多查询共享判定过程——并理解它们各自的适用场景。

## 理论基础

### 为什么需要学这个？

"离线"这个词听起来像是一种妥协——"因为在线做不了，才离线处理"。但事实上，离线算法是一种**战术性思维**：当你知道所有即将到来的操作后，你就能重新排列处理顺序、批量共享中间结果，从而把看似 O(N^2) 的问题压到 O(N log N) 甚至更低。这就像是玩策略游戏时"开了全图视野"——你可以做在线算法想都不敢想的优化。不过，离线三剑客各有各的脾气：莫队玩的是"区间指针的物理移动成本"，CDQ 玩的是"时间维上的分治"，整体二分玩的是"把所有二分合并在一起做"。学通之后你会发现，它们共同的核心只有一句话：**通过重排计算顺序来消除重复工作**。

### 核心概念

#### 1. 莫队算法：块大小 √N 是怎么来的？

**一句话定义**：将所有查询按 (L/block, R) 或 (L/block, R, 奇偶交替) 排序，双指针移动区间，均摊复杂度 O(N√N)。

**本质理解**：朴素做法每问独立 O(N)，总 O(NM)，M=Q。莫队的排序让指针移动代价分散。分析上：左指针在块内移动 O(√N) 每次查询（块大小 = B），共 M * B。右指针在块间单调移动 O(N) 每块，共 (N/B) * N。总有价 = M*B + N^2/B。由均值不等式，B = N/√M 时最小，取 M≈N 时 B = √N，总 O(N√N)。

**本质理解（一句话）**：**块大小 N/√M 是"左指针块内移动代价"和"右指针块间移动代价"的平衡点**。块太大则右指针移动太多，块太小则左指针移动太多。√N 是假设 M 和 N 同阶时的最优值。

#### 2. CDQ 分治：时间维上的归并

**一句话定义**：CDQ 分治把修改和查询混合在一起，按时间分治——先递归处理左区间，再统计左区间修改对右区间查询的贡献，最后递归右区间。

**本质理解**：在线情况下，你只能"查询→获取结果→继续"。但 CDQ 说：**把所有操作按"时间中点"切开，左边先处理完（已经得到正确内部结果），然后让左边的所有修改"穿越"到右边、一起对右边的查询产生贡献**。右侧查询不需要知道左侧的修改是"哪个时刻"产生的——你只需要知道"在它之前"就够了。这就是"把时间维度消除掉"的精髓。

**最小示例**：统计动态插入过程中的逆序对数。CDQ 分治把"删除"操作倒过来看作是"插入"，然后在每个分治层中，用 BIT 做左右归并统计贡献。左边是"早插入的"（时间维度更小），右边是"晚插入的"。

#### 3. 整体二分：N 个查询共享同一遍判定

**一句话定义**：把所有查询放在同一个二分区间 [L, R] 内，共享判定过程——对当前二分值 mid，全部查询一起判断"答案是否 ≤ mid"，然后将查询分流到左右两个子区间。

**本质理解**：普通的二分答案是"每个查询单独二分一次"，但很多查询的判定过程涉及相同的中间计算（比如遍历事件序列）。整体二分把这些共享的计算提取出来：**只遍历一次 mid 前的所有事件，就能同时判定所有查询的归属**。这就像你有一堆人要去不同楼层，与其每个人单独坐一次电梯，不如让所有人都站进电梯，楼层到了就放一部分人下。

#### 4. 莫队块大小 B = √N 的最优性推导

**问题**：N 个元素，M 个查询。莫队排序后，左指针在块内移动，右指针在块间单调移动。总移动代价 = 左指针移动次数 × O(1) + 右指针移动次数 × O(1)。设块大小为 B。

**分析**：
- 左指针代价：同一块内，相邻查询的左指针移动最多 B 步，共 M 个查询。每块间切换一次左指针也最多移动 B 步。总左指针移动 = O(M × B)。
- 右指针代价：在每个块内，右指针按排序后单调移动（或奇偶交替减少回退），每个块内右指针移动 O(N)。共有 N/B 个块。总右指针移动 = O(N × N/B) = O(N²/B)。

**总代价**：T(B) = M×B + N²/B。由均值不等式，当 M×B = N²/B，即 B = N/√M 时总代价最小，最小值为 2N√M。

**特殊情形**：当 M ≈ N 时（查询数与元素数同阶），B = √N，总代价 = O(N√N)。这正是经典莫队的复杂度。当 M ≫ N 时（查询远多于元素数），B ≈ N/√M < √N，即块应该更小——因为左指针代价与查询数成正比。当 M ≪ N 时，B > √N，块应该更大——此时右指针代价主导。

#### 5. CDQ 分治解决三维偏序的标准处理流程

**问题定义**：给定 N 个三维点 (aᵢ, bᵢ, cᵢ)，对每个点 i 统计满足 aⱼ ≤ aᵢ, bⱼ ≤ bᵢ, cⱼ ≤ cᵢ 的 j 的数量。这是经典的三维偏序计数问题。

**标准流程**：
1. **第一维排序去重**：将所有点按 a 升序排序。相等的 a 值需要合并（如果问题要求严格偏序则拆开）。这一步将三维降为二维——之后只需处理 b 和 c 两维。
2. **CDQ 分治**：按 b 维度进行归并分治。递归函数 cdq(l, r) 中：(a) 若 l==r 返回；(b) m = (l+r)/2；(c) cdq(l, m)，递归处理左半；(d) 统计左半 [l,m] 对右半 [m+1,r] 的贡献——对左右两半分别按 c 排序，用 BIT 在 c 维度上做前缀和：遍历左半的点在 BIT 的 c 位置加 1，对右半的点在 BIT 上查前缀和 c 得到贡献；(e) 清空 BIT；(f) cdq(m+1, r)，递归处理右半。
3. **BIT 加速**：CDQ 的每一层用 BIT 将第三维的计数复杂度从 O(N²) 降到 O(N log V)。整体复杂度 O(N log² N)。

**关键理解**：CDQ 的本质是"在分治过程中，利用左侧已经确定的顺序来批量回答右侧查询"。它与归并排序的结构完全一致——把"排序"换成了"统计贡献"。

### 知识脉络

```
离线算法三剑客
    │
    ├──→ 区间查询(静态) ──→ 莫队算法
    │      分块排序 + 双指针
    │      O(N√N), 可扩展为带修改莫队 O(N^(5/3))
    │
    ├──→ 多维偏序/动态逆序对 ──→ CDQ分治
    │      按时间维归并 + BIT
    │      O(N log² N)
    │
    └──→ 多查询求第K小/阈值判定 ──→ 整体二分
          共享判定过程 + BIT模拟
          O((N+Q) log V log N)
```

**本书跨章节连接**：离线算法与第 1.3 节（meet-in-the-middle）共享核心思想——**通过重排计算顺序消除重复工作**。meet-in-the-middle 把问题拆成两半分别计算再合并，离线算法一次性利用"全知视角"共享中间结果。CDQ 分治的"左区间修改→右区间查询"模式与点分治（3.7 节）"统计经过重心的路径"在分治结构上高度对称。莫队的√N分块思想在第 3.10 节（KD-Tree + 莫队）中交叉应用。整体二分在 4.3 节"二分答案 + 半平面交判定"中有相同的判定型策略。

### 快速上手模板

```cpp
// 基础莫队模板
int BLOCK = max((int)ceil(N / sqrt(M)), 16);
struct Query { int l, r, id;
    bool operator<(const Query& q) const {
        int lb = l/BLOCK, rb = q.l/BLOCK;
        if (lb != rb) return lb < rb;
        return (lb & 1) ? r < q.r : r > q.r;  // 奇偶优化
    }
};
// 双指针移动: add(pos), del(pos), 维护 curAns

// CDQ分治模板（以三维偏序为例）
void cdq(int l, int r) {
    if (l == r) return;
    int m = (l + r) / 2;
    cdq(l, m);                                // 递归左
    // 统计左区间对右区间的贡献
    for (int i = l; i <= r; i++) {
        if (ops[i].t <= m) BIT.add(ops[i].val, 1);  // 左区间修改
        else ans[ops[i].id] += BIT.sum(ops[i].val); // 右区间查询
    }
    for (int i = l; i <= r; i++) if (ops[i].t <= m) BIT.add(... -1); // 清空
    cdq(m+1, r);                              // 递归右
    // 归并排序使子区间内部按某维有序
}

// 整体二分模板
void solve(int l, int r, vector<Query>& Q) {
    if (Q.empty()) return;
    if (l == r) { /* Q中所有查询答案 = l */ return; }
    int m = (l + r) / 2;
    施加 [l,m] 中的修改操作;
    for (auto& q : Q) {
        if (判定(q) ≤ m) 左分组.push(q);
        else 右分组.push(q), q.k -= 贡献;
    }
    回退修改;
    solve(l, m, 左分组), solve(m+1, r, 右分组);
}
```

## 例题48 金币（Coins, ACM/ICPC Asia – Amritapuri 2015，Codechef AMCOINS）

### 题目描述
给定一棵N个节点的树（节点1为根）和M个操作，操作分为两种类型：
- 类型1（添加硬币）：在时间time，将一枚价值为w的金币放在节点x。金币会沿着树向下传递——它会出现在以x和y的LCA为根的子树中的所有节点（即在x和y到根的路径上的节点的子树中都可见）。更准确地说，操作`1 x y w`表示在路径(x,y)经过的所有节点的子树中都会增加这枚金币。
- 类型2（查询）：查询在节点z，时间区间[I, J]内出现的金币中，第k小的价值是多少，输出该价值；如果不足k个金币则输出-1。

N, M ≤ 10^5, 操作类型2的数量 ≤ 10^5, w ≤ 10^5。

### 解题思路
1. **树上差分转子树查询**：路径(x,y)上的点增加金币，等价于在x和y子树中+1，在lca子树中-1，在fa(lca)子树中-1。用BIT维护每个节点的DFS序区间实现单点修改和区间求和。
2. **整体二分框架**：对所有查询第k小的操作使用整体二分。二分金币价值区间[L, R]，检查当前区间[mid+1, R]中的金币是否贡献给查询。
3. **拆分查询**：将查询拆成两个时间点——时间点J和时间点I-1，用BIT.sum(Tout[z]) - BIT.sum(Tin[z]-1)计算节点z在某个时间之前获得的特定价值区间金币数。
4. **分治过程**：递归处理，将所有金币和查询按照二分结果的左右子区间分类，继续递归。

### 算法方法
**整体二分（Parallel Binary Search）+ BIT + 树上差分**。将所有查询放在一起二分答案（金币价值），用BIT实时维护差分标记的子树和。

### 复杂度分析
- **时间复杂度**：O((N+M) log N log V)，其中V=100000为金币价值范围。二分深度O(log V)，每层处理所有操作O(M log N)。
- **空间复杂度**：O(N+M)，树结构、操作序列和BIT。

```cpp
// 例题48 金币（Coins, ACM/ICPC Asia – Amritapuri 2015，Codechef AMCOINS）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
template <int SZ>
struct BIT {
  int C[SZ], sz;
  void init(int _sz) {
    sz = _sz;
    assert(sz + 1 < SZ);
  }
  inline int lowbit(int x) { return x & -x; }
  void add(int x, int y) {
    while (x < SZ) C[x] += y, x += lowbit(x);
  }
  int sum(int x) {
    int s = 0;
    while (x > 0) s += C[x], x -= lowbit(x);
    return s;
  }
};
const int NN = 5e5 + 8, QQ = 1e5 + 8, HH = 20;
vector<int> G[NN];
struct Cmd {
  int op, x, y, w, z, k, id, time;
  friend bool operator<(const Cmd& a, const Cmd& b) {
    if (a.time != b.time) return a.time < b.time;
    return a.op < b.op;
  }
};
int Tin[NN], Tout[NN], Dfn, Fa[NN][HH + 1], Dep[NN];  // DFS, LCA
int lca(int u, int v) {
  if (Dep[u] < Dep[v]) swap(u, v);
  int d = Dep[u] - Dep[v];
  for (int h = 0; h <= HH; h++)
    if (d & (1 << h)) u = Fa[u][h];
  if (u == v) return u;
  for (int h = HH; h >= 0; h--)
    if (Fa[u][h] != Fa[v][h]) u = Fa[u][h], v = Fa[v][h];
  return Fa[u][0];
}
void dfs(int u, int fa) {  // Tin[u]:先序遍历序列中的编号，
  Tin[u] = ++Dfn, Fa[u][0] = fa, Dep[u] = Dep[fa] + 1;
  for (int h = 1; h <= HH; h++) Fa[u][h] = Fa[Fa[u][h - 1]][h - 1];
  for (auto v : G[u])
    if (fa != v) dfs(v, u);
  Tout[u] = Dfn;  // Tin[u]-Tout[u]: u子树先序遍历序列中的区间
}
BIT<NN> S;
int Cnt[QQ], Ans[QQ];
void apply(const Cmd& q, bool rev = false) {
  int d = lca(q.x, q.y), c = rev ? -1 : 1;  // x-y路径上全部增加一个计数
  S.add(Tin[q.x], c), S.add(Tin[q.y], c),
      S.add(Tin[d], -c);                 // +(x-root), +(y-root), -(d-root)
  if (d != 1) S.add(Tin[Fa[d][0]], -c);  // d != root, -(fa(d)-root)
}
void solve(int al, int ar,
           const vector<Cmd>& qs) {  // Qs[ql,qr]的答案都在[al, ar]中
  if (qs.empty()) return;
  int am = (al + ar) / 2;
  vector<Cmd> B;
  for (const auto& q : qs) {
    if (q.op == 1) {                  // 修改操作
      if (q.w <= am) B.push_back(q);  // 增加一个[al, am]中的Coin
    } else {  // query[]，拆成对两个时间段的查询:[1,I-1],[1,J],结果考虑正负
      B.push_back(q), B.back().time = q.x - 1, B.back().w = -1;
      B.push_back(q), B.back().time = q.y, B.back().w = 1;
      Cnt[q.id] = 0;  // [al,am]中的操作在q.z节点增加了几个硬币
    }
  }
  sort(begin(B), end(B));  // 时间排序，相同时间: 写在读前
  for (const Cmd& q : B) {
    if (q.op == 1)
      apply(q);  // 修改操作，树上差分
    else  // 版本[1,J]增加的[al,am]中的硬币数量-[1,I-1]增加的[al,am]中的
      Cnt[q.id] += q.w * (S.sum(Tout[q.z]) - S.sum(Tin[q.z] - 1));
  }
  for (const Cmd& q : B)
    if (q.op == 1) apply(q, true);  // 还原所有修改操作

  if (al == ar) {  // 答案已经锁定
    for (auto& q : qs)
      if (q.op == 2 && Cnt[q.id] >= q.k) Ans[q.id] = al;
    return;
  }
  vector<Cmd> lqs, rqs;
  for (auto& q : qs) {
    if (q.op == 1) {
      if (q.w <= am)
        lqs.push_back(q);  // 拆入一个[al,am]中的硬币
      else
        rqs.push_back(q);  // 插入一个[am+1,ar]中的
    } else {
      if (Cnt[q.id] >= q.k)
        lqs.push_back(q);  // 答案在[al,am]中的查询
      else
        rqs.push_back(q), rqs.back().k -= Cnt[q.id];  // 答案在[am+1,ar]中的查询
    }
  }
  solve(al, am, lqs), solve(am + 1, ar, rqs);
}
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int n, m, qc = 0;
  cin >> n;
  for (int i = 1, x, y; i < n; i++)
    cin >> x >> y, G[x].push_back(y), G[y].push_back(x);
  Dfn = 0, dfs(1, 0);
  cin >> m;
  vector<Cmd> Qs(m);
  for (int i = 1; i <= m; i++) {
    Cmd& q = Qs[i - 1];
    cin >> q.op;
    if (q.op == 1)
      cin >> q.x >> q.y >> q.w, q.time = i;
    else
      cin >> q.z >> q.x >> q.y >> q.k, q.id = ++qc;
  }
  solve(1, 100000, Qs);
  for (int i = 1; i <= qc; i++) printf("%d\n", Ans[i] ? Ans[i] : -1);
  return 0;
}
// 30222279 05:42 PM 09/03/20 sukhoeing   0.96  116.4M  C++14
```

## 例题46  公交路线（Bus Routes, ACM/ICPC Asia-Hefei 2015, HDU5552）

### 题目描述
有N个公交站，需要在它们之间建立M条双向路线。要求任意两个车站之间最多有一条路线，且路线图是连通的。求满足条件的方案数，模152076289。N ≤ 10000。

### 解题思路
1. **问题转化**：N个节点有M条边的连通图计数。等价于有N个节点，恰好M条边的连通图的个数。
2. **生成函数方法**：F[n] = 有n个节点恰好M条边且连通的方案数。G[n] = M条边任意图的方案数 = C(C(n,2), M)。
3. **递推关系（CDQ分治+NTT）**：使用连通图的指数生成函数递推：将所有图分为包含节点1的连通块和其余部分，得到递推关系，可以在CDQ分治过程中用NTT（快速数论变换）加速多项式乘法。
4. **NTT原理**：NTT是FFT在模意义下的变体，需要在模数为形如 K*2^m+1 的质数下工作，模数152076289恰好满足条件，原根g=106。
5. **CDQ分治**：分治处理区间[l,r]，先递归处理左区间[l,m]，计算左区间对右区间(m,r]的贡献，再递归处理右区间。

### 算法方法
**CDQ分治 + NTT（数论变换）**。利用生成函数和连通图的经典递推关系，在CDQ分治框架中用NTT加速卷积计算。

### 复杂度分析
- **时间复杂度**：O(N log² N)。NTT每次O(N log N)，CDQ分治深度O(log N)。
- **空间复杂度**：O(N)，存储生成函数和中间结果。

```cpp
// 例题46  公交路线（Bus Routes, ACM/ICPC Asia-Hefei 2015, HDU5552）
// 陈锋
#include <bits/stdc++.h>
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)
using namespace std;
typedef long long LL;
const int MOD = 152076289, NN = 10000 + 8;
LL gcd(LL a, LL b) { return b ? gcd(b, a % b) : a; }
void exgcd(LL a, LL b, LL &x, LL &y) {
  if (!b) {
    x = 1, y = 0;
    return;
  }
  exgcd(b, a % b, y, x), y -= a / b * x;
}
inline LL mul_mod(LL a, LL b) { return a * b % MOD; }
inline LL pow_mod(LL a, LL p) {
  LL res = 1;
  for (; p > 0; p >>= 1, (a *= a) %= MOD)
    if (p & 1) (res *= a) %= MOD;
  return res;
}
inline LL inv(LL a) {
  LL x, y;
  exgcd(a, MOD, x, y);
  return (x % MOD + MOD) % MOD;
}

namespace _Polynomial {
const int g = 106;  // 原根
int A[NN << 1], B[NN << 1];
int w[NN << 1], r[NN << 1];
void DFT(int *a, int op, int n) {
  _for(i, 0, n) if (i < r[i]) swap(a[i], a[r[i]]);
  for (int i = 2; i <= n; i <<= 1)
    for (int j = 0; j < n; j += i)
      for (int k = 0; k < i / 2; k++) {
        int u = a[j + k],
            t = (LL)w[op == 1 ? n / i * k : (n - n / i * k) & (n - 1)] *
                a[j + k + i / 2] % MOD;
        a[j + k] = (u + t) % MOD, a[j + k + i / 2] = (u - t) % MOD;
      }
  if (op == -1) {
    int I = inv(n);
    _for(i, 0, n) a[i] = (LL)a[i] * I % MOD;
  }
}
void multiply(const int *a, const int *b, int *c, int n1, int n2) {
  int n = 1;
  while (n < n1 + n2 - 1) n <<= 1;
  copy_n(a, n1, A), copy_n(b, n2, B);
  fill(A + n1, A + n, 0), fill(B + n2, B + n, 0);

  _for(i, 0, n) r[i] = (r[i >> 1] >> 1) | ((i & 1) * (n >> 1));
  w[0] = 1, w[1] = pow_mod(g, (MOD - 1) / n);
  _for(i, 2, n) w[i] = mul_mod(w[i - 1], w[1]);

  DFT(A, 1, n), DFT(B, 1, n);
  _for(i, 0, n) A[i] = mul_mod(A[i], B[i]);
  DFT(A, -1, n);
  _for(i, 0, n1 + n2 - 1) c[i] = (A[i] + MOD) % MOD;
}
};  // namespace _Polynomial

int A[NN], B[NN], C[NN * 2];
LL Fact[NN], FactInv[NN], F[NN], G[NN];
void solve(int l, int r) {
  if (l == r) {
    F[l] = (G[l] - mul_mod(Fact[l - 1], F[l])) % MOD;
    return;
  }
  int m = (l + r) / 2;
  solve(l, m);  // F[l~m] -> F(m,r]
  _rep(i, l, m) A[i - l] =
      mul_mod(F[i], FactInv[i - 1]);  // ∑F(i)/(i-1)!, i = l~m

  for (int i = r - 1, j = 0; i >= l; --i, ++j)
    B[j] = mul_mod(G[r - i], FactInv[r - i]);
  _Polynomial::multiply(A, B, C, m - l + 1, r - l);
  _rep(i, m + 1, r)(F[i] += C[i - l - 1]) %= MOD;
  solve(m + 1, r);
}

int main() {
  Fact[0] = Fact[1] = 1, FactInv[0] = FactInv[1] = 1;  // i!, (i!)^-1 % MOD
  _for(i, 2, NN) Fact[i] = mul_mod(Fact[i - 1], i), FactInv[i] = inv(Fact[i]);
  LL m;
  int T;
  scanf("%d", &T);
  for (int t = 1, n; t <= T; t++) {
    scanf("%d%lld", &n, &m);
    fill_n(F, n + 1, 0);
    _rep(i, 1, n) G[i] = pow_mod(m + 1, (LL)i * (i - 1) / 2);
    solve(1, n);
    printf("Case #%d: %lld\n", t,
           ((F[n] - pow_mod(n, n - 2) * pow_mod(m, n - 1)) % MOD + MOD) % MOD);
  }
  return 0;
}
// 34867205 2020-12-13 23:04:33 Accepted 5552 1076MS 2072K 2947 B G++ chenwz
```

## 例题45  动态逆序对（CQOI2011）

### 题目描述
给定一个长度为N的排列A[1..N]，依次进行M次操作。第i次操作删除排列中值为x的元素（x保证在剩余排列中存在）。要求在每次删除操作前，输出当前排列的逆序对总数（即满足i < j且A[i] > A[j]的(i,j)对数）。N ≤ 10^5, M ≤ 5×10^4。

### 解题思路
1. **逆向视角**：正序删除难以处理，改为逆向思考——初始排列中除了M个被删除的元素外其余都在，然后按删除顺序的逆序逐个"插入"被删除的元素。每次插入一个元素，新增的逆序对 = 已插入元素中在它前面且值比它大的个数 + 已插入元素中在它后面且值比它小的个数。
2. **CDQ分治**：这是经典的三维偏序问题（时间、位置、值）。将操作按位置递减排序，然后CDQ分治：
   - 情况1：对于右区间的每个插入操作，统计左区间中已插入的、值小于当前值v的元素数（这些元素都在它后面，且值比它小）。
   - 情况2：同样，统计左区间中已插入的、值大于当前值v的元素数（通过值域映射N-v+1实现）。
3. **BIT加速**：在CDQ分治的归并过程中，用BIT维护值域的前缀和，实现O(log N)的单点修改和前缀查询。
4. **前缀求和**：最终每个时刻的逆序对数 = 前面所有插入操作的贡献累加，前缀和即为答案。

### 算法方法
**CDQ分治（三维偏序）+ BIT**。将时间、位置、值作为三个维度，用CDQ分治解决动态插入过程中的逆序对统计问题。

### 复杂度分析
- **时间复杂度**：O(N log² N)。CDQ分治O(log N)层，每层归并用BIT O(log N)。
- **空间复杂度**：O(N)，存储操作序列和BIT。

```cpp
// 例题45  动态逆序对（CQOI2011）
// 陈锋
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;
template <int SZ>
struct BIT {
  int C[SZ], N;
  inline int lowbit(int x) { return x & -x; }
  void add(int x, int v) {
    while (x <= N) C[x] += v, x += lowbit(x);
  }
  int sum(int x) {
    int r = 0;
    while (x) r += C[x], x -= lowbit(x);
    return r;
  }
};
const int NN = 1e5 + 8;
BIT<NN> S;
struct OP {
  int id, p, v;  //第id个命令，在位置p插入v
  bool operator<(const OP &b) { return p > b.p; }
} O[NN], T[NN];
int N, M, A[NN], Pos[NN], Vis[NN];
LL Ans[NN];  // Ans[id]：第id个插入操作新增的逆序对数
void solve(int l, int r) {  // CDQ分治：按插入位置从大到小排序处理后，处理时间[l,r]的操作
  if (l == r) return;
  int m = (l + r) / 2, l1 = l, l2 = m + 1;
  for (int i = l; i <= r; i++) {  // 情况1：统计左边元素对右边元素的贡献（位置在左、值更小的）
    const OP &o = O[i];
    if (o.id <= m) S.add(o.v, 1);  // 左区间的插入：BIT中记录值v
    else Ans[o.id] += S.sum(o.v);  // 右区间的插入：查询已插入中值≤v的个数
  }
  for (int i = l; i <= r; i++)
    if (O[i].id <= m) S.add(O[i].v, -1);  // 还原BIT
  for (int i = r; i >= l; --i) {          // 情况2：统计左边元素对右边元素的贡献（位置在左、值更大的）
    const OP &o = O[i];
    if (o.id <= m)
      S.add(N - o.v + 1, 1);  // 左区间：将值映射到N-v+1（值越大映射值越小）
    else
      Ans[o.id] += S.sum(N - o.v + 1);
    // 右区间：查询映射值小于等于N-v+1的个数（即原值大于v的个数）
  }

  for (int i = l; i <= r; i++) {  // 归并：将id∈[l,m]和[m+1,r]的操作分别放在两侧
    const OP &o = O[i];
    if (o.id <= m) T[l1++] = o, S.add(N - o.v + 1, -1);  // 还原BIT + 归并
    else T[l2++] = o;
  }
  copy(T + l, T + r + 1, O + l);  // 归并结果写回
  solve(l, m), solve(m + 1, r);   // 递归处理左右子区间
}

int main() {
  cin >> N >> M;
  int id = N, qc = M;
  S.N = N;
  for (int i = 1; i <= N; ++i) cin >> A[i], Pos[A[i]] = i;
  for (int i = 1; i <= M; ++i) {
    OP &q = O[i];
    cin >> q.v, Vis[q.p = Pos[q.v]] = true, q.id = id--;
  }
  for (int i = 1; i <= N; ++i) {
    if (Vis[i]) continue;
    O[++qc] = {id--, i, A[i]};
  }
  sort(O + 1, O + 1 + N);  //根据插入位置递减排序
  solve(1, N);
  for (int i = 1; i <= N; ++i) Ans[i] += Ans[i - 1];
  _for(i, 0, M) cout << Ans[N - i] << endl;
  return 0;
}
// 46047579 [CQOI2011]动态逆序对 答案正确 100 201 5604 2010 C++ 2020-12-13 22:59:28
```

## 例题50  数颜色（牛客NC202003）

### 题目描述
给定一个长度为N的整数序列，每个位置有一个颜色。有M个操作：
- `Q L R`：查询区间[L, R]内有多少种不同的颜色。
- `R P C`：将位置P的颜色改为C。
N ≤ 10000, M ≤ 10000, 颜色值 ≤ 10^6。

### 解题思路
1. **带修改莫队算法**：在普通莫队（l, r双指针）的基础上增加时间维度（t指针），形成三维莫队((l, r, t)三元组)。
2. **分块策略**：块大小设为 N^(2/3)，按 `l/block`、`r/block`、`t` 三级排序。
3. **指针移动**：
   - curL和curR指针：与普通莫队相同，在区间上左右移动，增/删元素并维护颜色种数cnt。
   - last_c（时间指针）：移动到目标查询的时间点，应用或回退修改操作。
4. **修改操作**：应用修改时，如果修改位置在[l,r]区间内，先删除旧颜色再添加新颜色；回退时相反。
5. **答案统计**：每个查询处理完后记录当前的curAns。

### 算法方法
**带修改莫队（Mo's Algorithm with Updates）**。将时间作为第三维，分块大小O(N^(2/3))，排序后按(l, r, t)三维指针移动。

### 复杂度分析
- **时间复杂度**：O(N^(5/3))。指针移动次数分析：l指针O(N^(5/3))，r指针O(N^(5/3))，t指针O(N^(5/3))。
- **空间复杂度**：O(N + MAXC)，MAXC为颜色值域大小（10^6）。

```cpp
// 例题50  数颜色（牛客NC202003）
// 陈锋
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)

const int SZ = 10005, MAXC = 1e6 + 4;
int BLOCK, Color[SZ], CurColor[SZ], CNT[MAXC], Ans[SZ];
struct Query {
  int l, r, id, c;
  bool operator<(const Query &rhs) const {
    if (l / BLOCK == rhs.l / BLOCK) {
      if (r / BLOCK == rhs.r / BLOCK) return id < rhs.id;  //时间维度优化
      return r < rhs.r;
    }
    return l < rhs.l;
  }
};
struct Change {
  int pos, old_color, color;  //位置，旧颜色，新颜色
  void apply();
  void revert();
};
Query Q[SZ];
Change Changes[SZ];
int curAns, curL, curR;
void add_pos(int a) {
  if (++CNT[a] == 1) curAns++;
}
void del_pos(int a) {
  if (--CNT[a] == 0) curAns--;
}
void Change::apply() {
  //修改位置在当前区间内，应用修改到结果中
  if (curL <= pos && pos <= curR) del_pos(old_color), add_pos(color);
  Color[pos] = color;  //应用修改
}
void Change::revert() {
  //修改位置在当前区间内，还原结果中的答案
  if (curL <= pos && pos <= curR) del_pos(color), add_pos(old_color);
  Color[pos] = old_color;  //应用还原
}

int main() {
  int N, M, c1 = 0, c2 = 0;
  cin >> N >> M;
  BLOCK = pow(N, 2.0 / 3.0);
  _rep(i, 1, N) cin >> Color[i], CurColor[i] = Color[i];
  char opt[4];
  _rep(i, 1, M) {
    cin >> opt;
    if (opt[0] == 'Q') {
      Query &q = Q[c1];
      cin >> q.l >> q.r, q.id = c1++, q.c = c2;
    } else {
      Change &ch = Changes[c2++];
      cin >> ch.pos >> ch.color;
      ch.old_color = CurColor[ch.pos], CurColor[ch.pos] = ch.color;
    }
  }
  sort(Q, Q + c1);
  curL = 1, curR = 1, curAns = 0;
  int last_c = 0;  //第一条还未执行的修改命令编号
  add_pos(Color[1]);

  _for(i, 0, c1) {
    while (last_c < Q[i].c) Changes[last_c++].apply();
    //应用在此查询时间之前的命令
    while (last_c > Q[i].c) Changes[--last_c].revert();
    //回退在此查询时间之后的命令
    while (curR < Q[i].r) add_pos(Color[++curR]);
    while (curR > Q[i].r) del_pos(Color[curR--]);
    while (curL > Q[i].l) add_pos(Color[--curL]);
    while (curL < Q[i].l) del_pos(Color[curL++]);
    Ans[Q[i].id] = curAns;
  }
  _for(i, 0, c1) cout << Ans[i] << endl;
  return 0;
}
// 46047654 数颜色 答案正确 100 35 4608 2080 C++ 2020-12-13 23:07:27
```

## 例题49 D-查询（SPOJ DQUERY）

### 题目描述
给定一个长度为N的整数序列A[1..N]，有M个查询，每个查询给出区间[L, R]，要求输出该区间内不同元素的个数。N ≤ 30000, M ≤ 200000, A[i] ≤ 10^6。

### 解题思路
1. **基础莫队算法**：将所有查询离线处理，按左端点所在块的编号排序。同一块内按右端点排序（奇偶性优化：奇数块右端点升序，偶数块右端点降序）。
2. **双指针移动**：维护curL和curR指针及当前区间内每种颜色的计数CNT[]和当前答案ans。
   - 当指针向右扩展时，如果新增元素的计数从0变为1，答案+1。
   - 当指针向左收缩时，如果被移除元素的计数从1变为0，答案-1。
3. **分块大小选择**：取 `max(N/sqrt(M), 16)` 作为分块大小，平衡左右指针移动次数。
4. **奇偶排序优化**：同一块内根据块编号的奇偶性改变右端点排序方向，减少右端点回退次数。

### 算法方法
**莫队算法（Mo's Algorithm）**。基础离线区间查询算法，通过分块和双指针移动实现O((N+M)sqrt(N))的区间颜色种类统计。

### 复杂度分析
- **时间复杂度**：O((N+M) sqrt(N))。左指针移动O(M sqrt(N))，右指针在同一块内单调移动O(N sqrt(N))。
- **空间复杂度**：O(N + MAXA)，存储序列、查询数组和颜色计数器。

```cpp
// 例题49 D-查询（SPOJ DQUERY）
// 陈锋
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)

const int NN = 300000 + 4, MM = 200000 + 4, AA = 1000000 + 4;
int A[NN], ANS[MM], N, M, BLOCK;
struct query {
  int L, R, id;
  bool operator<(const query& q) const {
    int lb = L / BLOCK;
    if (lb != q.L / BLOCK) return lb < q.L / BLOCK;
    if (lb % 2) return R < q.R;
    return R > q.R;
  }
};

query Q[MM];
int ans, curL, curR, CNT[AA];
void add(int pos) {
  if (++CNT[A[pos]] == 1) ++ans;
}
void remove(int pos) {
  if (--CNT[A[pos]] == 0) --ans;
}

typedef long long LL;
int main() {
  scanf("%d", &N);
  _rep(i, 1, N) scanf("%d", &A[i]), CNT[A[i]] = 0;
  scanf("%d", &M);
  BLOCK = max((int)ceil((double)N / sqrt(M)), 16);
  _for(i, 0, M) scanf("%d%d", &Q[i].L, &Q[i].R), Q[i].id = i;
  sort(Q, Q + M);
  CNT[A[1]] = 1, ans = 1, curL = 1, curR = 1;
  _for(i, 0, M) {
    while (curL < Q[i].L) remove(curL++);
    while (curL > Q[i].L) add(--curL);
    while (curR < Q[i].R) add(++curR);
    while (curR > Q[i].R) remove(curR--);
    ANS[Q[i].id] = ans;
  }
  _for(i, 0, M) printf("%d\n", ANS[i]);
  return 0;
}
// Accepted 310ms 11264kB 1215 C++(gcc 8.3)2020-12-13 23:10:54 27090670
```

## 例题47 流星（Meteors，POI2011，SPOJ METEORS）

### 题目描述
有一个环形轨道分为M个扇区（编号1到M），有N个国家，每个国家拥有若干个扇区（一个扇区可能属于多个国家）。计划有K场流星雨，第i场流星雨在扇区区间[l_i, r_i]（环形）内下a_i颗流星。每个国家有一个目标值P[i]——需要收集到至少P[i]颗流星。对于每个国家，求在哪一场流星雨之后（最少需要多少场）才能达到目标。如果始终达不到则输出"NIE"。N, M ≤ 3×10^5, K ≤ 3×10^5。

### 解题思路
1. **整体二分**：将所有国家放在一起二分答案（需要的流星雨场数）。二分区间为[1, K+1]，其中K+1表示始终达不到（输出NIE）。
2. **BIT维护区间加**：当前二分到mid时，将前mid场流星雨用BIT施加到环形区间上。BIT维护差分数组，支持区间加法（环形拆成两个区间：如果l<=r则直接[l,r]加；否则[l,M]和[1,r]加）。
3. **国家分类**：对每个国家，累加它所有扇区的流星数。如果达到目标P[i]，则答案在[1, mid]中（分到左边）；否则P[i]减去已收集的量，分到右边[mid+1, K+1]。
4. **递归处理**：递归处理左右两组国家，每层只施加当前区间的流星雨。
5. **还原操作**：处理完当前层后，回退BIT中本次施加的增量。

### 算法方法
**整体二分（Parallel Binary Search）+ BIT（差分数组）**。将所有国家放在一起二分答案，用BIT支持区间加减和单点查询，实现环形区间的流星雨模拟。

### 复杂度分析
- **时间复杂度**：O((N+M+K) log K log M)。整体二分深度O(log K)，每层BIT操作O(log M)。
- **空间复杂度**：O(N+M+K)，存储国家扇区列表和流星雨操作。

```cpp
// 例题47 流星（Meteors，POI2011，SPOJ METEORS）
// 陈锋
#include<bits/stdc++.h>
#define _for(i,a,b) for(int i=(a); i<(int)(b); ++i)
#define _rep(i,a,b) for(int i=(a);i<=(b);++i)
using namespace std;
typedef long long LL;
template<int SZ>
struct BIT {
  LL C[SZ];
  int N;
  void init(int _n) { N = _n; }
  inline int lowbit(int x) { return x & -x; }
  inline void add(int x, int d) { while (x <= N) C[x] += d, x += lowbit(x); }
  inline LL sum(int x) {
    LL ret = 0;
    while (x) ret += C[x], x -= lowbit(x);
    return ret;
  }
};
struct Rain { int l, r, a; };
const int NN = 3e5 + 8;
Rain Rs[NN];
vector<int> St[NN]; // 每个国家的空间站
int N, M, Ans[NN], P[NN];
BIT<NN> S;
inline void apply(const Rain& q, bool revert = false) {
  int x = q.a, l = q.l, r = q.r;
  if (revert) x = -x;
  if (l <= r) S.add(l, x), S.add(r + 1, -x); // 区间加单点询问用BIT差分实现
  else S.add(l, x), S.add(M + 1, -x), S.add(1, x), S.add(r + 1, -x); // 拆成两个区间
}
// C中的每个国家的查询结果进行二分，目标答案区间是[al, ar]
// 整体二分：所有国家一起二分答案（需要经历几场流星雨才能满足需求）
void solve(const vector<int>& C, int l, int r) {
  if (C.empty()) return;
  if (l == r) { // 答案区间已经锁定为单点
    for (int c : C) Ans[c] = l; // 记录每个国家的答案
    return;
  }
  int m = (l + r) / 2;
  _rep(ai, l, m) apply(Rs[ai]); // 施加前m场流星雨（使用BIT差分）
  vector<int> LC, RC; // 左右分组
  for (int c : C) { // 对每个国家，检查前m场流星雨是否满足需求
    int &p = P[c];
    LL x = 0;
    for (int s : St[c]) if ((x += S.sum(s)) >= p) break; // 累加该国所有扇区收集到的流星
    if (p <= x) LC.push_back(c); // 需求已满足，答案在[l,m]中
    else p -= x, RC.push_back(c); // 不够，减去已收集的，答案在[m+1,r]中
  }
  _rep(ai, l, m) apply(Rs[ai], true); // 回退流星雨（恢复BIT）
  solve(LC, l, m), solve(RC, m + 1, r); // 递归处理左右两组
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  cin >> N >> M, S.init(M + 2);
  int qc, x;
  vector<int> C;
  _rep(i, 1, M) cin >> x, St[x].push_back(i);
  _rep(i, 1, N) cin >> P[i], C.push_back(i);
  cin >> qc;
  _rep(i, 1, qc) cin >> Rs[i].l >> Rs[i].r >> Rs[i].a; // 流星雨下到[l, r]，雨量a
  solve(C, 1, qc + 1);
  _rep(i, 1, N) {
    if (Ans[i] <= qc) cout << Ans[i] << endl;
    else cout << "NIE" << endl;
  }
  return 0;
}
// 25024499   2019-12-07 17:50:24   Feng Chen Meteors accepted  0.92  19M   CPP14
```
