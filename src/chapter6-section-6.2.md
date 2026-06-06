# 6.2 嵌套和分块数据结构

嵌套和分块数据结构是处理复杂查询的两类重要方法。嵌套数据结构将一种数据结构嵌入另一种中（如Fenwick树的每个节点是一棵树），分块则将数据分成若干块，每块内部预处理排序以加速查询。

> **学习目标**：掌握树套树的设计思想和分块的复杂度均衡原理，能根据n和m的数量级选择合适的结构。

## 理论基础

### 为什么需要学这个？

你肯定写过"区间查询+单点修改"——一棵线段树或者Fenwick树就够了。但面试官突然问："如果要查区间里比v大的元素有几个呢？"一棵树只能维护你告诉它的信息（max/min/sum），它不知道"排名"。

这就是嵌套和分块数据结构出场的时候。本质上，你需要一个结构同时具备两种能力：按位置快速定位（区间）和按数值排序查询（排名）。两种经典思路由此分岔：**树套树**（外层维护位置，内层维护排序）和**分块**（把数据切成√n块，块内排序）。

学完这一节，你会收获：树套树是如何把 Fenwick 树的每个节点变成一棵平衡BST的（以及它是怎么在 O(log² n) 时间内完成查询的）；分块为什么"块大小取√n"（以及背后的复杂度均衡推导）；树上分块怎样通过 DFS+栈 保证连通性。这些都是"遇到需要维护排名信息的区间查询"时的手册级解决方案。

### 核心概念

**树套树（Nested Data Structure）**：外层结构按位置索引（如Fenwick树），内层结构按数值排序（如名次树）。每个外层节点维护一个"区间内所有元素的有序集合"。查询"区间[L,R]中小于v的元素个数"时，把区间拆成 O(log n) 个Fenwick节点，每个节点在对应的名次树中二分——总复杂度 O(log² n)。

```
朴素做法（线段树每个节点维护排序vector）：修改 O(n log n)，爆炸
树套树（线段树节点内是平衡BST）：修改 O(log² n)，可接受
```

*树套树的本质是"用空间换操作复杂度降维"——把一次需要 O(n) 的区间暴力，拆成 log n 次 O(log n) 的子树查询。*

**分块与复杂度均衡**：将 n 个元素分成大小为 S 的块，对于"区间查询+单点修改"：
- 完整块查询用二分：O(n/S × log S)
- 两端零散部分暴力：O(S)
- 使两者均衡：O(n/S × log S) ≈ O(S)，解得 S ≈ √(n log n)，但实践中直接取 S = √n 就足够漂亮。

*Ω(√n) 是分块类算法的"魔力常数"——查询和修改都压在这个量级，不要求 log 但比 O(n) 好太多。*

**树上分块的直径约束**：在树上进行DFS时维护栈，当"自上次分块以来新增的节点数达到块大小阈值B"时，将栈中这些节点弹出作为一个块，当前节点u作为"省会"。这样保证：①每个块大小在[B, 2B)之间（最后一块≤3B）；②块内节点连通（都是DFS过程中顺序访问的）；③省会是块的"连通枢纽"。

**线段树套平衡树的空间复杂度分析**：线段树有O(n)个节点（准确地说，叶节点n个，内部节点约2n个），如果每个节点都维护一棵平衡树（如Treap或Splay树），总空间为：∑(每个节点管理的区间大小) = O(n log n)。这是因为：在二叉线段树中，第i层的节点管理区间长度为 n/2^i，该层有 2^i 个节点，该层所有节点管理的总元素个数为 n。而线段树共有约 log n 层，所以所有节点管理的元素总个数约为 n × log n。因此，如果将每个元素存储为其所在区间平衡树的一个节点，总空间为 O(n log n)。在实践中，如果n=200,000，n log n ≈ 200,000×18 ≈ 3.6×10^6个节点，每个节点约32字节，总内存约115MB——在竞赛环境的内存限制内（通常256MB或512MB）。值得注意的是，如果用Fenwick树替代线段树作为外层结构，空间可以进一步优化：Fenwick树的每个节点管理的区间大小恰为lowbit(i)，所有lowbit(i)之和约为 n log n / 2（约为线段树的一半），因为Fenwick树比线段树"稀疏"。

**数论分块的整除性质与莫队的关系**：数论中的经典结论：对于正整数n，⌊n/i⌋（i=1,2,...,n）只有O(√n)种不同的取值。证明：当 i ≤ √n 时，⌊n/i⌋ 最多有 √n 种取值；当 i > √n 时，⌊n/i⌋ < √n，也最多 √n 种取值。因此总取值数 ≤ 2√n。这个性质引发了一个重要应用：莫队算法处理形如"查询∑f(⌊a_i/k⌋)"这类问题时，可以先对⌊a_i/k⌋的取值进行分块预处理。当k变化时，每个a_i的⌊a_i/k⌋值只在O(√a_i)个位置发生变化，将这些变化位置作为莫队的"事件"排序后处理，总事件数O(n√A)（A=max(a_i)），配合莫队的指针移动即可高效处理离线查询。这与分块数据结构形成了互补：分块在线处理"区间+排名"查询（O(√n)每次），而莫队+数论分块离线批量处理"参数变化的整除查询"。

### 知识脉络

```
嵌套结构（树套树）
    → 外层按位置索引, 内层按数值排序
    → 每个外层节点维护一个"有序集合"（Fenwick+名次树）
    → O(log² n) 完成区间排名查询

分块结构
    → 块大小 = √n（复杂度均衡推导）
    → 块内排序 + 惰性更新标记
    → O(√n) 完成区间查询和单点修改

树上分块（为莫队服务）
    → DFS+栈, 阈值B触发分块
    → 保证连通性和大小约束
    → 将树上路径查询转化为块间查询
```

> **跨章关联**：树套树和分块是处理"区间+排名"查询的两条互补路线——树套树偏重在线高效查询，而分块偏重实现简单——与**3.2节**线段树的对比分析呼应了"数据结构选型取决于操作类型和复杂度要求"的核心思想；**3.9节**莫队算法与分块共享√n的复杂度均衡逻辑（莫队将√n用在"按块排序查询"上，分块将√n用在"按块维护有序"上），两者结合（莫队+分块）可以处理带修改的离线区间查询问题；**5.4节**的次小生成树也使用了类似的"枚举替换边"策略，说明"局部替代验证最优性"是一种跨领域的通用思维。

### 快速上手模板

```cpp
// 分块通用模板（区间查询+单点修改, O(√n)每次）
const int SIZE = 4096;  // √n
int n, A[maxn], block[maxn / SIZE + 1][SIZE];

// 查询区间[L, R]中小于v的元素个数
int query(int L, int R, int v) {
  int lb = L / SIZE, rb = R / SIZE, cnt = 0;
  if (lb == rb) {
    for (int i = L; i <= R; i++) if (A[i] < v) cnt++;
  } else {
    for (int i = L; i < (lb+1)*SIZE; i++) if (A[i] < v) cnt++;
    for (int i = rb*SIZE; i <= R; i++) if (A[i] < v) cnt++;
    // 完整块二分查找
    for (int b = lb+1; b < rb; b++)
      cnt += lower_bound(block[b], block[b]+SIZE, v) - block[b];
  }
  return cnt;
}
```

核心要点：
1. 块大小取 `SIZE = max(√n, 1024)` 或更大以优化cache
2. 修改后通过单元素冒泡维护块内有序（O(SIZE)）
3. 莫队分块求SIZE时考虑 O(n×q/SIZE + SIZE×q) 要使两者相等

## 「SCOI2005」王室联邦

### 题目描述
给定一棵N个节点的树和一个参数B，要求将树划分为若干"块"（每个节点恰好属于一个块），使得：
1. 每个块的大小（节点数）在[B, 3B]之间
2. 每个块的节点在原树中构成一个连通子图
3. 每个块指定一个"省会"节点，块内每个节点到省会的路径上所有节点都必须属于该块
4. 省会可以不在块内（即作为连接枢纽）

输出：块的数量、每个节点所属的块编号、每个块对应的省会节点编号。

### 解题思路
此题是树上莫队（Mo's Algorithm on Tree）的预处理基础——将树分块以便后续处理树上路径查询。核心算法是DFS+栈的方式：

1. 从根节点1开始DFS遍历整棵树
2. 维护一个栈记录DFS过程中访问的节点顺序
3. 每次进入一个子树前记录当前栈大小sz，递归处理子树后，如果栈的大小增加了至少B个，说明该子树中已积累了足够多的未分配节点
4. 此时以当前节点u为省会，将栈中从sz位置之后的所有节点弹出一并归入一个新块
5. DFS结束后，栈中剩余节点（包括根节点）归入以根为中心的最后一个块

这样能保证每个块的大小恰好接近B（在[B, 2B)之间，最后一个块可能略大但≤3B）。

### 算法方法
**树上分块（DFS + 栈）**：
- 利用DFS访问顺序的自然连续性保证块的连通性
- 以B为阈值触发分块操作
- 根节点的特殊处理：最后所有剩余节点归入以根为中心的块

这种分块方法为"树上莫队"算法提供了基础——后续可以将树上路径查询转化为块间查询。

### 复杂度分析
- **时间复杂度**：O(N)，只需一次DFS遍历整棵树
- **空间复杂度**：O(N)，邻接表存储树结构，栈最多存储N个节点

```cpp
// 「SCOI2005」王室联邦
// 陈锋
// 题目：树上分块 - 将树划分为大小在[B,3B]之间的连通块
#include <iostream>
#include <stack>
#include <vector>
using namespace std;

typedef long long LL;
const int NN = 1000 + 4;
vector<int> G[NN];       // 邻接表存储树
stack<int> S;            // DFS访问顺序栈
int N, B;                // N=节点数, B=块大小参数
int BCnt;                // 块的数量
int BId[NN];             // BId[i] = 节点i所属的块编号
int Cap[NN];             // Cap[i] = 第i个块的省会节点编号

// 树上分块DFS
// u: 当前访问节点, fa: 父节点
void dfs(int u, int fa) {
  size_t sz = S.size();  // 进入子树前栈的大小（作为基准）
  for (auto v : G[u]) {
    if (v == fa) continue;  // 避免回到父节点
    dfs(v, u);
    // 如果新增的未分配节点达到B个，就形成一个新块
    if (S.size() >= sz + B) {
      Cap[++BCnt] = u;      // 以当前节点u为新块的省会
      // 将栈中基准点之后的所有节点弹出，归入新块
      while (S.size() > sz) BId[S.top()] = BCnt, S.pop();
    }
  }
  S.push(u);  // 将当前节点入栈（在上方，但尚未分配）
  
  // 根节点的特殊处理：剩余未分配节点全部归入以根为中心的块
  if (u == 1)
    while (!S.empty()) BId[S.top()] = BCnt, S.pop();
}

int main() {
  ios::sync_with_stdio(false), cin.tie(nullptr);
  cin >> N >> B, BCnt = 0;
  // 读入树的边
  for (int i = 1, u, v; i < N; i++) {
    cin >> u >> v;
    G[u].push_back(v), G[v].push_back(u);
  }
  dfs(1, -1);
  
  // 输出块的数量
  cout << BCnt << endl;
  // 输出每个节点所属的块编号
  for (int i = 1; i <= N; i++) cout << BId[i] << (i == N ? "\n" : " ");
  // 输出每个块的省会节点编号
  for (int i = 1; i <= BCnt; i++) cout << Cap[i] << (i == BCnt ? "\n" : " ");
  return 0;
}
// 46047872 「SCOI2005」王室联邦 答案正确 100 3 504 1000 C++ 2020-12-13 23:33:34
```

## UVa11297 - Census

### 题目描述
维护一个n×n（n ≤ 500）的整数矩阵，支持两种操作：
- `q x1 y1 x2 y2`：查询子矩阵[x1..x2][y1..y2]中的最大值和最小值
- `c x y v`：将位置(x, y)的值修改为v

多组数据，每组数据先输入n，然后输入n×n矩阵；接着输入m（操作次数），然后m行操作。

### 解题思路
这是一个二维RMQ（区间最值查询）带修改的问题。采用简化的二维线段树：
- 对矩阵的每一行（x坐标），独立建立一棵一维线段树，维护该行各列区间的最大/最小值
- 查询子矩阵时，遍历所有涉及的行（x1到x2），对每行在列区间[y1, y2]上进行线段树查询，汇总所有行的结果
- 修改时，只更新对应行的线段树中对应列的值

虽然是"二维"但没有使用真正的二维线段树嵌套，而是"多棵一维线段树"的方式，实现更简单但查询时需要遍历行。

### 算法方法
**多行线段树（Row-wise Segment Tree）**：
- 数据结构：`NS[row][node]`表示第row行线段树的第node个节点
- 每个节点维护该行某列区间内的最大值和最小值
- 通过维护函数 `maintain(c, o)` 自底向上更新
- 查询按行逐行进行，每行调用 `query(c, ...)` 查询该行的列区间最值

### 复杂度分析
- **时间复杂度**：
  - 建树：O(n²)，每行独立建树O(n)，共n行
  - 查询：O(n log n)每次，遍历最多n行，每行线段树查询O(log n)
  - 修改：O(log n)每次，只需更新一行的一个叶子到根的路径
- **空间复杂度**：O(n²)，n×4n个节点，约500×2000=1e6个节点

```cpp
// UVa11297 - Census
// 陈锋
// 题目：二维RMQ - 查询子矩阵的最大值和最小值，支持单点修改
#include<stdio.h>
#include<algorithm>
#include<cstring>
using namespace std;

const int NN = 508, INF = 1e9;

struct SegTree2D {
  struct Node {
    int Max, Min;  // 该节点对应区间的最大值和最小值
    // 用另一个节点的值更新当前节点
    void update(const Node& nd) {
      Max = max(Max, nd.Max), Min = min(Min, nd.Min);
    }
  } NS[NN][NN * 4];  // 第一维：行编号；第二维：该行线段树的节点

  Node qAns;  // 查询过程中临时保存的汇总结果

  // 自底向上更新节点o（使用左右子节点更新）
  void maintain(int c, int o) {
    Node& nd = NS[c][o], ld = NS[c][2 * o], rd = NS[c][2 * o + 1];
    nd.Max = max(ld.Max, rd.Max), nd.Min = min(ld.Min, rd.Min);
  }

  // 为第c行建立线段树，节点o对应列区间[l, r]
  void build(int c, int o, int l, int r) {
    Node& nd = NS[c][o];
    if (l == r) {  // 叶子节点：直接读入矩阵值
      scanf("%d", &nd.Min), nd.Max = nd.Min;
      return;
    }
    int mid = (l + r) / 2, lc = o * 2, rc = o * 2 + 1;
    build(c, lc, l, mid), build(c, rc, mid + 1, r);
    maintain(c, o);  // 自底向上合并
  }

  // 在第c行查询列区间[qL, qR]的最值
  // 注意：此版本使用"中点拆分"的方式（非经典的"区间拆分"）
  void query(int c, int o, int l, int r, int qL, int qR) {
    if (l == qL && r == qR) {  // 区间完全匹配
      qAns.update(NS[c][o]);
      return;
    }
    int qM = (qL + qR) / 2, lc = o * 2, rc = o * 2 + 1;
    // 根据中点与当前区间的关系决定查询方向
    if (qM >= r) query(c, lc, l, r, qL, qM);
    else if (qM < l) query(c, rc, l, r, qM + 1, qR);
    else query(c, lc, l, qM, qL, qM), query(c, rc, qM + 1, r, qM + 1, qR);
  }

  // 修改第c行第x列的值为val
  void modify(int c, int x, int val, int o, int l, int r) {
    Node& nd = NS[c][o];
    if (l == r && l == x) {  // 找到目标叶子
      nd.Max = nd.Min = val;
      return;
    }
    int m = (l + r) / 2, lc = o * 2, rc = o * 2 + 1;
    if (m >= x) modify(c, x, val, lc, l, m);
    else if (m < x) modify(c, x, val, rc, m + 1, r);
    maintain(c, o);  // 自底向上更新路径上的节点
  }
};

SegTree2D ST;

int main() {
  char op[10];
  for (int m, n, x1, y1, x2, y2, v; scanf("%d", &n) != EOF;) {
    // 为每一行建立线段树
    for (int x = 1; x <= n; x++) ST.build(x, 1, 1, n);
    scanf("%d", &m);
    while (m--) {
      scanf("%s", op);
      if (op[0] == 'q') {  // 查询操作
        ST.qAns.Max = -INF, ST.qAns.Min = INF;  // 初始化查询结果
        scanf("%d%d%d%d", &x1, &y1, &x2, &y2);
        // 逐行查询，汇总所有行的结果
        for (int x = x1; x <= x2; x++) ST.query(x, 1, y1, y2, 1, n);
        printf("%d %d\n", ST.qAns.Max, ST.qAns.Min);
      }
      if (op[0] == 'c')  // 修改操作
        scanf("%d%d%d", &x1, &y1, &v), ST.modify(x1, y1, v, 1, 1, n);
    }
  }
  return 0;
}
// 25858184 11297 Census  Accepted  C++ 0.430 2020-12-17 09:28:06
```

## UVa11990 "Dynamic" Inversion

### 题目描述
给定一个1~n（n ≤ 200,000）的排列A[1..n]。然后依次处理m（m ≤ 100,000）次删除操作：
1. 输出当前排列中的逆序对总数
2. 然后删除值为x的元素（x保证存在）

要求对每次删除操作输出删除前的逆序对数量。

### 解题思路
这是一个动态逆序对问题。核心思路是：初始逆序对数可以通过普通Fenwick树O(n log n)计算；每次删除元素x时，需要快速知道x参与了多少对逆序对，从而从总数中减去。

删除x时，x贡献的逆序对包含两部分：
1. **x左边的比x大的数** — 这些"逆序对"的"左元素"在x左边
2. **x右边的比x小的数** — 这些"逆序对"的"右元素"在x右边

为了高效查询，使用**嵌套数据结构**：
- **FenwickRankTree**：外层Fenwick树按数组位置索引，每个Fenwick节点是一棵名次树（RankTree），维护该位置区间内所有元素值的排序信息
- 这样可以在O(log² n)时间内查询"区间内比某值大/小的元素个数"

另外还需维护已删除元素的信息：
- 用另一个普通Fenwick树记录"已删除的元素"，用于修正计算（排除已删除元素的影响）
- x右边比x小的数 = (总数比x小的) - (已删除的比x小的) - (x位置左边未删除的比x小的)

### 算法方法
**嵌套数据结构（Fenwick Tree + Rank Tree）**：
1. **名次树（RankTree）**：静态构建的平衡BST，支持：
   - `count(v, type)`：统计比v小/大的元素个数
   - `erase(v)`：懒删除标记元素
2. **FenwickRankTree**：每个Fenwick节点维护一棵名次树
   - `count(x, v, type)`：统计A[1..x]中比v小(type=0)或大(type=1)的元素个数
   - `erase(x, v)`：删除位置x的值v

### 复杂度分析
- **时间复杂度**：
  - 构建FenwickRankTree：O(n log² n)，每个元素在O(log n)个Fenwick节点中，每个插入O(log n)
  - 每次删除操作：O(log² n)，在O(log n)个Fenwick节点中查询和删除
  - 总复杂度：O((n+m)log² n)，约(3e5)×400=1.2e8，可接受
- **空间复杂度**：O(n log n)，名次树节点总数约n log n

```cpp
// UVa11990 "Dynamic" Inversion
// 刘汝佳
// 题目：动态逆序对 - 依次删除排列中的元素，每次输出删除前的逆序对数
#include<cstdio>
#include<vector>
#include<algorithm>
#include<cassert>
using namespace std;

// Fenwick树的lowbit操作
inline int lowbit(int x) { return x & -x; }

// 名次树节点
struct Node {
  Node *ch[2];  // 左右子节点：ch[0]=左, ch[1]=右
  int v;        // 节点存储的值（排序关键字）
  int s;        // 以该节点为根的子树中有效节点总数（未删除的）
  int d;        // 删除标记：0=有效, 1=已删除
  Node(): d(0) {}
  // 获取某侧子树的节点数（若为空返回0）
  int ch_s(int d) { return ch[d] == NULL ? 0 : ch[d]->s; }
};

// 名次树（Rank Tree / 顺序统计树）
// 支持统计比某值小/大的元素个数，支持懒删除
struct RankTree {
  int n, next;         // n=元素个数, next=节点分配下标
  int *v;              // 临时数组，用于排序后构建平衡树
  Node *nodes, *root;  // 节点池和根节点

  // 构造函数：用排序数组A构建平衡BST
  RankTree(int n, int* A): n(n) {
    nodes = new Node[n];  // 预分配n个节点
    next = 0;
    v = new int[n];
    for(int i = 0; i < n; i++) v[i] = A[i];
    sort(v, v + n);       // 排序
    root = build(0, n-1); // 递归构建平衡BST
    delete[] v;           // 临时数组不再需要
  }

  // 递归构建平衡二叉搜索树
  // 每次取中点作为根，保证树高度为O(log n)
  Node* build(int L, int R) {
    if(L > R) return NULL;
    int M = L + (R-L) / 2;               // 取中点
    int u = next++;
    nodes[u].v = v[M];                   // 节点的值
    nodes[u].ch[0] = build(L, M-1);      // 左子树
    nodes[u].ch[1] = build(M+1, R);      // 右子树
    // 更新子树大小（有效节点数）
    nodes[u].s = nodes[u].ch_s(0) + nodes[u].ch_s(1) + 1;
    return &nodes[u];
  }

  // type = 0：统计树中比v小的有效元素个数
  // type = 1：统计树中比v大的有效元素个数
  int count(int v, int type) {
    Node* u = root;
    int cnt = 0;
    while(u != NULL) {
      if(u->v == v) {
        // 找到目标值，加上同侧子树的元素数（满足大小关系）
        cnt += u->ch_s(type);
        break;
      }
      // 决定往左(c=0)还是往右(c=1)
      int c = (v < u->v ? 0 : 1);
      // 如果去的方向与需求相反，把另一侧所有的都算上
      if(c != type) cnt += u->s - u->ch_s(c);
      u = u->ch[c];
    }
    return cnt;
  }

  // 懒删除：标记v对应的节点为已删除
  // 前提：v在树中且尚未删除
  void erase(int v) {
    Node* u = root;
    while(u != NULL) {
      u->s--;  // 路径上每个节点的有效计数减1
      if(u->v == v) {
        assert(u->d == 0);  // 确保尚未删除
        u->d = 1;            // 标记为已删除
        return;
      }
      int c = (v < u->v ? 0 : 1);
      u = u->ch[c];
    }
    assert(0);  // 不应到达这里
  }

  ~RankTree() {
    delete[] nodes;
  }
};

// 嵌套名次树的Fenwick树
// 外层按位置索引，内层维护该位置区间内所有元素值的名次树
struct FenwickRankTree {
  int n;
  vector<RankTree*> C;  // C[i]维护[ i-lowbit(i)+1, i ]区间内元素的名次树

  // 初始化：为每个Fenwick节点建立名次树
  void init(int n, int* A) {
    this->n = n;
    C.resize(n + 1);  // 1-indexed
    // C[i]管理区间[i-lowbit(i)+1, i]，大小为lowbit(i)
    for(int i = 1; i <= n; i++) {
      C[i] = new RankTree(lowbit(i), A + i - lowbit(i) + 1);
    }
  }

  void clear() { for(int i = 1; i <= n; i++) delete C[i]; }

  // 统计A[1..x]中比v大(type=1)或比v小(type=0)的元素个数
  int count(int x, int v, int type) {
    int ret = 0;
    while(x > 0) {
      ret += C[x]->count(v, type);
      x -= lowbit(x);  // 跳到前一个Fenwick节点
    }
    return ret;
  }

  // 删除A[x] = v（在所有包含位置x的名次树中删除v）
  void erase(int x, int v) {
    while(x <= n) {
      C[x]->erase(v);
      x += lowbit(x);  // 跳到下一个包含x的Fenwick节点
    }
  }
};

// 普通Fenwick树（用于维护已删除元素信息）
struct FenwickTree {
  int n;
  vector<int> C;

  void init(int n) {
    this->n = n;
    C.resize(n + 1);
    fill(C.begin(), C.end(), 0);
  }

  // 前缀和：A[1] + A[2] + ... + A[x]
  int sum(int x) {
    int ret = 0;
    while(x > 0) {
      ret += C[x];
      x -= lowbit(x);
    }
    return ret;
  }

  // 单点加：A[x] += d
  void add(int x, int d) {
    while(x <= n) {
      C[x] += d;
      x += lowbit(x);
    }
  }
};

const int maxn = 200000 + 5;
const int maxm = 100000 + 5;
typedef long long LL;

int n, m, A[maxn], B[maxn], pos[maxn];
FenwickRankTree frt;  // 嵌套名次树的Fenwick树
FenwickTree f;        // 用于：1)计算初始逆序对 2)记录已删除元素

// 计算初始排列的逆序对数
LL inversion_pairs() {
  LL ans = 0;
  f.init(n);
  // 从后向前遍历，统计比当前元素小的元素个数
  for(int i = n; i >= 1; i--) {
    ans += f.sum(A[i] - 1);  // 查询比A[i]小的已遍历元素有几个
    f.add(A[i], 1);          // 将A[i]加入Fenwick树
  }
  return ans;
}

int main() {
  while(scanf("%d%d", &n, &m) == 2) {
    // 读入排列，同时建立值到位置的映射
    for(int i = 1; i <= n; i++) {
      scanf("%d", &A[i]);
      pos[B[i] = A[i]] = i;  // pos[值] = 位置
    }
    // 计算初始逆序对数
    LL cnt = inversion_pairs();
    
    // 初始化嵌套名次树的Fenwick树
    frt.init(n, A);
    // 初始化普通Fenwick树（用于记录已删除元素）
    f.init(n);
    
    for(int i = 0; i < m; i++) {
      printf("%lld\n", cnt);  // 输出当前逆序对数
      int x;
      scanf("%d", &x);
      f.add(x, 1);  // 标记x已被删除
      
      // 计算删除x后减少的逆序对数
      int a = frt.count(pos[x]-1, x, 1);  // x左边还有a个比x大（未被删的）
      int b = x - 1;                       // 总共比x小的数有x-1个
      int c = f.sum(x - 1);               // 已删除的比x小的数
      int d = frt.count(pos[x]-1, x, 0);  // x左边未删且比x小的数
      b -= c + d;                          // 剩余的：x右边未删且比x小的数
      
      cnt -= a + b;  // 逆序对减少 = 左边比x大 + 右边比x小
      frt.erase(pos[x], x);  // 在所有嵌套树中删除x
    }
  }
  return 0;
}
// 25878364	11990	``Dynamic'' Inversion	Accepted	C++	0.900	2020-12-23 09:02:59
```

## UVa12003 Array Transformer

### 题目描述
给定一个长度为n（n ≤ 300,000）的整数数组A[0..n-1]和一个参数u。进行m次操作，每次操作给定L, R, v, p（1-indexed，即L,R,p∈[1,n]）：
1. 查询区间A[L..R]中有多少个元素小于v，记结果为k
2. 将A[p]的值修改为 `(u * k) / (R - L + 1)`（整数除法）

重复m次后，输出最终的完整数组。

### 解题思路
这是一个"区间查询 + 单点修改"问题，但修改的值依赖于查询结果，必须在线处理。由于n,m都很大（300,000），需要使用分块（Sqrt Decomposition）技术：

1. **分块**：将数组分成大小为SIZE=4096的块（约√n）
2. **块内排序**：每块内维护排序后的数组副本，用于二分查找
3. **查询**：
   - 两端不完整块：逐一遍历（O(SIZE)）
   - 中间完整块：二分查找（O(log SIZE)）
4. **修改**：在原数组和排序块中同时更新，通过冒泡调整位置保持块内有序

### 算法方法
**分块（Block Decomposition / Sqrt Decomposition）**：
- 分块参数：SIZE = 4096
- 块内排序维护：`block[i]`为第i块元素的排序版本
- 查询时混合遍历和二分查找
- 修改时在块内做交换维护有序性（最多O(SIZE)的冒泡操作）

### 复杂度分析
- **时间复杂度**：
  - 查询：O(SIZE + (n/SIZE) × log SIZE) ≈ O(√n log √n) 每次，约4096+73×12≈5000
  - 修改：O(SIZE) 每次，块内冒泡最多移动SIZE个元素
  - 总：O(m√n)，约3e5×4e3=1.2e9（实际远小于此，因为修改和查询不是每次都有完整块遍历）
- **空间复杂度**：O(n)，存储原数组和分块排序数组

```cpp
// UVa12003 Array Transformer
// 刘汝佳
// 题目：数组变换 - 区间查询+单点修改，修改值依赖查询结果
#include<cstdio>
#include<algorithm>
using namespace std;

const int maxn = 300000 + 10;
const int SIZE = 4096;  // 块大小 ≈ sqrt(300000)

int n, m, u;
int A[maxn];                     // 原始数组
int block[maxn/SIZE+1][SIZE];   // 分块排序数组，block[i][j]为第i块的第j个元素

// 初始化：读入数据并分块排序
void init() {
  scanf("%d%d%d", &n, &m, &u);
  int b = 0, j = 0;  // b=当前块编号, j=当前块内的位置
  for(int i = 0; i < n; i++) {
    scanf("%d", &A[i]);
    block[b][j] = A[i];  // 放入当前块
    if(++j == SIZE) { b++; j = 0; }  // 块满，换下一块
  }
  // 对每个完整的块排序
  for(int i = 0; i < b; i++) sort(block[i], block[i] + SIZE);
  // 对最后不完整的块排序
  if(j) sort(block[b], block[b] + j);
}

// 查询区间[L, R]中小于v的元素个数k
int query(int L, int R, int v) {
  int lb = L / SIZE, rb = R / SIZE;  // 左右端点所在块编号
  int k = 0;
  
  if(lb == rb) {
    // 同一块内：直接遍历
    for(int i = L; i <= R; i++) if(A[i] < v) k++;
  } else {
    // 左端不完整块：逐一遍历
    for(int i = L; i < (lb+1)*SIZE; i++) if(A[i] < v) k++;
    // 右端不完整块：逐一遍历
    for(int i = rb*SIZE; i <= R; i++) if(A[i] < v) k++;
    // 中间完整块：二分查找（块内已排序）
    for(int b = lb+1; b < rb; b++)
      k += lower_bound(block[b], block[b] + SIZE, v) - block[b];
  }
  return k;
}

// 修改A[p]的值为x，并维护分块排序
void change(int p, int x) {
  if(A[p] == x) return;  // 值未变，无需修改
  
  int old = A[p], pos = 0;
  int *B = &block[p/SIZE][0];  // B指向p所在块的排序数组
  A[p] = x;  // 更新原始数组
  
  // 在排序块中找到old的位置，替换为x
  while(B[pos] < old) pos++;
  B[pos] = x;
  
  // 维护块内有序性（冒泡调整）
  if(x > old) {
    // 新值变大，向后冒泡
    while(pos < SIZE-1 && B[pos] > B[pos+1]) {
      swap(B[pos+1], B[pos]); pos++;
    }
  } else {
    // 新值变小，向前冒泡
    while(pos > 0 && B[pos] < B[pos-1]) {
      swap(B[pos-1], B[pos]); pos--;
    }
  }
}

int main() {
  init();
  while(m--) {
    int L, R, v, p;
    scanf("%d%d%d%d", &L, &R, &v, &p);
    L--; R--; p--;  // 转换为0-indexed
    
    int k = query(L, R, v);  // 查询区间内小于v的元素个数
    // 修改：新值 = (u * k) / (R-L+1)，注意使用long long防止溢出
    change(p, (long long)u * k / (R - L + 1));
  }
  // 输出最终数组
  for(int i = 0; i < n; i++) printf("%d\n", A[i]);
  return 0;
}
// 25878377	12003	Array Transformer	Accepted	C++	0.530	2020-12-23 09:05:32
```
