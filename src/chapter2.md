# 第2章 数学基础

## 2.1 基本计数方法

### 例题2  数三角形（Triangle Counting, UVa11401）

```cpp
// 例题2  数三角形（Triangle Counting, UVa11401）
// Rujia Liu
#include <bits/stdc++.h>
using namespace std;

using LL = long long;  // int存不下
int main() {
  vector<LL> f(1e6 + 4);
  for (LL x = 4; x < (LL)f.size(); x++)
    f[x] = f[x - 1] + ((x - 1) * (x - 2) / 2 - (x - 1) / 2) / 2;  // 递推
  for (int n; cin >> n && n >= 3;) cout << f[n] << endl;
  return 0;
}
// 25877025 11401 Triangle Counting Accepted C++ 0.020 2020-12-23 01:22:22
```

### 例题1  象棋中的皇后（Chess Queen, UVa 11538）

```cpp
// 例题1  象棋中的皇后（Chess Queen, UVa 11538）
// Rujia Liu
#include<iostream>
#include<algorithm>
using namespace std;

int main() {
  unsigned long long n, m; // 最大可以保存2^64-1>1.8*10^19
  while(cin >> n >> m) {
    if(!n && !m) break;
    if(n > m) swap(n, m); // 这样就避免了对n<=m和n>m两种情况分类讨论
    cout << n*m*(m+n-2)+2*n*(n-1)*(3*m-n-1)/3 << endl;
  }
  return 0;
}
// 25877028 11538 Chess Queen Accepted C++ 0.000 2020-12-23 01:22:44
```

### 例题3  拉拉队（Cheerleaders, UVa 11806）

```cpp
// 例题3  拉拉队（Cheerleaders, UVa 11806）
// 陈锋
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
typedef long long LL;
const int MOD = 1000007, MAXC = 400 + 4;
int M, N, K;
LL C[MAXC][MAXC];
void init() {
  C[1][0] = C[1][1] = 1;
  for (int n = 2; n < MAXC; n++) {
    C[n][0] = 1;
    for (int k = 1; k <= n; k++)
      C[n][k] = (C[n - 1][k - 1] + C[n - 1][k]) % MOD;
  }
}
inline LL CK(int m, int n) { return C[m * n][K]; } // get C(m*n, k)

LL solve() {
  if (K < 2 || K > M * N) return 0;
  LL S = C[M * N][K];
  /*S -= (2*CK(M, N-1) + 2*CK(M-1, N))%MOD; // A,B,C,D
    S += (4*CK(M-1,N-1) + CK(M-2, N) + CK(M,N-2))%MOD; // AB,AC,AD,BC,BD,CD
    S -= (2*CK(M-2,N-1) + 2*CK(M-1, N-2))%MOD; // ABC, ABD, ACD, BCD
    S += CK(M-2, N-2); // ABCD */
  for (int b = 1; b < 16; b++) { // 3210 LRTB
    int cnt = 0, m = M, n = N;
    if (b & 8) --m, ++cnt;
    if (b & 4) --m, ++cnt;
    if (b & 2) --n, ++cnt;
    if (b & 1) --n, ++cnt;
    LL x = C[m * n][K];
    if (cnt % 2) x = -x;
    S = (S + MOD + x) % MOD;
  }
  return S;
}

int main() {
  int T;

  init();
  ios::sync_with_stdio(false), cin.tie(0);
  cin >> T;
  for (int t = 1; t <= T; t++) {
    cin >> M >> N >> K;
    printf("Case %d: %lld\n", t, solve());
  }
  return 0;
}
// 21079866 11806 Cheerleaders  Accepted  C++11 0.000 2018-04-04 06:06:31
```

## 2.2 递推关系

### 例题4  多叉树遍历（Exploring Pyramids, NEERC 2005, Codeforces Gym101334E）

```cpp
// 例题4  多叉树遍历（Exploring Pyramids, NEERC 2005, Codeforces Gym101334E）
// Rujia Liu
#include<cstdio>
#include<cstring>
using namespace std;

const int maxn = 300 + 10;
const int MOD = 1000000000;
typedef long long LL;

char S[maxn];
int d[maxn][maxn];

int dp(int i, int j) {
  if(i == j) return 1;
  if(S[i] != S[j]) return 0;
  int& ans = d[i][j];
  if(ans >= 0) return ans;
  ans = 0;
  for(int k = i+2; k <= j; k++) if(S[i] == S[k])
    ans = (ans + (LL)dp(i+1,k-1) * (LL)dp(k,j)) % MOD;
  return ans;
}

int main() {
  freopen("exploring.in", "r", stdin);
  freopen("exploring.out", "w", stdout);
  while(scanf("%s", S) == 1) {
    memset(d, -1, sizeof(d));
    printf("%d\n", dp(0, strlen(S)-1));
  }
  return 0;
}
// 102083028 	Dec/23/2020 09:32UTC+8 	chenwz 	E - Exploring Pyramids 	GNU C++11 	Accepted 	61 ms 	300 KB 
```

### 例题7  串并联网络（Series-Parallel Networks, UVa 10253）

```cpp
// 例题7  串并联网络（Series-Parallel Networks, UVa 10253）
// Rujia Liu
#include<cstdio>
#include<cstring>

long long C(long long n, long long m) {
  double ans = 1;
  for(int i = 0; i < m; i++)
    ans *= n-i;
  for(int i = 0; i < m; i++)
    ans /= i+1;
  return (long long)(ans + 0.5);
}

const int maxn = 30 + 5;
long long f[maxn], d[maxn][maxn]; //d(i,j)表示每棵树最多包含i个叶子，一共有j个叶子的方案数

int main() {
  f[1] = 1;
  memset(d, 0, sizeof(d));

  int n = 30;
  for(int i = 0; i <= n; i++) d[i][0] = 1;
  for(int i = 1; i <= n; i++) { d[i][1] = 1; d[0][i] = 0; }

  for(int i = 1; i <= n; i++) {
    for(int j = 2; j <= n; j++) {
      d[i][j] = 0;
      for(int p = 0; p*i <= j; p++)
        d[i][j] += C(f[i]+p-1, p) * d[i-1][j-p*i];
    }
    f[i+1] = d[i][i+1];
  }

  while(scanf("%d", &n) == 1 && n)
    printf("%lld\n", n == 1 ? 1 : 2*f[n]);
  return 0;
}
// 25877044  10253  Series-Parallel Networks  Accepted  C++  0.000  2020-12-23 01:33:19
```

### 例题6  葛伦堡博物馆（Glenbow Museum, World Finals 2008, UVa1073）

```cpp
// 例题6  葛伦堡博物馆（Glenbow Museum, World Finals 2008, UVa1073）
// Rujia Liu
#include<cstdio>
#include<cstring>
const int maxn = 1000;

long long d[maxn+1][5][2], ans[maxn+1];

int main() {
  memset(d, 0, sizeof(d));
  for(int k = 0; k < 2; k++) {
    d[1][0][k] = 1;
    for(int i = 2; i <= maxn; i++)
      for(int j = 0; j < 5; j++) {
        d[i][j][k] = d[i-1][j][k];
        if(j > 0) d[i][j][k] += d[i-1][j-1][k];
      }
  }

  memset(ans, 0, sizeof(ans));
  for(int i = 1; i <= maxn; i++) {
    if(i < 4 || i % 2 == 1) continue;
    int R = (i+4)/2;    
    ans[i] = d[R][3][0] + d[R][4][1] + d[R][4][0];
  }

  int n, kase = 1;
  while(scanf("%d", &n) == 1 && n)
    printf("Case %d: %lld\n", kase++, ans[n]);
  return 0;
}
// 25877043  1073  Glenbow Museum  Accepted  C++  0.000  2020-12-23 01:32:37
```

### 例题5  数字和与倍数（Investigating Div-Sum Property, UVa 11361）

```cpp
// 例题5  数字和与倍数（Investigating Div-Sum Property, UVa 11361）
// Rujia Liu
#include<cstdio>
#include<cstring>
using namespace std;

int MOD; // 题目中叫k，改名为MOD可以让代码更清晰
int pow10[10];

// 整数n除以MOD的余数，返回0~MOD-1
int mod(int n) {
  return (n % MOD + MOD) % MOD;
}

// 共d个数字，数字之和除以k的余数为m1，整数本身除以k的余数为m2
int memo[11][90][90];
int f(int d, int m1, int m2) {
  if(d == 0) return m1 == 0 && m2 == 0 ? 1 : 0;

  int& ans = memo[d][m1][m2];
  if(ans >= 0) return ans;
  ans = 0;
  for(int x = 0; x <= 9; x++)
    ans += f(d-1, mod(m1-x), mod(m2-x*pow10[d-1]));
  return ans;
}

// 统计0~n-1中满足条件的整数个数（和书上的分析有一点出入，但没有本质区别）
int sumf(int n) {
  char digits[11];
  sprintf(digits, "%d", n);
  int nd = strlen(digits);

  int base = 0; // 当前区间的左边界
  int sumd = 0; // 当前区间的左边界的数字和
  int ans = 0;
  for(int i = 0; i < nd; i++) { // 有i个数字(i>=0)
    int na = nd - 1 - i; // 星号的个数
    for(int d = 0; d < digits[i] - '0'; d++) {
      int cnt = f(na, mod(-sumd - d), mod(-base - d*pow10[na]));
      ans += cnt;
    }
    base += (digits[i] - '0') * pow10[na];
    sumd += (digits[i] - '0');
  }
  return ans;
}

int main() {
  pow10[0] = 1;
  for(int i = 1; i <= 9; i++) pow10[i] = pow10[i-1] * 10;

  int T;
  scanf("%d", &T);
  while(T--) {
    int a, b;
    scanf("%d%d%d", &a, &b, &MOD);
    memset(memo, -1, sizeof(memo));
    if(MOD > 85) printf("0\n"); // 数字和最多为1+9*9=82，如果MOD大于此值，一定无解
    else printf("%d\n", sumf(b+1) - sumf(a));
  }
  return 0;
}
// 25877033 	11361 	Investigating Div-Sum Property 	Accepted 	C++11 	0.020 	2020-12-23 01:24:34
```

## 2.3 数论

### 例题14  墨菲斯（Mophues, ACM/ICPC Asia Regional Hangzhou Online 2013, HDU4746）

```cpp
// 例题14  墨菲斯（Mophues, ACM/ICPC Asia Regional Hangzhou Online 2013, HDU4746）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;

const int MAXN = 500000 + 4, MAXP = MAXN;
vector<bool> isPrime(MAXP, true);
vector<LL> Mu(MAXP), Primes, H(MAXP, 1);
LL G[MAXN][20];
void sieve() {
  Mu[1] = 1, H[1] = 0;
  for (int i = 2; i < MAXP; ++i) {
    if (isPrime[i]) Primes.push_back(i), Mu[i] = -1, H[i] = 1;
    for(size_t j = 0; j < Primes.size(); ++j) {
      LL p = Primes[j], t = p * i;
      if (t >= MAXP) break;
      isPrime[t] = false, H[t] = H[i] + 1;
      if (i % p == 0) {
        Mu[t] = 0;
        break;
      }
      Mu[t] = -Mu[i];
    }
  }
  memset(G, 0, sizeof(G));
  for (int n = 1; n < MAXN; n++) {
    for (int k = 1, T = n; T < MAXN; ++k, T += n)
      G[T][H[n]] += Mu[k];  //Σμ(T/n)|h(n)=P
  }

  for (int n = 1; n < MAXN; n++) 
    for(int p = 1; p < 20; p++)
      G[n][p] += G[n][p - 1];  // Σμ(T/n)|h(n)≤P
  for (int n = 1; n < MAXN; n++) 
    for(int p = 0; p < 20; p++)  G[n][p] += G[n - 1][p];  // ∑nΣμ(T/n)|h(n)≤P
}

LL N, M, P;
LL solve() {
  if (P >= 20) return N * M;
  if (N > M) swap(N, M);
  LL ans = 0;
  for (int T = 1, et = 0; T <= N; T = et + 1) {
    et = min(N / (N / T), M / (M / T));  // All t in [T, et] same N/t, M/t
    ans += (G[et][P] - G[T - 1][P]) * (N / T) * (M / T);
  }
  return ans;
}

int main() {
  sieve();
  int Q;
  scanf("%d", &Q);
  while (Q--) {
    scanf("%lld%lld%lld", &N, &M, &P);
    printf("%lld\n", solve());
  }
  return 0;
}
// Accepted 608ms 88356kB 1456 G++ 2020-12-09 18:01:47 34811735
```

### 例题15  数一数a x b（Count a x b, ACM/ICPC Changchun 2015, LA7184/HDU5528）

```cpp
// 例题15  数一数a x b（Count a x b, ACM/ICPC Changchun 2015, LA7184/HDU5528）
// 陈锋
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
const int MAXN = (int)(1e9) + 4, MAXP = 31622 + 4;
typedef unsigned long long ULL;

// lp:i的最小素因子, primes: 记录所有素数
int lp[MAXP], primes[MAXP], pcnt;
void sieve(int N) {
  pcnt = 0;
  fill_n(lp, N, 0);
  for (int i = 2; i < N; ++i) {
    int& l = lp[i]; // i的最小素因子l
    if (l == 0) l = i, primes[pcnt++] = i; // i是素数
    for (int j = 0; j < pcnt && primes[j] <= l; ++j) {
      int p = primes[j]; // p <= l
      if (i * p >= N) break;
      lp[i * p] = p; // i * p的最小素因子是p
    }
  }
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T, N;
  cin >> T;
  sieve(MAXP);
  while (T--) {
    cin >> N;
    ULL g = 1, h = N, x = N;
    _for(i, 0, pcnt) {
      ULL p = primes[i];
      if (p > x) break;
      if (x % p != 0) continue;
      int k = 0;
      ULL sp = 1, pp = p * p;  // Σp^(2i), p^2i
      for (k = 0; x % p == 0; k++) {
        x /= p;
        sp += pp, pp *= p * p;
      }
      g *= sp, h *= k + 1;
    }
    if (x > 1) g *= (1 + x * x), h *= 2;
    cout << g - h << endl;
  }
  return 0;
}
// 2620236  7184  Count a × b   Accepted  C++11   0.436   2019-12-10 06:01:35
```

### 例题12  可怕的诗篇（A Horrible Poem，POI2012）

```cpp
// 例题12  可怕的诗篇（A Horrible Poem，POI2012）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

const int NN = 5e5 + 4, x = 263;
typedef unsigned long long ULL;
typedef long long LL;

ULL XP[NN];
void initXP() {
  XP[0] = 1;
  for (size_t i = 1; i < NN; i++) XP[i] = x * XP[i - 1];
}
template <size_t SZ>
struct StrHash {
  size_t N;
  ULL H[SZ];

  void init(const char* pc, size_t n = 0) {
    if (XP[0] != 1) initXP();
    if (n == 0) n = strlen(pc);
    N = n;
    assert(N > 0);
    assert(N + 1 < SZ);
    H[N] = 0;
    for (int i = N - 1; i >= 0; --i) H[i] = pc[i] - 'a' + 1 + x * (H[i + 1]);
  }

  void init(const string& S) { init(S.c_str(), S.size()); }
  inline ULL hash(size_t i, size_t j) {  // hash[i, j]
    // assert(i <= j);
    // assert(j < N);
    return H[i] - H[j + 1] * XP[j - i + 1];
  }
  inline ULL hash() { return H[0]; }
};

StrHash<NN> hs;
char S[NN];
int lastP[NN], primes[NN], pCnt;
void sieve(int N) {
  pCnt = 0;
  fill_n(lastP, N, 0);
  int* P = primes;
  for (int i = 2; i < N; ++i) {
    int& l = lastP[i];                 // i的最小素因子
    if (l == 0) l = i, P[pCnt++] = i;  // i是素数
    for (int j = 0; j < pCnt && P[j] <= l && P[j] * i < N; ++j)
      lastP[i * P[j]] = P[j];  // i*p的最小素因子是p
  }
}

int find_rep(int a, int b) {
  int L = b - a + 1, xl = L;
  while (xl > 1) {
    int p = lastP[xl];  // 尝试每一个素因子
    if (hs.hash(a, b - L / p) == hs.hash(a + L / p, b)) L /= p;
    xl /= p;
  }
  return L;
}

int main() {
  int n, q;
  S[0] = '|';
  scanf("%d%s%d", &n, S + 1, &q);
  hs.init(S, n + 1), sieve(n + 1);
  for (int i = 0, a, b; i < q; i++)
    scanf("%d%d", &a, &b), printf("%d\n", find_rep(a, b));
  return 0;
}
// 45995132	A Horrible Poem	答案正确 100 1117 24464 1612 C++ 2020-12-09
```

### 例题13  可见格点（Visible Lattice Points, Indian ICPC training camp, SPOJ VLATTICE）

```cpp
// 例题13  可见格点（Visible Lattice Points, Indian ICPC training camp, SPOJ VLATTICE）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)
typedef long long LL;
const int MAXN = 1000000 + 4;
valarray<bool> isPrime(true, MAXN);
valarray<LL> Mu(0LL, MAXN), Lp(0LL, MAXN);
vector<LL> Ps;
void sieve(int N) {
  Ps.clear(), Mu[1] = 1;
  _for(i, 2, N) {
    LL& l = Lp[i];
    if (l == 0) Ps.push_back(i), Mu[i] = -1, l = i;
    for (size_t j = 0; j < Ps.size() && Ps[j] <= l && Ps[j] * i < N; ++j) {
      LL p = Ps[j];
      Lp[i * p] = p;
      if (i % p == 0) {
        Mu[i * p] = 0;
        break;
      }
      Mu[i * p] = -Mu[i];
    }
  }
}

int main() {
  sieve(MAXN);
  int T, N;
  scanf("%d", &T);
  while (T--) {
    scanf("%d", &N);
    LL ans = 3;  // 3个坐标轴上的点
    _rep(d, 1, N) {
      LL k = N / d;
      ans += Mu[d] * k * k * (k + 3);  // (x,y,z)个数以及三个平面上的(x,y)个数
    }
    printf("%lld\n", ans);
  }
  return 0;
}
// 25042176 2019-12-10 15:00:43 Feng Chen Visible Lattice Points accepted 0.09 20M CPP14
```

### 例题8  总是整数（Always an Integer, World Finals 2008, UVa1069）

```cpp
// 例题8  总是整数（Always an Integer, World Finals 2008, UVa1069）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;

struct Polynomial {
  vector<int> a, p;                     //第i项为a[i] * n^p[i]
  void parse_polynomial(string expr) {  //解析多项式（不带括号）
    int i = 0, len = expr.size();
    while (i < len) {  //每次循环体解析一个a * n^p
      int sign = 1, v = 0;
      if (expr[i] == '+') i++;
      if (expr[i] == '-') sign = -1, i++;
      while (i < len && isdigit(expr[i])) v = v * 10 + expr[i++] - '0';
      //系数的绝对值
      if (i == len) {
        a.push_back(v), p.push_back(0);
        continue;
      }  //常数项
      assert(expr[i] == 'n');
      if (v == 0) v = 1;  //无系数，按1处理
      v *= sign;
      if (expr[++i] == '^') {   //有指数项
        a.push_back(v), v = 0;  //清空v，接下来用v保存指数
        i++;
        while (i < len && isdigit(expr[i])) v = v * 10 + expr[i++] - '0';
        p.push_back(v);
      } else  //无指数项
        a.push_back(v), p.push_back(1);
    }
  }

  // 计算f(x)除以MOD的余数
  int mod(int x, int MOD) {
    int ans = 0;
    for (size_t i = 0; i < a.size(); i++) {
      int m = a[i];
      for (int j = 0; j < p[i]; j++) m = (LL)m * x % MOD;
      //注意避免溢出
      ans = ((LL)ans + m) % MOD;  //加法也可能会溢出。
    }
    return ans;
  }
};

bool check(string expr) {
  int p = expr.find('/');
  Polynomial poly;
  poly.parse_polynomial(expr.substr(1, p - 2));
  int D = atoi(expr.substr(p + 1).c_str());
  for (int i = 1; i <= poly.p[0] + 1; i++)
    if (poly.mod(i, D) != 0) return false;
  return true;
}

int main() {
  string expr;
  for (int kase = 1; cin >> expr; kase++) {
    if (expr[0] == '.') break;
    printf("Case %d: ", kase);
    if (check(expr))
      puts("Always an integer");
    else
      puts("Not always an integer");
  }
  return 0;
}
// Accepted 70ms 1829 C++5.3.0 2020-12-12 16:16:22 25838756
```

### 例题9  最大公约数之和——极限版II（GCD Extreme(II), UVa 11426）

```cpp
// 例题9  最大公约数之和——极限版II（GCD Extreme(II), UVa 11426）
// 刘汝佳
#include <cstdio>
#include <cstring>
const int NN = 4000000;
typedef long long LL;

int phi[NN + 1];
void phi_table(int n) {
  for (int i = 2; i <= n; i++) phi[i] = 0;
  phi[1] = 1;
  for (int i = 2; i <= n; i++)
    if (!phi[i])
      for (int j = i; j <= n; j += i) {
        if (!phi[j]) phi[j] = j;
        phi[j] = phi[j] / i * (i - 1);
      }
}
LL S[NN + 1], f[NN + 1];
int main() {
  phi_table(NN);

  // 预处理f
  memset(f, 0, sizeof(f));
  for (int i = 1; i <= NN; i++)
    for (int n = i * 2; n <= NN; n += i) f[n] += i * phi[n / i];

  // 预处理S
  S[2] = f[2];
  for (int n = 3; n <= NN; n++) S[n] = S[n - 1] + f[n];
  for (int n; scanf("%d", &n) == 1 && n;) printf("%lld\n", S[n]);
  return 0;
}
// Accepted 760ms 727 C++ 5.3.0 2020-12-09 17:21:08 25828691
```

### 例题10  数论难题（Code Feat, UVa 11754）

```cpp
// 例题10  数论难题（Code Feat, UVa 11754）
// 刘汝佳
typedef long long LL;

// 即使a, b在int范围内，x和y有可能超出int范围
void gcd(LL a, LL b, LL& d, LL& x, LL& y) {
  if (!b) {
    d = a, x = 1, y = 0;
  } else {
    gcd(b, a % b, d, y, x);
    y -= x * (a / b);
  }
}

// n个方程：x=a[i](mod m[i]) (0<=i<n)
LL china(int n, int* a, int* m) {
  LL M = 1, d, y, x = 0;
  for (int i = 0; i < n; i++) M *= m[i];
  for (int i = 0; i < n; i++) {
    LL w = M / m[i];
    gcd(m[i], w, d, d, y);
    x = (x + y * w * a[i]) % M;
  }
  return (x + M) % M;
}

#include <algorithm>
#include <cstdio>
#include <set>
#include <vector>
using namespace std;

const int maxc = 9, maxk = 100, LIMIT = 10000;
set<int> values[maxc];
int C, X[maxc], k[maxc], Y[maxc][maxk];

void solve_enum(int S, int bc) {
  for (int c = 0; c < C; c++)
    if (c != bc) {
      values[c].clear();
      for (int i = 0; i < k[c]; i++) values[c].insert(Y[c][i]);
    }
  for (int t = 0; S != 0; t++) {
    for (int i = 0; i < k[bc]; i++) {
      LL n = (LL)X[bc] * t + Y[bc][i];
      if (n == 0) continue;  // 只输出正数解
      bool ok = true;
      for (int c = 0; c < C; c++)
        if (c != bc)
          if (!values[c].count(n % X[c])) {
            ok = false;
            break;
          }
      if (ok) {
        printf("%lld\n", n);
        if (--S == 0) break;
      }
    }
  }
}

int a[maxc];  // 搜索对象，用于中国剩余定理
vector<LL> sol;

void dfs(int dep) {
  if (dep == C)
    sol.push_back(china(C, a, X));
  else
    for (int i = 0; i < k[dep]; i++) a[dep] = Y[dep][i], dfs(dep + 1);
}

void solve_china(int S) {
  sol.clear();
  dfs(0);
  sort(sol.begin(), sol.end());

  LL M = 1;
  for (int i = 0; i < C; i++) M *= X[i];

  vector<LL> ans;
  for (int i = 0; S != 0; i++) {
    for (int j = 0; j < sol.size(); j++) {
      LL n = M * i + sol[j];
      if (n > 0) {
        printf("%lld\n", n);
        if (--S == 0) break;
      }
    }
  }
}

int main() {
  int S;
  while (scanf("%d%d", &C, &S) == 2 && C) {
    LL tot = 1;
    int bestc = 0;
    for (int c = 0; c < C; c++) {
      scanf("%d%d", &X[c], &k[c]);
      tot *= k[c];
      for (int i = 0; i < k[c]; i++) scanf("%d", &Y[c][i]);
      sort(Y[c], Y[c] + k[c]);
      if (k[c] * X[bestc] < k[bestc] * X[c]) bestc = c;
    }
    if (tot > LIMIT)
      solve_enum(S, bestc);
    else
      solve_china(S);
    printf("\n");
  }
  return 0;
}
// Accepted 10ms 2326 C++5.3.0 2020-12-09 17:27:16 25828703
```

### 例题11  网格涂色（Emoogle Grid, UVa 11916）

```cpp
// 例题11  网格涂色（Emoogle Grid, UVa 11916）
// Rujia Liu
#include<cstdio>
#include<algorithm>
#include<cmath>
#include<set>
#include<map>
using namespace std;

const int MOD = 100000007;
const int maxb = 500 + 10;
int n, m, k, b, r, x[maxb], y[maxb];
set<pair<int, int> > bset;

int pow_mod(int a, long long p) {
  if(p == 0) return 1;
  int ans = pow_mod(a, p/2);
  ans = (long long)ans * ans % MOD;
  if(p%2) ans = (long long)ans * a % MOD;
  return ans;
}

int mul_mod(int a, int b) {
  return (long long)a * b % MOD;
}

int inv(int a) {
  return pow_mod(a, MOD-2);
}

int log_mod(int a, int b) {
  int m, v, e = 1, i;
  m = (int)sqrt(MOD);
  v = inv(pow_mod(a, m));
  map <int,int> x;
  x[1] = 0;
  for(i = 1; i < m; i++){ e = mul_mod(e, a); if (!x.count(e)) x[e] = i; }
  for(i = 0; i < m; i++){
    if(x.count(b)) return i*m + x[b];
    b = mul_mod(b, v);
  }
  return -1;
}

// 计算可变部分的方案数
int count() {
  int c = 0; // 有k种涂法的格子数
  for(int i = 0; i < b; i++) {
    if(x[i] != m && !bset.count(make_pair(x[i]+1, y[i]))) c++; // 不可涂色格下面的可涂色格
  }
  c += n; // 第一行所有空格都有k种涂法
  for(int i = 0; i < b; i++)
    if(x[i] == 1) c--; // 扣除那些不能涂色的格子

  // ans = k^c * (k-1)^(mn - b - c)
  return mul_mod(pow_mod(k, c), pow_mod(k-1, (long long)m*n - b - c));
}

int doit() {
  int cnt = count();
  if(cnt == r) return m; // 不变部分为空

  int c = 0;
  for(int i = 0; i < b; i++)
    if(x[i] == m) c++; // 可变部分第一行中有k种涂法的格子数
  m++; // 多了一行（可变部分的第一行）
  cnt = mul_mod(cnt, pow_mod(k, c));
  cnt = mul_mod(cnt, pow_mod(k-1, n - c));
  if(cnt == r) return m; // 此时cnt为不变部分和可变部分第一行的方案总数

  return log_mod(pow_mod(k-1,n), mul_mod(r, inv(cnt))) + m;
}

int main() {
  int T;
  scanf("%d", &T);
  for(int t = 1; t <= T; t++) {
    scanf("%d%d%d%d", &n, &k, &b, &r);
    bset.clear();
    m = 1;
    for(int i = 0; i < b; i++) {
      scanf("%d%d", &x[i], &y[i]);
      if(x[i] > m) m = x[i]; // 更新不变部分的行数
      bset.insert(make_pair(x[i], y[i]));
    }
    printf("Case %d: %d\n", t, doit());
  }
}
// 25877053  11916  Emoogle Grid  Accepted  C++  0.280  2020-12-23 01:39:19
```

## 2.4 组合游戏

### 例题17  Treblecross游戏（Treblecross, UVa 10561）

```cpp
// 例题17  Treblecross游戏（Treblecross, UVa 10561）
// 刘汝佳
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;

const int NN = 200;
int g[NN + 10];

bool winning(const char* state) {
  int n = strlen(state);
  for (int i = 0; i < n - 2; i++)
    if (state[i] == 'X' && state[i + 1] == 'X' && state[i + 2] == 'X')
      return false;  // 已经输掉了

  int no[NN + 1];  // no[i] = 1: 下标为i的格子是“禁区”（离某个'X'的距离不超过2）
  fill_n(no, NN + 1, 0);
  no[n] = 1;  // 哨兵
  for (int i = 0; i < n; i++) {
    if (state[i] != 'X') continue;
    for (int d = -2; d <= 2; d++)
      if (i + d >= 0 && i + d < n) {
        if (d != 0 && state[i + d] == 'X')
          return true;  // 有两个距离不超过2的'X'，一步即可取胜
        no[i + d] = 1;
      }
  }

  int sg = 0;                                 // 当前块的起点坐标
  for (int i = 0, start = -1; i <= n; i++) {  // 注意要循环到“哨兵”为止
    if (start < 0 && !no[i]) start = i;       // 新的块
    if (no[i] && start >= 0) sg ^= g[i - start];  // 当前块结束
    if (no[i]) start = -1;
  }
  return sg != 0;
}

int mex(vector<int>& s) {
  if (s.empty()) return 0;
  sort(s.begin(), s.end());
  if (s[0] != 0) return 0;
  for (int i = 1; i < s.size(); i++)
    if (s[i] > s[i - 1] + 1) return s[i - 1] + 1;
  return s[s.size() - 1] + 1;
}

void init() {  // 预处理计算g数组
  g[0] = 0, g[1] = g[2] = g[3] = 1;
  for (int i = 4; i <= NN; i++) {
    vector<int> s;
    s.push_back(g[i - 3]);              // 最左边（下标为0的格子）
    s.push_back(g[i - 4]);              // 下标为1的格子
    if (i >= 5) s.push_back(g[i - 5]);  // 下标为2的格子
    for (int j = 3; j < i - 3; j++)     // 下标为3~i-3的格子
      s.push_back(g[j - 2] ^ g[i - j - 3]);  // 左边有j-2个，右边有i-j-3个格子
    g[i] = mex(s);
  }
}

int main() {
  init();
  int T;
  scanf("%d", &T);
  while (T--) {
    char state[NN + 10];
    scanf("%s", state);
    int n = strlen(state);
    if (!winning(state))
      puts("LOSING\n");
    else {
      puts("WINNING");
      vector<int> moves;
      for (int i = 0; i < n; i++)
        if (state[i] == '.') {
          state[i] = 'X';
          if (!winning(state)) moves.push_back(i + 1);
          state[i] = '.';
        }
      printf("%d", moves[0]);
      for (int i = 1; i < moves.size(); i++) printf(" %d", moves[i]);
      puts("");
    }
  }
  return 0;
}
// Accepted 2240 C++5.3.0 2020-12-12 17:23:57 25839095
```

### 例题16  石子游戏（Playing with Stones, Jakarta 2010, UVa1482）

```cpp
// 例题16  石子游戏（Playing with Stones, Jakarta 2010, UVa1482）
// Rujia Liu
#include <iostream>
using namespace std;

long long SG(long long x){
  return x%2==0 ? x/2 : SG(x/2);
}

int main() {
  int T;
  cin >> T;
  while (T--){
    int n;
    long long a, v = 0;
    cin >> n;
    for(int i = 0; i < n; i++) {
      cin >> a;
      v ^= SG(a);
    }
    if(v) cout << "YES\n";
    else cout << "NO\n";
  }
  return 0;
}
// 25877087  1482  Playing With Stones  Accepted  C++  0.000  2020-12-23 02:08:00
```

## 2.5 概率与数学期望

### UVa11021 Tribles

```cpp
// UVa11021 Tribles
// 陈锋
#include <cmath>
#include <cstdio>
using namespace std;
typedef long long LL;
const int MAXN = 1000 + 4;
double P[MAXN], F[MAXN];
int main() {
  int T;
  scanf("%d", &T);
  for (int t = 1, n, k, m; t <= T; t++) {
    scanf("%d%d%d", &n, &k, &m);
    for (int i = 0; i < n; i++) scanf("%lf", &(P[i]));
    F[0] = 0, F[1] = P[0];
    for (int x = 2; x <= m; x++) {
      F[x] = 0;
      for (int i = 0; i < n; i++) F[x] += P[i] * pow(F[x - 1], i);
    }
    printf("Case #%d: %.7lf\n", t, pow(F[m], k));
  }
  return 0;
}
// 25838816 11021 Tribles Accepted C++ 0.050 2020-12-12 08:28:17
```

### UVa11427 Expect the Expected

```cpp
// UVa11427 Expect the Expected
// 刘汝佳
#include <cmath>
#include <cstdio>
#include <cstring>
const int NN = 100 + 5;
double D[NN][NN];
int main() {
  int T;
  scanf("%d", &T);
  for (int kase = 1, n, a, b; kase <= T; kase++) {
    scanf("%d/%d%d", &a, &b, &n);  // 请注意scanf的技巧
    double p = (double)a / b;
    memset(D, 0, sizeof(D));
    D[0][0] = 1.0, D[0][1] = 0.0;
    for (int i = 1; i <= n; i++)
      for (int j = 0; j * b <= a * i; j++) {
        // 等价于枚举满足j/i <= a/b的j，但避免了除法误差
        double &d = D[i][j];
        d = D[i - 1][j] * (1 - p);
        if (j) d += D[i - 1][j - 1] * p;
      }
    double Q = 0.0;
    for (int j = 0; j * b <= a * n; j++) Q += D[n][j];
    printf("Case #%d: %d\n", kase, (int)(1 / Q));
  }
  return 0;
}
// Accepted 10ms 739 C++5.3.0 2020-12-12 16:44:12 25838891
```

### UVa11722 Joining with Friend （限于篇幅，书上无此代码）

```cpp
// UVa11722 Joining with Friend （限于篇幅，书上无此代码）
// Rujia Liu
#include<cstdio>
double t1, t2, s1, s2, width, height;

// 求直线y=x+w上方被矩形(s1,t1)-(s2,t2)切割得到的面积
double get_area(double w) {
  double ly = t1+w, ry = t2+w; // 左右交点的y坐标
  double tx = s2-w, bx = s1-w; // 上下交点的x坐标
  bool on_left   = s1 <= ly && ly <= s2;
  bool on_right  = s1 <= ry && ry <= s2;
  bool on_top    = t1 <= tx && tx <= t2;
  bool on_bottom = t1 <= bx && bx <= t2;
  if(on_left && on_right)   return (s2 - ly + s2 - ry) * width * 0.5;
  if(on_left && on_top)     return (s2 - ly) * (tx - t1) * 0.5;
  if(on_top && on_bottom)   return (bx - t1 + tx - t1) * height * 0.5;
  if(on_right && on_bottom) return height * width - (t2 - bx) * (ry - s1) * 0.5;
  return ly <= s1 ? width * height : 0;
}

int main() {
  int T, kase = 1;
  scanf("%d", &T);
  while(T--) {
    double w;
    scanf("%lf%lf%lf%lf%lf", &t1, &t2, &s1, &s2, &w);
    width = t2 - t1;
    height = s2 - s1;
    double a1 = get_area(w);
    double a2 = get_area(-w);
    printf("Case #%d: %.6lf\n", kase++, (a2 - a1) / width / height);
  }
  return 0;
}
```

### UVa11762 Race To 1

```cpp
// UVa11762 Race To 1
// 陈锋
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstring>
using namespace std;

const int NN = 1e6 + 10;
double F[NN];
int IsPrime[NN], primes[NN], vis[NN];

void gen_primes(int n) {
  fill_n(IsPrime, n + 1, 1);
  for (int i = 2, p = 0; i <= n; i++) {
    if (!IsPrime[i]) continue;
    primes[p++] = i;
    if (i <= n / i)
      for (int j = i * i; j <= n; j += i) IsPrime[j] = 0;
  }
}

double dp(int x) {
  double& f = F[x];
  if (x == 1) return 0.0;  // 边界
  if (vis[x]) return f;    // 记忆化
  vis[x] = 1;
  int g = 0, p = 0;  // 累加g(x)和p(x)
  f = 0;
  for (int i = 0; primes[i] <= x; i++) {
    p++;
    if (x % primes[i] == 0) g++, f += dp(x / primes[i]);
  }
  return f = (f + p) / g;
}

int main() {
  int T;
  scanf("%d", &T);
  gen_primes(NN - 1), fill_n(vis, NN, 0);
  for (int kase = 1, n; kase <= T; kase++) {
    scanf("%d", &n);
    printf("Case %d: %.10lf\n", kase, dp(n));
  }
  return 0;
}
// Accepted 190ms 964 C++ 5.3.0 2020-12-12 16:51:29 25838925
```

## 2.6 置换及其应用

### 例题23  Leonardo的笔记本（Leonardo's Notebook , NWERC 2006, Codeforces Gym100722I）

```cpp
// 例题23  Leonardo的笔记本（Leonardo's Notebook , NWERC 2006, Codeforces Gym100722I）
// Rujia Liu
#include<cstdio>
#include<cstring>
int main() {
  char B[30];
  int vis[30], cnt[30], T;
  scanf("%d", &T);
  while(T--) {
    scanf("%s", B);
    memset(vis, 0, sizeof(vis));
    memset(cnt, 0, sizeof(cnt));
    for(int i = 0; i < 26; i++)
      if(!vis[i]) { // 找一个从i开始的循环
        int j = i, n = 0;
        do {
          vis[j] = 1; // 标记j为“已访问”
          j = B[j] - 'A';
          n++;
        } while(j != i);
        cnt[n]++;
      }
    int ok = 1;
    for(int i = 2; i <= 26; i++)
      if(i%2 == 0 && cnt[i]%2 == 1) ok = 0;
    if(ok) printf("Yes\n"); else printf("No\n");
  }
  return 0;
}
// 102084408 	Dec/23/2020 10:33UTC+8 	chenwz 	I - Leonardo's Notebook 	GNU C++11 	Accepted 	15 ms 	0 KB
```

### 例题22  项链和手镯（Arif in Dhaka(First Love Part 2), UVa 10294）

```cpp
// 例题22  项链和手镯（Arif in Dhaka(First Love Part 2), UVa 10294）
// 陈锋
#include <cstdio>
typedef long long LL;
const int NN = 100;
int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }

int main() {
  for (int n, t; scanf("%d%d", &n, &t) == 2 && n;) {
    LL pow[NN], a = 0, b = 0;
    pow[0] = 1;
    for (int i = 1; i <= n; i++) pow[i] = pow[i - 1] * t;
    for (int i = 0; i < n; i++) a += pow[gcd(i, n)];
    if (n % 2 == 1)
      b = n * pow[(n + 1) / 2];
    else
      b = n / 2 * (pow[n / 2 + 1] + pow[n / 2]);
    printf("%lld %lld\n", a / n, (a + b) / 2 / n);
  }
  return 0;
}
// Accepted 583 C++5.3.0 2020-12-12 17:34:43 25839147
```

### 例题24  排列统计（Find the Permutations, UVa 11077）

```cpp
// 例题24  排列统计（Find the Permutations, UVa 11077）
// 刘汝佳
#include <cstdio>
#include <cstring>
const int maxn = 30;
unsigned long long f[maxn][maxn];
int main() {
  memset(f, 0, sizeof(f));
  f[1][0] = 1;
  for (int i = 2; i <= 21; i++)
    for (int j = 0; j < i; j++) {
      f[i][j] = f[i - 1][j];
      if (j > 0) f[i][j] += f[i - 1][j - 1] * (i - 1);
    }
  int n, k;
  while (scanf("%d%d", &n, &k) == 2 && n) printf("%llu\n", f[n][k]);
  return 0;
}
// Accepted 435 C++5.3.0 2020-12-12 20:34:55 25839718
```

## 2.7 矩阵和线性方程组

### 例题27  细胞自动机（Cellular Automaton, NEERC 2006, Codeforces Gym100287C）

```cpp
// 例题27  细胞自动机（Cellular Automaton, NEERC 2006, Codeforces Gym100287C）
// 陈锋
#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;
typedef long long LL;
const int maxn = 500 + 8;
int MOD;
struct Matrix {
  int a[maxn], n;
  Matrix(int _n = 1) : n(_n) { fill_n(a, n + 1, 0); }
  Matrix operator * (const Matrix &rhs) {
    Matrix m(n);
    for (int i = 0; i < n; i++)
      for (int j = 0; j < n; j++)
        (m.a[i] += (LL)a[(i - j + n) % n] * rhs.a[j] % MOD) %= MOD;
    return m;
  }
};

Matrix fast_pow(Matrix x, int n) {
  Matrix m(x.n); m.a[0] = 1;
  while (n) {
    if (n % 2) m = m * x;
    x = x * x, n /= 2;
  }
  return m;
}

int main() {
  freopen("cell.in", "r", stdin);
  freopen("cell.out", "w", stdout);
  for (int d, k, n, m; scanf("%d %d %d %d", &n, &m, &d, &k) == 4;) {
    MOD = m;
    Matrix x(n), y(n);
    for (int i = 0; i < n; ++i)  scanf("%d", &x.a[i]);
    fill_n(y.a, d + 1, 1), fill_n(y.a + n - d, d, 1);
    Matrix ans = x * fast_pow(y, k);
    for (int i = 0; i < n; ++i)  printf("%d%c", ans.a[i], " \n"[i + 1 == n]);
  }
  return 0;
}
// 102084977 	Dec/23/2020 10:57UTC+8 	chenwz 	C - Cellular Automaton 	GNU C++11 	Accepted 	248 ms 	0 KB 
```

### 例题28  随机程序（Back to Kernighan-Ritchie, UVa 10828）

```cpp
// 例题28  随机程序（Back to Kernighan-Ritchie, UVa 10828）
// Rujia Liu
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;

const double eps = 1e-8;
const int NN = 100 + 10;
typedef double Matrix[NN][NN];

// 由于本题的特殊性，消元后不一定是对角阵，甚至不一定是阶梯阵
// 但若x[i]解惟一且有限，第i行除了A[i][i]和A[i][n]之外的其他元素均为0
void gauss_jordan(Matrix A, int n) {
  int i, j, k, r;
  for (i = 0; i < n; i++) {
    r = i;
    for (j = i + 1; j < n; j++)
      if (fabs(A[j][i]) > fabs(A[r][i])) r = j;
    if (fabs(A[r][i]) < eps) continue;  // 放弃这一行，直接处理下一行 (*)
    if (r != i)
      for (j = 0; j <= n; j++) swap(A[r][j], A[i][j]);

    // 与除了第i行外的其他行进行消元
    for (k = 0; k < n; k++)
      if (k != i)
        for (j = n; j >= i; j--) A[k][j] -= A[k][i] / A[i][i] * A[i][j];
  }
}

int main() {
  int d[NN], inf[NN];
  Matrix A;
  vector<int> pre[NN];
  for (int kase = 1, n; scanf("%d", &n) == 1 && n; kase++) {
    memset(d, 0, sizeof(d));
    for (int i = 0; i < n; i++) pre[i].clear();
    for (int a, b; scanf("%d%d", &a, &b) == 2 && a; pre[b].push_back(a))
      a--, b--, d[a]++;  // 改成从0开始编号, a的出度加1
    // 构造方程组
    memset(A, 0, sizeof(A));
    for (int i = 0; i < n; i++) {
      A[i][i] = 1;
      for (int j = 0; j < pre[i].size(); j++)
        A[i][pre[i][j]] -= 1.0 / d[pre[i][j]];
      if (i == 0) A[i][n] = 1;
    }

    // 解方程组，标记无穷变量
    gauss_jordan(A, n);
    memset(inf, 0, sizeof(inf));
    for (int i = n - 1; i >= 0; i--) {
      if (fabs(A[i][i]) < eps && fabs(A[i][n]) > eps)
        inf[i] = 1;  // 直接解出来的无穷变量
      for (int j = i + 1; j < n; j++)
        if (fabs(A[i][j]) > eps && inf[j])
          inf[i] = 1;  // 和无穷变量扯上关系的变量也是无穷的
    }

    int q, u;
    scanf("%d", &q);
    printf("Case #%d:\n", kase);
    while (q--) {
      scanf("%d", &u), u--;
      if (inf[u])
        printf("infinity\n");
      else
        printf("%.3lf\n", fabs(A[u][u]) < eps ? 0.0 : A[u][n] / A[u][u]);
    }
  }
  return 0;
}
// Accepted 20ms 2002 C++5.3.0 2020-12-12 21:41:59 25840104
```

### 例题26  递推关系（Recurrences, UVa 10870）

```cpp
// 例题26  递推关系（Recurrences, UVa 10870）
// 刘汝佳
#include <cstring>
#include <iostream>
#include <string>
using namespace std;

const int NN = 20;
typedef long long Matrix[NN][NN];
typedef long long Vector[NN];

int sz, mod;
void matrix_mul(Matrix A, Matrix B, Matrix res) {
  Matrix C;
  memset(C, 0, sizeof(C));
  for (int i = 0; i < sz; i++)
    for (int j = 0; j < sz; j++)
      for (int k = 0; k < sz; k++)
        C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod;
  memcpy(res, C, sizeof(C));
}

void matrix_pow(Matrix A, int n, Matrix res) {
  Matrix a, r;
  memcpy(a, A, sizeof(a)), memset(r, 0, sizeof(r));
  for (int i = 0; i < sz; i++) r[i][i] = 1;
  while (n) {
    if (n & 1) matrix_mul(r, a, r);
    n >>= 1;
    matrix_mul(a, a, a);
  }
  memcpy(res, r, sizeof(r));
}

void transform(Vector d, Matrix A, Vector res) {
  Vector r;
  memset(r, 0, sizeof(r));
  for (int i = 0; i < sz; i++)
    for (int j = 0; j < sz; j++) r[j] = (r[j] + d[i] * A[i][j]) % mod;
  memcpy(res, r, sizeof(r));
}

int main() {
  for (int d, n, m; cin >> d >> n >> m && d;) {
    Matrix A;
    Vector a, f;
    for (int i = 0; i < d; i++) cin >> a[i], a[i] %= m;
    for (int i = d - 1; i >= 0; i--) cin >> f[i], f[i] %= m;
    memset(A, 0, sizeof(A));
    for (int i = 0; i < d; i++) A[i][0] = a[i];
    for (int i = 1; i < d; i++) A[i - 1][i] = 1;
    sz = d, mod = m;
    matrix_pow(A, n - d, A);
    transform(f, A, f);
    cout << f[0] << endl;
  }
  return 0;
}
// 25839977 10870 Recurrences Accepted C++ 0.030 2020-12-12 13:16:01
```

### 例题29  乘积是平方数（Square, UVa 11542）

```cpp
// 例题29  乘积是平方数（Square, UVa 11542）
// Rujia Liu
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <vector>
using namespace std;

const int NN = 500 + 10, maxp = 100;
int vis[NN], prime[maxp];
int gen_primes(int n) {
  int m = (int)sqrt(n + 0.5);
  fill_n(vis, NN, 0);
  for (int i = 2; i <= m; i++)
    if (!vis[i])
      for (int j = i * i; j <= n; j += i) vis[j] = 1;
  int c = 0;
  for (int i = 2; i <= n; i++)
    if (!vis[i]) prime[c++] = i;
  return c;
}

typedef int Matrix[NN][NN];

// m个方程，n个变量
int get_rank(Matrix A, int m, int n) {
  int i = 0, j = 0, k, r, u;
  while (i < m && j < n) {  // 当前正在处理第i个方程，第j个变量
    r = i;
    for (k = i; k < m; k++)
      if (A[k][j]) {
        r = k;
        break;
      }
    if (A[r][j]) {
      if (r != i)
        for (k = 0; k <= n; k++) swap(A[r][k], A[i][k]);
      // 消元后第i行的第一个非0列是第j列，且第u>i行的第j列均为0
      for (u = i + 1; u < m; u++)
        if (A[u][j])
          for (k = i; k <= n; k++) A[u][k] ^= A[i][k];
      i++;
    }
    j++;
  }
  return i;
}

Matrix A;

int main() {
  int m = gen_primes(500), T;
  cin >> T;
  while (T--) {
    int n, maxp = 0;
    long long x;  // 注意x的范围
    cin >> n;
    memset(A, 0, sizeof(A));
    for (int i = 0; i < n; i++) {
      cin >> x;
      for (int j = 0; j < m; j++)  // 求x中的prime[j]的幂，并更新系数矩阵
        while (x % prime[j] == 0)
          maxp = max(maxp, j), x /= prime[j], A[j][i] ^= 1;
    }
    int r = get_rank(A, maxp + 1, n);      // 只用到了前maxp+1个素数
    cout << (1LL << (n - r)) - 1 << endl;  // 空集不是解，所以要减1
  }
  return 0;
}
// Accepted 1573 C++ 5.3.0 2020-12-12 21:46:13 25840133
```

## 2.8 快速傅里叶变换（FFT）

### 例题33  等差数列（Arithmetic Progressions, CodeChef COUNTARI）

```cpp
// 例题33  等差数列（Arithmetic Progressions, CodeChef COUNTARI）
// 陈锋
#include <vector>
#include <iostream>
#include <cmath>
#include <complex>
#define _for(i,a,b) for( int i=(a); i<(b); ++i)
using namespace std;
typedef long long LL;
typedef complex<double> Cplx;  // 复数 x + i*y
template<size_t N> // 多项式的阶
struct FFT {
  const double PI = acos(-1);
  Cplx Epsilon[N], Arti_Epsilon[N]; // FFT和插值运算FFT所用的(w_n)^k
  void slice_vec(const vector<Cplx>& v, int start, int step, vector<Cplx> &ans) {
    ans.clear();
    for (size_t i = start; i < v.size(); i += step) ans.push_back(v[i]);
  }
  void rec_fft_impl(vector<Cplx>& A, int n, int level, const Cplx* EP) {
    int m = n / 2;
    if (n == 1) return;
    vector<Cplx> A0, A1;
    slice_vec(A, 0, 2, A0), slice_vec(A, 1, 2, A1);
    rec_fft_impl(A0, m, level + 1, EP), rec_fft_impl(A1, m, level + 1, EP);
    _for(k, 0, m) {
      A[k] = A0[k] + EP[k * (1 << level)] * A1[k];
      A[k + m] = A0[k] - EP[k * (1 << level)] * A1[k];
    }
  }
  // 提前计算所有的(w_n)^k，提升递归fft的运行时间，免得每一层重复计算
  void init_fft(int n) {
    double theta = 2.0 * PI / n;
    _for(i, 0, n) {
      Epsilon[i] = Cplx(cos(theta * i), sin(theta * i));  // (w_n)^i
      Arti_Epsilon[i] =  conj(Epsilon[i]); // 共轭复数
    }
  }
  void idft(vector<Cplx>& A, int n) {  // DFT^(-1)，从y求a
    rec_fft_impl(A, n, 0, Arti_Epsilon);
    for (size_t i = 0; i < A.size(); i++) A[i] /= n;
  }
  void dft(vector<Cplx>& A, int n) { rec_fft_impl(A, n, 0, Epsilon); }
};
const int N2 = 65536, MAXA = 30000, BLK_CNT = 30, MAXN = 1e5 + 4;
FFT<N2> solver;
vector<int> A(MAXN);
vector<Cplx> A1(N2), A2(N2);
vector<LL> PREV(N2, 0ll), NEXT(N2, 0ll), INSIDE(N2);
int main() {
  int N; scanf("%d", &N);
  _for(i, 0, N) scanf("%d", &(A[i])), A[i]--, NEXT[A[i]]++;
  solver.init_fft(N2); // 初始化所有的单位根
  LL ans = 0;
  int BLK_SZ = (N + BLK_CNT - 1) / BLK_CNT; /* 每个BLOCK的大小 */
  _for(bi, 0, BLK_CNT) {
    int L = bi * BLK_SZ, R = min((bi + 1) * BLK_SZ, N);
    _for(i, L, R) NEXT[A[i]]--;
    fill(INSIDE.begin(), INSIDE.end(), 0);
    _for(i, L, R) { /* 至少两个元素在这个Block内，且三个元素都不相等 */
      _for(j, i + 1, R) if (A[j] != A[i]) {
        int AK = 2 * A[i] - A[j];
        if (0 <= AK && AK < MAXA) ans += PREV[AK] + INSIDE[AK]; /* 考虑后两个元素是Ai和Aj */
        AK = 2 * A[j] - A[i]; /* 考虑前两个元素是Ai和Aj，则后一个元素必然在NEXT，
                    后一个元素在INSIDE的情况已经在上面考虑过了 */
        if (0 <= AK && AK < MAXA) ans += NEXT[AK];
      }
      INSIDE[A[i]]++;
    }
    _for(ak, 0, MAXA) { /* 三个元素相等=ak的情况 */
      LL ki = INSIDE[ak];
      ans += ki * (ki - 1) / 2 * (PREV[ak] + NEXT[ak]); // 两个元素在Block内 C(ki, 2) * (PREV + NEXT)
      ans += ki * (ki - 1) * (ki - 2) / 6; // 三个元素都在Block内 C(ki, 3)
    }
    if (bi > 0 && bi + 1 < BLK_CNT) { /* 只有中间元素在当前Block内 */
      _for(i, 0, N2) A1[i] = Cplx(PREV[i], 0), A2[i] = Cplx(NEXT[i], 0);
      solver.dft(A1, N2), solver.dft(A2, N2);
      for (size_t i = 0; i < A1.size(); i++) A1[i] *= A2[i];
      solver.idft(A1, N2); // 卷积计算，计算分别位于Prev和Next内的两个和为2*ak的情况
      _for(ak, 0, MAXA) ans += INSIDE[ak] * llrint(A1[2 * ak].real());
    }

    _for(i, L, R) PREV[A[i]]++;
  }
  printf("%lld\n", ans);
  return 0;
}
// 11275383 2 min ago   sukhoeing       1.99    3.2M    C++14
```

### 例题34  多项式求值（Evaluate the polynomial, CodeChef POLYEVAL）

```cpp
// 例题34  多项式求值（Evaluate the polynomial, CodeChef POLYEVAL）
// 陈锋
#include <bits/stdc++.h>
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
using namespace std;
typedef long long LL;
const int MOD = 786433, K = 1 << 18, w = 1000;
typedef vector<int> IVec;
int add_mod(int a, int b) {
  LL ret = a + b;
  while (ret < 0) ret += MOD;
  return ret % MOD;
}
int mul_mod(int a, int b) { return (((LL)a) * b) % MOD; }
int pow_mod(int a, int b) {
  LL ans = 1;
  while (b > 0) {
    if (b & 1) ans = mul_mod(ans, a);
    a = mul_mod(a, a);
    b /= 2;
  }
  return ans;
}
int getGen(int P) {  // 原根
  unordered_set<int> set;
  _for(g, 1, P) {
    set.clear();
    int pm = g;
    _for(ex, 1, P) {
      if (set.count(pm)) break;
      set.insert(pm);
      pm = (pm * g) % P;
    }
    if (set.size() == MOD - 1) {  // 找到原根了
      assert(pm == g);
      return g;
    }
  }
  return -1;
}
int eval(const IVec& A, int x) {  // 求A(x)
  int ans = 0, cur = 1;
  for (size_t i = 0; i < A.size(); i++)
    ans = add_mod(ans, mul_mod(A[i], cur)), cur = mul_mod(cur, x);
  return ans;
}
IVec slice_vec(const IVec& vec, int start, int step) {
  IVec ans;
  for (size_t i = start; i < vec.size(); i += step) ans.push_back(vec[i]);
  return ans;
}
// 对于多项式A(x), 使用{w^0, w^1, w^(K-1)}做DFT(数论模运算)
IVec NTT(const IVec& A, const IVec& W, int level = 1) {
  int n = W.size() / level, m = n / 2, An = A.size();
  IVec ans(n, 0);
  if (An < 1) return ans;
  if (n <= 2) {
    _for(i, 0, n) ans[i] = eval(A, W[level * i]);
    return ans;
  }
  const IVec &A0 = NTT(slice_vec(A, 0, 2), W, level * 2),
              &A1 = NTT(slice_vec(A, 1, 2), W, level * 2);
  _for(i, 0, n) ans[i] = add_mod(A0[i % m], mul_mod(W[level * i], A1[i % m]));
  return ans;
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  const int g = getGen(MOD);
  int n;
  cin >> n;
  n++;
  IVec A(n), ans(MOD), W(K), B(n);
  _for(i, 0, n) cin >> A[i];
  _for(i, 0, K) W[i] = pow_mod(w, i);
  _rep(c, 0, 2) {
    _for(i, 0, n) B[i] = mul_mod(A[i], pow_mod(g, c * i));
    const IVec& Y = NTT(B, W);
    _for(i, 0, K) ans[mul_mod(pow_mod(g, c), W[i])] = Y[i];
  }
  ans[0] = A[0];
  int Q, x;
  cin >> Q;
  while (Q--) cin >> x, cout << ans[x] << endl;
  return 0;
}
// Accepted 1520ms 25292kB 2222 C++14(gcc 6.3)2020-12-12 21:56:24 40368549
```

### 例题31  高尔夫机器人（Golf Bot, SWERC 2014, LA6886）

```cpp
// 例题31  高尔夫机器人（Golf Bot, SWERC 2014, LA6886）
// 陈锋
#include <vector>
#include <iostream>
#include <cmath>
#include <complex>
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
using namespace std;
typedef complex<double> Cplx;  // 复数 x + i*y
template<size_t N> // 多项式的阶
struct FFT {
  const double PI = acos(-1);
  Cplx Epsilon[N], Arti_Epsilon[N]; // FFT和插值运算FFT所用的(w_n)^k
  void slice_vec(const vector<Cplx>& v, int start, int step, vector<Cplx> &ans) {
    ans.clear();
    for (size_t i = start; i < v.size(); i += step) ans.push_back(v[i]);
  }
  void rec_fft_impl(vector<Cplx>& A, int n, int level, const Cplx* EP) {
    int m = n / 2;
    if (n == 1) return;
    vector<Cplx> A0, A1;
    slice_vec(A, 0, 2, A0), slice_vec(A, 1, 2, A1);
    rec_fft_impl(A0, m, level + 1, EP), rec_fft_impl(A1, m, level + 1, EP);
    _for(k, 0, m) {
      A[k] = A0[k] + EP[k * (1 << level)] * A1[k];
      A[k + m] = A0[k] - EP[k * (1 << level)] * A1[k];
    }
  }
  // 提前计算所有的(w_n)^k，提升递归fft的运行时间，免得每一层重复计算
  void init_fft(int n) {
    double theta = 2.0 * PI / n;
    _for(i, 0, n) {
      Epsilon[i] = Cplx(cos(theta * i), sin(theta * i));  // (w_n)^i
      Arti_Epsilon[i] =  conj(Epsilon[i]); // 共轭复数
    }
  }
  void idft(vector<Cplx>& A, int n) {  // DFT^(-1)，从y求a
    rec_fft_impl(A, n, 0, Arti_Epsilon);
    for (size_t i = 0; i < A.size(); i++) A[i] /= n;
  }
  void dft(vector<Cplx>& A, int n) { rec_fft_impl(A, n, 0, Epsilon); }
};

const double EPS = 1e-8;
const int MAXN = 1 << 18;  // 262144;
FFT<MAXN * 2> solver;
int main() {
  vector<int> A(MAXN);
  vector<Cplx> F(MAXN * 2);
  for (int n, M, x; scanf("%d", &n) == 1 && n;) {
    int N = 1;
    _for(i, 0, n) {
      scanf("%d", &(A[i]));
      while (A[i] >= N) N *= 2;
    } // N是 > max(A[i])的2的幂
    N *= 2, fill_n(F.begin(), N, Cplx());
    F[0].real(1);
    _for(i, 0, n) F[A[i]] = 1;
    solver.init_fft(N), solver.dft(F, N);
    for (int i = 0; i < N; i++) F[i] *= F[i];
    solver.idft(F, N);
    int ans = 0; scanf("%d", &M);
    _for(i, 0, M) {
      scanf("%d", &x);
      if (x < N && fabs(F[x].real()) > EPS) ans++;
    }
    printf("%d\n", ans);
  }
  return 0;
}
/*
算法分析请参考: 《入门经典训练指南-升级版》2.8节 例题31
*/
// Accepted 1010ms 46080kB 2618 C++14(gcc 8.3)2020-12-12 21:51:34 27085962
```

### 例题32  瓷砖切割（Tile Cutting, World Finals 2007 LA7159）

```cpp
// 例题32  瓷砖切割（Tile Cutting, World Finals 2007 LA7159）
// 陈锋
#include <bits/stdc++.h>
#define _for(i,a,b) for( int i=(a); i<(b); ++i)
#define _rep(i,a,b) for( int i=(a); i<=(b); ++i)
using namespace std;
typedef long long LL;

typedef complex<double> Cplx;  // 复数 x + i*y
template<size_t N> // 多项式次数*2
struct FFT {
  const double PI = acos(-1);
  Cplx Epsilon[N], Arti_Epsilon[N]; // FFT和插值运算FFT所用的(w_n)^k
  void slice_vec(const vector<Cplx>& v, int start, int step, vector<Cplx> &ans) {
    ans.clear();
    for (size_t i = start; i < v.size(); i += step) ans.push_back(v[i]);
  }
  void rec_fft_impl(vector<Cplx>& A, int n, int level, const Cplx* EP) {
    int m = n / 2;
    if (n == 1) return;
    vector<Cplx> A0, A1;
    slice_vec(A, 0, 2, A0), slice_vec(A, 1, 2, A1);
    rec_fft_impl(A0, m, level + 1, EP), rec_fft_impl(A1, m, level + 1, EP);
    _for(k, 0, m) {
      A[k] = A0[k] + EP[k * (1 << level)] * A1[k];
      A[k + m] = A0[k] - EP[k * (1 << level)] * A1[k];
    }
  }
  // 提前计算所有的(w_n)^k，提升递归fft的运行时间，免得每一层重复计算
  void init_fft(int n) {
    double theta = 2.0 * PI / n;
    _for(i, 0, n) {
      Epsilon[i] = Cplx(cos(theta * i), sin(theta * i));  // (w_n)^i
      Arti_Epsilon[i] =  conj(Epsilon[i]); // 共轭复数
    }
  }
  void idft(vector<Cplx>& A, int n) {  // DFT^(-1)，从y求a
    rec_fft_impl(A, n, 0, Arti_Epsilon);
    for (size_t i = 0; i < A.size(); i++) A[i] /= n;
  }
  void dft(vector<Cplx>& A, int n) { rec_fft_impl(A, n, 0, Epsilon); }
};

const double EPS = 1e-6;
const int MAXA = 1 << 19, N2 = 1 << 20; // 524288;
FFT<N2> solver;

int main() {
  vector<LL> C(N2, 0LL);
  vector<Cplx> F(N2);
  for (LL a = 1; a < MAXA; a++)
    for (LL b = 1; a * b < MAXA; b++) C[a * b]++;
  _for(i, 0, N2) F[i] = Cplx(C[i], 0);
  solver.init_fft(N2), solver.dft(F, N2);
  for (int i = 0; i < N2; i++) F[i] *= F[i];
  solver.idft(F, N2);
  int n; scanf("%d", &n);
  _for(i, 0, n) {
    LL maxW = -1; int al, ah, ans = 0;
    scanf("%d%d", &al, &ah); assert(al <= ah);
    for (int a = al; a <= ah; a++) {
      LL w = llround(F[a].real());
      if (w > maxW) ans = a, maxW = w;
    }
    printf("%d %lld\n", ans, maxW);
  }
  return 0;
}
// Accepted 780ms  2504  C++  2021-04-0416:10:15            7107540
```

### 例题30  超级扑克II（Super Joker II, UVa 12298）

```cpp
// 例题30  超级扑克II（Super Joker II, UVa 12298）
// Rujia Liu
#include <complex>
#include <cmath>
#include <vector>
using namespace std;

const long double PI = acos(0.0) * 2.0;

typedef complex<double> CD;

// Cooley-Tukey的FFT算法，迭代实现。inverse = false时计算逆FFT
inline void FFT(vector<CD> &a, bool inverse) {
  int n = a.size();
  // 原地快速bit reversal
  for(int i = 0, j = 0; i < n; i++) {
    if(j > i) swap(a[i], a[j]);
    int k = n;
    while(j & (k >>= 1)) j &= ~k;
    j |= k;
  }

  double pi = inverse ? -PI : PI;
  for(int step = 1; step < n; step <<= 1) {
    // 把每相邻两个“step点DFT”通过一系列蝴蝶操作合并为一个“2*step点DFT”
    double alpha = pi / step;
    // 为求高效，我们并不是依次执行各个完整的DFT合并，而是枚举下标k
    // 对于一个下标k，执行所有DFT合并中该下标对应的蝴蝶操作，即通过E[k]和O[k]计算X[k]
    // 蝴蝶操作参考：http://en.wikipedia.org/wiki/Butterfly_diagram
    for(int k = 0; k < step; k++) {
      // 计算omega^k. 这个方法效率低，但如果用每次乘omega的方法递推会有精度问题。
      // 有更快更精确的递推方法，为了清晰起见这里略去
      CD omegak = exp(CD(0, alpha*k)); 
      for(int Ek = k; Ek < n; Ek += step << 1) { // Ek是某次DFT合并中E[k]在原始序列中的下标
        int Ok = Ek + step; // Ok是该DFT合并中O[k]在原始序列中的下标
        CD t = omegak * a[Ok]; // 蝴蝶操作：x1 * omega^k
        a[Ok] = a[Ek] - t;  // 蝴蝶操作：y1 = x0 - t
        a[Ek] += t;         // 蝴蝶操作：y0 = x0 + t
      }
    }
  }

  if(inverse)
    for(int i = 0; i < n; i++) a[i] /= n;
}

// 用FFT实现的快速多项式乘法
inline vector<double> operator * (const vector<double>& v1, const vector<double>& v2) {
  int s1 = v1.size(), s2 = v2.size(), S = 2;
  while(S < s1 + s2) S <<= 1;
  vector<CD> a(S,0), b(S,0); // 把FFT的输入长度补成2的幂，不小于v1和v2的长度之和
  for(int i = 0; i < s1; i++) a[i] = v1[i];
  FFT(a, false);
  for(int i = 0; i < s2; i++) b[i] = v2[i];
  FFT(b, false);
  for(int i = 0; i < S; i++) a[i] *= b[i];
  FFT(a, true);
  vector<double> res(s1 + s2 - 1);
  for(int i = 0; i < s1 + s2 - 1; i++) res[i] = a[i].real(); // 虚部均为0
  return res;
}

/////////// 题目相关
#include<cstdio>
#include<cstring>
const int maxn = 50000 + 10;

int composite[maxn];
void sieve(int n) {
  int m = (int)sqrt(n+0.5);
  memset(composite, 0, sizeof(composite));
  for(int i = 2; i <= m; i++) if(!composite[i])
    for(int j = i*i; j <= n; j+=i) composite[j] = 1;
}

const char* suites = "SHCD";
int idx(char suit) {
  return strchr(suites, suit) - suites;
}

int lost[4][maxn];
int main(int argc, char *argv[]) {
  sieve(50000);
  int a, b, c;
  while(scanf("%d%d%d", &a, &b, &c) == 3 && a) {
    memset(lost, 0, sizeof(lost));
    for(int i = 0; i < c; i++) {
      int d; char s;
      scanf("%d%c", &d, &s);
      lost[idx(s)][d] = 1;
    }   
    vector<double> ans(1,1), poly;
    for(int s = 0; s < 4; s++) {
      poly.clear();
      poly.resize(b+1, 0);
      for(int i = 4; i <= b; i++)
        if(composite[i] && !lost[s][i]) poly[i] = 1.0;
      ans = ans * poly;
      ans.resize(b+1);
    }
    for(int i = a; i <= b; i++)
      printf("%.0lf\n", fabs(ans[i]));    
    printf("\n");
  }
  return 0;
}
// 25877111  12298  Super Poker II  Accepted  C++  0.170  2020-12-23 03:00:11
```

### 例题35  异或路径(XOR Path, ACM/ICPC, Asia-Dhaka 2017, UVa13277)

```cpp
// 例题35  异或路径(XOR Path, ACM/ICPC, Asia-Dhaka 2017, UVa13277)
// 陈锋
#include <bits/stdc++.h>

using namespace std;
typedef long long LL;
static const int maxn = 1e5 + 5, N = 1 << 16;
template <typename T = int>
struct FWT {
  void fwt(T A[], int n) {
    for (int d = 1; d < n; d <<= 1) {
      for (int i = 0, m = d << 1; i < n; i += m) {
        for (int j = 0; j < d; j++) {
          T x = A[i + j], y = A[i + j + d];
          A[i + j] = (x + y), A[i + j + d] = (x - y); // xor
          //A[i+j] = x+y;                     // and
          //A[i+j+d] = x+y;                   // or
        }
      }
    }
  }
  void ufwt(T A[], int n)  {
    for (int d = 1; d < n; d <<= 1)    {
      for (int i = 0, m = d << 1; i < n; i += m) {
        for (int j = 0; j < d; j++) {
          T x = A[i + j], y = A[i + j + d];
          A[i + j] = (x + y) >> 1, A[i + j + d] = (x - y) >> 1; // xor
          //A[i+j] = x-y;                          // and
          //A[i+j+d] = y-x;                        // or
        }
      }
    }
  }

  void conv(T a[], T b[], int n)  {
    fwt(a, n), fwt(b, n);
    for (int i = 0; i < n; i++) a[i] = a[i] * b[i];
    ufwt(a, n);
  }

  void self_conv(T a[], int n) {
    fwt(a, n);
    for (int i = 0; i < n; i++) a[i] = a[i] * a[i];
    ufwt(a, n);
  }
};

struct Edge {
  int v, w;
  Edge(int _v = 0, int _w = 0) : v(_v), w(_w) {}
};

vector<Edge> G[maxn];
FWT<LL> fwt;
LL A[N + 5];
void dfs(int u, int p = -1, int x = 0) {
  A[x]++;
  for (auto &e : G[u]) if (e.v != p) dfs(e.v, u, x ^ e.w);
}

int main() {
  int T; scanf("%d", &T);
  for (int t = 1, n; t <= T; t++) {
    scanf("%d", &n);
    for (int i = 0; i <= n; i++) G[i].clear();
    fill(begin(A), end(A), 0);
    for (int e = 1, u, v, w; e < n; e++) {
      scanf("%d %d %d", &u, &v, &w);
      G[u].push_back(Edge(v, w)), G[v].push_back(Edge(u, w));
    }
    dfs(1);
    fwt.self_conv(A, N);
    printf("Case %d:\n", t);
    printf("%lld\n", (A[0] - n) / 2);
    for (int i = 1; i < (1 << 16); i++) printf("%lld\n", A[i] / 2);
  }
}
// 24926296 13277 XOR Path  Accepted  C++11 0.350 2020-04-24 15:32:51
```

## 2.9 数值方法简介

### 例题37  误差曲线（Error Curves, Chengdu 2010, LA5009）

```cpp
// 例题37  误差曲线（Error Curves, Chengdu 2010, LA5009）
// 刘汝佳
#include <algorithm>
#include <cstdio>
using namespace std;
const int NN = 10000 + 10;
int T, n, a[NN], b[NN], c[NN];
double F(double x) {
  double ans = a[0] * x * x + b[0] * x + c[0];
  for (int i = 1; i < n; i++) ans = max(ans, a[i] * x * x + b[i] * x + c[i]);
  return ans;
}

int main() {
  scanf("%d", &T);
  while (T--) {
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d%d%d", &a[i], &b[i], &c[i]);
    double L = 0.0, R = 1000.0;
    for (int i = 0; i < 100; i++) {
      double m1 = L + (R - L) / 3, m2 = R - (R - L) / 3;
      if (F(m1) < F(m2)) R = m2;
      else L = m1;
    }
    printf("%.4lf\n", F(L));
  }
  return 0;
}
// 34852546 2020-12-12 22:21:37 Accepted 3714 280MS 1344K 686 B G++
```

### 例题36  解方程（Solve It!, UVa 10341）

```cpp
// 例题36  解方程（Solve It!, UVa 10341）
// 刘汝佳
#include<cstdio>
#include<cmath>
#include <iostream>
#define F(x) (p*exp(-x)+q*sin(x)+r*cos(x)+s*tan(x)+t*(x)*(x)+u)
using namespace std;
const double eps = 1e-14;
int main() {
  for(int p, r, q, s, t, u; cin>>p>>q>>r>>s>>t>>u; ) {
    double f0 = F(0), f1 = F(1);
    if(f1 > eps || f0 < -eps) {
      puts("No solution");
      continue;
    }
    double x = 0, y = 1, m;
    for(int i = 0; i < 100; i++) {
      m = x + (y-x)/2;
      if(F(m) < 0) y = m; else x = m;
    }
    printf("%.4lf\n", m);
  }
  return 0;
}
// Accepted 10ms 548 C++5.3.0 2020-12-12 22:18:30 25840322
```

### 例题38  桥上的绳索（Bridge, Hangzhou 2005, UVa1356）

```cpp
// 例题38  桥上的绳索（Bridge, Hangzhou 2005, UVa1356）
// 刘汝佳
#include <cmath>
#include <cstdio>

// sqrt(a^2+x^2)的原函数
double F(double a, double x) {
  double a2 = a * a, x2 = x * x;
  return (x * sqrt(a2 + x2) + a2 * log(fabs(x + sqrt(a2 + x2)))) / 2;
}

// 宽度为w，高度为h的抛物线长度，也就是前文中的p(w,h)
double parabola_arc_length(double w, double h) {
  double a = 4.0 * h / (w * w), b = 1.0 / (2 * a);
  // 如果不用对称性，就是(F(b,w/2)-F(b,-w/2))*2*a
  return (F(b, w / 2) - F(b, 0)) * 4 * a;
}

int main() {
  int T;
  scanf("%d", &T);
  for (int kase = 1, D, H, B, L; kase <= T; kase++) {
    scanf("%d%d%d%d", &D, &H, &B, &L);
    int n = (B + D - 1) / D;  // 间隔数
    double D1 = (double)B / n, L1 = (double)L / n, x = 0, y = H;
    while (y - x > 1e-5) {  // 二分法求解高度
      double m = x + (y - x) / 2;
      if (parabola_arc_length(D1, m) < L1) x = m;
      else y = m;
    }
    if (kase > 1) puts("");
    printf("Case %d:\n%.2lf\n", kase, H - x);
  }
  return 0;
}
// 25877139 	1356 	Bridge 	Accepted 	C++ 	0.000 	2020-12-23 03:17:10
```
