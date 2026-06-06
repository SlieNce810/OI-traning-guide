# 2.7 矩阵和线性方程组

## 例题27  细胞自动机（Cellular Automaton, NEERC 2006, Codeforces Gym100287C）

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

## 例题28  随机程序（Back to Kernighan-Ritchie, UVa 10828）

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

## 例题29  乘积是平方数（Square, UVa 11542）

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
