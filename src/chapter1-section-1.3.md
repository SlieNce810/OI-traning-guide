# 1.3 高效算法设计举例

## 例题25  侏罗纪（Jurassic Remains, NEERC 2003, Codeforces Gym101388J）

### 题目描述

有 n 个字符串（n ≤ 24），每个字符串只包含大写字母。需要选出尽量多的字符串，使得选出的字符串中每个字母的出现总次数都是偶数。求最大可选数量和具体方案。

**输入格式**：多组数据（文件 jurassic.in）。每组第一行 n，n=0 结束。接下来 n 行，每行一个字符串。

**输出格式**：第一行输出最大数量，第二行按编号输出所选字符串（1-indexed），空格分隔。

### 解题思路

**1. 字符串编码为位向量**

每个字母的奇偶性用 1 位表示（26 个字母，需要 26 位，可用 int 表示）。对于每个字符串，计算其包含字母的奇偶位掩码：`A[i] = XOR(1 << (ch - 'A'))`。

问题转化为：找出最多的位向量，使得它们的 XOR 和为 0。

**2. 中途相遇法（Meet in the Middle）**

n ≤ 24，但 2^24 ≈ 1.6×10⁷，直接枚举所有子集太快亦可能超时（但对 24 确实可行）。更高效的方法是将 n 分成两半：
- 前 n/2 个，枚举所有 2^(n/2) 个子集，计算 XOR 值，记录到 hash map 中
- 后 n/2 个，枚举所有 2^(n/2) 个子集，在 hash map 中查找与其 XOR 值相同的子集，合并得到更大的合法子集

**3. 合并条件**

前一半子集的 XOR 为 x，后一半子集的 XOR 为 y。如果 x == y，则 x XOR y = 0，即两半合起来 XOR 为 0，所有字母出现偶数次。取子集大小最大的。

### 算法方法

**1. 中途相遇法（Meet in the Middle）**
- 将 2^n 的搜索空间分成两个 2^(n/2)，大幅降低复杂度
- 用 hash map 存储前一半的结果，O(1) 查找配对

**2. 位运算 / 状态压缩**
- 每个字符串编码为一个 26 位的 bitmask
- XOR 运算天然表示奇偶性变化

**3. 哈希表优化**
- 对于同一 XOR 值，只需保留子集大小最大的那个
- 使用 map 实现

### 复杂度分析

- **时间复杂度**：O(2^(n/2) × n)。前半部分枚举 2^12 = 4096，后半部分枚举 2^12 = 4096。每子集 O(n) 计算 XOR，总计约 2×10⁵。
- **空间复杂度**：O(2^(n/2))。hash map 存储前一半所有子集。

```cpp
// 例题25  侏罗纪（Jurassic Remains, NEERC 2003, Codeforces Gym101388J）
// Rujia Liu
#include<cstdio>
#include<map>
using namespace std;

const int maxn = 24;  // n ≤ 24
// table: XOR值 → 子集掩码（记录最优子集）
// key = 前一半子集的XOR值, value = 该XOR值对应的具有最多元素的子集掩码
map<int,int> table;

// 计算二进制中1的个数（集合大小）
int bitcount(int x) { return x == 0 ? 0 : bitcount(x/2) + (x&1); }

int main() {
  int n, A[maxn];
  char s[1000];

  freopen("jurassic.in", "r", stdin);
  freopen("jurassic.out","w",stdout);

  while(scanf("%d", &n) == 1 && n) {
    // ---- 输入并计算每个字符串对应的位向量 ----
    for(int i = 0; i < n; i++) {
      scanf("%s", s);
      A[i] = 0;
      for(int j = 0; s[j] != '\0'; j++)
        A[i] ^= (1<<(s[j]-'A'));  // XOR：每个字母切换奇偶位
      // 最终A[i]中为1的位表示该字母出现了奇数次
    }

    // ---- 中途相遇法 第一阶段：前半部分 ----
    // table[x]保存的是xor值为x的、元素数量最多的子集掩码
    table.clear();
    int n1 = n/2, n2 = n-n1;  // 将n分成两半
    for(int i = 0; i < (1<<n1); i++) {  // 枚举前n1个的所有子集(2^n1种)
      int x = 0;  // 当前子集的XOR值
      for(int j = 0; j < n1; j++)
        if(i & (1<<j)) x ^= A[j];  // 子集包含第j个元素，XOR上它
      // 对于同一XOR值，保留元素更多的子集
      if(!table.count(x) || bitcount(table[x]) < bitcount(i))
        table[x] = i;
    }

    // ---- 中途相遇法 第二阶段：后半部分 + 合并 ----
    int ans = 0;  // 最终最优子集掩码
    for(int i = 0; i < (1<<n2); i++) {  // 枚举后n2个的所有子集
      int x = 0;
      for(int j = 0; j < n2; j++)
        if(i & (1<<j)) x ^= A[n1+j];  // 后半部分的XOR值
      // 如果前半部分存在相同XOR的子集，则合并后XOR=0（合法）
      if(table.count(x) &&
         bitcount(ans) < bitcount(table[x]) + bitcount(i))
        ans = (i<<n1) ^ table[x];  // 合并：左移n1位拼接两个子集掩码
    }

    // ---- 输出结果 ----
    printf("%d\n", bitcount(ans));  // 最多选择多少个
    for(int i = 0; i < n; i++)
      if(ans & (1<<i)) printf("%d ", i+1);  // 输出所选编号(1-indexed)
    printf("\n");
  }
  return 0;
}
// 102052000	Dec/22/2020 22:56UTC+8	chenwz	J - Jurassic Remains	GNU C++11	Accepted	31 ms	300 KB
```

## 例题22  最大子矩阵（City Game, SEERC 2004, LA3029/POJ1964）

### 题目描述

给定一个 m×n（m,n ≤ 1000）的网格，每个格子要么是空地 `F`，要么是障碍 `R`。需要找一个全为空地的矩形子区域，求其最大面积（单位：格子数），输出面积 × 3 的结果。

**输入格式**：第一行 T，测试用例数。每组第一行 m 和 n，接下来 m 行每行 n 个字符（`F` 或 `R`），字符间可能有空格。

**输出格式**：每组输出一行，整数表示最大矩形面积 × 3。

### 解题思路

**1. 转化：处理每一行**

对于每个位置 (i, j)，定义：
- `up[i][j]`：从 (i, j) 向上延伸的最长连续空地长度
- `left[i][j]`：以 up[i][j] 为高度的矩形，其左边界能延伸到的最左位置
- `right[i][j]`：以 up[i][j] 为高度的矩形，其右边界能延伸到的最右位置

**2. 逐行递推**

从左到右扫描第 i 行：
- 如果 (i,j) 是障碍，up=0, left=0
- 如果 (i,j) 是空地：
  - `up[i][j] = up[i-1][j] + 1`（第一行则为 1）
  - `left[i][j] = max(left[i-1][j], lo+1)`（lo 是最近障碍的列号）
  
从右到左扫描更新 right，并计算面积：
- `right[i][j] = min(right[i-1][j], ro-1)`（ro 是最近障碍的列号）
- `area = up[i][j] × (right[i][j] - left[i][j] + 1)`

**3. 关键洞察**

`left[i][j]` 维护的是"高度为 up[i][j] 的柱子能向左延伸多远"。由于上方的 left 限制了下方，使用 max 取限制。right 同理但用 min。

### 算法方法

**1. 悬线法 / 单调栈思想的递推实现**
- 维护每个位置的 up、left、right 三个值
- 逐行递推 O(nm)，比枚举上下界 O(n²) 高效

**2. 递推约束传递**
- left 从上向下传递时取 max（更严格的约束）
- right 从上向下传递时取 min

### 复杂度分析

- **时间复杂度**：O(m × n)。每行两次扫描（左到右、右到左），每次 O(n)，共 m 行。
- **空间复杂度**：O(m × n)。三个 m×n 数组存储 up、left、right。

```cpp
// 例题22  最大子矩阵（City Game, SEERC 2004, LA3029/POJ1964）
// 刘汝佳
#include <algorithm>
#include <cstdio>
using namespace std;

const int maxn = 1000;
// mat[i][j]: 0=空地(F), 1=障碍(R)
// up[i][j]: 从(i,j)向上延伸的连续空地长度
// left[i][j]: 高度为up[i][j]的矩形左边界
// right[i][j]: 高度为up[i][j]的矩形右边界
int mat[maxn][maxn], up[maxn][maxn], left[maxn][maxn], right[maxn][maxn];

int main() {
  int T;
  scanf("%d", &T);
  while (T--) {
    int m, n;
    scanf("%d%d", &m, &n);
    // ---- 输入阶段：读取网格 ----
    for (int i = 0; i < m; i++)
      for (int j = 0; j < n; j++) {
        int ch = getchar();
        while (ch != 'F' && ch != 'R') ch = getchar();  // 跳过空格和换行
        mat[i][j] = ch == 'F' ? 0 : 1;  // F=0(空地), R=1(障碍)
      }

    int ans = 0;
    // ---- 逐行递推阶段 ----
    for (int i = 0; i < m; i++) {  // 从上到下逐行处理
      int lo = -1, ro = n;  // lo: 左侧最近障碍列; ro: 右侧最近障碍列

      // ---- 从左到右扫描：计算 up 和 left ----
      for (int j = 0; j < n; j++)
        if (mat[i][j] == 1) {  // 障碍
          up[i][j] = left[i][j] = 0;  // 高度和左边界清零
          lo = j;  // 更新最近障碍位置
        } else {  // 空地
          up[i][j] = i == 0 ? 1 : up[i - 1][j] + 1;  // 向上延伸高度+1
          // 左边界受限于：上一行同列的左边界 或 本行左侧最近的障碍
          left[i][j] = i == 0 ? lo + 1 : max(left[i - 1][j], lo + 1);
        }

      // ---- 从右到左扫描：计算 right 并更新答案 ----
      for (int j = n - 1; j >= 0; j--)
        if (mat[i][j] == 1) {  // 障碍
          right[i][j] = n;
          ro = j;  // 更新最近障碍位置
        } else {  // 空地
          // 右边界受限于：上一行同列的右边界 或 本行右侧最近的障碍
          right[i][j] = i == 0 ? ro - 1 : min(right[i - 1][j], ro - 1);
          // 面积 = 高度 × 宽度，取最大值
          ans = max(ans, up[i][j] * (right[i][j] - left[i][j] + 1));
        }
    }
    printf("%d\n", ans * 3);  // 输出最大面积乘以3（题目要求）
  }
  return 0;
}
// Accepted 32ms 15988kB 1252 G++ 2020-12-08 21:55:10 22197363
```

## 例题21  子序列（Subsequence, SEERC 2006, POJ3061）

### 题目描述

给定一个长度为 n 的正整数序列 A[1..n]（n ≤ 10⁵，A[i] ≤ 10⁴），和一个目标值 S（S ≤ 10⁸）。求满足连续子序列之和 ≥ S 的最短长度。如果不存在这样的子序列，输出 0。

**输入格式**：第一行 T，测试用例数。每组第一行两个整数 n 和 S，接下来一行 n 个整数。

**输出格式**：每组输出一行，一个整数表示最短长度，不存在则输出 0。

### 解题思路

**1. 前缀和转化**

设前缀和 `B[i] = sum(A[1..i])`，则区间 [l, r] 的和 = `B[r] - B[l-1]`。原问题转化为：找满足 `B[r] - B[l-1] ≥ S` 的最小 `r - l + 1`。

**2. 双指针/滑动窗口**

使用两个指针 i（左端点）和 j（右端点）：
- 对于每个 j，找到最小的 i 使得 `B[i] ≤ B[j] - S`（即区间 [i+1, j] 的和 ≥ S）
- 由于 A[i] 为正，B 单调递增，i 可以单调移动

**3. 实现技巧**

使用二分或直接递增 i。这里采用递增 i：对于每个 j，如果 `B[i-1] > B[j] - S`，则当前没有更短的区间，跳过；否则不断增大 i 直到条件不满足，然后取 `j - i + 1` 更新答案。

### 算法方法

**1. 前缀和**
- 将区间和查询转化为 O(1) 的减法操作
- B 数组的单调性保证算法的正确性

**2. 双指针 / 滑动窗口**
- 两个指针均单调右移，每个元素被访问常数次
- 实现 O(n) 的线性扫描

### 复杂度分析

- **时间复杂度**：O(n)。每个元素最多被左指针和右指针各访问一次。
- **空间复杂度**：O(n)。需要存储 A 数组和 B 前缀和数组。

```cpp
// 例题21  子序列（Subsequence, SEERC 2006, POJ3061）
// 陈锋
#include <algorithm>
#include <cstdio>
using namespace std;

const int maxn = 1e5 + 8;
int A[maxn], B[maxn], T;  // A: 原数组; B: 前缀和 B[i]=sum(A[1..i])

int main() {
  scanf("%d", &T);
  for (int n, S; scanf("%d%d", &n, &S) == 2 && T--;) {
    for (int i = 1; i <= n; i++) scanf("%d", &A[i]);

    // ---- 计算前缀和：B[i] = sum(A[1..i]) ----
    B[0] = 0;
    for (int i = 1; i <= n; i++) B[i] = B[i - 1] + A[i];

    // ---- 双指针扫描：找最小长度子序列 ----
    int ans = n + 1;  // 初始化为不可能的大值
    int i = 1;  // 左指针(实际上i-1是左边界)
    for (int j = 1; j <= n; j++) {  // j是右边界
      // (1) 如果当前i-1不满足条件(B[i-1] > B[j]-S)，说明不存在更短的区间
      // 跳过，等j增大后才可能满足
      if (B[i - 1] > B[j] - S) continue;

      // (2) 单调增大i，找到使B[i-1] ≤ B[j]-S的最大i
      // 即区间[i, j]的和 = B[j]-B[i-1] ≥ S
      while (B[i] <= B[j] - S) i++;

      // 区间长度为 j - i + 1（注意i已被增加到不满足条件的位置）
      ans = min(ans, j - i + 1);
    }
    printf("%d\n", ans == n + 1 ? 0 : ans);  // 无解输出0
  }
  return 0;
}
// Accepted 79ms 1104kB 731 G++2020-12-24 10:55:33 22229063
```

## 例题23  遥远的银河（Distant Galaxy, Shanghai 2006, POJ3141/LA3695）

### 题目描述

平面上有 n 个点（n ≤ 100）。需要找一个矩形边界（四条直线 x=x1, x=x2, y=y1, y=y2），使得边界上和边界内的点数最多。求这个最大值。

**输入格式**：多组数据。每组第一行为 n，n=0 结束。接下来 n 行每行两个整数 (x, y)，坐标范围 [-10⁹, 10⁹]。

**输出格式**：每组输出 `Case X: Y`，X 编号，Y 为最大值。

### 解题思路

**1. 简化为逐对水平线枚举**

枚举矩形的上下边界 ymin = y[a], ymax = y[b]（a < b，不同的 y 值）。然后扫描 x 坐标：
- 对于每条竖线（同一 x 的多个点组），统计：
  - `on[k]`：严格在边界内部的点数
  - `on2[k]`：在边界上或内部的点数
  - `left[k]`：当前竖线左边的在边界上的点数累计

**2. 动态规划扫描**

对于每个 x 坐标的竖线，计算：
- `left[k] = left[k-1] + on2[k-1] - on[k-1]`

最终答案 = max(left[j] + on2[j] + max(on[i] - left[i]))（i < j）
其中 `M = max(on[j] - left[j])` 在扫描过程中维护。

**3. 核心方程解析**

设选定矩形在竖线 j 处结束，在竖线 i 处开始，则：
总点数 = (左边界的点) + (内部x在[i+1..j]的点) + (右边界的点)
= left[j] - left[i] + on2[j] + on2[i]

### 算法方法

**1. 枚举 + 动态规划**
- O(m²) 枚举上下界（m ≤ n 为不同 y 的数量）
- O(n) 扫描 x 方向

**2. 前缀和 / 扫描线**
- left 数组本质是前缀和
- 在扫描中维护 M 值实现 O(k) 每次

### 复杂度分析

- **时间复杂度**：O(n³)。枚举上下界 O(m²)（m ≤ n），每次扫描 O(k)（k 为不同 x 数量），最坏 O(n³)。n ≤ 100，100³ = 10⁶，可接受。
- **空间复杂度**：O(n)。存储点数组和辅助数组。

```cpp
// 例题23  遥远的银河（Distant Galaxy, Shanghai 2006, POJ3141/LA3695）
// Rujia Liu
#include<cstdio>
#include<algorithm>
using namespace std;

struct Point {
  int x, y;
  bool operator < (const Point& rhs) const {
    return x < rhs.x;  // 按x排序，便于扫描
  }
};

const int maxn = 100 + 10;
Point P[maxn];  // 所有点
int n, m;
int y[maxn];    // 所有不同的y坐标值（排序去重后）
// on[k]: 第k条竖线上严格在(ymin, ymax)内部的点数
// on2[k]: 第k条竖线上在[ymin, ymax]内部或边界上的点数
// left[k]: 第k条竖线左边在线边界上的点数
int on[maxn], on2[maxn], left[maxn];

int solve() {
  // ---- 预处理：排序并去重 ----
  sort(P, P+n);       // 按x坐标排序
  sort(y, y+n);       // 提取并排序y坐标
  m = unique(y, y+n) - y;  // 去重，m=不同y坐标的数量
  if(m <= 2) return n;     // 只有1或2种y→所有点都在一个水平带内，直接取全部

  int ans = 0;
  // ---- 枚举上下边界 ----
  for(int a = 0; a < m; a++)
    for(int b = a+1; b < m; b++) {
      int ymin = y[a], ymax = y[b];  // 上下边界

      // ---- 按x坐标分组扫描 ----
      int k = 0;  // 竖线计数（不同x值的组数）
      for(int i = 0; i < n; i++) {
        if(i == 0 || P[i].x != P[i-1].x) {  // 新的竖线（x值变化）
          k++;
          on[k] = on2[k] = 0;  // 初始化新竖线的统计
          // left[k]: 第k条竖线左边在边界上的点数
          // 由前一竖线的left + 前一竖线边界上但不算入内部的点(边界点)
          left[k] = k == 0 ? 0 : left[k-1] + on2[k-1] - on[k-1];
        }
        // 统计当前点属于哪个区域
        if(P[i].y > ymin && P[i].y < ymax) on[k]++;   // 严格在内部
        if(P[i].y >= ymin && P[i].y <= ymax) on2[k]++; // 在内部或边界上
      }
      if(k <= 2) return n;  // 只有1或2列，直接取全部

      // ---- 动态规划扫描：维护最佳左边界 ----
      int M = 0;  // M = max(on[j] - left[j])，表示最佳左边界贡献
      for(int j = 1; j <= k; j++) {
        // ans = max(left[j] + on2[j] + max(on[i]-left[i])) (i < j)
        ans = max(ans, left[j] + on2[j] + M);
        M = max(M, on[j] - left[j]);  // 更新最佳值
      }
    }
  return ans;
}

int main() {
  int kase = 0;
  while(scanf("%d", &n) == 1 && n) {
    for(int i = 0; i < n; i++) {
      scanf("%d%d", &P[i].x, &P[i].y);
      y[i] = P[i].y;  // 同时提取y坐标
    }
    printf("Case %d: %d\n", ++kase, solve());
  }
  return 0;
}
// Accepted 16ms 352kB 1338 G++2020-12-22 22:50:02 22226059
```

## UVa10755 Garbage heap

### 题目描述

给定一个 A×B×C（A,B,C ≤ 20）的三维长方体，每个格子有一个整数值（正负均可，long long 范围）。求一个**非空子长方体**，使得其数值之和最大（三维最大子段和）。

**输入格式**：第一行 T，测试用例数。每组第一行三个整数 A, B, C，接下来依次给出所有格子的值（按层、行、列的顺序）。

**输出格式**：每组输出一行最大和，测试用例间空一行。

### 解题思路

**1. 降维策略**

三维最大子段和可以降维为二维最大子段和：
- 枚举 x 方向的上下界 (x1, x2)，将三维压缩成二维
- 在二维平面上做最大子矩阵和，进一步压缩成一维

**2. 三维前缀和**

使用三维前缀和快速计算任意子长方体的和：
- `S[x][y][z] =` 前缀和（需要容斥原理计算）
- 子长方体 (x1,x2, y1,y2, z1,z2) 的和可通过 8 个前缀和项计算

**3. 一维最大子段和**

固定 x1, x2 和 y1, y2 后，问题变成一维：在 z 方向找最大子段和。经典算法：
- 维护当前和 cur 和最小前缀 minS
- ans = max(ans, cur - minS)

**4. 八重循环的结构**

枚举 x1(1..A) → x2(x1..A) → y1(1..B) → y2(y1..B) → z方向扫描(C)。总体 O(A²B²C)，当 A=B=C=20 时约 20⁵ = 3,200,000，可接受。

### 算法方法

**1. 三维前缀和（容斥原理）**
- 3D 前缀和有 2³ = 8 项参与计算
- 用 expand 和 sign 函数处理容斥符号

**2. 降维 + 最大子段和**
- 三维 → 二维（枚举 x 范围）→ 一维（枚举 y 范围）→ Kadane算法
- 逐层降维是处理高维子段和问题的标准技巧

### 复杂度分析

- **时间复杂度**：O(A² × B² × C)。A,B,C ≤ 20，最坏约 20⁵ = 3.2×10⁶。
- **空间复杂度**：O(A × B × C)。存储三维前缀和数组。

```cpp
// UVa10755 Garbage heap
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<algorithm>
#define FOR(i,s,t)  for(int i = (s); i <= (t); ++i)
using namespace std;

// 分解3位二进制：i的低3位分别对应b0,b1,b2（容斥原理的符号位）
void expand(int i, int& b0, int& b1, int& b2) {
  b0 = i&1; i >>= 1;
  b1 = i&1; i >>= 1;
  b2 = i&1;
}

// 容斥符号：奇数个1为+1，偶数个1为-1
int sign(int b0, int b1, int b2) {
  return (b0 + b1 + b2) % 2 == 1 ? 1 : -1;
}

const int maxn = 30;
const long long INF = 1LL << 60;  // 足够大的值

long long S[maxn][maxn][maxn];  // 三维前缀和

// 三维前缀和查询：子长方体(x1..x2, y1..y2, z1..z2)的元素和
// 容斥原理8个顶点，sign决定加减
long long sum(int x1, int x2, int y1, int y2, int z1, int z2) {
  int dx = x2-x1+1, dy = y2-y1+1, dz = z2-z1+1;
  long long s = 0;
  for(int i = 0; i < 8; i++) {  // 8个容斥顶点
    int b0, b1, b2;
    expand(i, b0, b1, b2);
    // S[x2-b0*dx][y2-b1*dy][z2-b2*dz]
    // b0=0时取x2（最大），b0=1时取x1-1（最小-1）
    s -= S[x2-b0*dx][y2-b1*dy][z2-b2*dz] * sign(b0, b1, b2);
  }
  return s;
}

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    int a, b, c, b0, b1, b2;
    scanf("%d%d%d", &a, &b, &c);
    memset(S, 0, sizeof(S));

    // ---- 读入三维数组 ----
    FOR(x,1,a) FOR(y,1,b) FOR(z,1,c)
      scanf("%lld", &S[x][y][z]);

    // ---- 计算三维前缀和 ----
    // S[x][y][z] = 原值 + 累加所有低维前缀和（容斥）
    FOR(x,1,a) FOR(y,1,b) FOR(z,1,c)
      FOR(i,1,7){  // 7种低维情况（除(0,0,0)外的所有组合）
        expand(i, b0, b1, b2);
        S[x][y][z] += S[x-b0][y-b1][z-b2] * sign(b0, b1, b2);
      }

    // ---- 枚举x和y范围，z方向做一维最大子段和 ----
    long long ans = -INF;
    FOR(x1,1,a) FOR(x2,x1,a)       // 枚举x方向上下界
      FOR(y1,1,b) FOR(y2,y1,b) {   // 枚举y方向上下界
        long long M = 0;  // 维护当前最小前缀和
        FOR(z,1,c) {
          long long s = sum(x1,x2,y1,y2,1,z);  // 子长方体的前缀和
          ans = max(ans, s - M);  // 最大子段和 = 当前前缀 - 最小前缀
          M = min(M, s);          // 更新最小前缀
        }
      }
    printf("%lld\n", ans);
    if(T) printf("\n");  // 用例间空行
  }
  return 0;
}
// 25875865	10755	Garbage Heap	Accepted	C++	0.210	2020-12-22 14:49:13
```

## 例题18  开放式学分制（Open Credit System, UVa 11078）

### 题目描述

某大学实行开放式学分制，每个学生入学时有一个初始分数。给定 n 个学生按学号顺序的分数 A[0..n-1]（n ≤ 10⁵），学号越小的学生入学越早。定义：高年级学生（i < j）的 A[i] - A[j] 表示这名高年级学生的优势。求所有高年级学生中最大的优势值。

**输入格式**：第一行 T，测试用例数。每组第一行 n，接下来 n 行每行一个整数 A[i]（|A[i]| ≤ 150000）。

**输出格式**：每组输出一行，一个整数表示最大优势值。

### 解题思路

**1. 问题本质**

求 `max{A[i] - A[j] | i < j}`，即从左到右扫描，维护 `maxA = max(A[0..i-1])`，对于每个 j，计算 `maxA - A[j]`，取最大值。

**2. 在线处理**

单次扫描 O(n)：
- 初始化 `m = A[0]`（前 i 个元素的最大值）
- 对于每个 i ≥ 1，更新 `ans = max(ans, m - A[i])`，然后 `m = max(m, A[i])`

这本质是"最大前缀差"问题，可以通过维护前缀最大值在线解决。

**3. 为什么不需要排序？**

因为问题是找 i < j 时的 A[i] - A[j] 最大值，且 A[i] 和 A[j] 的相对顺序固定。只需在扫描过程中记录"迄今为止的最大值"，用该最大值减去当前值即可。

### 算法方法

**1. 前缀最大值（在线处理）**
- 单次扫描，维护当前位置之前的最大值
- 每次用最大值减去当前值，更新答案

**2. 动态维护**
- 不需要存储全部数据（当然本题 n 不大，存储也无妨）
- 看到新值时同时完成两件事：更新答案、更新最大值

### 复杂度分析

- **时间复杂度**：O(n)。一次线性扫描。
- **空间复杂度**：O(1)。只需几个变量。

```cpp
// 例题18  开放式学分制（Open Credit System, UVa 11078）
// 陈锋
#include <cassert>
#include <cstdio>
#include <algorithm>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
const int MAXN = 1e5 + 4;
int A[MAXN];

int main() {
  int n, T;
  scanf("%d", &T);
  while (T--) {
    scanf("%d", &n);
    _for(i, 0, n) scanf("%d", &(A[i]));

    // ---- 在线处理：维护前缀最大值，计算最大差值 ----
    // m: 当前位置之前的最大值 (max{A[0]..A[i-1]})
    // ans: 当前找到的最大差值 (max{A[i]-A[j] | i<j})
    int m = A[0], ans = A[0] - A[1];  // 初始化：第一个元素为前缀最大值
    _for(i, 1, n) {  // 从第二个元素开始扫描
      // 用前缀最大值减去当前值 = 此前最高分的高年级 - 当前低年级
      ans = max(m - A[i], ans);  // 更新最大优势
      m = max(A[i], m);          // 更新前缀最大值
      // 关键：先更新答案再更新m，因为A[i]不能和自己相减（需满足i<j）
    }
    printf("%d\n", ans);
  }
  return 0;
}
// 18756057	11078	Open Credit System	Accepted	C++11	0.060	2017-02-10 14:12:42
```

## 例题17  年龄排序（Age Sort, UVa 11462）

### 题目描述

给定 n 个年龄（1 ≤ n ≤ 2×10⁶），每个年龄是 1 到 100 之间的整数。要求将这些年龄按升序排列后输出（空格分隔）。

**输入格式**：多组数据。每组第一行为 n，n=0 结束。接下来一行（或多行）包含 n 个整数。

**输出格式**：每组输出一行，排序后的年龄，空格分隔。

### 解题思路

**1. 数据特点**

年龄的范围非常小（1-100），而 n 可能非常大（2×10⁶）。这种场景下，使用 O(n log n) 的比较排序显然不够高效。应使用**计数排序（Counting Sort）**。

**2. 计数排序**

- 统计每个年龄出现了多少次（cnt[age]++）
- 按年龄从小到大输出，每个年龄输出 cnt[age] 次
- 时间复杂度 O(n)，空间复杂度 O(MAX_AGE) = O(1)

**3. 为什么不用 std::sort？**

std::sort 的时间复杂度是 O(n log n)，当 n=2×10⁶ 时约 4×10⁷ 次比较，虽然能过但计数排序 O(n + 100) 更优。本题的年龄范围固定且很小，计数排序是最佳选择。

### 算法方法

**1. 计数排序（Counting Sort）**
- 适用于数据范围远小于数据量的场景
- 统计 → 输出，不涉及比较和交换

### 复杂度分析

- **时间复杂度**：O(n)。输入 O(n)，统计 O(n)，输出 O(n)。
- **空间复杂度**：O(MAX_AGE) = O(1)。计数数组大小固定为 101。

```cpp
// 例题17  年龄排序（Age Sort, UVa 11462）
// 陈锋
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
const int MAXN = 100;  // 年龄范围1-100

int main() {
  int n, a, cnt[MAXN + 4];  // cnt[age]: 年龄age的出现次数
  while (scanf("%d", &n) == 1 && n) {
    fill_n(cnt, MAXN + 4, 0);  // 初始化计数数组

    // ---- 统计阶段：记录每个年龄的人数 ----
    _for(i, 0, n) scanf("%d", &a), ++cnt[a];  // 计数

    // ---- 输出阶段：按年龄升序输出 ----
    _for(i, 0, MAXN)  // 遍历年龄1-100
      _for(j, 0, cnt[i])  // 每个年龄输出cnt[i]次
        // 注意输出格式：最后一个数后面不加空格
        printf("%d%s", i, (i == MAXN - 1 && j == cnt[i] - 1) ? "" : " ");
    puts("");  // 换行
  }
}
// 25875806	11462	Age Sort	Accepted	C++	0.250	2020-12-22 14:38:05
```

## 例题19  计算器谜题（Calculator Conundrum, UVa 11549）

### 题目描述

一个老旧的计算器只能显示 n 位数字（n ≤ 9）。输入一个初始数 K（n 位数以内）。每次操作：将当前显示的数的平方求出来，如果结果超过 n 位，则只显示高 n 位（即不断除以 10 直到不超过 n 位）。这个过程会形成一个循环。求在这个过程中出现过的**最大数**。

**输入格式**：第一行 T，测试用例数。每组一行两个数 n 和 K。

**输出格式**：每组输出一行，一个整数表示过程中出现的最大值。

### 解题思路

**1. 问题本质**

这是一个有限状态机上的遍历问题。由于只有最多 10^n 种状态，过程最终一定会进入循环。问题要求在进入循环后停止，并输出遇到的最大值。

**2. Floyd 判圈算法（快慢指针）**

不需要存储所有访问过的状态来判断循环，使用 Floyd 判圈法：
- 慢指针 k1 每次走一步（调用一次 next）
- 快指针 k2 每次走两步（调用两次 next）
- 当 k1 == k2 时，说明已经进入循环
- 在行走过程中记录遇到的最大值

**3. next 函数的实现**

`next(x) = x*x`，然后不断 `/= 10` 直到 < M（M = 10^n）

### 算法方法

**1. Floyd 判圈算法（Tortoise and Hare）**
- 空间 O(1) 的循环检测方法
- 不需要记录 visited 集合

**2. 模拟**
- 直接模拟计算器的运算过程
- 使用 long long 避免溢出

### 复杂度分析

- **时间复杂度**：O(λ + μ)，其中 λ 为进入循环前的步数，μ 为循环长度。最坏情况下约 10^n，但实际远小于此。
- **空间复杂度**：O(1)。只使用快慢指针等常数变量。

```cpp
// 例题19  计算器谜题（Calculator Conundrum, UVa 11549）
// 陈锋
#include <iostream>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
LL K, M;  // K: 初始值; M: 10^n（n位数的上限）

// 计算下一步的值：x → 只保留 x^2 的高n位
LL next(LL x) {
  LL ans = x * x;  // 平方（可能溢出long long？注意范围，n≤9，x<10^9，x^2<10^18在LL范围内）
  while (ans >= M) ans /= 10;  // 不断去掉低位直到剩下n位
  return ans;
}

int main() {
  int T, n;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%lld", &n, &K);
    M = 1;
    _for(i, 0, n) M *= 10;  // M = 10^n

    // ---- Floyd判圈法（快慢指针） ----
    LL ans = K;               // 记录遇到的最大值
    LL k1 = K, k2 = K;        // k1: 慢指针(每次一步), k2: 快指针(每次两步)
    do {
      k1 = next(k1);          // 慢指针走一步
      ans = max(ans, k1);     // 更新最大值
      k2 = next(k2);          // 快指针走第一步
      ans = max(ans, k2);
      k2 = next(k2);          // 快指针走第二步
      ans = max(ans, k2);
    } while (k1 != k2);       // 当快慢指针相遇时，说明进入循环

    printf("%lld\n", ans);
  }
}
// 21699036 11549 Calculator Conundrum Accepted C++11 0.050 2018-07-28 07:37:08
```

## UVa1398 Meteor (整数版本, 更快)

### 题目描述

有一个宽 w、高 h（w,h ≤ 10⁹）的矩形相机视野。有 n 个流星（n ≤ 10⁵），每个流星在 t=0 时位于 (x, y)，以速度 (a, b) 做匀速直线运动（|a|,|b| ≤ 10⁹）。求在 t ≥ 0 的某个时刻，相机视野内最多同时能看到多少个流星。

**输入格式**：第一行 T，测试用例数。每组第一行三个整数 w, h, n。接下来 n 行每行四个整数 x, y, a, b。

**输出格式**：每组输出一行，一个整数表示最大同时可见流星数。

### 解题思路

**1. 每个流星的可见时间段**

对于单个流星，其 x 坐标随时间变化为 x + a·t。要满足 0 < x+a·t < w。解不等式得到 t 的范围 [Lx, Rx]。同理解 y 方向的范围 [Ly, Ry]。取交集得到该流星在视野内的总时间区间 [L, R] = [max(Lx,Ly), min(Rx,Ry)]。

如果 L ≥ R（或区间为空），该流星永远不可见，忽略。

**2. 扫描线求最大重叠数**

将所有流星的 [L, R] 区间转化为事件：
- 在 L 时刻：流星进入视野（cnt++）
- 在 R 时刻：流星离开视野（cnt--）

将所有事件按时间排序，扫描过程中维护当前计数 cnt，更新最大值 ans。

关键：事件的时间可能非常大（10⁹量级），需要用整数处理。这里使用分数形式避免浮点误差（乘以公分母 2520）。

**3. 整数化处理**

使用 `update` 函数计算每个方向的时间区间。将时间放大 2520 倍（h和w的倍数），使用整数运算：
- 当速度 a > 0 时：进入时间 = -x/a，离开时间 = (w-x)/a
- 当速度 a < 0 时：进入时间 = (w-x)/|a|，离开时间 = -x/|a|
- 当速度 a = 0 时：如果 x 不在 (0,w) 内则永不可见

所有结果乘以 2520 用整数表示（最小公倍数技巧避免除法截断误差）。

### 算法方法

**1. 扫描线算法**
- 将区间问题转化为事件排序 + 扫描
- 在扫描过程中维护重叠计数的最大值

**2. 有理数/整数化处理**
- 使用 2520 作为放大系数，将浮点边界转为整数事件
- 避免浮点精度问题

**3. 事件排序**
- 按时间排序，同时时间点优先处理右端点（离开事件），避免端点处计数错误

### 复杂度分析

- **时间复杂度**：O(n log n)。每个流星产生 2 个事件，排序 2n 个事件 O(n log n)，扫描 O(n)。
- **空间复杂度**：O(n)。存储事件数组。

```cpp
// UVa1398 Meteor (整数版本, 更快)
// 刘汝佳
#include <algorithm>
#include <cstdio>
using namespace std;

// 更新流星在某个维度上的可见时间区间
// 约束条件：0 < x + a*t < w
// 将时间乘以2520（w和h的最小公倍数），使用整数避免浮点误差
// 参数：x=初始坐标, a=速度, w=边界长度
// 结果更新到L(可见开始), R(可见结束)
// 0<x+at<w
void update(int x, int a, int w, int& L, int& R) {
  if (a == 0) {
    // 速度为0：如果初始就在边界外，则永远不可见
    if (x <= 0 || x >= w) R = L - 1;  // 使区间无效（R < L）
  } else if (a > 0) {
    // 正速度：进入时间 = -x/a（需t≥0），离开时间 = (w-x)/a
    L = max(L, -x * 2520 / a);      // 下界：max(当前L, 进入时间×2520)
    R = min(R, (w - x) * 2520 / a);  // 上界：min(当前R, 离开时间×2520)
  } else {
    // 负速度（a < 0）：求解 0 < x+a*t < w（除以负数不等式方向翻转）
    // 进入条件 t > (w-x)/a → L = max(L, (w-x)*2520/a)（a<0, 整数值为负时取max得非负下界）
    L = max(L, (w - x) * 2520 / a);
    // 离开条件 t < -x/a → R = min(R, -x*2520/a)
    R = min(R, -x * 2520 / a);
  }
}

const int maxn = 1e5 + 8;

// 事件结构体
struct Event {
  int x;     // 时间（×2520后的整数时间）
  int type;  // 0=进入, 1=离开
  bool operator<(const Event& a) const {
    // 先按时间排序，同时刻先处理右端点（离开事件）
    // 确保"离开"在"进入"之前处理，避免端点处重叠计数错误
    return x < a.x || (x == a.x && type > a.type);
  }
} events[maxn * 2];

int main() {
  int T;
  scanf("%d", &T);
  while (T--) {
    int w, h, n, e = 0;  // e: 事件计数器
    scanf("%d%d%d", &w, &h, &n);
    for (int i = 0; i < n; i++) {
      int x, y, a, b;
      scanf("%d%d%d%d", &x, &y, &a, &b);

      // ---- 计算该流星在视野内的时间区间 ----
      // 约束: 0 < x+a*t < w, 0 < y+b*t < h, t >= 0
      int L = 0, R = 1e9;  // 初始区间 [0, ∞)（乘以2520范围）
      update(x, a, w, L, R);  // x方向的约束
      update(y, b, h, L, R);  // y方向的约束

      if (R > L) {  // 有效区间（可见时间段）
        events[e++] = (Event){L, 0};  // 进入事件
        events[e++] = (Event){R, 1};  // 离开事件
      }
    }

    // ---- 扫描线阶段 ----
    sort(events, events + e);  // 按时间排序
    int cnt = 0, ans = 0;     // cnt: 当前可见流星数; ans: 历史最大
    for (int i = 0; i < e; i++) {
      if (events[i].type == 0)  // 进入事件
        ans = max(ans, ++cnt);  // 计数+1, 更新最大值
      else                      // 离开事件
        cnt--;                  // 计数-1
    }
    printf("%d\n", ans);
  }
  return 0;
}
// 28685849 UVa1398 Accepted 50ms 1246	C++
```
