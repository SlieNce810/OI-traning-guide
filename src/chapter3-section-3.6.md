# 3.6 排序二叉树

## 例题30  图询问（Graph and Queries, Tianjin 2010, LA 5031/HDU3726）

```cpp
// 例题30  图询问（Graph and Queries, Tianjin 2010, LA 5031/HDU3726）
// 刘汝佳
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;

struct Node {
  Node* ch[2];  // 左右子树
  int r;        // 随机优先级
  int v;        // 值
  int s;        // 结点总数
  Node(int v) : v(v) {
    ch[0] = ch[1] = NULL;
    r = rand();
    s = 1;
  }
  int cmp(int x) const {
    if (x == v) return -1;
    return x < v ? 0 : 1;
  }
  void maintain() {
    s = 1;
    if (ch[0] != NULL) s += ch[0]->s;
    if (ch[1] != NULL) s += ch[1]->s;
  }
};
typedef Node* PNode;

void rotate(PNode &o, int d) {
  PNode k = o->ch[d ^ 1];
  o->ch[d ^ 1] = k->ch[d];
  k->ch[d] = o;
  o->maintain();
  k->maintain();
  o = k;
}

void insert(PNode &o, int x) {
  if (o == NULL)
    o = new Node(x);
  else {
    int d = (x < o->v ? 0 : 1);  // 不要用cmp函数，因为可能会有相同结点
    insert(o->ch[d], x);
    if (o->ch[d]->r > o->r) rotate(o, d ^ 1);
  }
  o->maintain();
}

void remove(PNode &o, int x) {
  int d = o->cmp(x);
  if (d == -1) {
    Node* u = o;
    if (o->ch[0] != NULL && o->ch[1] != NULL) {
      int d2 = (o->ch[0]->r > o->ch[1]->r ? 1 : 0);
      rotate(o, d2);
      remove(o->ch[d2], x);
    } else {
      if (o->ch[0] == NULL)
        o = o->ch[1];
      else
        o = o->ch[0];
      delete u;
    }
  } else
    remove(o->ch[d], x);
  if (o) o->maintain();
}

const int maxc = 500000 + 4;
struct Command {
  char type;
  int x, p;  // 根据type, p代表k或者v
} Cmds[maxc];
const int maxn = 20000 + 4, maxm = 60000 + 4;
int n, m, weight[maxn], from[maxm], to[maxm], removed[maxm];

// 并查集相关
int pa[maxn];
int findset(int x) { return pa[x] != x ? pa[x] = findset(pa[x]) : x; }

// 名次树相关
Node* root[maxn];  // Treap

int kth(Node* o, int k) {  // 第k大的值
  if (o == NULL || k <= 0 || k > o->s) return 0;
  int s = (o->ch[1] == NULL ? 0 : o->ch[1]->s);
  if (k == s + 1) return o->v;
  if (k <= s) return kth(o->ch[1], k);
  return kth(o->ch[0], k - s - 1);
}

void mergeto(Node*& src, Node*& dest) {
  if (src->ch[0]) mergeto(src->ch[0], dest);
  if (src->ch[1]) mergeto(src->ch[1], dest);
  insert(dest, src->v);
  delete src;
  src = NULL;
}

void removetree(Node*& x) {
  if (x->ch[0]) removetree(x->ch[0]);
  if (x->ch[1]) removetree(x->ch[1]);
  delete x;
  x = NULL;
}

// 主程序相关
void add_edge(int x) {
  int u = findset(from[x]), v = findset(to[x]);
  if (u != v) {
    if (root[u]->s < root[v]->s) {
      pa[u] = v;
      mergeto(root[u], root[v]);
    } else {
      pa[v] = u;
      mergeto(root[v], root[u]);
    }
  }
}

int query_cnt;
LL query_tot;
void query(int x, int k) {
  query_cnt++;
  query_tot += kth(root[findset(x)], k);
}

void change_weight(int x, int v) {
  int u = findset(x);
  remove(root[u], weight[x]);
  insert(root[u], v);
  weight[x] = v;
}

int main() {
  for (int kase = 1; scanf("%d%d", &n, &m) == 2 && n; kase++) {
    for (int i = 1; i <= n; i++) scanf("%d", &weight[i]);
    for (int i = 1; i <= m; i++) scanf("%d%d", &from[i], &to[i]);
    memset(removed, 0, sizeof(removed));

    int c = 0;  // 读命令
    while (true) {
      char type;
      int x, p = 0, v = 0;
      scanf(" %c", &type);
      if (type == 'E') break;
      scanf("%d", &x);
      if (type == 'D') removed[x] = 1;
      if (type == 'Q') scanf("%d", &p);
      if (type == 'C') scanf("%d", &v), p = weight[x], weight[x] = v;
      Cmds[c++] = (Command){type, x, p};
    }

    // 最终的图
    for (int i = 1; i <= n; i++) {
      pa[i] = i;
      if (root[i] != NULL) removetree(root[i]);
      root[i] = new Node(weight[i]);
    }
    for (int i = 1; i <= m; i++)
      if (!removed[i]) add_edge(i);

    // 反向操作
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

```cpp
// 例题29 优势人群（Efficient Solutions, UVa 11020）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;
struct Point {
  int x, y;
  bool operator<(const Point& p2) const {
    if (x != p2.x) return x < p2.x;
    return y < p2.y;
  }
};

int main() {
  int T;
  scanf("%d", &T);
  for (int n, x, y, t = 1; t <= T; t++) {
    scanf("%d", &n);
    if (t > 1) puts("");
    printf("Case #%d:\n", t);
    multiset<Point> s;
    for (int i = 0, x, y; i < n; i++) {
      scanf("%d%d", &x, &y);
      Point p = {x, y};
      multiset<Point>::iterator it = s.lower_bound(p);
      if (it == s.begin() || (--it)->y > p.y) {
        s.insert(p), it = s.upper_bound(p);
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

```cpp
// 例题31  排列变换（Permutation Transformer, UVa 11922）
// 刘汝佳
#include <algorithm>
#include <cstdio>
#include <vector>
using namespace std;

struct Node {
  Node* ch[2];
  int s, flip, v;
  int cmp(int k) const {
    int d = k - ch[0]->s;
    if (d == 1) return -1;
    return d <= 0 ? 0 : 1;
  }
  void maintain() { s = ch[0]->s + ch[1]->s + 1; }
  void pushdown() {
    if (flip) {
      flip = 0;
      swap(ch[0], ch[1]);
      ch[0]->flip = !ch[0]->flip;
      ch[1]->flip = !ch[1]->flip;
    }
  }
};

Node* null = new Node();

void rotate(Node*& o, int d) {
  Node* k = o->ch[d ^ 1];
  o->ch[d ^ 1] = k->ch[d];
  k->ch[d] = o;
  o->maintain();
  k->maintain();
  o = k;
}

void splay(Node*& o, int k) {  // 找到序列的左数第k个元素并伸展到根结点
  o->pushdown();
  int d = o->cmp(k);  // 看看第k个元素在整个树中的位置
  if (d == 1) k -= o->ch[0]->s + 1;  // 第k个元素在o的右子树中
  if (d == -1) return;               // 已经在根上了
  Node* p = o->ch[d];                // 第k个元素所在的子树
  p->pushdown();
  int d2 = p->cmp(k);  // 第k个元素是在p的左子树?→d2
  int k2 = (d2 == 0 ? k : k - p->ch[0]->s - 1);  // 在树中的排名
  if (d2 != -1) {          // 不是子树的根，伸展到p
    splay(p->ch[d2], k2);  // 伸展到p的子树根，下面旋转到p
    if (d == d2)
      rotate(o, d ^ 1);  // 一条直线
    else
      rotate(o->ch[d], d);  // 不是一条直线
  }
  rotate(o, d ^ 1);  // 从p旋转到o
}

// 合并left和right。假定left的所有元素比right小。注意right可以是null，但left不可以
Node* merge(Node* left, Node* right) {
  splay(left, left->s);
  left->ch[1] = right;
  left->maintain();
  return left;
}

// 把o的前k小结点放在left里，其他的放在right里。1<=k<=o->s。当k=o->s时，right=null
void split(Node* o, int k, Node*& left, Node*& right) {
  splay(o, k);
  left = o;
  right = o->ch[1];
  o->ch[1] = null;
  left->maintain();
}

const int NN = 100000 + 10;
struct SplaySequence {
  int n;
  Node seq[NN];
  Node* root;

  Node* build(int sz) {
    if (!sz) return null;
    Node* L = build(sz / 2);
    Node* o = &seq[++n];
    o->v = n;  // 节点编号
    o->ch[0] = L;
    o->ch[1] = build(sz - sz / 2 - 1);
    o->flip = o->s = 0;
    o->maintain();
    return o;
  }

  void init(int sz) { n = 0, null->s = 0, root = build(sz); }
};

vector<int> ans;
void print(Node* o) {
  if (o == null) return;
  o->pushdown();
  print(o->ch[0]);
  ans.push_back(o->v);
  print(o->ch[1]);
}

void debug(Node* o) {
  if (o == null) return;
  o->pushdown();
  debug(o->ch[0]);
  printf("%d ", o->v - 1);
  debug(o->ch[1]);
}

SplaySequence ss;
int main() {
  int n, m;
  scanf("%d%d", &n, &m);
  ss.init(n + 1);  // 最前面有一个虚拟结点
  for (int i = 0, a, b; i < m; i++) {
    scanf("%d%d", &a, &b);
    Node *left, *mid, *right, *o;
    split(ss.root, a, left, o);  // 如无虚拟结点，a将改成a-1，违反split的限制
    split(o, b - a + 1, mid, right);
    mid->flip ^= 1;
    ss.root = merge(merge(left, right), mid);
  }

  print(ss.root);
  for (size_t i = 1; i < ans.size(); i++)
    printf("%d\n", ans[i] - 1);  // 节点编号减1才是本题的元素值

  return 0;
}
// 24489045 11922 Permutation Transformer Accepted C++11 0.150 2020-01-31
// 04:01:04
```

## 例题32 魔法珠宝（Jewel Magic, UVa 11996）

```cpp
// 例题32 魔法珠宝（Jewel Magic, UVa 11996）
// Rujia Liu
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
