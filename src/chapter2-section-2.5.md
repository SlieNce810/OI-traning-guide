# 2.5 概率与数学期望

## UVa11021 Tribles

### 题目描述
有k个Tribble生物，每个Tribble只能存活一天。在它死亡之前，每个Tribble会繁殖出0到n-1个子代，繁殖i个子代的概率为p[i]（i=0,1,…,n-1，∑p[i]=1）。所有这些Tribble的后代都以相同的方式独立地生活和繁殖。问经过m天后所有Tribble都死亡的概率是多少。

**输入**：第一行T。每组一行n, k, m（1≤n,k,m≤1000）。接下来一行n个浮点数p[0],p[1],…,p[n-1]。

**输出**：对于每组数据，输出"Case #X: Y"，Y保留7位小数。

### 解题思路

**核心递推**：
设F[x] = 一只Tribble在x天后全部死亡的概率。

递推公式：
F[0] = 0（一只Tribble第一天死亡概率为0，因为它会在死亡时繁殖）
F[1] = p[0]（繁殖0个子代，第一天就全灭）

对于x ≥ 2：
F[x] = Σ_{i=0}^{n-1} p[i] · (F[x-1])^i

**推导**：一只Tribble繁殖i个子代的概率为p[i]。如果它繁殖了i个子代，那么这i个子代在x天后全部死亡的概率就是每只子代在x-1天后全灭概率的乘积 = (F[x-1])^i。对所有i的贡献求和。

**最终答案**：k只独立的Tribble在m天后全灭的概率 = (F[m])^k

### 算法方法
- **概率期望/递推**：定义状态函数，使用全概率公式递推
- 子代之间的独立性保证了概率相乘

### 复杂度分析
- **时间复杂度**：O(m·n)，对每个x需要累加n个概率
- **空间复杂度**：O(m)，存储F数组

```cpp
// UVa11021 Tribles
// 陈锋
#include <cmath>
#include <cstdio>
using namespace std;
typedef long long LL;
const int MAXN = 1000 + 4;
double P[MAXN], F[MAXN];  // P[i]: 繁殖i个子代的概率; F[x]: 1只Tribble在x天后全灭的概率

int main() {
  int T;
  scanf("%d", &T);
  for (int t = 1, n, k, m; t <= T; t++) {
    scanf("%d%d%d", &n, &k, &m);
    for (int i = 0; i < n; i++) scanf("%lf", &(P[i]));  // 读取繁殖概率
    F[0] = 0, F[1] = P[0];  // 边界：1天后全灭仅当繁殖0个
    for (int x = 2; x <= m; x++) {
      F[x] = 0;
      // 全概率公式：枚举繁殖的子代数i
      for (int i = 0; i < n; i++)
        F[x] += P[i] * pow(F[x - 1], i);  // p[i] * (F[x-1])^i
    }
    // k只独立的Tribble全灭概率 = (F[m])^k
    printf("Case #%d: %.7lf\n", t, pow(F[m], k));
  }
  return 0;
}
// 25838816 11021 Tribles Accepted C++ 0.050 2020-12-12 08:28:17
```

## UVa11427 Expect the Expected

### 题目描述
每天晚上玩一个游戏。每局游戏获胜的概率为p = a/b。每晚最多玩n局游戏，如果当晚胜率超过p就停止并去睡觉；如果玩完n局仍无法达到胜率p也去睡觉。游戏局数期望值是通过多天实验的平均来计算的。问平均每天需要玩多少天才能遇到一个"成功日"（即某晚在胜率超过p时停止），输出期望天数（取整）。（实际上，每天的最大局数有限，需要计算一天内玩完n局仍未成功的概率Q，然后期望天数=1/Q。）

**输入**：第一行T。每组一行"a/b n"（1 ≤ a ≤ b ≤ 100, 1 ≤ n ≤ 100）。

**输出**：对于每组数据，输出"Case #X: Y"，Y为期望天数（整数）。

### 解题思路

**递推公式**：
设D[i][j] = 玩了i局，赢了j局的概率（在未停止的情况下）。

初始：D[0][0] = 1, D[0][1] = 0

递推：对于第i局（1 ≤ i ≤ n），枚举赢得j局（0 ≤ j ≤ i），要求j/i ≤ p（即 j*b ≤ a*i，用乘法避免浮点数误差）：
D[i][j] = D[i-1][j]·(1-p) + D[i-1][j-1]·p

**一天内"失败"的概率Q**：Q = Σ_{j: j*b ≤ a*n} D[n][j]（即玩完n局仍未达到胜率>p的概率，也就是未能在该晚提前停止）。

**期望天数**：每天独立，每轮实验直到第一个成功日为止。由数学推导，期望天数 = 1/Q。（注意：代码中的Q是失败概率，不是成功概率；但期望天数恰好等于 1/失败概率。）

### 算法方法
- **概率期望/DP**：二维DP递推概率
- **几何分布期望**：期望 = 1/p

### 复杂度分析
- **时间复杂度**：O(n²)，二维DP
- **空间复杂度**：O(n²)，DP数组

```cpp
// UVa11427 Expect the Expected
// 刘汝佳
#include <cmath>
#include <cstdio>
#include <cstring>
const int NN = 100 + 5;
double D[NN][NN];  // D[i][j]: 玩了i局，赢了j局的概率（未停止前提下）

int main() {
  int T;
  scanf("%d", &T);
  for (int kase = 1, n, a, b; kase <= T; kase++) {
    scanf("%d/%d%d", &a, &b, &n);  // scanf支持"a/b"格式读取
    double p = (double)a / b;  // 单局胜率
    memset(D, 0, sizeof(D));
    D[0][0] = 1.0, D[0][1] = 0.0;  // 初始状态
    for (int i = 1; i <= n; i++)
      for (int j = 0; j * b <= a * i; j++) {  // 只枚举满足j/i ≤ a/b的j（使用乘法避免浮点误差）
        double &d = D[i][j];
        d = D[i - 1][j] * (1 - p);  // 第i局输，保持j胜
        if (j) d += D[i - 1][j - 1] * p;  // 第i局赢，从j-1胜转移
      }
    // 计算玩完n局仍未达到胜率>p的概率（即"失败日"概率）
    double Q = 0.0;
    for (int j = 0; j * b <= a * n; j++) Q += D[n][j];
    // Q是失败概率，需要成功概率P_success=1-Q
    // 但题意是：每晚某时刻胜率超过p则停止→失败=n局结束时仍≤p
    // 期望天数 = 1/(1-Q)
    printf("Case #%d: %d\n", kase, (int)(1 / Q));  // 期望天数 = 1/Q（Q为失败概率，数学推导得1/Q）
  }
  return 0;
}
// Accepted 10ms 739 C++5.3.0 2020-12-12 16:44:12 25838891
```

## UVa11722 Joining with Friend （限于篇幅，书上无此代码）

### 题目描述
两人约定在[t1, t2]时间段内见面，每人到达时间均匀分布在该区间内。到达后最多等w分钟，如果对方在w分钟内到达就见上面，否则离开。求两人能见面的概率。

**输入**：第一行T。每组五个整数t1, t2, s1, s2, w（实际期望时间范围，但s1=s2-w?）。实际输入为浮点数值。

**输出**：对于每组数据，输出"Case #X: Y"，Y保留6位小数。

### 解题思路

**几何概型**：
设x为第一个人到达时刻（均匀分布在[t1,t2]），y为第二个人到达时刻（均匀分布在[s1,s2]）。矩形区域面积为width=(t2-t1)，height=(s2-s1)。

见面的条件是：|x - y| ≤ w，即 y - w ≤ x ≤ y + w。

这是矩形内满足|x-y|≤w的区域面积除以总面积。

**面积计算**：
矩形(t1,t2)×(s1,s2)内，满足条件|x-y|≤w的区域是两条直线y=x+w和y=x-w之间的条带与矩形的交集。

函数get_area(w)计算y=x+w上方被矩形截得的面积（即y>x+w的区域面积）。那么：
- 满足|x-y|≤w的面积 = get_area(-w) - get_area(w)
- 概率 = (get_area(-w) - get_area(w)) / (width·height)

**get_area(w)的几何实现**：计算直线y=x+w与矩形四条边交点的位置关系，分情况用三角形或梯形面积公式计算。

### 算法方法
- **概率期望/几何概型**：将概率问题转化为面积比
- **计算几何**：直线与矩形的交点及其面积计算

### 复杂度分析
- **时间复杂度**：O(1)每组数据
- **空间复杂度**：O(1)

```cpp
// UVa11722 Joining with Friend （限于篇幅，书上无此代码）
// Rujia Liu
#include<cstdio>
double t1, t2, s1, s2, width, height;  // 时间区间和矩形尺寸

// 计算直线y = x + w上方被矩形(s1,t1)-(s2,t2)切割得到的面积
double get_area(double w) {
  double ly = t1+w, ry = t2+w; // 左右边界交点的y坐标
  double tx = s2-w, bx = s1-w; // 上下边界交点的x坐标
  // 判断4个交点是否在矩形边上
  bool on_left   = s1 <= ly && ly <= s2;   // 左交点在矩形左边线上
  bool on_right  = s1 <= ry && ry <= s2;   // 右交点在矩形右边线上
  bool on_top    = t1 <= tx && tx <= t2;   // 上交点在矩形上边线上
  bool on_bottom = t1 <= bx && bx <= t2;   // 下交点在矩形下边线上

  // 四种情况的面积计算
  if(on_left && on_right)   // 直线穿过左右两边 → 梯形
    return (s2 - ly + s2 - ry) * width * 0.5;
  if(on_left && on_top)     // 直线穿过左边和上边 → 三角形
    return (s2 - ly) * (tx - t1) * 0.5;
  if(on_top && on_bottom)   // 直线穿过上边和下边 → 梯形
    return (bx - t1 + tx - t1) * height * 0.5;
  if(on_right && on_bottom) // 直线穿过右边和下边 → 矩形减去三角形
    return height * width - (t2 - bx) * (ry - s1) * 0.5;

  // 直线完全在矩形上/下方
  return ly <= s1 ? width * height : 0;
}

int main() {
  int T, kase = 1;
  scanf("%d", &T);
  while(T--) {
    double w;
    scanf("%lf%lf%lf%lf%lf", &t1, &t2, &s1, &s2, &w);
    width = t2 - t1;    // 矩形宽度
    height = s2 - s1;   // 矩形高度
    double a1 = get_area(w);   // y > x+w 的面积
    double a2 = get_area(-w);  // y > x-w 的面积（等价于y-w > x）
    // 满足|x-y|≤w的面积 = a2 - a1，概率 = 面积/总面积
    printf("Case #%d: %.6lf\n", kase++, (a2 - a1) / width / height);
  }
  return 0;
}
```

## UVa11762 Race To 1

### 题目描述
有一个正整数N，每次操作如下：如果N=1，停止；否则，等概率地选择一个不超过N的素数p。如果p|N，则将N替换为N/p；否则N保持不变。求将N变为1所需操作次数的数学期望。

**输入**：第一行T（T ≤ 1000）。接下来T行，每行一个整数N（1 ≤ N ≤ 10^6）。

**输出**：对于每组数据，输出"Case X: Y"，Y保留10位小数。

### 解题思路

**期望DP**：
设F[x]为从x变到1所需的期望操作次数。

边界：F[1] = 0

递推公式推导：
设不超过x的素数总数为p(x)，其中能整除x的素数个数为g(x)。

在一次操作中：
- 以概率g(x)/p(x)命中整除x的素数，转移到状态x/p（各种p）
- 以概率1-g(x)/p(x)选到不能整除x的素数，保持x不变（操作浪费了）

因此：
F[x] = 1 + (1/p(x))·Σ_{p|x} F[x/p] + (1-g(x)/p(x))·F[x]

化简：
g(x)/p(x)·F[x] = 1 + (1/p(x))·Σ_{p|x} F[x/p]
F[x] = (p(x) + Σ_{p|x} F[x/p]) / g(x)

**实现**：使用记忆化搜索（或DP递推）。预计算素数表，对于每个x枚举不超过x的素数来计算p(x)和g(x)。

### 算法方法
- **概率期望/DP**：全期望公式 + 递推化简
- **筛法**：预计算素数表

### 复杂度分析
- **时间复杂度**：O(N·π(N)/ln N)，每个x枚举所有不超过x的素数，但只计算需要的状态
- **空间复杂度**：O(N)，F数组和素数表

```cpp
// UVa11762 Race To 1
// 陈锋
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstring>
using namespace std;

const int NN = 1e6 + 10;
double F[NN];     // F[x]: x变到1的期望操作次数
int IsPrime[NN], primes[NN], vis[NN];  // vis[x]: 标记是否已计算F[x]

// 埃氏筛生成素数表
void gen_primes(int n) {
  fill_n(IsPrime, n + 1, 1);
  for (int i = 2, p = 0; i <= n; i++) {
    if (!IsPrime[i]) continue;
    primes[p++] = i;  // 记录素数
    if (i <= n / i)
      for (int j = i * i; j <= n; j += i) IsPrime[j] = 0;  // 筛去合数
  }
}

// 记忆化搜索计算F[x]（期望DP）
double dp(int x) {
  double& f = F[x];
  if (x == 1) return 0.0;  // 边界条件
  if (vis[x]) return f;    // 已计算过，避免重复
  vis[x] = 1;              // 标记为已访问

  int g = 0, p = 0;  // g: 能整除x的素数个数; p: 不超过x的素数总数
  f = 0;
  // 枚举所有不超过x的素数
  for (int i = 0; primes[i] <= x; i++) {
    p++;  // 素数计数
    if (x % primes[i] == 0)  // 该素数整除x
      g++, f += dp(x / primes[i]);  // 累加F[x/prime]
  }
  // F[x] = (p(x) + Σ_{p|x} F[x/p]) / g(x)
  return f = (f + p) / g;
}

int main() {
  int T;
  scanf("%d", &T);
  gen_primes(NN - 1), fill_n(vis, NN, 0);  // 预处理
  for (int kase = 1, n; kase <= T; kase++) {
    scanf("%d", &n);
    printf("Case %d: %.10lf\n", kase, dp(n));
  }
  return 0;
}
// Accepted 190ms 964 C++ 5.3.0 2020-12-12 16:51:29 25838925
```
