# 3.11 可持久化数据结构

## 例题55  树上异或（Tree, ACM/ICPC 2013南京在线赛, HDU4757）

### 题目描述
给定一棵N个节点的树，每个节点有一个权值A[i]（0 ≤ A[i] < 2^16）。有M个查询，每个查询给出(u, v, x)，求节点u到v的路径上选择一个节点z，使得 `A[z] XOR x` 的值最大，输出该最大值。N, M ≤ 10^5。

### 解题思路
1. **可持久化Trie**：构建从根到每个节点的可持久化Trie，Ver[u]是根节点到节点u路径上所有节点权值的二进制字典树（Trie）版本。
2. **树上路径Trie表示**：路径(u, v)上的权值集合对应的Trie可以通过可持久化Trie的差分得到：`Trie(u) + Trie(v) - Trie(lca) - Trie(fa(lca))`。
3. **Trie插入**：从高位（第15位）到低位逐位插入。每个新版本在旧版本基础上新建一条路径，共享未修改的子树。每个节点维护cnt表示该子树中数的个数。
4. **查询最大异或**：从最高位开始贪心——如果与当前位相反的位所对应的子树中存在非零cnt（通过 `cnt[lu.ch[!f]] + cnt[lv.ch[!f]] - cnt[ld.ch[!f]] - cnt[lf.ch[!f]] > 0` 判断），则走相反位置，贡献1<<i到答案；否则走相同位置。
5. **LCA预处理**：用倍增法预处理LCA以快速找到路径端点的祖先。

### 算法方法
**可持久化Trie（Persistent Trie）+ 倍增LCA**。构建从根到每个节点的可持久化Trie，用差分思想表示路径上的集合，在Trie上贪心查询最大异或值。

### 复杂度分析
- **时间复杂度**：O((N+M) log MAXA)。每个Trie节点插入O(log MAXA)=16，每次查询O(log MAXA)。
- **空间复杂度**：O(N log MAXA)，Trie节点总数≈N*16=1.6M。

```cpp
// 例题55  树上异或（Tree, ACM/ICPC 2013南京在线赛, HDU4757）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i,a,b) for( int i=(a); i<(int)(b); ++i)
#define _rep(i,a,b) for( int i=(a); i<=(int)(b); ++i)
const int MAXH = 16, NN = 1e5 + 8, MM = NN * 32;
int A[NN], TC, Ver[NN];
vector<int> G[NN];
struct Trie { int ch[2], cnt; };
Trie B[MM]; // Trie内存分配
int newTrie() {
  int c = TC++;
  fill_n(B[c].ch, 2, 0), B[c].cnt = 0;
  return c;
}
int insert(int p, int v, int dep) {
  int np = newTrie();
  Trie &t = B[np], &t0 = B[p];
  t = t0, t.cnt = t0.cnt + 1;
  if (dep >= 0) {
    bool c = v & 1 << dep;
    t.ch[c] = insert(t0.ch[c], v, dep - 1);
  }
  return np;
}
int Fa[NN][MAXH + 1], D[NN]; // LCA
void dfs(int u, int f) {
  Fa[u][0] = f, D[u] = D[f] + 1;
  _rep(i, 1, MAXH) Fa[u][i] = Fa[Fa[u][i - 1]][i - 1];
  Ver[u] = insert(Ver[f], A[u], 15); // A[u] < 2^16
  for (auto v : G[u]) if (v != f) dfs(v, u);
}

int lca(int u, int v) {
  if (D[u] < D[v]) swap(u, v);
  int diff = D[u] - D[v];
  _rep(h, 0, MAXH) if (diff & (1 << h)) u = Fa[u][h];
  if (u == v) return u;
  for (int h = MAXH; h >= 0; h--)
    if (Fa[u][h] != Fa[v][h]) u = Fa[u][h], v = Fa[v][h];
  return Fa[u][0];
}
int query(int u, int v, int x) {
  int ans = 0, d = lca(u, v), ru = Ver[u], rv = Ver[v], rd = Ver[d], rf = Ver[Fa[d][0]];
  for (int i = 15; i >= 0; i--) { // x < 2^16，从高位到低位遍历
    bool f = !(x & 1 << i);
    const Trie &tu = B[ru], &tv = B[rv], &td = B[rd], &tf = B[rf];
    if (B[tu.ch[f]].cnt + B[tv.ch[f]].cnt > B[td.ch[f]].cnt + B[tf.ch[f]].cnt)
      ans |= 1 << i;
    else
      f = !f;
    ru = tu.ch[f], rv = tv.ch[f], rd = td.ch[f], rf = tf.ch[f];
  }
  return max(ans, x ^ A[d]);
}
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  for (int n, m, u, v, x; cin >> n >> m; ) {
    for (int i = 1; i <= n; i++) cin >> A[i], G[i].clear();
    for (int i = 1; i < n; i++)
      cin >> u >> v, G[u].push_back(v), G[v].push_back(u);
    Ver[0] = TC = 0, newTrie(), dfs(1, 0);
    while (m--)
      cin >> u >> v >> x, printf("%d\n", query(u, v, x));
  }
}
// 32535416 2020-02-19 16:52:41 Accepted  4757  1825MS  38120K  2045 B  G++
```

## 例题56  网格监控（Grid surveillance, IPSC 2011）

### 题目描述
在一个DIM x DIM（DIM=4096）的网格上进行在线操作。所有操作重复R轮，每轮依次执行Q个操作。操作分为两种：
- 类型1（加点）：在坐标(x,y)处添加一个值为v的点。坐标由前一操作的返回值c异或计算得到：`x = (x XOR c) % 4096 + 3`。
- 类型2（查询）：查询矩形(x1,y1)-(x2,y2)内的所有点的值之和。如果v=0则查询当前最新版本的区间和；如果v>0则查询第v个版本的区间和；如果v<0则查询从当前版本往回数|v|个版本的区间和。
所有操作共用全局版本号，每执行一次类型1操作版本号+1。

### 解题思路
1. **可持久化二维BIT**：二维BIT的每个位置C[i][j]维护一个vector<{version, cumulative_sum}>，每个版本在该位置记录累积和。使用版本号作为时间戳。
2. **更新操作**：每次更新时版本号+1，在二维BIT的路径上（lowbit迭代），每个C[i][j]的vector追加一个新的{version, cumulative_sum}对。
3. **查询操作**：在指定版本ver下查询前缀和。对于每个BIT路径上的C[i][j]，用lower_bound找到版本号≤ver的最近记录，取其累积和。
4. **矩形查询**：标准二维前缀和差分——`sum(xr, yr) - sum(xl-1, yr) - sum(xr, yl-1) + sum(xl-1, yl-1)`。
5. **输出优化**：结果不需要全部输出，只需从第qi+20000个结果开始输出（防止输出过多）。

### 算法方法
**可持久化二维BIT（版本化树状数组）**。每个BIT节点维护版本号有序序列和前缀累积和，支持任意历史版本的二维区间求和。

### 复杂度分析
- **时间复杂度**：每次更新O(log² DIM)，每次查询O(log² DIM * log V)（log V为版本二分查找开销）。总复杂度与操作数和轮数相关。
- **空间复杂度**：O(N * log² DIM)，每个更新在O(log² DIM)个BIT节点上追加记录。

```cpp
// 例题56  网格监控（Grid surveillance, IPSC 2011）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i,a,b) for( int i=(a); i<(int)(b); ++i)

template<int SZ>
struct BIT2D {
  struct Item {
    int ver, c;
    bool operator<(const Item& i) const {
      if (ver != i.ver) return ver < i.ver;
      return c < i.c;
    }
  };
  vector<Item> C[SZ][SZ];
  int vals[SZ][SZ], version;
  BIT2D() { version = 0; }
  int lowbit(int x) { return x & (x ^ (x - 1)); }
  void add(int x, int y, int c) {
    int ver = ++version;
    vals[x][y] += c;
    for (int i = x; i < SZ; i += lowbit(i))
      for (int j = y; j < SZ; j += lowbit(j)) {
        auto& v = C[i][j];
        v.push_back({ver, v.empty() ? c : v.back().c + c});
      }
  }
  // 版本ver中，[0,0] → [x,y] 区域的元素和
  int sum(int x, int y, int ver) {
    int ret = 0;
    for (int i = x; i > 0; i -= lowbit(i))
      for (int j = y; j > 0; j -= lowbit(j)) {
        auto &v = C[i][j];
        auto it = lower_bound(v.begin(), v.end(), (Item) {ver + 1, 0});
        if (it != v.begin()) ret += (--it)->c;
      }
    return ret;
  }
};

const int DIM = 4096;
int XM(int x, int C) { return (x ^ C) % 4096 + 3; }
BIT2D < DIM + 16 > S;

struct OP {
  int type, x1, x2, y1, y2, v;
  int exec(int c) {
    if (type == 1) {
      int x = XM(x1, c), y = XM(y1, c);
      S.add(x, y, v);
      return S.vals[x][y];
    }

    int _x1 = XM(x1, c), _x2 = XM(x2, c), _y1 = XM(y1, c) , _y2 = XM(y2, c);
    int xl = min(_x1, _x2), xr = max(_x1, _x2), yl = min(_y1, _y2), yr = max(_y1, _y2);
    int ver; // 版本号
    if (v == 0) ver = S.version;
    else if (v > 0) ver = v;
    else if (v < 0) ver = max(S.version + v, 0);
    return S.sum(xr, yr, ver) + S.sum(xl - 1, yl - 1, ver)
           - S.sum(xl - 1, yr, ver) - S.sum(xr, yl - 1, ver);
  }
};

istream& operator>>(istream& is, OP& o) {
  is >> o.type;
  if (o.type == 1) is >> o.x1 >> o.y1;
  if (o.type == 2) is >> o.x1 >> o.x2 >> o.y1 >> o.y2;
  return is >> o.v;
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int r, q, qc = 0 ;
  cin >> r >> q;
  vector<OP> ops(q);
  for (auto& o : ops) {
    cin >> o;
    if (o.type == 2) qc++;
  }
  int c = 0, qi = 0;
  _for(i, 0, r) for (auto& o : ops) {
    c = o.exec(c);
    if (o.type == 2) {
      if (qi + 20000 >= r * qc) cout << c << endl;
      ++qi;
    }
  }
}
```

## 例题54  树上计数（Count on a tree, SPOJ COT）

### 题目描述
给定一棵N个节点的树，每个节点有一个权值W[i]。有M个查询，每个查询给出(u, v, k)，求节点u到v的路径上第k小的节点权值是多少。N ≤ 10^5, M ≤ 10^5。

### 解题思路
1. **可持久化权值线段树（主席树）**：从根节点开始DFS，每个节点在其父节点版本的权值线段树基础上插入自己的权值W[u]，形成可持久化线段树版本链。Ver[u] = 根到u路径上所有节点的权值线段树。
2. **树上路径线段树**：路径(u,v)上的权值集合对应的线段树可以通过差分得到：`Tree(u) + Tree(v) - Tree(lca) - Tree(fa(lca))`。在四棵线段树上同时进行二分查找。
3. **查询过程**：在区间[l, r)（离散化后的权值范围）上，计算左子树的元素个数 count = `pu->left->count + pv->left->count - pd->left->count - ppd->left->count`。如果count >= k，递归到左子树；否则k -= count，递归到右子树。
4. **离散化**：将节点权值离散化到[0, maxw)范围，RM数组记录每个离散值对应的原始权值。
5. **LCA预处理**：用倍增法预处理LCA和Tin/Tout时间戳。

### 算法方法
**可持久化线段树（主席树）+ 倍增LCA + 离散化**。构造树上路径的权值线段树，通过在四棵线段树上同时二分来查询路径上第k小的权值。

### 复杂度分析
- **时间复杂度**：O(N log N + M log N)。主席树构建O(N log N)，每次查询O(log N)。
- **空间复杂度**：O(N log N)，主席树节点数约N*log(N)，每个版本新建O(log N)个节点。

```cpp
// 例题54  树上计数（Count on a tree, SPOJ COT）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
const int MAXN = 100000 + 4, LN = 19;
int W[MAXN], RM[MAXN], maxw = 0;
map<int, int> WI;
vector<int> G[MAXN]; // 树结构以及LCA
int N, L, Tin[MAXN], Tout[MAXN], UP[MAXN][18], timer;

/* 主席树 */
struct Node;
typedef Node *PNode;
struct Node {
  int count;
  Node *left, *right;
  Node(int count, Node *left, Node *right)
    : count(count), left(left), right(right) {}
  Node *insert(int l, int r, int w);
};

PNode Null = new Node(0, nullptr, nullptr);
PNode Node::insert(int l, int r, int w) {
  if (l <= w && w < r) {  // need a new Node
    if (l + 1 == r) return new Node(count + 1, Null, Null);
    int m = (l + r) / 2;
    return new Node(count + 1, left->insert(l, m, w), right->insert(m, r, w));
  }
  return this;
}
PNode VER[MAXN];

// LCA
void dfs(int u, int fa) {
  Tin[u] = ++timer, UP[u][0] = fa;
  for (int i = 1; i < L; i++) UP[u][i] = UP[UP[u][i - 1]][i - 1];
  VER[u] = (u == 0 ? Null : VER[fa])->insert(0, maxw, WI[W[u]]);
  for (auto v : G[u]) if (v != fa) dfs(v, u);
  Tout[u] = ++timer;
}

bool isAncestor(int u, int v) { return Tin[u] <= Tin[v] && Tout[u] >= Tout[v]; }

int LCA(int u, int v) {
  if (isAncestor(u, v)) return u;
  if (isAncestor(v, u)) return v;
  for (int i = L; i >= 0; --i)
    if (!isAncestor(UP[u][i], v)) u = UP[u][i];
  return UP[u][0];
}

// 主席树查询 u,v,lca(u,v), pa(lca), get kth in [l,r)
int query(PNode pu, PNode pv, PNode pd, PNode ppd, int l, int r, int k) {
  if (l + 1 == r) return l;
  int count = pu->left->count + pv->left->count - pd->left->count -
              ppd->left->count,
              m = (l + r) / 2;
  if (count >= k)
    return query(pu->left, pv->left, pd->left, ppd->left, l, m, k);
  return query(pu->right, pv->right, pd->right, ppd->right, m, r, k - count);
}

int main() {
  int M;
  ios::sync_with_stdio(false), cin.tie(0);
  cin >> N >> M;
  L = ceil(log2(N));
  _for(i, 0, N) cin >> W[i], WI[W[i]];
  maxw = 0;
  for (auto it = WI.begin(); it != WI.end(); it++, maxw++)
    it->second = maxw, RM[maxw] = it->first;

  int u, v, k;
  _for(i, 0, N - 1) {
    cin >> u >> v, u--, v--;
    G[u].push_back(v), G[v].push_back(u);
  }
  Null->left = Null->right = Null;
  timer = 0;
  dfs(0, 0);
  while (M--) {
    cin >> u >> v >> k, u--, v--;
    int d = LCA(u, v),
        ans = query(VER[u], VER[v], VER[d],
                    (d == 0 ? Null : VER[UP[d][0]]), 0, maxw, k);
    cout << RM[ans] << endl;
  }
  return 0;
}
// 27147320 2020-12-23 07:33:54 Feng Chen Count on a tree accepted 4.03 82M CPP
```

## 例题53  区间第K小查询（K-th Number, SPOJ MKTHNUM）

### 题目描述
给定一个长度为N的整数序列A[1..N]和M个查询，每个查询给出(l, r, k)，输出区间A[l..r]中第k小的数。N ≤ 10^5, M ≤ 5000。

### 解题思路
1. **可持久化权值线段树（主席树）**：第i个版本的线段树存储了前i个元素（A[1..i]）在值域[0, maxa)上的分布情况。每个节点记录该值域区间内元素的出现次数count。
2. **版本差分**：区间[l, r]的权值分布 = VER[r] - VER[l-1]（两棵线段树的对应节点count相减）。
3. **二分查找**：从根节点开始，在值域[l, mid)上查找。计算左子树的元素个数count = `a->left->count - b->left->count`。如果count >= k，则第k小的数在左子树；否则k -= count，递归到右子树。
4. **持久化机制**：插入新值时，沿着从根到叶子的路径创建新的节点（路径长度O(log maxa)），路径之外共享旧版本的节点。每个版本的新增节点数 = O(log maxa)。
5. **离散化**：将原始序列值映射到[0, maxa)的紧凑区间，查询结果通过RM数组反查原始值。

### 算法方法
**可持久化线段树（主席树 / Persistent Segment Tree）+ 离散化**。每个前缀构建一棵权值线段树，通过版本差分实现区间查询第k小。

### 复杂度分析
- **时间复杂度**：O(N log N + M log N)。建树O(N log N)，每次查询O(log N)。
- **空间复杂度**：O(N log N)，主席树节点总数约N*log(N)。

```cpp
// 例题53  区间第K小查询（K-th Number, SPOJ MKTHNUM）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
const int MAXN = 100000 + 4;
struct Node;
typedef Node* PNode;
struct Node {  // 权值线段树
  int count;
  PNode left, right;
  Node(int count = 0, PNode left = NULL, PNode right = NULL)
      : count(count), left(left), right(right) {}
  PNode insert(int l, int r, int w);
};

const PNode Null = new Node();
PNode Node::insert(int l, int r, int w) {
  if (l <= w && w < r) {
    if (l + 1 == r) return new Node(count + 1, Null, Null);
    int m = (l + r) / 2;
    return new Node(count + 1, left->insert(l, m, w), right->insert(m, r, w));
  }
  return this;
}

int query(PNode a, PNode b, int l, int r, int k) {  // 二分查找逻辑
  if (l + 1 == r) return l;
  int m = (l + r) / 2;
  int count = a->left->count - b->left->count;
  if (count >= k) return query(a->left, b->left, l, m, k);
  return query(a->right, b->right, m, r, k - count);
}

int A[MAXN], RM[MAXN];  // A:原始数组, RM:离散值到原始值的映射
PNode VER[MAXN]; // VER[i]：前i个元素的权值线段树版本（根节点指针）
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  Null->left = Null->right = Null; // 空节点初始化（左右儿子都指向自己）
  int n, m, maxa = 0;
  cin >> n >> m;
  map<int, int> M;
  _for(i, 0, n) cin >> A[i], M[A[i]] = 0; // 统计所有出现过的值
  for (map<int, int>::iterator p = M.begin(); p != M.end(); p++)
    p->second = maxa, RM[maxa] = p->first, maxa++; // 离散化：分配连续的id
  VER[0] = Null; // 空版本的根节点
  _for(i, 0, n)  // 依次插入每个元素，构建可持久化线段树
      VER[i + 1] = VER[i]->insert(0, maxa, M[A[i]]); // 在前一版本基础上插入

  for (int i = 0, u, v, k; i < m; i++) {
    cin >> u >> v >> k;
    // 版本差分：VER[v]减去VER[u-1]得到区间[u,v]的权值线段树
    int ans = query(VER[v], VER[u - 1], 0, maxa, k);
    cout << RM[ans] << endl; // 映射回原始权值
  }
}
// Accepted 1480ms 33792kB 1578 C++(g++ 4.3.2)2020-12-13 23:19:23 27090723
```

## 例题57  自带版本控制功能的IDE（Version Controlled IDE, ACM/ICPC Hatyai 2012, UVa12538）

### 题目描述
你需要实现一个自带版本控制的文本编辑器（IDE）。支持三种操作：
- `1 p s`：在当前版本的第p个字符后插入字符串s，生成新版本。
- `2 p c`：在当前版本中删除从第p个字符开始的c个字符，生成新版本。
- `3 v p c`：查询第v个版本中从第p个字符开始的c个字符，输出到屏幕。

所有位置参数p和c都需要减去一个偏移量d，d为迄今所有类型3操作输出的字符'c'的总数（用于加密/纠偏）。N ≤ 50000（操作数）。

### 解题思路（可持久化Treap版本）
1. **可持久化Treap**：Treap（随机平衡二叉搜索树）的每个节点有随机key保证期望平衡。通过copyOf在修改时复制节点，实现结构共享的可持久化。
2. **核心操作**：
   - `split(pn, l, r, k)`：将Treap按前k个元素分裂为左右两棵子树。
   - `merge(a, b)`：合并两棵Treap（a中所有元素在b前）。
   - `insert(ver, pos, s)`：先split在pos处分裂，然后合并左子树+新字符串Treap+右子树。
   - `remove(ver, pos, n)`：两次split取出要删除的区间，merge首尾。
3. **版本管理**：VER[i]存储第i个版本的Treap根节点指针。每次修改操作返回新版本并ver++。
4. **持久化机制**：merge和split在修改节点时先copyOf创建副本再修改，旧版本不受影响。节点从预分配的数组Nodes中分配。

### 解题思路（rope版本）
1. **C++ STL rope**：GCC扩展库`__gnu_cxx::crope`提供了可持久化字符串——一种基于平衡树的字符串实现。
2. **自动持久化**：`crope`的赋值操作`version[ver++] = ro`自动复制了一份快照，后续修改不影响之前的版本。
3. **简洁操作**：`ro.insert(p, buf)`插入字符串，`ro.erase(p-1, c)`删除区间，`version[v].substr(p-1, c)`查询子串。

### 算法方法
**方法一**：**可持久化Treap（Persistent Treap）**，通过copy-on-write实现版本化，支持O(log N)的插入、删除和区间操作。

**方法二**：**GCC rope（可持久化平衡树字符串）**，利用STL内置的可持久化数据结构简化实现。

### 复杂度分析
- **Treap版本**：
  - 时间复杂度：每次操作O(log N)。split/merge路径长度O(log N)，每个节点copyOf O(1)。
  - 空间复杂度：O(N log N)，每次修改新建O(log N)个节点。
- **rope版本**：
  - 时间复杂度：每次操作均摊O(log N)。
  - 空间复杂度：O(N log N)。

```cpp
// 例题57  自带版本控制功能的IDE（Version Controlled IDE, ACM/ICPC Hatyai 2012, UVa12538）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (decltype(b) i = (a); i < (b); ++i)
const int MAXN = (1 << 23), MAXQ = 50000 + 4;
struct Node;
typedef Node *PNode;
PNode Null, VER[MAXQ];
struct Node {
  PNode left, right;
  char label;  // user def label
  int key, sz;
  Node(char c = 0, int s = 1) : label(c), sz(s) {
    left = right = Null, key = rand();
  }
  PNode update() {
    sz = 1 + left->sz + right->sz;
    return this;
  }
};
Node Nodes[MAXN];
struct Treap {
  int bufIdx = 0, d;  // this problem need.
  PNode copyOf(PNode u) {
    if (u == Null) return u;
    PNode ret = &Nodes[bufIdx++];
    *ret = *u;
    return ret;
  }
  PNode merge(PNode a, PNode b) {
    if (a == Null) return copyOf(b);
    if (b == Null) return copyOf(a);
    PNode ret;
    if (a->key < b->key)
      ret = copyOf(a), ret->right = merge(a->right, b);
    else
      ret = copyOf(b), ret->left = merge(a, b->left);
    return ret->update();
  }
  void split(PNode pn, PNode &l, PNode &r, const int k) {
    int psz = pn->sz, plsz = pn->left->sz;
    if (k == 0)
      l = Null, r = copyOf(pn);
    else if (psz <= k)
      l = copyOf(pn), r = Null;
    else if (plsz >= k)
      r = copyOf(pn), split(pn->left, l, r->left, k), r->update();
    else
      l = copyOf(pn), split(pn->right, l->right, r, k - plsz - 1), l->update();
  }

  PNode build(int l, int r, const char *s) {
    if (l > r) return Null;
    int m = (l + r) / 2;
    Node u(s[m]);
    PNode a = copyOf(&u), p = build(l, m - 1, s), q = build(m + 1, r, s);
    p = merge(p, a), a = merge(p, q);
    return a->update();
  }
  PNode insert(const PNode ver, int pos, const char *s) {
    PNode p, q, r = build(0, strlen(s) - 1, s);
    split(ver, p, q, pos);
    return merge(merge(p, r), q);
  }
  PNode remove(PNode ver, int pos, int n) {
    PNode p, q, r;
    split(ver, p, q, pos - 1), split(q, q, r, n);
    return merge(p, r);
  }
  void print(PNode ver) {
    if (ver == Null) return;
    print(ver->left), d += (ver->label == 'c');
    putchar(ver->label);
    print(ver->right);
  }
  void debugPrint(PNode pn) {
    if (pn == Null) return;
    debugPrint(pn->left), putchar(pn->label), debugPrint(pn->right);
  }
  void traversal(PNode pn, int pos, int n) {
    PNode p, q, r;
    split(pn, p, q, pos - 1), split(q, q, r, n), print(q);
  }
  void init() { bufIdx = 0, d = 0, Null = &Nodes[bufIdx++], Null->sz = 0; }
};
Treap tree;
int main() {
  int n, opt, v, p, c, ver = 0;
  scanf("%d", &n), tree.init();
  char s[128];
  VER[0] = Null;
  _for(i, 0, n) {
    scanf("%d", &opt);
    switch (opt) {
      case 1:
        scanf("%d %s", &p, s), p -= tree.d;
        VER[ver + 1] = tree.insert(VER[ver], p, s), ver++;
        break;
      case 2:
        scanf("%d %d", &p, &c), p -= tree.d, c -= tree.d;
        VER[ver + 1] = tree.remove(VER[ver], p, c), ver++;
        break;
      case 3:
        scanf("%d%d%d", &v, &p, &c), v -= tree.d, p -= tree.d, c -= tree.d;
        tree.traversal(VER[v], p, c), puts("");
        break;
      default:
        break;
    }
  }
  return 0;
}
// Accepted 280ms 3205 C++5.3.0 2020-12-13 23:23:21 25844155
```

## 例题57  自带版本控制功能的IDE（rope实现版本）

### 题目描述
（同上题，使用C++ GCC扩展库rope的更简洁实现。）

### 解题思路
使用`__gnu_cxx::crope`（可持久化字符串rope），它是GCC STL扩展中基于平衡树的可持久化字符串类型。每次对rope的修改操作都自动创建新版本（通过赋值和快照机制），版本通过`version[ver++] = ro`保存。插入使用`ro.insert(p, buf)`，删除使用`ro.erase(p-1, c)`，子串查询使用`version[v].substr(p-1, c)`获得。

### 算法方法
**GCC crope（可持久化平衡树字符串）**。利用STL内置rope数据结构的自动持久化特性。

### 复杂度分析
- **时间复杂度**：每次操作均摊O(log N)。
- **空间复杂度**：O(N log N)，rope内部自动管理版本节点的存储。

```cpp
// 例题57  自带版本控制功能的IDE（Version Controlled IDE, ACM/ICPC Hatyai 2012, UVa12538）
// rope实现版本
#include <bits/stdc++.h>

#include <ext/rope>
using namespace std;
using namespace __gnu_cxx;
crope ro, version[50100];

int main() {
  int n, d = 0, ver = 1;
  string buf;
  cin >> n;
  for (int i = 0, opt, p, c, v; i < n; i++) {
    cin >> opt;
    switch (opt) {
      case 1:
        cin >> p >> buf, p -= d;
        ro.insert(p, buf.c_str()), version[ver++] = ro;  // 保留历史版本
        break;
      case 2:
        cin >> p >> c, p -= d, c -= d;
        ro.erase(p - 1, c), version[ver++] = ro;  // 保留历史版本
        break;
      default:
        cin >> v >> p >> c;
        v -= d, p -= d, c -= d;
        const crope& tmp = version[v].substr(p - 1, c);
        for (size_t i = 0; i < tmp.size(); i++) {
          char c = tmp[i];
          d += (c == 'c'), cout << c;
        }
        cout << endl;
        break;
    }
  }
  return 0;
}
// Accepted 270ms 941 C++5.3.0 2020-12-13 23:28:49 25844185
```
