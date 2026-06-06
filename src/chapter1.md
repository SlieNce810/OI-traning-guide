# 第1章 算法设计基础

## 1.1 思维的体操

### 例题4  墓地雕塑（Graveyard, NEERC 2006, CodeForces Gym100287G）

```cpp
// 例题4  墓地雕塑（Graveyard, NEERC 2006, CodeForces Gym100287G）
// Rujia Liu
#include<cstdio>
#include<cmath>
using namespace std;

int main() {
  freopen("graveyard.in", "r", stdin);
  freopen("graveyard.out","w",stdout);

  for(int n, m; scanf("%d%d", &n, &m) == 2; ) {
    double ans = 0.0;
    for(int i = 1; i < n; i++) {
      double pos = (double)i / n * (n+m); //计算每个需要移动的雕塑的坐标
      ans += fabs(pos - floor(pos+0.5)) / (n+m); //累加移动距离
    }
    printf("%.4lf\n", ans*10000); //等比例扩大坐标
  }
  return 0;
}
// 102052134 Dec/22/2020 22:58UTC+8 chenwz G - Graveyard GNU C++11 Accepted 60 ms 0 KB
```

### 例题6  立方体成像（Image Is Everything, World Finals 2004, UVa1030）

```cpp
// 例题6  立方体成像（Image Is Everything, World Finals 2004, UVa1030）
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<cmath>
#include<algorithm>
using namespace std;

#define REP(i,n) for(int i = 0; i < (n); i++)

const int maxn = 10;
int n;
char pos[maxn][maxn][maxn];
char view[6][maxn][maxn];

char read_char() {
  char ch;
  for(;;) {
    ch = getchar();
    if((ch >= 'A' && ch <= 'Z') || ch == '.') return ch;
  }
}

void get(int k, int i, int j, int len, int &x, int &y, int &z)
{
  if (k == 0) { x = len; y = j; z = i; } 
  if (k == 1) { x = n - 1 - j; y = len; z = i; }
  if (k == 2) { x = n - 1 - len; y = n - 1 - j; z = i; }
  if (k == 3) { x = j; y = n - 1 - len; z = i; }
  if (k == 4) { x = n - 1 - i; y = j; z = len; }
  if (k == 5) { x = i; y = j; z = n - 1 - len; }
}

int main() {
  while(scanf("%d", &n) == 1 && n) {
    REP(i,n) REP(k,6) REP(j,n) view[k][i][j] = read_char();
    REP(i,n) REP(j,n) REP(k,n) pos[i][j][k] = '#';

    REP(k,6) REP(i,n) REP(j,n) if (view[k][i][j] == '.')
      REP(p,n) {
        int x, y, z;
        get(k, i, j, p, x, y, z);
        pos[x][y][z] = '.';
      }

    for(;;) {
      bool done = true;
      REP(k,6) REP(i,n) REP(j,n) if (view[k][i][j] != '.') {
        REP(p,n) {
          int x, y, z;
          get(k, i, j, p, x, y, z);
          if (pos[x][y][z] == '.') continue;
          if (pos[x][y][z] == '#') {
            pos[x][y][z] = view[k][i][j];
            break;
          }
          if (pos[x][y][z] == view[k][i][j]) break;
          pos[x][y][z] = '.';
          done = false;
        }
      }
      if(done) break;
    }

    int ans = 0;
    REP(i,n) REP(j,n) REP(k,n)
      if (pos[i][j][k] != '.') ans ++;

    printf("Maximum weight: %d gram(s)\n", ans);
  }
  return 0;
}
// 25875758 1030 Image Is Everything Accepted C++ 0.000 2020-12-22 14:26:41
```

### 例题5  蚂蚁（Piotr’s Ants, UVa 10881）

```cpp
// 例题5  蚂蚁（Piotr’s Ants, UVa 10881）
// Rujia Liu
#include <algorithm>
#include <cstdio>
using namespace std;
const int maxn = 10000 + 5;

struct Ant {
  int id;  // 输入顺序
  int p;   // 位置
  int d;   // 朝向。 -1: 左; 0:转身中; 1:右
  bool operator<(const Ant& a) const { return p < a.p; }
} before[maxn], after[maxn];
const char dirName[][10] = {"L", "Turning", "R"};
int order[maxn];  //输入的第i只蚂蚁是终态中的左数第order[i]只蚂蚁
int main() {
  int K; scanf("%d", &K);
  for (int kase = 1, L, T, n; kase <= K; kase++) {
    scanf("%d%d%d", &L, &T, &n);
    for (int i = 0, p, d; i < n; i++) {
      char c;
      scanf("%d %c", &p, &c);
      d = (c == 'L' ? -1 : 1);
      // 相撞后可以看做对穿而过,这里id是未知的
      before[i] = (Ant){i, p, d}, after[i] = (Ant){0, p + T * d, d};
    }
    printf("Case #%d:\n", kase);
    sort(before, before + n);  //计算order数组
    for (int i = 0; i < n; i++)
      order[before[i].id] = i;  // 第一次从左到右所有的蚂蚁的相对位置没有变化
    sort(after, after + n);          //计算终态
    for (int i = 0; i < n - 1; i++)  //修改碰撞中的蚂蚁的方向
      if (after[i].p == after[i + 1].p) after[i].d = after[i + 1].d = 0;
    for (int i = 0; i < n; i++) {
      int a = order[i];
      if (after[a].p < 0 || after[a].p > L)
        puts("Fell off");
      else
        printf("%d %s\n", after[a].p, dirName[after[a].d + 1]);
    }
    printf("\n");
  }
  return 0;
}
// 25879739 10881 Piotr's Ants Accepted C++ 0.010 2020-12-23 15:21:04
```

### 例题1  勇者斗恶龙（The Dragon of Loowater, UVa 11292）

```cpp
// 例题1  勇者斗恶龙（The Dragon of Loowater, UVa 11292）
// Waterloo Local Contest, 2007.9.29
// Rujia Liu
#include<cstdio>
#include<algorithm>       // 因为用到了sort
using namespace std;

const int maxn = 20000 + 5;
int A[maxn], B[maxn];
int main() {
  int n, m;
  while(scanf("%d%d", &n, &m) == 2 && n && m) {
    for(int i = 0; i < n; i++) scanf("%d", &A[i]);
    for(int i = 0; i < m; i++) scanf("%d", &B[i]);
    sort(A, A+n);
    sort(B, B+m);
    int cur = 0;         // 当前需要砍掉的头的编号
    int cost = 0;        // 当前总费用
    for(int i = 0; i < m; i++)
      if(B[i] >= A[cur]) {
        cost += B[i];           // 雇佣该骑士
        if(++cur == n) break;   // 如果头已经砍完，及时退出循环
      }
    if(cur < n) printf("Loowater is doomed!\n");
    else printf("%d\n", cost);
  }
  return 0;
}
// 25875724	11292	Dragon of Loowater	Accepted	C++	0.000	2020-12-22 14:20:28
```

### 例题3  分金币（Spreading the Wealth, UVa 11300）

```cpp
// 例题3  分金币（Spreading the Wealth, UVa 11300）
// Rujia Liu
#include<cstdio>
#include<algorithm>
using namespace std;

const int maxn = 1000000 + 10;
long long A[maxn], C[maxn], tot, M;
int main() {
  int n;
  while(scanf("%d", &n) == 1) { // 输入数据大，scanf比cin快 
    tot = 0;
    for(int i = 1; i <= n; i++) { scanf("%lld", &A[i]); tot += A[i]; } // 用%lld输入long long
    M = tot / n;
    C[0] = 0; 
    for(int i = 1; i < n; i++) C[i] = C[i-1] + A[i] - M; // 递推C数组
    sort(C, C+n);
    long long x1 = C[n/2], ans = 0; // 计算x1
    for(int i = 0; i < n; i++) ans += abs(x1 - C[i]); 
    // 把x1代入，计算转手的总金币数
    printf("%lld\n", ans);
  }
  return 0;
}
// 25875737	11300	Spreading the Wealth	Accepted	C++	0.120	2020-12-22 14:22:29
```

### 例题2  突击战（Commando War, UVa 11729）

```cpp
// 例题2  突击战（Commando War, UVa 11729）
// 陈锋
#include <algorithm>
#include <cstdio>
#include <iostream>
#include <vector>
using namespace std;

struct Job {
  int j, b;
  bool operator<(const Job& x) const {
    return j > x.j;  // 运算符重载。不要忘记const修饰符
  }
};

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  for (int n, b, j, kase = 1; cin >> n && n; kase++) {
    vector<Job> v(n);
    for (int i = 0; i < n; i++) cin >> v[i].b >> v[i].j;
    sort(v.begin(), v.end());  //使用Job类的 < 运算符排序
    int ans = 0;
    for (int i = 0, s = 0; i < n; i++) {
      s += v[i].b;                 //当前任务的开始执行时间
      ans = max(ans, s + v[i].j);  //任务执行完毕时的最晚时间
    }
    printf("Case %d: %d\n", kase, ans);
  }
  return 0;
}
// 25875729	11729	Commando War	Accepted	C++	0.000	2020-12-22 14:21:50
```

## 1.2 问题求解常见策略

### 例题13  派（Pie, NWERC 2006, Codeforces Gym100722C）

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

### 例题12  组装电脑（Assemble, NWERC 2007,  LA3971/POJ3497）

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

### 例题11  新汉诺塔问题（A Different Task, UVa 10795）

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

### 例题9  中国麻将（Chinese Mahjong, UVa 11210）

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

### 例题10  正整数序列（Help is needed for Dexter, UVa 11384）

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

### 例题7  偶数矩阵（Even Parity, UVa 11464）

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

### 例题14  填充正方形（Fill the Square, UVa11520）

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

### 例题15  网络（Network, Seoul 2007,UVa1267）

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

### 例题16  长城守卫（Beijing Guards, CERC 2004, UVa1335）

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

### 例题8  彩色立方体（Colored Cubes, Tokyo 2005, UVa1352）

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

## 1.3 高效算法设计举例

### 例题25  侏罗纪（Jurassic Remains, NEERC 2003, Codeforces Gym101388J）

```cpp
// 例题25  侏罗纪（Jurassic Remains, NEERC 2003, Codeforces Gym101388J）
// Rujia Liu
#include<cstdio>
#include<map>
using namespace std;

const int maxn = 24;
map<int,int> table;

int bitcount(int x) { return x == 0 ? 0 : bitcount(x/2) + (x&1); }

int main() {
  int n, A[maxn];
  char s[1000];

  freopen("jurassic.in", "r", stdin);
  freopen("jurassic.out","w",stdout);

  while(scanf("%d", &n) == 1 && n) {
    // 输入并计算每个字符串对应的位向量
    for(int i = 0; i < n; i++) {
      scanf("%s", s);
      A[i] = 0;
      for(int j = 0; s[j] != '\0'; j++) A[i] ^= (1<<(s[j]-'A'));
    }
    // 计算前n1个元素的所有子集的xor值
    // table[x]保存的是xor值为x的，bitcount尽量大的子集
    table.clear();
    int n1 = n/2, n2 = n-n1;
    for(int i = 0; i < (1<<n1); i++) {
      int x = 0;
      for(int j = 0; j < n1; j++) if(i & (1<<j)) x ^= A[j];
      if(!table.count(x) || bitcount(table[x]) < bitcount(i)) table[x] = i;
    }
    // 枚举后n2个元素的所有子集，并在table中查找
    int ans = 0;
    for(int i = 0; i < (1<<n2); i++) {
      int x = 0;
      for(int j = 0; j < n2; j++) if(i & (1<<j)) x ^= A[n1+j];
      if(table.count(x)&&bitcount(ans)<bitcount(table[x])+bitcount(i)) ans = (i<<n1)^table[x];
    }
    // 输出结果
    printf("%d\n", bitcount(ans));
    for(int i = 0; i < n; i++) if(ans & (1<<i)) printf("%d ", i+1);
    printf("\n");
  }
  return 0;
}
// 102052000	Dec/22/2020 22:56UTC+8	chenwz	J - Jurassic Remains	GNU C++11	Accepted	31 ms	300 KB
```

### 例题22  最大子矩阵（City Game, SEERC 2004, LA3029/POJ1964）

```cpp
// 例题22  最大子矩阵（City Game, SEERC 2004, LA3029/POJ1964）
// 刘汝佳
#include <algorithm>
#include <cstdio>
using namespace std;

const int maxn = 1000;
int mat[maxn][maxn], up[maxn][maxn], left[maxn][maxn], right[maxn][maxn];
int main() {
  int T;
  scanf("%d", &T);
  while (T--) {
    int m, n;
    scanf("%d%d", &m, &n);
    for (int i = 0; i < m; i++)
      for (int j = 0; j < n; j++) {
        int ch = getchar();
        while (ch != 'F' && ch != 'R') ch = getchar();
        mat[i][j] = ch == 'F' ? 0 : 1;
      }

    int ans = 0;
    for (int i = 0; i < m; i++) {  //从上到下逐行处理
      int lo = -1, ro = n;
      for (int j = 0; j < n; j++)  //从左到右扫描，维护up和left
        if (mat[i][j] == 1) {
          up[i][j] = left[i][j] = 0;
          lo = j;
        } else {
          up[i][j] = i == 0 ? 1 : up[i - 1][j] + 1;
          left[i][j] = i == 0 ? lo + 1 : max(left[i - 1][j], lo + 1);
        }
      for (int j = n - 1; j >= 0; j--)  //从右到左扫描，维护right并更新答案
        if (mat[i][j] == 1) {
          right[i][j] = n;
          ro = j;
        } else {
          right[i][j] = i == 0 ? ro - 1 : min(right[i - 1][j], ro - 1);
          ans = max(ans, up[i][j] * (right[i][j] - left[i][j] + 1));
        }
    }
    printf("%d\n", ans * 3);  //输出最大面积乘以3后的结果
  }
  return 0;
}
// Accepted 32ms 15988kB 1252 G++ 2020-12-08 21:55:10 22197363
```

### 例题21  子序列（Subsequence, SEERC 2006, POJ3061）

```cpp
// 例题21  子序列（Subsequence, SEERC 2006, POJ3061）
// 陈锋
#include <algorithm>
#include <cstdio>
using namespace std;

const int maxn = 1e5 + 8;
int A[maxn], B[maxn], T;
int main() {
  scanf("%d", &T);
  for (int n, S; scanf("%d%d", &n, &S) == 2 && T--;) {
    for (int i = 1; i <= n; i++) scanf("%d", &A[i]);
    B[0] = 0;
    for (int i = 1; i <= n; i++) B[i] = B[i - 1] + A[i];
    int ans = n + 1, i = 1;
    for (int j = 1; j <= n; j++) {
      if (B[i - 1] > B[j] - S) continue;  // (1)没有满足条件的i，换下一个j
      while (B[i] <= B[j] - S) i++;  // (2)求满足B[i-1]<=B[j]-S的最大i
      ans = min(ans, j - i + 1);
    }
    printf("%d\n", ans == n + 1 ? 0 : ans);
  }
  return 0;
}
// Accepted 79ms 1104kB 731 G++2020-12-24 10:55:33 22229063
```

### 例题23  遥远的银河（Distant Galaxy, Shanghai 2006, POJ3141/LA3695）

```cpp
// 例题23  遥远的银河（Distant Galaxy, Shanghai 2006, POJ3141/LA3695）
// Rujia Liu
#include<cstdio>
#include<algorithm>
using namespace std;

struct Point {
  int x, y;
  bool operator < (const Point& rhs) const {
    return x < rhs.x;
  }
};

const int maxn = 100 + 10;
Point P[maxn];
int n, m, y[maxn], on[maxn], on2[maxn], left[maxn];

int solve() {
  sort(P, P+n);
  sort(y, y+n);
  m = unique(y, y+n) - y; // 所有不同的y坐标的个数
  if(m <= 2) return n; // 最多两种不同的y

  int ans = 0;
  for(int a = 0; a < m; a++)
    for(int b = a+1; b < m; b++) {
      int ymin = y[a], ymax = y[b]; // 计算上下边界分别为ymin和ymax时的解

      // 计算left, on, on2
      int k = 0;
      for(int i = 0; i < n; i++) {
        if(i == 0 || P[i].x != P[i-1].x) { // 一条新的竖线
          k++;
          on[k] = on2[k] = 0;
          left[k] = k == 0 ? 0 : left[k-1] + on2[k-1] - on[k-1];
        } 
        if(P[i].y > ymin && P[i].y < ymax) on[k]++;
        if(P[i].y >= ymin && P[i].y <= ymax) on2[k]++;
      }
      if(k <= 2) return n; // 最多两种不同的x

      int M = 0;
      for(int j = 1; j <= k; j++) {
        ans = max(ans, left[j]+on2[j]+M);
        M = max(M, on[j]-left[j]);
      }
    }
  return ans;
}

int main() {
  int kase = 0;
  while(scanf("%d", &n) == 1 && n) {
    for(int i = 0; i < n; i++) { scanf("%d%d", &P[i].x, &P[i].y); y[i] = P[i].y; }
    printf("Case %d: %d\n", ++kase, solve());
  }
  return 0;
}
// Accepted 16ms 352kB 1338 G++2020-12-22 22:50:02 22226059
```

### UVa10755 Garbage heap

```cpp
// UVa10755 Garbage heap
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<algorithm>
#define FOR(i,s,t)  for(int i = (s); i <= (t); ++i)
using namespace std;

void expand(int i, int& b0, int& b1, int& b2) {
  b0 = i&1; i >>= 1;
  b1 = i&1; i >>= 1;
  b2 = i&1;
}

int sign(int b0, int b1, int b2) {
  return (b0 + b1 + b2) % 2 == 1 ? 1 : -1;
}

const int maxn = 30;
const long long INF = 1LL << 60;

long long S[maxn][maxn][maxn];

long long sum(int x1, int x2, int y1, int y2, int z1, int z2) {
  int dx = x2-x1+1, dy = y2-y1+1, dz = z2-z1+1;
  long long s = 0;
  for(int i = 0; i < 8; i++) {
    int b0, b1, b2;
    expand(i, b0, b1, b2);
    s -= S[x2-b0*dx][y2-b1*dy][z2-b2*dz] * sign(b0, b1, b2);
  }
  return s;
}

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    int a, b, c, b0, b1, b2;
    scanf("%d%d%d", &a, &b, &c);
    memset(S, 0, sizeof(S));
    FOR(x,1,a) FOR(y,1,b) FOR(z,1,c) scanf("%lld", &S[x][y][z]);
    FOR(x,1,a) FOR(y,1,b) FOR(z,1,c) FOR(i,1,7){
      expand(i, b0, b1, b2);
      S[x][y][z] += S[x-b0][y-b1][z-b2] * sign(b0, b1, b2);
    }
    long long ans = -INF;
    FOR(x1,1,a) FOR(x2,x1,a) FOR(y1,1,b) FOR(y2,y1,b) {
      long long M = 0;
      FOR(z,1,c) {
        long long s = sum(x1,x2,y1,y2,1,z);
        ans = max(ans, s - M);
        M = min(M, s);
      }
    }
    printf("%lld\n", ans);
    if(T) printf("\n");
  }
  return 0;
}
// 25875865	10755	Garbage Heap	Accepted	C++	0.210	2020-12-22 14:49:13
```

### 例题18  开放式学分制（Open Credit System, UVa 11078）

```cpp
// 例题18  开放式学分制（Open Credit System, UVa 11078）
// 陈锋
#include <cassert>
#include <cstdio>
#include <algorithm>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
const int MAXN = 1e5 + 4;
int A[MAXN];
int main() {
  int n, T;
  scanf("%d", &T);
  while (T--) {
    scanf("%d", &n);
    _for(i, 0, n) scanf("%d", &(A[i]));
    int m = A[0], ans = A[0] - A[1];  // maxA[i]
    _for(i, 1, n) // m is max{A0, A1, A_{i-1}}      
      ans = max(m - A[i], ans), m = max(A[i], m);
    printf("%d\n", ans);
  }
  return 0;
}
// 18756057	11078	Open Credit System	Accepted	C++11	0.060	2017-02-10 14:12:42
```

### 例题17  年龄排序（Age Sort, UVa 11462）

```cpp
// 例题17  年龄排序（Age Sort, UVa 11462）
// 陈锋
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
const int MAXN = 100;
int main() {
  int n, a, cnt[MAXN + 4];
  while (scanf("%d", &n) == 1 && n) {
    fill_n(cnt, MAXN + 4, 0);
    _for(i, 0, n) scanf("%d", &a), ++cnt[a];
    _for(i, 0, MAXN) _for(j, 0, cnt[i])
      printf("%d%s", i, (i == MAXN - 1 && j == cnt[i] - 1) ? "" : " ");
    puts("");
  }
}
// 25875806	11462	Age Sort	Accepted	C++	0.250	2020-12-22 14:38:05
```

### 例题19  计算器谜题（Calculator Conundrum, UVa 11549）

```cpp
// 例题19  计算器谜题（Calculator Conundrum, UVa 11549）
// 陈锋
#include <iostream>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
LL K, M;
LL next(LL x) {
  LL ans = x * x;
  while (ans >= M) ans /= 10;
  return ans;
}
int main() {
  int T, n;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%lld", &n, &K);
    M = 1;
    _for(i, 0, n) M *= 10;
    LL ans = K, k1 = K, k2 = K;
    do {
      k1 = next(k1), ans = max(ans, k1);
      k2 = next(k2), ans = max(ans, k2);
      k2 = next(k2), ans = max(ans, k2);
    } while (k1 != k2);
    printf("%lld\n", ans);
  }
}
// 21699036 11549 Calculator Conundrum Accepted C++11 0.050 2018-07-28 07:37:08
```

### UVa1398 Meteor (整数版本, 更快)

```cpp
// UVa1398 Meteor (整数版本, 更快)
// 刘汝佳
#include <algorithm>
#include <cstdio>
using namespace std;
// 0<x+at<w
void update(int x, int a, int w, int& L, int& R) {
  if (a == 0) {
    if (x <= 0 || x >= w) R = L - 1;  // 无解
  } else if (a > 0) {
    L = max(L, -x * 2520 / a);
    R = min(R, (w - x) * 2520 / a);
  } else {
    L = max(L, (w - x) * 2520 / a);
    R = min(R, -x * 2520 / a);
  }
}
const int maxn = 1e5 + 8;

struct Event {
  int x;
  int type;
  bool operator<(const Event& a) const {
    return x < a.x || (x == a.x && type > a.type);  // 先处理右端点
  }
} events[maxn * 2];

int main() {
  int T;
  scanf("%d", &T);
  while (T--) {
    int w, h, n, e = 0;
    scanf("%d%d%d", &w, &h, &n);
    for (int i = 0; i < n; i++) {
      int x, y, a, b;
      scanf("%d%d%d%d", &x, &y, &a, &b);
      // 0<x+at<w, 0<y+bt<h, t>=0
      int L = 0, R = 1e9;
      update(x, a, w, L, R);
      update(y, b, h, L, R);
      if (R > L) {
        events[e++] = (Event){L, 0};
        events[e++] = (Event){R, 1};
      }
    }
    sort(events, events + e);
    int cnt = 0, ans = 0;
    for (int i = 0; i < e; i++) {
      if (events[i].type == 0)
        ans = max(ans, ++cnt);
      else
        cnt--;
    }
    printf("%d\n", ans);
  }
  return 0;
}
// 28685849 UVa1398 Accepted 50ms 1246	C++
```

## 1.4 动态规划专题

### 例题26  约瑟夫问题的变形（And Then There Was One, Japan 2007, Codeforces Gym101415A

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

### 例题27  王子和公主（Prince and Princess, UVa 10635）

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

### 例题30  放置街灯（Placing Lampposts, UVa 10859）

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

### 例题28  Sum游戏（Game of Sum, UVa 10891）

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

### 例题32  分享巧克力（Sharing Chocolate, World Finals 2010, UVa1099）

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

### 例题31  捡垃圾的机器人（Robotruck, SWERC 2007, UVa1169）

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

### 例题29  黑客的攻击（Hacker’s Crackdown, UVa 11825）

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
