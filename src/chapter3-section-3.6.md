# 3.6 排序二叉树

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
#include<cstdio>
#include<algorithm>
#include<vector>
using namespace std;

const int maxn = 400000 + 20;
unsigned powers[maxn];

struct Node *null, *pit;
struct Node {
  Node *ch[2];
  int s;           // number of nodes in the subtree
  int flip;        // if flip=1, children and hashes are ALREADY swapped, so ch[0] and h1 are always corresponding to left child
  int v;           // value
  unsigned h1, h2; // hash

  Node() {}
  Node(int v) : flip(0), s(1), v(v), h1(v), h2(v) { ch[0] = ch[1] = null; }

  void *operator new(size_t) { return pit++; }

  // k = 1 means the smallest node
  int cmp(int k) const {
    int d = k - ch[0]->s;
    if(d == 1) return -1;
    return d <= 0 ? 0 : 1;
  }
  void maintain() {
    s = ch[0]->s + ch[1]->s + 1;
    h1 = ch[0]->h1*powers[ch[1]->s+1] + v*powers[ch[1]->s] + ch[1]->h1;
    h2 = ch[1]->h2*powers[ch[0]->s+1] + v*powers[ch[0]->s] + ch[0]->h2;
  }
  void reverse() {
    flip ^= 1;
    swap(ch[0], ch[1]);
    swap(h1, h2);
  }
  void pushdown() {
    if(flip) {
      flip = 0;
      ch[0]->reverse();
      ch[1]->reverse();
    }
  }
}pool[maxn];

void init_null() {
  null = new Node();
  null->s = 0;
}

void rotate(Node* &o, int d) {
  Node* k = o->ch[d^1]; o->ch[d^1] = k->ch[d]; k->ch[d] = o;
  o->maintain(); k->maintain(); o = k; 
}

// k >= 1
void splay(Node* &o, int k) {
  o->pushdown();
  int d = o->cmp(k);
  if(d == 1) k -= o->ch[0]->s + 1;
  if(d != -1) {
    Node* p = o->ch[d];
    p->pushdown();
    int d2 = p->cmp(k);
    int k2 = (d2 == 0 ? k : k - p->ch[0]->s - 1);
    if(d2 != -1) {
      splay(p->ch[d2], k2);
      if(d == d2) rotate(o, d^1); else rotate(o->ch[d], d);
    }
    rotate(o, d^1);
  }
}

#include<cstring>
struct SplaySequence {
  char* s;
  Node *root;

  // build s[L,R)
  Node* build(int L, int R) {
    int M = L + (R - L) / 2;
    Node* o = new Node(s[M]);
    if(L < M) o->ch[0] = build(L, M);
    if(M+1 < R) o->ch[1] = build(M+1, R);
    o->maintain();
    return o;
  }

  // update dummy nodes
  // root: dummy min node
  // root->ch[1]: dummy max node
  // root->ch[1]->ch[0]: actual sequence
  void update_dummy() {
    root->ch[1]->maintain();
    root->maintain();
  }

  Node* last() const {
    return root->ch[1]->ch[0];
  }

  Node* build(char* s) {
    this->s = s;
    root = new Node('[');
    root->ch[1] = new Node(']');
    root->ch[1]->ch[0] = build(0, strlen(s));
    update_dummy();
    return root;
  }

  // splay and returns the range [L,R)
  // L >= 1
  Node*& range(int L, int R) {
    splay(root, L);
    splay(root->ch[1], R-L+1);
    return root->ch[1]->ch[0];
  }

  void print(Node* o, int flip) {
    if(o == null) return;
    if(!flip) { print(o->ch[0], o->flip); printf("%c", o->v); print(o->ch[1], o->flip); }
    else { print(o->ch[1], o->flip); printf("%c", o->v); print(o->ch[0], o->flip); }
  }

  void print() {
    print(root, 0);
    printf("\n");
  }

};

#include<cstdlib>
#include<ctime>
SplaySequence ss;
char s[maxn];
int main()
{
  int n, m;
  powers[0] = 1;
  for(int i = 1; i < maxn; i++)
    powers[i] = powers[i-1]*3137;


  while(scanf("%d%d%s", &n, &m, s) == 3) {
    SplaySequence ss;
    pit = pool;
    init_null();
    ss.build(s);
    //ss.print();
    while (m--) {
      int op, x, y;
      scanf("%d%d", &op, &x);
      // 1 p c, insert jewel c after position p (0<=p<=L), p=0 means before the whole string
      if(op == 1) { 
        scanf("%d", &y);
        ss.range(x+1, x+1) = new Node(y+'0');
        ss.update_dummy();
        //ss.print();
      }
      // 2 p, remove the jewel at position p (1<=p<=L)
      else if(op == 2) {
        ss.range(x, x+1) = null;
        ss.update_dummy();
        //ss.print();
      }
      // 3 p1 p2, reverse the part starting from position p1, ending at position p2 (1<=p1<p2<=L)
      else if(op == 3) {
        scanf("%d", &y);
        ss.range(x, y+1)->reverse();
        ss.update_dummy();
        //ss.print();
      }
      // 4 p1 p2, output the LCP length of jewel strings starting from p1 and p2 (1<=p1<p2<=L)
      else {
        scanf("%d", &y);
        int L = 0, R = ss.root->s - y;
        while(L < R-1) {
          int M = L + (R-L)/2;
          unsigned h1 = ss.range(x, x+M)->h1;
          unsigned h2 = ss.last()->h2;
          h1 -= ss.range(y, y+M)->h1;
          h2 -= ss.last()->h2;
          if(!h1 && !h2) L = M; else R = M;
        }
        printf("%d\n", L);
      }
    }
  }
  fprintf(stderr, "time = %.3lf\n", clock() / (double)CLOCKS_PER_SEC);
  return 0;
}
// 25877640	11996	Jewel Magic	Accepted	C++	1.170	2020-12-23 06:11:55
```
