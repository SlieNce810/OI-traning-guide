# 2.7 矩阵和线性方程组

## 例题27  细胞自动机（Cellular Automaton, NEERC 2006, Codeforces Gym100287C）

### 题目描述
有一个环形排列的n个细胞，初始时每个细胞有值x[i]（0 ≤ x[i] < m）。经过一轮演化，每个细胞的新值等于它自己以及左右各d范围内的细胞（共2d+1个）的旧值之和模m。给定演化轮数k（k ≤ 10^7），求最终每个细胞的值。

**输入**：一行n, m, d, k（1 ≤ n ≤ 500, 1 ≤ m ≤ 10^6, 0 ≤ d < n/2, 1 ≤ k ≤ 10^7）。第二行n个整数，表示初始值。

**输出**：n个整数，表示k轮演化后的值。

### 解题思路

**矩阵表示**：演化过程可表示为n维向量x乘以一个n×n的转移矩阵T。

T是一个循环矩阵：T[i][j] = 1 当且仅当(i-j) mod n ≤ d或n-(i-j) mod n ≤ d（即j在i的左右d范围内）。

k轮演化后x' = x · T^k。使用矩阵快速幂O(n³ log k)会超时。

**循环矩阵优化**：
由于T是循环矩阵（每行是上一行的循环右移），循环矩阵的乘积仍然是循环矩阵。因此可以用一维向量t[0…n-1]表示循环矩阵T，使得T[i][j] = t[(i-j+n) mod n]。

矩阵乘法可从O(n³)优化到O(n²)：
(C[i][j]) = Σ A[i][l]·B[l][j]  → 用一维表示后，卷积形式可O(n²)

代码中的实现：
Matrix的a[i]存的是t[i]，表示T[0][i] = a[i]。乘法实现为：
(m.a[i] += a[(i-j+n)%n] * rhs.a[j]) % MOD

实际上这是循环卷积，可以继续用FFT优化到O(n log n)，但n≤500时O(n²)已足够。

### 算法方法
- **矩阵快速幂**：重复平方法计算T^k
- **循环矩阵**：利用循环矩阵性质将空间和时间从O(n²)优化到O(n)和O(n²·log k)
- **模运算**：所有运算模m

### 复杂度分析
- **时间复杂度**：O(n²·log k)，n≤500，k≤10^7
- **空间复杂度**：O(n)，一维循环矩阵表示

```cpp
// 例题27  细胞自动机（Cellular Automaton, NEERC 2006, Codeforces Gym100287C）
// 陈锋
#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;
typedef long long LL;
const int maxn = 500 + 8;
int MOD;  // 模数

// 循环矩阵：用一维数组表示n×n的循环矩阵
// a[i] 表示 T[0][i]，即第一行第i列元素
struct Matrix {
  int a[maxn], n;  // n是矩阵维度
  Matrix(int _n = 1) : n(_n) { fill_n(a, n + 1, 0); }

  // 循环矩阵乘法：C = A * B，C[i][j] = Σ A[i][l] * B[l][j]
  // 在循环矩阵表示下：C.a[i] = Σ A.a[(i-j+n)%n] * B.a[j]
  Matrix operator * (const Matrix &rhs) {
    Matrix m(n);
    for (int i = 0; i < n; i++)
      for (int j = 0; j < n; j++)
        (m.a[i] += (LL)a[(i - j + n) % n] * rhs.a[j] % MOD) %= MOD;
    return m;
  }
};

// 矩阵快速幂：计算x^n
Matrix fast_pow(Matrix x, int n) {
  Matrix m(x.n); m.a[0] = 1;  // 单位矩阵（循环矩阵形式，只有a[0]=1）
  while (n) {
    if (n % 2) m = m * x;  // 二进制位为1则乘上
    x = x * x, n /= 2;     // 平方
  }
  return m;
}

int main() {
  freopen("cell.in", "r", stdin);   // NEERC题目要求文件IO
  freopen("cell.out", "w", stdout);
  for (int d, k, n, m; scanf("%d %d %d %d", &n, &m, &d, &k) == 4;) {
    MOD = m;
    Matrix x(n), y(n);  // x:初始向量, y:转移矩阵（循环矩阵）
    for (int i = 0; i < n; ++i)  scanf("%d", &x.a[i]);

    // 构造转移矩阵y：y[i] = 1当且仅当|i| ≤ d 或 n-|i| ≤ d
    fill_n(y.a, d + 1, 1);         // [0, d] 设置为1
    fill_n(y.a + n - d, d, 1);     // [n-d, n-1] 设置为1（环形对称另一侧）

    Matrix ans = x * fast_pow(y, k);  // ans = x * y^k

    for (int i = 0; i < n; ++i)
      printf("%d%c", ans.a[i], " \n"[i + 1 == n]);  // 输出结果
  }
  return 0;
}
// 102084977 	Dec/23/2020 10:57UTC+8 	chenwz 	C - Cellular Automaton 	GNU C++11 	Accepted 	248 ms 	0 KB 
```

## 例题28  随机程序（Back to Kernighan-Ritchie, UVa 10828）

### 题目描述
给定一个由n个语句组成的程序，语句之间可能会跳转。每个语句执行完后，以等概率跳转到它的每条出边指向的语句。程序从语句0开始执行。对于每个语句i，求程序执行的无穷长过程中，语句i被执行次数的期望占比（即极限概率）。如果期望无穷大，输出infinity。

**输入**：多组数据。每组第一行n（n ≤ 100）。接下来若干行，每行两个整数a b（1 ≤ a,b ≤ n），表示从语句a-1可以等概率跳转到语句b-1。a=b=0表示跳转输入结束。接下来一行一个整数q，然后是q个询问，每个询问一个语句编号（1-indexed）。

**输出**：对于每组数据，输出"Case #X:"，然后每个询问一行，输出期望占比（保留3位小数）或"infinity"。

### 解题思路

**马尔可夫链/线性方程组**：
设x[i]为语句i被执行的期望次数占比。需要满足的方程为：

x[i] = Σ_{j: j→i} x[j] / out[j]（"流入=流出"的稳态方程）

改写为标准形式：
x[i] - Σ_{j: j→i} x[j] / out[j] = 0

其中out[j]是语句j的出度。

再加上起始条件：因为程序从语句0开始，x[0]需要有一个+1的初始项。

这构成一个线性方程组 A·x = b，其中：
- A[i][i] = 1
- A[i][j] = -1/out[j]（如果j能到达i）
- b[0] = 1，其他b[i] = 0

**高斯-约旦消元**：
解这个线性方程组。注意可能存在自由变量（方程组不满秩），导致某些x[i]的解不唯一（即infinity）。

**无穷解判定**：
- 如果某个方程消元后对应行全为0但右端不为0 → 该变量无穷
- 如果某个变量与其他无穷变量有关联 → 也是无穷

### 算法方法
- **线性方程组/高斯消元**：求解稳态概率分布
- **马尔可夫链**：稳态方程的建模

### 复杂度分析
- **时间复杂度**：O(n³)，n≤100，高斯消元
- **空间复杂度**：O(n²)，系数矩阵

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

## 例题26  递推关系（Recurrences, UVa 10870）

### 题目描述
给定d阶线性递推公式：f[n] = a[1]·f[n-1] + a[2]·f[n-2] + … + a[d]·f[n-d]（n ≥ d），以及初始值f[0], f[1], …, f[d-1]。给定正整数n和模数m，求f[n] mod m的值。

**输入**：多组数据。每组第一行d, n, m（1 ≤ d ≤ 15, 0 ≤ n < 2^31, 1 ≤ m < 10^9+7）。第二行d个整数a[1]…a[d]。第三行d个整数f[0]…f[d-1]。d=0结束。

**输出**：对于每组数据，输出f[n] mod m。

### 解题思路

**矩阵快速幂**：将d阶线性递推转化为d×d矩阵的幂运算。

构造状态向量：S[n] = [f[n], f[n-1], …, f[n-d+1]]^T

构造转移矩阵A（d×d）：
```
A = [a[1] a[2] … a[d-1] a[d]]
    [  1    0   …   0      0  ]
    [  0    1   …   0      0  ]
    [ ...  ...  …  ...    ... ]
    [  0    0   …   1      0  ]
```

则S[n] = A · S[n-1]，所以S[n] = A^{n-d+1} · S[d-1]（当n ≥ d时）。

用矩阵快速幂计算A^{n-d}，然后乘以初始向量f[d-1…0]得到结果。

### 算法方法
- **矩阵快速幂**：利用矩阵乘法将递推加速到O(log n)
- **线性递推**：将齐次线性递推转化为向量-矩阵乘法的迭代形式

### 复杂度分析
- **时间复杂度**：O(d³·log n)，d≤15
- **空间复杂度**：O(d²)，矩阵存储

```cpp
// 例题26  递推关系（Recurrences, UVa 10870）
// 刘汝佳
#include <cstring>
#include <iostream>
#include <string>
using namespace std;

const int NN = 20;
typedef long long Matrix[NN][NN];  // d×d矩阵
typedef long long Vector[NN];      // d维向量

int sz, mod;  // sz:实际矩阵大小(d), mod:模数

// 矩阵乘法 C = A * B (mod mod)
void matrix_mul(Matrix A, Matrix B, Matrix res) {
  Matrix C;
  memset(C, 0, sizeof(C));
  for (int i = 0; i < sz; i++)
    for (int j = 0; j < sz; j++)
      for (int k = 0; k < sz; k++)
        C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod;
  memcpy(res, C, sizeof(C));
}

// 矩阵快速幂：res = A^n (mod mod)
void matrix_pow(Matrix A, int n, Matrix res) {
  Matrix a, r;
  memcpy(a, A, sizeof(a)), memset(r, 0, sizeof(r));
  for (int i = 0; i < sz; i++) r[i][i] = 1;  // 单位矩阵
  while (n) {
    if (n & 1) matrix_mul(r, a, r);  // 二进制位1则乘
    n >>= 1;
    matrix_mul(a, a, a);  // A = A^2
  }
  memcpy(res, r, sizeof(r));
}

// 向量-矩阵变换：res = d * A (行向量×矩阵)
void transform(Vector d, Matrix A, Vector res) {
  Vector r;
  memset(r, 0, sizeof(r));
  for (int i = 0; i < sz; i++)
    for (int j = 0; j < sz; j++)
      r[j] = (r[j] + d[i] * A[i][j]) % mod;
  memcpy(res, r, sizeof(r));
}

int main() {
  for (int d, n, m; cin >> d >> n >> m && d;) {
    Matrix A;
    Vector a, f;  // a:系数, f:初始值
    for (int i = 0; i < d; i++) cin >> a[i], a[i] %= m;  // 读系数
    for (int i = d - 1; i >= 0; i--) cin >> f[i], f[i] %= m;  // 读初值(逆序存储)

    // 构造转移矩阵
    memset(A, 0, sizeof(A));
    for (int i = 0; i < d; i++) A[i][0] = a[i];  // 第一列是系数
    for (int i = 1; i < d; i++) A[i - 1][i] = 1;  // 次对角线全1（移位）

    sz = d, mod = m;
    matrix_pow(A, n - d, A);  // A = A^(n-d)
    transform(f, A, f);       // f = f * A^(n-d)
    cout << f[0] << endl;     // f[0]即f[n]
  }
  return 0;
}
// 25839977 10870 Recurrences Accepted C++ 0.030 2020-12-12 13:16:01
```

## 例题29  乘积是平方数（Square, UVa 11542）

### 题目描述
给定n个正整数，问有多少个非空子集，使得子集中所有数的乘积是一个完全平方数。n ≤ 100，每个数 ≤ 10^15。

**输入**：第一行T（T ≤ 30）。每组第一行n，第二行n个正整数。

**输出**：对于每组数据，输出非空子集个数。

### 解题思路

**转化为线性方程组（在GF(2)上）**：
乘积为平方数 ⟺ 每个质因子的指数之和为偶数 ⟺ 每个质因子的指数之和对2取模为0。

对每个数进行质因数分解（只需要考虑≤500的质数，共95个），将每个质因子的指数模2映射到GF(2)域上。

构造m×n的0-1矩阵A：
- A[i][j] = 质因子prime[i]在第j个数中的指数（mod 2）
- m是涉及的质因子个数，n是数的个数

问题转化为：求系数矩阵A的零空间大小。即求解Ax=0（mod 2），x∈{0,1}^n，x的第j个分量表示是否选择第j个数。

零空间的维数 = n - rank(A)，其中rank(A)是在GF(2)上矩阵A的秩。

非零解个数 = 2^{n-rank(A)} - 1（减1排除全0解）。

### 算法方法
- **线性方程组/GF(2)高斯消元**：在模2域上求矩阵秩
- **数论**：质因数分解 + 指数模2映射

### 复杂度分析
- **时间复杂度**：O(T·(n√N + m·n²))，n≤100，m≤95
- **空间复杂度**：O(m·n)，系数矩阵

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

// 埃氏筛生成≤500的素数表
int gen_primes(int n) {
  int m = (int)sqrt(n + 0.5);
  fill_n(vis, NN, 0);
  for (int i = 2; i <= m; i++)
    if (!vis[i])
      for (int j = i * i; j <= n; j += i) vis[j] = 1;  // 标记合数
  int c = 0;
  for (int i = 2; i <= n; i++)
    if (!vis[i]) prime[c++] = i;  // 收集素数
  return c;
}

typedef int Matrix[NN][NN];

// GF(2)上的高斯消元求矩阵秩
// m个方程，n个变量
int get_rank(Matrix A, int m, int n) {
  int i = 0, j = 0, k, r, u;
  while (i < m && j < n) {  // 依次处理第j列
    // 找第j列中第i行及以下最近的非0行
    r = i;
    for (k = i; k < m; k++)
      if (A[k][j]) { r = k; break; }
    if (A[r][j]) {
      if (r != i)
        for (k = 0; k <= n; k++) swap(A[r][k], A[i][k]);  // 交换到第i行
      // 用第i行消去下面所有行第j列的非零元（GF(2)上用异或）
      for (u = i + 1; u < m; u++)
        if (A[u][j])
          for (k = i; k <= n; k++) A[u][k] ^= A[i][k];  // 异或消元
      i++;  // 秩+1，处理下一行
    }
    j++;  // 处理下一列
  }
  return i;  // 返回秩
}

Matrix A;

int main() {
  int m = gen_primes(500), T;  // m = 素数个数
  cin >> T;
  while (T--) {
    int n, maxp = 0;
    long long x;  // 注意x可达10^15，需用long long
    cin >> n;
    memset(A, 0, sizeof(A));
    for (int i = 0; i < n; i++) {
      cin >> x;
      // 质因数分解，记录每个质因子的指数模2
      for (int j = 0; j < m; j++)
        while (x % prime[j] == 0)
          maxp = max(maxp, j), x /= prime[j], A[j][i] ^= 1;  // 模2翻转
    }
    // 只用前maxp+1个素数（实际涉及到的质因子）
    int r = get_rank(A, maxp + 1, n);
    // 解空间大小 = 2^(n-r)，非空子集 = 2^(n-r) - 1
    cout << (1LL << (n - r)) - 1 << endl;
  }
  return 0;
}
// Accepted 1573 C++ 5.3.0 2020-12-12 21:46:13 25840133
```
