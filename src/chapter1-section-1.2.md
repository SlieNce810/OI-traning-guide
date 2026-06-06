# 1.2 问题求解常见策略

## 例题13  派（Pie, NWERC 2006, Codeforces Gym100722C）

```cpp
// 例题13  派（Pie, NWERC 2006, Codeforces Gym100722C）
// 陈锋
#include <cmath>
#include <cstdio>
#include <algorithm>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
const int NN = 10000 + 4;
double S[NN];
const double PI = acos(-1), EPS = 1e-6;

int main() {
  int T; scanf("%d", &T);
  for (int t = 0, N, F; t < T; t++) {
    scanf("%d%d", &N, &F), ++F;
    double L = 0, R = 0, r;
    _for(i, 0, N) scanf("%lf", &r), R = max(R, S[i] = r * r * PI);
    while (L + EPS < R) { // L is always an min answer
      double M = (L + R) / 2; int f = 0;
      _for(i, 0, N) {
        f += (int)floor(S[i] / M);
        if (f >= F) break;
      }
      if (f >= F) L = M; else R = M;
    }
    printf("%.4lf\n", L);
  }
}
// 102050321	Dec/22/2020 22:37UTC+8	chenwz	C - Pie	GNU C++11	Accepted	62 ms	100 KB
```

## 例题12  组装电脑（Assemble, NWERC 2007,  LA3971/POJ3497）

```cpp
// 例题12  组装电脑（Assemble, NWERC 2007,  LA3971/POJ3497）
// Rujia Liu
#include<cstdio>
#include<string>
#include<vector>
#include<map>
using namespace std;

int cnt; // 组件的类型数
map<string,int> id;
int ID(string s) {
  if(!id.count(s)) id[s] = cnt++;
  return id[s];
}

const int maxn = 1000 + 5;

struct Component {
  int price;
  int quality;
};
int n, b; // 组件的数目，预算
vector<Component> comp[maxn];

// 品质因子不小于q的组件能否组装成一个不超过b元的电脑
bool ok(int q) {
  int sum = 0;
  for(int i = 0; i < cnt; i++) {
    int cheapest = b+1, m = comp[i].size();
    for(int j = 0; j < m; j++)
      if(comp[i][j].quality >= q) cheapest = min(cheapest, comp[i][j].price);
    if(cheapest == b+1) return false;
    sum += cheapest;
    if(sum > b) return false;
  }
  return true;
}

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    scanf("%d%d", &n, &b);

    cnt = 0;
    for(int i = 0; i < n; i++) comp[i].clear();
    id.clear();

    int maxq = 0;
    for(int i = 0; i < n; i++) {
      char type[30], name[30];
      int p, q;
      scanf("%s%s%d%d", type, name, &p, &q);
      maxq = max(maxq, q);
      comp[ID(type)].push_back((Component){p, q});
    }

    int L = 0, R = maxq;
    while(L < R) {
      int M = L + (R-L+1)/2;
      if(ok(M)) L = M; else R = M-1;
    }
    printf("%d\n", L);
  }
  return 0;
}
// Accepted 297ms 748kB 1267 G++2020-12-2222:35:1622226024
```

## 例题11  新汉诺塔问题（A Different Task, UVa 10795）

```cpp
// 例题11  新汉诺塔问题（A Different Task, UVa 10795）
// Rujia Liu
#include<cstdio>

long long f(int* P, int i, int final) {
  if(i == 0) return 0;
  if(P[i] == final) return f(P, i-1, final);
  return f(P, i-1, 6-P[i]-final) + (1LL << (i-1));
}

const int maxn = 60 + 10;
int n, start[maxn], finish[maxn];

int main() {
  int kase = 0;
  while(scanf("%d", &n) == 1 && n) {
    for(int i = 1; i <= n; i++) scanf("%d", &start[i]);
    for(int i = 1; i <= n; i++) scanf("%d", &finish[i]);
    int k = n;
    while(k >= 1 && start[k] == finish[k]) k--;

    long long ans = 0;
    if(k >= 1) {
      int other = 6-start[k]-finish[k];
      ans = f(start, k-1, other) + f(finish, k-1, other) + 1;
    }
    printf("Case %d: %lld\n", ++kase, ans);
  }
  return 0;
}
// 25875783	10795	A Different Task	Accepted	C++	0.000	2020-12-22 14:31:51
```

## 例题9  中国麻将（Chinese Mahjong, UVa 11210）

```cpp
// 例题9  中国麻将（Chinese Mahjong, UVa 11210）
// Rujia Liu

#include<stdio.h>
#include<string.h>

const char* mahjong[] = {
"1T","2T","3T","4T","5T","6T","7T","8T","9T",
"1S","2S","3S","4S","5S","6S","7S","8S","9S",
"1W","2W","3W","4W","5W","6W","7W","8W","9W",
"DONG","NAN","XI","BEI",
"ZHONG","FA","BAI"
};

int convert(char *s){ // 只在预处理时调用，因此速度无关紧要
  for(int i = 0; i < 34; i++)
    if(strcmp(mahjong[i], s) == 0) return i;
  return -1;
}

int c[34];
bool search(int dep){ // 回溯法递归过程
  int i;
  for(i = 0; i < 34; i++) if (c[i] >= 3){ // 刻子
    if(dep == 3) return true; 
    c[i] -= 3; 
    if(search(dep+1)) return true; 
    c[i] += 3;
  }
  for(i = 0; i <= 24; i++) if (i % 9 <= 6 && c[i] >= 1 && c[i+1] >= 1 && c[i+2] >= 1){ 											//顺子
    if(dep == 3) return true; 
    c[i]--; c[i+1]--; c[i+2]--;
    if(search(dep+1)) return true; 
    c[i]++; c[i+1]++; c[i+2]++;
  }
  return false;
}

bool check(){
  int i;
  for(i = 0; i < 34; i++)
    if(c[i] >= 2){ // 将牌
      c[i] -= 2;
      if(search(0)) return true;
      c[i] += 2;
  }
  return false;
}

int main(){
  int caseno = 0, i, j;
  bool ok;
  char s[100];
  int mj[15];

  while(scanf("%s", &s) == 1){
    if(s[0] == '0') break;
    printf("Case %d:", ++caseno);
    mj[0] = convert(s);
    for(i = 1; i < 13; i++){
      scanf("%s", &s);
      mj[i] = convert(s);
    }
    ok = false;
    for(i = 0; i < 34; i++){
      memset(c, 0, sizeof(c));
      for(j = 0; j < 13; j++) c[mj[j]]++;
      if(c[i] >= 4) continue; // 每种牌最多只有4张
      c[i]++;  // 假设拥有这张牌
      if(check()){ // 如果“和”了
        ok = true; // 说明听这张牌
        printf(" %s", mahjong[i]);
      }
      c[i]--;
    }
    if(!ok) printf(" Not ready");
    printf("\n");
  }
  return 0;
}
// 5875774	11210	Chinese Mahjong	Accepted	C++	0.000	2020-12-22 14:30:15
```

## 例题10  正整数序列（Help is needed for Dexter, UVa 11384）

```cpp
// 例题10  正整数序列（Help is needed for Dexter, UVa 11384）
// Rujia Liu
#include<cstdio>
int f(int n) {
  return n == 1 ? 1 : f(n/2) + 1;
}

int main() {
  int n;
  while(scanf("%d", &n) == 1)
    printf("%d\n", f(n));
  return 0;
}
// 25875779	11384	Help is needed for Dexter	Accepted	C++	0.020	2020-12-22 14:31:10
```

## 例题7  偶数矩阵（Even Parity, UVa 11464）

```cpp
// 例题7  偶数矩阵（Even Parity, UVa 11464）
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<algorithm>
using namespace std;

const int maxn = 20;
const int INF = 1000000000;
int n, A[maxn][maxn], B[maxn][maxn];

int check(int s) {
  memset(B, 0, sizeof(B));
  for(int c = 0; c < n; c++) {
    if(s & (1<<c)) B[0][c] = 1;
    else if(A[0][c] == 1) return INF; // 1不能变成0
  }
  for(int r = 1; r < n; r++)
    for(int c = 0; c < n; c++) {
      int sum = 0; // 元素B[r-1][c]的上、左、右3个元素之和
      if(r > 1) sum += B[r-2][c];
      if(c > 0) sum += B[r-1][c-1];
      if(c < n-1) sum += B[r-1][c+1];
      B[r][c] = sum % 2;
      if(A[r][c] == 1 && B[r][c] == 0) return INF; // 1不能变成0
    }
  int cnt = 0;
  for(int r = 0; r < n; r++)
    for(int c = 0; c < n; c++) if(A[r][c] != B[r][c]) cnt++;
  return cnt;
}

int main() {
  int T;
  scanf("%d", &T);
  for(int kase = 1; kase <= T; kase++) {
    scanf("%d", &n);
    for(int r = 0; r < n; r++)
      for(int c = 0; c < n; c++) scanf("%d", &A[r][c]);

    int ans = INF;
    for(int s = 0; s < (1<<n); s++)
      ans = min(ans, check(s));
    if(ans == INF) ans = -1;
    printf("Case %d: %d\n", kase, ans);
  }
  return 0;
}
// 25875764	11464	Even Parity	Accepted	C++	0.060	2020-12-22 14:28:27
```

## 例题14  填充正方形（Fill the Square, UVa11520）

```cpp
// 例题14  填充正方形（Fill the Square, UVa11520）
// Rujia Liu
#include<cstdio>
#include<cstring>
const int maxn = 10 + 5;
char grid[maxn][maxn];
int n;
int main() {
  int T;
  scanf("%d", &T);
  for(int kase = 1; kase <= T; kase++) {
    scanf("%d", &n);
    for(int i = 0; i < n; i++) scanf("%s", grid[i]);
    for(int i = 0; i < n; i++)
      for(int j = 0; j < n; j++) if(grid[i][j] == '.') {//没填过的字母才需要填
        for(char ch = 'A'; ch <= 'Z'; ch++) { 		//按照字典序依次尝试
          bool ok = true;
          if(i>0 && grid[i-1][j] == ch) ok = false; 	//和上面的字母冲突
          if(i<n-1 && grid[i+1][j] == ch) ok = false;
          if(j>0 && grid[i][j-1] == ch) ok = false;
          if(j<n-1 && grid[i][j+1] == ch) ok = false;
          if(ok) { grid[i][j] = ch; break; } //没有冲突，填进网格，停止继续尝试
        }
      }
    printf("Case %d:\n", kase);
    for(int i = 0; i < n; i++) printf("%s\n", grid[i]);
  }
  return 0;
}
// 25875795	11520	Fill the Square	Accepted	C++	0.000	2020-12-22 14:35:49
```

## 例题15  网络（Network, Seoul 2007,UVa1267）

```cpp
// 例题15  网络（Network, Seoul 2007,UVa1267）
// Rujia Liu
#include <bits/stdc++.h>
using namespace std;
const int NN = 1000 + 4;
vector<int> G[NN], nodes[NN];
int N, S, K, fa[NN];
bool covered[NN];
// 无根树转有根树，计算fa数组，根据深度把叶子结点插入nodes表里
void dfs(int u, int f, int d) {
  fa[u] = f;
  if (G[u].size() == 1 && d > K)
    nodes[d].push_back(u);
  for (int v : G[u])
    if (v != f)
      dfs(v, u, d + 1);
}
void dfs2(int u, int f, int d) {
  covered[u] = true;
  for (int v : G[u])
    if (v != f && d < K) // 只覆盖到新服务器距离不超过k的结点
      dfs2(v, u, d + 1); 
}
int solve() {
  int ans = 0;
  fill_n(covered, N+1, 0);
  for (int d = N - 1; d > K; d--)
    for(int u : nodes[d]){
      if (covered[u]) continue; // 不考虑已覆盖的结点
      int v = u;
      for (int j = 0; j < K; j++) v = fa[v];    // v是u的k级祖先
      dfs2(v, -1, 0), ans++; // 在结点v放服务器
    }
  return ans;
}
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T; cin >> T;
  while (T--) {
    cin >> N >> S >> K;
    for (int i = 1; i <= N; i++)
      G[i].clear(), nodes[i].clear();
    for (int i = 0, a, b; i < N - 1; i++)
      cin>>a>>b, G[a].push_back(b), G[b].push_back(a);
    dfs(S, -1, 0);
    printf("%d\n", solve());
  }
  return 0;
}
// 25875799	1267	Network	Accepted	C++	0.000	2020-12-22 14:36:36
```

## 例题16  长城守卫（Beijing Guards, CERC 2004, UVa1335）

```cpp
// 例题16  长城守卫（Beijing Guards, CERC 2004, UVa1335）
// Rujia Liu
#include <bits/stdc++.h>
#define _all(i, a, b) for (int i = (a); i <= (int)(b); ++i)
using namespace std;
const int NN = 1e5 + 4;
// 测试p个礼物是否足够, Lᵢ,Rᵢ是第i个人拿到的“左≤(r₁)/右(>r₁)的礼物”总数
int N, A[NN], L[NN], R[NN];
bool test(int p) {
  int lc = A[1], rc = p - A[1];
  L[1] = lc, R[1] = 0;
  _all(i, 2, N) {
    if (i % 2)
      R[i] = min(rc - R[i - 1], A[i]), L[i] = A[i] - R[i]; // 尽量拿右边的礼物
    else
      L[i] = min(lc - L[i - 1], A[i]), R[i] = A[i] - L[i]; // 尽量拿左边的礼物
  }
  return L[N] == 0; // 跟1都不冲突
}
int solve() {
  if (N == 1) return A[1]; // 特判n=1
  A[N + 1] = A[1];
  int l = 0, r = 0;
  _all(i, 1, N) l = max(l, A[i] + A[i + 1]), r = max(r, A[i] * 3);
  while (N % 2 && l < r) {
    int m = l + (r - l) / 2;
    if (test(m)) r = m;
    else l = m + 1;
  }
  return l;
}
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  while (cin >> N && N) {
    _all(i, 1, N) cin >> A[i];
    cout << solve() << endl;
  }
  return 0;
}
// 25875801	1335	Beijing Guards	Accepted	C++	0.010	2020-12-22 14:37:13
```

## 例题8  彩色立方体（Colored Cubes, Tokyo 2005, UVa1352）

```cpp
// 例题8  彩色立方体（Colored Cubes, Tokyo 2005, UVa1352）
// Rujia Liu

// generated by la3401_make.cpp, then removed extra spaces
int dice24[24][6] = {
{2, 1, 5, 0, 4, 3},{2, 0, 1, 4, 5, 3},{2, 4, 0, 5, 1, 3},{2, 5, 4, 1, 0, 3},{4, 2, 5, 0, 3, 1},
{5, 2, 1, 4, 3, 0},{1, 2, 0, 5, 3, 4},{0, 2, 4, 1, 3, 5},{0, 1, 2, 3, 4, 5},{4, 0, 2, 3, 5, 1},
{5, 4, 2, 3, 1, 0},{1, 5, 2, 3, 0, 4},{5, 1, 3, 2, 4, 0},{1, 0, 3, 2, 5, 4},{0, 4, 3, 2, 1, 5},
{4, 5, 3, 2, 0, 1},{1, 3, 5, 0, 2, 4},{0, 3, 1, 4, 2, 5},{4, 3, 0, 5, 2, 1},{5, 3, 4, 1, 2, 0},
{3, 4, 5, 0, 1, 2},{3, 5, 1, 4, 0, 2},{3, 1, 0, 5, 4, 2},{3, 0, 4, 1, 5, 2},
};

#include<cstdio>
#include<cstring>
#include<string>
#include<vector>
#include<algorithm>
using namespace std;

const int maxn = 4;
int n, dice[maxn][6], ans;

vector<string> names;
int ID(const char* name) {
  string s(name);
  int n = names.size();
  for(int i = 0; i < n; i++)
    if(names[i] == s) return i;
  names.push_back(s);
  return n;
}

int r[maxn], color[maxn][6]; // 每个立方体的旋转方式和旋转后各个面的颜色

void check() {
  for(int i = 0; i < n; i++)
    for(int j = 0; j < 6; j++) color[i][dice24[r[i]][j]] = dice[i][j];

  int tot = 0; // 需要重新涂色的面数
  for(int j = 0; j < 6; j++) { // 考虑每个面
    int cnt[maxn*6]; // 每种颜色出现的次数
    memset(cnt, 0, sizeof(cnt));
    int maxface = 0;
    for(int i = 0; i < n; i++)
      maxface = max(maxface, ++cnt[color[i][j]]);
    tot += n - maxface;
  }
  ans = min(ans, tot);
}

void dfs(int d) {
  if(d == n) check();
  else for(int i = 0; i < 24; i++) {
    r[d] = i;
    dfs(d+1);
  }
}

int main() {
  while(scanf("%d", &n) == 1 && n) {
    names.clear();
    for(int i = 0; i < n; i++)
      for(int j = 0; j < 6; j++) {
        char name[30];
        scanf("%s", name);
        dice[i][j] = ID(name);
      }
    ans = n*6; // 上界：所有面都重涂色
    r[0] = 0; // 第一个立方体不旋转
    dfs(1);
    printf("%d\n", ans);
  }
  return 0;
}
// 25875769	1352	Colored Cubes	Accepted	C++	0.020	2020-12-22 14:29:29
```
