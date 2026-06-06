# 5.5 二分图匹配

## 例题25  固定分区内存管理（Fixed Partition Memory Management, World Finals 2001, LA 2238/UVa1006

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

## 例题29  出租车（Taxi Cab Scheme, NWERC 2004, LA 3126/POJ2060

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

## 例题28  保守的老师（Guardian of Decency, NWERC 2005, LA 3415/POJ2771

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

## 例题26  女士的选择（Ladies’ Choice, SWERC 2007, LA3989/UVa1175

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

## 例题23  蚂蚁（Ants, NEERC 2008, LA 4043/POJ3565

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

## 例题24  少林决胜（Golden Tiger Claw, UVa 11383）

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

## 例题27  我是SAM（SAM I AM, UVa 11419）

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
