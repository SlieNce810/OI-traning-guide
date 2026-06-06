# 3.7 树的经典问题与方法

## 例题34  Rikka与路径的交集（Rikka with Intersection of Paths, ACM/ICPC徐州2018, CodeforceGym 102012G）

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

## 例题33  村庄有多远（How far away, HDU 2586） ECJTU 2009 Spring Contest

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

## 例题37  竞赛（Race, IOI 2011，牛客NC51143）

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

## 例题40 要有彩虹（Let there be rainbows!, IPSC 2009 Problem L）

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

## 例题39 软件包管理器（NOI 2015）牛客NC 17882）

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

## 例题35  路径统计（Tree, POJ1741）

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

## 例题36  铁人比赛（Ironman Race in Treeland, ACM/ICPC Kuala Lumpur 2008, UVa12161）

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

## 例题38 闪电的能量（Lightning Energy Report, ACM/ICPC Jakarta2010, UVa1674）

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

## 例题38 闪电的能量（Lightning Energy Report, ACM/ICPC Jakarta2010, UVa1674）

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
