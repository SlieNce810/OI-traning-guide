# 3.5 字符串（3）

## 例题25  转世（Reincarnation HDU4622）

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

## 例题28  第K次出现（Kth-occurrence, HDU6704, CCPC 2019网络选拔赛）

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

## 例题27  子串之和（str2int, Asia – Tianjin 2012, LA6387/UVa1673）

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

## 例题22  最小循环串（Glass Beads, SPOJ BEADS）

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

## 例题24  最长公共子串（Longest Common Substring, SPOJ LCS）

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

## 例题26  子串计数（Substrings, SPOJ NSUBSTR）

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

## 例题23 不同的子串（New Distinct Substrings, SPOJ SUBST1）

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
