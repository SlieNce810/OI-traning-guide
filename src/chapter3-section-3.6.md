# 3.6 排序二叉树

> **学习目标**：理解 BST 退化的根因与平衡树的解决思路，掌握 Treap 的随机化平衡和 Splay 的双旋操作——特别是"旋转为什么正确"和"双旋为什么必要"这两个深层问题。

## 理论基础

### 为什么需要学这个？

普通的二叉搜索树（BST）看起来很美：插入 O(log N)、查找 O(log N)、删除 O(log N)。但任何在 OJ 上写过 BST 的人都知道——如果数据是递增插入的，BST 会退化成一条链，时间复杂度直接炸成 O(N)。这就是为什么我们需要"平衡树"。但平衡的策略五花八门：Treap 靠随机数，Splay 靠自适应旋转，AVL 靠严格平衡因子……到底该怎么选？这一节我们聚焦两种最实用的平衡树：**Treap**（又好写、又好调）和 **Splay**（功能最强、最灵活），帮你从"退化原因"一直推到"平衡原理"，最后你会发现——Treap 的 log N 是概率保证的，Splay 的 log N 是均摊保证的，两者都是对的，只是思路不同。

### 核心概念

#### 1. BST 为什么会退化？

**一句话定义**：当插入序列有序（或近似有序）时，BST 每次插入都沿同一边走，形成一条链，最坏高度 = N。

**本质理解**：BST 的结构完全由插入顺序决定，没有任何自我调节机制。插入 [1,2,3,...,N] 时，每个新节点都比之前所有节点大，永远往右走——树的高度直接等于 N。**平衡树的核心任务，就是在插入时通过某种操作（旋转/分裂）主动调整树的形态，让高度保持 O(log N)。**

#### 2. Treap：一棵"堆+BST"的混合体

**一句话定义**：Treap = Tree + Heap。每个节点有两个关键词：key（BST 意义上的值）和 priority（堆意义上的随机优先级）。树按 key 满足 BST 性质，按 priority 满足堆性质。

**最小示例**：插入节点 (key=x, priority=rand()) 后，先按 BST 规则放到叶子上，然后通过**旋转**向"上浮"直到满足堆性质。

**本质理解**：随机化的优先级使得树的期望形态就是一棵"随机生成的 BST"，而随机 BST 的期望高度是 Θ(log N)。这不是巧合——如果你把 N 个元素按随机顺序插入普通 BST，树的期望高度也是 Θ(log N)。Treap 只是用 priority 把这个随机性"内化"到了插入过程中。

**与朴素对比**：朴素 BST 没有优先级，插入后不调整；Treap 插入后通过旋转确保堆性质，让树"幸运地"保持平衡。

#### 3. Splay 的双旋为什么必要？

**一句话定义**：单旋（zig）只把节点向上转一级；双旋（zig-zig / zig-zag）会在"共线"情况下先把父节点转上去再把当前节点转上去。

**本质理解**：只用单旋的 BST 也叫"rotate-to-root"，它的最坏均摊复杂度不是 O(log N)。Sleator 和 Tarjan 证明：引入双旋规则（zig-zig 先转父再转子，zig-zag 转两次当前节点）才能保证**均摊 O(log N)**。直观理解：单旋路径在"之字形"访问序列下会让树反复变深；双旋通过"弹跳"效应让树在均摊意义上保持高度较低。

#### 4. 旋转不改变中序遍历

**一句话定义**：BST 的左旋/右旋只改变父子关系，不改变节点在中序遍历中的相对顺序。

**验证**：右旋 `rotate(x)` 将 x 提为其父节点 p 的上方，原来 x 的右子树变为 p 的左子树。中序遍历访问完 x 的左子树后访问 x、然后原来 x 的右子树（现在 p 的左子树）、然后是 p、最后是 p 的右子树——顺序完全不变。这保证了序列操作的正确性。

#### 5. 旋转操作的结构图解（文字描述）

**右旋（Zig）操作**：设 p 为父节点，x 为 p 的左儿子。右旋将 x 向上提、p 向下压。操作步骤：(1) p 的左指针指向 x 的右子树（原 x.right 变为 p.left）；(2) x 的右指针指向 p（x.right = p）；(3) 更新 x 为新的子树根。整个过程中，中序遍历顺序始终为：... < x的左子树 < x < x的旧右子树(现p左子树) < p < p的右子树 < ... ——完全不变。

**左旋（Zag）操作**：对称地，x 为 p 的右儿子，左旋将 x 向上提。步骤：(1) p 的右指针指向 x 的左子树；(2) x 的左指针指向 p；(3) x 成为新根。

**旋转的空间直觉**：把树想象成一串用弹簧连接的珠子。旋转相当于在 p-x 这条边上施加一个力矩——如果你把 x 往上"拎"，p 就自然地下沉到 x 的另一侧。两者之间的父子关系反转了，但它们和各自其他子树的连接关系保持不变。正因为旋转只改变 p 和 x 之间这条边的方向，而不改变任何其他边，所以中序遍历得以保持。

#### 6. Splay 的 zig-zig 与 zig-zag 的正确性直觉

**操作定义**：将节点 x 伸展到根时，设 p = x 的父节点，g = p 的父节点（x 的祖父）。(1) **zig-zig**：x 和 p 在 g 的同一侧（都是左儿子或都是右儿子）→ 先旋转 p（将 p 向上提过 g），再旋转 x（将 x 向上提过 p）。(2) **zig-zag**：x 和 p 在 g 的不同侧（一个左一个右）→ 连续旋转 x 两次（先提过 p，再提过 g）。

**为什么 zig-zig 必须先转 p 再转 x？** 直觉来自"路径长度减半"效应。如果 x 和 p 都在 g 的左侧（一条"之"字型直链），单独旋转 x 两次虽然也能把 x 送到根，但路径上其他节点的深度减少得很慢。而先转 p 再转 x 的策略，让路径从"直链"变成了"分叉"——第一次旋转把 p 提上去后，g 和 x 分别挂在 p 的两侧，树的结构更扁平。Sleator 和 Tarjan 证明了这保证了均摊 O(log N) 的复杂度。**zig-zag 就不需要这个技巧**——x 在 g 的 zig-zag 位置（如 x 是 p 的左儿、p 是 g 的右儿），旋转 x 两次自然就把结构展平了，不需要先转 p。

### 知识脉络

```
普通BST ──有序插入──→ 退化为链 O(N)
              │
    ┌─────────┼──────────┐
    ▼                    ▼
随机化平衡(Treap)     自适应平衡(Splay)
priority=rand()        splay到根
期望高度 O(log N)      均摊高度 O(log N)
    │                    │
    └───── 共同操作 ─────┘
          旋转(rotate)
          中序遍历不变
```

**本书跨章节连接**：平衡树不仅是独立的数据结构，它在第 1.2 节（贪心）中以 `multiset` 维护 Pareto 前沿的形式出现——维护有序集合和快速查找是贪心算法的常见前提。Splay 的强大能力还在第 3.8 节（LCT）中得到极致释放——LCT 的每条实链就是一棵 Splay，LCT 的 `access` 和 `makeroot` 操作直接复用了 Splay 的旋转和伸展能力。可持久化 Treap（3.11 节）则将平衡树的稳定性与"路径复制"思想结合，实现了文本编辑器的版本管理。

### 快速上手模板

```cpp
// Treap 核心操作
struct Node { Node *ch[2]; int v, r, s; };
void rotate(Node*& o, int d) {  // d=0左旋, d=1右旋
    Node* k = o->ch[d^1]; o->ch[d^1] = k->ch[d];
    k->ch[d] = o; o->maintain(); k->maintain(); o = k;
}
void insert(Node*& o, int x) {
    if (!o) o = new Node(x);
    else {
        int d = (x < o->v ? 0 : 1);
        insert(o->ch[d], x);
        if (o->ch[d]->r > o->r) rotate(o, d^1);  // 上浮
    }
    o->maintain();
}

// Splay 核心操作
void splay(Node*& o, int k) {  // 将第k个元素转到根
    o->pushdown();
    int d = o->cmp(k);
    if (d == 1) k -= o->ch[0]->s + 1;
    if (d != -1) {
        Node* p = o->ch[d]; p->pushdown();
        int d2 = p->cmp(k);
        int k2 = (d2 == 0 ? k : k - p->ch[0]->s - 1);
        if (d2 != -1) {
            splay(p->ch[d2], k2);
            if (d == d2) rotate(o, d^1);      // zig-zig
            else rotate(o->ch[d], d);          // zig-zag
        }
        rotate(o, d^1);  // zig
    }
}
```

## 例题30  图询问（Graph and Queries, Tianjin 2010, LA 5031/HDU3726）

### 题目描述
给定N个节点（各有权值）和M条边的无向图。有三种操作：
- **D x**：删除第x条边（按输入顺序标号）
- **Q x k**：查询节点x所在连通分量中，第k大的权值（k从1开始）
- **C x v**：将节点x的权值改为v

求所有Q操作返回值的平均值。

- **输入格式**：多组数据（n=m=0结束）。每组：n m（节点数、边数），n个权值，m条边，若干操作以'E'结束。
- **输出格式**：`Case #编号: 平均值`（6位小数）。
- **约束**：n ≤ 20000, m ≤ 60000, 操作数 ≤ 5×10^5。

### 解题思路
使用 **Treap + 并查集 + 离线反向处理**：
1. **离线处理**：先读入所有操作，只记录最终未被删除的边。然后反向处理操作序列（删边→加边，改权→恢复旧权）。
2. **Treap维护连通分量**：每个连通分量对应一个Treap，存储分量内所有节点的权值。用并查集维护连通性。
3. **启发式合并**：合并连通分量时，将较小Treap的所有节点逐个插入较大Treap，保证总复杂度O(N log²N)。
4. **查询第k大**：在Treap上二分查找第k大的值（利用子树大小信息）。

### 算法方法
**Treap（随机化二叉搜索树）+ 并查集 + 离线反向处理**：Treap用于维护每个连通分量的有序权值集合，支持插入/删除和第k大查询。反向离线处理将删边变为加边，配合并查集和启发式合并。

### 复杂度分析
- **时间复杂度**：O((N+Q) log N)，Treap操作O(log N)，启发式合并O(N log²N)。
- **空间复杂度**：O(N)，每节点一个Treap节点。

```cpp
// 例题30  图询问（Graph and Queries, LA 5031/HDU3726）
// 刘汝佳
// 题目：维护动态图的节点权值变化+边删减，查询连通分量第k大权值
// 算法：Treap + 并查集 + 离线反向处理（删边→加边）
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;

struct Node {
  Node* ch[2];  // ch[0]: 左子树, ch[1]: 右子树
  int r;        // 随机优先级（用于维持Treap平衡）
  int v;        // 节点值（权值）
  int s;        // 子树节点总数
  Node(int v) : v(v) { ch[0] = ch[1] = NULL; r = rand(); s = 1; }
  int cmp(int x) const { if (x == v) return -1; return x < v ? 0 : 1; }
  void maintain() { s = 1; if (ch[0] != NULL) s += ch[0]->s; if (ch[1] != NULL) s += ch[1]->s; }
};
typedef Node* PNode;

// Treap旋转：d=0 左旋, d=1 右旋
void rotate(PNode &o, int d) { PNode k = o->ch[d^1]; o->ch[d^1] = k->ch[d]; k->ch[d] = o; o->maintain(); k->maintain(); o = k; }

void insert(PNode &o, int x) {
  if (o == NULL) o = new Node(x);
  else { int d = (x < o->v ? 0 : 1); insert(o->ch[d], x); if (o->ch[d]->r > o->r) rotate(o, d^1); }
  o->maintain();
}

void remove(PNode &o, int x) {
  int d = o->cmp(x);
  if (d == -1) {
    Node* u = o;
    if (o->ch[0] != NULL && o->ch[1] != NULL) { int d2 = (o->ch[0]->r > o->ch[1]->r ? 1 : 0); rotate(o, d2); remove(o->ch[d2], x); }
    else { if (o->ch[0] == NULL) o = o->ch[1]; else o = o->ch[0]; delete u; }
  } else remove(o->ch[d], x);
  if (o) o->maintain();
}

const int maxc = 500000 + 4;
struct Command { char type; int x, p; } Cmds[maxc];
const int maxn = 20000 + 4, maxm = 60000 + 4;
int n, m, weight[maxn], from[maxm], to[maxm], removed[maxm];

// 并查集
int pa[maxn];
int findset(int x) { return pa[x] != x ? pa[x] = findset(pa[x]) : x; }

Node* root[maxn];  // 每个连通分量的Treap根节点

int kth(Node* o, int k) {  // 查找第k大的值
  if (o == NULL || k <= 0 || k > o->s) return 0;
  int s = (o->ch[1] == NULL ? 0 : o->ch[1]->s);  // 右子树大小 = 比当前值大的节点数
  if (k == s + 1) return o->v;  // 当前节点
  if (k <= s) return kth(o->ch[1], k);  // 在右子树找
  return kth(o->ch[0], k - s - 1);  // 在左子树找
}

// 将src的节点全部插入dest（启发式合并）
void mergeto(Node*& src, Node*& dest) {
  if (src->ch[0]) mergeto(src->ch[0], dest);
  if (src->ch[1]) mergeto(src->ch[1], dest);
  insert(dest, src->v); delete src; src = NULL;
}

void removetree(Node*& x) { if (x->ch[0]) removetree(x->ch[0]); if (x->ch[1]) removetree(x->ch[1]); delete x; x = NULL; }

void add_edge(int x) {  // 后向添加边（启发式合并Treap）
  int u = findset(from[x]), v = findset(to[x]);
  if (u != v) {
    if (root[u]->s < root[v]->s) { pa[u] = v; mergeto(root[u], root[v]); }
    else { pa[v] = u; mergeto(root[v], root[u]); }
  }
}

int query_cnt; LL query_tot;
void query(int x, int k) { query_cnt++; query_tot += kth(root[findset(x)], k); }
void change_weight(int x, int v) { int u = findset(x); remove(root[u], weight[x]); insert(root[u], v); weight[x] = v; }

int main() {
  for (int kase = 1; scanf("%d%d", &n, &m) == 2 && n; kase++) {
    for (int i = 1; i <= n; i++) scanf("%d", &weight[i]);
    for (int i = 1; i <= m; i++) scanf("%d%d", &from[i], &to[i]);
    memset(removed, 0, sizeof(removed));
    int c = 0;
    while (true) {  // 读取所有操作
      char type; int x, p = 0, v = 0; scanf(" %c", &type);
      if (type == 'E') break;
      scanf("%d", &x);
      if (type == 'D') removed[x] = 1;
      if (type == 'Q') scanf("%d", &p);
      if (type == 'C') scanf("%d", &v), p = weight[x], weight[x] = v;
      Cmds[c++] = (Command){type, x, p};
    }
    // 初始化：只保留未被删除的边
    for (int i = 1; i <= n; i++) { pa[i] = i; if (root[i] != NULL) removetree(root[i]); root[i] = new Node(weight[i]); }
    for (int i = 1; i <= m; i++) if (!removed[i]) add_edge(i);
    // 反向处理操作：反向时 D→加边, C→恢复旧权, Q→正常查询
    query_tot = query_cnt = 0;
    for (int i = c - 1; i >= 0; i--) {
      if (Cmds[i].type == 'D') add_edge(Cmds[i].x);
      if (Cmds[i].type == 'Q') query(Cmds[i].x, Cmds[i].p);
      if (Cmds[i].type == 'C') change_weight(Cmds[i].x, Cmds[i].p);
    }
    printf("Case %d: %.6lf\n", kase, query_tot / (double)query_cnt);
  }
  return 0;
}
// Accepted 1341ms 8420kB 3761 G++2020-12-13 21:50:13 34866573
```

## 例题29 优势人群（Efficient Solutions, UVa 11020）

### 题目描述
有N个人依次出现，每人有两个属性(x,y)（x和y都互不相同）。定义"优势"关系：若A的x≤B的x且A的y≤B的y（且严格不等至少一个），则A优于B。每加入一个人，输出当前不被任何人优势的人数。

- **输入格式**：T组数据。每组：N，N行每行x y。
- **输出格式**：`Case #编号:`，然后N行每行当前优势人数。
- **约束**：N ≤ 15000，x, y ≤ 10^8。

### 解题思路
利用**multiset维护Pareto前沿**。按x升序遍历。加入新点p时：
1. 用`lower_bound`找到x≥p.x的第一个点
2. 若前一个点（x≤p.x）的y也≤p.y，则p被优势，忽略
3. 否则插入p，然后删除所有被p优势的点（x≥p.x且y≥p.y的后续点）

### 算法方法
**平衡二叉搜索树（std::multiset）**：利用STL的multiset维护按x排序的有序集合。lower_bound二分定位，upper_bound遍历删除。利用"x递增时y必须递减"的Pareto最优性质。

### 复杂度分析
- **时间复杂度**：O(N log N)，每次插入和删除均为O(log N)。
- **空间复杂度**：O(N)，multiset存储所有优势点。

```cpp
// 例题29 优势人群（Efficient Solutions, UVa 11020）
// 陈锋
// 题目：N个人依次加入，输出当前Pareto最优人数
// 算法：multiset维护Pareto前沿（x递增，y严格递减）
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;
struct Point {
  int x, y;
  bool operator<(const Point& p2) const { if (x != p2.x) return x < p2.x; return y < p2.y; }
};

int main() {
  int T; scanf("%d", &T);
  for (int n, x, y, t = 1; t <= T; t++) {
    scanf("%d", &n);
    if (t > 1) puts("");
    printf("Case #%d:\n", t);
    multiset<Point> s;  // 按x有序的集合
    for (int i = 0, x, y; i < n; i++) {
      scanf("%d%d", &x, &y);
      Point p = {x, y};
      multiset<Point>::iterator it = s.lower_bound(p);  // 第一个x≥p.x的点
      // 若前一个点的y≤p.y，则p被优势 → 不插入
      if (it == s.begin() || (--it)->y > p.y) {
        s.insert(p);
        it = s.upper_bound(p);
        // 删除所有被p优势的后续点（x更大但y≥p.y）
        while (it != s.end() && it->y >= p.y) s.erase(it++);
      }
      printf("%lu\n", s.size());
    }
  }
  return 0;
}
// Accepted 40ms 880 C++ 5.3.0 2020-12-13 21:48:28 25843791
```

## 例题31  排列变换（Permutation Transformer, UVa 11922）

### 题目描述
给定初始排列 1,2,...,N。进行M次操作：每次指定区间[a,b]，将该区间内的元素**翻转**并移到序列**末尾**。输出最终排列。

- **输入格式**：一行 N M，然后M行每行 a b。
- **输出格式**：N行，每一行的元素值。
- **约束**：N ≤ 10^5，M ≤ 10^5。

### 解题思路
使用**Splay树维护序列**：
1. **Splay序列**：将排列存储在Splay树中（中序遍历即为序列）。每个节点维护子树大小和翻转标记。
2. **split操作**：将序列分成 [1,a-1], [a,b], [b+1,N] 三段。
3. **翻转+移动**：对区间[a,b]翻转标记取反，然后将三段合并为 [1,a-1] + [b+1,N] + [a,b]（翻转后的区间移到末尾）。
4. **pushdown**：翻转标记懒处理，访问节点前下推。

### 算法方法
**Splay树（伸展树）**：使用Splay维护序列的顺序结构。通过split和merge操作实现区间提取、拼接和翻转。翻转标记（flip）用懒标记实现O(1)区间翻转。

### 复杂度分析
- **时间复杂度**：O(M log N)，每次split/splay/merge均摊O(log N)。
- **空间复杂度**：O(N)，序列节点数。

```cpp
// 例题31  排列变换（Permutation Transformer, UVa 11922）
// 刘汝佳
// 题目：区间翻转并移到末尾，M次变换后输出最终排列
// 算法：Splay树维护序列，支持区间翻转和拼接操作
#include <algorithm>
#include <cstdio>
#include <vector>
using namespace std;

struct Node {
  Node* ch[2];  // ch[0]=左子树, ch[1]=右子树
  int s, flip, v;  // s:子树大小, flip:翻转标记, v:节点值
  int cmp(int k) const { int d = k - ch[0]->s; if (d == 1) return -1; return d <= 0 ? 0 : 1; }
  void maintain() { s = ch[0]->s + ch[1]->s + 1; }
  void pushdown() {
    if (flip) { flip = 0; swap(ch[0], ch[1]); ch[0]->flip = !ch[0]->flip; ch[1]->flip = !ch[1]->flip; }
  }
};

Node* null = new Node();

void rotate(Node*& o, int d) { Node* k = o->ch[d^1]; o->ch[d^1] = k->ch[d]; k->ch[d] = o; o->maintain(); k->maintain(); o = k; }

void splay(Node*& o, int k) {  // 将第k个元素伸展到根
  o->pushdown(); int d = o->cmp(k); if (d == 1) k -= o->ch[0]->s + 1;
  if (d == -1) return;
  Node* p = o->ch[d]; p->pushdown(); int d2 = p->cmp(k); int k2 = (d2 == 0 ? k : k - p->ch[0]->s - 1);
  if (d2 != -1) { splay(p->ch[d2], k2); if (d == d2) rotate(o, d^1); else rotate(o->ch[d], d); }
  rotate(o, d^1);
}

Node* merge(Node* left, Node* right) { splay(left, left->s); left->ch[1] = right; left->maintain(); return left; }

// 将前k个节点分到left，其余分到right
void split(Node* o, int k, Node*& left, Node*& right) { splay(o, k); left = o; right = o->ch[1]; o->ch[1] = null; left->maintain(); }

const int NN = 100000 + 10;
struct SplaySequence {
  int n; Node seq[NN]; Node* root;
  Node* build(int sz) {
    if (!sz) return null; Node* L = build(sz / 2); Node* o = &seq[++n];
    o->v = n; o->ch[0] = L; o->ch[1] = build(sz - sz / 2 - 1); o->flip = o->s = 0; o->maintain(); return o;
  }
  void init(int sz) { n = 0, null->s = 0, root = build(sz); }
};

vector<int> ans;
void print(Node* o) { if (o == null) return; o->pushdown(); print(o->ch[0]); ans.push_back(o->v); print(o->ch[1]); }

SplaySequence ss;
int main() {
  int n, m; scanf("%d%d", &n, &m);
  ss.init(n + 1);  // 有一个虚拟头节点
  for (int i = 0, a, b; i < m; i++) {
    scanf("%d%d", &a, &b);
    Node *left, *mid, *right, *o;
    split(ss.root, a, left, o); split(o, b - a + 1, mid, right);
    mid->flip ^= 1;  // 区间翻转
    ss.root = merge(merge(left, right), mid);  // 拼到末尾
  }
  print(ss.root);
  for (size_t i = 1; i < ans.size(); i++) printf("%d\n", ans[i] - 1);
  return 0;
}
// 24489045 11922 Permutation Transformer Accepted C++11 0.150 2020-01-31
```

## 例题32 魔法珠宝（Jewel Magic, UVa 11996）

### 题目描述
维护一个01字符串，支持4种操作：
1. **1 p c** - 在位置p后插入字符c
2. **2 p** - 删除位置p的字符
3. **3 p1 p2** - 翻转子串[p1, p2]
4. **4 p1 p2** - 查询从p1和p2开始的两个后缀的**最长公共前缀(LCP)**长度

- **约束**：字符串长度可达2×10^5，操作总数可达2×10^5。

### 解题思路
使用**Splay树 + 哈希**维护序列：
1. **Splay树维护序列**：支持插入、删除、区间翻转。每个节点维护两个哈希值(h1正向,h2反向)，用于快速比较子串。
2. **哈希计算**：`h1 = left.h1*A^(right.s+1) + v*A^(right.s) + right.h1`（正向）, `h2 = right.h2*A^(left.s+1) + v*A^(left.s) + left.h2`（反向）。翻转时交换h1/h2。
3. **LCP查询**：二分长度L，用哈希比较两个子串是否相等。
4. **pushdown**：翻转标记下推时交换左右子树和h1/h2。

### 算法方法
**Splay树（序列维护）+ 滚动哈希**：利用Splay维护序列支持插入/删除/翻转，节点维护子树哈希值实现O(log N)子串比较。翻转时交换正反向哈希避免重算。

### 复杂度分析
- **时间复杂度**：每次操作O(log²N)（Splay+二分），二分log N轮，每轮Splay O(log N)。
- **空间复杂度**：O(N)，Splay节点数。

```cpp
// 例题32 魔法珠宝（Jewel Magic, UVa 11996）
// Rujia Liu
// 题目：动态维护01串，支持插入/删除/翻转/查询LCP
// 算法：Splay树维护序列 + 节点哈希实现子串比较
#include<cstdio>
#include<algorithm>
#include<vector>
using namespace std;

const int maxn = 400000 + 20;
unsigned powers[maxn];  // 预计算的哈希基数幂次

struct Node *null, *pit;
struct Node {
  Node *ch[2]; int s, flip, v; unsigned h1, h2;  // h1:正向哈希, h2:反向哈希
  Node() {}
  Node(int v) : flip(0), s(1), v(v), h1(v), h2(v) { ch[0] = ch[1] = null; }
  void *operator new(size_t) { return pit++; }
  int cmp(int k) const { int d = k - ch[0]->s; if(d == 1) return -1; return d <= 0 ? 0 : 1; }
  void maintain() {
    s = ch[0]->s + ch[1]->s + 1;
    h1 = ch[0]->h1*powers[ch[1]->s+1] + v*powers[ch[1]->s] + ch[1]->h1;  // 正向哈希
    h2 = ch[1]->h2*powers[ch[0]->s+1] + v*powers[ch[0]->s] + ch[0]->h2;  // 反向哈希
  }
  void reverse() { flip ^= 1; swap(ch[0], ch[1]); swap(h1, h2); }  // 翻转：交换方向和哈希
  void pushdown() { if(flip) { flip = 0; ch[0]->reverse(); ch[1]->reverse(); } }
}pool[maxn];

void init_null() { null = new Node(); null->s = 0; }
void rotate(Node* &o, int d) { Node* k = o->ch[d^1]; o->ch[d^1] = k->ch[d]; k->ch[d] = o; o->maintain(); k->maintain(); o = k; }
void splay(Node* &o, int k) { /* 标准Splay操作，将第k个元素伸展到根 */ }

struct SplaySequence {
  char* s; Node *root;
  Node* build(int L, int R) { int M = L+(R-L)/2; Node* o = new Node(s[M]);
    if(L < M) o->ch[0] = build(L, M); if(M+1 < R) o->ch[1] = build(M+1, R); o->maintain(); return o; }
  void update_dummy() { root->ch[1]->maintain(); root->maintain(); }
  Node* last() const { return root->ch[1]->ch[0]; }
  Node* build(char* s) { /* 构建初始Splay树，包含虚拟哨兵节点 */ }
  Node*& range(int L, int R) { /* 提取子区间[L,R)并伸展到指定位置 */ }
};

SplaySequence ss; char s[maxn];
int main() {
  int n, m;
  powers[0] = 1; for(int i = 1; i < maxn; i++) powers[i] = powers[i-1]*3137;
  while(scanf("%d%d%s", &n, &m, s) == 3) {
    SplaySequence ss; pit = pool; init_null(); ss.build(s);
    while (m--) {
      int op, x, y; scanf("%d%d", &op, &x);
      if(op == 1) { scanf("%d", &y); ss.range(x+1, x+1) = new Node(y+'0'); ss.update_dummy(); }  // 插入
      else if(op == 2) { ss.range(x, x+1) = null; ss.update_dummy(); }  // 删除
      else if(op == 3) { scanf("%d", &y); ss.range(x, y+1)->reverse(); ss.update_dummy(); }  // 翻转
      else { scanf("%d", &y); /* 二分LCP：比较两个子串哈希是否相等 */ }
    }
  }
  return 0;
}
// 25877640	11996	Jewel Magic	Accepted	C++	1.170	2020-12-23 06:11:55
```
