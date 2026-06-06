# 3.8 动态树与LCT

## 例题43  大厨和图上查询（Chef and Graph Queries，Codechef GERALD 07）

### 题目描述
给定N个节点（初始无边），依次加入M条带编号的边（编号为加入顺序1..M）。有Q个查询[L,R]，问在仅考虑编号在[L,R]范围内的边时，图的连通分量数。

- **约束**：N, M, Q ≤ 2×10^5。

### 解题思路
使用**LCT + BIT**维护动态图连通性和"最小标号边"：
1. 按编号顺序依次加入边i=(u,v)。用LCT维护动态森林（节点数为N+M，节点1..M代表边，M+1..M+N代表原图节点）。
2. 若加入边i时u和v已连通：找到u-v路径上标号最小的边e。若e < i，则删除边e，替换为边i（因为边i的标号更大，在查询时更可能被包含）。BIT中标记：e位置-1，i位置+1。
3. 查询[L,R]时：区间内有效边数 = `S.sum(R) - S.sum(L-1)`。连通分量数 = N - 有效边数。
4. 因为维护的是"最大生成树"结构：LCT中保留的边构成每个时刻的"最后加入的生成树"。

### 算法方法
**LCT（Link-Cut Tree）+ BIT（树状数组）**：LCT维护动态树结构，支持link/cut/findroot操作，并用minw维护路径上的最小权值边。BIT维护每个时间点的有效边数。核心思想：用LCT维护"时间最大生成树"，边的权值为其编号。

### 复杂度分析
- **时间复杂度**：O((M+Q) log N)，每次LCT操作O(log N)。
- **空间复杂度**：O(N+M)，LCT节点约N+M个。

```cpp
// 例题43  大厨和图上查询（Chef and Graph Queries, GERALD07）
// 陈锋
// 题目：动态加边图，查询编号区间内的边构成图的连通分量数
// 算法：LCT维护最大生成树 + BIT统计有效边
#include <bits/stdc++.h>
using namespace std;

template <int SZ> struct LCT {
  int ch[SZ][2], fa[SZ], minw[SZ]; bool rev[SZ];
  // LCT标准操作：rotate, splay, access, makeroot, link, cut, split, findroot, init
  inline int& ls(int x) { return ch[x][0]; } inline int& rs(int x) { return ch[x][1]; }
  inline void reverse(int x) { rev[x] ^= 1, swap(ls(x), rs(x)); }
  inline void maintain(int x) { minw[x] = min(x, min(minw[ls(x)], minw[rs(x)])); }
  inline void pushdown(int x) { if (rev[x]) reverse(ls(x)), reverse(rs(x)), rev[x] = false; }
  inline bool isroot(int x) { return ls(fa[x]) != x && rs(fa[x]) != x; }
  inline int isright(int x) { return rs(fa[x]) == x; }
  void rotate(int x) { /* 标准旋转 */ }
  void pushup(int x) { if (!isroot(x)) pushup(fa[x]); pushdown(x); }
  void splay(int x) { pushup(x); while (!isroot(x)) { /* 双旋 */ } }
  void access(int x) { for (int t = 0; x; t = x, x = fa[x]) splay(x), rs(x) = t, maintain(x); }
  void makeroot(int x) { access(x), splay(x), reverse(x); }
  void link(int x, int y) { makeroot(x), fa[x] = y; }
  void cut(int x, int y) { makeroot(x), access(y), splay(y); ls(y) = fa[x] = 0; maintain(y); }
  void split(int x, int y) { makeroot(x), access(y), splay(y); }
  int findroot(int x) { access(x), splay(x); while (ls(x)) pushdown(x), x = ls(x); splay(x); return x; }
  void init(int sz) { minw[0] = 1e9; for (int i = 1; i <= sz; i++) minw[i] = i, ch[i][0] = ch[i][1] = fa[i] = 0, rev[i] = 0; }
};

template <int SZ> struct BIT { /* 标准BIT */ };
const int NN = 2e5 + 4;
BIT<NN> S; LCT<NN * 2> lct;
int QL[NN], Ans[NN], EU[NN], EV[NN];
vector<int> EQ[NN];

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T; cin >> T;
  for (int t = 0, n, m, q; t < T; t++) {
    cin >> n >> m >> q;
    for (int i = 1; i <= m; i++) { int &u = EU[i], &v = EV[i]; cin >> u >> v; u += m, v += m; EQ[i].clear(); }
    S.init(m), lct.init(m + n);
    for (int i = 1, qr; i <= q; i++) cin >> QL[i] >> qr, EQ[qr].push_back(i);
    for (int i = 1; i <= m; i++) {  // 按编号加入边
      int u = EU[i], v = EV[i];
      if (lct.findroot(u) == lct.findroot(v)) {  // 已连通
        lct.split(u, v); int e = lct.minw[v];
        if (e < i) { lct.cut(e, EU[e]), lct.cut(e, EV[e]), S.add(e, -1); lct.link(i, u), lct.link(i, v), S.add(i, 1); }  // 替换
      } else lct.link(u, i), lct.link(v, i), S.add(i, 1);
      for (size_t xi = 0; xi < EQ[i].size(); xi++) Ans[EQ[i][xi]] = n - (S.sum(i) - S.sum(QL[EQ[i][xi]] - 1));
    }
    for (int i = 1; i <= q; i++) cout << Ans[i] << endl;
  }
  return 0;
}
// 40407264	sukhoeing 0.62 33.4M C++14
```
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

## 例题44  大象（Elephants, Codechef ELPHANT, IOI 2011 Day 2）

### 题目描述
数轴上有N只大象，每只大象有一个不同的位置P[i]。大象之间有一个特殊的关系：两只大象如果位置差大于L则互相不可见，否则可以经由对方"链接"。一种链接方案是一棵生成树——如果两只大象的位置差≤L，它们之间可以有一条边。

现在有M次修改操作，每次将第X[i]只大象移动到新的位置Y[i]。每次修改后，需要输出当前链接方案下，生成树需要的边数（即N减去连通块数）。初始时大象位置不保证连通。N, M ≤ 10^5。

更具体地：把所有大象的位置坐标离散化，在离散化后的坐标轴上，每只大象只与其位置+L+1处的虚拟节点相连（表示这个位置的大象可以链接到右侧L范围内的所有位置）。问题转化为：有多少个区间被大象覆盖，这等价于数轴上被覆盖的连续段数。

### 解题思路
1. **离散化坐标**：将大象位置P[i]和P[i]+L+1都离散化到1..sz的范围。
2. **LCT建模**：坐标轴上的每个整数点作为一个LCT节点，初始将所有相邻位置link起来。如果位置u有大象，则cut(u, u+1)并link(u, u+L+1)，表示这个位置的大象可以"跳过"它从u到u+L+1之间的所有位置。
3. **权值维护**：在LCT上每个节点维护val（该节点是否被大象占据）和子树sum。当大象移动到位置u时，如果该位置之前无大象则modify(u, 1)，如果之前有则先modify(u, 0)。
4. **答案统计**：从位置1到sz的区间和就是覆盖的连续段数量，N减去此数即为答案。

### 算法方法
**LCT（Link-Cut Tree） + 离散化 + 区间建模**。将坐标轴建模为LCT中的链结构，大象占据的位置改变链的连接方式，用LCT维护子树和。

### 复杂度分析
- **时间复杂度**：O((N+M) log SZ)。每次LCT操作O(log SZ)，SZ为离散化后的坐标数（≤ 2N+2M）。
- **空间复杂度**：O(SZ)，LCT节点数。

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

## NC20311 例题41  洞穴勘测（Cave, SDOI2008）

### 题目描述
初始有N个孤立节点（洞穴），编号1..N。需要处理Q个操作，操作类型包括：
- `Connect u v`：在节点u和v之间建立一条边（洞穴通道），保证操作前u和v不连通。
- `Destroy u v`：摧毁节点u和v之间的边，保证操作前这条边存在。
- `Query u v`：查询节点u和v是否连通。
N ≤ 10000, Q ≤ 200000。

### 解题思路
1. **动态树需求**：需要支持动态加边（link）、删边（cut）和连通性查询（find_root）。这正好是LCT（Link-Cut Tree）的标准应用场景。
2. **LCT基本操作**：
   - `link(x, y)`：先判断x和y不在同一棵树中，然后makeroot(x)，fa[x] = y。
   - `cut(x, y)`：split(x, y)，检查y在辅助树中的左孩子是否为x且x没有右孩子（确保x和y在原树中直接相邻），然后断开连接。
   - `find_root(x)`：access(x) + splay(x)，沿着左子树逐个下推直到叶子，最后splay叶子上来，返回叶子的编号。
3. **翻转标记（rev）**：makeroot操作需要翻转整条路径的深度关系，用懒标记rev实现。
4. **辅助树（Splay）**：每个节点的虚边组成一棵Splay（按深度为关键字），access将根到x的路径变成一棵Splay中的首选边。

### 算法方法
**LCT（Link-Cut Tree）**。最基本的LCT实现，支持 link / cut / find_root 操作，只维护结构不维护额外权值。

### 复杂度分析
- **时间复杂度**：O(Q log N)。每次LCT操作（access、splay）均摊O(log N)。
- **空间复杂度**：O(N)，每个节点维护ch[2], fa, rev。

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
  // 判断x是辅助树上父亲的右儿子
  inline int is_right_ch(int x) { return ch[fa[x]][1] == x; }
  // 判断x是否为辅助树的根（虚边父节点不认x为儿子）
  inline int is_root(int x) { return ch[fa[x]][0] != x && ch[fa[x]][1] != x; }
  void pushdown(int x) { // 下推翻转标记到左右儿子
    if (rev[x] == 0) return;
    int lx = ch[x][0], rx = ch[x][1];
    if (lx) swap(ch[lx][0], ch[lx][1]), rev[lx] ^= 1;
    if (rx) swap(ch[rx][0], ch[rx][1]), rev[rx] ^= 1;
    rev[x] = 0;
  }
  void pushup(int x) { // 从x向根递归下推所有懒标记
    if (!is_root(x)) pushup(fa[x]);
    pushdown(x);
  }
  void rotate_up(int x) {  // Splay旋转：将x向上旋转一级
    int y = fa[x], z = fa[y], chx = is_right_ch(x), chy = is_right_ch(y),
        &t = ch[x][chx ^ 1]; // t在x和y之间，方向与x-y相反
    fa[x] = z;
    if (!is_root(y)) ch[z][chy] = x;              // x和y在z的同一侧
    ch[y][chx] = t, fa[t] = y, t = y, fa[y] = x;  // 保证t仍在x和y之间
  }
  void splay(int x) { // 将x旋转为辅助树的根
    pushup(x);  // 先下推从根到x的所有翻转标记
    for (int f = fa[x]; f = fa[x], !is_root(x); rotate_up(x))
      if (!is_root(f)) rotate_up(is_right_ch(x) == is_right_ch(f) ? f : x);
  }
  void access(int x) {  // 将根到x的路径变为首选边（实链）
    for (int f = 0; x; f = x, x = fa[x]) splay(x), ch[x][1] = f;
  }
  void make_root(int x) {  // 将x变为所在原树的根（翻转整条路径）
    access(x), splay(x), swap(ch[x][0], ch[x][1]), rev[x] ^= 1;
  }
  void split(int x, int y) { make_root(x), access(y), splay(y); } // 将x-y路径提取到一棵Splay中
  int find_root(int x) {  // 寻找x所在原树的根
    access(x), splay(x);
    while (ch[x][0]) x = ch[x][0]; // 沿左子树走到最深处
    splay(x);
    return x;
  }
  void cut(int x, int y) {
    split(x, y);  // 将x变为根，提取x-y路径到y的Splay
    if (ch[y][0] == x && !ch[x][1]) ch[y][0] = fa[x] = 0; // 确认x和y直接相邻后断开
  }
  void link(int x, int y) {
    if (find_root(x) != find_root(y)) make_root(x), fa[x] = y; // 先判断不连通再连边
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

## 例题42  快乐涂色（Happy Painting, UVa11994）

### 题目描述
给定一棵有根树（每个节点有一个父节点），每条边有一个初始颜色（用整数表示）。需要处理M个操作：
- `1 x y c`：将节点x的父边重新连接到节点y，并将这条边的颜色设为c。（如果x == y则忽略）
- `2 x y c`：将x到y路径上所有边的颜色都改为c。
- `3 x y`：查询x到y路径上有多少条边，以及有多少种不同的颜色。
N, M ≤ 10^5。

### 解题思路
1. **LCT维护边权**：将每条边的颜色信息挂在该边较深的那个节点上（clr[x] = 边(fa[x], x)的颜色）。这样路径查询时，路径上的每个节点（除LCA外）都携带一条边的颜色。
2. **颜色集合**：用位运算（bitmask）维护颜色集合，因为颜色种类有限。set[x]存储x所在Splay子树中所有边的颜色集合的位或。
3. **路径染色（paint）**：split(x, y)后，在y的Splay根节点上打lazy标记（mark[y] = c），同时set[y] = 1 << c。
4. **cut/link操作**：cut(x)操作是access(x) + splay(x)，然后断开x和其左子树（即x在原树中的父亲）的连接。link(x, y, c)先cut(x)，然后fa[x] = y, clr[x] = c。
5. **查询（query）**：split(x, y)后，从set[y]中统计不同颜色的位数（有多少个1），size[y]-1为路径边数。

### 算法方法
**LCT（Link-Cut Tree）维护边权 + 位运算颜色压缩**。边权挂在子节点上，用位运算压缩颜色集合，支持路径染色、重新连边和路径颜色统计。

### 复杂度分析
- **时间复杂度**：O(M log N)。每次LCT操作O(log N)。
- **空间复杂度**：O(N)，每个节点存储ch[2], fa, rev, size, clr, set, mark。

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
