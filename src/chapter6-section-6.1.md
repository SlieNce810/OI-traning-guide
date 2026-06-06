# 6.1 轮廓线动态规划

## LA3620 Manhattan Wiring

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

## UVa10572 Black and White

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

## UVa11270 Tiling Dominoes

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
