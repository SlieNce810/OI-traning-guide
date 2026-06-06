# 1.4 动态规划专题

## 例题26  约瑟夫问题的变形（And Then There Was One, Japan 2007, Codeforces Gym101415A

```cpp
// 例题26  约瑟夫问题的变形（And Then There Was One, Japan 2007, Codeforces Gym101415A
// Rujia Liu
#include<cstdio>
const int maxn = 10000 + 2;
int f[maxn];

int main() {
  freopen("A.in", "r", stdin);
  for( int n, k, m; scanf("%d%d%d", &n, &k, &m) == 3 && n;) {
    f[1] = 0;
    for(int i = 2; i <= n; i++) f[i] = (f[i-1] + k) % i;
    int ans = (m - k + 1 + f[n]) % n;
    if (ans <= 0) ans += n;
    printf("%d\n", ans);
  }
  return 0;
}
// 102052339 Dec/22/2020 23:00UTC+8 chenwz A - And Then There Was One GNU C++11 Accepted 15 ms 0 KB
```

## 例题27  王子和公主（Prince and Princess, UVa 10635）

```cpp
// 例题27  王子和公主（Prince and Princess, UVa 10635）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 256, MAXP = MAXN * MAXN;
using namespace std;
typedef long long LL;
int B[MAXP], IDX[MAXP], D[MAXP];

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T, n, a, p, q;
  cin >> T;
  for (int t = 1; cin >> n >> p >> q && n; t++) {
    ++p, ++q;
    fill_n(IDX, n * n + 2, 0);
    for (int i = 1; i <= p; i++) cin >> a, IDX[a] = i;
    int bi = 0, b;
    for (int i = 0; i < q; i++) {
      cin >> b, b = IDX[b];
      if (b) B[bi++] = b;
    }
    fill_n(D, bi + 1, 1); // 计算B的LIS
    int ans = -1;
    for (int i = 0; i < bi; i++) {
      for (int j = i + 1; j < bi; j++)
        if (B[j] > B[i]) D[j] = max(D[j], 1 + D[i]);
      ans = max(ans, D[i]);
    }
    printf("Case %d: %d\n", t, ans);
  }
  return 0;
}
// Accepted 2250ms 826 C++5.3.0 2020-12-08 20:27:25 25825777
```

## 例题30  放置街灯（Placing Lampposts, UVa 10859）

```cpp
// 例题30  放置街灯（Placing Lampposts, UVa 10859）
// 陈锋
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;
const int NN = 1000 + 8, BASE = 2000;
vector<int> G[NN];  // 森林是稀疏的，这样保存省空间，枚举相邻结点也更快
int Vis[NN][2], D[NN][2], N, M;

int dp(int i, int j, int f) {  // DFS的同时进行动态规划,f是父结点, 不存入状态里
  if (Vis[i][j]) return D[i][j];
  Vis[i][j] = 1;
  int& ans = D[i][j];

  // 放灯总是合法决策
  ans = BASE;  // 灯的数量加1，x加BASE
  for (int k = 0; k < G[i].size(); k++)
    if (G[i][k] != f)  // 这个判断非常重要！除了父结点之外的相邻结点才是子结点
      ans += dp(G[i][k], 1, i);  // 注意，这些结点的父结点是i
  if (!j && f >= 0) ans++;  // 如果i不是根，且父结点没放灯，则x加1

  if (j || f < 0) {  // i是根或者其父结点已放灯，i才可以不放灯
    int sum = 0;
    for (int k = 0; k < G[i].size(); k++)
      if (G[i][k] != f) sum += dp(G[i][k], 0, i);
    if (f >= 0) sum++;  // 如果i不是根，则x加1
    ans = min(ans, sum);
  }
  return ans;
}

int main() {
  int T, a, b;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%d", &N, &M);
    for (int i = 0; i < N; i++) G[i].clear();
    for (int i = 0, a, b; i < M; i++)
      scanf("%d%d", &a, &b), G[a].push_back(b), G[b].push_back(a);
    memset(Vis, 0, sizeof(Vis));
    int ans = 0;
    for (int i = 0; i < N; i++)
      if (!Vis[i][0]) ans += dp(i, 0, -1);  // 新的一棵树的树根
    printf("%d %d %d\n", ans/BASE, M - ans%BASE, ans%BASE);  //从x计算3个整数
  }
  return 0;
}
// Accepted 1365 C++5.3.0 2020-12-08 21:06:32 25825938
```

## 例题28  Sum游戏（Game of Sum, UVa 10891）

```cpp
// 例题28  Sum游戏（Game of Sum, UVa 10891）
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<algorithm>
using namespace std;

int S[110], A[110], d[110][110], vis[110][110], f[110][110], g[110][110], n;

// f[i+1][j] = min{d(i+1,j),d(i+2,j)...,d(j,j)}
// g[i][j-1] = min{d(i,j-1),d(i,j-2)...,d(i,i)}
int main() {
  while(scanf("%d", &n) && n) {
    S[0] = 0;
    for(int i = 1; i <= n; i++) { scanf("%d", &A[i]); S[i]=S[i-1]+A[i]; }
    for(int i = 1; i <= n; i++) f[i][i] = g[i][i] = d[i][i] = A[i]; // 边界
    for(int L = 1; L < n; L++) // 按照L=j-i递增的顺序计算
      for(int i = 1; i+L <= n; i++) {
        int j = i+L;
        int m = 0; // m = min{f(i+1,j), g(i,j-1), 0}
        m = min(m, f[i+1][j]);
        m = min(m, g[i][j-1]);
        d[i][j] = S[j]-S[i-1] - m;
        f[i][j] = min(d[i][j], f[i+1][j]); // 递推f和g
        g[i][j] = min(d[i][j], g[i][j-1]);
      }
    printf("%d\n", 2*d[1][n]-S[n]);
  }
  return 0;
}
// 25875896	10891	Game of Sum	Accepted	C++	0.000	2020-12-22 15:00:28
```

## 例题32  分享巧克力（Sharing Chocolate, World Finals 2010, UVa1099）

```cpp
// 例题32  分享巧克力（Sharing Chocolate, World Finals 2010, UVa1099）
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<algorithm>
using namespace std;

const int maxn = 16;
const int maxw = 100 + 10;
int n, A[maxn], sum[1<<maxn], f[1<<maxn][maxw], vis[1<<maxn][maxw];

int bitcount(int x) { return x == 0 ? 0 : bitcount(x/2) + (x&1); }

int dp(int S, int x) {
  if(vis[S][x]) return f[S][x];
  vis[S][x] = 1;
  int& ans = f[S][x];
  if(bitcount(S) == 1) return ans = 1;
  int y = sum[S] / x;
  for(int S0 = (S-1)&S; S0; S0 = (S0-1)&S) {
    int S1 = S-S0;
    if(sum[S0]%x==0&&dp(S0,min(x,sum[S0]/x))&&dp(S1,min(x,sum[S1]/x))) return ans = 1;
    if(sum[S0]%y==0&&dp(S0,min(y,sum[S0]/y))&&dp(S1,min(y,sum[S1]/y))) return ans = 1;
  }
  return ans = 0;
}

int main() {
  int kase = 0, n, x, y;
  while(scanf("%d", &n) == 1 && n) {
    scanf("%d%d", &x, &y);
    for(int i = 0; i < n; i++) scanf("%d", &A[i]);

    // 每个子集中的元素之和
    memset(sum, 0, sizeof(sum));
    for(int S = 0; S < (1<<n); S++)
      for(int i = 0; i < n; i++) if(S & (1<<i)) sum[S] += A[i];

    memset(vis, 0, sizeof(vis));
    int ALL = (1<<n) - 1;
    int ans;
    if(sum[ALL] != x*y || sum[ALL] % x != 0) ans = 0;
    else ans = dp(ALL, min(x,y));
    printf("Case %d: %s\n", ++kase, ans ? "Yes" : "No");
  }
  return 0;
}
// 25875902	1099	Sharing Chocolate	Accepted	C++	0.410	2020-12-22 15:02:15
```

## 例题31  捡垃圾的机器人（Robotruck, SWERC 2007, UVa1169）

```cpp
// 例题31  捡垃圾的机器人（Robotruck, SWERC 2007, UVa1169）
// Rujia Liu
#include<cstdio>
#include<algorithm>
using namespace std;

const int maxn = 100000 + 10;

int x[maxn], y[maxn];
int total_dist[maxn], total_weight[maxn], dist2origin[maxn];
int q[maxn], d[maxn];

int func(int i) {
  return d[i] - total_dist[i+1] + dist2origin[i+1];
}

main() {
  int T, c, n, w, front, rear;
  scanf("%d", &T);
  while(T--) {
    scanf("%d%d", &c, &n);
    total_dist[0] = total_weight[0] = x[0] = y[0] = 0;
    for(int i = 1; i <= n; i++) {
      scanf("%d%d%d", &x[i], &y[i], &w);
      dist2origin[i] = abs(x[i]) + abs(y[i]);
      total_dist[i] = total_dist[i-1] + abs(x[i]-x[i-1]) + abs(y[i]-y[i-1]);
      total_weight[i] = total_weight[i-1] + w;
    }
    front = rear = 1;
    for (int i = 1; i <= n; i++) {
      while (front <= rear && total_weight[i] - total_weight[q[front]] > c) front++;
      d[i] = func(q[front]) + total_dist[i] + dist2origin[i];
      while (front <= rear && func(i) <= func(q[rear])) rear--;
      q[++rear] = i;
    }
    printf("%d\n", d[n]);
    if(T > 0) printf("\n");
  }
  return 0;
}
// 25875898	1169	Robotruck	Accepted	C++	0.030	2020-12-22 15:01:28
```

## 例题29  黑客的攻击（Hacker’s Crackdown, UVa 11825）

```cpp
// 例题29  黑客的攻击（Hacker’s Crackdown, UVa 11825）
// 陈锋
#include <algorithm>
#include <cstdio>
using namespace std;

const int NN = 16;
int P[NN], cover[1 << NN], f[1 << NN];
int main() {
  for (int kase = 1, n; scanf("%d", &n) == 1 && n; kase++) {
    for (int i = 0, m, x; i < n; i++) {
      scanf("%d", &m), P[i] = 1 << i;
      while (m--) scanf("%d", &x), P[i] |= (1 << x);
    }
    for (int S = 0; S < (1 << n); S++) {
      cover[S] = 0;
      for (int i = 0; i < n; i++)
        if (S & (1 << i)) cover[S] |= P[i];
    }
    f[0] = 0;
    int ALL = (1 << n) - 1;
    for (int S = 1; S < (1 << n); S++) {
      f[S] = 0;
      for (int S0 = S; S0; S0 = (S0 - 1) & S)
        if (cover[S0] == ALL) f[S] = max(f[S], f[S ^ S0] + 1);
    }
    printf("Case %d: %d\n", kase, f[ALL]);
  }
  return 0;
}
// Accepted 720ms 795 C++5.3.02020-12-08 21:14:04 25825962
```
