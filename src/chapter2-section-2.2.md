# 2.2 递推关系

## 例题4  多叉树遍历（Exploring Pyramids, NEERC 2005, Codeforces Gym101334E）

### 题目描述
考古学家发现了一座金字塔，内部的墙壁上刻有字母序列。已知金字塔内部的房间构成一棵多叉树：从根节点开始，按照深度优先搜索（DFS）的方式遍历整棵树，进入一个房间时写下该房间的字母，离开子树回到该房间时也写下该字母。给定最终得到的字母序列S，问有多少种不同的树结构能生成该序列。答案对10^9取模。

**输入**：每组一行，包含一个字符串S（|S| ≤ 300），每个字符是大写字母。输入以EOF结束。

**输出**：对于每组数据，输出可能的树结构数量模10^9。

### 解题思路

设S[0…n-1]为序列。如果S是一棵多叉树DFS遍历的结果，则S[0] = S[n-1] = 根节点字母，且序列长度n必须为奇数。

**区间DP/递推**：定义d[i][j]表示子串S[i…j]对应的子树的方案数。

初始条件：d[i][i] = 1（单节点子树，i=j表示到达叶子节点后退出）。

递推：若S[i] ≠ S[j]，则d[i][j] = 0（子树的DFS序列必须首尾相同，都是子树的根）。

若S[i] = S[j]，则需要枚举第一棵子树的右边界k（k从i+2到j，步长为2），使得S[i] = S[k]（第一棵子树的DFS序列以S[i]开头、S[k]结尾）。第一棵子树对应S[i+1…k-1]，方案数为d[i+1][k-1]；剩余子树森林对应S[k…j]，方案数为d[k][j]。两者相乘相加。

递推公式：
d[i][j] = Σ_{k=i+2}^{j} [S[i]==S[k]] · d[i+1][k-1] · d[k][j]

### 算法方法
- **递推/区间DP**：将问题分解为子树+森林的组合
- **Catalan数思想**：二叉或多叉树的DFS遍历与括号匹配有深刻联系
- **记忆化搜索**：避免重复计算子区间

### 复杂度分析
- **时间复杂度**：O(n³)，n≤300，三层循环（i,j,k）
- **空间复杂度**：O(n²)，用于存储所有子区间的DP值

```cpp
// 例题4  多叉树遍历（Exploring Pyramids, NEERC 2005, Codeforces Gym101334E）
// Rujia Liu
#include<cstdio>
#include<cstring>
using namespace std;

const int maxn = 300 + 10;
const int MOD = 1000000000;  // 模数10^9
typedef long long LL;

char S[maxn];
int d[maxn][maxn];  // d[i][j]: 子串S[i..j]对应的子树方案数

// 计算S[i..j]这段子串对应子树的方案数（记忆化搜索）
int dp(int i, int j) {
  if(i == j) return 1;  // 单节点子树，只有一种方案
  if(S[i] != S[j]) return 0;  // 子树DFS序列首尾必须相等（都是该子树的根节点字母）
  int& ans = d[i][j];  // 引用，方便记忆化存储
  if(ans >= 0) return ans;  // 已计算过，直接返回
  ans = 0;
  // 枚举第一棵子树的结束位置k，步长2（因为每棵子树长度必为奇数）
  for(int k = i+2; k <= j; k++) if(S[i] == S[k])
    // d[i+1][k-1]: 第一棵子树的方案数（去掉外层根节点S[i]=S[k]）
    // d[k][j]: 剩余森林（从k到j，包含k这棵子树根）的方案数
    ans = (ans + (LL)dp(i+1,k-1) * (LL)dp(k,j)) % MOD;
  return ans;
}

int main() {
  // NEERC题目要求文件输入输出
  freopen("exploring.in", "r", stdin);
  freopen("exploring.out", "w", stdout);
  while(scanf("%s", S) == 1) {
    memset(d, -1, sizeof(d));  // -1表示未计算（记忆化搜索标记）
    printf("%d\n", dp(0, strlen(S)-1));
  }
  return 0;
}
// 102083028 	Dec/23/2020 09:32UTC+8 	chenwz 	E - Exploring Pyramids 	GNU C++11 	Accepted 	61 ms 	300 KB 
```

## 例题7  串并联网络（Series-Parallel Networks, UVa 10253）

### 题目描述
串并联网络是一种由串联和并联两种操作递归构造的二端网络。网络有两个端点A和B。最基本的网络就是一条连接A和B的边（叶子网络）。n-叶子串并联网络是指恰好有n片叶子的网络（n个边），且这些叶子按以下方式构建：
- **串联**：将多个子网络首尾相连（A→网络1→网络2→…→B）
- **并联**：将多个子网络的两端分别连到A和B

给定叶子数n（1 ≤ n ≤ 30），问有多少种不同构的n-叶子串并联网络。注意：串联组合时子网络的顺序无关（视为相同网络），并联组合同样顺序无关。

**输入**：多组数据，每行一个n。n=0结束。

**输出**：对于每个n，输出方案总数。

### 解题思路

**核心递推**：设f[i]为i片叶子的串并联网络个数。

但光有f[i]还不够，需要引入辅助性DP：
设d[i][j]表示最多使用i片叶子的子树，总共组成j片叶子的方案数。
具体地，d[i][j] = 用不超过i片叶子的网络作为组件（component），组合成总叶子数为j的网络方案数。

**组合数学推导**：
对于串联（或并联）操作，我们选择若干个组件（组件之间顺序无关），每个组件有f[i]种可能。如果有p个i-叶子组件，从f[i]种网络中可重复地选p个的方案数是C(f[i]+p-1, p)（可重组合数，即stars and bars）。

递推过程：
1. d[i][0] = 1（0片叶子的空网络）
2. d[i][1] = 1（1片叶子的网络就是一条边）
3. 对于j ≥ 2：d[i][j] = Σ_{p=0}^{⌊j/i⌋} C(f[i]+p-1, p) · d[i-1][j-p·i]
   - 即：选p个i-叶子组件，剩余用更小叶子数的组件补齐
4. 最后f[i+1] = d[i][i+1]（i片叶子的组件通过串联/并联得到i+1片叶子的新网络）

注意：由于串联和并联是对称的，最终答案需要乘以2（除了只有1片叶子的特例）。

**关于组合数计算**：由于n≤30，可以直接用浮点数计算组合数并四舍五入（+0.5）转整数，精度足够。

### 算法方法
- **组合数学**：可重组合数 C(n+p-1, p)（stars and bars）
- **递推**：DP + 整数划分思想
- **生成函数**：实际上是在用指数生成函数的思想枚举组件组合

### 复杂度分析
- **时间复杂度**：O(n³)，n≤30，三层循环（i, j, p）均可接受
- **空间复杂度**：O(n²)，存储d数组

```cpp
// 例题7  串并联网络（Series-Parallel Networks, UVa 10253）
// Rujia Liu
#include<cstdio>
#include<cstring>

// 计算组合数C(n, m)，使用double防止溢出，结果+0.5四舍五入到整数
// 由于n≤30，double精度足够
long long C(long long n, long long m) {
  double ans = 1;
  // 分子：n*(n-1)*...*(n-m+1)
  for(int i = 0; i < m; i++)
    ans *= n-i;
  // 分母：m!
  for(int i = 0; i < m; i++)
    ans /= i+1;
  return (long long)(ans + 0.5);  // 四舍五入
}

const int maxn = 30 + 5;
// f[i]: i片叶子的网络方案数
// d[i][j]: 每棵树最多包含i个叶子，一共有j个叶子的方案数
long long f[maxn], d[maxn][maxn];

int main() {
  f[1] = 1;  // 1片叶子只有一条边
  memset(d, 0, sizeof(d));

  int n = 30;
  // 初始化边界
  for(int i = 0; i <= n; i++) d[i][0] = 1;  // 0片叶子：空网络
  for(int i = 1; i <= n; i++) { d[i][1] = 1; d[0][i] = 0; }

  for(int i = 1; i <= n; i++) {
    for(int j = 2; j <= n; j++) {
      d[i][j] = 0;
      // 枚举使用p个i-叶子组件
      for(int p = 0; p*i <= j; p++)
        // C(f[i]+p-1, p): 从f[i]种网络中可重复选p个的方案数（可重组合）
        // d[i-1][j-p*i]: 剩余叶子用更小叶子数的组件补齐
        d[i][j] += C(f[i]+p-1, p) * d[i-1][j-p*i];
    }
    // i片叶子的组件只能组合出i+1片叶子的网络（至少用一个i-叶子组件）
    f[i+1] = d[i][i+1];
  }

  while(scanf("%d", &n) == 1 && n)
    // 串联和并联是对称的，除了单叶子特例外需要乘以2
    printf("%lld\n", n == 1 ? 1 : 2*f[n]);
  return 0;
}
// 25877044  10253  Series-Parallel Networks  Accepted  C++  0.000  2020-12-23 01:33:19
```

## 例题6  葛伦堡博物馆（Glenbow Museum, World Finals 2008, UVa1073）

### 题目描述
博物馆的平面图是一个多边形，由若干内部夹角为90°或270°的房间组成。博物馆的墙壁平行于坐标轴。给定博物馆的总墙壁段数n（n为偶数，4 ≤ n ≤ 1000），问有多少种不同的博物馆平面图（即有多少种不同的正交多边形，周长由n段单位长度墙壁组成）。两个平面图视为相同当且仅当它们可以通过旋转和平移重合（即不考虑平移和旋转带来的差异）。

**输入**：多组数据，每组一行一个n。n=0结束。

**输出**：对于每组数据，输出"Case X: Y"，其中X为测试编号，Y为方案数。

### 解题思路

**问题转化**：将博物馆的墙壁转化为方向序列。在正交多边形中，每段墙壁是水平或垂直的。可以把水平段和垂直段交替出现的特点转化为序列问题。

**关键观察**：
- 用R表示"向右转"（顺时针旋转90°），用O表示"向左转"（逆时针旋转90°）。多边形的内部角要么是90°（外角270°→内角90°），要么是270°（外角90°→内角270°）。
- 将多边形用R/O序列描述：每个顶点处选择R或O
- 多边形总共n个顶点，R和O的总和为n
- 绕一圈回到起点，总旋转角度为360°，即(n_R - n_O)·90° = 360°，所以n_R - n_O = 4，结合n_R + n_O = n得：n_R = (n+4)/2，n_O = (n-4)/2
- 因此n必须是偶数且≥4，且(n+4)/2个R与(n-4)/2个O排列

**递推**：需要计数长度为n的RRR…序列满足：
- 恰好有R = (n+4)/2个R
- 不存在连续5个R（否则会形成一个贯穿洞，多边形不自交）
- 其他约束确保多边形不自交

使用DP：d[i][j][k]表示前i个顶点，已经连续出现了j个R，当前最后一个是否为R（k=0表示O，k=1表示R）的方案数。

最终答案ans[n] = d[R][3][0] + d[R][4][1] + d[R][4][0]，其中R = (n+4)/2。

解释：d[R][3][0]表示以O结尾（最后是O结尾保证没有5连续R）、最多连续3个R的方案；d[R][4][0]和d[R][4][1]分别是以O或R结尾但有4个连续R的情况。

### 算法方法
- **递推/DP**：状态转移DP，将几何约束转化为序列约束
- **组合数学**：将多边形遍历转化为R/O序列计数问题

### 复杂度分析
- **时间复杂度**：O(n·5·2)，n≤1000，预处理所有n
- **空间复杂度**：O(n·5·2)，DP数组

```cpp
// 例题6  葛伦堡博物馆（Glenbow Museum, World Finals 2008, UVa1073）
// Rujia Liu
#include<cstdio>
#include<cstring>
const int maxn = 1000;

// d[i][j][k]:
//   i: 已经放置的顶点数
//   j: 当前连续R的个数（0~4）
//   k: 当前顶点的类型 0=O(逆时针转), 1=R(顺时针转)
long long d[maxn+1][5][2], ans[maxn+1];

int main() {
  memset(d, 0, sizeof(d));
  // k=0和k=1两种起始状态分别DP
  for(int k = 0; k < 2; k++) {
    d[1][0][k] = 1;  // 第一个顶点只有一种情况
    for(int i = 2; i <= maxn; i++)
      for(int j = 0; j < 5; j++) {
        // 当前选择O（逆时针转），连续R计数归0
        d[i][j][k] = d[i-1][j][k];
        // 当前选择R（顺时针转），连续R计数+1
        if(j > 0) d[i][j][k] += d[i-1][j-1][k];
      }
  }

  memset(ans, 0, sizeof(ans));
  for(int i = 1; i <= maxn; i++) {
    if(i < 4 || i % 2 == 1) continue;  // 顶点数必须≥4且为偶数
    int R = (i+4)/2;  // 顺时针转(R)的个数 = (n+4)/2
    // d[R][3][0]: 以O结尾，最多连续3个R（不会出现连续5个R）
    // d[R][4][1]: 以R结尾，最多连续4个R（也是安全的）
    // d[R][4][0]: 以O结尾，连续4个R的情况
    ans[i] = d[R][3][0] + d[R][4][1] + d[R][4][0];
  }

  int n, kase = 1;
  while(scanf("%d", &n) == 1 && n)
    printf("Case %d: %lld\n", kase++, ans[n]);
  return 0;
}
// 25877043  1073  Glenbow Museum  Accepted  C++  0.000  2020-12-23 01:32:37
```

## 例题5  数字和与倍数（Investigating Div-Sum Property, UVa 11361）

### 题目描述
给定正整数a, b, k，求区间[a, b]中有多少个整数n满足：n能被k整除，且n的各位数字之和也能被k整除。

**输入**：第一行为测试组数T（T ≤ 100）。每组一行，包含三个整数a, b, k（1 ≤ a ≤ b < 2^31，0 < k < 10000）。

**输出**：对于每组数据，输出满足条件的整数个数。

### 解题思路

**数位DP（Digit DP）**：这是典型的数位统计问题，使用记忆化搜索处理。

设函数f(d, m1, m2)表示有d个数字位需要填充，数字之和除以k的余数为m1，整数本身除以k的余数为m2，满足条件的方案数。

递推：f(d, m1, m2) = Σ_{x=0}^{9} f(d-1, (m1-x) mod k, (m2-x·10^{d-1}) mod k)

边界：f(0, m1, m2) = 1当且仅当m1=m2=0（填完所有位且两个条件都满足）。

**统计区间**：使用标准数位DP技巧。定义sumf(n)返回[0, n)中满足条件的个数（左闭右开），则[a,b] = sumf(b+1) - sumf(a)。

sumf(n)的实现：逐位遍历n的十进制表示，固定高位后，统计低位任意填的方案数。

**优化**：特判k>85直接输出0，因为最大数字和=1+9×9=82（假设最多10位数字，2^31约10位）。

### 算法方法
- **递推/数位DP**：将计数问题分解为按位决策
- **模运算**：利用(a+b) mod k = ((a mod k) + (b mod k)) mod k的性质

### 复杂度分析
- **时间复杂度**：O(10·k²·log_b)，每组数据最多计算d·k·k个状态（d≈10位，k≤85）
- **空间复杂度**：O(10·90·90)，memo数组大小

```cpp
// 例题5  数字和与倍数（Investigating Div-Sum Property, UVa 11361）
// Rujia Liu
#include<cstdio>
#include<cstring>
using namespace std;

int MOD; // 题目中的k，重命名为MOD使代码语义更清晰
int pow10[10]; // 预计算10^0到10^9的值

// 整数n除以MOD的余数，返回0~MOD-1（处理负数取模情况）
int mod(int n) {
  return (n % MOD + MOD) % MOD;
}

// 记忆化数组：memo[d][m1][m2]
// d: 剩余要填充的数字位数
// m1: 当前已确定的数字之和除以MOD的余数
// m2: 当前已确定的整数除以MOD的余数
int memo[11][90][90];
int f(int d, int m1, int m2) {
  if(d == 0) return m1 == 0 && m2 == 0 ? 1 : 0;  // 边界：全部填完且余数均为0

  int& ans = memo[d][m1][m2];
  if(ans >= 0) return ans;  // 记忆化，已计算过
  ans = 0;
  // 枚举当前位填的数字x（0~9）
  for(int x = 0; x <= 9; x++)
    // 下一状态：d-1位，数字之和余数更新为(m1-x)mod k，数值余数更新为(m2-x*10^(d-1))mod k
    ans += f(d-1, mod(m1-x), mod(m2-x*pow10[d-1]));
  return ans;
}

// 统计0~n-1中满足条件的整数个数（左闭右开区间）
int sumf(int n) {
  char digits[11];
  sprintf(digits, "%d", n);  // 将整数转为字符串
  int nd = strlen(digits);    // 数字位数

  int base = 0; // 前缀固定部分的数值
  int sumd = 0; // 前缀固定部分的数字和
  int ans = 0;
  // 逐位枚举，构造小于n的所有符合条件的数
  for(int i = 0; i < nd; i++) {
    int na = nd - 1 - i; // 当前位之后还有na个自由位（星号位）
    // 当前位选择比digits[i]小的数字d
    for(int d = 0; d < digits[i] - '0'; d++) {
      // 需要满足：总的数字和 ≡ 0 (mod MOD)，总的数值 ≡ 0 (mod MOD)
      int cnt = f(na, mod(-sumd - d), mod(-base - d*pow10[na]));
      ans += cnt;
    }
    // 固定当前位为digits[i]的值，更新base和sumd
    base += (digits[i] - '0') * pow10[na];
    sumd += (digits[i] - '0');
  }
  return ans;
}

int main() {
  // 预计算10的幂
  pow10[0] = 1;
  for(int i = 1; i <= 9; i++) pow10[i] = pow10[i-1] * 10;

  int T;
  scanf("%d", &T);
  while(T--) {
    int a, b;
    scanf("%d%d%d", &a, &b, &MOD);
    memset(memo, -1, sizeof(memo));  // -1表示未计算
    // 数字和最大为1+9×9=82（10位数字的首位最多1），若MOD>82则无解
    if(MOD > 85) printf("0\n");
    else printf("%d\n", sumf(b+1) - sumf(a));  // 区间[a,b] = [0,b+1) - [0,a)
  }
  return 0;
}
// 25877033 	11361 	Investigating Div-Sum Property 	Accepted 	C++11 	0.020 	2020-12-23 01:24:34
```
