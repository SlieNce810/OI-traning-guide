# 6.5 数学专题

## LA3700/POJ3146 Interesting Yang Hui Triangle, Asia上海 2016

```cpp
// LA3700/POJ3146 Interesting Yang Hui Triangle, Asia上海 2016
// 刘汝佳
#include <cstdio>
int main() {
  for (int kase = 0, n, p; scanf("%d%d", &p, &n) == 2 && p;) {
    int ans = 1;
    while (n > 0) ans = ans * (n % p + 1) % 10000, n /= p;
    printf("Case %d: %04d\n", ++kase, ans);
  }
  return 0;
}
// Accepted 328kB 298 G++ 2020-12-12 22:41:35 22206289
```

## UVa1457/LA4746 Decrypt Messages

```cpp
// UVa1457/LA4746 Decrypt Messages
// 刘汝佳
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <vector>
#include <map>
#include <algorithm>
#include <iostream>
using namespace std;

typedef long long LL;
//// 日期时间部分
const int SECONDS_PER_DAY = 24 * 60 * 60;
const int num_days[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
bool is_leap(int year) {
  if (year % 400 == 0) return true;
  if (year % 4 == 0) return year % 100 != 0;
  return false;
}

int leap_second(int year, int month) {
  return ((year % 10 == 5 || year % 10 == 8) && month == 12) ? 1 : 0;
}

void print(int year, int month, int day, int hh, int mm, int ss) {
  printf("%d.%02d.%02d %02d:%02d:%02d\n", year, month, day, hh, mm, ss);
}

void print_time(LL t) {
  int year = 2000;
  while(1) {
    int days = is_leap(year) ? 366 : 365;
    LL sec = (LL)days * SECONDS_PER_DAY + leap_second(year, 12);
    if(t < sec) break;
    t -= sec;
    year++;
  }

  int month = 1;
  while(1) {
    int days = num_days[month-1];
    if(is_leap(year) && month == 2) days++;
    LL sec = (LL)days * SECONDS_PER_DAY + leap_second(year, month);
    if(t < sec) break;
    t -= sec;
    month++;
  }

  if(leap_second(year, month) && t == 31 * SECONDS_PER_DAY)
    print(year, 12, 31, 23, 59, 60);
  else {
    int day = t / SECONDS_PER_DAY + 1;
    t %= SECONDS_PER_DAY;
    int hh = t / (60*60);
    t %= 60*60;
    int mm = t / 60;
    t %= 60;
    int ss = t;
    print(year, month, day, hh, mm, ss);
  }
}

//// 数论部分

LL gcd(LL a, LL b) {
  return b ? gcd(b, a%b) : a;
}

// 求d = gcd(a, b)，以及满足ax+by=d的(x,y)（注意，x和y可能为负数）
// 扩展euclid算法。
void gcd(LL a, LL b, LL& d, LL& x, LL& y) {
  if(!b){ d = a; x = 1; y = 0; }
  else{ gcd(b, a%b, d, y, x); y -= x*(a/b); }
}

// 注意，返回值可能是负的
int pow_mod(LL a, LL p, int MOD) {
  if(p == 0) return 1;
  LL ans = pow_mod(a, p/2, MOD);
  ans = ans * ans % MOD;
  if(p%2) ans = ans * a % MOD;
  return ans;
}

// 注意，返回值可能是负的
int mul_mod(LL a, LL b, int MOD) {
  return a * b % MOD;
}

// 求ax = 1 (mod MOD) 的解，其中a和MOD互素。
// 注意，由于MOD不一定为素数，因此不能直接用pow_mod(a, MOD-2, MOD)求解
// 解法：先求ax + MODy = 1的解(x,y)，则x为所求
int inv(LL a, int MOD) {
  LL d, x, y;
  gcd(a, MOD, d, x, y);
  return (x + MOD) % MOD; // 这里的x可能是负数，因此要调整
}

// 解模方程（即离散对数）a^x = b。要求MOD为素数
// 解法：Shank的大步小步算法
int log_mod(int a, int b, int MOD) {
  int m, v, e = 1, i;
  m = (int)sqrt(MOD);
  v = inv(pow_mod(a, m, MOD), MOD);
  map<int,int> x;
  x[1] = 0;
  for(i = 1; i < m; i++){ e = mul_mod(e, a, MOD); if (!x.count(e)) x[e] = i; }
  for(i = 0; i < m; i++){
    if(x.count(b)) return i*m + x[b];
    b = mul_mod(b, v, MOD);
  }
  return -1;
}

// 返回MOD（不一定是素数）的某一个原根，phi为MOD的欧拉函数值（若MOD为素数则phi=MOD-1）
// 解法：考虑phi(MOD)的所有素因子p，如果所有m^(phi/p) mod MOD都不等于1，则m是MOD的原根
int get_primitive_root(int MOD, int phi) {
  // 计算phi的所有素因子
  vector<int> factors;
  int n = phi;
  for(int i = 2; i*i <= n; i++) {
    if(n % i != 0) continue;
    factors.push_back(i);
    while(n % i == 0) n /= i;
  }
  if(n > 1) factors.push_back(n);

  while(1) {
    int m = rand() % (MOD-2) + 2; // m = 2~MOD-1
    bool ok = true;
    for(int i = 0; i < factors.size(); i++)
      if(pow_mod(m, phi/factors[i], MOD) == 1) { ok = false; break; }
    if(ok) return m;
  }
}

// 解线性模方程 ax = b (mod n)，返回所有解（模n剩余系）
// 解法：令d = gcd(a, n)，两边同时除以d后得a'x = b' (mod n')，由于此时gcd(a',n')=1，两边同时左乘a'在模n'中的逆即可，最后把模n'剩余系中的解转化为模n剩余系
vector<LL> solve_linear_modular_equation(int a, int b, int n) {
  vector<LL> ans;
  int d = gcd(a, n);
  if(b % d != 0) return ans;
  a /= d; b /= d;
  int n2 = n / d;
  int p = mul_mod(inv(a, n2), b, n2);
  for(int i = 0; i < d; i++)
    ans.push_back(((LL)i * n2 + p) % n);
  return ans;
}

// 解高次模方程 x^q = a (mod p)，返回所有解（模n剩余系）
// 解法：设m为p的一个原根，且x = m^y, a = m^z，则m^qy = m^z(mod p)，因此qy = z(mod p-1)，解线性模方程即可
vector<LL> mod_root(int a, int q, int p) {
  vector<LL> ans;
  if(a == 0) {
    ans.push_back(0);
    return ans;
  }
  int m = get_primitive_root(p, p-1); // p是素数，因此phi(p)=p-1
  int z = log_mod(m, a, p);
  ans = solve_linear_modular_equation(q, z, p-1);
  for(int i = 0; i < ans.size(); i++)
    ans[i] = pow_mod(m, ans[i], p);
  sort(ans.begin(), ans.end());
  return ans;
}

int main() {
  int T, P, Q, A;
  cin >> T;
  for(int kase = 1; kase <= T; kase++) {
    cin >> P >> Q >> A;
    vector<LL> ans = mod_root(A, Q, P);
    cout << "Case #" << kase << ":" << endl;
    if (ans.empty()) {
      cout << "Transmission error" << endl;
    } else {
      for(int i = 0; i < ans.size(); i++) print_time(ans[i]);
    }
  }	
  return 0;
}
// 25878475	1457	Decrypt Messages	Accepted	C++	0.570	2020-12-23 09:22:31
```

## UVa10498 Happiness

```cpp
// UVa10498 Happiness
// 刘汝佳
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<cassert>
using namespace std;

// 改进单纯性法的实现
// 参考：http://en.wikipedia.org/wiki/Simplex_algorithm
// 输入矩阵a描述线性规划的标准形式。a为m+1行n+1列，其中行0~m-1为不等式，行m为目标函数（最大化）。列0~n-1为变量0~n-1的系数，列n为常数项
// 第i个约束为a[i][0]*x[0] + a[i][1]*x[1] + ... <= a[i][n]
// 目标为max(a[m][0]*x[0] + a[m][1]*x[1] + ... + a[m][n-1]*x[n-1] - a[m][n])
// 注意：变量均有非负约束x[i] >= 0
const int maxm = 500; // 约束数目上限
const int maxn = 500; // 变量数目上限
const double INF = 1e100, eps = 1e-10;

struct Simplex {
  int n; // 变量个数
  int m; // 约束个数
  double a[maxm][maxn]; // 输入矩阵
  int B[maxm], N[maxn]; // 算法辅助变量

  void pivot(int r, int c) {
    swap(N[c], B[r]);
    a[r][c] = 1 / a[r][c];
    for(int j = 0; j <= n; j++) if(j != c) a[r][j] *= a[r][c];
    for(int i = 0; i <= m; i++) if(i != r) {
      for(int j = 0; j <= n; j++) if(j != c) a[i][j] -= a[i][c] * a[r][j];
      a[i][c] = -a[i][c] * a[r][c];
    }
  }

  bool feasible() {
    for(;;) {
      int r, c;
      double p = INF;
      for(int i = 0; i < m; i++) if(a[i][n] < p) p = a[r = i][n];
      if(p > -eps) return true;
      p = 0;
      for(int i = 0; i < n; i++) if(a[r][i] < p) p = a[r][c = i];
      if(p > -eps) return false;
      p = a[r][n] / a[r][c];
      for(int i = r+1; i < m; i++) if(a[i][c] > eps) {
        double v = a[i][n] / a[i][c];
        if(v < p) { r = i; p = v; }
      }
      pivot(r, c);
    }
  }

  // 解有界返回1，无解返回0，无界返回-1。b[i]为x[i]的值，ret为目标函数的值
  int simplex(int n, int m, double x[maxn], double& ret) {
    this->n = n;
    this->m = m;
    for(int i = 0; i < n; i++) N[i] = i;
    for(int i = 0; i < m; i++) B[i] = n+i;
    if(!feasible()) return 0;
    for(;;) {
      int r, c;
      double p = 0;
      for(int i = 0; i < n; i++) if(a[m][i] > p) p = a[m][c = i];
      if(p < eps) {
        for(int i = 0; i < n; i++) if(N[i] < n) x[N[i]] = 0;
        for(int i = 0; i < m; i++) if(B[i] < n) x[B[i]] = a[i][n];
        ret = -a[m][n];
        return 1;
      }
      p = INF;
      for(int i = 0; i < m; i++) if(a[i][c] > eps) {
        double v = a[i][n] / a[i][c];
        if(v < p) { r = i; p = v; }
      }
      if(p == INF) return -1;
      pivot(r, c);
    }
  }
};

//////////////// 题目相关
#include<cmath>
Simplex solver;

int main() {
  for(int n, m;scanf("%d%d", &n, &m) == 2;) {
    for(int i = 0; i < n; i++) scanf("%lf", &solver.a[m][i]); // 目标函数
    solver.a[m][n] = 0; // 目标函数常数项
    for(int i = 0; i < m; i++)
      for(int j = 0; j < n+1; j++)
        scanf("%lf", &solver.a[i][j]);
    double ans, x[maxn];
    assert(solver.simplex(n, m, x, ans) == 1);
    ans *= m;
    printf("Nasa can spend %d taka.\n", (int)floor(ans + 1 - eps));
  }
  return 0;
}
// Accepted 10ms 2716 C++5.3.0 2020-12-12 22:39:36 25840427
```

## UVa11017 A Greener World

```cpp
// UVa11017 A Greener World
// Rujia Liu
#include <cmath>
#include <cstdio>
#include <vector>
using namespace std;

typedef long long LL;

const double PI = acos(-1.0);

struct Point {
  int x, y;
  Point(int x = 0, int y = 0) : x(x), y(y) {}
};

typedef Point Vector;

Vector operator+(const Vector& A, const Vector& B) {
  return Vector(A.x + B.x, A.y + B.y);
}
Vector operator-(const Point& A, const Point& B) {
  return Vector(A.x - B.x, A.y - B.y);
}
double Cross(const Vector& A, const Vector& B) {
  return (LL)A.x * B.y - (LL)A.y * B.x;
}

LL PolygonArea2(const vector<Point>& p) {
  int n = p.size();
  LL area2 = 0;
  for (int i = 1; i < n - 1; i++) area2 += Cross(p[i] - p[0], p[i + 1] - p[0]);
  return abs(area2);
}

inline int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }

// 线段a-b上的格点数。不包含a和b。设参数t = b/d
// 则d必须是b.x-a.x和b.y-a.y的公约数，且0<b<d,
// 减1因为要排除端点，因此0和d都不能做分子
LL count_on_segment(const Point& a, const Point& b) {
  return gcd(abs(b.x - a.x), abs(b.y - a.y)) - 1;
}

// Pick's Theorem: A = I + B/2 - 1 => I = A - B/2 + 1
LL count_inside_polygon(const vector<Point>& poly) {
  int n = poly.size();
  LL A2 = PolygonArea2(poly);
  int B = n;  // 多边形的顶点
  for (int i = 0; i < n; i++) B += count_on_segment(poly[i], poly[(i + 1) % n]);
  return (A2 - B) / 2 + 1;
}

// 计算内部的、x和y的小数部分都是0.5的点
LL count(const vector<Point>& poly) {
  vector<Point> poly2;
  for (int i = 0; i < poly.size(); i++)  // 旋转45度后的稠密网格坐标
    poly2.push_back(Point(poly[i].x - poly[i].y, poly[i].x + poly[i].y));
  return count_inside_polygon(poly2) - count_inside_polygon(poly);
}

int main() {
  // theta和d仅仅用来算面积
  for (int d, theta, N, x, y; scanf("%d%d%d", &d, &theta, &N) == 3 && d;) {
    vector<Point> poly;
    for (int i = 0; i < N; i++)
      scanf("%d%d", &x, &y), poly.push_back(Point(x, y));
    LL area2 = PolygonArea2(poly);
    printf("%lld %.0lf\n", count(poly),
           sin((double)theta / 180 * PI) * d * d * area2 / 2.0);
  }
  return 0;
}
// Accepted 1963 C++5.3.0 2020-12-1222:36:42|□25840418
```
