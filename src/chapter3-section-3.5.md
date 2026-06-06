# 3.5 字符串（3）

## 例题25  转世（Reincarnation HDU4622）

### 题目描述
给定一个字符串S，有Q个查询，每个查询给出区间[L, R]（1-based），问该子串中**有多少个不同的子串**（本质不同子串数）。

- **输入格式**：T组数据。每组：一行S，一行Q，Q行每行L R。
- **输出格式**：每组Q行回答。
- **约束**：|S| ≤ 2000, Q ≤ 10000。

### 解题思路
由于S长度很小（2000），可以预处理所有O(N²)个答案。对每个起始位置i，建立从位置i开始的后缀自动机（SAM）。逐个插入字符，利用SAM的性质计算新增的本质不同子串数：`新节点len - link节点len = 新增子串数`。`F[i][j]`表示子串S[i..j]中的本质不同子串数。

### 算法方法
**后缀自动机（Suffix Automaton, SAM）**：每个子串对应SAM中从初始状态出发的一条路径。本质不同子串数 = Σ(len[u] - len[link[u]])。以每个位置为起点构建SAM，在线的增量构建配合前缀和实现O(N²)预处理。

### 复杂度分析
- **时间复杂度**：O(N²)预处理 + O(Q)查询。对每个起始位置建SAM，单次插入O(1)均摊。
- **空间复杂度**：O(N²)，存储F表（2000×2000）。

```cpp
// 例题25  转世（Reincarnation HDU4622）
// 陈锋
// 题目：查询任意区间[L,R]内本质不同的子串个数
// 算法：对每个起点建SAM，利用 len[u]-len[link[u]] 统计新增不同子串
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
    len[last = cur] = len[p] + 1;  // 新节点的maxlen = 父节点maxlen + 1
    // 沿link链设置转移
    while (p != -1 && !next[p][x]) next[p][x] = cur, p = link[p];
    if (p == -1) { link[cur] = 0; return; }
    int q = next[p][x];
    if (len[p] + 1 == len[q]) { link[cur] = q; return; }
    // 需要分裂节点：创建克隆节点nq
    int nq = new_node();
    isClone[nq] = 1;
    copy_n(next[q], SIG, next[nq]);
    link[nq] = link[q], len[nq] = len[p] + 1, link[cur] = link[q] = nq;
    while (p >= 0 && next[p][x] == q) next[p][x] = nq, p = link[p];
  }
  inline void build(const char* s) { while (*s) insert(*s++); }
};

const int NN = 2000 + 4;
Suffix_Automaton<2 * NN> sam;
int F[NN][NN];  // F[i][j] = S[i..j]中本质不同子串个数

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
        // 新增的不同子串数 = len[新节点] - len[link[新节点]]
        F[i][j] = F[i][j - 1] + sam.len[p] - sam.len[sam.link[p]];
      }
    }
    int Q, l, r; cin >> Q;
    _for(i, 0, Q) { cin >> l >> r; cout << F[l - 1][r - 1] << endl; }
  }
  return 0;
}
// Accepted 1076ms 18576kB 1780 G++ 2019-09-26 23:54:34
```

## 例题28  第K次出现（Kth-occurrence, HDU6704, CCPC 2019网络选拔赛）

### 题目描述
给定字符串S（1-indexed），Q个查询 (l, r, k)：求子串 S[l..r] 在S中**第k次出现**的起始位置。若出现次数不足k次，输出-1。

- **输入格式**：T组数据。每组：N Q（|S|和查询数），S（字符串），Q行每行 l r k。
- **输出格式**：每组Q行答案。
- **约束**：|S|, Q ≤ 10^5。

### 解题思路
**SAM + 权值线段树合并 + 倍增**：
1. **SAM构建**：构建字符串S的SAM，记录每个字符插入时对应SAM中的节点（end_pos数组）。
2. **parent树构建**：对SAM的link边构建树结构（后缀树），在树上的每个节点挂一个权值线段树记录endpos集合。
3. **线段树合并**：自底向上合并权值线段树，每个SAM节点对应一个线段树，维护该等价类在S中的所有出现位置。
4. **查询处理**：
   - 定位子串对应的SAM节点：从end_pos[r]出发，沿倍增数组向上跳到len≥(r-l+1)的最高节点
   - 在线段树中查询第k小的endpos值作为答案
5. 注意答案需调整为起始位置：`ans - (r-l)`。

### 算法方法
**后缀自动机（SAM）+ 动态开点权值线段树合并 + 倍增（Binary Lifting）**：SAM用于管理子串等价类。线段树合并用于合并endpos集合（处理出现位置）。倍增用于从子串终点位置快速定位到对应SAM节点。

### 复杂度分析
- **时间复杂度**：O((N+Q) log N)，SAM构建O(N)，线段树合并O(N log N)，每次查询O(log N)。
- **空间复杂度**：O(N log N)，SAM节点≈2N，线段树节点≈N log N。

```cpp
// 例题28  第K次出现（Kth-occurrence, HDU6704）
// 陈锋
// 题目：查询子串S[l..r]在原串中第k次出现的起始位置
// 算法：SAM + 权值线段树合并(维护endpos) + 倍增查找对应节点
#include<bits/stdc++.h>
using namespace std;
const int NN = 1e6 + 10;

// 动态开点权值线段树
template<int SZ>
struct WSegTree {
  int sz, ls[SZ * 4], rs[SZ * 4], sum[SZ * 4];
  void init() { sz = 0; }
  int maintain(int u) { sum[u] = sum[ls[u]] + sum[rs[u]]; return u; }
  int new_node() { ++sz; sum[sz] = ls[sz] = rs[sz] = 0; return sz; }

  void insert(int& u, int l, int r, int k) {  // 在位置k插入
    if (u == 0) u = new_node();
    if (l == r) { sum[u]++; return; }
    int m = (l + r) / 2;
    if (k <= m) insert(ls[u], l, m, k);
    else insert(rs[u], m + 1, r, k);
    maintain(u);
  }

  int merge(int x, int y) {  // 合并两棵线段树
    if (x == 0 || y == 0) return x + y;
    int p = new_node();
    ls[p] = merge(ls[x], ls[y]), rs[p] = merge(rs[x], rs[y]);
    return maintain(p);
  }

  int kth(int u, int l, int r, int k) {  // 查询第k小的值
    if (l == r) return l;
    int m = (l + r) / 2, lc = ls[u], rc = rs[u];
    if (k <= sum[lc]) return kth(lc, l, m, k);
    if (k <= sum[u]) return kth(rc, m + 1, r, k - sum[lc]);
    return -1;  // 不足k个
  }
};

struct Edge { int to, next; };

template<int SZ>
struct SAM {
  WSegTree<SZ> st;
  int sz, last, len[SZ], link[SZ], ch[SZ][30], end_pos[SZ];
  int seg_root[SZ], fa[SZ][30], ecnt, EHead[SZ];
  Edge E[SZ * 2];

  void init() { last = 1, ecnt = 0, sz = 0; new_stat(), st.init(); }
  int new_stat() {
    int q = ++sz;
    EHead[q] = 0, len[q] = 0, link[q] = 0, seg_root[q] = 0;
    fill_n(ch[q], 30, 0);
    return q;
  }

  void insert(int i, int c, int n) {  // 插入字符c（位置i）
    int cur = new_stat(), p = last;
    end_pos[i] = cur, len[cur] = i;
    for (; p && !ch[p][c]; p = link[p]) ch[p][c] = cur;
    if (!p) link[cur] = 1;
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
    st.insert(seg_root[cur], 1, n, i);  // 在endpos集合中插入位置i
  }

  void add_edge(int x, int y) { E[++ecnt] = {y, EHead[x]}, EHead[x] = ecnt; }

  void dfs(int u) {  // 倍增预处理 + 线段树合并
    for (int i = 1; i <= 20; ++i) fa[u][i] = fa[fa[u][i - 1]][i - 1];
    for (int i = EHead[u]; i; i = E[i].next) {
      int v = E[i].to;
      fa[v][0] = u;
      dfs(v);
      seg_root[u] = st.merge(seg_root[u], seg_root[v]);  // 合并子树的endpos
    }
  }

  void build() {
    for (int i = 2; i <= sz; ++i) add_edge(link[i], i);
    dfs(1);
  }

  int kth(int l, int r, int k, int n) {  // 查询子串S[l..r]的第k次出现
    int u = end_pos[r];
    // 倍增跳祖先：找到len>=子串长度的最高节点
    for (int i = 20; i >= 0; --i) {
      int p = fa[u][i];
      if (l + len[p] - 1 >= r) u = p;
    }
    int ans = st.kth(seg_root[u], 1, n, k);
    return (ans == -1) ? ans : ans - (r - l);  // 转为起始位置
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
    while (q--) { scanf("%d%d%d", &l, &r, &k); printf("%d\n", sam.kth(l, r, k, N)); }
  }
  return 0;
}
// Accepted 1684ms 92092kB 3271 G++2019-12-09 21:34:42 31813560
```

## 例题27  子串之和（str2int, Asia – Tianjin 2012, LA6387/UVa1673）

### 题目描述
给定N个数字字符串，将这些字符串中的所有非空前导零不含法的子串转为整数，求所有不同子串对应的整数之和（模2012）。前导零不含法指子串不以'0'开头（除了单个'0'）。

- **输入格式**：多组数据，N=0结束。每组：N，N行每行一个数字字符串。
- **输出格式**：每组一行结果。
- **约束**：N ≤ 10000，每个串长度 ≤ 1000。

### 解题思路
使用**广义SAM + DP**：
1. **广义SAM**：将多个字符串插入同一个SAM，字符串间用特殊字符（'9'+1）分隔，避免跨串子串。
2. **拓扑排序DP**：按len排序，对每个节点u：
   - `Cnt[u]`：以u为终点的不同路径数（即子串个数）
   - `Sum[u]`：以u为终点的所有子串的数值和
   - 从节点u向子节点v转移时：`Cnt[v] += Cnt[u]`, `Sum[v] += Sum[u]*10 + digit*Cnt[u]`
3. 注意根节点(0)不能以'0'开始转移（避免前导零）。

### 算法方法
**广义后缀自动机 + 拓扑DP**：将多串插入SAM，利用len数组进行拓扑排序，从短到长DP累加子串数值和。

### 复杂度分析
- **时间复杂度**：O(总字符串长度 × SIGMA)。
- **空间复杂度**：O(总字符串长度)，SAM节点数≤2×总长。

```cpp
// 例题27  子串之和（str2int, LA6387/UVa1673）
// 陈锋
// 题目：所有不同子串（除去前导零）的数值和，模2012
// 算法：广义SAM + 拓扑DP统计Cnt和Sum
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
    int nd = sz++; next[nd].clear(), link[nd] = -1, len[nd] = 0; return nd;
  }
  inline void insert(char x) {
    int p = last, cur = new_node(); len[last = cur] = len[p] + 1;
    while (p != -1 && !next[p].count(x)) next[p][x] = cur, p = link[p];
    if (p == -1) { link[cur] = 0; return; }
    int q = next[p][x];
    if (len[p] + 1 == len[q]) { link[cur] = q; return; }
    int nq = new_node(); next[nq] = next[q];
    link[nq] = link[q], len[nq] = len[p] + 1, link[cur] = link[q] = nq;
    while (p >= 0 && next[p][x] == q) next[p][x] = nq, p = link[p];
  }
  inline void build(const char* s) { while (*s) insert(*s++); }
};

typedef long long LL;
const int NS = 2e5 + 4, M = 2012;
Suffix_Automaton<NS> sam;
int V[NS], Cnt[NS], Sum[NS];  // V: 拓扑序, Cnt: 子串数, Sum: 子串数值和

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  string s; int N;
  while (cin >> N && N) {
    sam.init();
    _for(i, 0, N) {
      cin >> s, sam.build(s.c_str());
      if (i != N - 1) sam.insert('9' + 1);  // 分隔符
    }
    _for(i, 0, sam.sz) V[i] = i;
    sort(V, V + sam.sz, [](int a, int b) { return sam.len[a] < sam.len[b]; });
    fill_n(Cnt, sam.sz, 0), fill_n(Sum, sam.sz, 0);
    Cnt[0] = 1; int ans = 0;
    _for(i, 0, sam.sz) {
      int u = V[i];
      char st = u ? '0' : '1';  // 根节点跳过'0'避免前导零
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

### 题目描述
给定一个字符串S的循环表示，求其**字典序最小的循环表示**的起始位置（1-based）。循环表示指将字符串首尾相连后，从任意位置开始的|S|个字符。

- **输入格式**：T组数据。每组一行字符串S（仅小写字母）。
- **输出格式**：每组一个整数，最小循环表示的起始位置。
- **约束**：|S| ≤ 10000。

### 解题思路
将字符串S重复一次得到SS，问题转化为求SS的长度为|S|的字典序最小子串的起始位置。分析SS的长度为|S|的字典序最小子串必须在第一个S内（否则可以向左移|S|位得到更小的）。因此只需在SS的前|S|个后缀中找字典序最小的。

使用**后缀自动机**：将SS插入SAM，从根节点出发，重复|S|次：每次选择字典序最小的转移边（map::begin()），沿途跟踪len。最终 `len[当前节点] - |S| + 1` 即为起始位置。

### 算法方法
**后缀自动机（SAM）**：利用SAM中从根节点贪心选择最小字符的转移边来找到字典序最小的子串。map保证了转移边的有序性。

### 复杂度分析
- **时间复杂度**：O(|S|)，SAM构建和贪心行走均为线性。
- **空间复杂度**：O(|S| × 转移数)，约O(2|S| * log|Σ|)。

```cpp
// 例题22  最小循环串（Glass Beads, SPOJ BEADS）
// 陈锋
// 题目：求字符串最小循环表示的起始位置
// 算法：构建SS的SAM，从根贪心走最小字符边，行走|S|步
#include <bits/stdc++.h>
using namespace std;

#define _for(i,a,b) for( int i=(a); i<(int)(b); ++i)
#define _rep(i,a,b) for( int i=(a); i<=(int)(b); ++i)

template<int SZ, int SIG = 32>
struct Suffix_Automaton {
  int link[SZ], len[SZ], last, sz;
  map<char, int> next[SZ];  // map保证转移边有序（字典序）
  inline void init() { sz = 0, last = new_node(); }
  inline int new_node() {
    assert(sz + 1 < SZ);
    int nd = sz++; next[nd].clear(), link[nd] = -1, len[nd] = 0; return nd;
  }
  inline void insert(char x) {
    int p = last, cur = new_node(); len[last = cur] = len[p] + 1;
    while (p != -1 && !next[p].count(x)) next[p][x] = cur, p = link[p];
    if (p == -1) { link[cur] = 0; return; }
    int q = next[p][x];
    if (len[p] + 1 == len[q]) { link[cur] = q; return; }
    int nq = new_node(); next[nq] = next[q];
    link[nq] = link[q], len[nq] = len[p] + 1, link[cur] = link[q] = nq;
    while (p >= 0 && next[p][x] == q) next[p][x] = nq, p = link[p];
  }
  inline void build(char* s) { while (*s) insert(*s++); }
};

typedef long long LL;
const int NN = 10000 + 4;
char S[NN];
Suffix_Automaton<NN * 4> sam;  // SS 需要4倍空间

int main() {
  int T; scanf("%d", &T);
  while (T--) {
    scanf("%s", S);
    sam.init(), sam.build(S), sam.build(S);  // 将S插入两次 = SS
    int p = 0, N = strlen(S);
    for (int i = 0; i < N; i++)  // 贪心行走N步，每次选最小字符
      p = sam.next[p].begin()->second;  // map::begin()返回最小字符的转移
    printf("%d\n", sam.len[p] - N + 1);  // 起始位置 = 当前长度 - N + 1
  }
  return 0;
}
// 2594177 Glass Beads Accepted  C++11 0.452 2019-09-26 04:30:13
```

## 例题24  最长公共子串（Longest Common Substring, SPOJ LCS）

### 题目描述
给定两个字符串S和T，求它们的最长公共子串（LCS，连续的公共子串，不是子序列）。

- **输入格式**：两行，每行一个字符串（仅小写字母）。
- **输出格式**：一个整数，最长公共子串的长度。
- **约束**：|S|, |T| ≤ 250000。

### 解题思路
使用**后缀自动机**解决：
1. **构建SAM(T)**：将第二个字符串T插入SAM。
2. **匹配过程**：遍历S的每个字符c，在SAM中维护当前状态p和当前匹配长度l：
   - 若p有转移c：`p = next[p][c]`, `l += 1`
   - 否则沿link链回溯，直到找到有转移c的节点或回到根节点。若找到：`l = len[p] + 1`, `p = next[p][c]`；若找不到：`p = 0, l = 0`
3. 匹配过程中维护 `ans = max(ans, l)`。

### 算法方法
**后缀自动机（SAM）**：将一个字符串建SAM，另一个字符串在SAM上匹配，维护当前最长匹配长度。利用link链加速失配回溯。

### 复杂度分析
- **时间复杂度**：O(|S| + |T|)，SAM构建和匹配均为线性。
- **空间复杂度**：O(|T| × |Σ|)，约O(2|T| × 26)。

```cpp
// 例题24  最长公共子串（Longest Common Substring, SPOJ LCS）
// 陈锋
// 题目：求两个字符串的最长公共子串长度
// 算法：对T建SAM，在SAM上匹配S，维护当前最长匹配长度
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
  inline int new_node() { assert(sz + 1 < SZ); int nd = sz++; next[nd].clear(), link[nd] = -1, len[nd] = 0; return nd; }
  inline void insert(char x) {
    int p = last, cur = new_node(); len[last = cur] = len[p] + 1;
    while (p != -1 && !next[p].count(x)) next[p][x] = cur, p = link[p];
    if (p == -1) { link[cur] = 0; return; }
    int q = next[p][x];
    if (len[p] + 1 == len[q]) { link[cur] = q; return; }
    int nq = new_node(); next[nq] = next[q];
    link[nq] = link[q], len[nq] = len[p] + 1, link[cur] = link[q] = nq;
    while (p >= 0 && next[p][x] == q) next[p][x] = nq, p = link[p];
  }
  inline void build(char* s) { while (*s) insert(*s++); }
};

const int NN = 5e5 + 5;
Suffix_Automaton<NN> sam;

// 计算字符串s在SAM上的最长匹配长度
int lcs(char* s) {
  int p = 0, l = 0, ans = 0;
  map<char, int>* nxt = sam.next;
  while (*s) {
    char x = *s++;
    if (nxt[p].count(x)) p = nxt[p][x], l++;  // 可以直接转移
    else {
      while (p != -1 && !nxt[p].count(x)) p = sam.link[p];  // 沿link链回溯
      if (p != -1) l = sam.len[p] + 1, p = nxt[p][x];  // 找到转移
      else p = 0, l = 0;  // 回到根节点
    }
    ans = max(ans, l);
  }
  return ans;
}

char S[NN];
int main() {
  scanf("%s", S); sam.init(), sam.build(S);  // 对第一个串建SAM
  scanf("%s", S);
  printf("%d", lcs(S));  // 第二个串在SAM上匹配
  return 0;
}
// 24466222 2019-09-26 14:53:40 Feng Chen Longest Common Substring  accepted 0.25  56M CPP14
```

## 例题26  子串计数（Substrings, SPOJ NSUBSTR）

### 题目描述
给定一个字符串S（长度N）。对每个长度L（1≤L≤N），求在S中**出现次数最多的、长度为L的子串**的出现次数。即 `F[L] = max{出现次数 | 子串长度=L}`。

- **输入格式**：一行字符串S（仅小写字母）。
- **输出格式**：N行，第i行为F[i]。
- **约束**：|S| ≤ 250000。

### 解题思路
使用**后缀自动机 + parent树DP**：
1. **SAM构建**：插入时非克隆节点的`isterminal[u]=1`（表示该节点对应某个前缀的终点）。
2. **parent树DP**：对link边构成的树做DFS，每个节点的endpos大小 = 自身isterminal + 所有子节点的endpos大小之和。endpos大小即该等价类中字符串的出现次数。
3. **更新F数组**：`F[len[u]] = max(F[len[u]], endpos_size[u])`。注意还需要从大到小传递：`F[i] = max(F[i], F[i+1])`，因为较长的子串出现次数≤较短子串的出现次数（后缀性质）。

### 算法方法
**后缀自动机（SAM）+ 树形DP**：利用SAM的link树（parent树）统计各等价类的endpos集合大小。F数组利用SAM的len信息记录不同长度子串的最大出现次数。

### 复杂度分析
- **时间复杂度**：O(N)，SAM构建O(N)，DFS O(N)。
- **空间复杂度**：O(N × 26)，约2N×26。

```cpp
// 例题26  子串计数（Substrings, SPOJ NSUBSTR）
// 陈锋
// 题目：对每个长度L，求出现次数最多的长度L子串的出现次数
// 算法：SAM + parent树DFS统计endpos大小
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
    len[last = cur] = len[p] + 1;
    isterminal[cur] = 1;  // 标记为原字符串前缀的终点（非克隆节点）
    while (p != -1 && !next[p][x]) next[p][x] = cur, p = link[p];
    if (p == -1) { link[cur] = 0; return; }
    int q = next[p][x];
    if (len[p] + 1 == len[q]) { link[cur] = q; return; }
    int nq = new_node();  // 克隆节点：非前缀终点
    copy_n(next[q], SIG, next[nq]);
    link[nq] = link[q], len[nq] = len[p] + 1, link[cur] = link[q] = nq;
    while (p >= 0 && next[p][x] == q) next[p][x] = nq, p = link[p];
  }
  inline void build(const char* s) { while (*s) insert(*s++); }
};

const int NN = 250000 + 4;
vector<int> G[NN * 2];  // parent树的邻接表
Suffix_Automaton<NN * 2> sam;
int F[NN];  // F[L] = 长度L子串的最大出现次数

// DFS统计每个节点的endpos大小（出现次数）
int dfs(int u) {
  int s = sam.isterminal[u];  // 自身贡献
  for (auto v : G[u]) s += dfs(v);  // 累加所有子节点贡献
  F[sam.len[u]] = max(F[sam.len[u]], s);  // 更新对应长度的最大值
  return s;
}

char S[NN];
int main() {
  scanf("%s", S); int N = strlen(S);
  sam.init(), sam.build(S);
  // 构建parent树（link边的反向）
  _for(u, 1, sam.sz) G[sam.link[u]].push_back(u);
  dfs(0);
  // 从大到小传递：长串出现次数 <= 短串出现次数
  _rep(l, 1, N) printf("%d\n", F[l]);
  return 0;
}
// 24467571 2019-09-26 17:18:19 Feng Chen Substrings  accepted 0.22  70M CPP14
```

## 例题23 不同的子串（New Distinct Substrings, SPOJ SUBST1）

### 题目描述
给定一个字符串S，求S中**不同子串的数量**（即所有子串去重后的个数）。

- **输入格式**：T组数据。每组一行字符串S（仅小写字母）。
- **输出格式**：每组一行，本质不同子串数。
- **约束**：|S| ≤ 50000。

### 解题思路
使用**后缀自动机 + DP**：
1. **SAM构建**：在增量构建SAM时，每插入一个字符新增的本质不同子串数 = `len[cur] - len[link[cur]]`。这些子串都是以cur为终点的、长度在`(len[link[cur]]+1)`到`len[cur]`之间的新子串。
2. **动态统计**：累积所有增量的和即答案。也可构建完成后，`Σ(len[u] - len[link[u]])`。
3. 本题使用DP方法：在SAM的DAG上，`F[u]` = 以u为起点的路径数（含空路径）。从根节点0出发的路径数-1即为不同子串数。

### 算法方法
**后缀自动机（SAM）+ DAG上DP/记忆化搜索**：SAM的有向无环图（DAG）上，每个从根出发的路径唯一对应一个子串。统计路径数即为本质不同子串数。

### 复杂度分析
- **时间复杂度**：O(N × log|Σ|)，map实现的SAM每次插入O(log|Σ|)，DP O(N)。
- **空间复杂度**：O(N)，SAM节点数≤2N。

```cpp
// 例题23 不同的子串（New Distinct Substrings, SPOJ SUBST1）
// 陈锋
// 题目：求字符串中本质不同的子串个数
// 算法：SAM的DAG上DP/记忆化搜索统计从根出发的不同路径数
#include <bits/stdc++.h>
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)
typedef long long LL;
using namespace std;

template<int SZ, int SIG = 32>
struct Suffix_Automaton {
  int link[SZ], len[SZ], last, sz;
  map<char, int> next[SZ];  // 使用map支持大字符集
  inline void init() { sz = 0, last = new_node(); }
  inline int new_node() {
    assert(sz + 1 < SZ);
    int nd = sz++; next[nd].clear(), link[nd] = -1, len[nd] = 0; return nd;
  }
  inline void insert(char x) {
    int p = last, cur = new_node(); len[last = cur] = len[p] + 1;
    while (p != -1 && !next[p].count(x)) next[p][x] = cur, p = link[p];
    if (p == -1) { link[cur] = 0; return; }
    int q = next[p][x];
    if (len[p] + 1 == len[q]) { link[cur] = q; return; }
    int nq = new_node(); next[nq] = next[q];
    link[nq] = link[q], len[nq] = len[p] + 1, link[cur] = link[q] = nq;
    while (p >= 0 && next[p][x] == q) next[p][x] = nq, p = link[p];
  }
  inline void build(char* s) { while (*s) insert(*s++); }
};

const int NN = 5e4 + 4;
Suffix_Automaton<NN * 2> sam;
char S[NN];
LL F[NN * 2];

// 记忆化搜索：以节点v为起点的不同路径数（含空路径，即只包含v自身）
LL dpF(int v) {
  LL &f = F[v];
  if (f != -1) return f;
  f = 1;  // 空路径（即只到v自身）
  const auto& E = sam.next[v];
  if (E.empty()) return f = 1;
  for (const auto& p : E) f += dpF(p.second);  // 累加所有出边的路径数
  return f;
}

int main() {
  int T; scanf("%d", &T);
  while (T--) {
    scanf("%s", S);
    sam.init(), sam.build(S);
    fill_n(F, NN * 2, -1);
    printf("%lld\n", dpF(0) - 1);  // 减去空路径（不含任何字符）
  }
}
// 24466280 2019-09-26 14:59:33 Feng Chen New Distinct Substrings accepted 0.15  17M CPP14
```
