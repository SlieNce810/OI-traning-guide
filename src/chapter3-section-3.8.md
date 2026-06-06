# 3.8 动态树与LCT

> **学习目标**：理解 Link-Cut Tree 的实链剖分机制与树链剖分的本质区别，搞懂 Splay 为什么恰好适合维护实链，以及 Access 操作如何成为 LCT 所有能力的入口。

## 理论基础

### 为什么需要学这个？

你之前学过的树链剖分（HLD）很好用，但它有一个致命的局限：**树的结构不能变**。一旦你需要在树上动态加边（link）或删边（cut），树链剖分就傻眼了——因为重链的划分是基于静态子树大小计算的，一变树结构，整个剖分就失效了。这正是 LCT 登场的原因。但 LCT 又臭名昭著地"难学"：代码长、状态多、bug 横飞。这一节我们不求面面俱到，而是抓住最核心的三个问题：**LCT 的剖分和 HLD 到底不同在哪？Splay 在 LCT 里扮演什么角色？Access 操作为什么是"所有操作的入口"？** 这三个问题通了，LCT 就不再是"抄完模板就跑"的玄学。

### 核心概念

#### 1. 实链剖分 vs 树链剖分：动态 vs 静态

**一句话定义**：树链剖分（HLD）的"重边"是静态的（永不变），LCT 的"实边"是动态的（随操作改变）。

**本质理解**：HLD 说"哪棵子树最大，我就和谁连成重链"，这个决定做一次、永不更改（除非插删节点）。LCT 说"我每次 access(x) 的时候，就把从根到 x 这条路径上的所有边变成实边，其他的都变为虚边"。实边形成了若干条实链，每条实链用一棵 Splay 维护——Splay 的中序遍历恰好是按照深度从小到大的顺序。这恰恰是 LCT 最精妙的设计：**Splay 用来维护"当前实链"，access 用来动态切换"哪条链是实的"**。

#### 2. Splay 如何维护实链：区间反转 = 翻转深度

**一句话定义**：makeroot(x) 的本质是把 x 到原根的路径"翻个底朝天"——让 x 变成新的根。

**本质理解**：在实链对应的 Splay 中，节点按深度排列（左子树更浅，右子树更深）。如果要把一个节点变成原树的根，整条路径的深度关系就完全反过来了——原来深的变浅，原来浅的变深。在 Splay 上这就是经典的"区间翻转"操作：打一个 `rev` 标签，交换左右子树。LCT 中的 `makeroot(x)` 就是 `access(x)` 后 `splay(x)` 然后翻转 x 所在的 Splay。

#### 3. Access 的两种实现方式

**一句话定义**：`access(x)` 把从根到 x 的路径打通为一条实链，也就是让这条路径上不再有虚边。

**方式一（标准）**：`for (int t = 0; x; t = x, x = fa[x]) splay(x), rs(x) = t, maintain(x);`

**方式二（带维护信息）**：本质相同，但在 `splay(x)` 后除了设置 `rs(x) = t`，还需要更新与本节点关联的子树聚合信息（因为旧右儿子变为虚边，新虚边 t 变为实边）。

**本质理解**：Access 循环中对每个 Splay 节点的操作是"断掉旧的实儿子，接上新的实儿子"。整个循环扫过根到 x 路径上的所有节点，每个节点恰好被 splay 一次。均摊复杂度 O(log N)（由 Splay 的均摊性质保证）。

#### 4. makeroot 操作的完整原理详解

**操作序列**：`makeroot(x)` = access(x) + splay(x) + reverse(x)。整个操作的目标是将 x 变成原树的根节点。

**分步理解**：(1) **access(x)**：将原根到 x 的路径打通为一条实链，此时 x 是这条实链的最深节点（因为它距离原根最远）。实链对应的 Splay 中，x 在中序遍历的最右端。(2) **splay(x)**：将 x 旋转到它所在 Splay 的根。此时 x 成为这棵 Splay 的根，且 x 没有右儿子（因为 access 后 x 的右儿子被设为了 0）。(3) **reverse(x)**：对 x 打翻转标记——交换 x 的左右子树，并将 rev 标记下推。翻转后，x 的左右子树互换，中序遍历顺序完全反转，原链上 x 从"最深"变成了"最浅"——即在原树中 x 成为了新的根。

**直观理解**：整条路径的深度关系就像一根绳子，原来一端（原根）在顶、一端（x）在底。makeroot 所做的就是把绳子掉个头——x 变成顶、原根变成底。在 Splay 维护的中序遍历中，这就是一个区间翻转操作。这个设计的优雅之处在于：makeroot 之后，原来从根到 x 的路径变成了从 x 到原根的路径——路径上的节点集合完全不变，只是深度关系反转。这使得 link(x, y) 只需 makeroot(x) 后 fa[x]=y 即可。

#### 5. LCT 中 Splay 与普通 Splay 的关键区别

**区别一：isroot 判定**。普通 Splay 的根判定是 `fa[x] == 0`；LCT 中 Splay 的根判定是"父节点不认 x 为儿子"——即 `ch[fa[x]][0] != x && ch[fa[x]][1] != x`。这是因为 LCT 中的节点有双重身份：在同一条实链的 Splay 内部是父子关系（双向指针），不同 Splay 之间通过虚边连接（单向 fa 指针——子节点的 fa 指向父节点，但父节点不认这个子节点）。

**区别二：旋转时虚边的处理**。普通 Splay 旋转只需考虑 Splay 内部的连接关系；LCT 旋转时，若 y 的父节点 z 和 y 之间是虚边（即 `isroot(y)` 为 true），则旋转后 x 与 z 之间仍然是虚边关系（z 不把 x 当儿子，但 x 的 fa 指向 z）。只有在 y 不是 Splay 根时（实边连接），才按普通 Splay 旋转处理。

**区别三：pushup 和 pushdown 的路径**。LCT 中 splay(x) 前需要从 x 到所在 Splay 的根整条路径 pushdown（调用 pushup(x) 函数先沿 fa 链上溯、沿路下推懒标记）。这是因为 LCT 的翻转标记可能分布在从 Splay 根到 x 的路径上，必须在旋转操作前确保路径上的标记都已下推——否则旋转操作会破坏标记的语义正确性。

### 知识脉络

```
静态树 ──→ 树链剖分(HLD) ──不可动态──→ 需要LCT
                                    │
                    ┌───────────────┘
                    ▼
              实链剖分(LCT)
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    access(x)  makeroot(x) link/cut
   (入口操作) (翻转路径) (加点/断边)
        │           │
        └──── Splay ─┘ (维护每条实链的深度顺序)
```

**本书跨章节连接**：LCT 的"Splay 维护实链"直接复用了第 3.6 节的 Splay 旋转和伸展操作——isroot 判定和虚边处理是仅有的区别。LCT 与第 3.7 节的**树链剖分**形成"动态 vs 静态"的对比：HLD 的重边是在静态子树大小上的划分，LCT 的实边是随 access 操作动态变化的。在解决实际问题时，能用树链剖分就不用 LCT（代码量差数倍），只有当涉及动态 link/cut 时才需要 LCT。第 5 章图论中的动态连通性问题，当需要在树上增删边时，LCT 正是首选武器。

### 快速上手模板

```cpp
// LCT 核心六个操作
struct LCT {
    int ch[SZ][2], fa[SZ], rev[SZ];
    // 判断x是否为所在Splay的根（虚边的判定）
    bool isroot(int x) { return ch[fa[x]][0]!=x && ch[fa[x]][1]!=x; }
    void pushdown(int x) { if (rev[x]) swap(ch[x][0],ch[x][1]), rev[ch[x][0]]^=1, rev[ch[x][1]]^=1, rev[x]=0; }
    void rotate(int x) { /* 标准Splay旋转, 注意判断isroot */ }
    void splay(int x) { /* 标准Splay, 先下推标记 */ }

    void access(int x) {       // 打通root->x的实链
        for (int t = 0; x; t = x, x = fa[x])
            splay(x), ch[x][1] = t;  // 断开旧右儿子, 接入新的
    }
    void makeroot(int x) {     // 令x成为原树的根
        access(x), splay(x), rev[x] ^= 1;
    }
    int findroot(int x) {      // 找x所在原树的根
        access(x), splay(x);
        while (ch[x][0]) pushdown(x), x = ch[x][0];
        splay(x); return x;
    }
    void link(int x, int y) {  // 加边
        if (findroot(x) != findroot(y)) makeroot(x), fa[x] = y;
    }
    void cut(int x, int y) {   // 断边
        makeroot(x), access(y), splay(y);
        if (ch[y][0] == x && !ch[x][1]) ch[y][0] = fa[x] = 0;
    }
};
```

## 例题43  大厨和图上查询（Chef and Graph Queries，Codechef GERALD 07）

### 题目描述
给定N个节点（初始无边），依次加入M条带编号的边（编号为加入顺序1..M）。有Q个查询[L,R]，问在仅考虑编号在[L,R]范围内的边时，图的连通分量数。

- **约束**：N, M, Q ≤ 2×10^5。

### 解题思路
使用**LCT + BIT**维护动态图连通性和"最小标号边"：
1. 按编号顺序依次加入边i=(u,v)。用LCT维护动态森林（节点数为N+M，节点1..M代表边，M+1..M+N代表原图节点）。
2. 若加入边i时u和v已连通：找到u-v路径上标号最小的边e。若e < i，则删除边e，替换为边i（因为边i的标号更大，在查询时更可能被包含）。BIT中标记：e位置-1，i位置+1。
3. 查询[L,R]时：区间内有效边数 = `S.sum(R) - S.sum(L-1)`。连通分量数 = N - 有效边数。
4. 因为维护的是"最大生成树"结构：LCT中保留的边构成每个时刻的"最后加入的生成树"。

### 算法方法
**LCT（Link-Cut Tree）+ BIT（树状数组）**：LCT维护动态树结构，支持link/cut/findroot操作，并用minw维护路径上的最小权值边。BIT维护每个时间点的有效边数。核心思想：用LCT维护"时间最大生成树"，边的权值为其编号。

### 复杂度分析
- **时间复杂度**：O((M+Q) log N)，每次LCT操作O(log N)。
- **空间复杂度**：O(N+M)，LCT节点约N+M个。

```cpp
// 例题43  大厨和图上查询（Chef and Graph Queries, GERALD07）
// 陈锋
// 题目：动态加边图，查询编号区间内的边构成图的连通分量数
// 算法：LCT维护最大生成树 + BIT统计有效边
#include <bits/stdc++.h>
using namespace std;

template <int SZ> struct LCT {
  int ch[SZ][2], fa[SZ], minw[SZ]; bool rev[SZ];
  // LCT标准操作：rotate, splay, access, makeroot, link, cut, split, findroot, init
  inline int& ls(int x) { return ch[x][0]; } inline int& rs(int x) { return ch[x][1]; }
  inline void reverse(int x) { rev[x] ^= 1, swap(ls(x), rs(x)); }
  inline void maintain(int x) { minw[x] = min(x, min(minw[ls(x)], minw[rs(x)])); }
  inline void pushdown(int x) { if (rev[x]) reverse(ls(x)), reverse(rs(x)), rev[x] = false; }
  inline bool isroot(int x) { return ls(fa[x]) != x && rs(fa[x]) != x; }
  inline int isright(int x) { return rs(fa[x]) == x; }
  void rotate(int x) { /* 标准旋转 */ }
  void pushup(int x) { if (!isroot(x)) pushup(fa[x]); pushdown(x); }
  void splay(int x) { pushup(x); while (!isroot(x)) { /* 双旋 */ } }
  void access(int x) { for (int t = 0; x; t = x, x = fa[x]) splay(x), rs(x) = t, maintain(x); }
  void makeroot(int x) { access(x), splay(x), reverse(x); }
  void link(int x, int y) { makeroot(x), fa[x] = y; }
  void cut(int x, int y) { makeroot(x), access(y), splay(y); ls(y) = fa[x] = 0; maintain(y); }
  void split(int x, int y) { makeroot(x), access(y), splay(y); }
  int findroot(int x) { access(x), splay(x); while (ls(x)) pushdown(x), x = ls(x); splay(x); return x; }
  void init(int sz) { minw[0] = 1e9; for (int i = 1; i <= sz; i++) minw[i] = i, ch[i][0] = ch[i][1] = fa[i] = 0, rev[i] = 0; }
};

template <int SZ> struct BIT { /* 标准BIT */ };
const int NN = 2e5 + 4;
BIT<NN> S; LCT<NN * 2> lct;
int QL[NN], Ans[NN], EU[NN], EV[NN];
vector<int> EQ[NN];

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T; cin >> T;
  for (int t = 0, n, m, q; t < T; t++) {
    cin >> n >> m >> q;
    for (int i = 1; i <= m; i++) { int &u = EU[i], &v = EV[i]; cin >> u >> v; u += m, v += m; EQ[i].clear(); }
    S.init(m), lct.init(m + n);
    for (int i = 1, qr; i <= q; i++) cin >> QL[i] >> qr, EQ[qr].push_back(i);
    for (int i = 1; i <= m; i++) {  // 按编号加入边
      int u = EU[i], v = EV[i];
      if (lct.findroot(u) == lct.findroot(v)) {  // 已连通
        lct.split(u, v); int e = lct.minw[v];
        if (e < i) { lct.cut(e, EU[e]), lct.cut(e, EV[e]), S.add(e, -1); lct.link(i, u), lct.link(i, v), S.add(i, 1); }  // 替换
      } else lct.link(u, i), lct.link(v, i), S.add(i, 1);
      for (size_t xi = 0; xi < EQ[i].size(); xi++) Ans[EQ[i][xi]] = n - (S.sum(i) - S.sum(QL[EQ[i][xi]] - 1));
    }
    for (int i = 1; i <= q; i++) cout << Ans[i] << endl;
  }
  return 0;
}
// 40407264	sukhoeing 0.62 33.4M C++14
```

## 例题44  大象（Elephants, Codechef ELPHANT, IOI 2011 Day 2）

### 题目描述
数轴上有N只大象，每只大象有一个不同的位置P[i]。大象之间有一个特殊的关系：两只大象如果位置差大于L则互相不可见，否则可以经由对方"链接"。一种链接方案是一棵生成树——如果两只大象的位置差≤L，它们之间可以有一条边。

现在有M次修改操作，每次将第X[i]只大象移动到新的位置Y[i]。每次修改后，需要输出当前链接方案下，生成树需要的边数（即N减去连通块数）。初始时大象位置不保证连通。N, M ≤ 10^5。

更具体地：把所有大象的位置坐标离散化，在离散化后的坐标轴上，每只大象只与其位置+L+1处的虚拟节点相连（表示这个位置的大象可以链接到右侧L范围内的所有位置）。问题转化为：有多少个区间被大象覆盖，这等价于数轴上被覆盖的连续段数。

### 解题思路
1. **离散化坐标**：将大象位置P[i]和P[i]+L+1都离散化到1..sz的范围。
2. **LCT建模**：坐标轴上的每个整数点作为一个LCT节点，初始将所有相邻位置link起来。如果位置u有大象，则cut(u, u+1)并link(u, u+L+1)，表示这个位置的大象可以"跳过"它从u到u+L+1之间的所有位置。
3. **权值维护**：在LCT上每个节点维护val（该节点是否被大象占据）和子树sum。当大象移动到位置u时，如果该位置之前无大象则modify(u, 1)，如果之前有则先modify(u, 0)。
4. **答案统计**：从位置1到sz的区间和就是覆盖的连续段数量，N减去此数即为答案。

### 算法方法
**LCT（Link-Cut Tree） + 离散化 + 区间建模**。将坐标轴建模为LCT中的链结构，大象占据的位置改变链的连接方式，用LCT维护子树和。

### 复杂度分析
- **时间复杂度**：O((N+M) log SZ)。每次LCT操作O(log SZ)，SZ为离散化后的坐标数（≤ 2N+2M）。
- **空间复杂度**：O(SZ)，LCT节点数。

```cpp
// 例题44  大象（Elephants, Codechef ELPHANT, IOI 2011 Day 2）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int NN = 1e6 + 4;
template<int SZ>
struct LCT {
  int ch[SZ][2], fa[SZ], rev[SZ], val[NN], sum[NN];
  void clear(int x) { ch[x][0] = ch[x][1] = fa[x] = rev[x] = 0; }
  inline int is_right_ch(int x) // x是辅助树上父亲的右儿子?
  { return ch[fa[x]][1] == x; }
  inline int is_root(int x) // x是辅助树根?
  { return ch[fa[x]][0] != x && ch[fa[x]][1] != x; }
  void pushdown(int x) {
    if (rev[x] == 0) return;
    int lx = ch[x][0], rx = ch[x][1];
    if (lx) swap(ch[lx][0], ch[lx][1]), rev[lx] ^= 1;
    if (rx) swap(ch[rx][0], ch[rx][1]), rev[rx] ^= 1;
    rev[x] = 0;
  }
  void pushup(int x) {
    if (!is_root(x)) pushup(fa[x]);
    pushdown(x);
  }
  void rotate_up(int x) { // 在辅助树中将x向上旋转一级
    int y = fa[x], z = fa[y], chx = is_right_ch(x), chy = is_right_ch(y),
        &t = ch[x][chx ^ 1]; // t在x,y之间，但是t-x, x-y方向相反
    fa[x] = z;
    if (!is_root(y)) ch[z][chy] = x; // x,y在z的同一侧
    ch[y][chx] = t, fa[t] = y, t = y, fa[y] = x; // 保证t依然在x,y之间
    update_sum(y);
  }
  void splay(int x) {
    pushup(x); // x一直到树根路径上所有点的深度相对关系都要反转
    for (int f = fa[x]; f = fa[x], !is_root(x); rotate_up(x))
      if (!is_root(f)) rotate_up(is_right_ch(x) == is_right_ch(f) ? f : x);
    update_sum(x);
  }
  void access(int x) { // 将root-x变成首选边
    for (int f = 0; x; f = x, x = fa[x])
      splay(x), ch[x][1] = f, update_sum(x);
  }
  void make_root(int x) { access(x), splay(x), swap(ch[x][0], ch[x][1]), rev[x] ^= 1; }
  void split(int x, int y) { make_root(x), access(y), splay(y); }
  int find_root(int x) { // x所在树的树根
    access(x), splay(x);
    while (ch[x][0]) x = ch[x][0];
    splay(x);
    return x;
  }
  void cut(int x, int y) {
    split(x, y);  // x是y在辅助树中的左孩子且要求x,y相邻
    if (ch[y][0] == x && !ch[x][1]) ch[y][0] = fa[x] = 0;
  }
  void link(int x, int y) { if (find_root(x) != find_root(y)) make_root(x), fa[x] = y; }
  void update_sum(int x) { sum[x] = val[x] + sum[ch[x][0]] + sum[ch[x][1]]; }
  int query_sum(int x, int y) { split(x, y); return sum[y]; }
  void modify(int x, int w) { access(x), splay(x), val[x] = w, update_sum(x); }
};
LCT<NN> T;
int N, L, M, P[NN], X[NN], Y[NN], Cnt[NN];
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  cin >> N >> L >> M;
  vector<int> ps;
  ps.push_back(-1), ps.push_back(2e9);
  for (int i = 1; i <= N; i++)
    cin >> P[i], ps.push_back(P[i]), ps.push_back(P[i] + L + 1);
  for (int i = 1; i <= M; i++) {
    cin >> X[i] >> Y[i], X[i]++;
    ps.push_back(Y[i]), ps.push_back(Y[i] + L + 1);
  } // 记录所有可能的点的位置
  sort(ps.begin(), ps.end()), ps.erase(unique(ps.begin(), ps.end()), ps.end());
  int sz = ps.size();
  unordered_map<int, int> PLoc;
  for (int i = 0; i < sz; i++) PLoc[ps[i]] = i; // 离散化

  for (int i = 2; i <= sz; i++) T.link(i - 1, i);
  for (int i = 1; i <= N; i++) { // 所有大象
    int u = PLoc[P[i]]; // u是在i位置上的大象
    if (!Cnt[u]) T.cut(u, u + 1), T.link(u, PLoc[P[i] + L + 1]), T.modify(u, 1);
    Cnt[u]++; // 大象节点p只和p+L+1相连
  }

  for (int i = 1; i <= M; i++) {
    int &px = P[X[i]], y = Y[i], ou = PLoc[px], u = PLoc[y];
    if (--Cnt[ou] == 0) // ou不再是大象了
      T.cut(ou, PLoc[px + L + 1]), T.link(ou, ou + 1), T.modify(ou, 0);
    if (Cnt[u]++ == 0) // u变成大象了
      T.cut(u, u + 1), T.link(u, PLoc[y + L + 1]), T.modify(u, 1);
    px = y;
    cout << T.query_sum(1, sz) << endl;
  }
  return 0;
}
// 64389  1 min ago sukhoeing 100[1pts]  1.10  90.1M C++14
```

## NC20311 例题41  洞穴勘测（Cave, SDOI2008）

### 题目描述
初始有N个孤立节点（洞穴），编号1..N。需要处理Q个操作，操作类型包括：
- `Connect u v`：在节点u和v之间建立一条边（洞穴通道），保证操作前u和v不连通。
- `Destroy u v`：摧毁节点u和v之间的边，保证操作前这条边存在。
- `Query u v`：查询节点u和v是否连通。
N ≤ 10000, Q ≤ 200000。

### 解题思路
1. **动态树需求**：需要支持动态加边（link）、删边（cut）和连通性查询（find_root）。这正好是LCT（Link-Cut Tree）的标准应用场景。
2. **LCT基本操作**：
   - `link(x, y)`：先判断x和y不在同一棵树中，然后makeroot(x)，fa[x] = y。
   - `cut(x, y)`：split(x, y)，检查y在辅助树中的左孩子是否为x且x没有右孩子（确保x和y在原树中直接相邻），然后断开连接。
   - `find_root(x)`：access(x) + splay(x)，沿着左子树逐个下推直到叶子，最后splay叶子上来，返回叶子的编号。
3. **翻转标记（rev）**：makeroot操作需要翻转整条路径的深度关系，用懒标记rev实现。
4. **辅助树（Splay）**：每个节点的虚边组成一棵Splay（按深度为关键字），access将根到x的路径变成一棵Splay中的首选边。

### 算法方法
**LCT（Link-Cut Tree）**。最基本的LCT实现，支持 link / cut / find_root 操作，只维护结构不维护额外权值。

### 复杂度分析
- **时间复杂度**：O(Q log N)。每次LCT操作（access、splay）均摊O(log N)。
- **空间复杂度**：O(N)，每个节点维护ch[2], fa, rev。

```cpp
// NC20311 例题41  洞穴勘测（Cave, SDOI2008）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int NN = 1e5 + 4;
template <int SZ>
struct LCT {
  int ch[SZ][2], fa[SZ], rev[SZ];
  void clear(int x) { ch[x][0] = ch[x][1] = fa[x] = rev[x] = 0; }
  // 判断x是辅助树上父亲的右儿子
  inline int is_right_ch(int x) { return ch[fa[x]][1] == x; }
  // 判断x是否为辅助树的根（虚边父节点不认x为儿子）
  inline int is_root(int x) { return ch[fa[x]][0] != x && ch[fa[x]][1] != x; }
  void pushdown(int x) { // 下推翻转标记到左右儿子
    if (rev[x] == 0) return;
    int lx = ch[x][0], rx = ch[x][1];
    if (lx) swap(ch[lx][0], ch[lx][1]), rev[lx] ^= 1;
    if (rx) swap(ch[rx][0], ch[rx][1]), rev[rx] ^= 1;
    rev[x] = 0;
  }
  void pushup(int x) { // 从x向根递归下推所有懒标记
    if (!is_root(x)) pushup(fa[x]);
    pushdown(x);
  }
  void rotate_up(int x) {  // Splay旋转：将x向上旋转一级
    int y = fa[x], z = fa[y], chx = is_right_ch(x), chy = is_right_ch(y),
        &t = ch[x][chx ^ 1]; // t在x和y之间，方向与x-y相反
    fa[x] = z;
    if (!is_root(y)) ch[z][chy] = x;              // x和y在z的同一侧
    ch[y][chx] = t, fa[t] = y, t = y, fa[y] = x;  // 保证t仍在x和y之间
  }
  void splay(int x) { // 将x旋转为辅助树的根
    pushup(x);  // 先下推从根到x的所有翻转标记
    for (int f = fa[x]; f = fa[x], !is_root(x); rotate_up(x))
      if (!is_root(f)) rotate_up(is_right_ch(x) == is_right_ch(f) ? f : x);
  }
  void access(int x) {  // 将根到x的路径变为首选边（实链）
    for (int f = 0; x; f = x, x = fa[x]) splay(x), ch[x][1] = f;
  }
  void make_root(int x) {  // 将x变为所在原树的根（翻转整条路径）
    access(x), splay(x), swap(ch[x][0], ch[x][1]), rev[x] ^= 1;
  }
  void split(int x, int y) { make_root(x), access(y), splay(y); } // 将x-y路径提取到一棵Splay中
  int find_root(int x) {  // 寻找x所在原树的根
    access(x), splay(x);
    while (ch[x][0]) x = ch[x][0]; // 沿左子树走到最深处
    splay(x);
    return x;
  }
  void cut(int x, int y) {
    split(x, y);  // 将x变为根，提取x-y路径到y的Splay
    if (ch[y][0] == x && !ch[x][1]) ch[y][0] = fa[x] = 0; // 确认x和y直接相邻后断开
  }
  void link(int x, int y) {
    if (find_root(x) != find_root(y)) make_root(x), fa[x] = y; // 先判断不连通再连边
  }
};
LCT<NN> st;
int main() {
  int n, q, x, y;
  char op[16];
  scanf("%d%d", &n, &q);
  while (q--) {
    scanf("%s%d%d", op, &x, &y);
    switch (op[0]) {
      case 'Q':
        puts(st.find_root(x) == st.find_root(y) ? "Yes" : "No");
        break;
      case 'C':
        st.link(x, y);
        break;
      case 'D':
        st.cut(x, y);
        break;
      default:
        break;
    }
  }
  return 0;
}
// 46047349 [SDOI2008]CAVE 洞穴勘测 AC 100 176 632 2234 C++ 2020-12-13 22:37:56
```

## 例题42  快乐涂色（Happy Painting, UVa11994）

### 题目描述
给定一棵有根树（每个节点有一个父节点），每条边有一个初始颜色（用整数表示）。需要处理M个操作：
- `1 x y c`：将节点x的父边重新连接到节点y，并将这条边的颜色设为c。（如果x == y则忽略）
- `2 x y c`：将x到y路径上所有边的颜色都改为c。
- `3 x y`：查询x到y路径上有多少条边，以及有多少种不同的颜色。
N, M ≤ 10^5。

### 解题思路
1. **LCT维护边权**：将每条边的颜色信息挂在该边较深的那个节点上（clr[x] = 边(fa[x], x)的颜色）。这样路径查询时，路径上的每个节点（除LCA外）都携带一条边的颜色。
2. **颜色集合**：用位运算（bitmask）维护颜色集合，因为颜色种类有限。set[x]存储x所在Splay子树中所有边的颜色集合的位或。
3. **路径染色（paint）**：split(x, y)后，在y的Splay根节点上打lazy标记（mark[y] = c），同时set[y] = 1 << c。
4. **cut/link操作**：cut(x)操作是access(x) + splay(x)，然后断开x和其左子树（即x在原树中的父亲）的连接。link(x, y, c)先cut(x)，然后fa[x] = y, clr[x] = c。
5. **查询（query）**：split(x, y)后，从set[y]中统计不同颜色的位数（有多少个1），size[y]-1为路径边数。

### 算法方法
**LCT（Link-Cut Tree）维护边权 + 位运算颜色压缩**。边权挂在子节点上，用位运算压缩颜色集合，支持路径染色、重新连边和路径颜色统计。

### 复杂度分析
- **时间复杂度**：O(M log N)。每次LCT操作O(log N)。
- **空间复杂度**：O(N)，每个节点存储ch[2], fa, rev, size, clr, set, mark。

```cpp
// 例题42  快乐涂色（Happy Painting, UVa11994）
// 魏子豪 陈锋
#include <bits/stdc++.h>
const int NN = 1000005;
using namespace std;

template <int SZ>
struct LCT {  // clr[x]: x-fa[x]之间边权
  int ch[SZ][2], fa[SZ], rev[SZ], size[SZ], clr[SZ], set[SZ], mark[SZ];
  void init(int x) {
    ch[x][0] = ch[x][1] = fa[x] = 0;
    rev[x] = size[x] = clr[x] = set[x] = mark[x] = 0;
  }
  int is_right_ch(int x) { return ch[fa[x]][1] == x; }
  bool is_root(int x) { return ch[fa[x]][0] != x && ch[fa[x]][1] != x; }
  void maintain(int x) {
    int &sx = set[x], &sz = size[x], ls = ch[x][0], rs = ch[x][1];
    sx = 0, sz = 1;
    if (ls) sx |= set[ls] | (1 << clr[ls]), sz += size[ls];
    if (rs) sx |= set[rs] | (1 << clr[rs]), sz += size[rs];
  }
  void rotate_up(int x) {  //旋转和无根树的直接旋转不同
    int y = fa[x], d = is_right_ch(x), &t = ch[y][d], z = fa[y],
        cy_bak = clr[y], &cx = clr[x], &cy = clr[y];
    fa[x] = z;  // 辅助树中深度关系来说 t在x,y之间，x,y在z同一侧
    if (!is_root(y)) ch[z][is_right_ch(y)] = x;
    t = ch[x][d ^ 1];
    if (t)  // 边权挂在更深的点上
      fa[t] = y, cy = clr[t], clr[t] = cx, cx = cy_bak;
    else
      swap(cx, clr[y]);
    ch[x][d ^ 1] = y, fa[y] = x;
    maintain(y), maintain(x);
  }
  void pushup(int x) {
    if (!is_root(x)) pushup(fa[x]);
    pushdown(x);
  }
  void pushdown(int x) {  //将翻转标记和染色标记下传
    int ls = ch[x][0], rs = ch[x][1], &mk = mark[x];
    if (mk) {
      if (ls) clr[ls] = mark[ls] = mk, set[ls] = set[x];
      if (rs) clr[rs] = mark[rs] = mk, set[rs] = set[x];
      mk = 0;
    }
    if (rev[x]) {
      swap(ch[x][0], ch[x][1]);
      if (ls) rev[ls] ^= 1;
      if (rs) rev[rs] ^= 1;
      rev[x] = 0;
    }
  }
  void splay(int x) {
    pushup(x);
    for (int f = fa[x]; f = fa[x], !is_root(x); rotate_up(x))
      if (!is_root(f)) rotate_up(is_right_ch(x) == is_right_ch(f) ? f : x);
    maintain(x);
  }
  void access(int x) {
    for (int last = 0; x; x = fa[x])
      splay(x), ch[x][1] = last, last = x, maintain(last);
  }
  int find_root(int x) {
    access(x), splay(x);
    while (ch[x][0]) x = ch[x][0];
    splay(x);
    return x;
  }
  void make_root(int x) { access(x), splay(x), rev[x] ^= 1; }
  void split(int x, int y) { make_root(x), access(y), splay(y); }
  void cut(int x) {
    access(x), splay(x);  // x到Root拉成一条链 将x旋转至辅助树根
    int& ls = ch[x][0];
    if (ls) fa[ls] = 0, clr[ls] = 0, ls = 0;  // 左儿子就是树中x之父 直接断掉
  }
  void link(int x, int y, int color) {  // 实际数据中没有x为y父亲的情况
    access(y), splay(x);
    cut(x), fa[x] = y, clr[x] = color;  // 直接连边
  }
  // 使x成为所在树的根，然后将x-y的路径上的所有点加入一个Splay中
  void paint(int x, int y, int c) {
    int rx = find_root(x);
    if (rx != find_root(y)) return;  // x,y不连通
    // 根x-y是当前的首选路径, v是splay根, splay中只有x-y
    split(x, y), set[y] = 1 << c, mark[y] = c;
    make_root(rx);  // 还原树根
  }
  void query(int x, int y, int& sz, int& cc) {
    int rx = find_root(x);
    sz = 0, cc = 0;
    if (rx != find_root(y)) return;  //如果u和v不在同一颗树直接输出0 0
    split(x, y);
    for (int k = set[y]; k; k >>= 1) cc += k & 1;  //统计有几种不同的颜色
    sz = size[y] - 1;
    make_root(rx);  // 还原树根
  }
};

LCT<NN> T;
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  for (int n, m; cin >> n >> m;) {
    for (int i = 1; i <= n; i++) T.init(i);
    for (int i = 1, v; i <= n; i++) cin >> v, T.fa[i] = v;
    for (int i = 1, v; i <= n; i++) {
      cin >> v;
      if (T.fa[i]) T.clr[i] = v;  //将边权放在深度较深的点上
    }
    for (int i = 1, op, u, v, c; i <= m; i++) {
      cin >> op >> u >> v;
      switch (op) {
        case 1:
          cin >> c;  // x--c-→y
          if (u != v) T.link(u, v, c);
          break;
        case 2:
          cin >> c, T.paint(u, v, c);
          break;
        case 3:
          int sz, cc;
          T.query(u, v, sz, cc);
          printf("%d %d\n", sz, cc);
          break;
      }
    }
  }
  return 0;
}
// 24181017 11994 Happy Painting! Accepted C++11 0.390 2019-11-11 16:40:51
```
