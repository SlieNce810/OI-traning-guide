# 2.5 概率与数学期望

## UVa11021 Tribles

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

## UVa11427 Expect the Expected

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

## UVa11722 Joining with Friend （限于篇幅，书上无此代码）

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

## UVa11762 Race To 1

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
