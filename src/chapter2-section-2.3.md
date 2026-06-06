# 2.3 数论

## 例题14  墨菲斯（Mophues, ACM/ICPC Asia Regional Hangzhou Online 2013, HDU4746）

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

## 例题15  数一数a x b（Count a x b, ACM/ICPC Changchun 2015, LA7184/HDU5528）

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

## 例题12  可怕的诗篇（A Horrible Poem，POI2012）

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

## 例题13  可见格点（Visible Lattice Points, Indian ICPC training camp, SPOJ VLATTICE）

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

## 例题8  总是整数（Always an Integer, World Finals 2008, UVa1069）

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

## 例题9  最大公约数之和——极限版II（GCD Extreme(II), UVa 11426）

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

## 例题10  数论难题（Code Feat, UVa 11754）

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

## 例题11  网格涂色（Emoogle Grid, UVa 11916）

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
