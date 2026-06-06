# 3.11 可持久化数据结构

## 例题55  树上异或（Tree, ACM/ICPC 2013南京在线赛, HDU4757）

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

int A[MAXN], RM[MAXN];  // 离散化
PNode VER[MAXN];
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  Null->left = Null->right = Null;
  int n, m, maxa = 0;
  cin >> n >> m;
  map<int, int> M;
  _for(i, 0, n) cin >> A[i], M[A[i]] = 0;
  for (map<int, int>::iterator p = M.begin(); p != M.end(); p++)
    p->second = maxa, RM[maxa] = p->first, maxa++;
  VER[0] = Null;
  _for(i, 0, n)  // 权值线段树
      VER[i + 1] = VER[i]->insert(0, maxa, M[A[i]]);

  for (int i = 0, u, v, k; i < m; i++) {
    cin >> u >> v >> k;
    int ans = query(VER[v], VER[u - 1], 0, maxa, k);
    cout << RM[ans] << endl;
  }
}
// Accepted 1480ms 33792kB 1578 C++(g++ 4.3.2)2020-12-13 23:19:23 27090723
```

## 例题57  自带版本控制功能的IDE（Version Controlled IDE, ACM/ICPC Hatyai 2012, UVa12538）

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

## 例题57  自带版本控制功能的IDE（Version Controlled IDE, ACM/ICPC Hatyai 2012, UVa12538）

```cpp
// 例题57  自带版本控制功能的IDE（Version Controlled IDE, ACM/ICPC Hatyai 2012, UVa12538）
// 陈锋
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
