# 2.8 快速傅里叶变换（FFT）

## 例题33  等差数列（Arithmetic Progressions, CodeChef COUNTARI）

### 题目描述
给定一个长度为N的数组A（N ≤ 10^5，0 < A[i] < 30000），求满足0 ≤ i < j < k < N且A[j]-A[i] = A[k]-A[j]（即A[i], A[j], A[k]成等差数列）的三元组(i,j,k)的个数。

**输入**：第一行N。第二行N个整数。

**输出**：一个整数，表示等差数列三元组的个数。

### 解题思路

**分块+FFT**：
条件A[j]-A[i] = A[k]-A[j] 等价于 A[i] + A[k] = 2·A[j]。

将数组分为若干块，每个块大小为BLK_SZ ≈ N/30。

对于每个中间块（块号bi），考虑以该块中的元素作为中间元素A[j]的三元组：
1. 左侧已处理元素（prev）和右侧未处理元素（next）作为A[i]和A[k]
2. 块内元素之间的配对

**块处理流程**：
- 预处理NEXT数组统计块右侧的频次
- 对于块bi内的每个j和i：
  - 情况1：A[i]在prev, A[j]在块内, A[k]在next → ans += prev[2·A[j]-A[i]]
  - 情况2：A[i]在prev, A[j]在块内, A[k]在块内 → ans += INSIDE[2·A[j]-A[i]]
  - 情况3：A[i]在块内, A[j]在块内, A[k]在next → ans += next[2·A[j]-A[i]]
- 对于每个块，使用FFT做卷积：
  conv(prev, next) → 结果中位置2·ak的值 = Σ prev[i]·next[2·ak-i]
  即prev和next中各取一个和为2·ak的方案数
- 处理该块后，将块内元素加入prev

**FFT卷积**：
将prev数组和next数组作为多项式系数，做FFT乘法。卷积结果的第t项代表prev[x]和next[y]满足x+y=t的方案数之和。对于每个中间值ak，ans += INSIDE[ak] * conv_result[2·ak]。

### 算法方法
- **FFT/卷积**：大规模卷积加速计数
- **分块**：将暴力的O(N²)降低为O(BLK_CNT·N + BLK_CNT·N·log N)

### 复杂度分析
- **时间复杂度**：O(BLK_CNT·(BLK_SZ² + N log N))，BLK_CNT=30, BLK_SZ=N/30
- **空间复杂度**：O(N)，FFT临时数组

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
typedef complex<double> Cplx;  // 复数类型 x + i*y

// FFT模板：N为多项式的阶（必须是2的幂）
template<size_t N>
struct FFT {
  const double PI = acos(-1);
  Cplx Epsilon[N], Arti_Epsilon[N]; // DFT和IDFT所用的ω_n^k及其共轭

  // 从向量v中提取步长为step的子序列（用于奇偶分治）
  void slice_vec(const vector<Cplx>& v, int start, int step, vector<Cplx> &ans) {
    ans.clear();
    for (size_t i = start; i < v.size(); i += step) ans.push_back(v[i]);
  }

  // 递归FFT实现
  void rec_fft_impl(vector<Cplx>& A, int n, int level, const Cplx* EP) {
    int m = n / 2;
    if (n == 1) return;  // 递归边界
    vector<Cplx> A0, A1;
    slice_vec(A, 0, 2, A0), slice_vec(A, 1, 2, A1);  // 分离奇数项和偶数项
    rec_fft_impl(A0, m, level + 1, EP), rec_fft_impl(A1, m, level + 1, EP);
    // 蝴蝶操作：合并两个子DFT
    _for(k, 0, m) {
      A[k] = A0[k] + EP[k * (1 << level)] * A1[k];       // y_k = E_k + ω_n^k · O_k
      A[k + m] = A0[k] - EP[k * (1 << level)] * A1[k];    // y_{k+m} = E_k - ω_n^k · O_k
    }
  }

  // 预计算所有单位根ω_n^i，避免递归过程中的重复计算
  void init_fft(int n) {
    double theta = 2.0 * PI / n;
    _for(i, 0, n) {
      Epsilon[i] = Cplx(cos(theta * i), sin(theta * i));   // ω_n^i
      Arti_Epsilon[i] = conj(Epsilon[i]);                   // ω_n^{-i} (共轭)
    }
  }

  void idft(vector<Cplx>& A, int n) {  // 逆DFT: 从频域恢复时域
    rec_fft_impl(A, n, 0, Arti_Epsilon);  // 用共轭单位根做FFT
    for (size_t i = 0; i < A.size(); i++) A[i] /= n;  // 归一化
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

### 题目描述
给定一个n次多项式A(x) = a_0 + a_1·x + … + a_n·x^n（模MOD=786433），和Q个询问，每个询问给一个x值，求A(x) mod MOD。n ≤ 10^5，Q ≤ 10^5。

MOD=786433是特殊的质数：MOD = 3·2^18 + 1 ，是一个NTT友好的质数（存在2^18次本原单位根）。

**输入**：第一行n。第二行n+1个系数。第三行Q，然后Q行每行一个x。

**输出**：对于每个询问，输出A(x) mod MOD。

### 解题思路

**NTT（数论变换）多点求值**：
利用质数MOD和原根g构造类似FFT的数论变换。

关键观察：MOD = 786433 = 3 · 2^18 + 1，g = 10是该模的原根。取w = g^3 = 1000（满足w的阶为2^18）。

将多项式A(x)计算在所有x = w^0, w^1, …, w^(K-1)上的值（K=2^18）。

**Chirp Z-Transform思想**：
为了计算在所有幂次上的值，可以利用性质：
x = g^c · w^i 对于c∈{0,1}覆盖了所有MOD的非零元。

A(g^c · w^i)的值可以通过NTT快速计算。

**实现步骤**：
1. 找到原根g=10
2. 计算w = g^3 = 1000
3. 对于c=0和c=1，分别对多项式B_c(x) = A(g^c·x)做NTT
4. NTT使用{w^0, w^1, …, w^(K-1)}作为求值点
5. 对于每个询问x，查表得到答案（x映射到相应的NTT结果位置）

### 算法方法
- **NTT/数论变换**：模质数上的FFT变体，使用原根代替复数单位根
- **多点求值**：使用NTT在一次变换中计算多个点的多项式值
- **原根/数论**：MOD=786433的原根性质

### 复杂度分析
- **时间复杂度**：O(K log K)，K=2^18。预处理2次NTT，查询O(1)
- **空间复杂度**：O(K)，NTT数组和答案表

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

### 题目描述
高尔夫机器人可以将球击出特定距离。已知机器人可以击出n种不同距离d_1, d_2, …, d_n（每种可以使用多次），以及m个目标距离t_1, …, t_m。问有多少个目标可以通过至多两次击球（一杆或两杆）达到。即判断每个目标距离t是否可以表示为d_i或d_i+d_j（1≤i,j≤n）。

**输入**：多组数据。每组第一行n。第二行n个整数d_i。第三行m。第四行m个整数t_j。n=0结束。

**输出**：对于每组数据，输出可达到的目标数。

### 解题思路

**FFT卷积**：
问题转化为判断每个t是否可以表示为不超过两个距离的和。

构造多项式F(x) = Σ x^{d_i}（即各项系数为1当且仅当该距离存在）。则F²(x)的系数表示距离之和的方案数。

具体步骤：
1. 构造系数数组，F[d_i]=1（还包括F[0]=1表示单杆击球）
2. 使用FFT计算F²
3. 对于每个目标距离t，检查F²[t]是否大于0（即存在d_i+d_j=t），或者F[t]=1（一杆即可）

**FFT实现**：
使用N=MAXN*2的FFT，MAXN是所有距离的最大值。注意需要加1处理precF[0]=1的情况（单杆=第一个杆+距离0）。

### 算法方法
- **FFT/卷积**：使用多项式乘法加速求和判断
- **0-1多项式**：距离存在记为系数1，卷积后非零系数表示可达距离

### 复杂度分析
- **时间复杂度**：O(N log N)，N是2的幂且≥2·max(d_i)
- **空间复杂度**：O(N)，FFT复数数组

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

### 题目描述
一个矩形的瓷砖可以沿平行于边的直线切割。对于给定面积的瓷砖（面积=a×b），不同的长宽组合(长,宽)对应不同的切割方案数（因为不同的(a,b)会导致切割线位置选择不同）。定义函数f(area) = Σ_{a·b=area} 1（即面积area的不同长方形表示方式数，有序对(a,b)）。

给定多个询问，每个询问给出一个面积区间[al, ah]，求该区间内f(area)最大的area值及对应的最大值。

**输入**：第一行n。接下来n行，每行al, ah（1 ≤ al ≤ ah ≤ 500000）。

**输出**：对于每个询问，输出面积和对应的最大f值。

### 解题思路

**FFT自卷积**：
定义c[a] = Σ_{b: a·b<MAXA} 1，即a作为因子之一能形成的面积个数。

则f(area) = Σ_{a·b=area} 1 = (c ∗ c)(area)，即c与自身的卷积。

使用FFT计算c的自卷积：F = fft(c)，G = F²，再逆FFT得到卷积结果。结果中位置area的值即为f(area)。

对于每个询问[al, ah]，区间内扫描找最大值。

**预计算c数组**：
对于每个a，枚举其倍数b（O(MAXA·log MAXA)），c[a·b]++。

### 算法方法
- **FFT/自卷积**：卷积计算因子对计数
- **调和级数枚举**：预处理因子对计数

### 复杂度分析
- **时间复杂度**：预处理O(MAXA·log MAXA + N·log N)，N=2^20；查询O(n·(ah-al))
- **空间复杂度**：O(N)，FFT数组

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

### 题目描述
有4种花色(S/H/C/D)的扑克牌，每种花色有编号为1到b的牌。但其中c张牌已丢失。现在需要从剩余的每种花色中各选一张牌组成一手牌（共4张），使得总点数在[a, b]范围内且每张牌的点数必须是合数（composite number，非素数非1）。问对于每个可能的点数总和s∈[a,b]，有多少种不同的选牌方式。

**输入**：多组数据。每组第一行a, b, c。接下来c行每行一个数字后跟一个字母（花色）。a=b=c=0结束。

**输出**：对于每组数据，按顺序输出每个s∈[a,b]对应的方案数，每组后跟一个空行。

### 解题思路

**FFT多项式乘法**：
每种花色对应一个多项式P_s(x) = Σ x^i，其中i是花色s中可用的合数牌点数。则总方案数由四个多项式的卷积给出：P_S × P_H × P_C × P_D。

使用FFT加速多项式乘法（先用FFT做前两个乘，再用FFT与后两个乘）。

步骤：
1. 预处理50000以内的合数
2. 对于每种花色，构造多项式（只包含未丢失的合数点数）
3. 四次多项式相乘：ans = P_S * P_H * P_C * P_D
4. 输出区间[a,b]的系数

**FFT实现**：
使用Cooley-Tukey迭代FFT算法。包括bit-reversal重排和蝴蝶操作。

### 算法方法
- **FFT/多项式乘法**：用FFT加速大次数多项式卷积
- **筛法**：埃氏筛生成合数表

### 复杂度分析
- **时间复杂度**：O(b log b)，b≤50000
- **空间复杂度**：O(b)，FFT数组

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

### 题目描述
给定一棵n个节点的树，每条边有权值。定义节点u到v的异或路径值为路径上所有边的权值异或和。问有多少对不同的(u,v)（无序对）使得异或路径值等于k，对于所有k∈[0,2^16)。输出所有k对应的无序对个数。

**输入**：第一行T。每组第一行n。接下来n-1行每行u,v,w（一条边连接u和v，权值w）。1≤n≤10^5，0≤w<2^16。

**输出**：对于每组数据，输出"Case X:"，然后对于k=0到2^16-1，每行一个整数表示异或路径值为k的无序对个数。

### 解题思路

**树路径异或和转根异或和**：
定义X[u]为根(节点1)到节点u的路径异或和。则u到v的异或路径值 = X[u] ^ X[v]（因为根到LCA的路径被异或两次抵消）。

问题转化为数组X中两两异或值的分布。

**FWT（快速沃尔什-哈达玛变换）**：
异或卷积：定义A为X值的频次数组（A[t] = 异或和为t的节点数）。则A的自异或卷积结果B = A ⊕ A：
B[k] = Σ_{i⊕j=k} A[i]·A[j]

这恰好表示两两节点异或值为k的对数（有序对）。无序对需要除以2，且要去掉u=v的情况（i⊕i=0）。

**FWT变换过程（异或卷积）**：
正变换：对于长度d的步长，对每对(A[i+j], A[i+j+d])做蝴蝶变换：
- 新值：x' = x + y, y' = x - y
逆变换：x' = (x + y)/2, y' = (x - y)/2

### 算法方法
- **FWT（快速沃尔什变换）**：异或版本的卷积变换
- **树DFS**：计算根异或和
- **组合计数**：自卷积计算两两异或分布

### 复杂度分析
- **时间复杂度**：O(N log N + n)，N=2^16，FWT O(N log N)，DFS O(n)
- **空间复杂度**：O(N)，频次数组和FWT数组

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
