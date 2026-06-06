# 3.2 区间信息的维护与查询

## 例题7  乒乓比赛（Ping pong, Beijing 2008, LA4329）

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

## 例题11  山脉（Mountains, IOI05, SPOJ NKMOU）

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

## 例题8  频繁出现的数值（Frequent Values, UVa 11235）

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

## 例题10  快速矩阵操作（Fast Matrix Operations, UVa 11992）

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

## 例题12  堆内存管理器（Heap Manager, UVa12419）

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

## 例题9  动态最大连续和（Ray, Pass me the Dishes, UVa1400）

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
