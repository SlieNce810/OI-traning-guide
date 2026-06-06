# 6.5 数学专题

本章涵盖数论、组合数学、线性规划和计算几何中的数学问题，包括Lucas定理、离散对数、单纯形法、Pick定理等经典数学工具。

## LA3700/POJ3146 Interesting Yang Hui Triangle, Asia上海 2016

### 题目描述
给定质数p（2 ≤ p ≤ 10000）和整数n（0 ≤ n ≤ 10^9），求杨辉三角（帕斯卡三角）第n行中，有多少个数不能被p整除。结果对10000取模，输出时4位补零。

杨辉三角第n行第k列的元素为组合数C(n, k)（0 ≤ k ≤ n）。题目要求统计C(n, k) mod p ≠ 0的k的个数。

### 解题思路
使用**Lucas定理**的推论：C(n, k) mod p ≠ 0当且仅当n的p进制表示的每一位都≥k的p进制表示的对应位。

因此，对于n在p进制下的每一位数字n_i，k在对应位的数字可以有n_i+1种选择（0, 1, ..., n_i），使得C(n_i, k_i) mod p ≠ 0。

总答案 = ∏(n_i + 1)，其中n_i是n的p进制表示中的第i位。

例如：n = 232, p = 7
- n的7进制：232 = 4×49 + 5×7 + 1 → (4,5,1)
- 答案 = (4+1)×(5+1)×(1+1) = 5×6×2 = 60

### 算法方法
**Lucas定理的直接推论**：
- Lucas定理：C(n,k) mod p = ∏C(n_i, k_i) mod p
- C(n_i, k_i) mod p ≠ 0 ⇔ k_i ≤ n_i（因为p是质数，C(n_i, k_i)含有因子p当且仅当n_i < k_i）
- 因此每位有n_i+1种合法选择
- 总方案数：accumulate = ∏(n_i+1) mod 10000

### 复杂度分析
- **时间复杂度**：O(log_p n)，n≤10^9时最多约30次循环
- **空间复杂度**：O(1)，常数空间

```cpp
// LA3700/POJ3146 Interesting Yang Hui Triangle, Asia上海 2016
// 刘汝佳
// 题目：杨辉三角 - 求第n行中不被质数p整除的元素个数（Lucas定理）
#include <cstdio>

int main() {
  for (int kase = 0, n, p; scanf("%d%d", &p, &n) == 2 && p;) {
    int ans = 1;
    // 将n转为p进制，每位贡献(数字+1)的乘积
    // ans = ∏(n_i + 1) mod 10000
    while (n > 0) {
      ans = ans * (n % p + 1) % 10000;  // n%p = 当前位数字
      n /= p;                            // 去掉最低位
    }
    printf("Case %d: %04d\n", ++kase, ans);  // 4位补零输出
  }
  return 0;
}
// Accepted 328kB 298 G++ 2020-12-12 22:41:35 22206289
```

## UVa1457/LA4746 Decrypt Messages

### 题目描述
某加密系统中，消息的加密过程为：x^Q mod P = A，其中P是质数，Q是指数，A是密文，x是明文。已知P、Q、A（Q < P-1且与P-1互质），要求解密出x，并将x解释为从2000-01-01 00:00:00起经过的秒数（考虑闰秒），输出对应的日期时间。

如果x无解则输出"Transmission error"；如果有多解则输出所有合法解对应的日期时间。

### 解题思路
这是一个**模方程求根**问题：x^Q ≡ A (mod P)，需求解x。

方法：
1. **求质数P的原根m**：找一个数m使得m^((P-1)/f) mod P ≠ 1对所有P-1的素因子f成立
2. **求离散对数**：用大步小步算法（Baby-step Giant-step）求z满足m^z ≡ A (mod P)
3. **解线性模方程**：由m^(Qy) ≡ m^z (mod P)得Q·y ≡ z (mod P-1)，解此线性同余方程得y
4. **还原x**：x ≡ m^y (mod P)

日期时间部分：从2000-01-01开始计时，考虑闰年（每4年但不包括能被100整除非400整除的年份）和闰秒（年份末位为5或8的12月有61秒）。

### 算法方法
**离散对数 + 原根 + 线性同余方程**：
1. `get_primitive_root(MOD, phi)`：随机搜索原根
2. `log_mod(a, b, MOD)`：大步小步算法求离散对数
3. `solve_linear_modular_equation(a, b, n)`：扩展欧几里得解线性同余方程
4. `mod_root(A, Q, P)`：组合以上三步求x^Q≡A(mod P)的所有解

### 复杂度分析
- **时间复杂度**：
  - 原根查找：O(φ(P) × log P)，但实际很快（随机）
  - 大步小步：O(√P × log P)，P≈20000时约3000次
  - 解线性同余方程：O(log P)
  - 总：O(√P × log P)
- **空间复杂度**：O(√P)，大步小步算法的哈希表

```cpp
// UVa1457/LA4746 Decrypt Messages
// 刘汝佳
// 题目：解密消息 - 解x^Q≡A(mod P)并转换为日期时间
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

// 判断闰年
bool is_leap(int year) {
  if (year % 400 == 0) return true;
  if (year % 4 == 0) return year % 100 != 0;
  return false;
}

// 判断某年某月是否有闰秒（年份末位为5或8的12月）
int leap_second(int year, int month) {
  return ((year % 10 == 5 || year % 10 == 8) && month == 12) ? 1 : 0;
}

// 格式化输出日期时间
void print(int year, int month, int day, int hh, int mm, int ss) {
  printf("%d.%02d.%02d %02d:%02d:%02d\n", year, month, day, hh, mm, ss);
}

// 将秒数t转换为日期时间并打印（从2000-01-01 00:00:00起）
void print_time(LL t) {
  // 先确定年份
  int year = 2000;
  while(1) {
    int days = is_leap(year) ? 366 : 365;
    LL sec = (LL)days * SECONDS_PER_DAY + leap_second(year, 12);
    if(t < sec) break;
    t -= sec;
    year++;
  }

  // 再确定月份
  int month = 1;
  while(1) {
    int days = num_days[month-1];
    if(is_leap(year) && month == 2) days++;
    LL sec = (LL)days * SECONDS_PER_DAY + leap_second(year, month);
    if(t < sec) break;
    t -= sec;
    month++;
  }

  // 处理闰秒特殊情况（12月31日23:59:60）
  if(leap_second(year, month) && t == 31 * SECONDS_PER_DAY)
    print(year, 12, 31, 23, 59, 60);
  else {
    int day = t / SECONDS_PER_DAY + 1;  // 日期（1-indexed）
    t %= SECONDS_PER_DAY;
    int hh = t / (60*60);              // 小时
    t %= 60*60;
    int mm = t / 60;                   // 分钟
    t %= 60;
    int ss = t;                        // 秒
    print(year, month, day, hh, mm, ss);
  }
}

//// 数论部分

LL gcd(LL a, LL b) {
  return b ? gcd(b, a%b) : a;
}

// 扩展欧几里得算法：求d=gcd(a,b)及满足ax+by=d的(x,y)
void gcd(LL a, LL b, LL& d, LL& x, LL& y) {
  if(!b){ d = a; x = 1; y = 0; }
  else{ gcd(b, a%b, d, y, x); y -= x*(a/b); }
}

// 快速模幂：a^p mod MOD
int pow_mod(LL a, LL p, int MOD) {
  if(p == 0) return 1;
  LL ans = pow_mod(a, p/2, MOD);
  ans = ans * ans % MOD;
  if(p%2) ans = ans * a % MOD;
  return ans;
}

// 模乘法
int mul_mod(LL a, LL b, int MOD) {
  return a * b % MOD;
}

// 求a在模MOD下的逆元（a和MOD互素）
// 解法：扩展欧几里得求ax+MODy=1，x即为逆元
int inv(LL a, int MOD) {
  LL d, x, y;
  gcd(a, MOD, d, x, y);
  return (x + MOD) % MOD;  // x可能为负，调整为正
}

// 解离散对数方程 a^x ≡ b (mod MOD)，MOD为素数
// Shank's baby-step giant-step算法
int log_mod(int a, int b, int MOD) {
  int m, v, e = 1, i;
  m = (int)sqrt(MOD);  // 步长≈√MOD
  v = inv(pow_mod(a, m, MOD), MOD);  // v = a^{-m} mod MOD
  
  // Baby step：存储a^0, a^1, ..., a^{m-1}
  map<int,int> x;
  x[1] = 0;
  for(i = 1; i < m; i++) {
    e = mul_mod(e, a, MOD);
    if (!x.count(e)) x[e] = i;
  }
  
  // Giant step：用b乘以a^{-mi}查找匹配
  for(i = 0; i < m; i++){
    if(x.count(b)) return i*m + x[b];
    b = mul_mod(b, v, MOD);  // b *= a^{-m}
  }
  return -1;  // 无解
}

// 求MOD的原根（MOD不一定是素数，phi为MOD的欧拉函数值）
// 若MOD为素数，phi=MOD-1
// 判定条件：对phi的每个素因子p，m^(phi/p) mod MOD ≠ 1
int get_primitive_root(int MOD, int phi) {
  // 分解phi的素因子
  vector<int> factors;
  int n = phi;
  for(int i = 2; i*i <= n; i++) {
    if(n % i != 0) continue;
    factors.push_back(i);
    while(n % i == 0) n /= i;
  }
  if(n > 1) factors.push_back(n);

  // 随机搜索原根
  while(1) {
    int m = rand() % (MOD-2) + 2;  // m ∈ [2, MOD-1]
    bool ok = true;
    for(int i = 0; i < factors.size(); i++)
      if(pow_mod(m, phi/factors[i], MOD) == 1) { ok = false; break; }
    if(ok) return m;
  }
}

// 解线性同余方程 ax ≡ b (mod n)，返回所有解（模n剩余系）
// 解法：令d=gcd(a,n)，两边除d得a'x≡b'(mod n')，乘a'的逆元求解
vector<LL> solve_linear_modular_equation(int a, int b, int n) {
  vector<LL> ans;
  int d = gcd(a, n);
  if(b % d != 0) return ans;  // 无解
  a /= d; b /= d;
  int n2 = n / d;
  int p = mul_mod(inv(a, n2), b, n2);  // 基础解
  // 生成d个解（模n剩余系）
  for(int i = 0; i < d; i++)
    ans.push_back(((LL)i * n2 + p) % n);
  return ans;
}

// 解高次模方程 x^q ≡ a (mod p)，p为素数
// 解法：设m为p的原根，x=m^y, a=m^z，则m^{qy}≡m^z(mod p)
// 即qy≡z(mod p-1)，解线性同余方程后还原x
vector<LL> mod_root(int a, int q, int p) {
  vector<LL> ans;
  if(a == 0) {  // 平凡情况
    ans.push_back(0);
    return ans;
  }
  int m = get_primitive_root(p, p-1);  // p是素数，phi(p)=p-1
  int z = log_mod(m, a, p);            // 求离散对数z
  ans = solve_linear_modular_equation(q, z, p-1);  // 解qy≡z(mod p-1)
  for(int i = 0; i < ans.size(); i++)
    ans[i] = pow_mod(m, ans[i], p);    // 还原x = m^y mod p
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

### 题目描述
Nasa需要合理分配开支以最大化幸福感。问题建模为标准线性规划问题：
- 有n个变量（开支类别），m个约束条件
- 目标：最大化 Σ(c_i × x_i)
- 约束：Σ(a_ij × x_i) ≤ b_j, x_i ≥ 0

给定目标函数系数c_i和约束矩阵a_ij及常数b_j，求最大目标函数值（乘以m后输出整数）。

### 解题思路
使用**单纯形法（Simplex Algorithm）**求解标准线性规划问题。标准形式为：
- max c^T x
- s.t. Ax ≤ b, x ≥ 0

单纯形法的两个阶段：
1. **可行性阶段（Phase I）**：找到一个可行解
2. **优化阶段（Phase II）**：从可行解出发，通过pivot操作逐步优化目标函数

每次pivot选择一个入基变量（目标函数系数为正）和一个出基变量（约束最紧），进行高斯消元式的行变换。当目标函数行所有系数≤0时达到最优解。

### 算法方法
**改进单纯形法（Revised Simplex）**：
- 矩阵表示：a[m+1][n+1]，前m行是约束，第m行为目标函数
- `pivot(r, c)`：以(r,c)为枢轴元素进行变换
- `feasible()`：Phase I，确保基本解满足非负约束
- `simplex()`：Phase II，从可行解出发迭代优化

### 复杂度分析
- **时间复杂度**：O(m×n×迭代次数)，最坏指数级但实际很快。n,m ≤ 500
- **空间复杂度**：O(m×n)，存储系数矩阵

```cpp
// UVa10498 Happiness
// 刘汝佳
// 题目：幸福感 - 线性规划，使用单纯形法求最大值
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<cassert>
using namespace std;

// 改进单纯形法的实现
// 输入矩阵a描述标准线性规划形式：
// a为(m+1)×(n+1)矩阵，行0~m-1为不等式约束，行m为目标函数（最大化）
// 列0~n-1为变量系数，列n为常数项
// 第i个约束：a[i][0]*x[0] + ... + a[i][n-1]*x[n-1] ≤ a[i][n]
// 目标：max(a[m][0]*x[0] + ... + a[m][n-1]*x[n-1] - a[m][n])
// 变量均有非负约束：x[i] ≥ 0

const int maxm = 500;  // 约束数上限
const int maxn = 500;  // 变量数上限
const double INF = 1e100, eps = 1e-10;

struct Simplex {
  int n;               // 变量个数
  int m;               // 约束个数
  double a[maxm][maxn]; // 系数矩阵
  int B[maxm], N[maxn]; // B[i]=第i个基本变量, N[i]=第i个非基本变量

  // 以(r,c)为枢轴元素进行一次旋转操作（高斯消元）
  void pivot(int r, int c) {
    swap(N[c], B[r]);  // 交换基本变量和非基本变量
    a[r][c] = 1 / a[r][c];  // 枢轴元素取倒数
    // 更新第r行的其他元素
    for(int j = 0; j <= n; j++) if(j != c) a[r][j] *= a[r][c];
    // 更新其他行
    for(int i = 0; i <= m; i++) if(i != r) {
      for(int j = 0; j <= n; j++) if(j != c) a[i][j] -= a[i][c] * a[r][j];
      a[i][c] = -a[i][c] * a[r][c];
    }
  }

  // Phase I：寻找初始可行解
  // 迭代直到所有基本变量的常数项非负
  bool feasible() {
    for(;;) {
      int r, c;
      double p = INF;
      // 找常数项最小的约束（最违背非负条件的）
      for(int i = 0; i < m; i++) if(a[i][n] < p) p = a[r = i][n];
      if(p > -eps) return true;  // 所有常数项≥0，已可行
      // 在该行中找最负的非基本变量系数
      p = 0;
      for(int i = 0; i < n; i++) if(a[r][i] < p) p = a[r][c = i];
      if(p > -eps) return false;  // 无可行解
      // 选择出基变量（比例测试）
      p = a[r][n] / a[r][c];
      for(int i = r+1; i < m; i++) if(a[i][c] > eps) {
        double v = a[i][n] / a[i][c];
        if(v < p) { r = i; p = v; }
      }
      pivot(r, c);
    }
  }

  // Phase II：迭代优化目标函数
  // 返回值：1=有界最优解, 0=无解, -1=无界
  // b[i]=x[i]的值, ret=最优目标函数值
  int simplex(int n, int m, double x[maxn], double& ret) {
    this->n = n;
    this->m = m;
    for(int i = 0; i < n; i++) N[i] = i;       // 非基本变量
    for(int i = 0; i < m; i++) B[i] = n + i;   // 基本变量（松弛变量）
    
    if(!feasible()) return 0;  // Phase I失败
    
    for(;;) {
      int r, c;
      double p = 0;
      // 选择入基变量：目标函数系数最大的正系数
      for(int i = 0; i < n; i++) if(a[m][i] > p) p = a[m][c = i];
      if(p < eps) {  // 所有系数≤0，达到最优解
        for(int i = 0; i < n; i++) if(N[i] < n) x[N[i]] = 0;
        for(int i = 0; i < m; i++) if(B[i] < n) x[B[i]] = a[i][n];
        ret = -a[m][n];  // 注意目标函数常数项符号
        return 1;
      }
      // 选择出基变量：比例测试（Bland规则避免循环）
      p = INF;
      for(int i = 0; i < m; i++) if(a[i][c] > eps) {
        double v = a[i][n] / a[i][c];
        if(v < p) { r = i; p = v; }
      }
      if(p == INF) return -1;  // 目标函数无上界
      pivot(r, c);
    }
  }
};

//////////////// 题目相关
#include<cmath>
Simplex solver;

int main() {
  for(int n, m; scanf("%d%d", &n, &m) == 2;) {
    // 读入目标函数系数
    for(int i = 0; i < n; i++) scanf("%lf", &solver.a[m][i]);
    solver.a[m][n] = 0;  // 目标函数常数项设为0
    
    // 读入约束条件
    for(int i = 0; i < m; i++)
      for(int j = 0; j < n+1; j++)
        scanf("%lf", &solver.a[i][j]);
    
    double ans, x[maxn];
    assert(solver.simplex(n, m, x, ans) == 1);  // 确保有解
    
    ans *= m;  // 结果需乘以m
    printf("Nasa can spend %d taka.\n", (int)floor(ans + 1 - eps));
  }
  return 0;
}
// Accepted 10ms 2716 C++5.3.0 2020-12-12 22:39:36 25840427
```

## UVa11017 A Greener World

### 题目描述
给定一个整数多边形的顶点坐标（均为整数）、一个旋转角度θ和一个缩放因子d。要求计算在多边形内部有多少个点(x, y)满足：
- x和y的小数部分都是0.5（即形如 a+0.5, b+0.5 的格点半中心点）

同时输出多边形经过缩放和旋转后的真实面积。

### 解题思路
这是格点计数+面积计算的问题：
1. **面积计算**：使用多边形面积公式×三角形面积公式，输出`sin(θ)×d²×area2/2`
2. **半格点计数**（Pick定理的应用）：
   - 将原多边形旋转45度后变为稠密网格坐标系：`(x-y, x+y)`
   - 在半中心点(x+0.5, y+0.5)就变成了旋转后网格中的整数点
   - 然后用Pick定理求旋转后多边形内部的格点数
   - 减去原多边形内部的格点数（不包括恰好位于半中心点的）得到半中心点数

**Pick定理**：对于顶点为整数格点的简单多边形，面积A = I + B/2 - 1，其中I为内部格点数，B为边界格点数。

### 算法方法
**Pick定理 + 坐标变换**：
1. `PolygonArea2()`：计算多边形有向面积的2倍
2. `count_on_segment()`：计算线段上（不含端点）的格点数（gcd(|Δx|, |Δy|)-1）
3. `count_inside_polygon()`：用Pick定理计算多边形内部格点数
4. 坐标变换：`(x, y) → (x-y, x+y)`实现45度旋转变换

### 复杂度分析
- **时间复杂度**：O(N)，遍历多边形顶点一次
- **空间复杂度**：O(N)，存储多边形顶点

```cpp
// UVa11017 A Greener World
// Rujia Liu
// 题目：绿世界 - Pick定理计算多边形内部半中心格点数
#include <cmath>
#include <cstdio>
#include <vector>
using namespace std;

typedef long long LL;

const double PI = acos(-1.0);

// 整数坐标点
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
// 叉积（使用LL防溢出）
double Cross(const Vector& A, const Vector& B) {
  return (LL)A.x * B.y - (LL)A.y * B.x;
}

// 计算多边形有向面积的2倍（通过固定起点p[0]三角剖分）
LL PolygonArea2(const vector<Point>& p) {
  int n = p.size();
  LL area2 = 0;
  for (int i = 1; i < n - 1; i++)
    area2 += Cross(p[i] - p[0], p[i + 1] - p[0]);
  return abs(area2);  // 取绝对值（无向面积）
}

inline int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }

// 计算线段a-b上的格点数（不含端点）
// 公式：gcd(|Δx|, |Δy|) - 1
LL count_on_segment(const Point& a, const Point& b) {
  return gcd(abs(b.x - a.x), abs(b.y - a.y)) - 1;
}

// Pick定理：A = I + B/2 - 1 ⟹ I = A - B/2 + 1
// 计算多边形内部格点数
LL count_inside_polygon(const vector<Point>& poly) {
  int n = poly.size();
  LL A2 = PolygonArea2(poly);  // 面积的2倍
  int B = n;  // 边界格点：初始为顶点数
  for (int i = 0; i < n; i++)
    B += count_on_segment(poly[i], poly[(i + 1) % n]);  // 累加边上的格点
  return (A2 - B) / 2 + 1;  // Pick定理反求内部格点数
}

// 计算多边形内部x和y小数部分都是0.5的点的个数
// 方法：将多边形旋转45度（稠密网格），半中心点→整数格点
LL count(const vector<Point>& poly) {
  vector<Point> poly2;
  for (int i = 0; i < poly.size(); i++)
    // 坐标变换：旋转45度（稠密化）
    // (x+0.5, y+0.5) 在旋转后对应整数坐标
    poly2.push_back(Point(poly[i].x - poly[i].y, poly[i].x + poly[i].y));
  // 旋转后多边形内部格点总数 - 原多边形内部不含半中心的点数
  return count_inside_polygon(poly2) - count_inside_polygon(poly);
}

int main() {
  for (int d, theta, N, x, y; scanf("%d%d%d", &d, &theta, &N) == 3 && d;) {
    vector<Point> poly;
    for (int i = 0; i < N; i++)
      scanf("%d%d", &x, &y), poly.push_back(Point(x, y));
    LL area2 = PolygonArea2(poly);
    // 输出半中心格点数和实际面积
    printf("%lld %.0lf\n", count(poly),
           sin((double)theta / 180 * PI) * d * d * area2 / 2.0);
  }
  return 0;
}
// Accepted 1963 C++5.3.0 2020-12-1222:36:42|□25840418
```
