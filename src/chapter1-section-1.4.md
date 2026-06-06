# 1.4 动态规划专题

## 例题26  约瑟夫问题的变形（And Then There Was One, Japan 2007, Codeforces Gym101415A

### 题目描述

经典的约瑟夫问题变种：n 个人（编号 1..n）围成一圈从 1 到 k 报数，每次数到 k 的人出局。但初始时第一个人**已经死了**（即从第 m 个人开始报数）。求最后剩下的人的编号。n, k, m ≤ 10000。

**输入格式**：多组数据（文件 A.in）。每组一行三个整数 n, k, m，以 n=k=m=0 结束。

**输出格式**：每组输出一行，最后存活者的编号。

### 解题思路

**1. 经典约瑟夫问题的递推**

对于标准约瑟夫问题（从第一个人开始报数，每次报 k），设 f[i] 为 i 个人时最后存活者的编号（0-indexed），递推公式：
`f[1] = 0`，`f[i] = (f[i-1] + k) % i`

**2. 变形到从第 m 个开始**

由于第一个人（编号 m）在开始时已被"移除"，问题转化为：
- 从编号 m 的下一个人开始，对剩余 n-1 个人进行标准约瑟夫问题
- 最终存活者编号（1-indexed）需要做坐标偏移

**3. 坐标映射**

标准约瑟夫问题的 f[n] 是相对于"第一个报数的人"的偏移（0-indexed）。本题实际第一个报数的人是 m+1（如果 m 被移除）。所以：
- 最终答案 = (m - k + 1 + f[n]) mod n
- 由于模运算可能产生 0 或负数，需要调整到 [1, n]

### 算法方法

**1. 递推 / 动态规划**
- 利用经典约瑟夫问题的递推公式
- 自底向上计算 f[1] → f[2] → ... → f[n]

**2. 坐标变换**
- 将变形问题映射回标准约瑟夫问题
- 最后通过坐标偏移恢复答案

### 复杂度分析

- **时间复杂度**：O(n)。递推从 i=2 到 n，每次 O(1)。
- **空间复杂度**：O(n)。需要 f 数组存储递推结果。

```cpp
// 例题26  约瑟夫问题的变形（And Then There Was One, Japan 2007, Codeforces Gym101415A
// Rujia Liu
#include<cstdio>
const int maxn = 10000 + 2;
int f[maxn];  // f[i]: i个人时的约瑟夫问题答案（0-indexed, 相对于"第一个报数人"的偏移）

int main() {
  freopen("A.in", "r", stdin);
  for( int n, k, m; scanf("%d%d%d", &n, &k, &m) == 3 && n;) {

    // ---- 经典约瑟夫递推 ----
    f[1] = 0;  // 1个人时，存活者的偏移为0
    for(int i = 2; i <= n; i++)
      f[i] = (f[i-1] + k) % i;  // 递推：每多一个人，偏移向后移动k位
    // f[n] 表示：从"第一个报数的人"算起，最后存活者的偏移（0-indexed）

    // ---- 坐标变换：从变形回到标准 ----
    // 本题中第一个人（最初是m）已死，首个报数的人是m+1
    // 答案 = (m - k + 1 + f[n]) mod n
    int ans = (m - k + 1 + f[n]) % n;
    if (ans <= 0) ans += n;  // 模运算调整为[1, n]的1-indexed编号
    printf("%d\n", ans);
  }
  return 0;
}
// 102052339 Dec/22/2020 23:00UTC+8 chenwz A - And Then There Was One GNU C++11 Accepted 15 ms 0 KB
```

## 例题27  王子和公主（Prince and Princess, UVa 10635）

### 题目描述

王子和公主分别有一个长度为 p+1 和 q+1 的整数序列（p,q ≤ 62500），两个序列中的数字都是 1..n² 中的某个值（n ≤ 250）。求两个序列的**最长公共子序列（LCS）**的长度。

**输入格式**：第一行 T，测试用例数。每组第一行三个整数 n, p, q。接下来两行分别包含 p+1 个和 q+1 个整数。

**输出格式**：每组输出 `Case X: Y`，X 编号，Y 为 LCS 长度。

### 解题思路

**1. LCS 转化为 LIS**

当其中一个序列的元素**互不相同**时，LCS 可以转化为 LIS。因为题目保证了王子序列的元素互不相同（1..n² 每个至多出现一次），我们可以：
- 将王子序列中的每个数映射为其位置编号：`IDX[num] = position`
- 遍历公主序列，对于每个数，如果在王子序列中出现过，记录其位置编号
- 在得到的位置序列上求 LIS

**2. 为什么可以转化？**

LCS 要求挑选一个公共子序列，且子序列在两个序列中的相对顺序一致。将王子序列的元素映射为递增的编号后，LCS 等价于公主序列中那些编号构成的递增子序列（LIS）。

**3. LIS 的 O(n²) 实现**

由于本题 n 较小，直接用 O(n²) 的 DP 求 LIS：
`D[j] = max(D[j], D[i] + 1)` 当 B[j] > B[i] 时。

更高效的实现是 O(n log n) 的二分优化版，但本题 O(n²) 已足够。

### 算法方法

**1. 序列变换 + LIS**
- LCS → LIS 的经典转化技巧
- 前提条件：一个序列元素互不相同

**2. 动态规划（求 LIS）**
- D[i] = 以第 i 个元素结尾的最长上升子序列长度
- 递推：D[i] = max(D[j] + 1) for all j < i and B[j] < B[i]

### 复杂度分析

- **时间复杂度**：O(q²)。q ≤ 62501，O(q²) 约 3.9×10⁹，实际上优化后可通过（因为转换后序列长度远小于 q）。
- **空间复杂度**：O(n² + q)。需要 IDX 数组（大小 n²）和 B、D 数组。

```cpp
// 例题27  王子和公主（Prince and Princess, UVa 10635）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 256, MAXP = MAXN * MAXN;
using namespace std;
typedef long long LL;
int B[MAXP], IDX[MAXP], D[MAXP];  // B: 转换后的序列; IDX: 数值→位置映射; D: LIS的DP数组

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T, n, a, p, q;
  cin >> T;
  for (int t = 1; cin >> n >> p >> q && n; t++) {
    ++p, ++q;  // 序列长度 = p+1, q+1

    // ---- 第一阶段：LCS→LIS转化 ----
    fill_n(IDX, n * n + 2, 0);  // 初始化映射表
    // 将王子序列中的每个数映射为其位置（1-indexed）
    for (int i = 1; i <= p; i++) { cin >> a; IDX[a] = i; }

    // 遍历公主序列，提取在王子序列中出现过的数的位置
    int bi = 0, b;
    for (int i = 0; i < q; i++) {
      cin >> b;
      b = IDX[b];  // 查找该数在王子序列中的位置
      if (b) B[bi++] = b;  // 如果存在于王子序列中，加入B数组
    }
    // 现在B数组中的LIS长度 = 原两个序列的LCS长度

    // ---- 第二阶段：O(n²)求LIS ----
    fill_n(D, bi + 1, 1);  // D[i]初始为1（至少自身是长度为1的LIS）
    int ans = -1;
    for (int i = 0; i < bi; i++) {
      for (int j = i + 1; j < bi; j++)
        if (B[j] > B[i])  // 严格递增条件
          D[j] = max(D[j], 1 + D[i]);  // 状态转移
      ans = max(ans, D[i]);  // 更新答案
    }
    printf("Case %d: %d\n", t, ans);
  }
  return 0;
}
// Accepted 2250ms 826 C++5.3.0 2020-12-08 20:27:25 25825777
```

## 例题30  放置街灯（Placing Lampposts, UVa 10859）

### 题目描述

给定一个 N 个节点 M 条边的无向图（森林），N ≤ 1000，M < N。需要在一些节点上放置街灯，使得每条边至少有一个端点有街灯（即边被照亮）。在此前提下：
1. 最小化街灯总数
2. 在街灯总数最小的前提下，最大化被两盏灯同时照亮的边数（即两端都有灯的边）

**输入格式**：第一行 T，测试用例数。每组第一行 N, M，接下来 M 行每行两个整数 u, v。

**输出格式**：每组输出三个整数：最少灯数 A，最多同时被两盏灯照亮的边数 B，只被一盏灯照亮的边数 C。

### 解题思路

**1. 树形 DP（最小顶点覆盖）**

每条边至少有一个端点放灯 → 这是一个经典的"最小顶点覆盖"问题。对于树（或森林），可以用树形 DP 求解：
- `dp[u][0]`：节点 u 不放灯时，以 u 为根的子树的最优值
- `dp[u][1]`：节点 u 放灯时，以 u 为根的子树的最优值

**2. 两阶段优化：编码技巧**

由于有两个优化目标（灯数和双灯边数），可以将它们编码在一个整数中：
- 使用 BASE = 2000（大于最大边数 M）作为权重
- `ans = 灯数 × BASE + 单灯边数`
- 最小化灯数（主目标），最大化双灯边数 = 最小化单灯边数（次目标）

解码：灯数 = ans / BASE，单灯边数 = ans % BASE，双灯边数 = M - 单灯边数

### 算法方法

**1. 树形 DP（DFS + 记忆化）**
- 自底向上递推
- 每个节点有两个状态：放灯 / 不放灯

**2. 多目标优化编码**
- 将两个优化目标编码为一个整数，利用权重分离主次目标
- 常见技巧：`value = primary × BASE + secondary`

### 复杂度分析

- **时间复杂度**：O(N)。每个节点访问一次，每条边处理一次。
- **空间复杂度**：O(N)。存储邻接表和 DP 状态。

```cpp
// 例题30  放置街灯（Placing Lampposts, UVa 10859）
// 陈锋
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;
const int NN = 1000 + 8, BASE = 2000;  // BASE > 最大边数，用于编码多目标
vector<int> G[NN];  // 邻接表：森林是稀疏的，这样保存省空间，枚举相邻结点也更快
int Vis[NN][2], D[NN][2], N, M;  // Vis: 记忆化标记; D: DP值

// 树形DP：节点i，状态j(0=不放灯,1=放灯)，父节点f
// 返回值编码：灯数*BASE + 单灯照亮边数
int dp(int i, int j, int f) {
  if (Vis[i][j]) return D[i][j];  // 记忆化
  Vis[i][j] = 1;
  int& ans = D[i][j];

  // ---- 情况1：节点i放灯 ----
  ans = BASE;  // 灯数+1 (贡献BASE)
  for (int k = 0; k < G[i].size(); k++)
    if (G[i][k] != f)  // 关键判断：避免走回父节点
      ans += dp(G[i][k], 1, i);  // 子节点：父节点i已放灯
  // 如果i不放灯且i不是根(f>=0)，则边(i,f)是单灯边（f有灯但i没灯）
  if (!j && f >= 0) ans++;  // 单灯边+1

  // ---- 情况2：节点i不放灯（仅当父节点已放灯或i是根） ----
  if (j || f < 0) {  // i的父节点已放灯，或i是根节点（没有父节点）
    int sum = 0;
    for (int k = 0; k < G[i].size(); k++)
      if (G[i][k] != f)
        sum += dp(G[i][k], 0, i);  // 子节点：父节点i没放灯（状态j=0）
    if (f >= 0) sum++;  // 边(i,f)是单灯边（f有灯）
    ans = min(ans, sum);  // 取更优值
  }
  return ans;
}

int main() {
  int T, a, b;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%d", &N, &M);
    // ---- 初始化 ----
    for (int i = 0; i < N; i++) G[i].clear();
    for (int i = 0, a, b; i < M; i++)
      scanf("%d%d", &a, &b), G[a].push_back(b), G[b].push_back(a);

    // ---- 森林的树形DP：对每棵树分别计算 ----
    memset(Vis, 0, sizeof(Vis));
    int ans = 0;
    for (int i = 0; i < N; i++)
      if (!Vis[i][0])  // 未访问过的节点，作为新树的根
        ans += dp(i, 0, -1);  // 根节点，父节点为-1

    // ---- 解码：从编码值中分离三个目标 ----
    printf("%d %d %d\n",
      ans/BASE,          // 最少灯数 = ans / BASE
      M - ans % BASE,    // 双灯照亮边数 = 总边数 - 单灯边数
      ans % BASE);       // 单灯照亮边数 = ans % BASE
  }
  return 0;
}
// Accepted 1365 C++5.3.0 2020-12-08 21:06:32 25825938
```

## 例题28  Sum游戏（Game of Sum, UVa 10891）

### 题目描述

有一个长度为 n 的整数序列 A[1..n]（n ≤ 100，|A[i]| ≤ 1000）。两个玩家轮流取数，每次可以从序列的左端或右端取走任意数量的连续数（至少 1 个，至多全部）。两个玩家都采取最优策略，最大化自己的总分（取走数的和）减去对方总分的差值。求先手玩家的"自己的分 - 对手的分"的最大值。

**输入格式**：多组数据。每组第一行为 n，n=0 结束。接下来一行 n 个整数。

**输出格式**：每组输出一行，一个整数表示最优差值。

### 解题思路

**1. 博弈 DP 模型**

设 d[i][j] 为区间 [i, j] 上先手玩家能获得的最优差值（自己得分 - 对方得分）。

对于区间 [i, j]，先手可以选择从左边取 k 个（S[i..i+k-1]）或从右边取 k 个（S[j-k+1..j]）：
- 取走部分后，剩余区间变为对手的先手
- `d[i][j] = sum[i..j] - min{d[i+1][j], d[i+2][j], ..., d[j][j], d[i][i], ..., d[i][j-1], 0}`
- 其中 0 表示一次取光所有数（此时对手得 0 分）

**2. 优化：用 f 和 g 数组避免 O(n³)**

定义辅助数组：
- `f[i][j] = min{d[i][j], d[i+1][j], ..., d[j][j]}`
- `g[i][j] = min{d[i][j], d[i][j-1], ..., d[i][i]}`

递推公式：
- `d[i][j] = sum[j] - sum[i-1] - min(f[i+1][j], g[i][j-1], 0)`
- `f[i][j] = min(d[i][j], f[i+1][j])`
- `g[i][j] = min(d[i][j], g[i][j-1])`

**3. 最终答案**

先手的"自己 - 对手" = d[1][n]。实际上输出是 `2*d[1][n] - S[n]`，即（自己得分 - 对手得分）。

### 算法方法

**1. 区间 DP + 博弈论**
- Min-Max 博弈树搜索
- 利用"自己得分 - 对手得分 = sum - 2×对手得分"的等价变换

**2. 辅助数组优化**
- f 和 g 数组将最内层 min 操作从 O(n) 降为 O(1)

### 复杂度分析

- **时间复杂度**：O(n²)。两重循环枚举区间，每次 O(1) 递推。
- **空间复杂度**：O(n²)。需要 d、f、g 三个二维数组。

```cpp
// 例题28  Sum游戏（Game of Sum, UVa 10891）
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<algorithm>
using namespace std;

int S[110], A[110];  // S: 前缀和; A: 原数组
// d[i][j]: 区间[i,j]上先手能获得的最优差值(自己得分-对手得分)
// f[i][j]: min{d[i][j], d[i+1][j], ..., d[j][j]}
// g[i][j]: min{d[i][j], d[i][j-1], ..., d[i][i]}
int d[110][110], f[110][110], g[110][110], n;

// f[i+1][j] = min{d(i+1,j),d(i+2,j)...,d(j,j)}
// g[i][j-1] = min{d(i,j-1),d(i,j-2)...,d(i,i)}

int main() {
  while(scanf("%d", &n) && n) {
    // ---- 输入并计算前缀和 ----
    S[0] = 0;
    for(int i = 1; i <= n; i++) {
      scanf("%d", &A[i]);
      S[i] = S[i-1] + A[i];  // 前缀和：快速求区间和
    }

    // ---- 初始化：单个元素的区间 ----
    for(int i = 1; i <= n; i++)
      f[i][i] = g[i][i] = d[i][i] = A[i];  // 边界：只有一个数时直接取

    // ---- 区间DP：按区间长度递增递推 ----
    for(int L = 1; L < n; L++)       // L = j-i (区间长度)
      for(int i = 1; i+L <= n; i++) {
        int j = i+L;                 // 当前区间[i,j]
        int m = 0;                   // m = min{f(i+1,j), g(i,j-1), 0}
        m = min(m, f[i+1][j]);       // 从左边取若干数后，对手的最优值
        m = min(m, g[i][j-1]);       // 从右边取若干数后，对手的最优值
        // 对手最优值 = m，先手得分 = 总和 - 对手得分
        // 先手优势 = 先手得分 - 对手得分 = 总和 - 2*对手得分
        d[i][j] = S[j] - S[i-1] - m;  // 区间和 - 对手最优
        f[i][j] = min(d[i][j], f[i+1][j]);  // 更新f：包含当前区间
        g[i][j] = min(d[i][j], g[i][j-1]);  // 更新g：包含当前区间
      }
    // 先手得分 - 后手得分 = 2*d[1][n] - S[n]
    printf("%d\n", 2*d[1][n] - S[n]);
  }
  return 0;
}
// 25875896	10891	Game of Sum	Accepted	C++	0.000	2020-12-22 15:00:28
```

## 例题32  分享巧克力（Sharing Chocolate, World Finals 2010, UVa1099）

### 题目描述

有一块 x×y 的巧克力，需要分给 n 个人（n ≤ 15），第 i 个人分到的面积应为 A[i]。每次切割必须沿网格线，且只能将一块巧克力切成两块（水平或垂直切割）。问是否存在一种切割方案，使得每个人得到的巧克力恰好是所需面积。

**输入格式**：多组数据。每组第一行为 n，n=0 结束。第二行两个整数 x, y（x,y ≤ 100）。第三行 n 个整数 A[i]。

**输出格式**：每组输出 `Case X: Yes/No`。

### 解题思路

**1. 状态压缩 DP**

由于 n ≤ 15，可以使用状态压缩。`dp[S][x]` 表示能否用面积和为 sum[S] 的子集 S 拼成一个 x × (sum[S]/x) 的矩形。

**2. 子集枚举**

对于当前集合 S 和目标宽度 x：
- 如果集合只有一个元素（|=1），则面积为 sum[S]，总能拼成（只要 sum[S]/x 是整数）
- 否则，枚举 S 的真子集 S0，看能否将矩形水平或垂直分割成两部分

**3. 两种切割方向**

- **水平切割**（保留宽度 x）：检查 S0 和 S\S0 在相同宽度 x 下是否可行
- **垂直切割**（保留高度 y = sum[S]/x）：宽度变为 y，检查 S0 和 S\S0 在相同高度下是否可行

**4. 子集枚举技巧**

`for(int S0 = (S-1)&S; S0; S0 = (S0-1)&S)` 枚举 S 的所有真子集，比 `for 0..2^n` 效率更高。

### 算法方法

**1. 状态压缩 DP**
- S 用二进制表示参与的子集
- 每个状态表示"能否用这些元素拼成给定尺寸的矩形"

**2. 子集枚举 / 记忆化搜索**
- DFS + 记忆化，避免重复计算
- 利用 sum[S] 快速计算剩余面积

### 复杂度分析

- **时间复杂度**：O(3^n)。每个子集枚举其所有子集，总和 = 3^n。n ≤ 15，约 1.4×10⁷。
- **空间复杂度**：O(2^n × maxw)。状态空间约 32768 × 100。

```cpp
// 例题32  分享巧克力（Sharing Chocolate, World Finals 2010, UVa1099）
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<algorithm>
using namespace std;

const int maxn = 16;       // n ≤ 15
const int maxw = 100 + 10; // 宽度上限
int n, A[maxn];
int sum[1<<maxn];           // sum[S]: 子集S的总面积
int f[1<<maxn][maxw];       // f[S][x]: 子集S能否拼成宽x的矩形(-1未计算,0不可,1可)
int vis[1<<maxn][maxw];     // 记忆化标记

// 统计二进制中1的个数
int bitcount(int x) { return x == 0 ? 0 : bitcount(x/2) + (x&1); }

// DP：状态S能否拼成宽x的矩形（高=sum[S]/x）
int dp(int S, int x) {
  if(vis[S][x]) return f[S][x];  // 记忆化
  vis[S][x] = 1;
  int& ans = f[S][x];
  // 单个元素：只要面积能凑成矩形即可（高=面积/x必须是整数）
  if(bitcount(S) == 1) return ans = 1;

  int y = sum[S] / x;  // 对应的高度

  // ---- 枚举真子集，尝试水平或垂直切割 ----
  for(int S0 = (S-1)&S; S0; S0 = (S0-1)&S) {  // 枚举S的所有真子集
    int S1 = S - S0;  // 补子集

    // 水平切割：宽度保持x，高度分割
    // sum[S0]%x == 0 保证子集S0能形成宽x高为sum[S0]/x的矩形
    if(sum[S0] % x == 0 && dp(S0, min(x, sum[S0]/x)) && dp(S1, min(x, sum[S1]/x)))
      return ans = 1;

    // 垂直切割：高度保持y，宽度分割（即新宽度=y）
    if(sum[S0] % y == 0 && dp(S0, min(y, sum[S0]/y)) && dp(S1, min(y, sum[S1]/y)))
      return ans = 1;
  }
  return ans = 0;
}

int main() {
  int kase = 0, n, x, y;
  while(scanf("%d", &n) == 1 && n) {
    scanf("%d%d", &x, &y);
    for(int i = 0; i < n; i++) scanf("%d", &A[i]);

    // ---- 预处理：计算每个子集的面积和 ----
    memset(sum, 0, sizeof(sum));
    for(int S = 0; S < (1<<n); S++)
      for(int i = 0; i < n; i++)
        if(S & (1<<i)) sum[S] += A[i];  // 累加子集中所有元素的面积

    // ---- DP求解 ----
    memset(vis, 0, sizeof(vis));
    int ALL = (1<<n) - 1;
    int ans;
    // 剪枝：总面积不等于x*y 或 总面积无法被x整除 → 直接判定不可能
    if(sum[ALL] != x*y || sum[ALL] % x != 0) ans = 0;
    else ans = dp(ALL, min(x,y));  // 从全集开始，取宽高较小者为x（优化）
    printf("Case %d: %s\n", ++kase, ans ? "Yes" : "No");
  }
  return 0;
}
// 25875902	1099	Sharing Chocolate	Accepted	C++	0.410	2020-12-22 15:02:15
```

## 例题31  捡垃圾的机器人（Robotruck, SWERC 2007, UVa1169）

### 题目描述

一个机器人在二维平面上移动，需要依次捡起 n 个废弃物（n ≤ 100000）。每个废弃物有一个坐标 (x, y) 和重量 w。机器人的最大载重量为 C。机器人从原点 (0,0) 出发，每次可以装载若干连续的废弃物（只要总重量 ≤ C），然后将它们送回原点（垃圾处理站），再出发继续工作。求机器人完成所有任务的最短总路程。

**输入格式**：第一行 T，测试用例数。每组第一行两个整数 C 和 n。接下来 n 行每行三个整数 x, y, w。

**输出格式**：每组输出一行，最小总距离。测试用例间空一行。

### 解题思路

**1. 问题建模**

设 d[i] 为处理完前 i 个废弃物并回到原点的最短距离。转移时，考虑最后一批处理的废弃物为 [j+1, i]：
`d[i] = min_{j} { d[j] + dist_to_pickup[j+1..i] + dist[j+1] + dist[i] }`

其中 `dist_to_pickup[j+1..i]` 是从 j+1 走到 i 的路径长度，`dist[k]` 是原点到第 k 个点的曼哈顿距离。

**2. 简化递推公式**

设：
- `total_dist[i]`：累计路径长度（从原点到 i，按顺序经过各点）
- `dist2origin[i]`：第 i 个点到原点的曼哈顿距离

则最后的拾取路径 = `total_dist[i] - total_dist[j+1]`
转移：`d[i] = min_{j} { d[j] - total_dist[j+1] + dist2origin[j+1] } + total_dist[i] + dist2origin[i]`

其中 j 需要满足 `total_weight[i] - total_weight[j] ≤ C`

**3. 单调队列优化**

定义 `func(i) = d[i] - total_dist[i+1] + dist2origin[i+1]`

则 `d[i] = min{ func(j) } + total_dist[i] + dist2origin[i]`，其中 j 满足重量约束。

由于重量约束是滑动窗口性质（j 的取值范围是连续的），可以使用**单调队列**维护 func(j) 的最小值，O(n) 时间内解决。

### 算法方法

**1. 动态规划 + 单调队列优化**
- 线性 DP 的经典优化技巧
- 当转移中需要区间最值且区间单调移动时使用

**2. 前缀和**
- total_dist 和 total_weight 用于 O(1) 计算区间信息

### 复杂度分析

- **时间复杂度**：O(n)。单调队列的每个元素入队出队各一次。
- **空间复杂度**：O(n)。需要多个前缀和数组和 DP 数组。

```cpp
// 例题31  捡垃圾的机器人（Robotruck, SWERC 2007, UVa1169）
// Rujia Liu
#include<cstdio>
#include<algorithm>
using namespace std;

const int maxn = 100000 + 10;

int x[maxn], y[maxn];  // 各点的坐标
int total_dist[maxn];   // total_dist[i]: 从原点出发按顺序走到第i个点的累计曼哈顿距离
int total_weight[maxn]; // total_weight[i]: 前i个物品的累计重量
int dist2origin[maxn];  // dist2origin[i]: 第i个点到原点的曼哈顿距离
int q[maxn], d[maxn];   // q: 单调队列; d[i]: 处理完前i个物品的最短距离

// func: DP转移中的关键函数
// func(i) = d[i] - total_dist[i+1] + dist2origin[i+1]
// d[i] = min{func(j)} + total_dist[i] + dist2origin[i]  (重量约束下)
int func(int i) {
  return d[i] - total_dist[i+1] + dist2origin[i+1];
}

main() {
  int T, c, n, w, front, rear;
  scanf("%d", &T);
  while(T--) {
    scanf("%d%d", &c, &n);
    // ---- 初始化 ----
    total_dist[0] = total_weight[0] = x[0] = y[0] = 0;

    // ---- 读入各点并计算前缀和 ----
    for(int i = 1; i <= n; i++) {
      scanf("%d%d%d", &x[i], &y[i], &w);
      dist2origin[i] = abs(x[i]) + abs(y[i]);  // 到原点的曼哈顿距离
      // 累计路径长度：加上从上一个点到当前点的曼哈顿距离
      total_dist[i] = total_dist[i-1] + abs(x[i]-x[i-1]) + abs(y[i]-y[i-1]);
      total_weight[i] = total_weight[i-1] + w;  // 累计重量
    }

    // ---- 单调队列优化DP ----
    front = rear = 1;  // 队列初始化（队首和队尾指针）
    for (int i = 1; i <= n; i++) {
      // 维护重量约束：确保队列中j满足 total_weight[i]-total_weight[j] ≤ c
      while (front <= rear && total_weight[i] - total_weight[q[front]] > c)
        front++;  // 重量超限，弹出队首

      // 计算d[i]：取队首最优j
      d[i] = func(q[front]) + total_dist[i] + dist2origin[i];

      // 维护单调队列（递增）：func值更大的j不是最优，从队尾弹出
      while (front <= rear && func(i) <= func(q[rear]))
        rear--;

      q[++rear] = i;  // 当前j入队
    }

    printf("%d\n", d[n]);  // 处理完所有物品的最短距离
    if(T > 0) printf("\n");
  }
  return 0;
}
// 25875898	1169	Robotruck	Accepted	C++	0.030	2020-12-22 15:01:28
```

## 例题29  黑客的攻击（Hacker's Crackdown, UVa 11825）

### 题目描述

有 n 台计算机（n ≤ 16），每台计算机运行着一些服务（共 n 种服务）。黑客可以攻击某台计算机，使其上运行的所有服务停止。但同时，每台计算机也连接着其他计算机（形成邻接关系），攻击一台计算机会同时影响其邻接的计算机。目标是用最少的攻击次数，使所有 n 种服务都至少被停止一次（每种服务可能在多台计算机上运行，但只要停一次即可）。

**输入格式**：多组数据。每组第一行为 n，n=0 结束。接下来 n 行，第 i 行第一个整数 m 表示计算机 i 相连的计算机数，随后 m 个整数表示相连计算机编号(0..n-1)。

**输出格式**：每组输出 `Case X: Y`，X 编号，Y 为最少攻击次数。

### 解题思路

**1. 状态压缩建模**

n ≤ 16，可以用位掩码表示服务集合。定义：
- `P[i]`：攻击计算机 i 能覆盖的服务集合（计算机 i 及其邻接计算机上运行的所有服务）
- `cover[S]`：攻击集合 S 中所有计算机能覆盖的服务集合的并集

**2. 分组覆盖**

问题转化为：将 n 台计算机分成若干组，每组攻击一次，使得所有服务的并集覆盖全集。求最小组数。

**3. DP 状态转移**

设 `f[S]` 为服务集合 S 最少需要分为几组（即最少攻击次数）：
- 初始：`f[0] = 0`
- 转移：对于每个非空集合 S，枚举其子集 S0，如果 `cover[S0] == ALL`（ALL 为全集），则 `f[S] = max(f[S], f[S\S0] + 1)`
- 本质是求最大能分成多少个"能覆盖全集的子集"

**4. 子集枚举技巧**

同样使用 `for(int S0 = S; S0; S0 = (S0-1)&S)` 枚举子集。

### 算法方法

**1. 状态压缩 DP**
- 位掩码表示计算机集合和服务集合
- 子集枚举实现组合搜索

**2. 预处理优化**
- 预先计算每个计算机的 P[i] 和每个子集的 cover[S]

### 复杂度分析

- **时间复杂度**：O(3^n)。DP 中对每个集合枚举子集，总和 3^n。n ≤ 16，约 4.3×10⁷。
- **空间复杂度**：O(2^n)。cover 和 f 数组大小各 2^n。

```cpp
// 例题29  黑客的攻击（Hacker's Crackdown, UVa 11825）
// 陈锋
#include <algorithm>
#include <cstdio>
using namespace std;

const int NN = 16;
// P[i]: 攻击计算机i能覆盖的服务集合（bitmask）
// cover[S]: 攻击集合S中所有计算机能覆盖的服务集合的并集
// f[S]: 服务集合S最多能被分为几组（每组覆盖全集）
int P[NN], cover[1 << NN], f[1 << NN];

int main() {
  for (int kase = 1, n; scanf("%d", &n) == 1 && n; kase++) {
    // ---- 输入阶段：计算每台计算机的覆盖集合 ----
    for (int i = 0, m, x; i < n; i++) {
      scanf("%d", &m);
      P[i] = 1 << i;  // 计算机i自身运行服务i
      while (m--) {
        scanf("%d", &x);
        P[i] |= (1 << x);  // 邻接计算机的服务也加入
      }
    }

    // ---- 预处理：计算每个子集的覆盖集合 ----
    for (int S = 0; S < (1 << n); S++) {
      cover[S] = 0;
      for (int i = 0; i < n; i++)
        if (S & (1 << i))         // 子集包含计算机i
          cover[S] |= P[i];       // 合并i的覆盖集合
    }

    // ---- 状态压缩DP：子集枚举 ----
    f[0] = 0;  // 空集0组
    int ALL = (1 << n) - 1;  // 全集掩码
    for (int S = 1; S < (1 << n); S++) {
      f[S] = 0;
      // 枚举S的所有子集S0
      for (int S0 = S; S0; S0 = (S0 - 1) & S)
        // 如果子集S0覆盖全集，可以将其分为一组
        if (cover[S0] == ALL)
          f[S] = max(f[S], f[S ^ S0] + 1);  // S0一组 + 剩余的最优分组
    }
    // f[ALL] = 能覆盖全集的最多组数 = 最少攻击次数
    printf("Case %d: %d\n", kase, f[ALL]);
  }
  return 0;
}
// Accepted 720ms 795 C++5.3.02020-12-08 21:14:04 25825962
```
