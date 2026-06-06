# 5.3 最短路问题

## 例题18  低价空中旅行（Low Cost Air Travel, World Finals 2006, LA3561/UVa1048

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

## 例题19  动物园大逃亡（Animal Run, 北京 2006, UVa1376 LA 3661）

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

## 例题13  战争和物流（Warfare and Logistics, LA4080/UVa1416）

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

## 例题17  蒸汽式压路机（Steam Roller, LA 4128/UVa1078）

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

## 例题14  过路费（加强版）（The Toll! Revisited, UVa 10537）

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

## 例题12  林中漫步（A Walk Through the Forest, UVa 10917）

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

## 例题15  在环中（Going in Cycle!!, UVa 11090）

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

## 例题11  机场快线（Airport Express, UVa 11374）

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

## 例题16  Halum操作（Halum, UVa 11478）

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
