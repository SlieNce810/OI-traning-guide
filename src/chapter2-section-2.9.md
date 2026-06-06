# 2.9 数值方法简介

## 例题37  误差曲线（Error Curves, Chengdu 2010, LA5009）

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

## 例题36  解方程（Solve It!, UVa 10341）

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

## 例题38  桥上的绳索（Bridge, Hangzhou 2005, UVa1356）

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
