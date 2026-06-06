# 第5章 图论算法与模型

## 5.1 基础题目选讲

### 例题4  猜序列（Guess, Seoul 2008, LA 4255/UVa1423）

```cpp
// 例题4  猜序列（Guess, Seoul 2008, LA 4255/UVa1423）
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<vector>
#include<algorithm>
using namespace std;
const int maxn = 10 + 5;

int n, G[maxn][maxn]; // 注意本题结点编号为0~n
int c[maxn];
vector<int> topo;

bool dfs(int u){
  c[u] = -1;
  for(int v = 0; v <= n; v++) if(G[u][v]) {
    if(c[v]<0) return false;
    else if(!c[v]) dfs(v);
  }
  c[u] = 1; topo.push_back(u);
  return true;
}

bool toposort(){
  topo.clear();
  memset(c, 0, sizeof(c));
  for(int u = 0; u <= n; u++) if(!c[u])
    if(!dfs(u)) return false;
  reverse(topo.begin(), topo.end());
  return true;
}

// 用并查集合并相等结点
int pa[maxn];
int findset(int x) { return pa[x] != x ? pa[x] = findset(pa[x]) : x; }

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    char input[100], S[11][11];
    scanf("%d%s", &n, input);
    int idx = 0;
    for(int i = 0; i <= n; i++) pa[i] = i;
    for(int i = 1; i <= n; i++)
      for(int j = i; j <= n; j++) {
        S[i][j] = input[idx++];
        if(S[i][j] == '0') pa[j] = i-1; // sum[j]-sum[i-1]=0，因此j和i-1是等价结点
      }

    // 若前缀和sum[a] < sum[b]，连边a->b，在拓扑序中a会在b的前面
    memset(G, 0, sizeof(G));
    for(int i = 1; i <= n; i++)
      for(int j = i; j <= n; j++) {
        if(S[i][j] == '-') G[findset(j)][findset(i-1)] = 1; // sum[j]-sum[i-1] < 0
        if(S[i][j] == '+') G[findset(i-1)][findset(j)] = 1; // sum[j]-sum[i-1] > 0
      }
    toposort();
    int sum[maxn], cur = 0;
    for(int i = 0; i <= n; i++) sum[topo[i]] = cur++; // 按照拓扑序依次赋值0, 1, 2, ...
    for(int i = 1; i <= n; i++) {
      sum[i] = sum[findset(i)];
      if(i > 1) printf(" ");
      printf("%d", sum[i] - sum[i-1]); // 注意，sum[0]未必等于0
    }
    printf("\n");
  }
  return 0;
}
// 25878073	1423	Guess	Accepted	C++	0.000	2020-12-23 07:58:02
```

### 例题2  独轮车（The Monocycle, UVa 10047）

```cpp
// 例题2  独轮车（The Monocycle, UVa 10047）
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<queue>
#include<algorithm>
using namespace std;

const int INF = 1000000000;
const int maxr = 25 + 5;
const int maxc = 25 + 5;
int R, C, sr, sc, tr, tc;
char maze[maxr][maxc];

struct State {
  int r, c, dir, color;
  State(int r, int c, int dir, int color):r(r),c(c),dir(dir),color(color) {}
};

const int dr[] = {-1,0,1,0}; // north, west, south, east
const int dc[] = {0,-1,0,1};
int d[maxr][maxc][4][5], vis[maxr][maxc][4][5];

int ans;
queue<State> Q;

void update(int r, int c, int dir, int color, int v) {
  if(r < 0 || r >= R || c < 0 || c >= C) return; // 不能走出边界
  if(maze[r][c] == '.' && !vis[r][c][dir][color]) {
    Q.push(State(r, c, dir, color));
    vis[r][c][dir][color] = 1;
    d[r][c][dir][color] = v;
    if(r == tr && c == tc && color == 0) ans = min(ans, v); // 更新答案
  }
}

void bfs(State st) {
  d[st.r][st.c][st.dir][st.color] = 0;
  vis[st.r][st.c][st.dir][st.color] = 1;
  Q.push(st);
  while(!Q.empty()) {
    st = Q.front(); Q.pop();
    int v = d[st.r][st.c][st.dir][st.color] + 1;
    update(st.r, st.c, (st.dir+1)%4, st.color, v); // 左转
    update(st.r, st.c, (st.dir+3)%4, st.color, v); // 右转
    update(st.r+dr[st.dir], st.c+dc[st.dir], st.dir, (st.color+1)%5, v); // 前进
  }
}

int main() {
  int kase = 0;
  while(scanf("%d%d", &R, &C) == 2 && R && C) {
    for(int i = 0; i < R; i++) {
      scanf("%s", maze[i]);
      for(int j = 0; j < C; j++)
        if(maze[i][j] == 'S') { sr = i; sc = j; }
        else if(maze[i][j] == 'T') { tr = i; tc = j; }
    }
    maze[sr][sc] = maze[tr][tc] = '.';
    ans = INF;
    memset(vis, 0, sizeof(vis));
    bfs(State(sr, sc, 0, 0));

    if(kase > 0) printf("\n");
    printf("Case #%d\n", ++kase);
    if(ans == INF) printf("destination not reachable\n");
    else printf("minimum time = %d sec\n", ans);
  }
}
// 25878076	10047	The Monocycle	Accepted	C++	0.000	2020-12-23 07:58:30
```

### 例题3  项链（The Necklace, UVa 10054）

```cpp
// 例题3  项链（The Necklace, UVa 10054）
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<vector>
using namespace std;
const int maxcolor = 50;
int n, G[maxcolor+1][maxcolor+1], deg[maxcolor+1];

struct Edge {
  int from, to;
  Edge(int from, int to):from(from),to(to) {}
};

vector<Edge> ans;
void euler(int u){
  for(int v = 1; v <= maxcolor; v++) if(G[u][v]) {
    G[u][v]--; G[v][u]--;
    euler(v);
    ans.push_back(Edge(u, v));
  }
}

int main() {
  int T;
  scanf("%d", &T);
  for(int kase = 1; kase <= T; kase++) {
    scanf("%d", &n);
    memset(G, 0, sizeof(G));
    memset(deg, 0, sizeof(deg));
    int start = -1;
    for(int i = 0; i < n; i++) {
      int u, v;
      scanf("%d%d", &u, &v);
      G[u][v]++; G[v][u]++;
      deg[u]++; deg[v]++;
      start = u;
    }

    // 无向图的欧拉回路
    bool solved = true;
    for(int i = 1; i <= maxcolor; i++)
      if(deg[i] % 2 == 1) { solved = false; break; } // 检查度数
    if(solved) {
      ans.clear();
      euler(start);
      if(ans.size() != n || ans[0].to != ans[ans.size()-1].from) solved = false;
    }

    printf("Case #%d\n", kase);
    if(!solved)
      printf("some beads may be lost\n");
    else
      for(int i = ans.size()-1; i >= 0; i--) printf("%d %d\n", ans[i].from, ans[i].to);

    if(kase < T) printf("\n");
  }
  return 0;
}
// 25878077	10054	The Necklace	Accepted	C++	0.230	2020-12-23 07:58:44
```

### 例题1  大火蔓延的迷宫（Fire!, UVa 11624）

```cpp
// 例题1  大火蔓延的迷宫（Fire!, UVa 11624）
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<queue>
#include<algorithm>
using namespace std;

const int INF = 1000000000;
const int maxr = 1000 + 5;
const int maxc = 1000 + 5;
int R, C;
char maze[maxr][maxc];

struct Cell {
  int r, c;
  Cell(int r, int c):r(r),c(c) {}
};

const int dr[] = {-1,1,0,0};
const int dc[] = {0,0,-1,1};
int d[maxr][maxc][2], vis[maxr][maxc][2];

queue<Cell> Q;
void bfs(int kind) {
  while(!Q.empty()) {
    Cell cell = Q.front(); Q.pop();
    int r = cell.r, c = cell.c;
    for(int dir = 0; dir < 4; dir++) {
      int nr = r + dr[dir], nc = c + dc[dir];
      if(nr >= 0 && nr < R && nc >= 0 && nc < C && maze[nr][nc] == '.' && !vis[nr][nc][kind]) {
        Q.push(Cell(nr, nc));
        vis[nr][nc][kind] = 1;
        d[nr][nc][kind] = d[r][c][kind] + 1;
      }
    }
  }
}

int ans;
void check(int r, int c) {
  if(maze[r][c] != '.' || !vis[r][c][0]) return; // 必须是Joe可达的边界格子
  if(!vis[r][c][1] || d[r][c][0] < d[r][c][1]) ans = min(ans, d[r][c][0] + 1); // Joe必须先于火到达
}

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    scanf("%d%d", &R, &C);
    int jr, jc;
    vector<Cell> fires;
    for(int i = 0; i < R; i++) {
      scanf("%s", maze[i]);
      for(int j = 0; j < C; j++)
        if(maze[i][j] == 'J') { jr = i; jc = j; maze[i][j] = '.'; }
        else if(maze[i][j] == 'F') { fires.push_back(Cell(i,j)); maze[i][j] = '.'; }
    }
    memset(vis, 0, sizeof(vis));

    // Joe
    vis[jr][jc][0] = 1; d[jr][jc][0] = 0;
    Q.push(Cell(jr, jc));
    bfs(0);

    // Fire
    for(int i = 0; i < fires.size(); i++) {
      vis[fires[i].r][fires[i].c][1] = 1;
      d[fires[i].r][fires[i].c][1] = 0;
      Q.push(fires[i]);
    }
    bfs(1);

    // 计算答案
    ans = INF;
    for(int i = 0; i < R; i++) { check(i,0); check(i,C-1); }
    for(int i = 0; i < C; i++) { check(0,i); check(R-1,i); }
    if(ans == INF) printf("IMPOSSIBLE\n"); else printf("%d\n", ans);
  }
  return 0;
}
// 25878084	11624	Fire!	Accepted	C++	0.420	2020-12-23 08:00:22
```

## 5.2 深度优先遍历

### 例题9  飞机调度（Now or Later, LA 3211）

```cpp
// 例题9  飞机调度（Now or Later, LA 3211）
// Rujia Liu
#include<cstdio>
#include<vector>
#include<cstring>
using namespace std;

const int maxn = 2000 + 10;

struct TwoSAT {
  int n;
  vector<int> G[maxn*2];
  bool mark[maxn*2];
  int S[maxn*2], c;

  bool dfs(int x) {
    if (mark[x^1]) return false;
    if (mark[x]) return true;
    mark[x] = true;
    S[c++] = x;
    for (int i = 0; i < G[x].size(); i++)
      if (!dfs(G[x][i])) return false;
    return true;
  }

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n*2; i++) G[i].clear();
    memset(mark, 0, sizeof(mark));
  }

  // x = xval or y = yval
  void add_clause(int x, int xval, int y, int yval) {
    x = x * 2 + xval;
    y = y * 2 + yval;
    G[x^1].push_back(y);
    G[y^1].push_back(x);
  }

  bool solve() {
    for(int i = 0; i < n*2; i += 2)
      if(!mark[i] && !mark[i+1]) {
        c = 0;
        if(!dfs(i)) {
          while(c > 0) mark[S[--c]] = false;
          if(!dfs(i+1)) return false;
        }
      }
    return true;
  }
};

///////// 题目相关
#include<algorithm>

TwoSAT solver;

int n, T[maxn][2];

bool test(int diff) {
  solver.init(n);
    for(int i = 0; i < n; i++) for(int a = 0; a < 2; a++)
      for(int j = i+1; j < n; j++) for(int b = 0; b < 2; b++)
        if(abs(T[i][a] - T[j][b]) < diff) solver.add_clause(i, a^1, j, b^1);
  return solver.solve();
}

int main() {
  while(scanf("%d", &n) == 1 && n) {
    int L = 0, R = 0;
    for(int i = 0; i < n; i++) for(int a = 0; a < 2; a++) {
      scanf("%d", &T[i][a]);
      R = max(R, T[i][a]);
    }
    while(L < R) {
      int M = L + (R-L+1)/2;
      if(test(M)) L = M; else R = M-1;
    }
    printf("%d\n", L);
  }
  return 0;
}
// 25878101	1146	Now or later	Accepted	C++	0.540	2020-12-23 08:06:28
```

### 例题5  圆桌骑士（Knights of the Round Table, CERC2005, LA 3523/SPOJ	KNIGHTS

```cpp
// 例题5  圆桌骑士（Knights of the Round Table, CERC2005, LA 3523/SPOJ	KNIGHTS
// 陈锋
#include <bits/stdc++.h>
using namespace std;
struct Edge { int u, v; };
const int NN = 1000 + 10;
int pre[NN], iscut[NN], bccno[NN], dfs_clock, bcc_cnt; // 割顶的bccno无意义
vector<int> G[NN], bcc[NN];

stack<Edge> S;
int dfs(int u, int fa) {
  int lowu = pre[u] = ++dfs_clock, child = 0;
  for (int i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    Edge e = (Edge) {u, v};
    if (!pre[v]) { // 没有访问过v
      S.push(e);
      child++;
      int lowv = dfs(v, u);
      lowu = min(lowu, lowv); // 用后代的low函数更新自己
      if (lowv >= pre[u]) {
        iscut[u] = true, bcc[++bcc_cnt].clear();
        while (true) {
          Edge x = S.top(); S.pop();
          if (bccno[x.u] != bcc_cnt)
            bcc[bcc_cnt].push_back(x.u), bccno[x.u] = bcc_cnt;
          if (bccno[x.v] != bcc_cnt)
            bcc[bcc_cnt].push_back(x.v); bccno[x.v] = bcc_cnt;
          if (x.u == u && x.v == v) break;
        }
      }
    }
    else if (pre[v] < pre[u] && v != fa) {
      S.push(e), lowu = min(lowu, pre[v]); // 用反向边更新自己
    }
  }
  if (fa < 0 && child == 1) iscut[u] = 0;
  return lowu;
}

void find_bcc(int n) { // 调用结束后S保证为空，所以不用清空
  fill_n(pre, n + 1, 0), fill_n(iscut, n + 1, 0), fill_n(bccno, n + 1, 0);
  dfs_clock = bcc_cnt = 0;
  for (int i = 0; i < n; i++)
    if (!pre[i]) dfs(i, -1);
}

int odd[NN], color[NN];
bool bipartite(int u, int b) {
  for (int i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    if (bccno[v] != b) continue;
    if (color[v] == color[u]) return false;
    if (!color[v]) {
      color[v] = 3 - color[u];
      if (!bipartite(v, b)) return false;
    }
  }
  return true;
}

int A[NN][NN];
int main() {
  for (int kase = 0, u, v, n, m; scanf("%d%d", &n, &m) == 2 && n; ) {
    for (int i = 0; i < n; i++) G[i].clear();
    memset(A, 0, sizeof(A));
    for (int i = 0; i < m; i++) {
      scanf("%d%d", &u, &v), u--, v--;
      A[u][v] = A[v][u] = 1;
    }
    for (int u = 0; u < n; u++)
      for (int v = u + 1; v < n; v++)
        if (!A[u][v]) G[u].push_back(v), G[v].push_back(u);

    find_bcc(n);
    memset(odd, 0, sizeof(odd));
    for (int i = 1; i <= bcc_cnt; i++) {
      memset(color, 0, sizeof(color));
      for (int j = 0; j < bcc[i].size(); j++)
        bccno[bcc[i][j]] = i; // 主要是处理割顶
      int u = bcc[i][0];
      color[u] = 1;
      if (!bipartite(u, i))
        for (int j = 0; j < bcc[i].size(); j++) odd[bcc[i][j]] = 1;
    }
    int ans = n;
    for (int i = 0; i < n; i++) if (odd[i]) ans--;
    printf("%d\n", ans);
  }
  return 0;
}
// Accepted 310ms 7987kB 2556 C++(gcc 8.3)2020-12-1416:05:37  27093919
```

### 例题10  宇航员分组（Astronauts, LA3713/UVa1391） CERC2006

```cpp
// 例题10  宇航员分组（Astronauts, LA3713/UVa1391） CERC2006
// 陈锋
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;

const int maxn = 100000 + 5;

struct TwoSAT {
  int n;
  vector<int> G[maxn * 2];
  bool mark[maxn * 2];
  int S[maxn * 2], c;

  bool dfs(int x) {
    if (mark[x ^ 1]) return false;
    if (mark[x]) return true;
    mark[x] = true;
    S[c++] = x;
    for (int i = 0; i < G[x].size(); i++)
      if (!dfs(G[x][i])) return false;
    return true;
  }

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n * 2; i++) G[i].clear();
    memset(mark, 0, sizeof(mark));
  }

  // x = xval or y = yval
  void add_clause(int x, int xval, int y, int yval) {
    x = x * 2 + xval, y = y * 2 + yval;
    G[x ^ 1].push_back(y), G[y ^ 1].push_back(x);
  }

  bool solve() {
    for (int i = 0; i < n * 2; i += 2)
      if (!mark[i] && !mark[i + 1]) {
        c = 0;
        if (!dfs(i)) {
          while (c > 0) mark[S[--c]] = false;
          if (!dfs(i + 1)) return false;
        }
      }
    return true;
  }
};

#include <algorithm> //题目相关
int n, m, total_age, age[maxn];
int is_young(int x) { return age[x] * n < total_age; }
TwoSAT solver;
int main() {
  while (scanf("%d%d", &n, &m) == 2 && n) {
    total_age = 0;
    for (int i = 0; i < n; i++) scanf("%d", &age[i]), total_age += age[i];
    solver.init(n);
    for (int i = 0, a, b; i < m; i++) {
      scanf("%d%d", &a, &b), a--, b--;
      if (a == b) continue;
      solver.add_clause(a, 1, b, 1);    //不能同去任务C
      if (is_young(a) == is_young(b))   //同类宇航员
        solver.add_clause(a, 0, b, 0);  //不能同去任务A或者任务B
    }
    if (!solver.solve()) {
      puts("No solution.");
      continue;
    }
    for (int i = 0; i < n; i++)  // 看看x[i]的值
      if (solver.mark[i * 2])
        puts("C");  // false:去任务C
      else if (is_young(i))
        puts("B");  // true:年轻宇航员去任务B
      else
        puts("A");  // true: 年长宇航员去任务A
  }
  return 0;
}
// 5878107	1391	Astronauts	Accepted	C++	0.230	2020-12-23 08:07:31
```

### 例题7  等价性证明（Proving Equivalences, NWERC2008, LA4287/HDU2767）

```cpp
// 例题7  等价性证明（Proving Equivalences, NWERC2008, LA4287/HDU2767）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

const int NN = 20000 + 10;

vector<int> G[NN];
int pre[NN], lowlink[NN], sccno[NN], dfs_clock, scc_cnt;
stack<int> S;
void dfs(int u) {
  int &lu = lowlink[u];
  pre[u] = lu = ++dfs_clock, S.push(u);
  for (size_t i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    if (!pre[v]) dfs(v), lu = min(lu, lowlink[v]);
    else if (!sccno[v]) lu = min(lu, pre[v]);
  }
  if (lu == pre[u]) {
    scc_cnt++;
    for (int x = -1; x != u; S.pop()) x = S.top(), sccno[x] = scc_cnt;
  }
}

void find_scc(int n) {
  dfs_clock = scc_cnt = 0;
  fill_n(sccno, n, 0), fill_n(pre, n, 0);
  for (int i = 0; i < n; i++)
    if (!pre[i]) dfs(i);
}

int in0[NN], out0[NN];
int main() {
  int T, n, m;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%d", &n, &m);
    for (int i = 0; i < n; i++) G[i].clear();
    for (int i = 0, u, v; i < m; i++) {
      scanf("%d%d", &u, &v), u--, v--;
      G[u].push_back(v);
    }

    find_scc(n);
    fill_n(in0 + 1, scc_cnt, 1), fill_n(out0 + 1, scc_cnt, 1);
    for (int u = 0; u < n; u++)
      for (size_t i = 0; i < G[u].size(); i++) {
        int v = G[u][i];
        if (sccno[u] != sccno[v]) in0[sccno[v]] = out0[sccno[u]] = 0;
      }
    int a = 0, b = 0;
    for (int i = 1; i <= scc_cnt; i++) {
      if (in0[i]) a++;
      if (out0[i]) b++;
    }
    int ans = max(a, b);
    if (scc_cnt == 1) ans = 0;
    printf("%d\n", ans);
  }
  return 0;
}
// Accepted 187ms 5424kB 1665 G++2020-12-14 16:11:27 34870207
```

### 例题6  井下矿工（Mining Your Own Business, World Finals 2011, LA 5135/SPOJ BUSINESS）

```cpp
// 例题6  井下矿工（Mining Your Own Business, World Finals 2011, LA 5135/SPOJ BUSINESS）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int NN = 1e5 + 8;
typedef long long LL;
int Low[NN], Pre[NN], DfsClock, IsCut[NN], BccNo;
vector<int> G[NN], Bcc[NN];

stack<int> S;
void clear(int &n) {
  for (int i = 1; i <= n; ++i)
    G[i].clear(), Pre[i] = 0, IsCut[i] = 0;
  n = BccNo = DfsClock = 0;
}

void tarjan(int u, int root) {
  Pre[u] = Low[u] = ++DfsClock, S.push(u);
  int child = 0;
  for (auto v : G[u]) {
    if (!Pre[v]) {
      tarjan(v, root);
      Low[u] = min(Low[u], Low[v]), child++;
      if (Low[v] == Pre[u]) {
        Bcc[++BccNo].clear();
        for (int x = 0; x != v; S.pop()) Bcc[BccNo].push_back(x = S.top());
        Bcc[BccNo].push_back(u);
      }
      if (u != root && Low[v] >= Pre[u]) IsCut[u] = 1;
    }
    else
      Low[u] = min(Low[u], Pre[v]);
  }
  if (u == root && child > 1) IsCut[u] = 1;
}
int main() {
  for (int kase = 1, n, m; ~scanf("%d", &m) && m; ++kase) {
    clear(n);
    for (int i = 1, x, y; i <= m; ++i) {
      scanf("%d%d", &x, &y);
      n = max(n, max(x, y));
      G[x].push_back(y), G[y].push_back(x);
    }
    for (int i = 1; i <= n; ++i) if (!Pre[i]) tarjan(i, i);
    printf("Case %d:", kase);
    LL ans1 = 0, ans2 = 1;
    for (int i = 1; i <= BccNo; ++i) {
      int cutCnt = 0, sz = Bcc[i].size();
      for (auto v : Bcc[i]) if (IsCut[v]) cutCnt++;
      if (cutCnt == 0) ans1 += 2, ans2 *= 1LL * sz * (sz - 1) / 2;
      else if (cutCnt == 1) ans1++, ans2 *= sz - 1;
    }
    printf(" %lld %lld\n", ans1, ans2);
  }
  return 0;
}
//  Accepted 170ms 20480kB 1710 C++14(gcc 8.3)2020-12-14 16:07:37 27093931
```

### 例题8  最大团（The Largest Clique, UVa 11324）

```cpp
// 例题8  最大团（The Largest Clique, UVa 11324）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int NN = 1000 + 10;
vector<int> G[NN];
int pre[NN], lowlink[NN], sccno[NN], dfs_clock, scc_cnt;
stack<int> S;
void dfs(int u) {
  int& lu = lowlink[u];
  pre[u] = lu = ++dfs_clock, S.push(u);
  for (size_t i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    if (!pre[v])
      dfs(v), lu = min(lu, lowlink[v]);
    else if (!sccno[v])
      lu = min(lu, pre[v]);
  }
  if (lu == pre[u]) {
    scc_cnt++;
    for (int x = -1; x != u; S.pop()) sccno[x = S.top()] = scc_cnt;
  }
}

void find_scc(int n) {
  dfs_clock = scc_cnt = 0;
  fill_n(sccno, n, 0), fill_n(pre, n, 0);
  for (int i = 0; i < n; i++)
    if (!pre[i]) dfs(i);
}

int SccSz[NN], TG[NN][NN], D[NN];
int dp(int u) {
  int& ans = D[u];
  if (ans >= 0) return ans;
  ans = SccSz[u];
  for (int v = 1; v <= scc_cnt; v++)
    if (u != v && TG[u][v]) ans = max(ans, dp(v) + SccSz[u]);
  return ans;
}

int main() {
  int T, n, m;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%d", &n, &m);
    for (int i = 0; i < n; i++) G[i].clear();
    for (int i = 0, u, v; i < m; i++) {
      scanf("%d%d", &u, &v), u--, v--;
      G[u].push_back(v);
    }

    find_scc(n);  // 找强连通分量
    memset(TG, 0, sizeof(TG));
    memset(SccSz, 0, sizeof(SccSz));
    for (int i = 0; i < n; i++) {
      SccSz[sccno[i]]++;  // 累加强连通分量大小（结点数）
      for (size_t j = 0; j < G[i].size(); j++)
        TG[sccno[i]][sccno[G[i][j]]] = 1;  // 构造SCC图
    }

    int ans = 0;
    memset(D, -1, sizeof(D));           // 初始化动态规划记忆化数组
    for (int i = 1; i <= scc_cnt; i++)  // 注意，SCC编号为1~scc_cnt
      ans = max(ans, dp(i));
    printf("%d\n", ans);
  }
  return 0;
}
// Accepted 80ms 1740 C++5.3.0 2020-12-14 16:16:29 25846267
```

## 5.3 最短路问题

### 例题18  低价空中旅行（Low Cost Air Travel, World Finals 2006, LA3561/UVa1048

```cpp
// 例题18  低价空中旅行（Low Cost Air Travel, World Finals 2006, LA3561/UVa1048
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<queue>
#include<algorithm>
using namespace std;

const int INF = 1000000000;
const int maxn = 4000 + 10;

struct Edge {
  int from, to, dist, val;
};

struct HeapNode {
  int d, u;
  bool operator < (const HeapNode& rhs) const {
    return d > rhs.d;
  }
};

struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[maxn];
  bool done[maxn];    // 是否已永久标号
  int d[maxn];        // s到各个点的距离
  int p[maxn];        // 最短路中的上一条弧

  void init(int n) {
    this->n = n;
    for(int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int dist, int val) {
    edges.push_back((Edge){from, to, dist, val});
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

  vector<int> GetShortestPath(int s, int t) {
    vector<int> path;
    while(t != s) {
      path.push_back(edges[p[t]].val);
      t = edges[p[t]].from;
    }
    reverse(path.begin(), path.end());
    return path;
  }
};

//////// 题目相关
#include<map>

int n_cities;
map<int,int> city_id;

int ID(int city) {
  if(city_id.count(city)) return city_id[city];
  city_id[city] = n_cities++;
  return n_cities-1;
}

int ID(int visited, int cur) { return (visited-1) * n_cities + cur; }

const int maxnt = 100;
int cost[maxnt];
vector<int> cities[maxnt], iti;

Dijkstra solver;

int main() {
  int NT, NI, x, len, kase = 0;
  while(scanf("%d", &NT) == 1 && NT) {
    n_cities = 0;
    city_id.clear();
    for(int i = 0; i < NT; i++) {
      cities[i].clear();
      scanf("%d%d", &cost[i], &len);
      while(len--) { scanf("%d", &x); cities[i].push_back(ID(x)); }
    }
    scanf("%d", &NI);
    kase++;
    for(int trip = 1; trip <= NI; trip++) {
      iti.clear();
      scanf("%d", &len);
      for(int i = 0; i < len; i++) { scanf("%d", &x); iti.push_back(ID(x)); }

      solver.init(n_cities * len);
      for(int ticket = 0; ticket < NT; ticket++)
        for(int visited = 1; visited < len; visited++) {
          int cur = cities[ticket][0]; // 当前状态为(visited, cur)
          int next = visited;          // 下一个需要访问的城市在iti中的下标
          for(int leg = 1; leg < cities[ticket].size(); leg++) { // 使用前leg段
            if(cities[ticket][leg] == iti[next]) next++; // 行程上多经过一个城市
            solver.AddEdge(ID(visited, cur), ID(next, cities[ticket][leg]), cost[ticket], ticket+1);
            if(next == len) break; // 行程单已经走完
          }
        }
      int src = ID(1, iti[0]), dest = ID(len, iti[len-1]);
      solver.dijkstra(src);
      printf("Case %d, Trip %d: Cost = %d\n", kase, trip, solver.d[dest]);
      printf("  Tickets used:");
      vector<int> path = solver.GetShortestPath(src, dest);
      for(int i = 0; i < path.size(); i++) printf(" %d", path[i]);
      printf("\n");
    }
  }
  return 0;
}
// 25878128	1048	Low Cost Air Travel	Accepted	C++	0.000	2020-12-23 08:11:36
```

### 例题19  动物园大逃亡（Animal Run, 北京 2006, UVa1376 LA 3661）

```cpp
// 例题19  动物园大逃亡（Animal Run, 北京 2006, UVa1376 LA 3661）
// Rujia Liu
// ：每个三角形一个结点
#include<cstdio>
#include<cstring>
#include<queue>
#include<algorithm>
using namespace std;

const int INF = 1000000000;
const int maxn = 2000000 + 10;

struct Edge {
  int from, to, dist;
};

struct HeapNode {
  int d, u;
  bool operator < (const HeapNode& rhs) const {
    return d > rhs.d;
  }
};

struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[maxn];
  bool done[maxn];    // 是否已永久标号
  int d[maxn];        // s到各个点的距离
  int p[maxn];        // 最短路中的上一条弧

  void init(int n) {
    this->n = n;
    for(int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int dist) {
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

//////// 题目相关
#define REP(i,n) for(int i = 0; i < (n); ++i)

int n, m;
int ID(int r, int c, int half) { return half * n * m + r * m + c + 1; }

const int maxsize = 1000;
int cost[maxsize][maxsize][3];

Dijkstra solver;

int main() {
  int kase = 0;
  while(scanf("%d%d", &n, &m) == 2 && n && m) {
    REP(i,n) REP(j,m-1) scanf("%d", &cost[i][j][0]); // 横线
    REP(i,n-1) REP(j,m) scanf("%d", &cost[i][j][1]); // 竖线
    REP(i,n-1) REP(j,m-1) scanf("%d", &cost[i][j][2]); // 斜线
    solver.init(2*n*m+2);
    REP(i,n-1) REP(j,m-1) {
      // 左下half=0
      int id1 = ID(i, j, 0);
      if(j > 0) solver.AddEdge(id1, ID(i, j-1, 1), cost[i][j][1]); // 左
      if(i < n-1) solver.AddEdge(id1, ID(i+1, j, 1), cost[i+1][j][0]); // 下

      // 右上half=1
      int id2 = ID(i, j, 1);
      if(j < m-1) solver.AddEdge(id2, ID(i, j+1, 0), cost[i][j+1][1]); // 右
      if(i > 0) solver.AddEdge(id2, ID(i-1, j, 0), cost[i][j][0]); // 上

      solver.AddEdge(id1, id2, cost[i][j][2]);
      solver.AddEdge(id2, id1, cost[i][j][2]);
    }
    // 从起点到左/下边界的弧
    REP(i, n-1) solver.AddEdge(0, ID(i, 0, 0), cost[i][0][1]); // 左
    REP(i, m-1) solver.AddEdge(0, ID(n-2, i, 0), cost[n-1][i][0]); // 下

    // 从右/上边界到终点的弧
    REP(i, n-1) solver.AddEdge(ID(i, m-2, 1), 2*n*m+1, cost[i][m-1][1]); // 右
    REP(i, m-1) solver.AddEdge(ID(0, i, 1), 2*n*m+1, cost[0][i][0]); // 上
    solver.dijkstra(0);

    // 找出右/上边界的最少d值
    printf("Case %d: Minimum = %d\n", ++kase, solver.d[2*n*m+1]);
  }
  return 0;
}
// 25878139	1376	Animal Run	Accepted	C++	1.110	2020-12-23 08:13:32
```

### 例题13  战争和物流（Warfare and Logistics, LA4080/UVa1416）

```cpp
// 例题13  战争和物流（Warfare and Logistics, LA4080/UVa1416）
// 陈锋
#include<cstdio>
#include<cstring>
#include<vector>
#include<algorithm>
#include<queue>
using namespace std;

const int INF = 1e9, NN = 100 + 8;
struct Edge { int from, to, dist; };
struct HeapNode {
  int d, u;
  bool operator < (const HeapNode& rhs) const {
    return d > rhs.d;
  }
};

template<size_t SZ>
struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[SZ];
  bool done[SZ];		//是否已永久标号
  int d[SZ];			//s到各个点的距离
  int p[SZ];			//最短路中的上一条弧

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int dist) {
    edges.push_back((Edge) {from, to, dist});
    m = edges.size();
    G[from].push_back(m - 1);
  }

  void dijkstra(int s) {
    priority_queue<HeapNode> Q;
    for (int i = 0; i < n; i++) d[i] = INF;
    d[s] = 0;
    memset(done, 0, sizeof(done));
    Q.push((HeapNode) {0, s});
    while (!Q.empty()) {
      HeapNode x = Q.top(); Q.pop();
      int u = x.u;
      if (done[u]) continue;
      done[u] = true;
      for (size_t i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if (e.dist > 0 && d[e.to] > d[u] + e.dist) {
          //此处和模板不同，忽略了dist = -1的边。
          // 此为删除标记。
          // 根据题意和dijkstra算法的前提，正常的边dist > 0
          d[e.to] = d[u] + e.dist;
          p[e.to] = G[u][i];
          Q.push((HeapNode) {d[e.to], e.to});
        }
      }
    }
  }
};

//题目相关
Dijkstra<NN> solver;
int N, M, L;
vector<int> gr[NN][NN];	//两点之间的原始边权
int used[NN][NN][NN]; //used[src][a][b]表示源点为src的最短路树是否包含边a->b
int idx[NN][NN];      //idx[u][v]为边u->v在Dijkstra求解器中的编号
int sum_single[NN]; //sum_single[src]表示源点为src的最短路树的所有d之和

int compute_c() {
  int ans = 0;
  memset(used, 0, sizeof(used));
  for (int src = 0; src < N; src++) {
    solver.dijkstra(src);
    sum_single[src] = 0;
    for (int i = 0; i < N; i++) {
      if (i != src) {
        int fa = solver.edges[solver.p[i]].from;
        used[src][fa][i] = used[src][i][fa] = 1;
      }
      sum_single[src] += (solver.d[i] == INF ? L : solver.d[i]);
    }
    ans += sum_single[src];
  }
  return ans;
}

int compute_newc(int a, int b) {
  int ans = 0;
  for (int src = 0; src < N; src++)
    if (!used[src][a][b]) ans += sum_single[src];
    else {
      solver.dijkstra(src);
      for (int i = 0; i < N; i++)
        ans += (solver.d[i] == INF ? L : solver.d[i]);
    }
  return ans;
}

int main() {
  while (scanf("%d%d%d", &N, &M, &L) == 3) {
    solver.init(N);
    for (int i = 0; i < N; i++)
      for (int j = 0; j < N; j++) gr[i][j].clear();

    for (int i = 0, a, b, s; i < M; i++) {
      scanf("%d%d%d", &a, &b, &s), a--, b--;
      gr[a][b].push_back(s), gr[b][a].push_back(s);
    }

    //构造网络
    for (int i = 0; i < N; i++)
      for (int j = i + 1; j < N; j++) if (!gr[i][j].empty()) {
          sort(gr[i][j].begin(), gr[i][j].end());
          solver.AddEdge(i, j, gr[i][j][0]);
          idx[i][j] = solver.m - 1;
          solver.AddEdge(j, i, gr[i][j][0]);
          idx[j][i] = solver.m - 1;
        }

    int c = compute_c(), c2 = -1;
    for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++)
        if (!gr[i][j].empty()) {
          int& e1 = solver.edges[idx[i][j]].dist;
          int& e2 = solver.edges[idx[j][i]].dist;
          if (gr[i][j].size() == 1) e1 = e2 = -1;
          else e1 = e2 = gr[i][j][1]; //第一、第二短的边
          c2 = max(c2, compute_newc(i, j));
          e1 = e2 = gr[i][j][0]; //恢复
        }

    printf("%d %d\n", c, c2);
  }
  return 0;
}
// Accepted 230ms 3538 C++ 5.3.0 2020-12-14 17:00:37 25846446
```

### 例题17  蒸汽式压路机（Steam Roller, LA 4128/UVa1078）

```cpp
// 例题17  蒸汽式压路机（Steam Roller, LA 4128/UVa1078）
// 刘汝佳
#include <cstdio>
#include <cstring>
#include <iostream>
#include <queue>
using namespace std;
const int INF = 1e9, maxn = 50000 + 10;
struct Edge {
  int from, to, dist;
};
struct HeapNode {
  int d, u;
  bool operator<(const HeapNode& rhs) const { return d > rhs.d; }
};
struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[maxn];
  bool done[maxn];  // 是否已永久标号
  int d[maxn];      // s到各个点的距离
  int p[maxn];      // 最短路中的上一条弧

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int dist) {
    edges.push_back((Edge){from, to, dist});
    m = edges.size();
    G[from].push_back(m - 1);
  }

  void dijkstra(int s) {
    priority_queue<HeapNode> Q;
    for (int i = 0; i < n; i++) d[i] = INF;
    d[s] = 0;
    memset(done, 0, sizeof(done));
    Q.push((HeapNode){0, s});
    while (!Q.empty()) {
      HeapNode x = Q.top();
      Q.pop();
      int u = x.u;
      if (done[u]) continue;
      done[u] = true;
      for (int i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if (d[e.to] > d[u] + e.dist) {
          d[e.to] = d[u] + e.dist, p[e.to] = G[u][i];
          Q.push((HeapNode){d[e.to], e.to});
        }
      }
    }
  }
};

//////// 题目相关

const int UP = 0, LEFT = 1, DOWN = 2, RIGHT = 3;

const int inv[] = {2, 3, 0, 1};
const int dr[] = {-1, 0, 1, 0};  // 上左下右
const int dc[] = {0, -1, 0, 1};
const int maxr = 100, maxc = 100;
int grid[maxr][maxc][4], n, id[maxr][maxc][5], R, C;
int ID(int r, int c, int dir) {
  int& x = id[r][c][dir];
  if (x == 0) x = ++n;  // 从1开始编号
  return x;
}
bool cango(int r, int c, int dir) {
  if (r < 0 || r >= R || c < 0 || c >= C) return false;  // 走出网格
  return grid[r][c][dir] > 0;                            // 此路不通？
}

Dijkstra solver;

int main() {
  int r1, c1, r2, c2, kase = 0;
  while (cin >> R >> C >> r1 >> c1 >> r2 >> c2 && R) {
    r1--, c1--, r2--, c2--;
    for (int r = 0; r < R; r++) {
      for (int c = 0; c < C - 1; c++) {
        cin >> grid[r][c + 1][LEFT];
        grid[r][c][RIGHT] = grid[r][c + 1][LEFT];
      }
      if (r != R - 1)
        for (int c = 0; c < C; c++) {
          cin >> grid[r + 1][c][UP];
          grid[r][c][DOWN] = grid[r + 1][c][UP];
        }
    }
    solver.init(R * C * 5 + 1);
    n = 0, memset(id, 0, sizeof(id));
    // 源点出发的边
    for (int dir = 0; dir < 4; dir++)
      if (cango(r1, c1, dir)) {
        solver.AddEdge(0, ID(r1 + dr[dir], c1 + dc[dir], dir),
                       grid[r1][c1][dir] * 2);  // 开始走下去
        solver.AddEdge(0, ID(r1 + dr[dir], c1 + dc[dir], 4),
                       grid[r1][c1][dir] * 2);  // 走一步停下来
      }

    // 计算每个状态(r,c,dir)的后继状态
    for (int r = 0; r < R; r++)
      for (int c = 0; c < C; c++) {
        for (int dir = 0; dir < 4; dir++)
          if (cango(r, c, inv[dir])) {
            solver.AddEdge(ID(r, c, dir), ID(r, c, 4),
                           grid[r][c][inv[dir]]);  // 停下来！
            if (cango(r, c, dir))
              solver.AddEdge(ID(r, c, dir), ID(r + dr[dir], c + dc[dir], dir),
                             grid[r][c][dir]);  // 继续走
          }
        for (int dir = 0; dir < 4; dir++)
          if (cango(r, c, dir)) {
            solver.AddEdge(ID(r, c, 4), ID(r + dr[dir], c + dc[dir], dir),
                           grid[r][c][dir] * 2);  // 重新开始走
            solver.AddEdge(ID(r, c, 4), ID(r + dr[dir], c + dc[dir], 4),
                           grid[r][c][dir] * 2);  // 走一步停下来
          }
      }

    solver.dijkstra(0);
    int ans = solver.d[ID(r2, c2, 4)];  // 找最优解
    printf("Case %d: ", ++kase);
    if (ans == INF)
      printf("Impossible\n");
    else
      printf("%d\n", ans);
  }
  return 0;
}
// 25878161	1078	Steam Roller	Accepted	C++	0.070	2020-12-23 08:17:38
```

### 例题14  过路费（加强版）（The Toll! Revisited, UVa 10537）

```cpp
// 例题14  过路费（加强版）（The Toll! Revisited, UVa 10537）
// 陈锋
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<cctype>
using namespace std;

const int NN = 52 + 10;
const long long INF = 1LL << 60;
typedef long long LL;

int N, G[NN][NN], St, Ed, P, Vis[NN]; // 标记
LL D[NN];     // D[i]表示从点i出发（已经交过点i的税了）时至少要带多少东西，到Ed时还能剩p个东西

int read_node() {
  char s[9];
  scanf("%s", s);
  if (isupper(s[0])) return s[0] - 'A';
  return s[0] - 'a' + 26;
}
char node_label(int u) { return u < 26 ? 'A' + u : 'a' + (u - 26); }
LL forward(LL k, int u) { // 拿着k个东西去结点u，还剩多少个东西
  if (u < 26) return k - (k + 19) / 20; // 镇子
  return k - 1; // 村子
}
// 至少要拿着多少个东西到达结点u，交税以后还能剩D[u]个东西
LL back(int u) {
  if (u >= 26) return D[u] + 1; // 村子
  LL X = D[u] * 20 / 19; // 初始值
  while (forward(X, u) < D[u]) X++; // 调整，容易理解的做法
  return X;
}
void solve() {
  N = 52; // 总是有52个结点
  fill_n(Vis, N + 1, 0), fill_n(D, N, INF);
  D[Ed] = P, Vis[Ed] = 1;
  for (int i = 0; i < N; i++)
    if (i != Ed && G[i][Ed]) D[i] = back(Ed);

  while (!Vis[St]) { // Dijkstra主过程，逆推，规模小就不要优先级队列了
    int minu = -1; // 找最小的D[u]的u
    for (int i = 0; i < N; i++)
      if (!Vis[i] && (minu < 0 || D[i] < D[minu])) minu = i;
    Vis[minu] = 1;
    for (int i = 0; i < N; i++)
      if (!Vis[i] && G[i][minu]) D[i] = min(D[i], back(minu)); // 更新其他结点的d
  }
  printf("%lld\n%c", D[St], node_label(St)); // 输出
  LL k = D[St]; // 当前手里有多少货?
  for (int u = St, next; u != Ed; u = next) {
    for (next = 0; next < N; next++) // 找到第一个可以走的结点
      if (G[u][next] && forward(k, next) >= D[next]) break;
    k = D[next];
    printf("-%c", node_label(next));
    u = next;
  }
  puts("");
}

int main() {
  for (int kase = 1; scanf("%d", &N) == 1 && N >= 0; kase++) {
    memset(G, 0, sizeof(G));
    for (int i = 0; i < N; i++) {
      int u = read_node(), v = read_node();
      if (u != v) G[u][v] = G[v][u] = 1;
    }
    scanf("%d", &P);
    St = read_node(), Ed = read_node();
    printf("Case %d:\n", kase);
    solve();
  }
  return 0;
}
// 25878179	10537	The Toll! Revisited	Accepted	C++	0.000	2020-12-23 08:23:15
```

### 例题12  林中漫步（A Walk Through the Forest, UVa 10917）

```cpp
// 例题12  林中漫步（A Walk Through the Forest, UVa 10917）
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<queue>
using namespace std;

const int INF = 1000000000;
const int maxn = 1000 + 10;

struct Edge {
  int from, to, dist;
};

struct HeapNode {
  int d, u;
  bool operator < (const HeapNode& rhs) const {
    return d > rhs.d;
  }
};

struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[maxn];
  bool done[maxn];    // 是否已永久标号
  int d[maxn];        // s到各个点的距离
  int p[maxn];        // 最短路中的上一条弧

  void init(int n) {
    this->n = n;
    for(int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int dist) {
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

//////// 题目相关
Dijkstra solver;
int d[maxn]; // 到家距离

int dp(int u) {
  if(u == 1) return 1; // 到家了

  int& ans = d[u];
  if(ans >= 0) return ans;

  ans = 0;
  for(int i = 0; i < solver.G[u].size(); i++) {
    int v = solver.edges[solver.G[u][i]].to;
    if(solver.d[v] < solver.d[u]) ans += dp(v);
  }
  return ans;
}

int main() {
  int n, m;
  while(scanf("%d%d", &n, &m) == 2) {
    solver.init(n);
    for(int i = 0; i < m; i++) {
      int a, b, c;
      scanf("%d%d%d", &a, &b, &c); a--; b--;
      solver.AddEdge(a, b, c);
      solver.AddEdge(b, a, c);
    }

    solver.dijkstra(1); // 家(1)到所有点的距离。因为道路都是双向的，所以把家看作起点也行
    memset(d, -1, sizeof(d));
    printf("%d\n", dp(0)); // 办公室(0)到家的符合条件的路径条数
  }
  return 0;
}
// 25878181	10917	Walk Through the Forest	Accepted	C++	0.010	2020-12-23 08:23:48
```

### 例题15  在环中（Going in Cycle!!, UVa 11090）

```cpp
// 例题15  在环中（Going in Cycle!!, UVa 11090）
// 陈锋
#include<cstdio>
#include<cstring>
#include<queue>
using namespace std;

const int INF = 1e9, NN = 1000;

struct Edge {
  int from, to;
  double dist;
};

struct BellmanFord {
  int n, m;
  vector<Edge> edges;
  vector<int> G[NN];
  bool inq[NN];     // 是否在队列中
  double d[NN];     // s到各个点的距离
  int p[NN];        // 最短路中的上一条弧
  int cnt[NN];      // 进队次数

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, double dist) {
    edges.push_back((Edge) {from, to, dist});
    m = edges.size();
    G[from].push_back(m - 1);
  }

  bool negativeCycle() {
    queue<int> Q;
    memset(inq, 0, sizeof(inq));
    memset(cnt, 0, sizeof(cnt));
    for (int i = 0; i < n; i++) { d[i] = 0; inq[0] = true; Q.push(i); }

    while (!Q.empty()) {
      int u = Q.front(); Q.pop();
      inq[u] = false;
      for (int i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if (d[e.to] > d[u] + e.dist) {
          d[e.to] = d[u] + e.dist;
          p[e.to] = G[u][i];
          if (!inq[e.to]) { Q.push(e.to); inq[e.to] = true; if (++cnt[e.to] > n) return true; }
        }
      }
    }
    return false;
  }
};

BellmanFord solver;
bool test(double x) {
  for (int i = 0; i < solver.m; i++)
    solver.edges[i].dist -= x;
  bool ret = solver.negativeCycle();
  for (int i = 0; i < solver.m; i++)
    solver.edges[i].dist += x;
  return ret;
}

int main() {
  int T; scanf("%d", &T);
  for (int kase = 1, n, m; scanf("%d%d", &n, &m), kase <= T; kase++) {
    solver.init(n);
    int ub = 0;
    for (int i = 0, u, v, w; i < m; i++) {
      scanf("%d%d%d", &u, &v, &w), u--, v--, ub = max(ub, w);
      solver.AddEdge(u, v, w);
    }
    printf("Case #%d: ", kase);
    if (!test(ub + 1)) printf("No cycle found.\n");
    else {
      double L = 0, R = ub;
      while (R - L > 1e-3) {
        double M = L + (R - L) / 2;
        if (test(M)) R = M; else L = M;
      }
      printf("%.2lf\n", L);
    }
  }
  return 0;
}
// Accepted 50ms 2056 C++11 5.3.0 2020-01-31 17:59:48 24490896
```

### 例题11  机场快线（Airport Express, UVa 11374）

```cpp
// 例题11  机场快线（Airport Express, UVa 11374）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
struct Edge {
  int u, v, d;
  bool operator<(const Edge& e) const { return d < e.d; }
};

struct HeapNode {
  int u, d;
  bool operator<(const HeapNode& rhs) const { return d > rhs.d; }
};

template <int SZV, int INF>  // |V|
struct Dijkstra {
  int n;
  vector<Edge> edges;
  vector<int> G[SZV];
  bool done[SZV];
  int d[SZV], p[SZV];

  void init(int n) {
    assert(n < SZV);
    this->n = n;
    edges.clear();
    _for(i, 0, n) G[i].clear();
  }

  void addEdge(int u, int v, int d) {  // u-v,d
    G[u].push_back(edges.size()), edges.push_back({u, v, d});
  }

  void dijkstra(int s) {
    priority_queue<HeapNode> Q;
    fill_n(done, n, false), fill_n(d, n, INF);
    d[s] = 0, Q.push({s, 0});
    while (!Q.empty()) {
      HeapNode x = Q.top();
      Q.pop();
      int u = x.u;  // select a node nearest to the current node set
      if (done[u]) continue;
      done[u] = true;

      for (size_t ei = 0; ei < G[u].size(); ei++) {
        const auto& e = edges[G[u][ei]];
        int v = e.v;
        if (d[v] > d[u] + e.d)
          d[v] = d[u] + e.d, p[v] = G[u][ei], Q.push({v, d[v]});
      }
    }
  }

  // path of s->e
  void getPath(int s, int e, deque<int>& path, bool rev = false) {
    assert(d[s] == 0), assert(d[e] != INF);
    int x = e;
    if (rev) path.push_back(x);
    else path.push_front(x);
    while (x != s) {
      x = edges[p[x]].u;
      if (rev) path.push_back(x);
      else path.push_front(x);
    }
  }
};

const int MAXN = 500 + 4, INF = 1e9;
int main() {
  Dijkstra<MAXN, INF> SD, ED;  // S -> * , E -> *
  for (int t = 0, N, S, E, M, K, u, v, d; scanf("%d%d%d", &N, &S, &E) == 3; t++) {
    if (t) puts("");
    SD.init(N + 1), ED.init(N + 1);
    scanf("%d", &M);
    for (int i = 0; i < M; i++) {  // Economy-Xpress
      scanf("%d%d%d", &u, &v, &d);
      SD.addEdge(u, v, d), SD.addEdge(v, u, d);
      ED.addEdge(u, v, d), ED.addEdge(v, u, d);
    }
    SD.dijkstra(S), ED.dijkstra(E);
    int cu = -1, ans = INF;
    deque<int> path;
    if (SD.d[E] < ans) ans = SD.d[E], SD.getPath(S, E, path);

    auto update = [&](int u, int v, int d) {  // S -> u -> v -> E;
      if (SD.d[u] < ans && ED.d[v] < ans && SD.d[u] + d + ED.d[v] < ans) {
        ans = SD.d[u] + d + ED.d[v], cu = u, path.clear();
        SD.getPath(S, u, path), ED.getPath(E, v, path, true);
      }
    };

    scanf("%d", &K);
    _for(i, 0, K)
      scanf("%d%d%d", &u, &v, &d), update(u, v, d), update(v, u, d);
    _for(i, 0, path.size()) {
      if (i) printf(" ");
      printf("%d", path[i]);
    }
    puts("");
    if (cu == -1) puts("Ticket Not Used");
    else printf("%d\n", cu);
    printf("%d\n", ans);
  }
  return 0;
}
// 18869546 11374 Airport Express Accepted C++11 0.000 2017-03-01 03:10:33
```

### 例题16  Halum操作（Halum, UVa 11478）

```cpp
// 例题16  Halum操作（Halum, UVa 11478）
// 陈锋
#include <cstdio>
#include <cstring>
#include <queue>
using namespace std;

const int INF = 1e9, NN = 500 + 10, MM = 2700 + 10;
struct Edge {
  int to, dist;
};

// 邻接表写法
struct BellmanFord {
  int n, m, head[NN], next[MM];
  Edge edges[MM];
  bool inq[NN];  // 是否在队列中
  int d[NN];     // s到各个点的距离
  int cnt[NN];   // 进队次数

  void init(int n) {
    this->n = n;
    m = 0, memset(head, -1, sizeof(head));
  }

  void AddEdge(int from, int to, int dist) {
    next[m] = head[from], head[from] = m, edges[m++] = (Edge){to, dist};
  }

  bool negativeCycle() {
    queue<int> Q;
    memset(inq, 0, sizeof(inq)), memset(cnt, 0, sizeof(cnt));
    for (int i = 0; i < n; i++) d[i] = 0, Q.push(i);
    while (!Q.empty()) {
      int u = Q.front();
      Q.pop();
      inq[u] = false;
      for (int i = head[u]; i != -1; i = next[i]) {
        Edge& e = edges[i];
        if (d[e.to] > d[u] + e.dist) {
          d[e.to] = d[u] + e.dist;
          if (!inq[e.to]) {
            Q.push(e.to), inq[e.to] = true;
            if (++cnt[e.to] > n) return true;
          }
        }
      }
    }
    return false;
  }
};

BellmanFord solver;

// 判断在初始差分约束系统的每个不等式右侧同时减去x之后是否有解
bool test(int x) {
  for (int i = 0; i < solver.m; i++) solver.edges[i].dist -= x;
  bool ret = solver.negativeCycle();
  for (int i = 0; i < solver.m; i++) solver.edges[i].dist += x;
  return !ret;  // 如果有负环，说明差分约束系统无解
}

int main() {
  for (int n, m; scanf("%d%d", &n, &m) == 2;) {
    solver.init(n);
    int ub = 0;
    for (int i = 0, u, v, d; i < m; i++) {
      scanf("%d%d%d", &u, &v, &d);
      ub = max(ub, d);
      solver.AddEdge(u - 1, v - 1, d);
    }
    if (test(ub + 1))
      puts("Infinite");  // 如果可以让每条边权都>ub，说明每条边的权都增加了，重复一次会增加得更多...直到无限
    else if (!test(1))
      puts("No Solution");
    else {
      int L = 2, R = ub, ans = 1;
      while (L <= R) {
        int M = L + (R - L) / 2;
        if (test(M)) ans = M, L = M + 1;
        else R = M - 1;
      }
      printf("%d\n", ans);
    }
  }
  return 0;
}
// Accepted 820ms 2089 C++5.3.0 2020-12-1417:56:15 25846657
```

## 5.4 生成树相关问题

### 例题20  秦始皇修路（Qin Shi Huang’s National Road System, 北京 2011, LA5713/UVa1494）

```cpp
// 例题20  秦始皇修路（Qin Shi Huang’s National Road System, 北京 2011, LA5713/UVa1494）
// Rujia Liu
#include<cstdio>
#include<cmath>
#include<cstring>
#include<vector>
#include<algorithm>
using namespace std;

const int maxn = 1000 + 10;
int n, m, x[maxn], y[maxn], p[maxn];

int pa[maxn];
int findset(int x) { return pa[x] != x ? pa[x] = findset(pa[x]) : x; } 

vector<int> G[maxn];
vector<double> C[maxn];

struct Edge {
  int x, y;
  double d;
  bool operator < (const Edge& rhs) const {
    return d < rhs.d;
  }
};

Edge e[maxn*maxn];

double maxcost[maxn][maxn];
vector<int> nodes;

void dfs(int u, int fa, double facost) {
  for(int i = 0; i < nodes.size(); i++) {
    int x = nodes[i];
    maxcost[u][x] = maxcost[x][u] = max(maxcost[x][fa], facost);
  }
  nodes.push_back(u);
  for(int i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    if(v != fa) dfs(v, u, C[u][i]);
  }
}

double MST() {
  m = 0;
  for(int i = 0; i < n; i++)
    for(int j = i+1; j < n; j++)
      e[m++] = (Edge) { i, j, sqrt((x[i]-x[j])*(x[i]-x[j]) + (y[i] - y[j])*(y[i] - y[j])) };
  sort(e, e+m);
  for(int i = 0; i < n; i++) { pa[i] = i; G[i].clear(); C[i].clear(); }
  int cnt = 0;
  double ans = 0;
  for(int i = 0; i < m; i++) {
    int x = e[i].x, y = e[i].y, u = findset(x), v = findset(y);
    double d = e[i].d;
    if(u != v) {
      pa[u] = v;
      G[x].push_back(y); C[x].push_back(d);
      G[y].push_back(x); C[y].push_back(d);
      ans += d;
      if(++cnt == n-1) break;
    }
  }
  return ans;
}

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    scanf("%d", &n);
    for(int i = 0; i < n; i++) scanf("%d%d%d", &x[i], &y[i], &p[i]);
    double tot = MST();
    memset(maxcost, 0, sizeof(maxcost));
    nodes.clear();
    dfs(0, -1, 0);
    double ans = -1;
    for(int i = 0; i < n; i++)
      for(int j = i+1; j < n; j++) {
        ans = max(ans, (p[i] + p[j]) / (tot - maxcost[i][j]));
      }
   printf("%.2lf\n", ans);
  }
  return 0;
}
// 25878195	1494	Qin Shi Huang's National Road System	Accepted	C++	0.090	2020-12-23 08:29:32
```

### 例题21  邦德（Bond, UVa 11354）

```cpp
// 例题21  邦德（Bond, UVa 11354）
// 陈锋
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)

const int MAXN = 50000 + 4;
struct Edge {
  int u, v, w;
  Edge(int _u = 0, int _v = 0, int _w = 0) : u(_u), v(_v), w(_w) {}
  bool operator<(const Edge& e) const {
    return w < e.w;
  }
};

int N, M;
vector<Edge> G[MAXN]; // MST Tree
int L, Tin[MAXN], Tout[MAXN], UP[MAXN][20], MaxW[MAXN][20], timer;

bool isAncestor(int u, int v) { return Tin[u] <= Tin[v] && Tout[u] >= Tout[v]; }

void dfs(int u, int fa, int w) {
  Tin[u] = ++timer, UP[u][0] = fa, MaxW[u][0] = w;
  for (int i = 1; i <= L; i++) {
    int ui = UP[u][i - 1];
    UP[u][i] = UP[ui][i - 1];
    MaxW[u][i] = max(MaxW[u][i - 1], MaxW[ui][i - 1]);
  }
  _for(i, 0, G[u].size()) {
    const Edge& e = G[u][i];
    if (e.v != fa) dfs(e.v, u, e.w);
  }
  Tout[u] = ++timer;
}

int LCA(int u, int v) {
  if (isAncestor(u, v)) return u;
  if (isAncestor(v, u)) return v;
  for (int i = L; i >= 0; --i) if (!isAncestor(UP[u][i], v)) u = UP[u][i];
  return UP[u][0];
}

int find_maxw(int u, int v) { // max w of v → u, u = Ancestor(v)
  if (u == v) return 0;
  assert(isAncestor(u, v));
  int w = 0;
  for (int i = L; i >= 0; --i) {
    if (!isAncestor(UP[v][i], u) && UP[v][i] != u) { // 保证u是v的祖先，且u != v
      w = max(w, MaxW[v][i]);
      v = UP[v][i];
    }
  }
  assert(UP[v][0] == u);
  return max(w, MaxW[v][0]);
}

int PA[MAXN]; // Union-Set
int find_pa(int i) { return PA[i] == i ? i : (PA[i] = find_pa(PA[i])); }

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  vector<Edge> es;
  for (int kase = 0, Q; cin >> N >> M; kase++) {
    L = ceil(log2(N));
    if (kase) puts("");
    es.clear();
    Edge e;
    _for(i, 0, M) cin >> e.u >> e.v >> e.w, es.push_back(e);
    sort(es.begin(), es.end());
    _rep(i, 1, N) PA[i] = i;
    _rep(i, 0, N) G[i].clear();
    _for(i, 0, es.size()) {
      const Edge& e = es[i];
      int u = e.u, v = e.v, pu = find_pa(u), pv = find_pa(v);
      if (pu != pv) {
        PA[pv] = pu;
        G[u].push_back(Edge(u, v, e.w)), G[v].push_back(Edge(v, u, e.w));
      }
    }
    timer = 0, dfs(1, 1, 0); // MST LCA
    cin >> Q;
    for (int i = 0, s, t; i < Q; i++) {
      cin >> s >> t;
      int l = LCA(s, t);
      assert(s != t);
      printf("%d\n", max(find_maxw(l, s), find_maxw(l, t)));
    }
  }
  return 0;
}
// Accepted 70ms 2400 C++11 5.3.0 2020-01-31 11:54:07 24489014
```

### 例题22  比赛网络（Stream My Contest, UVa 11865）

```cpp
// 例题22  比赛网络（Stream My Contest, UVa 11865）
// 刘汝佳
#include <bits/stdc++.h>
using namespace std;
const int INF = 1e9, maxn = 100 + 10;

// 固定根的最小树型图，邻接矩阵写法
struct MDST {
  int n;
  int w[maxn][maxn]; // 边权
  int vis[maxn];     // 访问标记，仅用来判断无解
  int ans;           // 计算答案
  int removed[maxn]; // 每个点是否被删除
  int cid[maxn];     // 所在圈编号
  int pre[maxn];     // 最小入边的起点
  int iw[maxn];      // 最小入边的权值
  int max_cid;       // 最大圈编号

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++)
      for (int j = 0; j < n; j++) w[i][j] = INF;
  }

  void AddEdge(int u, int v, int cost) {
    w[u][v] = min(w[u][v], cost); // 重边取权最小的
  }

  // 从s出发能到达多少个结点
  int dfs(int s) {
    vis[s] = 1;
    int ans = 1;
    for (int i = 0; i < n; i++)
      if (!vis[i] && w[s][i] < INF) ans += dfs(i);
    return ans;
  }

  // 从u出发沿着pre指针找圈
  bool cycle(int u) {
    max_cid++;
    int v = u;
    while (cid[v] != max_cid) { cid[v] = max_cid; v = pre[v]; }
    return v == u;
  }

  // 计算u的最小入弧，入弧起点不得在圈c中
  void update(int u) {
    iw[u] = INF;
    for (int i = 0; i < n; i++)
      if (!removed[i] && w[i][u] < iw[u]) {
        iw[u] = w[i][u];
        pre[u] = i;
      }
  }

  // 根结点为s，如果失败则返回false
  bool solve(int s) {
    memset(vis, 0, sizeof(vis));
    if (dfs(s) != n) return false;

    memset(removed, 0, sizeof(removed));
    memset(cid, 0, sizeof(cid));
    for (int u = 0; u < n; u++) update(u);
    pre[s] = s; iw[s] = 0; // 根结点特殊处理
    ans = max_cid = 0;
    for (;;) {
      bool have_cycle = false;
      for (int u = 0; u < n; u++) if (u != s && !removed[u] && cycle(u)) {
          have_cycle = true;
          // 以下代码缩圈，圈上除了u之外的结点均删除
          int v = u;
          do {
            if (v != u) removed[v] = 1;
            ans += iw[v];
            // 对于圈外点i，把边i->v改成i->u（并调整权值）；v->i改为u->i
            // 注意圈上可能还有一个v'使得i->v'或者v'->i存在，因此只保留权值最小的i->u和u->i
            for (int i = 0; i < n; i++) if (cid[i] != cid[u] && !removed[i]) {
                if (w[i][v] < INF) w[i][u] = min(w[i][u], w[i][v] - iw[v]);
                w[u][i] = min(w[u][i], w[v][i]);
                if (pre[i] == v) pre[i] = u;
              }
            v = pre[v];
          } while (v != u);
          update(u);
          break;
        }
      if (!have_cycle) break;
    }
    for (int i = 0; i < n; i++)
      if (!removed[i]) ans += iw[i];
    return true;
  }
};

//////// 题目相关
MDST solver;
struct Edge {
  int u, v, b, c;
  bool operator < (const Edge& rhs) const {
    return b > rhs.b;
  }
};

const int maxm = 10000 + 10;
int N, M, C;
Edge edges[maxm];

// 取b前cnt大的边构造网络，判断最小树型图的边权和是否小于C
bool check(int cnt) {
  solver.init(N);
  for (int i = 0; i < cnt; i++)
    solver.AddEdge(edges[i].u, edges[i].v, edges[i].c);
  if (!solver.solve(0)) return false;
  return solver.ans <= C;
}

int main() {
  int T;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%d%d", &N, &M, &C);
    for (int i = 0; i < M; i++) {
      scanf("%d%d%d%d", &edges[i].u, &edges[i].v, &edges[i].b, &edges[i].c);
    }
    sort(edges, edges + M);
    int l = 1, r = M, ans = -1;
    while (l <= r) {
      int m = l + (r - l) / 2;
      if (check(m)) ans = edges[m - 1].b, r = m - 1;
      else l = m + 1;
    }
    if (ans < 0) printf("streaming not possible.\n");
    else printf("%d kbps\n", ans);
  }
  return 0;
}
// Accepted 10ms 3277 C++11 5.3.0 2020-01-3111:54:45 24489015
```

## 5.5 二分图匹配

### 例题25  固定分区内存管理（Fixed Partition Memory Management, World Finals 2001, LA 2238/UVa1006

```cpp
// 例题25  固定分区内存管理（Fixed Partition Memory Management, World Finals 2001, LA 2238/UVa1006
// Rujia Liu
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;

const int maxn = 500 + 5;  // 顶点的最大数目
const int INF = 1e9;

// 最大权匹配
struct KM {
  int n;                   // 左右顶点个数
  vector<int> G[maxn];     // 邻接表
  int W[maxn][maxn];       // 权值
  int Lx[maxn], Ly[maxn];  // 顶标
  int left[maxn];  // left[i]为右边第i个点的匹配点编号，-1表示不存在
  bool S[maxn], T[maxn];  // S[i]和T[i]为左/右第i个点是否已标记

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    memset(W, 0, sizeof(W));
  }

  void AddEdge(int u, int v, int w) { G[u].push_back(v), W[u][v] = w; }

  bool match(int u) {
    S[u] = true;
    for (int i = 0; i < G[u].size(); i++) {
      int v = G[u][i];
      if (Lx[u] + Ly[v] == W[u][v] && !T[v]) {
        T[v] = true;
        if (left[v] == -1 || match(left[v])) {
          left[v] = u;
          return true;
        }
      }
    }
    return false;
  }

  void update() {
    int a = INF;
    for (int u = 0; u < n; u++)
      if (S[u])
        for (int i = 0; i < G[u].size(); i++) {
          int v = G[u][i];
          if (!T[v]) a = min(a, Lx[u] + Ly[v] - W[u][v]);
        }
    for (int i = 0; i < n; i++) {
      if (S[i]) Lx[i] -= a;
      if (T[i]) Ly[i] += a;
    }
  }

  void solve() {
    for (int i = 0; i < n; i++) {
      Lx[i] = *max_element(W[i], W[i] + n), left[i] = -1, Ly[i] = 0;
    }
    for (int u = 0; u < n; u++) {
      for (;;) {
        for (int i = 0; i < n; i++) S[i] = T[i] = false;
        if (match(u))
          break;
        else
          update();
      }
    }
  }
};

KM solver;

const int maxp = 50 + 5;  // 程序(program)的最大数目
const int maxr = 10 + 5;  // 区域(region)的最大数目
int n, m;                 // 程序数目和区域数目
int runtime[maxp][maxr];  // runtime[p][r]为程序p在区域r中的运行时间

// 打印具体方案
void print_solution() {
  // 起始时刻、分配到得区域编号、总回转时间
  int start[maxp], region_number[maxp], total = 0;
  for (int r = 0; r < m; r++) {
    vector<int>
        programs;  // 本region执行的所有程序，按照逆序排列（“倒数”第pos个程序）
    for (int pos = 0; pos < n; pos++) {
      int right = r * n + pos, left = solver.left[right];
      if (left >= n) break;  // 匹配到虚拟结点，说明本region已经没有更多程序了
      programs.push_back(left), region_number[left] = r;
      total -= solver.W[left][right];  // 权值取过相反数
    }
    reverse(programs.begin(), programs.end());
    for (size_t i = 0, time = 0; i < programs.size(); i++)
      start[programs[i]] = time, time += runtime[programs[i]][r];
  }

  printf("Average turnaround time = %.2lf\n", (double)total / n);
  for (int p = 0; p < n; p++)
    printf("Program %d runs in region %d from %d to %d\n", p + 1,
           region_number[p] + 1, start[p],
           start[p] + runtime[p][region_number[p]]);
  printf("\n");
}

int main() {
  for (int kase = 1; scanf("%d%d", &m, &n) == 2 && m && n; kase++) {
    solver.init(m * n);
    int size[maxr];
    for (int r = 0; r < m; r++) scanf("%d", &size[r]);
    for (int p = 0; p < n; p++) {
      int s[10], t[10], k;
      scanf("%d", &k);
      for (int i = 0; i < k; i++) scanf("%d%d", &s[i], &t[i]);
      for (int r = 0; r < m; r++) {  // 计算程序p在内存区域r中的运行时间
        int& time = runtime[p][r];
        time = INF;
        if (size[r] < s[0]) continue;
        for (int i = 0; i < k; i++)
          if (i == k - 1 || size[r] < s[i + 1]) {
            time = t[i];
            break;
          }

        // 连边X(p) -> Y(r,pos)
        for (int pos = 0; pos < n; pos++)
          solver.AddEdge(p, r * n + pos,
                         -(pos + 1) * time);  // 本题要求最小值，权值要取相反数
      }
    }

    // 补完其他边
    for (int i = n; i < n * m; i++)
      for (int j = 0; j < n * m; j++) solver.AddEdge(i, j, 1);
    solver.solve();
    printf("Case %d\n", kase);
    print_solution();
  }
  return 0;
}
// Accepted 940ms 3795 C++5.3.0 2020-12-1418:34:10 25846819
```

### 例题29  出租车（Taxi Cab Scheme, NWERC 2004, LA 3126/POJ2060

```cpp
// 例题29  出租车（Taxi Cab Scheme, NWERC 2004, LA 3126/POJ2060
// 陈锋
#include <cstdio>
#include <cstring>
#include <vector>
#include <algorithm>
using namespace std;

const int maxn = 500 + 5;  // 单侧顶点的最大数目

// 二分图最大基数匹配，邻接矩阵写法
struct BPM {
  int n, m;           // 左右顶点个数
  int G[maxn][maxn];  // 邻接表
  int left[maxn];  // left[i]为右边第i个点的匹配点编号，-1表示不存在
  bool T[maxn];  // T[i]为右边第i个点是否已标记

  void init(int n, int m) {
    this->n = n, this->m = m;
    memset(G, 0, sizeof(G));
  }

  bool match(int u) {
    for (int v = 0; v < m; v++)
      if (G[u][v] && !T[v]) {
        T[v] = true;
        if (left[v] == -1 || match(left[v])) {
          left[v] = u;
          return true;
        }
      }
    return false;
  }

  // 求最大匹配
  int solve() {
    fill_n(left, m + 1, -1);
    int ans = 0;
    for (int u = 0; u < n; u++) {  // 从左边结点u开始增广
      fill_n(T, m + 1, false);
      if (match(u)) ans++;
    }
    return ans;
  }
};

BPM solver;
int X1[maxn], Y1[maxn], X2[maxn], Y2[maxn], T1[maxn], T2[maxn];
inline int dist(int a, int b, int c, int d) { return abs(a - c) + abs(b - d); }

int main() {
  int T;
  scanf("%d", &T);
  for (int t = 0, n; t < T; t++) {
    scanf("%d", &n);
    for (int i = 0, h, m; i < n; i++) {
      scanf("%d:%d%d%d%d%d", &h, &m, &X1[i], &Y1[i], &X2[i], &Y2[i]);
      T1[i] = h * 60 + m, T2[i] = T1[i] + dist(X1[i], Y1[i], X2[i], Y2[i]);
    }
    solver.init(n, n);
    for (int i = 0; i < n; i++)
      for (int j = i + 1; j < n; j++)
        if (T2[i] + dist(X2[i], Y2[i], X1[j], Y1[j]) < T1[j])
          solver.G[i][j] = 1;  // 至少要提前1分钟到达
    printf("%d\n", n - solver.solve());
  }
  return 0;
}
// Accepted 188ms 1332kB 1704 G++2020-12-14 18:19:37 22209579
```

### 例题28  保守的老师（Guardian of Decency, NWERC 2005, LA 3415/POJ2771

```cpp
// 例题28  保守的老师（Guardian of Decency, NWERC 2005, LA 3415/POJ2771
// 陈锋
#include <cstdio>
#include <cstring>
#include <vector>
#include <algorithm>
using namespace std;

const int maxn = 500 + 5; // 单侧顶点的最大数目

// 二分图最大基数匹配，邻接矩阵写法
struct BPM {
  int n, m;               // 左右顶点个数
  int G[maxn][maxn];      // 邻接表
  int left[maxn];         // left[i]为右边第i个点的匹配点编号，-1表示不存在
  bool T[maxn];           // T[i]为右边第i个点是否已标记

  void init(int n, int m) {
    this->n = n, this->m = m;
    memset(G, 0, sizeof(G));
  }

  bool match(int u) {
    for (int v = 0; v < m; v++) if (G[u][v] && !T[v]) {
        T[v] = true;
        if (left[v] == -1 || match(left[v])) {
          left[v] = u;
          return true;
        }
      }
    return false;
  }

  // 求最大匹配
  int solve() {
    int ans = 0;
    fill_n(left, m + 1, -1);
    for (int u = 0; u < n; u++) { // 从左边结点u开始增广
      fill_n(T, m + 1, false);
      if (match(u)) ans++;
    }
    return ans;
  }
};

BPM solver;

#include<iostream>
#include<string>
struct Student {
  int h;
  string music, sport;
  Student(int h = 0, const string& music = "", const string& sport = "")
    : h(h), music(music), sport(sport) {}
};

bool conflict(const Student& a, const Student& b) {
  return abs(a.h - b.h) <= 40 && a.music == b.music && a.sport != b.sport;
}

int main() {
  int T; cin >> T;
  for (int t = 0, n; cin >> n, t < T; t++) {
    vector<Student> male, female;
    Student s;
    for (int i = 0; i < n; i++) {
      string gender;
      cin >> s.h >> gender >> s.music >> s.sport;
      if (gender[0] == 'M') male.push_back(s);
      else female.push_back(s);
    }
    int x = male.size(), y = female.size();
    solver.init(x, y);
    for (int i = 0; i < x; i++)
      for (int j = 0; j < y; j++)
        if (conflict(male[i], female[j])) solver.G[i][j] = 1;
    printf("%d\n", x + y - solver.solve());
  }
  return 0;
}
// Accepted 1641ms 1728kB 1908 G++ 2020-12-14 18:16:47 22209571
```

### 例题26  女士的选择（Ladies’ Choice, SWERC 2007, LA3989/UVa1175

```cpp
// 例题26  女士的选择（Ladies’ Choice, SWERC 2007, LA3989/UVa1175
// Rujia Liu
#include<cstdio>
#include<queue>
using namespace std;

const int maxn = 1000 + 10;
int pref[maxn][maxn], order[maxn][maxn], nxt[maxn], future_husband[maxn], future_wife[maxn];
queue<int> q; // 未订婚的男士队列

void engage(int man, int woman) {
  int m = future_husband[woman];
  if(m) {
    future_wife[m] = 0; // 抛弃现任未婚夫（如果有的话）
    q.push(m); // 加入未订婚男士队列
  }
  future_wife[man] = woman;
  future_husband[woman] = man;
}

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    int n;
    scanf("%d", &n);

    for(int i = 1; i <= n; i++) {
      for(int j = 1; j <= n; j++)
        scanf("%d", &pref[i][j]); // 编号为i的男士第j喜欢的人
      nxt[i] = 1; // 接下来应向排名为1的女士求婚
      future_wife[i] = 0; // 没有未婚妻
      q.push(i);
    }

    for(int i = 1; i <= n; i++) {
      for(int j = 1; j <= n; j++) {
        int x;
        scanf("%d", &x);
        order[i][x] = j; // 在编号为i的女士心目中，编号为x的男士的排名
      }
      future_husband[i] = 0; // 没有未婚夫
    }

    while(!q.empty()) {
      int man = q.front(); q.pop();
      int woman = pref[man][nxt[man]++];
      if(!future_husband[woman]) engage(man, woman); // woman没有未婚夫，直接订婚
      else if(order[woman][man] < order[woman][future_husband[woman]]) engage(man, woman); // 换未婚夫
      else q.push(man); // 下次再来
    }
    while(!q.empty()) q.pop();

    for(int i = 1; i <= n; i++) printf("%d\n", future_wife[i]);
    if(T) printf("\n");
  }
  return 0;
}
// 25878224	1175	Ladies' Choice	Accepted	C++	0.190	2020-12-23 08:37:23
```

### 例题23  蚂蚁（Ants, NEERC 2008, LA 4043/POJ3565

```cpp
// 例题23  蚂蚁（Ants, NEERC 2008, LA 4043/POJ3565
// 陈锋
#include <cstdio>
#include <cstring>
#include <cmath>
#include <algorithm>
#include <cassert>
using namespace std;

const double INF = 1e30;
template<size_t SZ>
struct KM {
  double W[SZ][SZ]; // 权值
  double Lx[SZ], Ly[SZ];   // 顶标
  int n, left[SZ];          // left[i]为右边第i个点的匹配点编号
  bool S[SZ], T[SZ];   // S[i]和T[i]为左/右第i个点是否已标记

  bool eq(double a, double b) { return fabs(a - b) < 1e-9; }

  void init(size_t _n) {
    assert(_n < SZ);
    this->n = _n;
  }

  bool match(int i) {
    S[i] = true;
    for (int j = 1; j <= n; j++) if (eq(Lx[i] + Ly[j], W[i][j]) && !T[j]) {
        T[j] = true;
        if (!left[j] || match(left[j])) {
          left[j] = i;
          return true;
        }
      }
    return false;
  }

  void update() {
    double a = INF;
    for (int i = 1; i <= n; i++) if (S[i])
        for (int j = 1; j <= n; j++) if (!T[j])
            a = min(a, Lx[i] + Ly[j] - W[i][j]);
    for (int i = 1; i <= n; i++) {
      if (S[i]) Lx[i] -= a;
      if (T[i]) Ly[i] += a;
    }
  }

  void solve() {
    for (int i = 1; i <= n; i++) {
      left[i] = Lx[i] = Ly[i] = 0;
      for (int j = 1; j <= n; j++)
        Lx[i] = max(Lx[i], W[i][j]);
    }
    for (int i = 1; i <= n; i++) {
      for (;;) {
        for (int j = 1; j <= n; j++) S[j] = T[j] = 0;
        if (match(i)) break; else update();
      }
    }
  }
};

const int NN = 100 + 10;
KM<NN> solver;
int main() {
  for (int kase = 1, n; scanf("%d", &n) == 1; kase++) {
    if (kase > 1) printf("\n");
    solver.init(n);
    int x1[NN], y1[NN], x2[NN], y2[NN];
    for (int i = 1; i <= n; i++)
      scanf("%d%d", &x1[i], &y1[i]);
    for (int i = 1; i <= n; i++)
      scanf("%d%d", &x2[i], &y2[i]);
    for (int i = 1; i <= n; i++) // ant colony
      for (int j = 1; j <= n; j++) // apple tree
        solver.W[j][i] = -sqrt((double)(x1[i] - x2[j]) * (x1[i] - x2[j]) + (double)(y1[i] - y2[j]) * (y1[i] - y2[j]));
    solver.solve(); // 最大权匹配
    for (int i = 1; i <= n; i++) printf("%d\n", solver.left[i]);
  }
  return 0;
}
// Accepted 113ms 2066 C++11 5.3.02020-02-0212:09:15
```

### 例题24  少林决胜（Golden Tiger Claw, UVa 11383）

```cpp
// 例题24  少林决胜（Golden Tiger Claw, UVa 11383）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

const int INF = 1e9;
template<size_t SZ>
struct KM {
  int n;                  // 左右顶点个数
  vector<int> G[SZ];    // 邻接表
  int W[SZ][SZ];      // 权值
  int Lx[SZ], Ly[SZ]; // 顶标
  int left[SZ];         // left[i]为右边第i个点的匹配点编号，-1表示不存在
  bool S[SZ], T[SZ];  // S[i]和T[i]为左/右第i个点是否已标记

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    memset(W, 0, sizeof(W));
  }

  void AddEdge(int u, int v, int w) {
    G[u].push_back(v), W[u][v] = w;
  }

  bool match(int u) {
    S[u] = true;
    for (size_t i = 0; i < G[u].size(); i++) {
      int v = G[u][i];
      if (Lx[u] + Ly[v] == W[u][v] && !T[v]) {
        T[v] = true;
        if (left[v] == -1 || match(left[v])) {
          left[v] = u;
          return true;
        }
      }
    }
    return false;
  }

  void update() {
    int a = INF;
    for (int u = 0; u < n; u++) if (S[u])
        for (size_t i = 0; i < G[u].size(); i++) {
          int v = G[u][i];
          if (!T[v]) a = min(a, Lx[u] + Ly[v] - W[u][v]);
        }
    for (int i = 0; i < n; i++) {
      if (S[i]) Lx[i] -= a;
      if (T[i]) Ly[i] += a;
    }
  }

  void solve() {
    for (int i = 0; i < n; i++) {
      Lx[i] = *max_element(W[i], W[i] + n);
      left[i] = -1;
      Ly[i] = 0;
    }
    for (int u = 0; u < n; u++) {
      for (;;) {
        for (int i = 0; i < n; i++) S[i] = T[i] = false;
        if (match(u)) break; else update();
      }
    }
  }
};

const int maxn = 500 + 5; // 顶点的最大数目
KM<maxn> km;
int main() {
  for (int n, w; scanf("%d", &n) == 1; ) {
    km.init(n);
    for (int i = 0; i < n; i++)
      for (int j = 0; j < n; j++)
        scanf("%d", &w), km.AddEdge(i, j, w);
    km.solve();
    int sum = 0;
    for (int i = 0; i < n - 1; i++) printf("%d ", km.Lx[i]), sum += km.Lx[i];
    printf("%d\n", km.Lx[n - 1]);
    for (int i = 0; i < n - 1; i++) printf("%d ", km.Ly[i]), sum += km.Ly[i];
    printf("%d\n", km.Ly[n - 1]);
    printf("%d\n", sum + km.Lx[n - 1] + km.Ly[n - 1]);
  }
  return 0;
}
// Accepted 80ms 2072 C++11 5.3.02020-02-02 12:23:15
```

### 例题27  我是SAM（SAM I AM, UVa 11419）

```cpp
// 例题27  我是SAM（SAM I AM, UVa 11419）
// 陈锋
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;

const int maxn = 1000 + 5;  // 单侧顶点的最大数目

// 二分图最大基数匹配
struct BPM {
  int n, m;             // 左右顶点个数
  vector<int> G[maxn];  // 邻接表
  int left[maxn];  // left[i]为右边第i个点的匹配点编号，-1表示不存在
  bool T[maxn];  // T[i]为右边第i个点是否已标记

  int right[maxn];  // 求最小覆盖用
  bool S[maxn];     // 求最小覆盖用

  void init(int n, int m) {
    this->n = n, this->m = m;
    for (int i = 0; i < n; i++) G[i].clear();
  }

  void AddEdge(int u, int v) { G[u].push_back(v); }

  bool match(int u) {
    S[u] = true;
    for (size_t i = 0; i < G[u].size(); i++) {
      int v = G[u][i];
      if (!T[v]) {
        T[v] = true;
        if (left[v] == -1 || match(left[v])) {
          left[v] = u, right[u] = v;
          return true;
        }
      }
    }
    return false;
  }

  // 求最大匹配
  int solve() {
    fill_n(left, m + 1, -1), fill_n(right, n + 1, -1);
    int ans = 0;
    for (int u = 0; u < n; u++) {  // 从左边结点u开始增广
      fill_n(S, n + 1, false), fill_n(T, m + 1, false);
      if (match(u)) ans++;
    }
    return ans;
  }

  // 求最小覆盖。X和Y为最小覆盖中的点集
  int mincover(vector<int>& X, vector<int>& Y) {
    int ans = solve();
    fill_n(S, n + 1, false), fill_n(T, m + 1, false);
    for (int u = 0; u < n; u++) if (right[u] == -1) match(u); // 从所有X未盖点出发增广
    for (int u = 0; u < n; u++) if (!S[u]) X.push_back(u); // X中的未标记点
    for (int v = 0; v < m; v++) if (T[v]) Y.push_back(v); // Y中的已标记点
    return ans;
  }
};

BPM solver;
int main() {
  for (int R, C, N; scanf("%d%d%d", &R, &C, &N) == 3 && R && C && N;) {
    solver.init(R, C);
    for (int i = 0, r, c; i < N; i++)
      scanf("%d%d", &r, &c), r--, c--, solver.AddEdge(r, c);
    vector<int> X, Y;
    int ans = solver.mincover(X, Y);
    printf("%d", ans);
    for (size_t i = 0; i < X.size(); i++) printf(" r%d", X[i] + 1);
    for (size_t i = 0; i < Y.size(); i++) printf(" c%d", Y[i] + 1);
    printf("\n");
  }
  return 0;
}
// Accepted 20ms 2047 C++5.3.0 2020-12-14 18:14:53 25846729
```

## 5.6 网络流问题

### 例题32  足球联赛（The K-league, 大田 2002, LA 2531/UVa1306

```cpp
// 例题32  足球联赛（The K-league, 大田 2002, LA 2531/UVa1306
// Rujia Liu
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <numeric>
#include <queue>
#include <vector>
using namespace std;

const int maxn = 700, INF = 1e9;

struct Edge {
  int from, to, cap, flow;
};
bool operator<(const Edge &a, const Edge &b) {
  return a.from < b.from || (a.from == b.from && a.to < b.to);
}
struct Dinic {
  int n, m, s, t;
  vector<Edge> edges; // 边数的两倍
  vector<int> G[maxn]; // 邻接表，G[i][j]表示结点i的第j条边在e数组中的序号
  bool vis[maxn]; // BFS使用
  int d[maxn];    // 从起点到i的距离
  int cur[maxn];  // 当前弧指针

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++)
      G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int cap) {
    edges.push_back((Edge){from, to, cap, 0});
    edges.push_back((Edge){to, from, 0, 0});
    m = edges.size();
    G[from].push_back(m - 2), G[to].push_back(m - 1);
  }

  bool BFS() {
    fill_n(vis, n + 1, false);
    queue<int> Q;
    Q.push(s), vis[s] = true, d[s] = 0;
    while (!Q.empty()) {
      int x = Q.front();
      Q.pop();
      for (size_t i = 0; i < G[x].size(); i++) {
        Edge &e = edges[G[x][i]];
        if (!vis[e.to] && e.cap > e.flow)
          vis[e.to] = true, d[e.to] = d[x] + 1, Q.push(e.to);
      }
    }
    return vis[t];
  }

  int DFS(int x, int a) {
    if (x == t || a == 0)
      return a;
    int flow = 0, f;
    for (int &i = cur[x]; i < G[x].size(); i++) {
      Edge &e = edges[G[x][i]];
      if (d[x] + 1 == d[e.to] && (f = DFS(e.to, min(a, e.cap - e.flow))) > 0) {
        e.flow += f, edges[G[x][i] ^ 1].flow -= f, flow += f, a -= f;
        if (a == 0)
          break;
      }
    }
    return flow;
  }

  int Maxflow(int s, int t) {
    this->s = s, this->t = t;
    int flow = 0;
    while (BFS())
      fill_n(cur, n + 1, 0), flow += DFS(s, INF);
    return flow;
  }
};
Dinic g;
const int maxt = 25 + 5;
int n, w[maxt], d[maxt], a[maxt][maxt];
inline int ID(int u, int v) { return u * n + v + 1; }
inline int ID(int u) { return n * n + u + 1; }
bool canWin(int team) { // 计算team全胜后的总胜利场数
  int total = w[team] + accumulate(a[team], a[team] + n, 0);
  for (int i = 0; i < n; i++) // 全胜又如何?
    if (w[i] > total)         // 有人已经胜的更多了
      return false;

  // 构图。s=0, 结点(u,v)的编号为u*n+v+1, 结点u的编号为n^2+u+1, t=n^2+n+1
  g.init(n * n + n + 2);
  int full = 0, s = 0, t = n * n + n + 1;
  for (int u = 0; u < n; u++) {
    for (int v = u + 1; v < n; v++) {
      if (a[u][v] > 0)
        g.AddEdge(s, ID(u, v), a[u][v]); // S到(u,v)的弧, 容量是剩余的场次
      full += a[u][v]; // (u,v)到u,v的弧，流量表示胜利属于?
      g.AddEdge(ID(u, v), ID(u), INF), g.AddEdge(ID(u, v), ID(v), INF);
    }
    if (w[u] < total)
      g.AddEdge(ID(u), t, total - w[u]); // u到T的弧，u的只能再胜total-w[u]局
  }
  return g.Maxflow(s, t) == full;
}

int main() {
  int T;
  scanf("%d", &T);
  while (T--) {
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
      scanf("%d%d", &w[i], &d[i]);
    for (int i = 0; i < n; i++)
      for (int j = 0; j < n; j++)
        scanf("%d", &a[i][j]);

    for (int i = 0, first = 1; i < n; i++)
      if (canWin(i)) {
        printf("%s", first ? "" : " "), first = 0;
        printf("%d", i+1);
      }
    printf("\n");
  }
  return 0;
}
// 25878256	10779	Collectors Problem	Accepted	C++	0.000	2020-12-23 08:44:16
```

### 例题31  运送超级计算机（Bring Them There, NEERC 2003,LA2957/UVa1324

```cpp
// 例题31  运送超级计算机（Bring Them There, NEERC 2003,LA2957/UVa1324
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<queue>
#include<vector>
#include<algorithm>
using namespace std;

const int maxn = 5000 + 10;
const int INF = 1000000000;

struct Edge {
  int from, to, cap, flow;
};

bool operator < (const Edge& a, const Edge& b) {
  return a.from < b.from || (a.from == b.from && a.to < b.to);
}

struct Dinic {
  int n, m, s, t;
  vector<Edge> edges;    // 边数的两倍
  vector<int> G[maxn];   // 邻接表，G[i][j]表示结点i的第j条边在e数组中的序号
  bool vis[maxn];        // BFS使用
  int d[maxn];           // 从起点到i的距离
  int cur[maxn];         // 当前弧指针

  void init() { edges.clear(); }

  void clearNodes(int a, int b) {
    for(int i = a; i <= b; i++) G[i].clear();
  }

  void AddEdge(int from, int to, int cap) {
    edges.push_back((Edge){from, to, cap, 0});
    edges.push_back((Edge){to, from, 0, 0});
    m = edges.size();
    G[from].push_back(m-2);
    G[to].push_back(m-1);
  }

  bool BFS() {
    memset(vis, 0, sizeof(vis));
    queue<int> Q;
    Q.push(s);
    vis[s] = 1;
    d[s] = 0;
    while(!Q.empty()) {
      int x = Q.front(); Q.pop();
      for(int i = 0; i < G[x].size(); i++) {
        Edge& e = edges[G[x][i]];
        if(!vis[e.to] && e.cap > e.flow) {
          vis[e.to] = 1;
          d[e.to] = d[x] + 1;
          Q.push(e.to);
        }
      }
    }
    return vis[t];
  }

  int DFS(int x, int a) {
    if(x == t || a == 0) return a;
    int flow = 0, f;
    for(int& i = cur[x]; i < G[x].size(); i++) {
      Edge& e = edges[G[x][i]];
      if(d[x] + 1 == d[e.to] && (f = DFS(e.to, min(a, e.cap-e.flow))) > 0) {
        e.flow += f;
        edges[G[x][i]^1].flow -= f;
        flow += f;
        a -= f;
        if(a == 0) break;
      }
    }
    return flow;
  }

  // 求s-t最大流。如果最大流超过limit，则只找一个流量为limit的流
  int Maxflow(int s, int t, int limit) {
    this->s = s; this->t = t;
    int flow = 0;
    while(BFS()) {
      memset(cur, 0, sizeof(cur));
      flow += DFS(s, limit - flow);
      if(flow == limit) break; // 达到流量限制，直接退出
    }
    return flow;
  }
};

Dinic g;

const int maxm = 200 + 10;
int main() {
  int n, m, k, S, T;
  int u[maxm], v[maxm]; // 输入边
  while(scanf("%d%d%d%d%d", &n, &m, &k, &S, &T) == 5) {
    for(int i = 0; i < m; i++) scanf("%d%d", &u[i], &v[i]);
    g.init();
    int day = 1;
    g.clearNodes(0, n-1); // 第一层结点编号为0~n-1。第day层(day>=1)结点编号为day*n~day*n+n-1
    int flow = 0;
    for(;;) {
      // 判断day天是否有解
      // 一架飞船最多需要n-1天到达目的地，沿着这一路线最多需要n+k-2天就可以运完所有飞船，总结点数不超过(n+k-1)n
      g.clearNodes(day*n, day*n+n-1);
      for(int i = 0; i < n; i++) g.AddEdge((day-1)*n+i, day*n+i, INF); // 原地不动
      for(int i = 0; i < m; i++) {
        g.AddEdge((day-1)*n+u[i]-1, day*n+v[i]-1, 1); // u[i]->v[i]
        g.AddEdge((day-1)*n+v[i]-1, day*n+u[i]-1, 1); // v[i]->u[i]
      }
      flow += g.Maxflow(S-1, day*n+T-1, k - flow);
      if(flow == k) break;
      day++;
    }

    // 输出解
    printf("%d\n", day);
    int idx = 0;
    vector<int> location(k, S); // 每架飞船的当前位置
    for(int d = 1; d <= day; d++) {
      idx += n*2;
      vector<int> moved(k, 0); // 第d天有没有移动飞船i
      vector<int> a, b;        // 第d天有一架飞船从a[i]到b[i]
      for(int i = 0; i < m; i++) {
        int f1 = g.edges[idx].flow; idx += 2;
        int f2 = g.edges[idx].flow; idx += 2;
        if(f1 == 1 && f2 == 0) { a.push_back(u[i]); b.push_back(v[i]); }
        if(f1 == 0 && f2 == 1) { a.push_back(v[i]); b.push_back(u[i]); }
      }
      printf("%d", a.size());
      for(int i = 0; i < a.size(); i++) {
        // 查找是哪架飞船从a[i]移动到了b[i]
        for(int j = 0; j < k; j++)
          if(!moved[j] && location[j] == a[i]) {
            printf(" %d %d", j+1, b[i]);
            moved[j] = 1;
            location[j] = b[i];
            break;
          }
      }
      printf("\n");
    }
  }
  return 0;
}
// 25878251	1324	Bring Them There	Accepted	C++	0.030	2020-12-23 08:43:47
```

### 例题33  收集者的难题（Collectors Problem, UVa 10779）

```cpp
// 例题33  收集者的难题（Collectors Problem, UVa 10779）
// Rujia Liu
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>
using namespace std;
const int maxn = 100 + 10, INF = 1e9;
struct Edge {
  int from, to, cap, flow;
};
bool operator<(const Edge &a, const Edge &b) {
  return a.from < b.from || (a.from == b.from && a.to < b.to);
}
struct Dinic {
  int n, m, s, t;
  vector<Edge> edges; // 边数的两倍
  vector<int> G[maxn]; // 邻接表，G[i][j]表示结点i的第j条边在e数组中的序号
  bool vis[maxn]; // BFS使用
  int d[maxn];    // 从起点到i的距离
  int cur[maxn];  // 当前弧指针
  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++)
      G[i].clear();
    edges.clear();
  }
  void ClearFlow() {
    for (size_t i = 0; i < edges.size(); i++)
      edges[i].flow = 0;
  }
  void AddEdge(int from, int to, int cap) {
    edges.push_back((Edge){from, to, cap, 0});
    edges.push_back((Edge){to, from, 0, 0});
    m = edges.size(), G[from].push_back(m - 2), G[to].push_back(m - 1);
  }
  bool BFS() {
    fill_n(vis, n + 1, false);
    queue<int> Q;
    Q.push(s), vis[s] = true, d[s] = 0;
    while (!Q.empty()) {
      int x = Q.front();
      Q.pop();
      for (size_t i = 0; i < G[x].size(); i++) {
        Edge &e = edges[G[x][i]];
        if (!vis[e.to] && e.cap > e.flow)
          vis[e.to] = true, d[e.to] = d[x] + 1, Q.push(e.to);
      }
    }
    return vis[t];
  }
  int DFS(int x, int a) {
    if (x == t || a == 0)
      return a;
    int flow = 0, f;
    for (int &i = cur[x]; i < G[x].size(); i++) {
      Edge &e = edges[G[x][i]];
      if (d[x] + 1 == d[e.to] && (f = DFS(e.to, min(a, e.cap - e.flow))) > 0) {
        e.flow += f, edges[G[x][i] ^ 1].flow -= f, flow += f, a -= f;
        if (a == 0)
          break;
      }
    }
    return flow;
  }
  int Maxflow(int s, int t) {
    this->s = s, this->t = t;
    int flow = 0;
    while (BFS())
      fill_n(cur, n + 1, 0), flow += DFS(s, INF);
    return flow;
  }
};
Dinic g;
int main() {
  int T; scanf("%d", &T);
  for (int kase = 1, n, m; kase <= T; kase++) {
    scanf("%d%d", &n, &m);
    g.init(n + m + 1); // s=0, 物品为点1~m, 除Bob外的人为m+1~m+n-1，t=m+n
    for (int i = 0, k; i < n; i++) {
      scanf("%d", &k);
      vector<int> cnt(m + 1, 0);
      for (int j = 0, kind; j < k; j++) scanf("%d", &kind), cnt[kind]++;
      if (i == 0) { // Bob
        for (int j = 1; j <= m; j++)
          if (cnt[j] >= 1) g.AddEdge(0, j, cnt[j]); // s连边到物品
      } else {                       // 其他人
        for (int j = 1; j <= m; j++) {
          if (cnt[j] >= 2) g.AddEdge(m + i, j, cnt[j] - 1); // 此人可以给出cnt[j]-1个物品j
          else if (cnt[j] == 0) g.AddEdge(j, m + i, 1); // 此人可以接受1个物品j
        }
      }
    }
    for (int i = 1; i <= m; i++) g.AddEdge(i, m + n, 1);
    printf("Case #%d: %d\n", kase, g.Maxflow(0, m+n));
  }
  return 0;
}
// 26481868 10779 Collectors Problem  Accepted  C++ 0.000 2021-06-13 11:55:19
```

### 例题30  UVa11248 Frequency Hopping：使用ISAP算法，加优化

```cpp
// 例题30  UVa11248 Frequency Hopping：使用ISAP算法，加优化
// 刘汝佳
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>
using namespace std;

const int NN = 100 + 10, INF = 1e9;
struct Edge {
  int from, to, cap, flow;
};
bool operator<(const Edge &a, const Edge &b) {
  return a.from < b.from || (a.from == b.from && a.to < b.to);
}
struct ISAP {
  int n, m, s, t;
  vector<Edge> edges;
  vector<int> G[NN]; // 邻接表，G[i][j]表示结点i的第j条边在e数组中的序号
  bool vis[NN]; // BFS使用
  int d[NN];    // 从起点到i的距离
  int cur[NN];  // 当前弧指针
  int p[NN];    // 可增广路上的上一条弧
  int num[NN];  // 距离标号计数

  void AddEdge(int from, int to, int cap) {
    edges.push_back((Edge){from, to, cap, 0});
    edges.push_back((Edge){to, from, 0, 0});
    m = edges.size();
    G[from].push_back(m - 2), G[to].push_back(m - 1);
  }

  bool BFS() {
    fill_n(vis, n + 1, false);
    queue<int> Q;
    Q.push(t), vis[t] = 1, d[t] = 0;
    while (!Q.empty()) {
      int x = Q.front();
      Q.pop();
      for (size_t i = 0; i < G[x].size(); i++) {
        Edge &e = edges[G[x][i] ^ 1];
        if (!vis[e.from] && e.cap > e.flow)
          vis[e.from] = 1, d[e.from] = d[x] + 1, Q.push(e.from);
      }
    }
    return vis[s];
  }

  void ClearAll(int n) {
    this->n = n;
    for (int i = 0; i < n; i++)
      G[i].clear();
    edges.clear();
  }

  void ClearFlow() {
    for (size_t i = 0; i < edges.size(); i++)
      edges[i].flow = 0;
  }

  int Augment() {
    int x = t, a = INF;
    while (x != s) {
      Edge &e = edges[p[x]];
      a = min(a, e.cap - e.flow), x = edges[p[x]].from;
    }
    x = t;
    while (x != s)
      edges[p[x]].flow += a, edges[p[x] ^ 1].flow -= a, x = edges[p[x]].from;
    return a;
  }

  int Maxflow(int s, int t, int need) {
    this->s = s, this->t = t;
    int flow = 0;
    BFS();
    fill_n(num, n + 1, 0);
    for (int i = 0; i < n; i++)
      num[d[i]]++;
    int x = s;
    fill_n(cur, n + 1, 0);
    while (d[s] < n) {
      if (x == t) {
        flow += Augment();
        if (flow >= need)
          return flow;
        x = s;
      }
      int ok = 0;
      for (size_t i = cur[x]; i < G[x].size(); i++) {
        Edge &e = edges[G[x][i]];
        if (e.cap > e.flow && d[x] == d[e.to] + 1) { // Advance
          ok = 1, p[e.to] = G[x][i], cur[x] = i;     // 注意
          x = e.to;
          break;
        }
      }
      if (!ok) {       // Retreat
        int m = n - 1; // 初值注意
        for (size_t i = 0; i < G[x].size(); i++) {
          Edge &e = edges[G[x][i]];
          if (e.cap > e.flow)
            m = min(m, d[e.to]);
        }
        if (--num[d[x]] == 0)
          break;
        num[d[x] = m + 1]++, cur[x] = 0; // 注意
        if (x != s)
          x = edges[p[x]].from;
      }
    }
    return flow;
  }

  vector<int> Mincut() { // call this after maxflow
    BFS();
    vector<int> ans;
    for (size_t i = 0; i < edges.size(); i++) {
      Edge &e = edges[i];
      if (!vis[e.from] && vis[e.to] && e.cap > 0)
        ans.push_back(i);
    }
    return ans;
  }

  void Reduce() {
    for (size_t i = 0; i < edges.size(); i++)
      edges[i].cap -= edges[i].flow;
  }

  void print() {
    printf("Graph:\n");
    for (size_t i = 0; i < edges.size(); i++) {
      const Edge &e = edges[i];
      printf("%d->%d, %d, %d\n", e.from, e.to, e.cap, e.flow);
    }
  }
};

ISAP g;
void solve(int n, int c) {
  int flow = g.Maxflow(0, n - 1, INF);
  if (flow >= c) {
    puts("possible");
    return;
  }
  vector<int> cut = g.Mincut();
  g.Reduce(); // 保留以前的流量
  vector<Edge> ans;
  for (size_t i = 0; i < cut.size(); i++) {
    Edge &e = g.edges[cut[i]];
    e.cap = c, g.ClearFlow();
    if (flow + g.Maxflow(0, n - 1, c) >= c) ans.push_back(e);
    e.cap = 0;
  }
  if (ans.empty()) {
    puts("not possible");
    return;
  }
  sort(ans.begin(), ans.end());
  printf("possible option:(%d,%d)", ans[0].from + 1, ans[0].to + 1);
  for (size_t i = 1; i < ans.size(); i++)
    printf(",(%d,%d)", ans[i].from + 1, ans[i].to + 1);
  puts("");
}

int main() {
  for (int n, e, c, kase = 1; scanf("%d%d%d", &n, &e, &c) == 3 && n; kase++) {
    g.ClearAll(n);
    for (int i = 0, b1, b2, fp; i < e; i++)
      scanf("%d%d%d", &b1, &b2, &fp), g.AddEdge(b1 - 1, b2 - 1, fp);
    printf("Case %d: ", kase);
    solve(n, c);
  }
  return 0;
}
// Accepted 360ms 4250 C++ 5.3.0 2020-12-1418:43:39 25846863
```

### 例题34  生产销售规划（Acme Corporation, UVa 11613）

```cpp
// 例题34  生产销售规划（Acme Corporation, UVa 11613）
// 陈锋
#include <algorithm>
#include <cassert>
#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>
using namespace std;
const int maxn = 202 + 10, INF = 1e9;
typedef long long LL;
struct Edge {
  int from, to, cap, flow, cost;
};

struct MCMF {
  int n, m, s, t;
  vector<Edge> edges;
  vector<int> G[maxn];
  int inq[maxn];  // 是否在队列中
  int d[maxn];    // Bellman-Ford
  int p[maxn];    // 上一条弧
  int a[maxn];    // 可改进量

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, int cap, int cost) {
    edges.push_back((Edge){from, to, cap, 0, cost});
    edges.push_back((Edge){to, from, 0, 0, -cost});
    m = edges.size();
    G[from].push_back(m - 2);
    G[to].push_back(m - 1);
  }

  bool BellmanFord(int s, int t, LL& ans) {
    for (int i = 0; i < n; i++) d[i] = INF;
    memset(inq, 0, sizeof(inq));
    d[s] = 0, inq[s] = 1, p[s] = 0, a[s] = INF;

    queue<int> Q;
    Q.push(s);
    while (!Q.empty()) {
      int u = Q.front();
      Q.pop();
      inq[u] = 0;
      for (int i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if (e.cap > e.flow && d[e.to] > d[u] + e.cost) {
          d[e.to] = d[u] + e.cost, p[e.to] = G[u][i];
          a[e.to] = min(a[u], e.cap - e.flow);
          if (!inq[e.to]) Q.push(e.to), inq[e.to] = 1;
        }
      }
    }
    if (d[t] > 0) return false;
    ans += (LL)d[t] * (LL)a[t];
    int u = t;
    while (u != s) {
      edges[p[u]].flow += a[t], edges[p[u] ^ 1].flow -= a[t];
      u = edges[p[u]].from;
    }
    return true;
  }

  // 需要保证初始网络中没有负权圈
  LL Mincost(int s, int t) {
    LL cost = 0;
    while (BellmanFord(s, t, cost))
      ;
    return cost;
  }
};

MCMF g;

int main() {
  int T;
  scanf("%d", &T);
  for (int kase = 1, M, store_cost; kase <= T; kase++) {
    scanf("%d%d", &M, &store_cost);
    g.init(2 * M + 2);
    int source = 0, sink = 2 * M + 1;
    for (int i = 1, make_cost, make_limit, price, sell_limit, max_store; i <= M; i++) {
      scanf("%d%d%d%d%d", &make_cost, &make_limit, &price, &sell_limit, &max_store);
      g.AddEdge(source, i, make_limit, make_cost);
      g.AddEdge(M + i, sink, sell_limit, -price);  // 收益是负费用
      for (int j = 0; j <= max_store; j++)
        if (i + j <= M) g.AddEdge(i, M + i + j, INF, store_cost * j);  // 存j个月以后卖
    }
    printf("Case %d: %lld\n", kase, -g.Mincost(source, sink));
  }
  return 0;
}
// Accepted 120ms 2480 C++5.3.0 2020-12-1418:56:06 25846919
```
