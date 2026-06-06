# 2.9 数值方法简介

## 例题37  误差曲线（Error Curves, Chengdu 2010, LA5009）

### 题目描述
有n条二次误差曲线，第i条为S_i(x) = a_i·x² + b_i·x + c_i（a_i ≥ 0）。定义总误差F(x) = max{S_1(x), S_2(x), …, S_n(x)}，即所有曲线的逐点最大值。求F(x)在区间[0, 1000]上的最小值。

**输入**：第一行T（T ≤ 100）。每组第一行n（1 ≤ n ≤ 10000）。接下来n行，每行三个整数a,b,c（0 ≤ a ≤ 100, |b| ≤ 5000, |c| ≤ 5000）。

**输出**：对于每组数据，输出F(x)的最小值，保留4位小数。

### 解题思路

**凸函数性质**：
每条曲线S_i(x)由于a_i ≥ 0，是凸函数（开口向上的抛物线）。多个凸函数的逐点最大值也是凸函数（U形）。

因此F(x)在[0, 1000]上是单峰的（先减后增），可以用三分搜索找到最小值。

**三分搜索**：
在区间[L, R]中，取两个三分点m1 = L + (R-L)/3和m2 = R - (R-L)/3。
- 如果F(m1) < F(m2)，最小值在[L, m2]中（收缩右边界R=m2）
- 否则，最小值在[m1, R]中（收缩左边界L=m1）

迭代约100次即可收敛到足够精度。

### 算法方法
- **数值方法/三分搜索**：利用凸函数的单峰性质
- **极值问题**：max of convex = convex

### 复杂度分析
- **时间复杂度**：O(T·n·iter)，n≤10000，iter≈100
- **空间复杂度**：O(n)，存储曲线系数

```cpp
// 例题37  误差曲线（Error Curves, Chengdu 2010, LA5009）
// 刘汝佳
#include <algorithm>
#include <cstdio>
using namespace std;
const int NN = 10000 + 10;
int T, n, a[NN], b[NN], c[NN];  // 曲线系数 a,b,c

// 计算F(x) = max a_i*x^2 + b_i*x + c_i（所有曲线的最大值）
double F(double x) {
  double ans = a[0] * x * x + b[0] * x + c[0];
  for (int i = 1; i < n; i++)
    ans = max(ans, a[i] * x * x + b[i] * x + c[i]);  // 取逐点最大值
  return ans;
}

int main() {
  scanf("%d", &T);
  while (T--) {
    scanf("%d", &n);
    for (int i = 0; i < n; i++) scanf("%d%d%d", &a[i], &b[i], &c[i]);
    double L = 0.0, R = 1000.0;  // 搜索区间[0,1000]
    for (int i = 0; i < 100; i++) {  // 迭代100次确保精度
      double m1 = L + (R - L) / 3;  // 左三分点
      double m2 = R - (R - L) / 3;  // 右三分点
      if (F(m1) < F(m2)) R = m2;   // 最小值在左侧，收缩右边界
      else L = m1;                  // 最小值在右侧，收缩左边界
    }
    printf("%.4lf\n", F(L));  // 输出最小误差
  }
  return 0;
}
// 34852546 2020-12-12 22:21:37 Accepted 3714 280MS 1344K 686 B G++
```

## 例题36  解方程（Solve It!, UVa 10341）

### 题目描述
解方程：p·e^{-x} + q·sin(x) + r·cos(x) + s·tan(x) + t·x² + u = 0，在x∈[0, 1]范围内求解（最多一个解）。系数p,q,r,s,t,u都是整数（0 ≤ p,r ≤ 20，-20 ≤ q,s,t ≤ 0）。

**输入**：多组数据，每组一行6个整数p,q,r,s,t,u。

**输出**：如果[0,1]内有解，输出解保留4位小数；否则输出"No solution"。

### 解题思路

**单调性分析**：
定义F(x) = p·e^{-x} + q·sin(x) + r·cos(x) + s·tan(x) + t·x² + u

分析各分量的单调性：
- p·e^{-x}递减（导数为-p·e^{-x}≤0，p≥0）
- q·sin(x)递减（q≤0）
- r·cos(x)递减（导数为-r·sin(x)，r≥0，sin(x)≥0在[0,1]上）
- s·tan(x)递减（s≤0，tan在[0,1]上递增）
- t·x²递减（t≤0）

所以F(x)在[0,1]上是严格单调递减的。因此最多有一个根。

**二分法求解**：
检查F(0)和F(1)：
- 如果F(0) < -eps 或 F(1) > eps → 无解（根不在[0,1]内）
- 否则，在[0,1]上二分：如果F(mid) < 0，根在左侧(y=mid)；否则根在右侧(x=mid)
  迭代约100次即可收敛。

### 算法方法
- **数值方法/二分法**：利用函数的单调性
- **微积分**：分析各项导数的符号确认单调性

### 复杂度分析
- **时间复杂度**：O(iter·T)，iter≈100
- **空间复杂度**：O(1)

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

### 题目描述
一座桥由若干段等宽的桥墩和桥面组成。给定总跨距D（桥墩宽度），总长度B，桥面下垂高度H（最大凹陷处），以及绳索总长度L。桥面形状是抛物线y = a·x²。需要计算桥面从最高点到最低点的竖直距离。桥面被n段等宽的桥墩支撑（n = ⌈B/D⌉），每段的绳索长度相等（L1 = L/n）。

**输入**：第一行T。每组一行D, H, B, L。

**输出**：对于每组数据，输出"Case X:\n"和桥面的竖直落差，保留2位小数。

### 解题思路

**抛物线弧长公式**：
对于抛物线y = a·x²，参数a满足在[-w/2, w/2]上最大高度为h，即a = 4h/w²。

抛物线弧长公式：
∫√(1 + (dy/dx)²) dx = ∫√(1 + (2a·x)²) dx

原函数：
F(a, x) = (x·√(a²+x²) + a²·ln|x+√(a²+x²)|)/2

其中这里的a参数是1/(2a)（抛物线的参数化）。

单段弧长 = 4a · (F(b, w/2) - F(b, 0))，其中b = 1/(2a) = w²/(8h)。

**二分法求解h**：
给定弧长L1和宽度D1，需要求高度h。弧长是h的单调递增函数，可以使用二分法求解h。

然后在已知h后计算最终答案H-h。

### 算法方法
- **数值方法/二分法**：利用弧长关于高度的单调性
- **微积分**：抛物线弧长的解析积分

### 复杂度分析
- **时间复杂度**：O(T·iter)，每次二分约50次迭代
- **空间复杂度**：O(1)

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
