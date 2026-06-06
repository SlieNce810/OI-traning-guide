# 第6章 更多算法专题

## 6.1 轮廓线动态规划

### LA3620 Manhattan Wiring

```cpp
// LA3620 Manhattan Wiring
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<algorithm>
using namespace std;

const int INF = 100000000;

int nrows, ncols;
int G[10][10];

// 插头编号：0表示无插头，1表示和数字2连通，2表示和数字3连通

struct State {
  int up[9]; // up[i](0<=i<m)表示第i列处轮廓线上方的插头编号
  int left; // 当前格（即下一个要放置的方格）左侧的插头

  // 三进制编码
  int encode() const {
    int key = left;
    for(int i = 0; i < ncols; i++) key = key * 3 + up[i];
    return key;
  }

  // 在(row,col)处放一个新方格。UDLR分别为该方格上下左右四个边界上的插头编号
  // 产生的新状态存放在T里，成功返回true，失败返回false
  bool next(int row, int col, int U, int D, int L, int R, State& T) const {
    if(row == nrows - 1 && D != 0) return false; // 最下行下方不能有插头
    if(col == ncols - 1 && R != 0) return false; // 最右列右边不能有插头

    int must_left = (col > 0 && left != 0); // 是否必须要有左插头
    int must_up = (row > 0 && up[col] != 0); // 是否必须要有上插头

    if((must_left && L != left) || (!must_left && L != 0)) return false; // 左插头不匹配
    if((must_up && U != up[col]) || (!must_up && U != 0)) return false; // 上插头不匹配
    if(must_left && must_up && left != up[col]) return false; // 若左插头和上插头都存在，二者必须匹配

    // 产生新状态。实际上只有当前列的下插头和left插头有变化
    for(int i = 0; i < ncols; i++) T.up[i] = up[i];
    T.up[col] = D;
    T.left = R;
    return true;
  }
};

int memo[9][9][59049]; // 3^10

// 当前要放置格子(row, col)，状态为S。返回最小总长度
int rec(int row, int col, const State& S) {
  if(col == ncols) { col = 0; row++; }
  if(row == nrows) return 0;

  int key = S.encode();
  int& res = memo[row][col][key];
  if(res >= 0) return res;
  res = INF;

  State T;
  if(G[row][col] <= 1) { // 空格（0）或者障碍格（1）
    if(S.next(row, col, 0, 0, 0, 0, T)) res = min(res, rec(row, col+1, T)); // 整个格子里都不连线
    if(G[row][col] == 0) // 如果是空格，可以连线。由于线不能分叉，所以这条线一定连接格子的某两个边界（6种情况）
      for(int t = 1; t <= 2; t++) { // 枚举线的种类。t=1表示2线，t=2表示3线
        if(S.next(row, col, t, t, 0, 0, T)) res = min(res, rec(row, col+1, T) + 2); // 上<->下
        if(S.next(row, col, t, 0, t, 0, T)) res = min(res, rec(row, col+1, T) + 2); // 上<->左
        if(S.next(row, col, t, 0, 0, t, T)) res = min(res, rec(row, col+1, T) + 2); // 上<->右
        if(S.next(row, col, 0, t, t, 0, T)) res = min(res, rec(row, col+1, T) + 2); // 下<->左
        if(S.next(row, col, 0, t, 0, t, T)) res = min(res, rec(row, col+1, T) + 2); // 下<->右
        if(S.next(row, col, 0, 0, t, t, T)) res = min(res, rec(row, col+1, T) + 2); // 左<->右
      }
  }
  else {
    int t = G[row][col] - 1; // 数字为2和3，但插头类型是1和2，所以要减1
    // 由于线不能分叉，所以这条线一定连接格子中间的数字和某一个边界（4种情况）
    if(S.next(row, col, t, 0, 0, 0, T)) res = min(res, rec(row, col+1, T) + 1); // 从上边界出来
    if(S.next(row, col, 0, t, 0, 0, T)) res = min(res, rec(row, col+1, T) + 1); // 从下边界出来
    if(S.next(row, col, 0, 0, t, 0, T)) res = min(res, rec(row, col+1, T) + 1); // 从左边界出来
    if(S.next(row, col, 0, 0, 0, t, T)) res = min(res, rec(row, col+1, T) + 1); // 从右边界出来
  }
  return res;
}

int main() {
  while(scanf("%d%d", &nrows, &ncols) == 2 && nrows && ncols) {
    for(int i = 0; i < nrows; i++)
      for(int j = 0; j < ncols; j++)
        scanf("%d", &G[i][j]);
    State S;
    memset(&S, 0, sizeof(S));
    memset(memo, -1, sizeof(memo));
    int ans = rec(0, 0, S);
    if(ans == INF) ans = 0;
    printf("%d\n", ans/2);
  }
  return 0;
}
// 25878347	1214	Manhattan Wiring	Accepted	C++	0.320	2020-12-23 08:59:49
```

### UVa10572 Black and White

```cpp
// UVa10572 Black and White
// Rujia Liu
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include <map>
using namespace std;

int nrows, ncols, has_sol;
char partial[8][9]; // 输入网格
char grid[8][8], sol[8][8]; // 当前正在填的网格和解网格

struct State {
  char color[8];       // 各列格子颜色
  char up_left;        // 左上方格子颜色（用来判断是否出现2x2同色子网格）
  char comp[8];        // 各格子连通分量
  char ncomp;          // 连通分量总数
  char ncolor_comp[2]; // 白连通分量个数和黑连通分量个数

  // 计算状态的最小表示
  void normalize() {
    int rep[10];
    memset(rep, -1, sizeof(rep));
    ncomp = ncolor_comp[0] = ncolor_comp[1] = 0;
    for (int i = 0; i < ncols; i++) {
      if (rep[comp[i]] < 0) {
        rep[comp[i]] = ncomp++;
        ncolor_comp[color[i]]++;
      }
      comp[i] = rep[comp[i]];
    }
  }

  // 把所有编号为b的连通分量改成a
  void merge(int a, int b) {
    if (a == b) return;
    for (int i = 0; i < ncols; i++)
      if (comp[i] == b) comp[i] = a;
  }

  // 正好不超过32位无符号整数范围
  unsigned int encode() {
    unsigned int key = 0;
    for (int i = 0; i < ncols; i++)
      key = key * 16 + color[i] * 8 + comp[i];
    return key;
  }
};

// 动态规划所用状态值表。只记录了不强制涂色（即force_color<0）时的值
map<unsigned, int> memo[8][8][2]; 

const int ch[] = { 'o', '#' };

// 当前要涂格子(row, col)，状态为S，必须涂force_color颜色。返回解的个数
int rec(int row, int col, State& S, int force_color) {
  if (col == ncols) { col = 0; row++; }
  S.normalize(); // 计算最小表示

  if (row == nrows) {
    if (S.ncolor_comp[0] > 1 || S.ncolor_comp[1] > 1) return 0;
    if (has_sol == 0) {
      has_sol = 1;
      for (int i = 0; i < nrows; i++)
        for (int j = 0; j < ncols; j++)
          sol[i][j] = grid[i][j];
    }
    return 1;
  }

  // 如果左格子和上格子颜色不同，则左上方格子的颜色是无关紧要的，统一设为0，减少状态
  if (row > 0 && col > 0 && S.color[col] != S.color[col-1])
    S.up_left = 0;

  // 只有不强制涂色（force_color<0）时key才有意义
  unsigned int key;
  if (force_color < 0) {
    key = S.encode();
    if (memo[row][col][S.up_left].count(key) != 0)
      return memo[row][col][S.up_left][key];
  }

  int res = 0;

  // 当前格子涂color这种颜色
  for(int color = 0; color < 2; color++) {
    if (force_color == 1 - color) continue; // 和force_color矛盾
    if (partial[row][col] == ch[1-color]) continue; // 和输入矛盾
    if (row > 0 && col > 0 && S.color[col-1] == color && S.color[col] == color && S.up_left == color) continue; // 出现2x2同色子网格

    State T = S;
    T.color[col] = color;
    T.up_left = S.color[col];
    T.comp[col] = (row > 0 && S.color[col] == color) ? S.comp[col] : S.ncomp; // 初始化新状态第col列的连通分量编号
    if (col > 0 && T.color[col-1] == color) T.merge(T.comp[col-1], T.comp[col]); // 如果颜色和左格子相同，则设置为左格子的连通分量

    grid[row][col] = ch[color];

    if (row > 0 && S.color[col] == 1-color) { // 检查上方格子是否为独立连通分量      
      if (find(T.comp, T.comp+ncols, S.comp[col]) == T.comp+ncols) { // 该连通分量已经消失
        if (S.ncolor_comp[1-color] > 1 || row < nrows-2) continue; // 如果color还有其他连通分量存在，或者至少还有两行需要涂，则无法继续
        res += rec(row, col+1, T, color); // 可以继续，但以后强制涂color
        continue;
      }
    }

    res += rec(row, col+1, T, force_color);
  }

  if (force_color < 0)
    memo[row][col][S.up_left][key] = res;
  return res;
}


int main() {
  int T;
  scanf("%d", &T);
  for(int kase = 1; kase <= T; kase++) {
    scanf("%d%d", &nrows, &ncols);
    for(int i = 0; i < nrows; i++) scanf("%s", partial[i]);

    State S;
    memset(&S, 0, sizeof(S));
    S.normalize();
    for (int i = 0; i < 8; i++)
      for (int j = 0; j < 8; j++)
        for (int k = 0; k < 2; k++)
          memo[i][j][k].clear();

    has_sol = 0;
    printf("%d\n", rec(0, 0, S, -1));
    if (has_sol) {
      for (int i = 0; i < nrows; i++) {
        for (int j = 0; j < ncols; j++)
          putchar(sol[i][j]);
        putchar('\n');
      }
    }
    printf("\n");
  }
  return 0;
}
// 25878350	10572	Black & White	Accepted	C++	0.440	2020-12-23 09:00:05
```

### UVa11270 Tiling Dominoes

```cpp
// UVa11270 Tiling Dominoes
// 刘汝佳
#include<cstdio>
#include<cstring>
#include<algorithm>
using namespace std;
int n, m, cur;

const int maxn = 15;
long long d[2][1<<maxn], memo[maxn*maxn][maxn*maxn];

void up(int a, int b) {
  if(b&(1<<m)) d[cur][b^(1<<m)] += d[1-cur][a];
}

long long solve(int n, int m) {
  memset(d, 0, sizeof(d));
  cur = 0;
  d[0][(1<<m)-1] = 1;
  for(int i = 0; i < n; i++)
    for(int j = 0; j < m; j++) { // 枚举当前要算的阶段
      cur ^= 1;
      memset(d[cur], 0, sizeof(d[cur]));
      for(int k = 0; k < (1<<m); k++) { // 枚举上个阶段的状态
        up(k, k<<1);
        if(i && !(k&(1<<m-1))) up(k, (k<<1)^(1<<m)^1);
        if(j && !(k&1)) up(k, (k<<1)^3);
      }
    }
  return d[cur][(1<<m)-1];
}

int main() {
  memset(memo, -1, sizeof(memo));
  while(scanf("%d%d", &n, &m) == 2) {
    if(n < m) swap(n, m);
    if(memo[n][m] < 0) memo[n][m] = solve(n, m);
    printf("%lld\n", memo[n][m]);
  }
  return 0;
}
// Accepted 10ms 927 C++ 5.3.0 2020-12-08 21:51:11 25826133
```

## 6.2 嵌套和分块数据结构

### 「SCOI2005」王室联邦

```cpp
// 「SCOI2005」王室联邦
// 陈锋
#include <iostream>
#include <stack>
#include <vector>
using namespace std;

typedef long long LL;
const int NN = 1000 + 4;
vector<int> G[NN];
stack<int> S;
int N, B, BCnt, BId[NN], Cap[NN];  //块的个数，每个点所属块编号，每个块的中心

void dfs(int u, int fa) {
  size_t sz = S.size();
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs(v, u);
    if (S.size() >= sz + B) {  //新增点可以分块
      Cap[++BCnt] = u;         //新增块中心点为u
      while (S.size() > sz) BId[S.top()] = BCnt, S.pop();
    }
  }
  S.push(u);
  if (u == 1)  // root特殊处理，未分块的点都放入以root为中心的块
    while (!S.empty()) BId[S.top()] = BCnt, S.pop();
}

int main() {
  ios::sync_with_stdio(false), cin.tie(nullptr);
  cin >> N >> B, BCnt = 0;
  for (int i = 1, u, v; i < N; i++) {
    cin >> u >> v;
    G[u].push_back(v), G[v].push_back(u);
  }
  dfs(1, -1);
  cout << BCnt << endl;
  for (int i = 1; i <= N; i++) cout << BId[i] << (i == N ? "\n" : " ");
  for (int i = 1; i <= BCnt; i++) cout << Cap[i] << (i == BCnt ? "\n" : " ");
  return 0;
}
// 46047872 「SCOI2005」王室联邦 答案正确 100 3 504 1000 C++ 2020-12-13 23:33:34
```

### UVa11297 - Census

```cpp
// UVa11297 - Census
// 陈锋
#include<stdio.h>
#include<algorithm>
#include<cstring>
using namespace std;
const int NN = 508, INF = 1e9;
struct SegTree2D {
  struct Node {
    int Max, Min;
    void update(const Node& nd) {
      Max = max(Max, nd.Max), Min = min(Min, nd.Min);
    }
  } NS[NN][NN * 4]; //第一维表示是用矩阵的第几行建立的线段树

  Node qAns;
  void maintain(int c, int o) {
    Node& nd = NS[c][o], ld = NS[c][2 * o], rd = NS[c][2 * o + 1];
    nd.Max = max(ld.Max, rd.Max), nd.Min = min(ld.Min, rd.Min);
  }

  void build(int c, int o, int l, int r) {
    Node& nd = NS[c][o];
    if (l == r) {
      scanf("%d", &nd.Min), nd.Max = nd.Min;
      return ;
    }
    int mid = (l + r) / 2, lc = o * 2, rc = o * 2 + 1;
    build(c, lc, l, mid), build(c, rc, mid + 1, r);
    maintain(c, o);
  }

  void query(int c, int o, int l, int r, int qL, int qR) {
    if (l == qL && r == qR) {
      qAns.update(NS[c][o]);
      return;
    }
    int qM = (qL + qR) / 2, lc = o * 2, rc = o * 2 + 1;
    if (qM >= r) query(c, lc, l, r, qL, qM);
    else if (qM < l) query(c, rc, l, r, qM + 1, qR);
    else query(c, lc, l, qM, qL, qM), query(c, rc, qM + 1, r, qM + 1, qR);
  }

  void modify(int c, int x, int val, int o, int l, int r) {
    Node& nd = NS[c][o];
    if (l == r && l == x) {
      nd.Max = nd.Min = val;
      return ;
    }
    int m = (l + r) / 2, lc = o * 2, rc = o * 2 + 1;
    if (m >= x) modify(c, x, val, lc, l, m);
    else if (m < x) modify(c, x, val, rc,  m + 1, r);
    maintain(c, o);
  }
};
SegTree2D ST;
int main() {
  char op[10];
  for (int m, n, x1, y1, x2, y2, v; scanf("%d", &n) != EOF;) {
    for (int x = 1; x <= n; x++) ST.build(x, 1, 1, n);
    scanf("%d", &m);
    while (m--) {
      scanf("%s", op);
      if (op[0] == 'q') {
        ST.qAns.Max = -INF, ST.qAns.Min = INF;
        scanf("%d%d%d%d", &x1, &y1, &x2, &y2);
        for (int x = x1; x <= x2; x++) ST.query(x, 1, y1, y2, 1, n);
        printf("%d %d\n", ST.qAns.Max, ST.qAns.Min);
      }
      if (op[0] == 'c')
        scanf("%d%d%d", &x1, &y1, &v), ST.modify(x1, y1, v, 1, 1, n);
    }
  }
  return 0;
}
// 25858184 11297 Census  Accepted  C++ 0.430 2020-12-17 09:28:06
```

### UVa11990 "Dynamic" Inversion

```cpp
// UVa11990 "Dynamic" Inversion
// 刘汝佳
#include<cstdio>
#include<vector>
#include<algorithm>
#include<cassert>
using namespace std;

inline int lowbit(int x) { return x&-x; }

struct Node {
  Node *ch[2]; // 左右子树
  int v; // 值
  int s; // 结点总数。有删除标记的结点未统计在内
  int d; // 删除标记
  Node():d(0) {}
  int ch_s(int d) { return ch[d] == NULL ? 0 : ch[d]->s; }
};

// 名次树，懒删除实现
struct RankTree {
  int n, next;
  int *v;
  Node *nodes, *root;
  RankTree(int n, int* A):n(n) {
    nodes = new Node[n];
    next = 0;
    v = new int[n];
    for(int i = 0; i < n; i++) v[i] = A[i];
    sort(v, v+n);
    root = build(0, n-1);
    delete[] v;
  }

  Node* build(int L, int R) {
    if(L > R) return NULL;
    int M = L + (R-L) / 2;
    int u = next++;
    nodes[u].v = v[M];
    nodes[u].ch[0] = build(L, M-1);
    nodes[u].ch[1] = build(M+1, R);
    nodes[u].s = nodes[u].ch_s(0) + nodes[u].ch_s(1) + 1;
    return &nodes[u];
  }

  // type = 0：统计比v小的元素个数
  // type = 1：统计比v大的元素个数  
  int count(int v, int type) {
    Node* u = root;
    int cnt = 0;
    while(u != NULL) {
      if(u->v == v) { cnt += u->ch_s(type); break; }
      int c = (v < u->v ? 0 : 1);
      if(c != type) cnt += u->s - u->ch_s(c);
      u = u->ch[c];
    }
    return cnt;
  }

  // 要保证v在树中且尚未删除
  void erase(int v) {
    Node* u = root;
    while(u != NULL) {
      u->s--;
      if(u->v == v) { assert(u->d == 0); u->d = 1; return; }
      int c = (v < u->v ? 0 : 1);
      u = u->ch[c];
    }
    assert(0);
  }

  ~RankTree() {
    delete[] nodes;
  }
};

// 嵌套名次树的Fenwick树
struct FenwickRankTree {
  int n;
  vector<RankTree*> C;

  void init(int n, int* A) {
    this->n = n;
    C.resize(n+1); // 存放在C[1]~C[n]
    for(int i = 1; i <= n; i++) {
      C[i] = new RankTree(lowbit(i), A+i-lowbit(i)+1);
    }
  }

  void clear() { for(int i = 1; i <= n; i++) delete C[i]; }

  // 统计A[1], A[2], ..., A[x]有多少个元素比v大(x<=n)
  int count(int x, int v, int type) {
    int ret = 0;
    while(x > 0) {
      ret += C[x]->count(v, type); x -= lowbit(x);
    }
    return ret;
  }

  // 删除A[x]=v
  void erase(int x, int v) {
    while(x <= n) {
      C[x]->erase(v); x += lowbit(x);
    }
  }
};

// 普通Fenwick树
struct FenwickTree {
  int n;
  vector<int> C;

  void init(int n) {
    this->n = n;
    C.resize(n+1);
    fill(C.begin(), C.end(), 0);
  }

  // 计算A[1]+A[2]+...+A[x] (x<=n)
  int sum(int x) {
    int ret = 0;
    while(x > 0) {
      ret += C[x]; x -= lowbit(x);
    }
    return ret;
  }

  // A[x] += d (1<=x<=n)
  void add(int x, int d) {
    while(x <= n) {
      C[x] += d; x += lowbit(x);
    }
  }
};

const int maxn = 200000 + 5;
const int maxm = 100000 + 5;
typedef long long LL;

int n, m, A[maxn], B[maxn], pos[maxn];
FenwickRankTree frt;
FenwickTree f; // 用来求逆序对数以及求已删除的元素有多少个比v小

LL inversion_pairs() {
  LL ans = 0;
  f.init(n);
  for(int i = n; i >= 1; i--) {
    ans += f.sum(A[i]-1);
    f.add(A[i], 1);
  }
  return ans;
}

int main() {
  while(scanf("%d%d", &n, &m) == 2) {
    for(int i = 1; i <= n; i++) {
      scanf("%d", &A[i]);
      pos[B[i] = A[i]] = i;
    }
    LL cnt = inversion_pairs();
    frt.init(n, A);
    f.init(n);
    for(int i = 0; i < m; i++) {
      printf("%lld\n", cnt);
      int x;
      scanf("%d", &x);
      f.add(x, 1);
      int a = frt.count(pos[x]-1, x, 1); // x左边有a个比x大
      int b = x-1; // 一共有x-1个数比x小
      int c = f.sum(x-1); // 删了c个比x小的
      int d = frt.count(pos[x]-1, x, 0);  // 现在左边有d个比x小
      b -= c + d;  // 还剩b个
      cnt -= a + b; // 逆序对减少a+b个
      frt.erase(pos[x], x);
    }
  }
  return 0;
}
// 25878364	11990	``Dynamic'' Inversion	Accepted	C++	0.900	2020-12-23 09:02:59
```

### UVa12003 Array Transformer

```cpp
// UVa12003 Array Transformer
// 刘汝佳
#include<cstdio>
#include<algorithm>
using namespace std;

const int maxn = 300000 + 10;
const int SIZE = 4096;

int n, m, u, A[maxn], block[maxn/SIZE+1][SIZE];

void init() {
  scanf("%d%d%d", &n, &m, &u);
  int b = 0, j = 0;
  for(int i = 0; i < n; i++) {
    scanf("%d", &A[i]);
    block[b][j] = A[i];
    if(++j == SIZE) { b++; j = 0; }
  }
  for(int i = 0; i < b; i++) sort(block[i], block[i]+SIZE);
  if(j) sort(block[b], block[b]+j);
}

int query(int L, int R, int v) {
  int lb = L/SIZE, rb = R/SIZE; // L和R所在块编号
  int k = 0;
  if(lb == rb) {
    for(int i = L; i <= R; i++) if(A[i] < v) k++;
  } else {
    for(int i = L; i < (lb+1)*SIZE; i++) if(A[i] < v) k++; // 第一块
    for(int i = rb*SIZE; i <= R; i++) if(A[i] < v) k++; // 最后一块
    for(int b = lb+1; b < rb; b++) // 中间的完整块
      k += lower_bound(block[b], block[b]+SIZE, v) - block[b];
  }
  return k;
}

void change(int p, int x) {
  if(A[p] == x) return;
  int old = A[p], pos = 0, *B = &block[p/SIZE][0]; // B就是p所在的块
  A[p] = x;

  while(B[pos] < old) pos++; B[pos] = x; // 找到x在块中的位置
  if(x > old) // x太大，往后交换
    while(pos < SIZE-1 && B[pos] > B[pos+1]) { swap(B[pos+1], B[pos]); pos++; }
  else // 往前交换
    while(pos > 0 && B[pos] < B[pos-1]) { swap(B[pos-1], B[pos]); pos--; }
}

int main() {
  init();
  while(m--) {
    int L, R, v, p;
    scanf("%d%d%d%d", &L, &R, &v, &p); L--; R--; p--;
    int k = query(L, R, v);
    change(p, (long long)u * k / (R-L+1));
  }
  for(int i = 0; i < n; i++) printf("%d\n", A[i]);
  return 0;
}
// 25878377	12003	Array Transformer	Accepted	C++	0.530	2020-12-23 09:05:32
```

## 6.3 暴力法专题

### LA2659 Sudoku/POJ3076 SEERC2006

```cpp
// LA2659 Sudoku/POJ3076 SEERC2006
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<vector>

using namespace std;

const int maxr = 5000;
const int maxn = 2000;
const int maxnode = 20000;

// 行编号从1开始，列编号为1~n，结点0是表头结点; 结点1~n是各列顶部的虚拟结点
struct DLX {
  int n, sz; // 列数，结点总数
  int S[maxn]; // 各列结点数

  int row[maxnode], col[maxnode]; // 各结点行列编号
  int L[maxnode], R[maxnode], U[maxnode], D[maxnode]; // 十字链表

  int ansd, ans[maxr]; // 解

  void init(int n) { // n是列数
    this->n = n;

    // 虚拟结点
    for(int i = 0 ; i <= n; i++) {
      U[i] = i; D[i] = i; L[i] = i-1, R[i] = i+1;
    }
    R[n] = 0; L[0] = n;

    sz = n + 1;
    memset(S, 0, sizeof(S));
  }

  void addRow(int r, vector<int> columns) {
    int first = sz;
    for(int i = 0; i < columns.size(); i++) {
      int c = columns[i];
      L[sz] = sz - 1; R[sz] = sz + 1; D[sz] = c; U[sz] = U[c];
      D[U[c]] = sz; U[c] = sz;
      row[sz] = r; col[sz] = c;
      S[c]++; sz++;
    }
    R[sz - 1] = first; L[first] = sz - 1;
  }

  // 顺着链表A，遍历除s外的其他元素
  #define FOR(i,A,s) for(int i = A[s]; i != s; i = A[i]) 

  void remove(int c) {
    L[R[c]] = L[c];
    R[L[c]] = R[c];
    FOR(i,D,c)
      FOR(j,R,i) { U[D[j]] = U[j]; D[U[j]] = D[j]; --S[col[j]]; }
  }

  void restore(int c) {
    FOR(i,U,c)
      FOR(j,L,i) { ++S[col[j]]; U[D[j]] = j; D[U[j]] = j; }
    L[R[c]] = c;
    R[L[c]] = c;
  }

  // d为递归深度
  bool dfs(int d) {
    if (R[0] == 0) { // 找到解
      ansd = d; // 记录解的长度
      return true;
    }

    // 找S最小的列c
    int c = R[0]; // 第一个未删除的列
    FOR(i,R,0) if(S[i] < S[c]) c = i;

    remove(c); // 删除第c列
    FOR(i,D,c) { // 用结点i所在行覆盖第c列
      ans[d] = row[i];
      FOR(j,R,i) remove(col[j]); // 删除结点i所在行能覆盖的所有其他列
      if(dfs(d+1)) return true;
      FOR(j,L,i) restore(col[j]); // 恢复结点i所在行能覆盖的所有其他列
    }
    restore(c); // 恢复第c列

    return false;
  }

  bool solve(vector<int>& v) {
    v.clear();
    if(!dfs(0)) return false;
    for(int i = 0; i < ansd; i++) v.push_back(ans[i]);
    return true;
  }

};

////////////// 题目相关
#include<cassert>

DLX solver;

const int SLOT = 0;
const int ROW = 1;
const int COL = 2;
const int SUB = 3;

// 行/列的统一编解码函数。从1开始编号
int encode(int a, int b, int c) {
  return a*256+b*16+c+1;
}

void decode(int code, int& a, int& b, int& c) {
  code--;
  c = code%16; code /= 16;
  b = code%16; code /= 16;
  a = code;
}

char puzzle[16][20];

bool read() {
  for(int i = 0; i < 16; i++)
    if(scanf("%s", puzzle[i]) != 1) return false;
  return true;
}

int main() {
  int kase = 0;
  while(read()) {
    if(++kase != 1) printf("\n");
    solver.init(1024);
    for(int r = 0; r < 16; r++)
      for(int c = 0; c < 16; c++) 
        for(int v = 0; v < 16; v++)
          if(puzzle[r][c] == '-' || puzzle[r][c] == 'A'+v) {
            vector<int> columns;
            columns.push_back(encode(SLOT, r, c));
            columns.push_back(encode(ROW, r, v));
            columns.push_back(encode(COL, c, v));
            columns.push_back(encode(SUB, (r/4)*4+c/4, v));
            solver.addRow(encode(r, c, v), columns);
          }

    vector<int> ans;
    assert(solver.solve(ans));

    for(int i = 0; i < ans.size(); i++) {
      int r, c, v;
      decode(ans[i], r, c, v);
      puzzle[r][c] = 'A'+v;
    }
    for(int i = 0; i < 16; i++)
      printf("%s\n", puzzle[i]);
  }
  return 0;
}
// Accepted 641ms 904kB 3295 G++2020-12-23 17:11:54|O22227210
```

### LA3789/UVa12112 Iceman

```cpp
// LA3789/UVa12112 Iceman
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<string>
#include<map>
#include<queue>
using namespace std;

int n, m, target;
map<string, string> sol;
queue<string> q;

bool icy[256];
char link_l[256], link_r[256], clear_l[256], clear_r[256];

void init(){
  memset(icy, 0, sizeof(icy));
  icy['O'] = icy['['] = icy[']'] = icy['='] = true;
  memset(link_l, ' ', sizeof(link_l));
  link_l['O'] = ']'; link_l['['] = '=';
  memset(link_r, ' ', sizeof(link_r));
  link_r['O'] = '['; link_r[']'] = '=';
  memset(clear_l, ' ', sizeof(clear_l));
  clear_l[']'] = 'O'; clear_l['='] = '['; clear_l['O'] = 'O'; clear_l['['] = '[';
  memset(clear_r, ' ', sizeof(clear_r));
  clear_r['['] = 'O'; clear_r['='] = ']'; clear_r['O'] = 'O'; clear_r[']'] = ']';
}

string fall(string s){
  int k, r, p;
  for(int i = n-1; i >=0; i--)
    for(int j = 0; j < m; j++){
      char ch = s[i*m+j];
      if(ch == 'O' || ch == '@'){
        for(k = i+1; k < n; k++) if(s[k*m+j] != '.') break;
        s[i*m+j] = '.'; s[(k-1)*m+j] = ch;
      }else if(ch == '['){
        for(r = j+1; r < m; r++) if(s[i*m+r] == 'X' || s[i*m+r] == ']') break;
        if(s[i*m+r] == ']'){
          for(k = i+1; k < n; k++){
            bool found = false;
            for(p = j; p <= r; p++) if(s[k*m+p] != '.'){ found = true; break; }
            if(found) break;
          }
          for(p = j; p <= r; p++) s[i*m+p] = '.';
          for(p = j+1; p < r; p++) s[(k-1)*m+p] = '=';                        
          s[(k-1)*m+j] = '['; s[(k-1)*m+r] = ']';
        }
        j = r;
      }
    }
  return s;
}

int h(string s){
  int a, b, x = s.find('@');
  a = x%m - target%m; if(a < 0) a = -a;
  if(x/m > target/m) b = x/m - target/m; else b = (x/m < target/m ? 1 : 0);    
  return a > b ? a : b;
}

bool expand(string s, char cmd){
  string seq = sol[s] + cmd;   
  int x = s.find('@');
  s[x] = '.';
  if(cmd == '<' || cmd == '>'){
    s[x] = '@';
    int p = (cmd == '<' ? x+m-1 : x+m+1);
    if(s[p] == 'X') return false;
    else if(s[p] == '.'){
      s[p] = 'O';
      if(icy[s[p-1]]) s[p-1] = link_r[s[p-1]]; 
      if(s[p-1] != '.') s[p] = link_l[s[p]]; 
      if(icy[s[p+1]]) s[p+1] = link_l[s[p+1]];
      if(s[p+1] != '.') s[p] = link_r[s[p]];
    }else{
      s[p] = '.';
      if(icy[s[p-1]]) s[p-1] = clear_r[s[p-1]];
      if(icy[s[p+1]]) s[p+1] = clear_l[s[p+1]];
    }
  }else{
    int p = (cmd == 'L' ? x-1 : x+1);
    if(s[p] == '.') s[p] = '@';
    else{
      if(s[p] == 'O'){
        int k;
        if(cmd == 'L' && s[p-1] == '.'){
            for(k = p-1; k > 0; k--) if(s[k-1] != '.' || s[k+m] == '.') break;
            s[p] = '.'; s[k] = 'O'; s[x] = '@';
        }
        if(cmd == 'R' && s[p+1] == '.'){
            for(k = p+1; k < n*m; k++) if(s[k+1] != '.' || s[k+m] == '.') break;
            s[p] = '.'; s[k] = 'O'; s[x] = '@';
        }
      }
      if(s[p] != '.'){
        if(s[p-m] == '.' && s[x-m] == '.') s[p-m] = '@'; else s[x] = '@';
      }
   }
  }  
  s = fall(s);
  if(h(s) + seq.length() > 15) return false;
  if(s.find('@') == target){ printf("%s\n", seq.c_str()); return true; }
  if(!sol.count(s)){ sol[s] = seq; q.push(s); }
  return false;
}

int main(){
  int caseno = 0;
  init();
  while(scanf("%d%d", &n, &m) == 2){
    if(!n) break;
    char map[20][20];  
    for(int i = 0; i < n; i++) scanf("%s", map[i]);
    string s = "";
    for(int i = 0; i < n; i++)
      for(int j = 0; j < m; j++){
        if(map[i][j] == '#'){ target = i*m + j; map[i][j] = '.'; }
        s += map[i][j];
      }
    q.push(s);
    sol.clear();
    sol[s] = "";
    printf("Case %d: ", ++caseno);
    while(!q.empty()){
      string s = q.front();
      q.pop();
      if(expand(s, '<')) break; if(expand(s, '>')) break;
      if(expand(s, 'L')) break; if(expand(s, 'R')) break;
    }
    while(!q.empty()) q.pop();        
  }
}
// 25878414	12112	Iceman	Accepted	C++	0.040	2020-12-23 09:13:13
```

### UVa1085 House of Cards

```cpp
// UVa1085 House of Cards
// 刘汝佳
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<vector>
using namespace std;

const int UP = 0, FLOOR = 1, DOWN = 2, maxn = 20;
int n, deck[maxn*2];
struct State {
  int card[8], type[8]; // 两张相同的FLOOR牌代表一张真实的FLOOR牌
  int hold[2], pos, score; // MAX游戏者(即Axel)的得分
  State child() const {
    State s;
    memcpy(&s, this, sizeof(s));
    s.pos = pos + 1;
    return s;
  }

  State() {
    for(int i = 0; i < 8; i++) {
      card[i] = deck[i];
      type[i] = i % 2 == 0 ? UP : DOWN;
    }
    hold[0] = hold[1] = score = 0;
    pos = 8;
  }

  bool isFinal() {
    if(pos == 2*n) {
      score += hold[0] + hold[1];
      hold[0] = hold[1] = 0;
      return true;
    }
    return false;
  }

  int getScore(int c1, int c2, int c3) const {
    int S = abs(c1) + abs(c2) + abs(c3);
    int cnt = 0;
    if(c1 > 0) cnt++; if(c2 > 0) cnt++; if(c3 > 0) cnt++;
    return cnt >= 2 ? S : -S;
  }

  void expand(int player, vector<State>& ret) const {
    int cur = deck[pos];

    // 决策1：拿在手里
    if(hold[player] == 0) {
      State s = child();
      s.hold[player] = cur;
      ret.push_back(s);
    }

    // 决策2：摆楼面牌
    for(int i = 0; i < 7; i++) if(type[i] == DOWN && type[i+1] == UP) {
      // 用当前的牌
      State s = child();
      s.score += getScore(card[i], card[i+1], cur);
      s.type[i] = s.type[i+1] = FLOOR;
      s.card[i] = s.card[i+1] = cur;
      ret.push_back(s);
      
      if(hold[player] != 0) {
        // 用手里的牌
        State s = child();
        s.score += getScore(card[i], card[i+1], hold[player]);
        s.type[i] = s.type[i+1] = FLOOR; 
        s.card[i] = s.card[i+1] = hold[player];
        s.hold[player] = cur;
        ret.push_back(s);
      }
    }

    // 决策3：新的山峰
    if(hold[player] != 0)
      for(int i = 0; i < 7; i++) if(type[i] == FLOOR && type[i+1] == FLOOR && card[i] == card[i+1]) {
        State s = child();
        s.score += getScore(card[i], hold[player], cur);
        s.type[i] = UP; s.type[i+1] = DOWN; 
        s.card[i] = cur; s.card[i+1] = hold[player]; s.hold[player] = 0;
        ret.push_back(s);

        swap(s.card[i], s.card[i+1]);
        ret.push_back(s);
      }
  }
};

// 带alpha-beta剪枝的对抗搜索
int alphabeta(State& s, int player, int alpha, int beta) {
  if(s.isFinal()) return s.score; // 终态

  vector<State> children;
  s.expand(player, children); // 扩展子结点

  int n = children.size();
  for(int i = 0; i < n; i++) {
    int v = alphabeta(children[i], player^1, alpha, beta);
    if(!player) alpha = max(alpha, v); else beta = min(beta, v);
    if(beta <= alpha) break; // alpha-beta剪枝
  }
  return !player ? alpha : beta;
}
const int INF = 1e9;

int main() {
  int kase = 0;
  char P[10];
  while(scanf("%s", P) == 1 && P[0] != 'E') {
    scanf("%d", &n);
    for(int i = 0; i < n*2; i++) {
      char ch;
      scanf("%d%c", &deck[i], &ch);
      if(ch == 'B') deck[i] = -deck[i];
    }
    State initial;
    int first_player = deck[0] > 0 ? 0 : 1, score = alphabeta(initial, first_player, -INF, INF);
    if(P[0] == 'B') score = -score;
    printf("Case %d: ", ++kase);
    if(score == 0) printf("Axel and Birgit tie\n");
    else if(score > 0) printf("%s wins %d\n", P, score);
    else printf("%s loses %d\n", P, -score);
  }
  return 0;
}
// 25878419	1085	House of Cards	Accepted	C++	0.470	2020-12-23 09:14:12
```

## 6.4 几何专题

### LA2397/UVa1060 Collecting Luggage

```cpp
// LA2397/UVa1060 Collecting Luggage
// Rujia Liu
#include<cstdio>
#include<cstdlib>
#include<cmath>
#include<cstring>
#include<vector>
#include<queue>
#include<algorithm>
using namespace std;

const double eps = 1e-10;
int dcmp(double x) {
  if(fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}

struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

Vector operator + (const Vector& A, const Vector& B) { return Vector(A.x+B.x, A.y+B.y); }
Vector operator - (const Point& A, const Point& B) { return Vector(A.x-B.x, A.y-B.y); }
Vector operator * (const Vector& A, double p) { return Vector(A.x*p, A.y*p); }

bool operator < (const Point& a, const Point& b) {
  return a.x < b.x || (a.x == b.x && a.y < b.y);
}

bool operator == (const Point& a, const Point &b) {
  return dcmp(a.x-b.x) == 0 && dcmp(a.y-b.y) == 0;
}

double Dot(const Vector& A, const Vector& B) { return A.x*B.x + A.y*B.y; }
double Cross(const Vector& A, const Vector& B) { return A.x*B.y - A.y*B.x; }
double Length(Vector A) { return sqrt(Dot(A, A)); }

bool SegmentProperIntersection(const Point& a1, const Point& a2, const Point& b1, const Point& b2) {
  double c1 = Cross(a2-a1,b1-a1), c2 = Cross(a2-a1,b2-a1),
  c3 = Cross(b2-b1,a1-b1), c4=Cross(b2-b1,a2-b1);
  return dcmp(c1)*dcmp(c2)<0 && dcmp(c3)*dcmp(c4)<0;
}

bool OnSegment(const Point& p, const Point& a1, const Point& a2) {
  return dcmp(Cross(a1-p, a2-p)) == 0 && dcmp(Dot(a1-p, a2-p)) < 0;
}

int isPointInPolygon(const Point& p, Point* poly, int n){
  int wn = 0;
  for(int i = 0; i < n; i++){
    const Point& p1 = poly[i];
    const Point& p2 = poly[(i+1)%n];
    if(p1 == p || p2 == p || OnSegment(p, p1, p2)) return -1; // 在边界上
    int k = dcmp(Cross(p2-p1, p-p1));
    int d1 = dcmp(p1.y - p.y);
    int d2 = dcmp(p2.y - p.y);
    if(k > 0 && d1 <= 0 && d2 > 0) wn++;
    if(k < 0 && d2 <= 0 && d1 > 0) wn--;
  }
  if (wn != 0) return 1; // 内部
  return 0; // 外部
}

const int maxn = 100 + 10;
const int INF = 1000000000;

struct Edge {
  int from, to;
  double dist;
};

struct HeapNode {
  double d;
  int u;
  bool operator < (const HeapNode& rhs) const {
    return d > rhs.d;
  }
};

struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[maxn];
  bool done[maxn];    // 是否已永久标号
  double d[maxn];     // s到各个点的距离
  int p[maxn];        // 最短路中的上一条弧

  void init(int n) {
    this->n = n;
    for(int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, double dist) {
    edges.push_back((Edge){from, to, dist});
    m = edges.size();
    G[from].push_back(m-1);
  }

  void dijkstra(int s) {
    priority_queue<HeapNode> Q;
    for(int i = 0; i < n; i++) d[i] = INF;
    d[s] = 0;
    memset(done, 0, sizeof(done));
    Q.push((HeapNode){0, s});
    while(!Q.empty()) {
      HeapNode x = Q.top(); Q.pop();
      int u = x.u;
      if(done[u]) continue;
      done[u] = true;
      for(int i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if(d[e.to] > d[u] + e.dist) {
          d[e.to] = d[u] + e.dist;
          p[e.to] = G[u][i];
          Q.push((HeapNode){d[e.to], e.to});
        }
      }
    }
  }
};

int n;
Point startp, belt[maxn]; // 为了方便，belt[n]是起点，belt[n+1]是终点
double vl, vp, perimeter, len[maxn];
Dijkstra solver;

// 边a-b是否被挡住
bool isBlocked(int a, int b) {
  for(int i = 0; i < n+2; i++)
    if(i != a && i != b && OnSegment(belt[i], belt[a], belt[b])) return true; // 中间不能有其他点
  for(int i = 0; i < n; i++)
    if(SegmentProperIntersection(belt[i], belt[(i+1)%n], belt[a], belt[b])) return true; // 不能和多边形的边规范相交
  Point midp = (belt[a] + belt[b]) * 0.5;
  if(isPointInPolygon(midp, belt, n) == 1) return true; // 整条线段在多边形内
  return false;
}

// 判断是否可以在时刻t拿到行李
bool check(double t) {
  solver.init(n+2); // 0~n-1是传送带顶点，n是起点，n+1是终点

  // 计算行李位置，存放到belt[n+1]
  double dist = fmod(vl*t, perimeter);
  for(int i = 0; i < n; i++) {
    if(len[i] >= dist) {
      belt[n+1] = belt[i] + (belt[(i+1)%n] - belt[i]) * (dist / len[i]);
      break;
    }
    dist -= len[i];
  }

  // 构图
  for(int i = 0; i < n+2; i++)
    for(int j = i+1; j < n+2; j++) {
      double d = Length(belt[i]-belt[j]);
      if(d > eps && isBlocked(i, j)) continue;
      solver.AddEdge(i, j, d);
      solver.AddEdge(j, i, d);
    }
  solver.dijkstra(n);
  return solver.d[n+1] <= vp*t;
}

int getSecond(double t) {
  return (int)floor(t * 60 + 0.5);
}

int main() {
  int kase = 0;
  while(scanf("%d", &n) == 1 && n > 0) {
    for(int i = 0; i < n; i++) scanf("%lf%lf", &belt[i].x, &belt[i].y);
    scanf("%lf%lf%lf%lf", &startp.x, &startp.y, &vl, &vp);
    perimeter = 0;
    double closest = 1e9;
    for(int i = 0; i < n; i++) {
      closest = min(closest, Length(startp - belt[i])); // 更新人到最近顶点的距离
      len[i] = Length(belt[i] - belt[(i+1)%n]);
      perimeter += len[i]; // 累加周长
    }
    belt[n] = startp;
    double L = 0, R = (closest + perimeter / 2) / vp; // 上界为人走到最近顶点再走半周长所需要的时间
    while(getSecond(L) != getSecond(R)) { // 这样写最保险。L和R很接近不代表四舍五入到“秒”后一定一样
      double M = L + (R-L)/2;
      if(check(M)) R = M; else L = M;
    }
    int t = getSecond(L);
    printf("Case %d: Time = %d:%02d\n", ++kase, t / 60, t % 60);
  }
  return 0;
}
// 25878459	1060	Collecting Luggage	Accepted	C++	0.200	2020-12-23 09:19:12
```

### LA3532/UVa1367 Nuclear Plants

```cpp
// LA3532/UVa1367 Nuclear Plants
// 刘汝佳
#include<cstdio>
#include<cmath>
#include<cstring>
#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

const double eps = 5 * 1e-13;
int dcmp(double x) {
  if(fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}

const double PI = acos(-1);
const double TWO_PI = PI * 2;

double NormalizeAngle(double rad, double center = PI) {
  return rad - TWO_PI * floor((rad + PI - center) / TWO_PI);
}

struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

Vector operator + (Vector A, Vector B) { return Vector(A.x+B.x, A.y+B.y); }
Vector operator - (Point A, Point B) { return Vector(A.x-B.x, A.y-B.y); }
Vector operator * (Vector A, double p) { return Vector(A.x*p, A.y*p); }
Vector operator / (Vector A, double p) { return Vector(A.x/p, A.y/p); }

// 理论上这个“小于”运算符是错的，因为可能有三个点a, b, c, a和b很接近（即a<b好b<a都不成立），b和c很接近，但a和c不接近
// 所以使用这种“小于”运算符的前提是能排除上述情况
bool operator < (const Point& a, const Point& b) {
  return dcmp(a.x - b.x) < 0 || (dcmp(a.x - b.x) == 0 && dcmp(a.y - b.y) < 0);
}

bool operator == (Point A, Point B) {
  return dcmp(A.x - B.x) == 0 && dcmp(A.y - B.y) == 0;
}

double Dot(Vector A, Vector B) { return A.x*B.x + A.y*B.y; }
double Length(Vector A) { return sqrt(Dot(A, A)); }
double Cross(Vector A, Vector B) { return A.x*B.y - A.y*B.x; }

double angle(Vector v) {
  return atan2(v.y, v.x);
}

bool OnSegment(const Point& p, const Point& a1, const Point& a2) {
  return dcmp(Cross(a1-p, a2-p)) == 0 && dcmp(Dot(a1-p, a2-p)) < 0;
}

// 交点相对于圆1的极角保存在rad中
void getCircleCircleIntersection(Point c1, double r1, Point c2, double r2, vector<double>& rad) {
  double d = Length(c1 - c2);
  if(dcmp(d) == 0) return; // 不管是内含还是重合，都不相交
  if(dcmp(r1 + r2 - d) < 0) return;
  if(dcmp(fabs(r1-r2) - d) > 0) return;

  double a = angle(c2 - c1);
  double da = acos((r1*r1 + d*d - r2*r2) / (2*r1*d));
  rad.push_back(NormalizeAngle(a-da));
  rad.push_back(NormalizeAngle(a+da));
}

Point GetLineProjection(Point P, Point A, Point B) {
  Vector v = B-A;
  return A+v*(Dot(v, P-A) / Dot(v, v));
}

// 直线AB和圆心为C，半径为r的圆的交点。相对于圆的极角保存在rad中
void getLineCircleIntersection(Point A, Point B, Point C, double r, vector<double>& rad){
  Point p = GetLineProjection(C, A, B);
  double a = angle(p - C);
  double d = Length(p - C);
  if(dcmp(d - r) > 0) return;
  if(dcmp(d) == 0) { // 过圆心
    rad.push_back(NormalizeAngle(angle(A - B)));
    rad.push_back(NormalizeAngle(angle(B - A)));
  }
  double da = acos(d / r);
}

/////////// 题目相关
const int maxn = 200 + 5;
int n, N, M; // n是圆的总数，N和M是场地长宽
Point P[maxn];
double R[maxn];

// 取圆no弧度为rad的点
Point getPoint(int no, double rad) {
  return Point(P[no].x + cos(rad)*R[no], P[no].y + sin(rad)*R[no]);
}

// 第no个圆弧度为rad的点是否可见。相同的圆只有编号最小的可见（虽然对于本题来说不必要）
bool visible(int no, double rad) {
  Point p = getPoint(no, rad);
  if(p.x < 0 || p.y < 0 || p.x > N || p.y > M) return false;
  for(int i = 0; i < n; i++) {
    if(P[no] == P[i] && dcmp(R[no] - R[i]) == 0 && i < no) return false;
    if(dcmp(Length(p - P[i]) - R[i]) < 0) return false;
  }
  return true;
}

// 场地边界上的点p是否可见
bool visible(Point p) {
  for(int i = 0; i < n; i++) {
    if(dcmp(Length(p - P[i]) - R[i]) <= 0) return false;
  }
  return true;
}

// 求圆的并在(0,0)-(N,M)内的面积
// 使用一般曲边图形的面积算法。下文中，“所求图形”指的是不能种菜的区域，它的边界由圆弧和直线段构成。
// 算法：对于所求图形边界上的每一段（可以是曲线）a~>b，累加Cross(a, b)和它在直线段a->b右边部分的面积（左边部分算负）
// 边界计算：
// 1. 每个圆被其他圆和场地边界分成了若干条圆弧，中点不被其他圆覆盖且在场地内的圆弧在所求图形边界上
// 2. 场地的四条边界被圆分成了若干条线段。中点在某个圆内部的线段在所求图形边界上
double getArea() {
  Point b[4];
  b[0] = Point(0, 0);
  b[1] = Point(N, 0);
  b[2] = Point(N, M);
  b[3] = Point(0, M);
  double area = 0;

  // 圆弧部分
  for(int i = 0; i < n; i++) {
    vector<double> rad;
    rad.push_back(0);
    rad.push_back(PI*2);

    // 圆和边界的交点
    for(int j = 0; j < 4; j++)
      getLineCircleIntersection(b[j], b[(j+1)%4], P[i], R[i], rad);

    // 圆和圆的交点
    for(int j = 0; j < n; j++)
      getCircleCircleIntersection(P[i], R[i], P[j], R[j], rad);
    
    sort(rad.begin(), rad.end());
    for(int j = 0; j < rad.size()-1; j++) if(rad[j+1] - rad[j] > eps) {
      double mid = (rad[j] + rad[j+1]) / 2.0; // 圆弧中点相对于圆i圆心的极角
      if(visible(i, mid)) { // 弧中点可见，因此弧在图形边界上
        area += Cross(getPoint(i, rad[j]), getPoint(i, rad[j+1])) / 2.0;
        double a = rad[j+1] - rad[j];
        area += R[i] * R[i] * (a - sin(a)) / 2.0;
      }
    }
  }

  // 直线段部分
  for(int i = 0; i < 4; i++) {
    Vector v = b[(i+1)%4] - b[i];
    double len = Length(v);

    vector<double> dist;
    dist.push_back(0);
    dist.push_back(len);
    for(int j = 0; j < n; j++) {
      vector<double> rad;
      getLineCircleIntersection(b[i], b[(i+1)%4], P[j], R[j], rad);
      for(int k = 0; k < rad.size(); k++) {
        Point p = getPoint(j, rad[k]);
        dist.push_back(Length(p - b[i]));
      }
    }

    sort(dist.begin(), dist.end()); // 必须按照到起点的距离排序而不是按照点的字典序排序，否则向量方向可能会反
    vector<Point> points;
    for(int j = 0; j < dist.size(); j++)
      points.push_back(b[i] + v * (dist[j] / len));

    for(int j = 0; j < dist.size()-1; j++) {
      Point midp = (points[j] + points[j+1]) / 2.0;
      if(!visible(midp)) area += Cross(points[j], points[j+1]) / 2.0; // 线段中点不可见，因此线段在图形边界上
    }
  }

  return N*M - area;
}

int main() {
  int ks, kl;
  while(scanf("%d%d%d%d", &N, &M, &ks, &kl) == 4 && N && M) {
    for(int i = 0; i < ks; i++) { scanf("%lf%lf", &P[i].x, &P[i].y); R[i] = 0.58; }
    sort(P, P+ks);
    ks = unique(P, P+ks) - P;
    for(int i = 0; i < kl; i++) { scanf("%lf%lf", &P[ks+i].x, &P[ks+i].y); R[ks+i] = 1.31; }
    sort(P+ks, P+ks+kl);
    n = unique(P+ks, P+ks+kl) - P;
    printf("%.2lf\n", getArea());
  }
  return 0;
}
// Accepted 220ms 5686 C++5.3.0 2020-12-14 15:34:52 25846126
```

### LA3809/UVa1065 Raising the Roof

```cpp
// LA3809/UVa1065 Raising the Roof
// Rujia Liu
// 寻找top时改用简单循环寻找，效率稍低但代码简单
#include <cmath>
#include <cstdio>
#define REP(i, n) for (int i = 0; i < (n); ++i)

const double eps = 1e-8;
int dcmp(double x) {
  if (fabs(x) < eps) return 0;
  return x < 0 ? -1 : 1;
}

struct Point3 {
  int x, y, z;
  Point3(int x = 0, int y = 0, int z = 0) : x(x), y(y), z(z) {}
};

typedef Point3 Vector3;

Vector3 operator-(const Point3& A, const Point3& B) {
  return Vector3(A.x - B.x, A.y - B.y, A.z - B.z);
}

int Dot(const Vector3& A, const Vector3& B) {
  return A.x * B.x + A.y * B.y + A.z * B.z;
}
double Length(const Vector3& A) { return sqrt(Dot(A, A)); }
Vector3 Cross(const Vector3& A, const Vector3& B) {
  return Vector3(A.y * B.z - A.z * B.y, A.z * B.x - A.x * B.z,
                 A.x * B.y - A.y * B.x);
}

#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <vector>
using namespace std;

const int maxn = 300 + 10, maxt = 1000 + 10;
Point3 p[maxn];
int n, m;
int t[maxt][3];
Vector3 normal[maxt];  // 三角形i的法向量
double d[maxt];        // 三角形i的点法式为Dot(normal[i], p) = d
double area_ratio[maxt];  // 三角形i的投影面积乘以area_ratio[i]就是实际面积

// 输入中有在竖直平面内（即normal[i].z=0）的三角形，但主算法会自动忽略它们，不用担心area_ratio[i]不存在
void init() {
  for (int i = 0; i < m; i++) {
    Point3 p0 = p[t[i][0]], p1 = p[t[i][1]], p2 = p[t[i][2]];
    normal[i] = Cross(p1 - p0, p2 - p0);
    d[i] = Dot(normal[i], p0);
    if (normal[i].z != 0)
      area_ratio[i] = fabs((double)Length(normal[i]) / normal[i].z);
  }
}

inline double getTriangleZ(int idx, double x, double y) {
  return (d[idx] - normal[idx].x * x - normal[idx].y * y) / normal[idx].z;
}

struct Event {
  int id;    // 涉及到的三角形编号
  double y;  // 与扫描线交点的y坐标
  Event(int id, double y) : id(id), y(y) {}
  bool operator<(const Event& rhs) const { return y < rhs.y; }
};

double solve() {
  // 离散化
  vector<double> sx;
  for (int i = 1; i <= n; i++) sx.push_back(p[i].x);
  REP(i, m) REP(j, m) REP(a, 3) REP(b, 3) {
    // 求pa-pb和qa-qb投影到XY平面后的交点。直接解参数方程
    Point3 pa = p[t[i][a]];
    Point3 pb = p[t[i][(a + 1) % 3]];
    Point3 qa = p[t[j][b]];
    Point3 qb = p[t[j][(b + 1) % 3]];
    int dpx = pb.x - pa.x;
    int dpy = pb.y - pa.y;
    int dqx = qb.x - qa.x;
    int dqy = qb.y - qa.y;
    int deno = dpx * dqy - dpy * dqx;
    if (deno == 0) continue;
    double t = (double)(dqy * (qa.x - pa.x) + dqx * (pa.y - qa.y)) / deno;
    double s = (double)(dpy * (qa.x - pa.x) + dpx * (pa.y - qa.y)) / deno;
    if (t > 1 || t < 0 || s > 1 || s < 0) continue;
    sx.push_back(pa.x + t * dpx);
  }
  sort(sx.begin(), sx.end());
  sx.erase(unique(sx.begin(), sx.end()), sx.end());

  double ans = 0;
  for (int i = 0; i < sx.size() - 1; i++) {
    // 扫描线位于x = xx
    double xx = (sx[i] + sx[i + 1]) / 2;
    // 计算扫描线穿过的三角形集合，为每个三角形创建“进入”和“离开”事件
    vector<Event> events;
    REP(j, m) if (normal[j].z != 0) REP(a, 3) {  // 忽略竖直平面内的三角形
      Point3 pa = p[t[j][a]], pb = p[t[j][(a + 1) % 3]];
      // 计算扫描线x = xx和pa-pb在平面XY上投影的交点
      if (pa.x == pb.x) continue;  // 竖直线段
      if (!(min(pa.x, pb.x) <= sx[i] && max(pa.x, pb.x) >= sx[i + 1]))
        continue;  // 不在竖直条内
      double y = pa.y + (pb.y - pa.y) * (xx - pa.x) / (pb.x - pa.x);  // 解方程
      events.push_back(Event(j, y));
    }
    if (events.empty()) continue;

    // 按照y递增的顺序处理事件
    int inside[maxt];
    fill_n(inside, maxt, 0), sort(events.begin(), events.end());
    for (int j = 0; j < events.size() - 1; j++) {
      inside[events[j].id] ^= 1;
      if (fabs(events[j].y - events[j + 1].y) < eps)
        continue;  // y相同的事件要等到所有inside更新完毕后才能处理

      // 投影梯形的面积等于中线乘以高
      double proj_are = (sx[i + 1] - sx[i]) * (events[j + 1].y - events[j].y);

      // 在下一个事件发生之前，哪个三角形在最上面？
      int top = -1;  // 测试y坐标中点，计算zz误差比较小
      double topz = -1e9, yy = (events[j].y + events[j + 1].y) / 2;
      for (int k = 0; k < m; k++)
        if (inside[k]) {
          double zz = getTriangleZ(k, xx, yy);
          if (zz > topz) topz = zz, top = k;  // 更新最上面的三角形编号top
        }

      // 投影部分面积乘以比例系数等于实际面积
      if (top >= 0) ans += area_ratio[top] * proj_are;
    }
  }
  return ans;
}

int main() {
  int kase = 0;
  while (scanf("%d%d", &n, &m) == 2 && n > 0) {
    for (int i = 1; i <= n; i++)
      scanf("%d%d%d", &p[i].x, &p[i].y, &p[i].z);  // 顶点编号为1~n
    for (int i = 0; i < m; i++) scanf("%d%d%d", &t[i][0], &t[i][1], &t[i][2]);
    init();
    double ans = solve();
    printf("Case %d: %.2lf\n\n", ++kase, ans);
  }
  return 0;
}
// Accepted 490ms 4467 C++ 5.3.0 2020-12-14 15:43:47O25846165
```

### LA4125/UVa1075 Painter

```cpp
// LA4125/UVa1075 Painter
// 刘汝佳
#include <cstdio>
#include <cstdlib>
#include <map>
#include<algorithm>
using namespace std;

typedef long long LL;

struct Point {
  int x, y;
  Point(int x = 0, int y = 0):x(x),y(y){}
  void read() { scanf("%d%d", &x, &y); }
  bool operator < (const Point& p) const {
    return x < p.x || x == p.x && y < p.y;
  }
  Point operator - (const Point& rhs) const {
    return Point(x - rhs.x, y - rhs.y);
  }
};

int icmp(LL x) {
  if(x == 0) return 0;
  return x > 0 ? 1 : -1;
}

inline LL Cross(Point p, Point p1, Point p2) {
  return (LL)(p1.x - p.x) * (LL)(p2.y - p.y) - (LL)(p1.y - p.y)*(LL)(p2.x - p.x);
}

// 由于线段相交判定执行次数较大，这里采用了一些小优化
inline bool SegmentIntersection(const Point& a1, const Point& a2, const Point& b1, const Point& b2) {
  if(min(a1.x, a2.x) > max(b1.x, b2.x)) return false; // 快速排除
  if(min(a1.y, a2.y) > max(b1.y, b2.y)) return false;
  if(max(a1.x, a2.x) < min(b1.x, b2.x)) return false;
  if(max(a1.y, a2.y) < min(b1.y, b2.y)) return false;
  LL c1 = Cross(a1, a2, b1), c2 = Cross(a1, a2, b2);
  if(icmp(c1) * icmp(c2) > 0) return false;
  LL c3 = Cross(b1, b2, a1), c4 = Cross(b1, b2, a2);
  return icmp(c3) * icmp(c4) <= 0;
}

int curx;
const double eps = 1e-6;

struct Segment {
  Point p1, p2;
  int no; // 三角形编号
  double d;
  Segment(Point p1, Point p2, int no):p1(p1),p2(p2),no(no) {
    d = (p2.y - p1.y) / (p2.x + eps - p1.x);
  }
  double y() const { return p1.y + d * (curx + eps - p1.x); }
  bool operator < (const Segment& rhs) const { return y() < rhs.y(); }
};

inline bool Intersect(const Segment& a, const Segment& b) {
  if(a.no == b.no) return false;
  return SegmentIntersection(a.p1, a.p2, b.p1, b.p2);
}

bool error;    // 是否已经出现相交线段
int max_depth; // 当前最大深度

const int INF = 200000;

// 本题这样做可以提高代码可读性，但不要在工程中这样使用，非常危险
#define L first   
#define depth second

// 扫描线类，用一个multimap实现
struct Scanline {
  multimap<Segment, int> line;
  typedef multimap<Segment, int>::iterator Pos;
  void init() {
    line.clear();
    line.insert(make_pair(Segment(Point(-INF,-INF), Point(INF,-INF), -1), 1));
    line.insert(make_pair(Segment(Point(-INF, INF), Point(INF, INF), -1), 0));
  }
  inline Pos Prev(const Pos& p) const { return --Pos(p); }
  inline Pos Next(const Pos& p) const { return ++Pos(p); }
  inline Pos Insert(const Segment& s, int d = 0) {
    Pos x = line.insert(make_pair(s, d));
    if(Intersect(x->L, Prev(x)->L) || Intersect(x->L, Next(x)->L)) error = true;
    return x;
  }  
  inline void Erase(const Pos& x) {
    if(Intersect(Prev(x)->L, Next(x)->L)) error = true;
    line.erase(x);
  }
} scanline;

struct Triangle {
  int no; // 编号
  Point P[3];
  Scanline::Pos p12, p13, p23;
  void read(int no) {
    this->no = no;
    for(int i = 0; i < 3; i++) scanf("%d%d", &P[i].x, &P[i].y);
    sort(P, P+3);
  }
  // 更新x1和x2的depth。其中x1是p12和p13中y较小的那个，x2是另一个（即Next(x1)=x2）
  void updateDepth(const Scanline::Pos& x1, Scanline::Pos& x2) {
    int d = scanline.Prev(x1)->depth + 1;
    max_depth = max(max_depth, d);
    x1->depth = d;
    x2->depth = d - 1;
  }
  // 处理第v个结点
  void process(int v) {
    if(v == 0) {
      p12 = scanline.Insert(Segment(P[0], P[1], no));
      p13 = scanline.Insert(Segment(P[0], P[2], no));
      scanline.Next(p12) == p13 ? updateDepth(p12, p13) : updateDepth(p13, p12);
    }
    else if(v == 1) {
      p23 = scanline.Insert(Segment(P[1], P[2], no), p12->depth);
      scanline.Erase(p12);
    }
    else {
      scanline.Erase(p13);
      scanline.Erase(p23);
    }
  }
};

struct Event {
  int x, t, v; // x坐标，三角形编号和顶点编号
  Event(){}
  Event(int x, int t, int v):x(x),t(t),v(v){}
  bool operator < (const Event& rhs) const {
    return x < rhs.x || x == rhs.x && v < rhs.v;
  }
};

const int maxn = 100000 + 10; // 最大三角形个数
Triangle tri[maxn];
Event events[maxn*3];

int main() {
  int n, kase = 0;
  while(scanf("%d",&n) == 1 && n >= 0) {
    error = false;
    max_depth = 1;
    scanline.init();
    for(int i = 0; i < n; i++) {
      tri[i].read(i);
      for(int j = 0; j < 3; j++)
        events[i*3+j] = Event(tri[i].P[j].x, i, j);
    }
    sort(events, events+n*3);
    for(int i = 0; i < n*3; i++) {
      curx = events[i].x;
      tri[events[i].t].process(events[i].v);
      if(error) break;
    }
    if(!error) printf("Case %d: %d shades\n", ++kase, max_depth);
    else printf("Case %d: ERROR\n", ++kase);
  }
  return 0;
}
// Accepted 710ms 4355 C++5.3.0 2020-12-14 15:46:00 25846168
```

### UVa1077 The Sky is the Limit

```cpp
// UVa1077 The Sky is the Limit
// 刘汝佳
#include<cstdio>
#include<cmath>
#include<algorithm>
using namespace std;

const double eps = 1e-10;
int dcmp(double x) {
  if(fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}

struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

Vector operator + (const Vector& A, const Vector& B) { return Vector(A.x+B.x, A.y+B.y); }
Vector operator - (const Point& A, const Point& B) { return Vector(A.x-B.x, A.y-B.y); }
Vector operator * (const Vector& A, double p) { return Vector(A.x*p, A.y*p); }

bool operator < (const Point& a, const Point& b) {
  return a.x < b.x || (a.x == b.x && a.y < b.y);
}

bool operator == (const Point& a, const Point &b) {
  return dcmp(a.x-b.x) == 0 && dcmp(a.y-b.y) == 0;
}

double Dot(const Vector& A, const Vector& B) { return A.x*B.x + A.y*B.y; }
double Cross(const Vector& A, const Vector& B) { return A.x*B.y - A.y*B.x; }
double Length(const Vector& A) { return sqrt(Dot(A, A)); }

Point GetLineIntersection(const Point& P, const Vector& v, const Point& Q, const Vector& w) { 
  Vector u = P-Q;
  double t = Cross(w, u) / Cross(v, w);
  return P+v*t;
}

bool SegmentProperIntersection(const Point& a1, const Point& a2, const Point& b1, const Point& b2) {
  double c1 = Cross(a2-a1,b1-a1), c2 = Cross(a2-a1,b2-a1),
  c3 = Cross(b2-b1,a1-b1), c4=Cross(b2-b1,a2-b1);
  return dcmp(c1)*dcmp(c2)<0 && dcmp(c3)*dcmp(c4)<0;
}

const int maxn = 100 + 10;
Point P[maxn], L[maxn][2][2];
double x[maxn*maxn];

int main() {
  int n, kase = 0;
  while(scanf("%d", &n) == 1 && n) {
    int c = 0;
    for(int i = 0; i < n; i++) {
      double X, H, B;
      scanf("%lf%lf%lf", &X, &H, &B);
      L[i][0][0] = Point(X-B*0.5, 0);
      L[i][0][1] = L[i][1][0] = Point(X, H);
      L[i][1][1] = Point(X+B*0.5, 0);
      x[c++] = X-B*0.5;
      x[c++] = X;
      x[c++] = X+B*0.5;
    }
    for(int i = 0; i < n; i++) for(int a = 0; a < 2; a++)
      for(int j = i+1; j < n; j++) for(int b = 0; b < 2; b++) {
        Point P1 = L[i][a][0], P2 = L[i][a][1], P3 = L[j][b][0], P4 = L[j][b][1];
        if(SegmentProperIntersection(P1, P2, P3, P4))
          x[c++] = GetLineIntersection(P1, P2-P1, P3, P4-P3).x;
      }

    // 根据所有交点离散化
    sort(x, x+c);
    c = unique(x, x+c) - x;

    double ans = 0;
    Point lastp;
    for(int k = 0; k < c; k++) {
      // 计算直线x=x[k]和山相交的最高点
      Point P(x[k], 0);
      Vector V(0, 1);
      double maxy = -1;
      for(int i = 0; i < n; i++) for(int a = 0; a < 2; a++) {
        Point P1 = L[i][a][0], P2 = L[i][a][1];
        Point intersection = GetLineIntersection(P, V, P1, P2-P1);
        if(dcmp(intersection.x-P1.x) >= 0 && dcmp(intersection.x-P2.x) <= 0)
          maxy = max(maxy, intersection.y);
      }
      Point newp(x[k], maxy);
      if(k > 0 && (dcmp(lastp.y) > 0 || dcmp(maxy) > 0)) ans += Length(newp - lastp);
      lastp = newp;
    }

    printf("Case %d: %.0lf\n\n", ++kase, ans);
  }
  return 0;
}
// Accepted 10ms 2973 C++5.3.0 2020-12-1415:32:51 25846121
```

### LA5129/HDU3838 Affine Mess

```cpp
// LA5129/HDU3838 Affine Mess
// 刘汝佳
#include<cstdio>
#include<cmath>
#include<vector>
#include<algorithm>
using namespace std;

/*
  求解下列方程组的整数解的个数：
  p*s + d = x
  q*s + d = y
  r*s + d = z
  其中s代表缩放系数，d代表平移量

  解：联立方程(1), (2)，得(p-q)*s = x-y
  i) 如果p-q = 0，则必须有x == y，否则无解
  ii) 如果p-q != 0，则s = (x-y)/(p-q)。如果s不是整数则无解，否则s是一个解

  类似的，还应联立(2), (3)和(3), (1)求解。
  i) 如果求出了多个s，他们必须相同；
  ii) 如果一个s都没有得到，说明有无穷多解（返回2就可以了）
  iii) 如果s = 0，根据题意，也无解
*/
int solve(int p, int q, int r, int x, int y, int z) {
  int a[] = {p, q, r};
  int b[] = {x, y, z};
  vector<int> ans;
  for(int i = 0; i < 3; i++) {
    int P = a[i], Q = a[(i+1)%3], X = b[i], Y = b[(i+1)%3];
    if(P == Q) { if(X != Y) return 0; }
    else if((X - Y) % (P - Q) != 0) return 0;
    else ans.push_back((X - Y) / (P - Q));
  }
  if(ans.empty()) return 2; // 三个方程等价，无穷多组解
  sort(ans.begin(), ans.end());
  if(ans[0] != ans.back() || ans[0] == 0) return 0; // 求出的s不全相同或者等于0
  return 1;
}

int x[3], y[3]; // 变换前的点
int x2[3], y2[3]; // 变换后的点
int ix[3], iy[3]; // 旋转+捕捉f后的点

int main() {
  int kase = 0;
  for(;;) {
    int ok = 0;
    for(int i = 0; i < 3; i++) {
      scanf("%d%d", &x[i], &y[i]);
      if(x[i] != 0 || y[i] != 0) ok = 1;
    }
    if(!ok) break;
    for(int i = 0; i < 3; i++) scanf("%d%d", &x2[i], &y2[i]);
    int ans = 0; // 解的个数

    // 枚举旋转方式
    // 注意旋转180度等价于缩放(-1,-1)，所以只枚举40个点而不是80个
    for(int i = 0; i < 40; i++) {
      int rx, ry;
      if(i < 20) { rx = 10; ry = i - 10; } // (10,-10), (10,-9), ..., (10,9), (10,9)
      else { rx = 30 - i; ry = 10; } // (10,10), (9,10), ..., (-9,10)

      // 变换前3个点，保存在(ix[i],iy[i])中
      double len = sqrt(rx*rx+ry*ry);
      double cosa = rx / len;
      double sina = ry / len;
      int ix[3], iy[3];
      for(int j = 0; j < 3; j++) {
        ix[j] = (int)floor(x[j] * cosa - y[j] * sina + 0.5);
        iy[j] = (int)floor(x[j] * sina + y[j] * cosa + 0.5);
      }

      // 枚举(ix, iy)和(x2, y2)的对应关系
      int p[3] = {0, 1, 2};
      do {
        int cnt1 = solve(ix[0], ix[1], ix[2], x2[p[0]], x2[p[1]], x2[p[2]]);
        int cnt2 = solve(iy[0], iy[1], iy[2], y2[p[0]], y2[p[1]], y2[p[2]]);
        ans += cnt1 * cnt2; // x, y方向独立，分别求解
      } while(next_permutation(p, p+3));
    }

    printf("Case %d: ", ++kase);
    if(ans == 0) printf("no solution\n");
    else if(ans == 1) printf("equivalent solutions\n");
    else printf("inconsistent solutions\n");
  }
  return 0;
}
```

### UVa12303 Composite Transformations

```cpp
// UVa12303 Composite Transformations
// 刘汝佳
#include<cstdio>
#include<cmath>
#include<cstdlib>
#include<cstring>
#include<cassert>
using namespace std;

const double PI = acos(-1.0);

struct Point3 {
  double x, y, z;
  Point3(double x=0, double y=0, double z=0):x(x),y(y),z(z) { }
};

typedef Point3 Vector3;

Vector3 operator + (const Vector3& A, const Vector3& B) {
  return Vector3(A.x+B.x, A.y+B.y, A.z+B.z);
}

Vector3 operator - (const Point3& A, const Point3& B) {
  return Vector3(A.x-B.x, A.y-B.y, A.z-B.z);
}

Vector3 operator * (const Vector3& A, double p) {
  return Vector3(A.x*p, A.y*p, A.z*p);
}

Vector3 operator / (const Vector3& A, double p) {
  return Vector3(A.x/p, A.y/p, A.z/p);
}

double Dot(const Vector3& A, const Vector3& B) { return A.x*B.x + A.y*B.y + A.z*B.z; }
double Length(const Vector3& A) { return sqrt(Dot(A, A)); }
Vector3 Cross(const Vector3& A, const Vector3& B) { return Vector3(A.y*B.z - A.z*B.y, A.z*B.x - A.x*B.z, A.x*B.y - A.y*B.x); }

// 平面
struct Plane {
  double a, b, c, d;
  Plane() {}
  Plane(Point3* P) { // 用三点确定一个平面。调用者需保证三点不共线
    Vector3 V = Cross(P[1]-P[0], P[2]-P[0]);
    V = V / Length(V);
    a = V.x; b = V.y; c = V.z; d = -Dot(V, P[0]);
  }
  Point3 sample() const { // 随机采样
    double v1 = rand() / (double)RAND_MAX;
    double v2 = rand() / (double)RAND_MAX;
    if(a != 0) return Point3(-(d+v1*b+v2*c)/a, v1, v2);
    if(b != 0) return Point3(v1, -(d+v1*a+v2*c)/b, v2);
    if(c != 0) return Point3(v1, v2, -(d+v1*a+v2*b)/c);
    assert(0); // 不是一个平面
  }
};

// 4x4齐次变换矩阵
struct Matrix4x4 {
  double v[4][4];

  // 矩阵乘法
  inline Matrix4x4 operator * (const Matrix4x4 &rhs) const {
    Matrix4x4 ans;   
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++) {
            ans.v[i][j] = 0;
            for (int k = 0; k < 4; k++)
                ans.v[i][j] += v[i][k] * rhs.v[k][j];
        }
    return ans;
  }

  // 变换一个点，相当于右乘列向量(x, y, z, 1}
  inline Point3 transform(Point3 P) const {
    double p[4] = {P.x, P.y, P.z, 1}, ans[4] = {0};
    for(int i = 0; i < 4; i++)
      for(int k = 0; k < 4; k++)
        ans[i] += v[i][k] * p[k];
    return Point3(ans[0], ans[1], ans[2]); // ans[3]肯定是1
  }

  // 单位矩阵
  void loadIdentity() {
    memset(v, 0, sizeof(v));
    v[0][0] = v[1][1] = v[2][2] = v[3][3] = 1;
  }

  // 平移矩阵
  void loadTranslate(double a, double b, double c) {
    loadIdentity();
    v[0][3] = a; v[1][3] = b; v[2][3] = c;
  }

  // 缩放矩阵
  void loadScale(double a, double b, double c) {
    loadIdentity();
    v[0][0] = a; v[1][1] = b; v[2][2] = c;
  }

  // 绕固定轴旋转一定角度的矩阵
  void loadRotation(double a, double b, double c, double deg) {
    loadIdentity();
    double rad = deg / 180 * PI;
    double sine = sin(rad), cosine = cos(rad);
    Vector3 L(a, b, c);
    L = L / Length(L);
    v[0][0] = cosine + L.x * L.x * (1.0 - cosine);
    v[0][1] = L.x * L.y * (1 - cosine) - L.z * sine;
    v[0][2] = L.x * L.z * (1 - cosine) + L.y * sine;
    v[1][0] = L.y * L.x * (1 - cosine) + L.z * sine;
    v[1][1] = cosine + L.y * L.y * (1 - cosine);
    v[1][2] = L.y * L.z * (1 - cosine) - L.x * sine;
    v[2][0] = L.z * L.x * (1 - cosine) - L.y * sine;
    v[2][1] = L.z * L.y * (1 - cosine) + L.x * sine;
    v[2][2] = cosine + L.z * L.z * (1 - cosine);
  }
};

const int maxn = 50000 + 10;
const int maxp = 50000 + 10;
Point3 P[maxn];
Plane planes[maxp];

int main() {
  int n, m, T;
  scanf("%d%d%d", &n, &m, &T);
  for(int i = 0; i < n; i++)
    scanf("%lf%lf%lf", &P[i].x, &P[i].y, &P[i].z);
  for(int i = 0; i < m; i++)
    scanf("%lf%lf%lf%lf", &planes[i].a, &planes[i].b, &planes[i].c, &planes[i].d);

  // 点P将被变换为 M[T-1] * ... * M[2] * M[1] * M[0] * P
  // 根据结合律，先计算mat = (M[T-1] * ... * M[0])，则点P变换为mat * P
  Matrix4x4 mat;
  mat.loadIdentity();
  for(int i = 0; i < T; i++) {
    char op[100];
    double a, b, c, theta;
    scanf("%s%lf%lf%lf", op, &a, &b, &c);
    Matrix4x4 M;
    if(op[0] == 'T') M.loadTranslate(a, b, c);
    else if(op[0] == 'S') M.loadScale(a, b, c);
    else if(op[0] == 'R') { scanf("%lf", &theta); M.loadRotation(a, b, c, theta); }
    mat = M * mat;
  }

  // 变换点
  for(int i = 0; i < n; i++) {
    Point3 ans = mat.transform(P[i]);
    printf("%.2lf %.2lf %.2lf\n", ans.x, ans.y, ans.z);
  }
  // 变换平面
  for(int i = 0; i < m; i++) {
    Point3 A[3];
    for(int j = 0; j < 3; j++) A[j] = mat.transform(planes[i].sample());
    Plane pl(A);
    printf("%.2lf %.2lf %.2lf %.2lf\n", pl.a, pl.b, pl.c, pl.d);
  }
  return 0;
}
// Accepted 70ms 4465 C++5.3.0 2020-12-14 15:31:02 25846118
```

## 6.5 数学专题

### LA3700/POJ3146 Interesting Yang Hui Triangle, Asia上海 2016

```cpp
// LA3700/POJ3146 Interesting Yang Hui Triangle, Asia上海 2016
// 刘汝佳
#include <cstdio>
int main() {
  for (int kase = 0, n, p; scanf("%d%d", &p, &n) == 2 && p;) {
    int ans = 1;
    while (n > 0) ans = ans * (n % p + 1) % 10000, n /= p;
    printf("Case %d: %04d\n", ++kase, ans);
  }
  return 0;
}
// Accepted 328kB 298 G++ 2020-12-12 22:41:35 22206289
```

### UVa1457/LA4746 Decrypt Messages

```cpp
// UVa1457/LA4746 Decrypt Messages
// 刘汝佳
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <vector>
#include <map>
#include <algorithm>
#include <iostream>
using namespace std;

typedef long long LL;
//// 日期时间部分
const int SECONDS_PER_DAY = 24 * 60 * 60;
const int num_days[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
bool is_leap(int year) {
  if (year % 400 == 0) return true;
  if (year % 4 == 0) return year % 100 != 0;
  return false;
}

int leap_second(int year, int month) {
  return ((year % 10 == 5 || year % 10 == 8) && month == 12) ? 1 : 0;
}

void print(int year, int month, int day, int hh, int mm, int ss) {
  printf("%d.%02d.%02d %02d:%02d:%02d\n", year, month, day, hh, mm, ss);
}

void print_time(LL t) {
  int year = 2000;
  while(1) {
    int days = is_leap(year) ? 366 : 365;
    LL sec = (LL)days * SECONDS_PER_DAY + leap_second(year, 12);
    if(t < sec) break;
    t -= sec;
    year++;
  }

  int month = 1;
  while(1) {
    int days = num_days[month-1];
    if(is_leap(year) && month == 2) days++;
    LL sec = (LL)days * SECONDS_PER_DAY + leap_second(year, month);
    if(t < sec) break;
    t -= sec;
    month++;
  }

  if(leap_second(year, month) && t == 31 * SECONDS_PER_DAY)
    print(year, 12, 31, 23, 59, 60);
  else {
    int day = t / SECONDS_PER_DAY + 1;
    t %= SECONDS_PER_DAY;
    int hh = t / (60*60);
    t %= 60*60;
    int mm = t / 60;
    t %= 60;
    int ss = t;
    print(year, month, day, hh, mm, ss);
  }
}

//// 数论部分

LL gcd(LL a, LL b) {
  return b ? gcd(b, a%b) : a;
}

// 求d = gcd(a, b)，以及满足ax+by=d的(x,y)（注意，x和y可能为负数）
// 扩展euclid算法。
void gcd(LL a, LL b, LL& d, LL& x, LL& y) {
  if(!b){ d = a; x = 1; y = 0; }
  else{ gcd(b, a%b, d, y, x); y -= x*(a/b); }
}

// 注意，返回值可能是负的
int pow_mod(LL a, LL p, int MOD) {
  if(p == 0) return 1;
  LL ans = pow_mod(a, p/2, MOD);
  ans = ans * ans % MOD;
  if(p%2) ans = ans * a % MOD;
  return ans;
}

// 注意，返回值可能是负的
int mul_mod(LL a, LL b, int MOD) {
  return a * b % MOD;
}

// 求ax = 1 (mod MOD) 的解，其中a和MOD互素。
// 注意，由于MOD不一定为素数，因此不能直接用pow_mod(a, MOD-2, MOD)求解
// 解法：先求ax + MODy = 1的解(x,y)，则x为所求
int inv(LL a, int MOD) {
  LL d, x, y;
  gcd(a, MOD, d, x, y);
  return (x + MOD) % MOD; // 这里的x可能是负数，因此要调整
}

// 解模方程（即离散对数）a^x = b。要求MOD为素数
// 解法：Shank的大步小步算法
int log_mod(int a, int b, int MOD) {
  int m, v, e = 1, i;
  m = (int)sqrt(MOD);
  v = inv(pow_mod(a, m, MOD), MOD);
  map<int,int> x;
  x[1] = 0;
  for(i = 1; i < m; i++){ e = mul_mod(e, a, MOD); if (!x.count(e)) x[e] = i; }
  for(i = 0; i < m; i++){
    if(x.count(b)) return i*m + x[b];
    b = mul_mod(b, v, MOD);
  }
  return -1;
}

// 返回MOD（不一定是素数）的某一个原根，phi为MOD的欧拉函数值（若MOD为素数则phi=MOD-1）
// 解法：考虑phi(MOD)的所有素因子p，如果所有m^(phi/p) mod MOD都不等于1，则m是MOD的原根
int get_primitive_root(int MOD, int phi) {
  // 计算phi的所有素因子
  vector<int> factors;
  int n = phi;
  for(int i = 2; i*i <= n; i++) {
    if(n % i != 0) continue;
    factors.push_back(i);
    while(n % i == 0) n /= i;
  }
  if(n > 1) factors.push_back(n);

  while(1) {
    int m = rand() % (MOD-2) + 2; // m = 2~MOD-1
    bool ok = true;
    for(int i = 0; i < factors.size(); i++)
      if(pow_mod(m, phi/factors[i], MOD) == 1) { ok = false; break; }
    if(ok) return m;
  }
}

// 解线性模方程 ax = b (mod n)，返回所有解（模n剩余系）
// 解法：令d = gcd(a, n)，两边同时除以d后得a'x = b' (mod n')，由于此时gcd(a',n')=1，两边同时左乘a'在模n'中的逆即可，最后把模n'剩余系中的解转化为模n剩余系
vector<LL> solve_linear_modular_equation(int a, int b, int n) {
  vector<LL> ans;
  int d = gcd(a, n);
  if(b % d != 0) return ans;
  a /= d; b /= d;
  int n2 = n / d;
  int p = mul_mod(inv(a, n2), b, n2);
  for(int i = 0; i < d; i++)
    ans.push_back(((LL)i * n2 + p) % n);
  return ans;
}

// 解高次模方程 x^q = a (mod p)，返回所有解（模n剩余系）
// 解法：设m为p的一个原根，且x = m^y, a = m^z，则m^qy = m^z(mod p)，因此qy = z(mod p-1)，解线性模方程即可
vector<LL> mod_root(int a, int q, int p) {
  vector<LL> ans;
  if(a == 0) {
    ans.push_back(0);
    return ans;
  }
  int m = get_primitive_root(p, p-1); // p是素数，因此phi(p)=p-1
  int z = log_mod(m, a, p);
  ans = solve_linear_modular_equation(q, z, p-1);
  for(int i = 0; i < ans.size(); i++)
    ans[i] = pow_mod(m, ans[i], p);
  sort(ans.begin(), ans.end());
  return ans;
}

int main() {
  int T, P, Q, A;
  cin >> T;
  for(int kase = 1; kase <= T; kase++) {
    cin >> P >> Q >> A;
    vector<LL> ans = mod_root(A, Q, P);
    cout << "Case #" << kase << ":" << endl;
    if (ans.empty()) {
      cout << "Transmission error" << endl;
    } else {
      for(int i = 0; i < ans.size(); i++) print_time(ans[i]);
    }
  }	
  return 0;
}
// 25878475	1457	Decrypt Messages	Accepted	C++	0.570	2020-12-23 09:22:31
```

### UVa10498 Happiness

```cpp
// UVa10498 Happiness
// 刘汝佳
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<cassert>
using namespace std;

// 改进单纯性法的实现
// 参考：http://en.wikipedia.org/wiki/Simplex_algorithm
// 输入矩阵a描述线性规划的标准形式。a为m+1行n+1列，其中行0~m-1为不等式，行m为目标函数（最大化）。列0~n-1为变量0~n-1的系数，列n为常数项
// 第i个约束为a[i][0]*x[0] + a[i][1]*x[1] + ... <= a[i][n]
// 目标为max(a[m][0]*x[0] + a[m][1]*x[1] + ... + a[m][n-1]*x[n-1] - a[m][n])
// 注意：变量均有非负约束x[i] >= 0
const int maxm = 500; // 约束数目上限
const int maxn = 500; // 变量数目上限
const double INF = 1e100, eps = 1e-10;

struct Simplex {
  int n; // 变量个数
  int m; // 约束个数
  double a[maxm][maxn]; // 输入矩阵
  int B[maxm], N[maxn]; // 算法辅助变量

  void pivot(int r, int c) {
    swap(N[c], B[r]);
    a[r][c] = 1 / a[r][c];
    for(int j = 0; j <= n; j++) if(j != c) a[r][j] *= a[r][c];
    for(int i = 0; i <= m; i++) if(i != r) {
      for(int j = 0; j <= n; j++) if(j != c) a[i][j] -= a[i][c] * a[r][j];
      a[i][c] = -a[i][c] * a[r][c];
    }
  }

  bool feasible() {
    for(;;) {
      int r, c;
      double p = INF;
      for(int i = 0; i < m; i++) if(a[i][n] < p) p = a[r = i][n];
      if(p > -eps) return true;
      p = 0;
      for(int i = 0; i < n; i++) if(a[r][i] < p) p = a[r][c = i];
      if(p > -eps) return false;
      p = a[r][n] / a[r][c];
      for(int i = r+1; i < m; i++) if(a[i][c] > eps) {
        double v = a[i][n] / a[i][c];
        if(v < p) { r = i; p = v; }
      }
      pivot(r, c);
    }
  }

  // 解有界返回1，无解返回0，无界返回-1。b[i]为x[i]的值，ret为目标函数的值
  int simplex(int n, int m, double x[maxn], double& ret) {
    this->n = n;
    this->m = m;
    for(int i = 0; i < n; i++) N[i] = i;
    for(int i = 0; i < m; i++) B[i] = n+i;
    if(!feasible()) return 0;
    for(;;) {
      int r, c;
      double p = 0;
      for(int i = 0; i < n; i++) if(a[m][i] > p) p = a[m][c = i];
      if(p < eps) {
        for(int i = 0; i < n; i++) if(N[i] < n) x[N[i]] = 0;
        for(int i = 0; i < m; i++) if(B[i] < n) x[B[i]] = a[i][n];
        ret = -a[m][n];
        return 1;
      }
      p = INF;
      for(int i = 0; i < m; i++) if(a[i][c] > eps) {
        double v = a[i][n] / a[i][c];
        if(v < p) { r = i; p = v; }
      }
      if(p == INF) return -1;
      pivot(r, c);
    }
  }
};

//////////////// 题目相关
#include<cmath>
Simplex solver;

int main() {
  for(int n, m;scanf("%d%d", &n, &m) == 2;) {
    for(int i = 0; i < n; i++) scanf("%lf", &solver.a[m][i]); // 目标函数
    solver.a[m][n] = 0; // 目标函数常数项
    for(int i = 0; i < m; i++)
      for(int j = 0; j < n+1; j++)
        scanf("%lf", &solver.a[i][j]);
    double ans, x[maxn];
    assert(solver.simplex(n, m, x, ans) == 1);
    ans *= m;
    printf("Nasa can spend %d taka.\n", (int)floor(ans + 1 - eps));
  }
  return 0;
}
// Accepted 10ms 2716 C++5.3.0 2020-12-12 22:39:36 25840427
```

### UVa11017 A Greener World

```cpp
// UVa11017 A Greener World
// Rujia Liu
#include <cmath>
#include <cstdio>
#include <vector>
using namespace std;

typedef long long LL;

const double PI = acos(-1.0);

struct Point {
  int x, y;
  Point(int x = 0, int y = 0) : x(x), y(y) {}
};

typedef Point Vector;

Vector operator+(const Vector& A, const Vector& B) {
  return Vector(A.x + B.x, A.y + B.y);
}
Vector operator-(const Point& A, const Point& B) {
  return Vector(A.x - B.x, A.y - B.y);
}
double Cross(const Vector& A, const Vector& B) {
  return (LL)A.x * B.y - (LL)A.y * B.x;
}

LL PolygonArea2(const vector<Point>& p) {
  int n = p.size();
  LL area2 = 0;
  for (int i = 1; i < n - 1; i++) area2 += Cross(p[i] - p[0], p[i + 1] - p[0]);
  return abs(area2);
}

inline int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }

// 线段a-b上的格点数。不包含a和b。设参数t = b/d
// 则d必须是b.x-a.x和b.y-a.y的公约数，且0<b<d,
// 减1因为要排除端点，因此0和d都不能做分子
LL count_on_segment(const Point& a, const Point& b) {
  return gcd(abs(b.x - a.x), abs(b.y - a.y)) - 1;
}

// Pick's Theorem: A = I + B/2 - 1 => I = A - B/2 + 1
LL count_inside_polygon(const vector<Point>& poly) {
  int n = poly.size();
  LL A2 = PolygonArea2(poly);
  int B = n;  // 多边形的顶点
  for (int i = 0; i < n; i++) B += count_on_segment(poly[i], poly[(i + 1) % n]);
  return (A2 - B) / 2 + 1;
}

// 计算内部的、x和y的小数部分都是0.5的点
LL count(const vector<Point>& poly) {
  vector<Point> poly2;
  for (int i = 0; i < poly.size(); i++)  // 旋转45度后的稠密网格坐标
    poly2.push_back(Point(poly[i].x - poly[i].y, poly[i].x + poly[i].y));
  return count_inside_polygon(poly2) - count_inside_polygon(poly);
}

int main() {
  // theta和d仅仅用来算面积
  for (int d, theta, N, x, y; scanf("%d%d%d", &d, &theta, &N) == 3 && d;) {
    vector<Point> poly;
    for (int i = 0; i < N; i++)
      scanf("%d%d", &x, &y), poly.push_back(Point(x, y));
    LL area2 = PolygonArea2(poly);
    printf("%lld %.0lf\n", count(poly),
           sin((double)theta / 180 * PI) * d * d * area2 / 2.0);
  }
  return 0;
}
// Accepted 1963 C++5.3.0 2020-12-1222:36:42|□25840418
```

## 6.6 浅谈代码设计与静态查错

### LA4488/UVa12233 Final Combat：正确版

```cpp
// LA4488/UVa12233 Final Combat：正确版
// Rujia Liu
#include<iostream>
#include<vector>
#include<map>
#include<string>
#include<algorithm>
using namespace std;

const int MAXTIME = 12;
const int INF = 100000000;
const string name[] = {"Y", "H", "L", "M"};

int SY_jing, XX_su, SY_su, yurun_jing, yurun_shen, shuerguo_shen;
int maxjing[4], maxshen[4], su[4];
int d1x[4], d2x[4], d1s[4], d2s[4];
int wad[4], ssd[4], ssq[4], ssp[4], q1[4], q2[4];
int jing[4], qi[4], shen[4];

int MaxT, Hero, Pos, HeroT, XXT, SYT;
map<int,int> Hash[MAXTIME + 1];
int dfs(int t, int j, int q, int s) {
  if(j <= 0) return -INF;
  if(t > MaxT) return 0;
  j = min(j, maxjing[Hero]); q = min(q, 100); s = min(s, maxshen[Hero]);
  int h = j*110000 + q*1000 + s;
  if(Hash[t].count(h)) return Hash[t][h];
  int dj = 0, dq = 0;
  if(t % XXT == 0) {
    if((t / XXT) % 4 == Pos) { dj -= d1x[Hero]; dq += q2[Hero]; }
    if((t / XXT) % 4 == 0) dj -= d2x[Hero];
  }
  if(t % SYT == 0) {
    if((t / SYT) % 4 == Pos) { dj -= d1s[Hero]; dq += q2[Hero]; }
    if((t / SYT) % 4 == 0) dj -= d2s[Hero];
  }
  Hash[t][h] = -INF;
  int& ans = Hash[t][h];
  if(t == MaxT) {
    ans = 0;
    if (t % HeroT != 0) return 0;
    if(j > wad[Hero]) ans = max(ans, wad[Hero]);
    if(q >= ssq[Hero]) {
      int dj2 = (ssp[Hero] == 1 ? -ssd[Hero] : 0);
      if(j+dj2 > 0) ans = max(ans, ssd[Hero]);
    }
  } else {
    if (t % HeroT != 0) return ans = dfs(t+1, j+dj, q+dq, s);
    ans = max(ans, dfs(t+1, j+dj, q+dq+q1[Hero], s));
    ans = max(ans, dfs(t+1, j+dj-wad[Hero], q+dq+q1[Hero], s) + wad[Hero]);
    if(s >= yurun_shen && j < maxjing[Hero]) ans = max(ans, dfs(t+1, min(j+yurun_jing, maxjing[Hero])+dj, q+dq, s-yurun_shen));
    if(s < maxshen[Hero]) ans = max(ans, dfs(t+1, j+dj, q+dq, s+shuerguo_shen));
    if(q >= ssq[Hero]) {
      int dj2 = (ssp[Hero] == 1 ? -ssd[Hero] : 0);
      ans = max(ans, dfs(t+1, j+dj+dj2, q+dq-ssq[Hero], s) + ssd[Hero]);
    }
  }
  return ans;
}

int d[4][4];
vector<string> ans;
int solve(int maxt) {
  for(int h = 0; h < 4; h++)
    for(int p = 1; p <= 3; p++) {
      MaxT = maxt; Hero = h; Pos = p; HeroT = 5 - su[h];
      for(int t = 1; t <= maxt; t++) Hash[t].clear();
      d[h][p] = dfs(1, jing[h], qi[h], shen[h]);
    }
  ans.clear();
  for(int h1 = 0; h1 < 4; h1++)
    for(int h2 = 0; h2 < 4; h2++) if(h2 != h1)
      for(int h3 = 0; h3 < 4; h3++) if(h3 != h1 && h3 != h2)
        if(d[h1][1] + d[h2][2] + d[h3][3] >= SY_jing)
          ans.push_back(name[h1] + name[h2] + name[h3]);
  sort(ans.begin(), ans.end());
  return ans.size();
}

int main() {
  int caseno = 0;
    while(cin >> SY_jing && SY_jing) {
    cin >> XX_su >> SY_su >> yurun_jing >> yurun_shen >> shuerguo_shen;
    for(int i = 0; i < 4; i++)
      cin >> maxjing[i] >> maxshen[i] >> su[i] >> d1x[i] >> d2x[i] >> d1s[i] >> d2s[i] >> wad[i] >> ssd[i] >> ssq[i] >> ssp[i] >> q1[i] >> q2[i] >> jing[i] >> qi[i] >> shen[i];
    XXT = 5 - XX_su; SYT = 5 - SY_su;
    cout << "Case " << ++caseno << ": ";
    for(int i = 1; i <= MAXTIME; i++) if(solve(i)) {
      cout << i;
      for(int j = 0; j < ans.size(); j++) cout << " " << ans[j];
      break;
    }
    if(ans.size() == 0) cout << -1;
    cout << endl << endl;
  }
  return 0;
}
// 25878492	12233	Final Combat	Accepted	C++	0.130	2020-12-23 09:26:25
```

### UVa10966 3KP-Bash Project

```cpp
// UVa10966 3KP-Bash Project
// Rujia Liu
#include<iostream>
#include<string>
#include<vector>
#include<algorithm>
#include<sstream>
#include<cstring>
using namespace std;

typedef unsigned long long LL;
typedef vector<int> VI;
typedef vector<string> VS;

const string ERROR_BAD_USAGE = "bad usage\n";
const string ERROR_NO_COMMAND = "no such command\n";
const string ERROR_DIR_NOT_FOUND = "path not found\n";
const string ERROR_DIR_FOUND = "a directory with the same name exists\n";
const string ERROR_DIR_OR_FILE_FOUND = "file or directory with the same name exists\n";
const string ERROR_FILE_NOT_FOUND = "file not found\n";
const string ERROR_EMPTY = "[empty]\n";

// if delim != ' ', make sure that no space characters exist in s
VS split(string s, char delim=' ') {
  if(delim != ' ')
    for(int i = 0; i < s.length(); i++) if(s[i] == delim) s[i] = ' ';
  stringstream ss(s);
  VS ret;
  string x;
  while(ss >> x) ret.push_back(x);
  return ret;
}

// return 1 if success, 0 if on error
int get_int(string s, LL& v) {
  stringstream ss(s);
  if(ss >> v) return 1;
  return 0;
}

string trim(string s) {
  int L, R;
  for(L = 0; L < s.length(); L++) if(!isspace(s[L])) break;
  for(R = s.length()-1; R > L; R--) if(!isspace(s[R])) break;
  return s.substr(L, R-L+1);
}

struct File {
  int parent;
  string name;
  string fullpath; // cached fullpath name
  LL size;
  bool dir;
  bool hidden;
  vector<int> subdir;
  File(int parent=0, string name="", LL size=0, bool dir=true, bool hidden=false):parent(parent),name(name),size(size),dir(dir),hidden(hidden) {}
};

vector<File> fs;
int curDir;

// lexicograhically smaller
bool comp(const int& x, const int& y) {
  return fs[x].fullpath < fs[y].fullpath;
}

// compare size first (increasing)
bool comps(const int& x, const int& y) {
  return fs[x].size < fs[y].size || (fs[x].size == fs[y].size && fs[x].fullpath < fs[y].fullpath);
}

// compare size first (decreasing)
bool compS(const int& x, const int& y) {
  return fs[x].size > fs[y].size || (fs[x].size == fs[y].size && fs[x].fullpath < fs[y].fullpath);
}

// return the node number. -1 on error
int findFileInDirectory(int node, string name) {
  VI& subdir = fs[node].subdir;
  for(int i = 0; i < subdir.size(); i++)
    if(fs[subdir[i]].name == name) return subdir[i];
  return -1;
}

// if the end of path is '/', remove it first
string joinPath(string path, string name) {
  if(path[path.size()-1] != '/') path += "/";
  return path + name;
}

// get the absolute path string for a node
string getAbsolutePath(int node) {
  if(!node) return "/";
  return joinPath(getAbsolutePath(fs[node].parent), fs[node].name);
}

// create a file (regular/directory) in a node (the caller should ensure that the node represents a directory)
int createFileInDirectory(int node, string name, LL size, bool dir, bool hidden) {
  fs.push_back(File(node, name, size, dir, hidden));
  int x = fs.size()-1;  
  fs[x].fullpath = joinPath(getAbsolutePath(node), name);
  fs[node].subdir.push_back(x);
  return x;
}

// return the node of a path (could be relative path or absolute path). return -1 on error
int getDirNode(string path) {
  if(!path.length()) return curDir;
  int node = curDir; // relative path by default
  if(path[0] == '/') node = 0; // absolute path
  VS dirs = split(path, '/');
  for(int i = 0; i < dirs.size(); i++) {
    if(dirs[i] == ".") continue;
    else if(dirs[i] == "..") {
      if(!node) return -1; // root has no parent
      node = fs[node].parent;
    } else {
      int x = findFileInDirectory(node, dirs[i]);
      if(x == -1 || !fs[x].dir) return -1; // cannot enter a regular file
      node = x;
    }
  }
  return node;
}

// check if the filename is valid
int isValidFileName(string name) {
  if(name.length() == 0 || name.length() > 255) return 0;
  if(name == "." || name.find("..") != string::npos) return 0;
  for(int i = 0; i < name.length(); i++)
    if(!isdigit(name[i]) && !isalpha(name[i]) && name[i] != '.') return 0;
  return 1;
}

// split a fullpath into a directory part and a filename part
// return the node of the directory part. return -1 if path not found
int splitFileName(string fullpath, string& filename) {
  int n = fullpath.length();
  int x = n;
  for(int i = fullpath.length()-1; i >= 0; i--) {
    if(fullpath[i] == '/') { // the last '/'
      filename = fullpath.substr(i+1);
	  string dir = fullpath.substr(0, i);
	  if(dir == "") return 0; // relative to root, NOT current directory
      return getDirNode(dir);
    }
  }
  filename = fullpath;
  return curDir;
}

// new BASH session
void newSession() { fs.clear(); fs.push_back(File()); curDir = 0; }

// Given the filename, find all matching files in a node, possibly recursively. Append the items in "out", which is a vector of nodes
// if filename == "", we simply list the files
void findFileEx(VI& out, int node, string filename, bool recur, bool hidden, bool f=true, bool d=true) {
  VI& subdir = fs[node].subdir;
  for(int i = 0; i < subdir.size(); i++) {
    int x = subdir[i];
    if(fs[x].dir && recur) findFileEx(out, x, filename, recur, hidden, f, d);
    if(fs[x].hidden && !hidden) continue;
    if(filename == "" || fs[x].name == filename) {
      if((fs[x].dir && d) || (!fs[x].dir && f)) out.push_back(x);
    }
  }
}

// format the file list
string formatFiles(const VI& out) {
  stringstream ss;
  for(int i = 0; i < out.size(); i++) {
    ss << fs[out[i]].fullpath << " " << fs[out[i]].size;
    if(fs[out[i]].hidden) ss << " " << "hidden";
    if(fs[out[i]].dir) ss << " " << "dir";
    ss << "\n";
  }
  return ss.str();
}

// get arguments and switches
bool parseArgs(VS params, VS& args, bool* sw, LL &v) {
  LL v2;
  for(int i = 0; i < params.size(); i++)
    if(params[i][0] == '-') {
      if(isalpha(params[i][1])) sw[params[i][1]] = 1;
	  else if(get_int(params[i].substr(1), v2)) v = v2; // if there are more than one, only the last one is used
	  else return false;
	}
    else args.push_back(params[i]); // regular arguments (without prefix '-')
  return true;
}

// run a command (except grep) without piping, returns the standard output
string runCommand(const VS& cmd) {
  VS params(cmd.begin()+1, cmd.end()), args;
  bool sw[256];
  LL v = 0;
  memset(sw, 0, sizeof(sw));
  if(!parseArgs(params, args, sw, v)) return ERROR_BAD_USAGE;
  
  int node;
  string filename;
  if(cmd[0] == "cd") {
    if(args.size() != 1) return ERROR_BAD_USAGE;
    if((node = getDirNode(args[0])) == -1) return ERROR_DIR_NOT_FOUND;
    curDir = node;
    return "";
  } else if(cmd[0] == "touch") {
    if(args.size() != 1) return ERROR_BAD_USAGE;
    if((node = splitFileName(args[0], filename)) == -1) return ERROR_DIR_NOT_FOUND;
    if(!isValidFileName(filename)) return ERROR_BAD_USAGE; //!

    int x = findFileInDirectory(node, filename);
    if(x != -1 && fs[x].dir) return ERROR_DIR_FOUND;
    if(x == -1) createFileInDirectory(node, filename, v, false, sw['h']);
    else { fs[x].size = v; fs[x].hidden = sw['h']; }
    return "";
  }
  if(cmd[0] == "mkdir") {
    if(args.size() != 1) return ERROR_BAD_USAGE;
    if((node = splitFileName(args[0], filename)) == -1) return ERROR_DIR_NOT_FOUND;
    if(!isValidFileName(filename)) return ERROR_BAD_USAGE; //!

    int x = findFileInDirectory(node, filename);
    if(x != -1) return ERROR_DIR_OR_FILE_FOUND;
    createFileInDirectory(node, filename, 0, true, sw['h']);
    return "";
  }
  if(cmd[0] == "find") {
    if(args.size() != 1) return ERROR_BAD_USAGE;
    if((node = splitFileName(args[0], filename)) == -1) return ERROR_DIR_NOT_FOUND;
	
    VI out;
    findFileEx(out, node, filename, sw['r'], sw['h']);
    if(out.size() == 0) return ERROR_FILE_NOT_FOUND;
    sort(out.begin(), out.end(), comp);
    return formatFiles(out);
  }
  if(cmd[0] == "ls") {
    if(args.size() > 1) return ERROR_BAD_USAGE;
	node = curDir;
	if(args.size() == 1) if((node = getDirNode(args[0])) == -1) return ERROR_DIR_NOT_FOUND;
	
    VI out;
    findFileEx(out, node, "", sw['r'], sw['h'], !sw['d'], !sw['f']); // ignore bad usage "-d -f"
    if(out.size() == 0) return ERROR_EMPTY;
    if(sw['s']) sort(out.begin(), out.end(), comps);
    else if(sw['S']) sort(out.begin(), out.end(), compS); // ignore bad usage "-s -S"
    else sort(out.begin(), out.end(), comp);
    return formatFiles(out);
  }
  if(cmd[0] == "pwd") {
    if(args.size() != 0) return ERROR_BAD_USAGE;
    return getAbsolutePath(curDir) + "\n";
  }
  if(cmd[0] == "exit") {
    if(args.size() != 0) return ERROR_BAD_USAGE;
    newSession();
    return "";
  }
  if(cmd[0] == "grep") return ERROR_BAD_USAGE;
  return ERROR_NO_COMMAND;
}

// run a commandline (pipes are possible)
string runCommandLine(string cmd) {
  // split commands
  int n = cmd.length();
  int start = 0, inq = 0;
  VS commands;
  for(int i = 0; i <= n; i++)
    if(i == n || (cmd[i] == '|' && !inq))  { commands.push_back(cmd.substr(start, i-start)); start = i+1; }
    else if(cmd[i] == '"') inq = !inq;
  if(!commands.size()) return "";

  // run the first command
  string lastoutput = runCommand(split(commands[0]));
  string line, s, ret;
  // chain the greps after that
  for(int i = 1; i < commands.size(); i++) {
    stringstream ss(commands[i]);
	if(!(ss >> s) || s != "grep") return ERROR_BAD_USAGE;
	getline(ss, s);
	s = trim(s);
	if(s.length() < 2 || s[0] != '"' || s[s.length()-1] != '"') return ERROR_BAD_USAGE;
	s = s.substr(1, s.length()-2); // get the string to be searched for
	
	stringstream input(lastoutput);
	ret = "";
    while(getline(input, line)) {
      if(line.find(s) != string::npos) ret += line + "\n";
	}
	lastoutput = ret;
  }
  return lastoutput;
}

int main() {
  string cmd;
  newSession();
  while(getline(cin, cmd)) {
    cout << runCommandLine(cmd);
  }
  return 0;
}
// 25878498	10966	3KP-BASH Project	Accepted	C++	0.120	2020-12-23 09:27:17
```
