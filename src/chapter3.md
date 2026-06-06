# 第3章 实用数据结构

## 3.1 基础数据结构回顾

### 例题6  合作网络（Corporative Network, Codeforces Gym 101461B）

```cpp
// 例题6  合作网络（Corporative Network, Codeforces Gym 101461B）
// Rujia Liu
#include <algorithm>
#include <iostream>
#include <string>
using namespace std;
const int maxn = 20000 + 10;
int pa[maxn], d[maxn];
int findset(int x) {
  if (pa[x] == x) return x;
  int root = findset(pa[x]);
  d[x] += d[pa[x]];
  return pa[x] = root;
}

int main() {
  freopen("network.in", "r", stdin);
  freopen("network.out", "w", stdout);
  ios_base::sync_with_stdio(false);
  int T;
  cin >> T;
  for (int kase = 0, n, u, v; kase < T; kase++) {
    string cmd;
    cin >> n;
    for (int i = 1; i <= n; i++) pa[i] = i, d[i] = 0;
    while (cin >> cmd && cmd[0] != 'O') {
      if (cmd[0] == 'E') cin >> u, findset(u), cout << d[u] << endl;
      if (cmd[0] == 'I') cin >> u >> v, pa[u] = v, d[u] = abs(u - v) % 1000;
    }
  }
  return 0;
}
// 102162738 Dec/24/2020 11:38UTC+8 B - Corporative Network GNU C++11 Accepted 343 ms 300 KB
```

### 例题3  阿格斯（Argus, Beijing 2004, POJ2051）

```cpp
// 例题3  阿格斯（Argus, Beijing 2004, POJ2051）
// 陈锋
#include<cstdio>
#include<queue>
using namespace std;

struct Item { // 优先队列中的元素
  int QNum, Period, Time;
  // 重要！优先级比较函数。优先级高的先出队
  bool operator < (const Item& a) const { // 这里的const必不可少，请读者注意
    if (Time != a.Time) return Time > a.Time;
    return QNum > a.QNum;
  }
};

int main() {
  priority_queue<Item> pq;
  char s[20];
  for (Item item; scanf("%s", s) && s[0] != '#'; pq.push(item)) {
    scanf("%d%d", &item.QNum, &item.Period);
    item.Time = item.Period; // 初始化“下一次事件的时间”为它的周期
  }
  int K;
  scanf("%d" , &K);
  while (K--) {
    Item r = pq.top(); // 取下一个事件
    pq.pop();
    printf("%d\n" , r.QNum);
    r.Time += r.Period; // 更新该触发器的“下一个事件”的时间
    pq.push(r); // 重新插入优先队列
  }
  return 0;
}
// Accepted 32ms 552kB 819 G++2020-12-1316:59:02 22207509
```

### 例题5  易爆物（X-Plosives, UVa1160）

```cpp
// 例题5  易爆物（X-Plosives, UVa1160）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
typedef long long LL;
const int MAXN = 100000 + 4;
int Pa[MAXN];

int findPa(int u) {
  return Pa[u] == u ? u : (Pa[u] = findPa(Pa[u]));
}

int main() {
  int u, v;
  while (true) {
    _rep(i, 0, MAXN) Pa[i] = i;
    int ans = 0;
    while (true) {
      if (scanf("%d", &u) != 1) return 0;
      if (u == -1) break;
      scanf("%d", &v);
      int pu = findPa(u), pv = findPa(v);
      if (pu == pv)
        ans++;
      else
        Pa[pu] = v;
    }
    printf("%d\n", ans);
  }
  return 0;
}
// Accepted 751 C++5.3.0 2020-12-1319:42:07 25843348
```

### 例题2  一道简单题（Easy Problem from Rujia Liu?, UVa 11991）

```cpp
// 例题2  一道简单题（Easy Problem from Rujia Liu?, UVa 11991）
// Rujia Liu
#include<cstdio>
#include<vector>
#include<map>
using namespace std;

map<int, vector<int> > a; // 最后两个>不要连写，否则会被误认为>>

int main() {
  int n, m, x, y;
  while(scanf("%d%d", &n, &m) == 2) {
    a.clear();
    for(int i = 0; i < n; i++) {
      scanf("%d", &x); if(!a.count(x)) a[x] = vector<int>();
      a[x].push_back(i+1);
    }
    while(m--) {
      scanf("%d%d", &x, &y);
      if(!a.count(y) || a[y].size() < x) printf("0\n");
      else printf("%d\n", a[y][x-1]);
    }
  }
  return 0;
}
// 25877211  11991  Easy Problem from Rujia Liu?  Accepted  C++  0.040  2020-12-23 03:44:34
```

### 例题1  猜猜数据结构（I Can Guess the Data Structure!, UVa 11995）

```cpp
// 例题1  猜猜数据结构（I Can Guess the Data Structure!, UVa 11995）
// Rujia Liu
#include<cstdio>
#include<queue>
#include<stack>
#include<cstdlib>
using namespace std;

const int maxn = 1000 + 10;
int n, t[maxn], v[maxn];

int check_stack() {
  stack<int> s;
  for(int i = 0; i < n; i++) {
    if(t[i] == 2) {
      if(s.empty()) return 0;
      int x = s.top(); s.pop();
      if(x != v[i]) return 0;
    }
    else s.push(v[i]);
  }
  return 1;
}

int check_queue() {
  queue<int> s;
  for(int i = 0; i < n; i++) {
    if(t[i] == 2) {
      if(s.empty()) return 0;
      int x = s.front(); s.pop();
      if(x != v[i]) return 0;
    }
    else s.push(v[i]);
  }
  return 1;
}

int check_pq() {
  priority_queue<int> s;
  for(int i = 0; i < n; i++) {
    if(t[i] == 2) {
      if(s.empty()) return 0;
      int x = s.top(); s.pop();
      if(x != v[i]) return 0;
    }
    else s.push(v[i]);
  }
  return 1;
}

int main() {
  while(scanf("%d", &n) == 1) {
    for(int i = 0; i < n; i++) scanf("%d%d", &t[i], &v[i]);
    int s = check_stack();
    int q = check_queue();
    int pq = check_pq();
    if(!s && !q && !pq) printf("impossible\n");
    else if(s && !q && !pq) printf("stack\n");
    else if(!s && q && !pq) printf("queue\n");
    else if(!s && !q && pq) printf("priority queue\n");
    else printf("not sure\n");
  }
  return 0;
}
// 25877209  11995  I Can Guess the Data Structure!  Accepted  C++  0.010  2020-12-23 03:44:22
```

### 例题4  K个最小和（K Smallest Sums, UVa 11997）

```cpp
// 例题4  K个最小和（K Smallest Sums, UVa 11997）
// http://codeforces.com/gym/100048 C
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
const int MAXK = 768, INF = 1e6 + 4;
int K, A[MAXK], B[MAXK];
struct Item {
  int sum, b;  // A[a] + B[b], b
  Item(int _sum, int _b) : sum(_sum), b(_b) {}
  bool operator<(const Item& i) const { return sum > i.sum; };
};

void merge() {  // AxB -> A
  priority_queue<Item> Q;
  _for(i, 0, K) Q.push(Item(A[i] + B[0], 0));
  _for(i, 0, K) {
    Item it = Q.top();
    Q.pop(), A[i] = it.sum;
    if (it.b < K - 1)
      Q.emplace(Item(it.sum + B[it.b + 1] - B[it.b], it.b + 1));
  }
}

void read_array(int *p) {
  _for(i, 0, K) scanf("%d", &(p[i]));
  sort(p, p + K);
}

int main() {
  while (scanf("%d", &K) == 1) {
    read_array(A);
    _for(i, 1, K) read_array(B), merge();
    _for(i, 0, K) printf("%d%c", A[i], i < K - 1 ? ' ' : '\n');
  }
  return 0;
}
// 18787064 11997 K Smallest Sums Accepted  C++11 0.110 2017-02-16 08:15:10
```

## 3.2 区间信息的维护与查询

### 例题7  乒乓比赛（Ping pong, Beijing 2008, LA4329）

```cpp
// 例题7  乒乓比赛（Ping pong, Beijing 2008, LA4329）
// 陈锋
#include <cassert>
#include <iostream>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
typedef long long LL;

template <typename T, size_t SZ>
struct BIT {  // Binary Indexed Tree
  T C[SZ];
  size_t N;
  inline void init(size_t sz) {
    N = sz;
    assert(N + 1 < SZ);
    fill_n(C, N + 1, 0);
  }
  inline int lowbit(int x) { return x & -x; }
  inline T sum(size_t i) {  // Σ(k = 1→i)
    T ans = 0;
    while (i > 0) ans += C[i], i -= lowbit(i);
    return ans;
  }
  inline void add(size_t i, const T& v) {
    while (i <= N) C[i] += v, i += lowbit(i);
  }
};

const int MAXN = 20000 + 4, MAXA = 1e5;
int A[MAXN], C[MAXN], D[MAXN];
/*
  i当裁判，考虑a[1~i-1]中有ci个比ai小，(i-1)-ci个比ai大,
  a[i+1~n]有di个比ai小，(n-i-di)个比ai大
  则i当裁判就有ci(n-i-di)+(i-1-ci)di种比赛，求Σ即可
  ci, di扫描求得，X[a] = 1 -> exist Ai = a before
*/
int main() {
  int T, N;
  ios::sync_with_stdio(false), cin.tie(0);
  cin >> T;
  BIT<int, MAXA + 4> X;
  while (T--) {
    cin >> N, fill_n(C, N + 1, 0);
    X.init(MAXA);
    _rep(i, 1, N) cin >> A[i], C[i] = X.sum(A[i] - 1), X.add(A[i], 1);
    X.init(MAXA);
    LL ans = 0;
    for (int i = N; i >= 1; i--) {
      int d = X.sum(A[i] - 1);
      X.add(A[i], 1);
      if (i < N && i > 1) ans += C[i] * (N - i - d) + (i - 1 - C[i]) * d;
    }
    cout << ans << endl;
  }
  return 0;
}
// Accepted 719ms 1184kB 1504 G++2020-12-13 20:47:28 22208011
```

### 例题11  山脉（Mountains, IOI05, SPOJ NKMOU）

```cpp
// 例题11  山脉（Mountains, IOI05, SPOJ NKMOU）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;
struct Node {
  LL sum, maxp; // 区间和，最大非负前缀
  Node *left, *right;
  int val;
  inline bool isleaf() { return !left && !right; }
  inline void init() { memset(this, 0, sizeof(Node));}
  inline void delchildren() {
    if (left) delete left;
    if (right) delete right;
    left = right = nullptr;
  }
  ~Node() { delchildren(); } // C++析构函数，delete的时候会调用
};
typedef Node* PN;
int N;
PN root;
void maintain(Node& p) {
  p.sum = p.left->sum + p.right->sum;
  p.maxp = max(p.left->maxp, p.left->sum + p.right->maxp);
}
void setval(Node& p, int v, int L, int R) {
  assert(L <= R); // 整个区间设置值
  p.sum = (LL)(p.val = v) * (R - L + 1);
  p.maxp = max(0LL, p.sum);
  p.delchildren(); // 左右孩子都可以不要了
}
void pushdown(Node& p, int L, int R) {
  int M = (L + R) / 2;
  p.left = new Node(), p.right = new Node();
  setval(*(p.left), p.val, L, M), setval(*(p.right), p.val, M + 1, R);
}
void modify(int l, int r, int v, Node& p = *root, int nL = 1, int nR = N) {
  int M = (nL + nR) / 2;
  if (l <= nL && nR <= r) {
    setval(p, v, nL, nR);
    return;
  }
  if (p.isleaf()) pushdown(p, nL, nR); // 左右区间创建子节点
  if (l <= M) modify(l, r, v, *(p.left), nL, M); // 递归
  if (r > M) modify(l, r, v, *(p.right), M + 1, nR); // 递归
  maintain(p); // 维护sum以及maxp
}
// 查询数组中前缀和<=h的最长前缀的右端点位置
int query(LL h, Node& p = *root, int L = 1, int R = N) {
  if (h >= p.maxp) return R; // 整个区间都行
  if (p.isleaf()) return L + (h / p.val) - 1; // 区间元素都相等，按比例返回
  int M = (L + R) / 2;
  Node& pl = *(p.left);
  return h >= pl.maxp ? query(h - pl.sum, *(p.right), M + 1, R) // 左边的最大非负前缀<=h，一定能跑到右边
         : query(h, pl, L, M); // 只能在左子区间内部
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
  root = new Node();
  for (int a, b, d, h; cin >> s && s[0] != 'E'; ) {
    if (s[0] == 'I') cin >> a >> b >> d, modify(a, b, d);
    else cin >> h, cout << query(h) << endl;
  }
  delete root;
  return 0;
}
// 25407608 2020-02-16 07:12:57 Feng Chen IOI05 Mountains 100 2.62 169M CPP14
```

### 例题8  频繁出现的数值（Frequent Values, UVa 11235）

```cpp
// 例题8  频繁出现的数值（Frequent Values, UVa 11235）
// Rujia Liu
#include<cstdio>
#include<algorithm>
#include<vector>
using namespace std;

const int maxn = 100000 + 5;
const int maxlog = 20;

// 区间最*大*值
struct RMQ {
  int d[maxn][maxlog];
  void init(const vector<int>& A) {
    int n = A.size();
    for(int i = 0; i < n; i++) d[i][0] = A[i];
    for(int j = 1; (1<<j) <= n; j++)
      for(int i = 0; i + (1<<j) - 1 < n; i++)
        d[i][j] = max(d[i][j-1], d[i + (1<<(j-1))][j-1]);
  }

  int query(int L, int R) {
    int k = 0;
    while((1<<(k+1)) <= R-L+1) k++; // 如果2^(k+1)<=R-L+1，那么k还可以加1
    return max(d[L][k], d[R-(1<<k)+1][k]);
  }
};

int a[maxn], num[maxn], left[maxn], right[maxn];
RMQ rmq;
int main() {
  int n, q;
  while(scanf("%d%d", &n, &q) == 2) {
    for(int i = 0; i < n; i++) scanf("%d", &a[i]);
    a[n] = a[n-1] + 1; // 哨兵
    int start = -1;
    vector<int> count;
    for(int i = 0; i <= n; i++) {
      if(i == 0 || a[i] > a[i-1]) { // 新段开始
        if(i > 0) {
          count.push_back(i - start);
          for(int j = start; j < i; j++) {
            num[j] = count.size() - 1; left[j] = start; right[j] = i-1;
          }
        }
        start = i;
      }
    }
    rmq.init(count);
    while(q--) {
      int L, R, ans;
      scanf("%d%d", &L, &R); L--; R--;
      if(num[L] == num[R]) ans = R-L+1;
      else {
        ans = max(R-left[R]+1, right[L]-L+1);
        if(num[L]+1 < num[R]) ans = max(ans, rmq.query(num[L]+1, num[R]-1));
      }
      printf("%d\n", ans);
    }
  }
  return 0;
}
// 25877221  11235  Frequent values  Accepted  C++  0.090  2020-12-23 03:51:01
```

### 例题10  快速矩阵操作（Fast Matrix Operations, UVa 11992）

```cpp
// 例题10  快速矩阵操作（Fast Matrix Operations, UVa 11992）
// 陈锋
#include <bits/stdc++.h>

using namespace std;

const int MAXC = 1e6 + 4, INF = 1e9;
struct NodeInfo {
  int minv, maxv, sumv;
};
NodeInfo operator+(const NodeInfo &n1, const NodeInfo &n2) {
  return {min(n1.minv, n2.minv), max(n1.maxv, n2.maxv), n1.sumv + n2.sumv};
}

struct IntervalTree {
  NodeInfo nodes[MAXC];
  int setv[MAXC], addv[MAXC], qL, qR;
  bitset<MAXC> isSet;
  inline void setFlag(int o, int v) { setv[o] = v, isSet.set(o), addv[o] = 0; }
  void init(int n) {
    int sz = n * 2 + 2;
    fill_n(addv, sz, 0);
    isSet.reset(), isSet.set(1);
    memset(nodes, 0, sizeof(NodeInfo) * sz);
  }

  inline void maintain(int o, int L, int R) {  // 维护信息
    int lc = o * 2, rc = o * 2 + 1, a = addv[o], s = setv[o];
    NodeInfo &nd = nodes[o], &li = nodes[lc], &ri = nodes[rc];
    if (R > L) nd = li + ri;
    if (isSet[o]) nd = {s, s, s * (R - L + 1)};
    if (a) nd.minv += a, nd.maxv += a, nd.sumv += a * (R - L + 1);
  }

  inline void pushdown(int o) {  // 标记传递
    int lc = o * 2, rc = o * 2 + 1;
    if (isSet[o])
      setFlag(lc, setv[o]), setFlag(rc, setv[o]), isSet.reset(o); // 清除标记
    if (addv[o])
      addv[lc] += addv[o], addv[rc] += addv[o], addv[o] = 0; // 清除标记
  }

  void update(int o, int L, int R, int op, int v) {  // op(1:add, 2:set)
    int lc = o * 2, rc = o * 2 + 1, M = L + (R - L) / 2;
    if (qL <= L && qR >= R) {  // 标记修改
      if (op == 1) addv[o] += v;  // add
      else setFlag(o, v);  // set
    } else {
      pushdown(o);
      if (qL <= M) update(lc, L, M, op, v);
      else maintain(lc, L, M);
      if (qR > M) update(rc, M + 1, R, op, v);
      else maintain(rc, M + 1, R);
    }
    maintain(o, L, R);
  }

  NodeInfo query(int o, int L, int R) {
    int lc = o * 2, rc = o * 2 + 1, M = L + (R - L) / 2;
    maintain(o, L, R);
    if (qL <= L && qR >= R) return nodes[o];

    pushdown(o);
    NodeInfo li = {INF, -INF, 0}, ri = {INF, -INF, 0};
    if (qL <= M) li = query(lc, L, M);
    else maintain(lc, L, M);
    if (qR > M) ri = query(rc, M + 1, R);
    else maintain(rc, M + 1, R);
    return li + ri;
  }
};

const int maxr = 20 + 5;
IntervalTree tree[maxr];
int main() {
  for (int r, c, m; scanf("%d%d%d", &r, &c, &m) == 3;) {
    for (int x = 1; x <= r; x++) tree[x].init(c);
    for (int i = 0, op, x1, y1, x2, y2, v; i < m; i++) {
      scanf("%d%d%d%d%d", &op, &x1, &y1, &x2, &y2);
      if (op < 3) {
        scanf("%d", &v);
        for (int x = x1; x <= x2; x++) {
          IntervalTree &tx = tree[x];
          tx.qL = y1, tx.qR = y2, tx.update(1, 1, c, op, v);
        }
      } else {
        NodeInfo gi = {INF, -INF, 0};
        for (int x = x1; x <= x2; x++) {
          IntervalTree &tx = tree[x];
          tx.qL = y1, tx.qR = y2, gi = gi + tx.query(1, 1, c);
        }
        printf("%d %d %d\n", gi.sumv, gi.minv, gi.maxv);
      }
    }
  }
  return 0;
}
// Accepted 550ms 2968 C++5.3.02020-12-1321:05:39 25843628
```

### 例题12  堆内存管理器（Heap Manager, UVa12419）

```cpp
// 例题12  堆内存管理器（Heap Manager, UVa12419）
// 陈锋
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)
typedef long long LL;
const LL INF = 1ll << 60;
struct IntTreeNode {
  IntTreeNode *lc, *rc;
  int setv, lz, rz, mz; // 懒标记, [0~0***], [**0~0], [**0~0**]
  IntTreeNode() : lc(nullptr), rc(nullptr) { }
  inline void delchildren() {
    if (lc) delete lc;
    if (rc) delete rc;
    lc = rc = nullptr;
  }
  ~IntTreeNode() { delchildren(); } // C++析构函数，delete的时候会调用
  void mark(int l, int r, int v) {
    lz = rz = mz = (v == 0 ? r - l + 1 : 0);
    setv = v, delchildren();
  }

  void mark(IntTreeNode* &p, int l, int r, int v) {
    if (!p) p = new IntTreeNode();
    p->mark(l, r, v);
  }

  void pushdown(int l, int r) {  // 标记pushdown
    int m = l + (r - l) / 2;
    if (setv == -1) return;
    mark(lc, l, m, setv), mark(rc, m + 1, r, setv);
    setv = -1;
  }

  void set(int l, int r, int ql, int qr, int v) { // set [ql,qr] = v o->[l,r]
    if (ql <= l && r <= qr) {
      mark(l, r, v);
      return;
    }
    pushdown(l, r);
    int m = l + (r - l) / 2;
    IntTreeNode &ld = *(lc), &rd = *(rc);
    if (ql <= m) ld.set(l, m, ql, qr, v);
    if (qr > m) rd.set(m + 1, r, ql, qr, v);
    lz = (ld.lz == m - l + 1) ? ld.lz + rd.lz : ld.lz;
    rz = (rd.rz == r - m) ? rd.rz + ld.rz : rd.rz;
    mz = max(max(ld.mz, rd.mz), ld.rz + rd.lz);
  }
  int query(int l, int r, int len) { // 查询 o→[l,r]区间内最左边的>=len全0区间位置
    if (lz >= len) return l;  // [0~0***]
    pushdown(l, r);
    IntTreeNode &ld = *lc, &rd = *rc;
    int m = l + (r - l) / 2;
    if (ld.mz >= len) return ld.query(l, m, len);     // [**0~0**][**]
    if (ld.rz + rd.lz >= len) return m - ld.rz + 1;  // [**0~0][0~0**]
    return rd.query(m + 1, r, len);                    // [***][?]
  }
};
struct Event {  // release time, memory address [l,r]
  LL t;
  int l, r;
  bool operator<(const Event& a) const { return t > a.t; }
};
struct Process { int len, t, id; };  // slice len, use time, id
priority_queue<Event> EQ;
queue<Process> Q;
IntTreeNode A;
void allocate(int N, int b, LL cur, const Process& p) {  // 在cur时给p分配内存
  int l = A.query(0, N - 1, p.len);
  A.set(0, N - 1, l, l + p.len - 1, 1);
  EQ.push(Event{cur + p.t, l, l + p.len - 1});
  if (b) printf("%lld %d %d\n", cur, p.id, l);
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int N, b, pcnt, m, p;
  for (LL t, ans = 0; cin >> N >> b;) {
    pcnt = 0, A.mark(0, N - 1, 0);
    for (int i = 1;; i++) {
      cin >> t >> m >> p; // time, mem slice len, time length
      if (t == 0 && m == 0 && p == 0) t = INF;
      while (!EQ.empty() && EQ.top().t <= t) {
        LL cur = EQ.top().t;  // 有释放内存的请求需要在t之前处理
        while (!EQ.empty() && EQ.top().t == cur) {  // 释放最近需要释放的内存
          const auto& e = EQ.top();
          ans = e.t;
          A.set(0, N - 1, e.l, e.r, 0), EQ.pop();
        }
        while (!Q.empty() && Q.front().len <= A.mz)
          allocate(N, b, cur, Q.front()), Q.pop();  // 需要分配内存的进程，分配内存
      }
      if (t == INF) break;
      if (A.mz >= m) allocate(N, b, t, Process{m, p, i}); // 现在就可以分配内存
      else Q.push(Process{m, p, i}), pcnt++;  // 排队
    }
    printf("%lld\n%d\n\n", ans, pcnt);  // 处理完所有进程，入过Q的进程
  }
  return 0;
}
// 24887303  12419   Heap Manager  Accepted  C++11   0.610   2020-04-17 02:50:01
```

### 例题9  动态最大连续和（Ray, Pass me the Dishes, UVa1400）

```cpp
// 例题9  动态最大连续和（Ray, Pass me the Dishes, UVa1400）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
typedef long long LL;
typedef pair<int, int> Interval;
const int MAXN = 5e5 + 4;
LL SD[MAXN];
inline LL sum(int L, int R) { // [L,R]
  // assert(L <= R);
  return SD[R] - SD[L - 1];
}
inline LL sum(const Interval& i) { return sum(i.first, i.second); }
inline Interval maxI(const Interval& i1, const Interval& i2) {
  LL s1 = sum(i1), s2 = sum(i2);
  if (s1 != s2) return s1 > s2 ? i1 : i2;
  return min(i1, i2);
}
struct MaxVal {
  int pfx, sfx;
  Interval sub;
};

struct IntervalTree {
  MaxVal Nodes[MAXN * 2];
  int qL, qR, N;
  void build(int N) { // [1, N]
    this->N = N;
    build(1, N, 1);
  }

  void build(int L, int R, int O) {
    assert(L <= R);
    assert(O > 0);
    if (L == R) {
      Nodes[O] = {L, L, make_pair(L, L)};
      return;
    }
    int M = (L + R) / 2, lc = 2 * O, rc = 2 * O + 1;
    build(L, M, lc), build(M + 1, R, rc);
    const MaxVal &nl = Nodes[lc], &nr = Nodes[rc];
    MaxVal &no = Nodes[O];
    no.pfx = sum(L, nl.pfx) >= sum(L, nr.pfx) ? nl.pfx : nr.pfx;
    no.sfx = sum(nl.sfx, R) >= sum(nr.sfx, R) ? nl.sfx : nr.sfx;
    no.sub = maxI(nl.sub, nr.sub);
    no.sub = maxI(no.sub, make_pair(nl.sfx, nr.pfx));
  }

  Interval query(int l, int r) { // max sub [a,b] in [l, r]
    assert(l <= r);
    qL = l, qR = r;
    return _query(1, N, 1);
  }

  Interval _query(const int L, const int R, const int O) {
    if (qL <= L && R <= qR) return Nodes[O].sub;
    int M = (L + R) / 2, lc = O * 2, rc = 2 * O + 1;
    if (qR <= M) return _query(L, M, lc);
    if (qL > M) return _query(M + 1, R, rc);
    Interval ans = make_pair(_querySfx(L, M, lc), _queryPfx(M + 1, R, rc));
    ans = maxI(ans, maxI(_query(L, M, lc), _query(M + 1, R, rc)));
    return ans;
  }

  int _queryPfx(const int L, const int R, const int O) {
    if (qL <= L && R <= qR) return Nodes[O].pfx;
    int M = (L + R) / 2, lc = 2 * O, rc = 2 * O + 1;
    if (qR <= M) return _queryPfx(L, M, lc);
    if (qL > M) return _queryPfx(M + 1, R, rc);
    int m1 = _queryPfx(L, M, lc), m2 = _queryPfx(M + 1, R, rc);
    return sum(L, m1) >= sum(L, m2) ? m1 : m2;
  }

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
    _rep(i, 1, N) cin >> d, SD[i] = SD[i - 1] + d;
    tree.build(N);
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

## 3.3 字符串（1）

### 例题15  周期（Period, SEERC 2004, Codeforces Gym101461A）

```cpp
// 例题15  周期（Period, SEERC 2004, Codeforces Gym101461A）
// 陈锋
#include <cstdio>
const int NN = 1e6 + 4;
char P[NN];
int F[NN];

int main() {
  freopen("period.in", "r", stdin);
  freopen("period.out", "w", stdout);

  for (int n, kase = 1; scanf("%d", &n) == 1 && n; kase++) {
    scanf("%s", P);
    F[0] = 0, F[1] = 0;  // 递推边界初值
    for (int i = 1; i < n; i++) {
      int j = F[i];
      while (j && P[i] != P[j]) j = F[j];
      F[i + 1] = (P[i] == P[j] ? j + 1 : 0);
    }

    printf("Test case #%d\n", kase);
    for (int i = 2; i <= n; i++)
      if (F[i] > 0 && i % (i - F[i]) == 0) printf("%d %d\n", i, i / (i - F[i]));
    printf("\n");
  }
  return 0;
}
// 102087071  Dec/23/2020 12:10UTC+8  chenwz  A - Period  GNU C++11  Accepted  46 ms  4800 KB
```

### UVa11019 Matrix Matcher

```cpp
// UVa11019 Matrix Matcher
// Rujia Liu
#include<cstring>
#include<queue>
#include<cstdio>
#include<map>
#include<string>
using namespace std;

const int SIGMA_SIZE = 26;
const int MAXNODE = 10000 + 10;

void process_match(int pos, int v); // AC自动机每找到一个匹配会调用一次，结束位置为pos，val为v

struct AhoCorasickAutomata {
  int ch[MAXNODE][SIGMA_SIZE];
  int f[MAXNODE];    // fail函数
  int val[MAXNODE];  // 每个字符串的结尾结点都有一个非0的val
  int last[MAXNODE]; // 输出链表的下一个结点
  int sz;

  void init() {
    sz = 1;
    memset(ch[0], 0, sizeof(ch[0]));
  }

  // 字符c的编号
  int idx(char c) {
    return c-'a';
  }

  // 插入字符串。v必须非0
  void insert(char *s, int v) {
    int u = 0, n = strlen(s);
    for(int i = 0; i < n; i++) {
      int c = idx(s[i]);
      if(!ch[u][c]) {
        memset(ch[sz], 0, sizeof(ch[sz]));
        val[sz] = 0;
        ch[u][c] = sz++;
      }
      u = ch[u][c];
    }
    val[u] = v;
  }

  // 递归打印以结点j结尾的所有字符串
  void report(int pos, int j) {
    if(j) {
      process_match(pos, val[j]);
      report(pos, last[j]);
    }
  }

  // 在T中找模板
  int find(char* T) {
    int n = strlen(T);
    int j = 0; // 当前结点编号，初始为根结点
    for(int i = 0; i < n; i++) { // 文本串当前指针
      int c = idx(T[i]);
      while(j && !ch[j][c]) j = f[j]; // 顺着细边走，直到可以匹配
      j = ch[j][c];
      if(val[j]) report(i, j);
      else if(last[j]) report(i, last[j]); // 找到了！
    }
  }

  // 计算fail函数
  void getFail() {
    queue<int> q;
    f[0] = 0;
    // 初始化队列
    for(int c = 0; c < SIGMA_SIZE; c++) {
      int u = ch[0][c];
      if(u) { f[u] = 0; q.push(u); last[u] = 0; }
    }
    // 按BFS顺序计算fail
    while(!q.empty()) {
      int r = q.front(); q.pop();
      for(int c = 0; c < SIGMA_SIZE; c++) {
        int u = ch[r][c];
        if(!u) continue;
        q.push(u);
        int v = f[r];
        while(v && !ch[v][c]) v = f[v];
        f[u] = ch[v][c];
        last[u] = val[f[u]] ? f[u] : last[f[u]];
      }
    }
  }

};

AhoCorasickAutomata ac;

const int maxn = 1000 + 10;
const int maxm = 1000 + 10;
const int maxx = 100 + 10;
const int maxy = 100 + 10;
char text[maxn][maxm], P[maxx][maxy];

int repr[maxx]; // repr[i]为模板第i行的“代表元”
int next[maxx]; // next[i]为模板中与第i行相等的下一个行编号
int len[maxx]; // 模板各行的长度

int tr; // 当前文本行编号
int cnt[maxn][maxm];
void process_match(int pos, int v) {
  int pr = repr[v - 1]; // 匹配到得模板行编号
  int c = pos - len[pr] + 1;
  while(pr >= 0) {
    if(tr >= pr) // P的行pr出现在在T的tr行，起始列编号为c
      cnt[tr - pr][c]++;
    pr = next[pr];
  }
}

int main() {
  int T, n, m, x, y;
  scanf("%d", &T);
  while(T--) {
    scanf("%d%d", &n, &m);
    for(int i = 0; i < n; i++)
      scanf("%s", text[i]);

    scanf("%d%d", &x, &y);
    ac.init();
    for(int i = 0; i < x; i++) {
      scanf("%s", P[i]);
      len[i] = strlen(P[i]);
      repr[i] = i;
      next[i] = -1;
      for(int j = 0; j < i; j++)
        if(strcmp(P[i], P[j]) == 0) {
          repr[i] = j;
          next[i] = next[j];
          next[j] = i;
          break;
        }
      if(repr[i] == i) ac.insert(P[i], i+1);
    }
    ac.getFail();

    memset(cnt, 0, sizeof(cnt));
    for(tr = 0; tr < n; tr++)
      ac.find(text[tr]);

    int ans = 0;
    for(int i = 0; i < n-x+1; i++)
      for(int j = 0; j < m-y+1; j++)
        if(cnt[i][j] == x) ans++;
    printf("%d\n", ans);
  }
  return 0;
}
```

### UVa11468 Substring

```cpp
// UVa11468 Substring
// 陈锋
#include <bits/stdc++.h>
using namespace std;

const int SIGMA_SIZE = 64;
const int MAXNODE = 500;   // 结点总数
const int MAXS = 20 + 10;  // 模板个数

int idx[256], n;
double prob[SIGMA_SIZE];

struct AhoCorasickAutomata {
  int ch[MAXNODE][SIGMA_SIZE];
  int f[MAXNODE];      // fail函数
  int match[MAXNODE];  // 是否包含某一个字符串
  int sz;              // 结点总数

  void init() {
    sz = 1;
    memset(ch[0], 0, sizeof(ch[0]));
  }

  void insert(const char *s) {  // 插入字符串
    int u = 0, n = strlen(s);
    for (int i = 0; i < n; i++) {
      int c = idx[s[i]];
      if (!ch[u][c]) {
        memset(ch[sz], 0, sizeof(ch[sz]));
        match[sz] = 0;
        ch[u][c] = sz++;
      }
      u = ch[u][c];
    }
    match[u] = 1;
  }

  void getFail() {  // 计算fail函数
    queue<int> q;
    f[0] = 0;
    for (int c = 0; c < SIGMA_SIZE; c++) {  // 初始化队列
      int u = ch[0][c];
      if (u) {
        f[u] = 0;
        q.push(u);
      }
    }
    while (!q.empty()) {  // 按BFS顺序计算fail
      int r = q.front();
      q.pop();
      for (int c = 0; c < SIGMA_SIZE; c++) {
        int u = ch[r][c];
        if (!u) {
          ch[r][c] = ch[f[r]][c];
          continue;
        }
        q.push(u);
        int v = f[r];
        while (v && !ch[v][c]) v = f[v];
        f[u] = ch[v][c];
        match[u] |= match[f[u]];
      }
    }
  }

  void dump() {
    printf("sz = %d\n", sz);
    for (int i = 0; i < sz; i++)
      printf("%d: %d %d %d\n", i, ch[i][0], ch[i][1], match[i]);
    printf("\n");
  }
};

AhoCorasickAutomata ac;

double d[MAXNODE][105];
int vis[MAXNODE][105];
double getProb(int u, int L) {
  if (!L) return 1.0;
  if (vis[u][L]) return d[u][L];
  vis[u][L] = 1;
  double &ans = d[u][L];
  ans = 0.0;
  for (int i = 0; i < n; i++)
    if (!ac.match[ac.ch[u][i]]) ans += prob[i] * getProb(ac.ch[u][i], L - 1);
  return ans;
}

char s[30][30];

int main() {
  int T;
  scanf("%d", &T);
  for (int kase = 1, k, L; kase <= T; kase++) {
    scanf("%d", &k);
    for (int i = 0; i < k; i++) scanf("%s", s[i]);
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
      char ch[9];
      scanf("%s%lf", ch, &prob[i]), idx[ch[0]] = i;
    }
    ac.init();
    for (int i = 0; i < k; i++) ac.insert(s[i]);
    ac.getFail();
    scanf("%d", &L);
    memset(vis, 0, sizeof(vis));
    printf("Case #%d: %.6lf\n", kase, getProb(0, L));
  }
  return 0;
}
// Accepted 310ms 2374 C++ 5.3.0 2020-12-14 11:44:03 25845650
```

### 例题14 strcmp()函数（“strcmp()” Anyone?, UVa11732）

```cpp
// 例题14 strcmp()函数（“strcmp()” Anyone?, UVa11732）
// 詹益瑞,陈锋
#include<bits/stdc++.h>
using namespace std;
typedef long long LL;
const int SZ = 4e6 + 5, SIGMA = 70;
struct Trie {
  int ch[SZ][SIGMA], cnt[SZ], val[SZ], sz = 0;
  int idx(char c) {
    if (isdigit(c)) return c - '0';
    if (c >= 'A' && c <= 'Z') return c - 'A' + 10;
    return c - 'a' + 38;
  }
  int newNode() {
    fill_n(ch[sz], SIGMA, 0), cnt[sz] = 0, val[sz] = 0;
    return sz++;
  }
  void insert(const char* s) {
    int len = strlen(s), u = 0;
    for (int i = 0; i < len; ++i) {
      int c = idx(s[i]), &uc = ch[u][c];
      if (!uc) uc = newNode();
      u = uc, cnt[u]++;
    }
    val[u]++; // 单词结束点
  }
  LL query(const char* s) {
    LL x = 0;
    int len = strlen(s), u = 0;
    for (int i = 0; i < len; ++i) {
      int c = idx(s[i]);
      if (!ch[u][c]) return x;
      // 不等的2个串的相同部分每个字符比较2次，最后一位不同的还有一次
      u = ch[u][c], x += cnt[u] * 2;
    }
    return x + val[u];
  }
  void init() { sz = 0, newNode(); }
};


Trie trie;
char s[1004];
int main() {
  for (int n, kase = 1; scanf("%d", &n) && n; kase++) {
    trie.init();
    LL ans = 0;
    for (int i = 1; i <= n; ++i)
      scanf("%s", s), ans += trie.query(s), trie.insert(s);
    ans += n * (n - 1) / 2; // 最后再补上每两个串的结尾比较一次
    printf("Case %d: %lld\n", kase, ans);
  }
  return 0;
}
// 26047697 11732 "strcmp()" Anyone?  Accepted  C++ 0.810 2021-02-02 06:31:12
```

### 例题13  背单词（Remember the Word, UVa1401）

```cpp
// 例题13  背单词（Remember the Word, UVa1401）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int maxnode = 4000 * 100 + 10, sigma_size = 26;

// 字母表为全体小写字母的Trie
struct Trie {
  int ch[maxnode][sigma_size];
  int val[maxnode];
  int sz; // 结点总数
  void clear() { sz = 1; memset(ch[0], 0, sizeof(ch[0])); } // 初始时只有一个根结点
  int idx(char c) { return c - 'a'; } // 字符c的编号

  // 插入字符串s，附加信息为v。注意v必须非0，因为0代表“本结点不是单词结点”
  void insert(const char *s, int v) {
    int u = 0, n = strlen(s);
    for (int i = 0; i < n; i++) {
      int c = idx(s[i]);
      if (!ch[u][c]) { // 结点不存在
        memset(ch[sz], 0, sizeof(ch[sz]));
        val[sz] = 0;  // 中间结点的附加信息为0
        ch[u][c] = sz++; // 新建结点
      }
      u = ch[u][c]; // 往下走
    }
    val[u] = v; // 字符串的最后一个字符的附加信息为v
  }

  // 找字符串s的长度不超过len的前缀
  void find_prefixes(const char *s, int len, vector<int>& ans) {
    int u = 0;
    for (int i = 0; i < len; i++) {
      if (s[i] == '\0') break;
      int c = idx(s[i]);
      if (!ch[u][c]) break;
      u = ch[u][c];
      if (val[u] != 0) ans.push_back(val[u]); // 找到一个前缀
    }
  }
};

// 文本串最大长度, 单词最大个数
const int TL = 3e5 + 4, WC = 4000 + 4, MOD = 20071027;
int D[TL], WLen[WC];
Trie trie;
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  string text, word;
  for (int kase = 1, S; cin >> text >> S; kase++) {
    trie.clear();
    for (int i = 1; i <= S; i++)
      cin >> word, WLen[i] = word.length(), trie.insert(word.c_str(), i);
    int L = text.length();
    fill_n(D, L, 0), D[L] = 1;
    for (int i = L - 1; i >= 0; i--) {
      vector<int> p;
      trie.find_prefixes(text.c_str() + i, L - i, p);
      for (size_t j = 0; j < p.size(); j++)
        D[i] = (D[i] + D[i + WLen[p[j]]]) % MOD;
    }
    printf("Case %d: %d\n", kase, D[0]);
  }
  return 0;
}
// Accepted 80ms 1784 C++ 5.3.0 2020-12-1411:33:14 25845627
```

### UVa1449 Dominating Patterns

```cpp
// UVa1449 Dominating Patterns
// 刘汝佳
#include <bits/stdc++.h>
using namespace std;

const int SIGMA_SIZE = 26, MAXNODE = 11000, MAXS = 150 + 10;
map<string, int> ms;
struct AhoCorasickAutomata {
  int ch[MAXNODE][SIGMA_SIZE];
  int f[MAXNODE];     // fail函数
  int val[MAXNODE];   // 每个字符串的结尾结点都有一个非0的val
  int last[MAXNODE];  // 输出链表的下一个结点
  int cnt[MAXS];
  int sz;

  void init() {
    sz = 1;
    memset(ch[0], 0, sizeof(ch[0]));
    memset(cnt, 0, sizeof(cnt));
    ms.clear();
  }

  // 字符c的编号
  int idx(char c) { return c - 'a'; }

  // 插入字符串。v必须非0
  void insert(char* s, int v) {
    int u = 0, n = strlen(s);
    for (int i = 0; i < n; i++) {
      int c = idx(s[i]);
      if (!ch[u][c]) {
        memset(ch[sz], 0, sizeof(ch[sz]));
        val[sz] = 0, ch[u][c] = sz++;
      }
      u = ch[u][c];
    }
    val[u] = v, ms[string(s)] = v;
  }

  // 递归打印以结点j结尾的所有字符串
  void print(int j) {
    if (j) cnt[val[j]]++, print(last[j]);
  }

  // 在T中找模板
  void find(char* T) {
    int n = strlen(T), j = 0;      // 当前结点编号，初始为根结点
    for (int i = 0; i < n; i++) {  // 文本串当前指针
      int c = idx(T[i]);
      while (j && !ch[j][c]) j = f[j];  // 顺着细边走，直到可以匹配
      j = ch[j][c];
      if (val[j]) print(j);
      else if (last[j]) print(last[j]);  // 找到了！
    }
  }

  // 计算fail函数
  void getFail() {
    queue<int> q;
    f[0] = 0;
    // 初始化队列
    for (int c = 0; c < SIGMA_SIZE; c++) {
      int u = ch[0][c];
      if (u) f[u] = 0, q.push(u), last[u] = 0;
    }
    // 按BFS顺序计算fail
    while (!q.empty()) {
      int r = q.front();
      q.pop();
      for (int c = 0; c < SIGMA_SIZE; c++) {
        int u = ch[r][c];
        if (!u) continue;
        q.push(u);
        int v = f[r];
        while (v && !ch[v][c]) v = f[v];
        f[u] = ch[v][c];
        last[u] = val[f[u]] ? f[u] : last[f[u]];
      }
    }
  }
};

AhoCorasickAutomata ac;

char text[1000001], P[MAXS][80];
int main() {
  for (int n; scanf("%d", &n) == 1 && n;) {
    ac.init();
    for (int i = 1; i <= n; i++) scanf("%s", P[i]), ac.insert(P[i], i);
    ac.getFail();
    scanf("%s", text), ac.find(text);
    int best = *max_element(ac.cnt + 1, ac.cnt + n + 1);
    printf("%d\n", best);
    for (int i = 1; i <= n; i++)
      if (ac.cnt[ms[string(P[i])]] == best) printf("%s\n", P[i]);
  }
  return 0;
}
// Accepted 20ms 2349 C++5.3.0 2020-12-1411:41:37 25845648
```

## 3.4 字符串（2）

### 例题20  口吃的外星人（Stammering Aliens, SWERC 2009, UVa12206）

```cpp
// 例题20  口吃的外星人（Stammering Aliens, SWERC 2009, UVa12206）
// 陈锋
#include <algorithm>
#include <cstdio>
#include <iostream>
#include <vector>
using namespace std;
typedef unsigned long long ULL;
const int MAXN = 40000 + 8;
const ULL x = 123;
ULL H[MAXN], PX[MAXN], Hash[MAXN];
void init_PX() {
  PX[0] = 1;
  for (int i = 1; i < MAXN; i++) PX[i] = x * PX[i - 1];
}
int N, sa[MAXN];
void init_hash(const string& s) {
  N = s.length(), H[N] = 0;
  for (int i = N - 1; i >= 0; i--) H[i] = (s[i] - 'a' + 1) + H[i + 1] * x;
}
bool hash_cmp(int a, int b) {
  if (Hash[a] != Hash[b]) return Hash[a] < Hash[b];
  return a < b;
}
bool ok(int L, int M, int& pos) {  // 是否有长度至少len的substr出现M次以上
  for (int i = 0; i <= N - L; i++)
    sa[i] = i, Hash[i] = H[i] - H[i + L] * PX[L];
  sort(sa, sa + N - L + 1, hash_cmp); // 对所有后缀按照hash排序
  pos = -1;
  for (int i = 0, c = 0; i <= N - L; i++) {
    if (i == 0 || Hash[sa[i]] != Hash[sa[i - 1]]) c = 0;
    if (++c >= M) pos = max(pos, sa[i]);
  }
  return pos >= 0;
}
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  init_PX();
  string word;
  for (int t = 0, pos, M; cin >> M >> word && M; t++) {
    init_hash(word);
    if (!ok(1, M, pos)) { puts("none"); continue; }
    int l = 1, r = N + 1;
    while (l + 1 < r) {
      int m = l + (r - l) / 2;
      if (ok(m, M, pos)) l = m;
      else r = m;
    }
    ok(l, M, pos);
    printf("%d %d\n", l, pos);
  }
  return 0;
}
// Accepted 880ms 1613 C++ 5.3.0 2020-12-14 13:07:48 25845792
```

### 例题19  生命的形式（Life Forms, UVa 11107）

```cpp
// 例题19  生命的形式（Life Forms, UVa 11107）
// 陈锋
#include <algorithm>
#include <cstdio>
#include <cstring>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
typedef long long LL;

template <int SZ>
struct SuffixArray {
  int s[SZ];  // 原始字符数组（最后一个字符应必须是0，而前面的字符必须非0）
  int sa[SZ];      // 后缀数组
  int rank[SZ];    // 名次数组. rank[0]一定是n-1，即最后一个字符
  int height[SZ];  // height数组
  int t[SZ], t2[SZ], c[SZ];  // 辅助数组
  int n;                     // 字符个数

  void clear() { n = 0, fill_n(sa, SZ, 0); }

  // m为最大字符值加1。调用之前需设置好s和n
  void build_sa(int m) {
    int i, *x = t, *y = t2;
    for (i = 0; i < m; i++) c[i] = 0;
    for (i = 0; i < n; i++) c[x[i] = s[i]]++;
    for (i = 1; i < m; i++) c[i] += c[i - 1];
    for (i = n - 1; i >= 0; i--) sa[--c[x[i]]] = i;
    for (int k = 1; k <= n; k <<= 1) {
      int p = 0;
      for (i = n - k; i < n; i++) y[p++] = i;
      for (i = 0; i < n; i++)
        if (sa[i] >= k) y[p++] = sa[i] - k;
      for (i = 0; i < m; i++) c[i] = 0;
      for (i = 0; i < n; i++) c[x[y[i]]]++;
      for (i = 0; i < m; i++) c[i] += c[i - 1];
      for (i = n - 1; i >= 0; i--) sa[--c[x[y[i]]]] = y[i];
      swap(x, y);
      p = 1;
      x[sa[0]] = 0;
      for (i = 1; i < n; i++)
        x[sa[i]] = y[sa[i - 1]] == y[sa[i]] && y[sa[i - 1] + k] == y[sa[i] + k]
                       ? p - 1 : p++;
      if (p >= n) break;
      m = p;
    }
  }

  void build_height() {
    for (int i = 0; i < n; i++) rank[sa[i]] = i;
    for (int i = 0, k = 0; i < n; i++) {
      if (k) k--;
      int j = sa[rank[i] - 1];
      while (s[i + k] == s[j + k]) k++;
      height[rank[i]] = k;
    }
  }
};

const int MAXL = 1000 + 8, MAXN = 100 + 4;
int idx[MAXL * MAXN], flag[MAXN], N;
char buf[MAXL];
SuffixArray<MAXL * MAXN> sa;

bool good(int L, int R) {
  if (R - L <= N / 2) return false;
  fill_n(flag, MAXN, 0);
  int cnt = 0;
  _for(i, L, R) {
    int x = idx[sa.sa[i]];
    if (x != N && !flag[x]) flag[x] = 1, cnt++;
  }
  return cnt > N / 2;
}

void print_sub(int L, int R) {  // print s[L,R)
  _for(i, L, R) printf("%c", sa.s[i] - 1 + 'a');
  puts("");
}

bool print_sol(int len, bool print = false) {
  for (int L = 0, R = 1; R <= sa.n; R++) {
    if (R == sa.n || sa.height[R] < len) {  // 新开一段
      if (good(L, R)) {
        if (!print) return true;
        print_sub(sa.sa[L], sa.sa[L] + len);
      }
      L = R;
    }
  }
  return false;
}

void solve(int maxLen) {
  if (!print_sol(1)) {
    puts("?");
    return;
  }
  int L = 1, R = maxLen, M;
  while (L < R) {
    M = L + (R - L + 1) / 2;
    if (print_sol(M)) L = M;
    else R = M - 1;
  }
  print_sol(L, true);
}

// 给字符串加上一个字符，属于字符串i
void add(int ch, int i) { idx[sa.n] = i, sa.s[sa.n++] = ch; }

int main() {
  for (int t = 0; scanf("%d", &N) == 1 && N; t++) {
    if (t) puts("");
    int maxl = 0;
    sa.n = 0;
    _for(i, 0, N) {
      scanf("%s", buf);
      int sz = strlen(buf);
      maxl = max(maxl, sz);
      _for(j, 0, sz) add(buf[j] - 'a' + 1, i);
      add(100 + i, N);
    }
    add(0, N);
    if (N == 1)
      puts(buf);
    else
      sa.build_sa(N + 100), sa.build_height(), solve(maxl);
  }
  return 0;
}
// Accepted 70ms 3250 C++5.3.0 2020-12-1412:59:10 25845774
```

### 例题21  扩展成回文（Extend to Palindrome, UVa11475）

```cpp
// 例题21  扩展成回文（Extend to Palindrome, UVa11475）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 1e5 + 4;
char S[MAXN], T[MAXN * 2];
int P[MAXN * 2];
void manacher(const char *s, int len) {
  int l = 0;
  T[l++] = '$', T[l++] = '#';
  for(int i = 0; i < len; i++) T[l++] = s[i], T[l++] = '#';
  T[l] = 0;
  int r = 0, c = 0;
  for(int i = 0; i < l; i++) {
    int &p = P[i];
    p = r > i ? min(P[2 * c - i], r - i) : 1;
    while(T[i + p] == T[i - p]) p++;
    if(i + p > r) r = i + p, c = i;
  }
}
int main() {
  while(scanf("%s", S) == 1) {
    int ans = 0, L = strlen(S);
    manacher(S, L);
    for(int i = 0; i < 2 * L + 2; i++)
      if(P[i] + i == 2 * L + 2) ans = max(ans, P[i] - 1); //此回文串是作为后缀出现的，更新答案
    printf("%s", S);
    for(int i = L - ans - 1; i >= 0; i--) printf("%c", S[i]);
    puts("");
  }
  return 0;
}
// 24183083 11475 Extend to Palindrome  Accepted  C++11 0.010 2019-11-12 07:25:40
```

## 3.5 字符串（3）

### 例题25  转世（Reincarnation HDU4622）

```cpp
// 例题25  转世（Reincarnation HDU4622）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i,a,b) for( int i=(a); i<(int)(b); ++i)
#define _rep(i,a,b) for( int i=(a); i<=(int)(b); ++i)
typedef long long LL;

template<int SZ, int SIG = 32>
struct Suffix_Automaton {
  int link[SZ], len[SZ], isClone[SZ], next[SZ][SIG], last, sz;
  inline void init() { sz = 0, last = new_node(); }
  inline int new_node() {
    assert(sz + 1 < SZ);
    int nd = sz++;
    fill_n(next[nd], SIG, 0), link[nd] = -1, len[nd] = 0, isClone[nd] = 0;
    return nd;
  }
  inline int idx(char c) { return c - 'a'; }
  inline void insert(char c) {
    int p = last, cur = new_node(), x = idx(c);
    len[last = cur] = len[p] + 1;
    while (p != -1 && !next[p][x]) next[p][x] = cur, p = link[p];
    if (p == -1) {
      link[cur] = 0;
      return;
    }
    int q = next[p][x];
    if (len[p] + 1 == len[q]) {
      link[cur] = q;
      return;
    }
    int nq = new_node();
    isClone[nq] = 1, copy_n(next[q], SIG, next[nq]);
    link[nq] = link[q], len[nq] = len[p] + 1, link[cur] = link[q] = nq;
    while (p >= 0 && next[p][x] == q) next[p][x] = nq, p = link[p];
  }
  inline void build(const char* s) { while (*s) insert(*s++); }
};

const int NN = 2000 + 4;
Suffix_Automaton<2 * NN> sam;
int F[NN][NN];

int main() {
  string s;
  ios::sync_with_stdio(false), cin.tie(0);
  int T; cin >> T;
  while (T--) {
    cin >> s;
    int N = s.size();
    memset(F, 0, sizeof(F));
    _for(i, 0, N) {
      sam.init();
      _for(j, i, N) {
        sam.insert(s[j]);
        int p = sam.last;
        F[i][j] = F[i][j - 1] + sam.len[p] - sam.len[sam.link[p]];
      }
    }
    int Q, l, r; cin >> Q;
    _for(i, 0, Q) {
      cin >> l >> r;
      cout << F[l - 1][r - 1] << endl;
    }
  }
  return 0;
}
// Accepted 1076ms 18576kB 1780 G++ 2019-09-26 23:54:34
```

### 例题28  第K次出现（Kth-occurrence, HDU6704, CCPC 2019网络选拔赛）

```cpp
// 例题28  第K次出现（Kth-occurrence, HDU6704, CCPC 2019网络选拔赛）
// 陈锋
#include<bits/stdc++.h>
using namespace std;
const int NN = 1e6 + 10;
template<int SZ>
struct WSegTree { // 动态权值线段树
  int sz, ls[SZ * 4], rs[SZ * 4], sum[SZ * 4];
  void init() { sz = 0; }
  int maintain(int u) { sum[u] = sum[ls[u]] + sum[rs[u]]; return u; }
  int new_node() {
    ++sz;
    sum[sz] = ls[sz] = rs[sz] = 0;
    return sz;
  }

  void insert(int& u, int l, int r, int k) { // add a k in u([l, r])
    if (u == 0) u = new_node();
    if (l == r) {
      assert(l <= k && k <= r);
      sum[u]++;
      return;
    }
    int m = (l + r) / 2;
    if (k <= m) insert(ls[u], l, m, k);
    else insert(rs[u], m + 1, r, k);
    maintain(u);
  }

  int merge(int x, int y) { // 权值线段树合并
    if (x == 0 || y == 0) return x + y;
    int p = new_node();
    ls[p] = merge(ls[x], ls[y]), rs[p] = merge(rs[x], rs[y]);
    return maintain(p);
  }

  int kth(int u, int l, int r, int k) {
    if (l == r) return l; // node u([l,r]), 查询第k小
    int m = (l + r) / 2, lc = ls[u], rc = rs[u];
    if (k <= sum[lc]) return kth(lc, l, m, k);
    if (k <= sum[u]) return kth(rc, m + 1, r, k - sum[lc]);
    return -1;
  }
};
struct Edge { int to, next; };
template<int SZ>
struct SAM {
  WSegTree<SZ> st;
  int sz, last, len[SZ], link[SZ], ch[SZ][30], end_pos[SZ];
  int seg_root[SZ], fa[SZ][30], ecnt, EHead[SZ];
  Edge E[SZ * 2];

  void init() {
    last = 1, ecnt = 0, sz = 0;
    new_stat(), st.init();
  }

  int new_stat() {
    int q = ++sz;
    EHead[q] = 0, len[q] = 0, link[q] = 0, seg_root[q] = 0;
    fill_n(ch[q], 30, 0);
    return q;
  }

  void insert(int i, int c, int n) {
    int cur = new_stat(), p = last;
    end_pos[i] = cur, len[cur] = i;
    for (; p && !ch[p][c]; p = link[p]) ch[p][c] = cur;
    if (!p)
      link[cur] = 1;
    else {
      int q = ch[p][c];
      if (len[q] == len[p] + 1) link[cur] = q;
      else {
        int nq = new_stat();
        link[nq] = link[q], len[nq] = len[p] + 1;
        for (; p && ch[p][c] == q; p = link[p]) ch[p][c] = nq;
        memcpy(ch[nq], ch[q], sizeof ch[q]);
        link[q] = link[cur] = nq;
      }
    }
    last = cur;
    st.insert(seg_root[cur], 1, n, i);
  }

  // 后缀树结构维护->倍增逻辑
  void add_edge(int x, int y) { E[++ecnt] = {y, EHead[x]}, EHead[x] = ecnt; }

  void dfs(int u) {
    for (int i = 1; i <= 20; ++i) fa[u][i] = fa[fa[u][i - 1]][i - 1];
    for (int i = EHead[u]; i; i = E[i].next) {
      int v = E[i].to;
      fa[v][0] = u, dfs(v);
      seg_root[u] = st.merge(seg_root[u], seg_root[v]);
    }
  }

  void build() {
    for (int i = 2; i <= sz; ++i) add_edge(link[i], i);
    dfs(1);
  }

  int kth(int l, int r, int k, int n) {
    int u = end_pos[r];
    for (int i = 20; i >= 0; --i) { // 倍增找S[l, r]对应的点
      int p = fa[u][i];
      if (l + len[p] - 1 >= r) u = p;
    }
    int ans = st.kth(seg_root[u], 1, n, k);
    return (ans == -1) ? ans : ans - (r - l);
  }
};

SAM<NN> sam;
char a[NN];
int main() {
  int N, T, q, l, r, k;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%d", &N, &q), scanf("%s", a + 1), sam.init();
    for (int i = 1; i <= N; ++i) sam.insert(i, a[i] - 'a' + 1, N);
    sam.build();
    while (q--) {
      scanf("%d%d%d", &l, &r, &k);
      printf("%d\n", sam.kth(l, r, k, N));
    }
  }
  return 0;
}
// Accepted 1684ms 92092kB 3271 G++2019-12-09 21:34:42 31813560
```

### 例题27  子串之和（str2int, Asia – Tianjin 2012, LA6387/UVa1673）

```cpp
// 例题27  子串之和（str2int, Asia – Tianjin 2012, LA6387/UVa1673）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

#define _for(i,a,b) for( int i=(a); i<(int)(b); ++i)
#define _rep(i,a,b) for( int i=(a); i<=(int)(b); ++i)

template<int SZ, int SIG = 32>
struct Suffix_Automaton {
  int link[SZ], len[SZ], last, sz;
  map<char, int> next[SZ];
  inline void init() { sz = 0, last = new_node(); }
  inline int new_node() {
    assert(sz + 1 < SZ);
    int nd = sz++;
    next[nd].clear(), link[nd] = -1, len[nd] = 0;
    return nd;
  }
  inline void insert(char x) {
    int p = last, cur = new_node();
    len[last = cur] = len[p] + 1;
    while (p != -1 && !next[p].count(x))
      next[p][x] = cur, p = link[p];
    if (p == -1) {
      link[cur] = 0;
      return;
    }
    int q = next[p][x];
    if (len[p] + 1 == len[q]) {
      link[cur] = q;
      return;
    }
    int nq = new_node();
    next[nq] = next[q];
    link[nq] = link[q], len[nq] = len[p] + 1, link[cur] = link[q] = nq;
    while (p >= 0 && next[p][x] == q) next[p][x] = nq, p = link[p];
  }
  inline void build(const char* s) { while (*s) insert(*s++); }
};

typedef long long LL;
const int NS = 2e5 + 4, M = 2012;
Suffix_Automaton<NS> sam;
int V[NS], Cnt[NS], Sum[NS];
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  string s;
  int N;
  while (cin >> N && N) {
    sam.init();
    _for(i, 0, N) {
      cin >> s, sam.build(s.c_str());
      if (i != N - 1) sam.insert('9' + 1);
    }
    _for(i, 0, sam.sz) V[i] = i;
    sort(V, V + sam.sz, [](int a, int b) { return sam.len[a] < sam.len[b]; });
    fill_n(Cnt, sam.sz, 0), fill_n(Sum, sam.sz, 0);

    Cnt[0] = 1;
    int ans = 0;
    _for(i, 0, sam.sz) {
      int u = V[i];
      char st = u ? '0' : '1';
      for (char c = st; c <= '9'; ++c)
        if (sam.next[u].count(c)) {
          int v = sam.next[u][c];
          (Cnt[v] += Cnt[u]) %= M;
          (Sum[v] += Sum[u] * 10 + (c - '0') * Cnt[u]) %= M;
        }
      (ans += Sum[u]) %= M;
    }
    cout << ans << endl;
  }
  return 0;
}
// 25877523	1673	str2int	Accepted	C++	0.410	2020-12-23 05:48:53
```

### 例题22  最小循环串（Glass Beads, SPOJ BEADS）

```cpp
// 例题22  最小循环串（Glass Beads, SPOJ BEADS）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

#define _for(i,a,b) for( int i=(a); i<(int)(b); ++i)
#define _rep(i,a,b) for( int i=(a); i<=(int)(b); ++i)

template<int SZ, int SIG = 32>
struct Suffix_Automaton {
  int link[SZ], len[SZ], last, sz;
  map<char, int> next[SZ];
  inline void init() { sz = 0, last = new_node(); }
  inline int new_node() {
    assert(sz + 1 < SZ);
    int nd = sz++;
    next[nd].clear(), link[nd] = -1, len[nd] = 0;
    return nd;
  }
  inline void insert(char x) {
    int p = last, cur = new_node();
    len[last = cur] = len[p] + 1;
    while (p != -1 && !next[p].count(x))
      next[p][x] = cur, p = link[p];
    if (p == -1) {
      link[cur] = 0;
      return;
    }
    int q = next[p][x];
    if (len[p] + 1 == len[q]) {
      link[cur] = q;
      return;
    }
    int nq = new_node();
    next[nq] = next[q];
    link[nq] = link[q], len[nq] = len[p] + 1, link[cur] = link[q] = nq;
    while (p >= 0 && next[p][x] == q) next[p][x] = nq, p = link[p];
  }
  inline void build(char* s) { while (*s) insert(*s++); }
};

typedef long long LL;
const int NN = 10000 + 4;
char S[NN];
Suffix_Automaton<NN * 4> sam;
int main() {
  int T;
  scanf("%d", &T);
  while (T--) {
    scanf("%s", S);
    sam.init(), sam.build(S), sam.build(S);
    int p = 0, N = strlen(S);
    for (int i = 0; i < N; i++)
      p = sam.next[p].begin()->second;
    printf("%d\n", sam.len[p] - N + 1);
  }
  return 0;
}
// 2594177 Glass Beads Accepted  C++11 0.452 2019-09-26 04:30:13
```

### 例题24  最长公共子串（Longest Common Substring, SPOJ LCS）

```cpp
// 例题24  最长公共子串（Longest Common Substring, SPOJ LCS）
// 陈锋
#include <bits/stdc++.h>
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)
typedef long long LL;
using namespace std;
template<int SZ, int SIG = 32>
struct Suffix_Automaton {
  int link[SZ], len[SZ], last, sz;
  map<char, int> next[SZ];
  inline void init() { sz = 0, last = new_node(); }
  inline int new_node() {
    assert(sz + 1 < SZ);
    int nd = sz++;
    next[nd].clear(), link[nd] = -1, len[nd] = 0;
    return nd;
  }
  inline void insert(char x) {
    int p = last, cur = new_node();
    len[last = cur] = len[p] + 1;
    while (p != -1 && !next[p].count(x))
      next[p][x] = cur, p = link[p];
    if (p == -1) {
      link[cur] = 0;
      return;
    }
    int q = next[p][x];
    if (len[p] + 1 == len[q]) {
      link[cur] = q;
      return;
    }
    int nq = new_node();
    next[nq] = next[q];
    link[nq] = link[q], len[nq] = len[p] + 1, link[cur] = link[q] = nq;
    while (p >= 0 && next[p][x] == q) next[p][x] = nq, p = link[p];
  }
  inline void build(char* s) { while (*s) insert(*s++); }
};

const int NN = 5e5 + 5;
Suffix_Automaton<NN> sam;
int lcs(char* s) {
  int p = 0, l = 0, ans = 0;
  map<char, int>* nxt = sam.next;
  while (*s) {
    char x = *s++;
    if (nxt[p].count(x)) p = nxt[p][x], l++;
    else {
      while (p != -1 && !nxt[p].count(x))
        p = sam.link[p];
      if (p != -1)
        l = sam.len[p] + 1, p = nxt[p][x];
      else
        p = 0, l = 0;
    }
    ans = max(ans, l);
  }
  return ans;
}
char S[NN];
int main() {
  scanf("%s", S);
  sam.init(), sam.build(S);
  scanf("%s", S);
  printf("%d", lcs(S));
  return 0;
}
// 24466222 2019-09-26 14:53:40 Feng Chen Longest Common Substring  accepted 0.25  56M CPP14
```

### 例题26  子串计数（Substrings, SPOJ NSUBSTR）

```cpp
// 例题26  子串计数（Substrings, SPOJ NSUBSTR）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i,a,b) for( int i=(a); i<(int)(b); ++i)
#define _rep(i,a,b) for( int i=(a); i<=(int)(b); ++i)
typedef long long LL;

template<int SZ, int SIG = 32>
struct Suffix_Automaton {
  int link[SZ], len[SZ], isterminal[SZ], next[SZ][SIG], last, sz;
  inline void init() { sz = 0, last = new_node(); }
  inline int new_node() {
    assert(sz + 1 < SZ);
    int nd = sz++;
    fill_n(next[nd], SIG, 0), link[nd] = -1, len[nd] = 0, isterminal[nd] = 0;
    return nd;
  }
  inline int idx(char c) { return c - 'a'; }
  inline void insert(char c) {
    int p = last, cur = new_node(), x = idx(c);
    len[last = cur] = len[p] + 1, isterminal[cur] = 1;
    while (p != -1 && !next[p][x]) next[p][x] = cur, p = link[p];
    if (p == -1) {
      link[cur] = 0;
      return;
    }
    int q = next[p][x];
    if (len[p] + 1 == len[q]) {
      link[cur] = q;
      return;
    }
    int nq = new_node();
    copy_n(next[q], SIG, next[nq]);
    link[nq] = link[q], len[nq] = len[p] + 1, link[cur] = link[q] = nq;
    while (p >= 0 && next[p][x] == q) next[p][x] = nq, p = link[p];
  }
  inline void build(const char* s) { while (*s) insert(*s++); }
};

const int NN = 250000 + 4;
vector<int> G[NN * 2];
Suffix_Automaton<NN * 2> sam;
int F[NN];
int dfs(int u) {
  int s = sam.isterminal[u];
  for (auto v : G[u]) s += dfs(v);
  F[sam.len[u]] = max(F[sam.len[u]], s);
  return s;
}

char S[NN];
int main() {
  scanf("%s", S);
  int N = strlen(S);
  sam.init(), sam.build(S);
  _for(u, 1, sam.sz) G[sam.link[u]].push_back(u);
  dfs(0);
  _rep(l, 1, N) printf("%d\n", F[l]);
  return 0;
}
// 24467571 2019-09-26 17:18:19 Feng Chen Substrings  accepted 0.22  70M CPP14
```

### 例题23 不同的子串（New Distinct Substrings, SPOJ SUBST1）

```cpp
// 例题23 不同的子串（New Distinct Substrings, SPOJ SUBST1）
// 陈锋
#include <bits/stdc++.h>
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)
typedef long long LL;
using namespace std;

template<int SZ, int SIG = 32>
struct Suffix_Automaton {
  int link[SZ], len[SZ], last, sz;
  map<char, int> next[SZ];
  inline void init() { sz = 0, last = new_node(); }
  inline int new_node() {
    assert(sz + 1 < SZ);
    int nd = sz++;
    next[nd].clear(), link[nd] = -1, len[nd] = 0;
    return nd;
  }
  inline void insert(char x) {
    int p = last, cur = new_node();
    len[last = cur] = len[p] + 1;
    while (p != -1 && !next[p].count(x))
      next[p][x] = cur, p = link[p];
    if (p == -1) {
      link[cur] = 0;
      return;
    }
    int q = next[p][x];
    if (len[p] + 1 == len[q]) {
      link[cur] = q;
      return;
    }
    int nq = new_node();
    next[nq] = next[q];
    link[nq] = link[q], len[nq] = len[p] + 1, link[cur] = link[q] = nq;
    while (p >= 0 && next[p][x] == q) next[p][x] = nq, p = link[p];
    return;
  }
  inline void build(char* s) { while (*s) insert(*s++); }
};

const int NN = 5e4 + 4;
Suffix_Automaton<NN * 2> sam;
char S[NN];
LL F[NN * 2];

LL dpF(int v) {
  LL &f = F[v];
  if (f != -1) return f;
  f = 1;
  const auto& E = sam.next[v];
  if (E.empty()) return f = 1;
  for (const auto& p : E) f += dpF(p.second);
  return f;
}

int main() {
  int T;
  scanf("%d", &T);
  while (T--) {
    scanf("%s", S);
    sam.init(), sam.build(S);
    fill_n(F, NN * 2, -1);
    printf("%lld\n", dpF(0) - 1);
  }
}
// 24466280 2019-09-26 14:59:33 Feng Chen New Distinct Substrings accepted 0.15  17M CPP14
```

## 3.6 排序二叉树

### 例题30  图询问（Graph and Queries, Tianjin 2010, LA 5031/HDU3726）

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

### 例题29 优势人群（Efficient Solutions, UVa 11020）

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

### 例题31  排列变换（Permutation Transformer, UVa 11922）

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

### 例题32 魔法珠宝（Jewel Magic, UVa 11996）

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

## 3.7 树的经典问题与方法

### 例题34  Rikka与路径的交集（Rikka with Intersection of Paths, ACM/ICPC徐州2018, CodeforceGym 102012G）

```cpp
// 例题34  Rikka与路径的交集（Rikka with Intersection of Paths, ACM/ICPC徐州2018, CodeforceGym 102012G）
// 陈锋
#include <bits/stdc++.h>
const int NN = 3e5 + 8, MOD = 1000000007, HH = ceil(log2(NN));
using namespace std;
typedef long long LL;
#define _for(i,a,b) for( int i=(a); i<(int)(b); ++i)
#define _rep(i,a,b) for( int i=(a); i<=(int)(b); ++i)

void gcd(LL a, LL b, LL& d, LL& x, LL& y) {
  if (!b) d = a, x = 1, y = 0;
  else gcd(b, a % b, d, y, x), y -= x * (a / b);
}
LL inv(LL a, LL n) { // solve ax≡1 mod n
  LL d, x, y;
  gcd(a, n, d, x, y);
  return d == 1 ? (x + n) % n : -1;
}

LL Fact[NN]; // i!
inline LL C(int a, int b) { // C(a, b)
  if (a < 0 || b < 0 || a < b) return 0;
  return 1LL * (Fact[a] * inv(Fact[a - b], MOD) % MOD)
         * inv(Fact[b], MOD) % MOD;
}

vector<int> G[NN];
int Fa[NN][HH + 1], D[NN], P[NN], A[NN];
inline void dfs(int u, int fa, int d) {
  Fa[u][0] = fa, D[u] = d;
  _rep(i, 1, HH) Fa[u][i] = Fa[Fa[u][i - 1]][i - 1];
  for (auto v : G[u]) if (v != fa) dfs(v, u, d + 1);
}

int lca(int u, int v) {
  if (D[u] < D[v]) swap(u, v);
  int diff = D[u] - D[v];
  _rep(h, 0, HH) if (diff & (1 << h)) u = Fa[u][h];
  if (u == v) return u;
  for (int h = HH; h >= 0; h--)
    if (Fa[u][h] != Fa[v][h]) u = Fa[u][h], v = Fa[v][h];
  return Fa[u][0];
}

inline void differ(int u, int fa) { // 树上差分
  for (auto v : G[u])
    if (v != fa) differ(v, u), P[u] += P[v];
}

int main() {
  Fact[0] = 1;
  _for(i, 1, NN) Fact[i] = 1LL * Fact[i - 1] * i % MOD;
  ios::sync_with_stdio(false), cin.tie(0);
  int T; cin >> T;
  for (int t = 0, N, m, k, u, v; t < T; ++t) {
    cin >> N >> m >> k;
    fill_n(P, N + 1, 0), fill_n(A, N + 1, 0);
    _rep(i, 0, N) G[i].clear();
    _for(i, 1, N) cin >> u >> v, G[u].push_back(v), G[v].push_back(u);
    dfs(1, 0, 1);
    for (int i = 1, d; i <= m; ++i) {
      cin >> u >> v, d = lca(u, v);
      ++A[d], ++P[u], ++P[v], --P[d]; // d多计算一次
      if (d != 1) --P[Fa[d][0]]; // Fa[d]-root多计算两次
    } // P[u]: u→根节点路径上点为端点的简单路径条数之和, A[u]: u是几条路径的LCA?
    differ(1, 0); // 树上差分合并之后：P[u]: 有多少条路径经过u
    LL ans = 0; // 对于两条路径的交点，我们只统计是某直线端点LCA的那个，不是LCA的不算
    _rep(i, 1, N) (ans += C(P[i], k) - C(P[i] - A[i], k) + MOD) %= MOD;
    printf("%lld\n", ans);
  }
  return 0;
}
// 72027006 Feb/28/2020 G - Rikka with Intersections of Paths GNU C++11 Accepted  5677 ms 46000 KB
```

### 例题33  村庄有多远（How far away, HDU 2586） ECJTU 2009 Spring Contest

```cpp
// 例题33  村庄有多远（How far away, HDU 2586） ECJTU 2009 Spring Contest
// 陈锋
#include <bits/stdc++.h>

using namespace std;
const int MAXN = 40000 + 4;
int N, L, Tin[MAXN], Tout[MAXN], UP[MAXN][18], timer;
struct Edge {
  int v, k;
  Edge(int _v, int _k) : v(_v), k(_k) {}
};
vector<Edge> G[MAXN];
int Dist[MAXN], D[MAXN]; // 到root的距离，深度

// LCA预处理
void dfs(int u, int fa) {
  Tin[u] = ++timer, UP[u][0] = fa;
  if (u) D[u] = D[fa] + 1;
  for (int i = 1; i < L; i++)
    UP[u][i] = UP[UP[u][i - 1]][i - 1];
  for (size_t i = 0; i < G[u].size(); i++) {
    const Edge& e = G[u][i];
    if (e.v != fa) Dist[e.v] = Dist[u] + e.k, dfs(e.v, u);
  }
  Tout[u] = ++timer;
}

bool isAncestor(int u, int v) { return Tin[u] <= Tin[v] && Tout[u] >= Tout[v]; }

int LCA(int u, int v) {
  if (D[u] > D[v]) return LCA(v, u); // 保证u的深度<v的深度
  if (isAncestor(u, v)) return u; // u是v的祖先
  for (int i = L; i >= 0; --i) if (!isAncestor(UP[u][i], v)) u = UP[u][i];
  return UP[u][0];
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T, M, u, v, k;
  L = ceil(log2(N));
  cin >> T;
  while (T--) {
    cin >> N >> M;
    for (int i = 0; i < N; i++) G[i].clear();
    for (int i = 0; i < N - 1; i++)  {
      cin >> u >> v >> k, u--, v--;
      G[u].push_back(Edge(v, k)), G[v].push_back(Edge(u, k));
    }
    memset(UP, 0, sizeof(UP));
    Dist[0] = 0, D[0] = 0;
    dfs(0, 0);

    for (int i = 0; i < M; i++) {
      cin >> u >> v, u--, v--;
      int w = LCA(u, v);
      cout << Dist[u] + Dist[v] - 2 * Dist[w] << endl;
    }
  }
  return 0;
}
// Accepted 46ms 10220kB 1526 G++2020-01-30 11:30:51
```

### 例题37  竞赛（Race, IOI 2011，牛客NC51143）

```cpp
// 例题37  竞赛（Race, IOI 2011，牛客NC51143）
// 求一条简单路径，权值和等于K，且边数最小。
// 陈锋
#include<bits/stdc++.h>
using namespace std;

const int NN = 2e5 + 8, KK = 1e6 + 8, INF = 1 << 30;
int N, K, MaxSub[NN], SZ[NN], F[KK];
// MaxSub[i]: 去除节点i后得到的森林中节点数最多的树的节点
// SZ：保存子树的节点数
// F[i]权值和为i的路径包含的最小边数
bool Vis[NN];
struct Edge { int v, w; };
struct Path { int w, ec; }; // 路径权值之和，边数
vector<Edge> G[NN];

// 获取子树u的重心, treesz为整个子树大小，重心用来更新center
void find_center(int u, int fa, const int treesz, int& center) {
  int &s = SZ[u], &m = MaxSub[u];
  s = 1, m = 0;
  for (const auto &e : G[u]) {
    if (e.v == fa || Vis[e.v]) continue;
    find_center(e.v, u, treesz, center);
    s += SZ[e.v], m = max(m, SZ[e.v]);
  }
  m = max(m, treesz - s);
  if (m < MaxSub[center]) center = u;
}
// 收集子树u中每个点到根节点的路径的{权值和sw,边数ec}，只考虑权值和<=K的
void collect_path(int u, int fa, int sw, int ec, vector<Path> &S) {
  if (sw > K) return;
  S.push_back({sw, ec});
  for (const Edge &e : G[u])
    if (e.v != fa && !Vis[e.v]) collect_path(e.v, u, sw + e.w, ec + 1, S);
}
// 子树u中所有经过u且权值和=K的路径，这些路径长度(边数)的最小值→min_ec
void solve(int u, int& min_ec) {
  vector<int> q;
  for (const auto & e : G[u]) {
    if (Vis[e.v]) continue;
    vector<Path> S;
    collect_path(e.v, u, e.w, 1, S);
    for (auto& it : S) min_ec = min(min_ec, it.ec + F[K - it.w]); // 当前路径和之前子树路径的组合
    for (auto& it : S) q.push_back(it.w), F[it.w] = min(F[it.w], it.ec); // 更新这条路径对应的F值，让后来的子树用
  }
  for (int i : q) F[i] = INF;
}
void dfs(int u, int& min_ec) { // 递归求解子树u
  Vis[u] = true, F[0] = 0;
  solve(u, min_ec); //
  for (const auto & e : G[u]) {
    if (Vis[e.v]) continue;
    int center = 0; // 找子树v的中心，然后递归求解子树v
    find_center(e.v, u, SZ[e.v], center), dfs(center, min_ec);
  }
}

int main() {
  int N;
  scanf("%d%d", &N, &K);
  for (int i = 1, u, v, w; i < N; ++i) {
    scanf("%d%d%d", &u, &v, &w), ++u, ++v;
    G[u].push_back({v, w}), G[v].push_back({u, w});
  }
  fill_n(F, K + 1, INF);
  MaxSub[0] = INF;
  int min_ec = INF, center = 0;
  find_center(1, 0, N, center), dfs(center, min_ec);
  printf("%d\n", min_ec == INF ? -1 : min_ec);
  return 0;
}
// 46224368 Race Accepted 100 643 31840 2091 C++ 2020-12-23 14:23:18
```

### 例题40 要有彩虹（Let there be rainbows!, IPSC 2009 Problem L）

```cpp
// 例题40 要有彩虹（Let there be rainbows!, IPSC 2009 Problem L）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i,a,b) for( int i=(a); i<(int)(b); ++i)
#define _rep(i,a,b) for( int i=(a); i<=(int)(b); ++i)
typedef long long LL;
struct IntTree { // 每颗重链对应的线段树，IPSC不卡内存，如果其它OJ，可以考虑动态开点
  struct Node {
    int color, sum[8]; // color:区间颜色:0无颜色, sum:颜色的个数
    void setc(int c, int len) {
      color = c;
      fill_n(sum, 8, 0), sum[c] = len;
    }
    Node() { setc(0, 0); }
  };
  int L;
  vector<Node> data;
  IntTree(int N) { L = 1 << (int)(ceil(log2(N + 2))), data.resize(2 * L); }
  void insert(int l, int r, int clr, int o, int L, int len) {
    if (r <= L || l >= L + len) return; // [L, L+len] ∩ [l,r] = Φ
    Node& d = data[o], &ld = data[2 * o], &rd = data[2 * o + 1];
    if (l <= L && L + len <= r) { // [L, L+len) ∈ (l, r)
      d.setc(clr, len);
      return;
    }
    if (d.color != 0) ld.setc(d.color, len / 2), rd.setc(d.color, len / 2);
    d.setc(0, 0);
    insert(l, r, clr, 2 * o, L, len / 2);
    insert(l, r, clr, 2 * o + 1, L + len / 2, len / 2);
    _for(i, 0, 8) d.sum[i] += ld.sum[i] + rd.sum[i];
  }
  int count(int l, int r, int clr, int o, int L, int len) {
    if (r <= L || l >= L + len) return 0; // [L, L+len] ∩ [l,r] = Φ
    Node& d = data[o], &ld = data[2 * o], &rd = data[2 * o + 1];
    if (l <= L && L + len <= r) return d.sum[clr]; // [L, L+len) ∈ (l, r)
    if (d.color != 0) ld.setc(d.color, len / 2), rd.setc(d.color, len / 2);
    return count(l, r, clr, 2 * o, L, len / 2)
           + count(l, r, clr, 2 * o + 1, L + len / 2, len / 2);
  }
  void insert(int l, int r, int clr) { insert(l, r, clr, 1, 0, L); }
  int count(int l, int r, int clr) { return count(l, r, clr, 1, 0, L); }
};
const int NN = 1e6 + 8;
typedef vector<int> IVec;
IVec G[NN], CH[NN]; // 图的结构
int N, Fa[NN], Tin[NN], Tout[NN], Tsz[NN]; // 父节点，时间戳，子树大小
bool Vis[NN];
int PathId[NN], PathOffset[NN]; // 每个点所在的重链以及在其中的位置
vector<IVec> Paths; // 所有重链独立存放
vector<IntTree> ST; // 每个重链对应一颗线段树

void hld() {
  fill_n(Vis, N + 1, false), fill_n(Tsz, N + 1, 0);
  _rep(i, 0, N) CH[i].clear();
  Paths.clear();

  vector<int> walk; // 后续遍历的DFS序
  int time = 0;
  Vis[0] = true, Tin[0] = time, Fa[0] = 0;
  stack<int> sv, se; // 当前处理的u以及下一个要处理的u的子节点v对应的边
  sv.push(0), se.push(0);
  while (!sv.empty()) { // 迭代版的DFS
    ++time;
    int u = sv.top(); sv.pop();
    int e = se.top(); se.pop(); // 当前要处理的子树v的编号
    if (e == (int)G[u].size()) { // u子树都已经处理完
      walk.push_back(u), Tout[u] = time, Tsz[u] = 1;
      for (auto v : CH[u]) Tsz[u] += Tsz[v]; // 子树u的体积
    } else {
      sv.push(u), se.push(e + 1);
      int v = G[u][e]; // u的子节点v
      if (!Vis[v]) {
        Vis[v] = true, Tin[v] = time, Fa[v] = u, CH[u].push_back(v);
        sv.push(v), se.push(0);
      }
    }
  }

  fill_n(Vis, N + 1, false);
  Vis[0] = true; // u->pa[u]处理过了?
  for (auto w : walk) {
    if (Vis[w]) continue;
    IVec p{w};
    while (true) {
      bool heavy = (2 * Tsz[w] >= Tsz[Fa[w]]);
      Vis[w] = true, w = Fa[w], p.push_back(w);
      if (!heavy || Vis[w]) break;
    }
    Paths.push_back(p);
  }

  PathId[0] = -1; // root不在任何链上
  _for(i, 0, Paths.size()) _for(j, 0, Paths[i].size() - 1) {
    PathId[Paths[i][j]] = i;
    PathOffset[Paths[i][j]] = j;
  }
  ST.clear();
  for (const auto& p : Paths) ST.emplace_back(p.size() - 1);
}

inline bool is_ancestor(int x, int y) { // x is an ancestor of y ?
  return (Tin[y] >= Tin[x] && Tout[y] <= Tout[x]);
}

// 统计[x-y]路径上过去不是颜色c的，这次被涂成c了
int query(int x, int y, int c) {
  if (x == y) return 0;
  if (is_ancestor(x, y)) return query(y, x, c);
  int pi = PathId[x], l = PathOffset[x], r = Paths[pi].size() - 1;
  const auto& pt = Paths[pi];
  if (is_ancestor(pt[r], y)) {
    while (r - l > 1) { // 确保r在LCA(x,y)下方
      int m = (r + l) / 2;
      if (is_ancestor(pt[m], y)) r = m; else l = m;
    }
    l = PathOffset[x];
  }
  int ans = r - l - ST[pi].count(l, r, c); // 以前有多少其它颜色, 会被涂成c
  ST[pi].insert(l, r, c);
  return ans + query(pt[r], y, c); // 加上 LCA(x, y)-y路径上的
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  string color[] = {"", "red", "orange", "yellow", "green", "blue", "indigo", "violet"};
  map<string, int> CI;
  _rep(i, 1, 7) CI[color[i]] = i;
  int T, Q; cin >> T;
  while (T--) {
    cin >> N;
    _rep(i, 0, N) G[i].clear();
    for (int i = 0, x, y; i < N - 1; ++i)
      cin >> x >> y, G[x].push_back(y), G[y].push_back(x);
    hld();
    cin >> Q;
    vector<LL> ans(8, 0);
    string c;
    for (int i = 0, x, y; i < Q; i++) {
      cin >> x >> y >> c;
      ans[CI[c]] += query(x, y, CI[c]);
    }
    _rep(i, 1, 7) cout << color[i] << " " << ans[i] << endl;
  }
  return 0;
}
```

### 例题39 软件包管理器（NOI 2015）牛客NC 17882）

```cpp
// 例题39 软件包管理器（NOI 2015）牛客NC 17882）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

typedef long long LL;

template <typename T, int SZ>
struct SegTree {
  struct Node {
    T sumv, setv;
    bool hasSet;
    void setVal(const T& val, int L, int R) {
      setv = val, hasSet = true, sumv = (R - L + 1) * setv;
    }
  };  // sumv: 最新的和；setv: 最新的set标记(子孙不受影响)
  Node NS[SZ];
  int N;
  void init(int _n) {
    N = _n;
    assert((1 << ((int)ceil(log2(N)))) < SZ);
  }

  void pushdown(int o, int L, int R) {
    Node& nd = NS[o];
    if (!nd.hasSet) return;
    int lc = 2 * o, rc = 2 * o + 1, M = (L + R) / 2;
    NS[lc].setVal(nd.setv, L, M), NS[rc].setVal(nd.setv, M + 1, R);
    nd.hasSet = false;
  }

  void setV(int l, int r, const T& v) { update(1, 1, N, v, l, r); }
  void update(int o, int L, int R, const T& v, int qL, int qR) {
    if (qL <= L && qR >= R) {
      NS[o].setVal(v, L, R);
      return;
    }
    int lc = 2 * o, rc = 2 * o + 1, M = (L + R) / 2;
    pushdown(o, L, R);
    if (qL <= M) update(lc, L, M, v, qL, qR);
    if (qR > M) update(rc, M + 1, R, v, qL, qR);
    NS[o].sumv = NS[lc].sumv + NS[rc].sumv;
  }
  T querysum(int l, int r) { return query(1, 1, N, l, r); }
  T query(int o, int L, int R, int qL, int qR) {
    if (qL <= L && qR >= R) return NS[o].sumv;
    pushdown(o, L, R);
    int lc = 2 * o, rc = 2 * o + 1, M = (L + R) / 2;
    T s = 0;
    if (qL <= M) s += query(lc, L, M, qL, qR);
    if (qR > M) s += query(rc, M + 1, R, qL, qR);
    return s;
  }
};

template <int SZ = 1004>
struct HLD {  //树链剖分
  int N, Fa[SZ], HcHead[SZ], Dep[SZ], HcTail[SZ], HSon[SZ], Usz[SZ];
  int ID[SZ], segSz;
  vector<int> G[SZ];
  void init(int _n) {
    segSz = 0;
    N = _n;
    assert(_n < SZ);
  }
  int dfs(int u, int fa) {  //返回子树体积
    int &h = HSon[u], &sz = Usz[u];
    sz = 1, Fa[u] = fa, h = 0, Dep[u] = Dep[fa] + 1;
    for (size_t i = 0; i < G[u].size(); i++) {
      int v = G[u][i];
      if (v == fa) continue;
      sz += dfs(v, u);
      if (Usz[v] > Usz[h]) h = v;  //体积最大的子树
    }
    return sz;  // dfs得到重儿子，深度，父节点
  }
  void hld(int u, int fa, int head) {  //轻重剖分
    ID[u] = ++segSz, HcHead[u] = head;
    if (HSon[u]) {
      hld(HSon[u], u, head);  //重链向下扩展
      for (size_t i = 0; i < G[u].size(); i++) {
        int v = G[u][i];  //轻儿子新开重链
        if (v != fa && v != HSon[u]) hld(v, u, v);
      }
      return;
    }
    HcTail[head] = u;
  }
  void addEdge(int u, int v) { G[u].push_back(v); }
  void build(int root = 1) { dfs(root, 0), hld(root, 0, root); }
};

const int NN = 1e5 + 8;
SegTree<int, NN * 3> St;
HLD<NN> H;
const int Root = 1;
int queryRootPathSum(int u) {  //查询u到树根路径上所有点的权值之和
  int ans = 0;
  while (true) {
    int hu = H.HcHead[u];
    ans += St.querysum(H.ID[hu], H.ID[u]);
    if (hu == Root) break;
    u = H.Fa[hu];
  }
  return ans;
}
void setRootPath(int u) {  //设置u到树根路径上所有点的权值为1
  while (true) {
    int hu = H.HcHead[u];
    St.setV(H.ID[hu], H.ID[u], 1);
    if (hu == Root) break;
    u = H.Fa[hu];
  }
}
int querySubTreeSum(int u) {  //子树u的所有点权之和，所有点在DFS序中是连续的
  return St.querysum(H.ID[u], H.ID[u] + H.Usz[u] - 1);
}
void clearSubTree(int u) {  //设置子树u的所有点权为0
  St.setV(H.ID[u], H.ID[u] + H.Usz[u] - 1, 0);
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int N, Q;
  cin >> N, H.init(N + 1), St.init(N + 1);
  for (int u = 2, p; u <= N; u++) cin >> p, H.addEdge(p + 1, u);
  H.build(Root), cin >> Q;
  string s;
  for (int i = 0, x; i < Q; i++) {
    cin >> s >> x, ++x;
    if (s[0] == 'i') {  //安装 x
      int s0 = queryRootPathSum(x);
      setRootPath(x);
      cout << queryRootPathSum(x) - s0 << endl;
    } else {  //卸载 x
      int s0 = querySubTreeSum(x);
      clearSubTree(x);
      cout << s0 << endl;
    }
  }
  return 0;
}
// 46047267 软件包管理器 答案正确 100 392 12212 3644 C++ 2020-12-13 22:29:46
```

### 例题35  路径统计（Tree, POJ1741）

```cpp
// 例题35  路径统计（Tree, POJ1741）
// 陈锋
#include<cstdio>
#include<cassert>
#include<vector>
#include<algorithm>
#include<iterator>

using namespace std;
const int INF = 2147483647, MAXN = 10000 + 4;

struct Edge {
  int v, w;
  Edge(int _v, int _w): v(_v), w(_w) {}
};
int N, K;
vector<Edge> G[MAXN];
bool VIS[MAXN];

int get_size(int u, int fa) { // 子树u的体积
  assert(!VIS[u]);
  int ans = 1;
  for (size_t i = 0; i < G[u].size(); i++) {
    int v = G[u][i].v;
    if (v == fa || VIS[v]) continue;
    ans += get_size(v, u);
  }
  return ans;
}

// 给出子树u的大小，找出其重心
int find_centroid(int u, int fa, int usz, int &ch_sz, int &ct) {
  assert(!VIS[u]);
  int sz = 1, max_ch = -INF;
  for (size_t i = 0; i < G[u].size(); i++) {
    int v = G[u][i].v;
    if (v == fa || VIS[v]) continue;
    int chsz = find_centroid(v, u, usz, ch_sz, ct);
    sz += chsz, max_ch = max(max_ch, chsz);
  }
  max_ch = max(max_ch, usz - sz);
  if (max_ch < ch_sz) ch_sz = max_ch, ct = u;
  return sz;
}

int find_centroid(int u) { // 子树u的重心
  int ch_sz = INF, ct = -1, sz = get_size(u, -1);
  find_centroid(u, -1, sz, ch_sz, ct);
  assert(ct != -1 && ch_sz <= sz / 2);
  return ct;
}

// 收集子树u中所有到u的≤K的路径长度
void get_paths(int u, int fa, int plen, vector<int>& paths) {
  if (plen > K) return;
  paths.push_back(plen);
  for (size_t i = 0; i < G[u].size(); i++) {
    const Edge &e = G[u][i];
    if (e.v != fa && !VIS[e.v])
      get_paths(e.v, u, plen + e.w, paths);
  }
}

// 统计P中两个元素之和<=K的pair个数
inline int count_pairs(vector<int>& P) {
  sort(P.begin(), P.end());
  int ans = 0;
  for (int l = 0, r = P.size() - 1; ; l++) {
    while (r > l && P[r] + P[l] > K) r--;
    if (r <= l) break; // 双指针扫描法
    ans += r - l; // 减去同一颗子树v中的路径
  }
  return ans;
}

int solve(int u) { // 对子树u递归求解
  int ans = 0;
  vector<int> lens; // 所有合法的路径长度
  for (size_t i = 0; i < G[u].size(); i++) {
    const Edge &e = G[u][i];
    if (VIS[e.v]) continue;
    vector<int> ps; // u→子树v中点的所有路径
    get_paths(e.v, u, e.w, ps), ans -= count_pairs(ps);
    copy(ps.begin(), ps.end(), back_inserter(lens));
  }
  ans += count_pairs(lens) + lens.size(); // 从u出发的路径
  VIS[u] = true;
  for (size_t i = 0; i < G[u].size(); i++) {
    const Edge &e = G[u][i];
    if (!VIS[e.v]) ans += solve(find_centroid(e.v));
  }
  return ans;
}

int main() {
  while (scanf("%d%d", &N, &K) == 2 && (N || K)) {
    for (int i = 0; i <= N; i++) G[i].clear(), VIS[i] = false;
    for (int i = 0, u, v, w; i < N - 1; i++) {
      scanf("%d%d%d", &u, &v, &w), u--, v--;
      G[u].push_back(Edge(v, w)), G[v].push_back(Edge(u, w));
    }
    printf("%d\n", solve(find_centroid(0)));
  }
  return 0;
}
// Accepted 547ms 2004kB 2671 G++2020-01-3011:32:29
```

### 例题36  铁人比赛（Ironman Race in Treeland, ACM/ICPC Kuala Lumpur 2008, UVa12161）

```cpp
// 例题36  铁人比赛（Ironman Race in Treeland, ACM/ICPC Kuala Lumpur 2008, UVa12161）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;
struct Edge { int v, d, l; };
const int INF = 0x3f3f3f3f, MAXN = 3e4 + 10;
typedef map<int, int>::iterator MIT;

int N, M, MaxSub[MAXN], SZ[MAXN], VIS[MAXN], Dep[MAXN], Cost[MAXN];
// MaxSub[i]: 去除节点i后得到的森林中节点数最多的树的节点, SZ[u]：子树u的体积,
// Dep:长度，Cost: 路径的费用
vector<Edge> G[MAXN];
void find_center(int u, int fa, const int tree_sz, int& center) {  //找重心
  int &szu = SZ[u], &msu = MaxSub[u];
  szu = 1, msu = 0;
  for (const Edge& e : G[u]) {
    if (e.v == fa || VIS[e.v]) continue;
    find_center(e.v, u, tree_sz, center);
    szu += SZ[e.v], msu = max(msu, SZ[e.v]);
  }
  msu = max(msu, tree_sz - SZ[u]);
  if (MaxSub[center] > msu) center = u;
}

void insert_cd(map<int, int>& ps, int c, int d) {
  if (c > M) return;
  MIT it = ps.upper_bound(c);
  if (it == ps.begin() || (--it)->second < d) {  // 保证ps里面{费用:长度}同时递增
    ps[c] = d;               // (it-1)->c≤c，要求d>(it-1)->d才插入c:d
    it = ps.upper_bound(c);  // 对于所有的 it(it->c>c)，要求it->d>d，否则删除
    while (it != ps.end() && it->second <= d) ps.erase(it++);
  }
}

void collect_deps(int u, int fa, map<int, int>& ps) {  // 子树u节点路径的花费:长度
  SZ[u] = 1;
  insert_cd(ps, Cost[u], Dep[u]);
  for (const Edge& e : G[u]) {
    if (e.v == fa || VIS[e.v]) continue;
    Dep[e.v] = Dep[u] + e.l, Cost[e.v] = Cost[u] + e.d;
    collect_deps(e.v, u, ps), SZ[u] += SZ[e.v];
  }
}

void count(int u, int& max_len) {  // 计算经过子树u根结点的路径数
  map<int, int> ps, vps;           // u子树, v子树中的 费用:长度
  ps[0] = 0;
  for (const Edge& e : G[u]) {
    if (VIS[e.v]) continue;
    Dep[e.v] = e.l, Cost[e.v] = e.d;
    vps.clear(), collect_deps(e.v, u, vps);
    for (const pair<int, int>& p : vps) {
      MIT it = ps.upper_bound(M - p.first);
      if (it != ps.begin()) max_len = max(max_len, p.second + (--it)->second);
    }
    for (const pair<int, int>& p : vps) insert_cd(ps, p.first, p.second);
  }
}

void solve(int u, int& max_len) {
  count(u, max_len), VIS[u] = true;
  for (const Edge& e : G[u]) {
    if (VIS[e.v]) continue;
    int center = 0;
    find_center(e.v, u, SZ[e.v], center), solve(center, max_len);
  }
}

int main() {
  int T;
  scanf("%d", &T);
  for (int kase = 1; kase <= T; kase++) {
    scanf("%d%d", &N, &M);
    fill_n(VIS, N + 1, 0), MaxSub[0] = N;
    for (int i = 1; i <= N; i++) G[i].clear();
    for (int i = 1, u, v, d, l; i < N; i++) {
      scanf("%d%d%d%d", &u, &v, &d, &l);
      G[u].push_back({v, d, l}), G[v].push_back({u, d, l});
    }
    int center = 0, max_len = 0;
    find_center(1, -1, N, center);  // 找到初始的重心
    solve(center, max_len);         // 递归求解
    printf("Case %d: %d\n", kase, max_len);
  }
  return 0;
}
// Accepted 210ms 2797 C++ 5.3.0 2020-12-13 22:11:33 25843886
```

### 例题38 闪电的能量（Lightning Energy Report, ACM/ICPC Jakarta2010, UVa1674）

```cpp
// 例题38 闪电的能量（Lightning Energy Report, ACM/ICPC Jakarta2010, UVa1674）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)
typedef long long LL;

const int MAXN = 65536;
struct SegTree {
  int addv[MAXN * 4], N;
  void update(int o, int L, int R, int qL, int qR, int val) {
    if (qL <= L && R <= qR) {
      addv[o] += val;  //区间加上val
      return;
    }
    int M = (L + R) / 2;
    if (qL <= M) update(o << 1, L, M, qL, qR, val);         //覆盖左区间
    if (M < qR) update(o << 1 | 1, M + 1, R, qL, qR, val);  //覆盖右区间
  }

  void add(int qL, int qR, int val) { update(1, 1, N, qL, qR, val); }

  void init(int o, int L, int R) {  //初始化线段树
    addv[o] = 0;
    if (L == R) return;
    int M = (L + R) / 2;
    init(o << 1, L, M), init(o << 1 | 1, M + 1, R);
  }

  int query(int o, int L, int R, int qv, int val) {
    if (L == R) return val + addv[o];  //找到答案并且将答案返回
    int M = (L + R) >> 1;
    if (qv <= M) return query(o << 1, L, M, qv, val + addv[o]);  //答案在左区间
    return query(o << 1 | 1, M + 1, R, qv, val + addv[o]);  //答案在右区间
  }
};
// Fa[i]为i的父节点,HcHead[i]为i所在重链头,HSon[i]:i重儿子,SZ[i]:子树体积,ID[i]:i在线段树中序号
int Fa[MAXN], HcHead[MAXN], Depth[MAXN], HSon[MAXN], SZ[MAXN], ID[MAXN], intSz;

SegTree ST;
vector<int> G[MAXN];  //存储图
int dfs(int u, int fa) {  //第一次dfs, 得到每个节点的重儿子, 深度, 和父节点
  SZ[u] = 1, Fa[u] = fa, HSon[u] = 0, Depth[u] = Depth[fa] + 1;
  for (auto v : G[u]) {
    if (v == fa) continue;
    SZ[u] += dfs(v, u);
    if (SZ[v] > SZ[HSon[u]]) HSon[u] = v;  //重儿子为体积最大的子树
  }
  return SZ[u];
}
void hld(int u, int fa, int x) {  // 得到节点在线段树中标号及重链的标号
  ID[u] = ++intSz, HcHead[u] = x;  // 重链的标号为该重链最顶端的节点
  if (HSon[u])  // 先处理重链，保证剖分完之后每条重链中的标号是连续的
    hld(HSon[u], u, x);
  for (auto v : G[u])
    if (v != fa && v != HSon[u]) hld(v, u, v);
}

void addPath(int u, int v, int w) {
  while (true) {
    int hu = HcHead[u], hv = HcHead[v];
    if (hu == hv) break;  // 直到两点位于同一条重链才停止
    if (Depth[hu] < Depth[hv]) swap(u, v), swap(hu, hv);  // 更新h→head()
    ST.add(ID[hu], ID[u], w), u = Fa[hu];
  }
  if (Depth[u] < Depth[v]) swap(u, v);
  ST.add(ID[v], ID[u], w);  // 更新u->v
}
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T;
  cin >> T;
  for (int kase = 1, Q, N; kase <= T; kase++) {
    cin >> N;
    assert(N < MAXN);
    ST.N = N, ST.init(1, 1, N);
    for (int i = 1; i <= N; i++) G[i].clear();
    SZ[0] = 0, Depth[1] = 0;
    for (int i = 1, u, v; i < N; i++) {
      cin >> u >> v, u++, v++;
      G[u].push_back(v), G[v].push_back(u);
    }
    dfs(1, 1);
    intSz = 0;
    hld(1, 1, 1);
    cin >> Q;
    for (int i = 0, u, v, w; i < Q; i++) {
      cin >> u >> v >> w, u++, v++;
      addPath(u, v, w);
    }
    printf("Case #%d:\n", kase);
    for (int i = 1; i <= N; i++) printf("%d\n", ST.query(1, 1, N, ID[i], 0));
  }
  return 0;
}
// Accepted 140ms 2976 C++5.3.02020-12-1322:18:36 25843914
```

### 例题38 闪电的能量（Lightning Energy Report, ACM/ICPC Jakarta2010, UVa1674）

```cpp
// 例题38 闪电的能量（Lightning Energy Report, ACM/ICPC Jakarta2010, UVa1674）
// 基于LCA的树上差分解法, 陈锋
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 50000 + 4;

template <int SZ>
struct LCA {
  vector<int> G[MAXN];
  int N, L, Tin[MAXN], Tout[MAXN], UP[MAXN][18], timer;  // LCA相关
  void init(int _n) {
    N = _n, L = ceil(log2(N)), timer = 0;
    for (int i = 0; i <= N; i++) G[i].clear();
  }
  void addEdge(int u, int v) { G[u].push_back(v), G[v].push_back(u); }
  void dfs(int u, int fa = 0) {
    Tin[u] = ++timer, UP[u][0] = fa;
    for (int i = 1; i <= L; i++) UP[u][i] = UP[UP[u][i - 1]][i - 1];
    for (size_t i = 0; i < G[u].size(); i++)
      if (G[u][i] != fa) dfs(G[u][i], u);
    Tout[u] = ++timer;
  }

  bool isAncestor(int u, int v) { return Tin[u] < Tin[v] && Tout[v] < Tout[u]; }

  int lca(int u, int v) {
    if (u == v) return u;
    if (isAncestor(u, v)) return u;
    if (isAncestor(v, u)) return v;
    for (int i = L; i >= 0; --i)
      if (!isAncestor(UP[u][i], v)) u = UP[u][i];
    return UP[u][0];
  }
};

LCA<MAXN> lca;
int mark[MAXN], ans[MAXN];

int dfs_mark(int u, int fa) {
  int &a = ans[u];
  a = mark[u];
  for (size_t i = 0; i < lca.G[u].size(); i++) {
    int v = lca.G[u][i];
    if (v == fa) continue;
    a += dfs_mark(v, u);
  }
  return a;
}

int main() {
  int T;
  cin >> T;
  for (int kase = 1, N, Q, x, y; kase <= T; kase++) {
    cin >> N, lca.init(N);
    for (int i = 1; i < N; i++) cin >> x >> y, lca.addEdge(x, y);
    lca.dfs(0);
    cin >> Q;
    fill_n(mark, N + 1, 0);
    for (int i = 0, c; i < Q; i++) {
      cin >> x >> y >> c;
      int d = lca.lca(x, y), pd = lca.UP[d][0];
      mark[x] += c, mark[y] += c, mark[d] -= c;
      if (pd != d) mark[pd] -= c;
    }
    dfs_mark(0, 0);
    printf("Case #%d:\n", kase);
    for (int i = 0; i < N; i++) printf("%d\n", ans[i]);
  }
}
// Accepted 130ms 1932 C++5.3.0 2020-12-13 22:25:38 25843936
```

## 3.8 动态树与LCT

### 例题43  大厨和图上查询（Chef and Graph Queries，Codechef GERALD 07）

```cpp
// 例题43  大厨和图上查询（Chef and Graph Queries，Codechef GERALD 07）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

template <int SZ>
struct LCT {
  int ch[SZ][2], fa[SZ], minw[SZ];  // 最小点权
  bool rev[SZ];
  inline int& ls(int x) { return ch[x][0]; }
  inline int& rs(int x) { return ch[x][1]; }
  inline void reverse(int x) { rev[x] ^= 1, swap(ls(x), rs(x)); }
  inline void maintain(int x) {
    minw[x] = min(x, min(minw[ls(x)], minw[rs(x)]));
  }
  inline void pushdown(int x) {
    if (rev[x]) reverse(ls(x)), reverse(rs(x)), rev[x] = false;
  }
  inline bool isroot(int x) { return ls(fa[x]) != x && rs(fa[x]) != x; }
  inline int isright(int x) {
    return rs(fa[x]) == x;
  }  // x是Splay上父亲的右儿子?
  void rotate(int x) {
    int y = fa[x], z = fa[y], k = isright(x), &t = ch[x][k ^ 1];
    if (!isroot(y)) ch[z][isright(y)] = x;  // x,y在z的同一侧
    ch[y][k] = t, fa[t] = y;  // 设置y,t之间的关系，x,t都在y的同一侧
    t = y, fa[y] = x, fa[x] = z;  // x-y, y-t方向相反
    maintain(y), maintain(x);
  }
  void pushup(int x) {
    if (!isroot(x)) pushup(fa[x]);
    pushdown(x);
  }
  void splay(int x) {
    pushup(x);
    while (!isroot(x)) {
      int y = fa[x];
      if (!isroot(y)) rotate(isright(y) == isright(x) ? x : y);
      rotate(x);
    }
  }
  void access(int x) {
    for (int t = 0; x; t = x, x = fa[x]) splay(x), rs(x) = t, maintain(x);
  }
  void makeroot(int x) { access(x), splay(x), reverse(x); }
  void link(int x, int y) { makeroot(x), fa[x] = y; }
  void cut(int x, int y) {
    makeroot(x), access(y), splay(y);
    ls(y) = fa[x] = 0;
    maintain(y);
  }
  void split(int x, int y) { makeroot(x), access(y), splay(y); }
  int findroot(int x) {
    access(x), splay(x);
    while (ls(x)) pushdown(x), x = ls(x);
    splay(x);
    return x;
  }
  void init(int sz) {
    minw[0] = 1e9;
    assert(sz < SZ);
    for (int i = 1; i <= sz; i++)  // LCT初始化, m+n?
      minw[i] = i, ch[i][0] = ch[i][1] = fa[i] = 0, rev[i] = 0;
  }
};

template <int SZ>
struct BIT {
  int C[SZ], n;
  void init(int sz) { assert(sz + 1 < SZ), fill_n(C, sz + 1, 0), this->n = sz; }
  inline int lowbit(int x) { return x & -x; }
  void add(int x, int v) {
    while (x <= n) C[x] += v, x += lowbit(x);
  }
  int sum(int x) {
    int ret = 0;
    while (x) ret += C[x], x -= lowbit(x);
    return ret;
  }
};
const int NN = 2e5 + 4;
BIT<NN> S;
LCT<NN * 2> lct;
int QL[NN], Ans[NN], EU[NN], EV[NN];
vector<int> EQ[NN];

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T;
  cin >> T;
  for (int t = 0, n, m, q; t < T; t++) {
    cin >> n >> m >> q;
    for (int i = 1; i <= m; i++) {
      int &u = EU[i], &v = EV[i];
      cin >> u >> v, u += m, v += m, EQ[i].clear();
    }
    S.init(m), lct.init(m + n);
    for (int i = 1, qr; i <= q; i++) cin >> QL[i] >> qr, EQ[qr].push_back(i);
    for (int i = 1; i <= m; i++) {
      int u = EU[i], v = EV[i];
      if (lct.findroot(u) == lct.findroot(v)) {  // u,v已经联通
        lct.split(u, v);
        int e = lct.minw[v];  // v所在分量的最小边权
        if (e < i) {          // 边i比x大，删除x
          lct.cut(e, EU[e]), lct.cut(e, EV[e]), S.add(e, -1);  // 删除边x
          lct.link(i, u), lct.link(i, v), S.add(i, 1);         // 加入边i
        }
      } else
        lct.link(u, i), lct.link(v, i), S.add(i, 1);  // 加入边i

      for (size_t xi = 0; xi < EQ[i].size(); xi++)
        Ans[EQ[i][xi]] = n - (S.sum(i) - S.sum(QL[EQ[i][xi]] - 1));
    }
    for (int i = 1; i <= q; i++) cout << Ans[i] << endl;
  }
  return 0;
}
// 40407264	sukhoeing 0.62 33.4M C++14
```

### 例题44  大象（Elephants, Codechef ELPHANT, IOI 2011 Day 2）

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

### NC20311 例题41  洞穴勘测（Cave, SDOI2008）

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
  // x是辅助树上父亲的右儿子?
  inline int is_right_ch(int x) { return ch[fa[x]][1] == x; }
  // x是辅助树根?
  inline int is_root(int x) { return ch[fa[x]][0] != x && ch[fa[x]][1] != x; }
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
  void rotate_up(int x) {  // 将x向上旋转一级
    int y = fa[x], z = fa[y], chx = is_right_ch(x), chy = is_right_ch(y),
        &t = ch[x][chx ^ 1];  // t在x,y之间，但是t-x, x-y方向相反
    fa[x] = z;
    if (!is_root(y)) ch[z][chy] = x;              // x,y在z的同一侧
    ch[y][chx] = t, fa[t] = y, t = y, fa[y] = x;  // 保证t依然在x,y之间
  }
  void splay(int x) {
    pushup(x);  // x一直到树根路径上所有点的深度相对关系都要反转
    for (int f = fa[x]; f = fa[x], !is_root(x); rotate_up(x))
      if (!is_root(f)) rotate_up(is_right_ch(x) == is_right_ch(f) ? f : x);
  }
  void access(int x) {  // 将root-x变成首选边
    for (int f = 0; x; f = x, x = fa[x]) splay(x), ch[x][1] = f;
  }
  void make_root(int x) {  // 将x变为树根
    access(x), splay(x), swap(ch[x][0], ch[x][1]), rev[x] ^= 1;
  }
  void split(int x, int y) { make_root(x), access(y), splay(y); }
  int find_root(int x) {  // x所在树的树根
    access(x), splay(x);
    while (ch[x][0]) x = ch[x][0];
    splay(x);
    return x;
  }
  void cut(int x, int y) {
    split(x, y);  // x是y在辅助树中的左孩子且要求x,y相邻
    if (ch[y][0] == x && !ch[x][1]) ch[y][0] = fa[x] = 0;
  }

  void link(int x, int y) {
    if (find_root(x) != find_root(y)) make_root(x), fa[x] = y;
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

### 例题42  快乐涂色（Happy Painting, UVa11994）

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

## 3.9 离线算法

### 例题48 金币（Coins, ACM/ICPC Asia – Amritapuri 2015，Codechef AMCOINS）

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

### 例题46  公交路线（Bus Routes, ACM/ICPC Asia-Hefei 2015, HDU5552）

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

### 例题45  动态逆序对（CQOI2011）

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
LL Ans[NN];  //第id个命令插入x之后增加多少个逆序对
void solve(int l, int r) {  // 按照插入位置从大到小排序
  if (l == r) return;
  int m = (l + r) / 2, l1 = l, l2 = m + 1;
  for (int i = l; i <= r; i++) {  //情况1
    const OP &o = O[i];
    if (o.id <= m) S.add(o.v, 1);  // id ∈ [l,m]
    else Ans[o.id] += S.sum(o.v);  // id ∈ [m + 1,r]
  }
  for (int i = l; i <= r; i++)
    if (O[i].id <= m) S.add(O[i].v, -1);  //还原BIT
  for (int i = r; i >= l; --i) {          //情况2
    const OP &o = O[i];
    if (o.id <= m)
      S.add(N - o.v + 1, 1);  // id∈[l,m],记录插入的N–v+1≥v的元素个数
    else
      Ans[o.id] += S.sum(N - o.v + 1);
    // id ∈ [m + 1,r],v映射到N – v + 1,比如N -> 1,N – 1 -> 2
  }

  for (int i = l; i <= r; i++) {  //分治：把id∈[l,m]，[m+1,r]的操作分别放两边
    const OP &o = O[i];
    if (o.id <= m) T[l1++] = o, S.add(N - o.v + 1, -1);  //还原BIT
    else T[l2++] = o;
  }
  copy(T + l, T + r + 1, O + l);
  solve(l, m), solve(m + 1, r);
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

### 例题50  数颜色（牛客NC202003）

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

### 例题49 D-查询（SPOJ DQUERY）

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

### 例题47 流星（Meteors，POI2011，SPOJ METEORS）

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
void solve(const vector<int>& C, int l, int r) {
  if (C.empty()) return;
  if (l == r) { // 答案的目标区间确定了
    for (int c : C) Ans[c] = l;
    return;
  }
  int m = (l + r) / 2;
  _rep(ai, l, m) apply(Rs[ai]); // 看看[l,m]中的下的雨够不够
  vector<int> LC, RC;
  for (int c : C) { // 每个国家都看看
    int &p = P[c];
    LL x = 0;
    for (int s : St[c]) if ((x += S.sum(s)) >= p) break; // 收集够了?
    if (p <= x) LC.push_back(c); // 答案在[l,m]中，国家分到左边
    else p -= x, RC.push_back(c); // 答案在[m+1,r]中，国家分到右边
  }
  _rep(ai, l, m) apply(Rs[ai], true); // 看看[l,m]中的下的雨够不够-还原
  solve(LC, l, m), solve(RC, m + 1, r); //更改顺序，整体二分
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

## 3.10 kd-Tree

### 例题51  寻找酒店（Finding Hotels, ACM/ICPC 青岛 2016, LA7744/HDU5992

```cpp
// 例题51  寻找酒店（Finding Hotels, ACM/ICPC 青岛 2016, LA7744/HDU5992
// 陈锋
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

### 例题52  保持健康（Keep Fit! UVa12939）

```cpp
// 例题52  保持健康（Keep Fit! UVa12939）
// 陈锋
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

## 3.11 可持久化数据结构

### 例题55  树上异或（Tree, ACM/ICPC 2013南京在线赛, HDU4757）

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

### 例题56  网格监控（Grid surveillance, IPSC 2011）

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

### 例题54  树上计数（Count on a tree, SPOJ COT）

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

### 例题53  区间第K小查询（K-th Number, SPOJ MKTHNUM）

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

### 例题57  自带版本控制功能的IDE（Version Controlled IDE, ACM/ICPC Hatyai 2012, UVa12538）

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

### 例题57  自带版本控制功能的IDE（Version Controlled IDE, ACM/ICPC Hatyai 2012, UVa12538）

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
