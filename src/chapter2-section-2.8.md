# 2.8 快速傅里叶变换（FFT）

## 例题33  等差数列（Arithmetic Progressions, CodeChef COUNTARI）

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

## 例题34  多项式求值（Evaluate the polynomial, CodeChef POLYEVAL）

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

## 例题31  高尔夫机器人（Golf Bot, SWERC 2014, LA6886）

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

## 例题32  瓷砖切割（Tile Cutting, World Finals 2007 LA7159）

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

## 例题30  超级扑克II（Super Joker II, UVa 12298）

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

## 例题35  异或路径(XOR Path, ACM/ICPC, Asia-Dhaka 2017, UVa13277)

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
