# 3.8 动态树与LCT

## 例题43  大厨和图上查询（Chef and Graph Queries，Codechef GERALD 07）

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

## 例题44  大象（Elephants, Codechef ELPHANT, IOI 2011 Day 2）

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

## 例题42  快乐涂色（Happy Painting, UVa11994）

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
