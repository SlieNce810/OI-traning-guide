# 5.1 基础题目选讲

## 例题4  猜序列（Guess, Seoul 2008, LA 4255/UVa1423）

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

## 例题2  独轮车（The Monocycle, UVa 10047）

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

## 例题3  项链（The Necklace, UVa 10054）

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

## 例题1  大火蔓延的迷宫（Fire!, UVa 11624）

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
