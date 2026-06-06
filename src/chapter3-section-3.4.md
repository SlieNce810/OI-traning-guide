# 3.4 字符串（2）

> **学习目标**：掌握字符串哈希的概率可靠性基础、滚动哈希的 O(1) 子串计算，以及"二分+哈希"这一判定型问题的高效解题模式。

## 理论基础

### 为什么需要学这个？

你第一次看到"用哈希比较两个子串是否相等"时，心里可能有疑问：哈希值不是可能冲突吗？万一两个不同的字符串算出了相同的哈希值怎么办？这是所有哈希问题的核心顾虑。好消息是：选用合适的基数（如 123、3137）和取模方式（自然溢出或大质数取模），哈希冲突的概率**远低于你的 CPU 算错一次的概率**。这一节我们就从概率分析入手，搞清楚"多安全才够安全"，然后重点掌握字符串哈希的两个看家本领——**滚动哈希**（每次 O(1) 算任意子串的哈希值，不管你用多少次）和**二分+哈希**（把"比较最长公共前缀"这种麻烦事转化成一个可二分的判定问题）。

### 核心概念

#### 1. 哈希冲突的概率：为什么"自然溢出"就够了

**一句话定义**：字符串哈希 `H(s) = Σ s[i] * BASE^(n-1-i) mod MOD`，冲突概率取决于 MOD 的取值和哈希值的空间大小。

**本质理解**：使用 `unsigned long long` 自然溢出相当于模 2^64。由生日悖论，当子串数量达到 √(2^64) ≈ 4×10^9 时才期望出现一个冲突。实际竞赛中 n ≤ 4×10^5，远远够用。如果愿意双哈希（两个不同基数+两个不同模数），冲突概率降到 2^(-128) 量级——比宇宙中原子数量还少。

**与朴素对比**：朴素逐字符比较 O(min(len1, len2))；哈希比较 O(1)。代价是 O(N) 的预处理时间。

#### 2. 滚动哈希：一次预处理，任意子串 O(1) 计算

**一句话定义**：预处理后缀哈希 `H[i] = s[i] + H[i+1] * BASE`，则 `Hash(s[l..r]) = H[l] - H[r+1] * BASE^(r-l+1)`。

**最小示例**：`H[i]` 表示从位置 i 到字符串末尾的哈希值。子串 `"ab"` 在位置 2 的哈希 = `H[2] - H[4] * BASE^2`。

**本质理解**：后缀哈希的设计巧妙的利用了**多项式性质**：如果你把字符串看作一个 BASE 进制的数，`H[l]` 就是这个"大数"的"低位部分"。减去 `H[r+1] * BASE^(r-l+1)` 就能消去尾部，得到纯子串部分。这个公式不需要重新扫描，所以是 O(1)。

#### 3. 二分+哈希：把"最长公共前缀"变成判定

**一句话定义**：二分枚举长度 L，用哈希检查两个子串的前 L 个字符是否相等，从而在 O(log N) 时间内求出最长公共前缀（LCP）。

**本质理解**：哈希让"相等判定"变为 O(1)，而"最大化长度"这种问题天然适合二分——如果长度 L 可行，那所有 ≤L 的长度也必然可行（单调性）。这就是"二分+哈希"套路：**用 O(1) 判定代替 O(N) 计算，用 log N 轮二分缩小搜索范围**。

#### 4. 双模数防冲突：生日悖论的定量分析

**核心原理**：生日悖论告诉我们，在 M 种可能的哈希值中，当元素数量达到约 √M 时，期望出现一对冲突。对于单模数 2^64（自然溢出），√(2^64) = 2^32 ≈ 4×10^9。竞赛中子串数量通常 ≤ 4×10^5（远小于 4×10^9），所以自然溢出在实践中很安全。但攻击者可以通过构造"反哈希测试数据"（如针对 BASE=131 的 CF 卡哈希测试）来人为制造冲突。

**双模数的威力**：使用两个不同的大质数模数 MOD₁ 和 MOD₂（如 10^9+7 和 10^9+9），哈希值空间变为 MOD₁ × MOD₂ ≈ 10^18。此时 √(M) ≈ 10^9——冲突概率降到完全可以忽略的水平。更精确地，两对不同的子串 (s₁, t₁) 和 (s₂, t₂) 同时碰撞的概率约为 (1/MOD₁) × (1/MOD₂)，对于 10^9 级别的模数，这是 10^(-18) 量级。**实用建议**：日常训练自然溢出够用；正式比赛中若有卡哈希风险，双模数或双基数（不同的 BASE 值）可提供几乎绝对的保障。

#### 5. 二维哈希：矩阵子矩阵的 O(1) 匹配

**公式定义**：对于字符矩阵 A，定义二维哈希 `H[i][j]` = 从 (i,j) 到右下角的子矩阵的哈希值。递推公式：`H[i][j] = A[i][j] + H[i+1][j] * BASE_R + H[i][j+1] * BASE_C - H[i+1][j+1] * BASE_R * BASE_C`。其中 BASE_R 和 BASE_C 分别是行方向和列方向的基数。

**子矩阵计算**：对于左上角 (r1,c1)、右下角 (r2,c2) 的子矩阵，其哈希 = `H[r1][c1] - H[r2+1][c1] * powR[r2-r1+1] - H[r1][c2+1] * powC[c2-c1+1] + H[r2+1][c2+1] * powR[r2-r1+1] * powC[c2-c1+1]`。这是容斥原理在矩阵上的直接应用——先减去下方子矩阵的贡献，再减去右方子矩阵的贡献，最后加回被重复减去的右下角部分。预处理 powR 和 powC 的幂次表后，任何子矩阵的哈希值都可以在 O(1) 时间内计算，这使得二维模式匹配（如 UVa11019 Matrix Matcher）可以使用哈希法在 O(NM) 时间内完成。

### 知识脉络

```
字符串比较需求
    │
    ├──→ 逐字符比较 O(N) ──→ 哈希 O(1) ──代价──→ 冲突风险
    │                                              │
    │                           ┌──────────────────┘
    │                           ▼
    │                     滚动哈希(后缀递推)
    │                           │
    ├──→ 子串查询 ──────────────┤
    │                           │
    └──→ 二分+哈希 ────────────→ LCP/最长子串/模式匹配(二分判定)
```

**本书跨章节连接**：字符串哈希的**二分+判定**模式在第 4.3 节（几何）中以"二分答案+半平面交判定"的形式出现——相同的策略用于判定"存在一个点满足距离约束"；在第 3.10 节（kd-Tree）中，"二分+哈希判定"的变形用于快速匹配二维子矩阵。哈希本质上是将比较性判定用 O(1) 时间完成，这是贯穿全书的优化思路。

### 快速上手模板

```cpp
const ULL BASE = 3137;  // 大于字符集大小的质数
ULL H[N], P[N];          // H: 后缀哈希, P: BASE的幂

void init_hash(const string& s) {
    int n = s.length();
    H[n] = 0, P[0] = 1;
    for (int i = 1; i <= n; i++) P[i] = P[i-1] * BASE;
    for (int i = n-1; i >= 0; i--)
        H[i] = s[i] + H[i+1] * BASE;  // 后缀递推
}

ULL get_hash(int l, int r) {  // 子串 [l, r] 的哈希, 0-based
    return H[l] - H[r+1] * P[r-l+1];
}

// 二分+哈希 求两个位置开始的 LCP
int lcp(int i, int j, int n) {
    int l = 0, r = min(n-i, n-j);
    while (l < r) {
        int mid = (l + r + 1) / 2;
        if (get_hash(i, i+mid-1) == get_hash(j, j+mid-1))
            l = mid;
        else r = mid - 1;
    }
    return l;
}
```

## 例题20  口吃的外星人（Stammering Aliens, SWERC 2009, UVa12206）

### 题目描述
给定一个字符串和一个整数M，求**长度最长**的子串，使得该子串在字符串中**不重叠地出现至少M次**。如果有多个相同长度的满足条件的子串，输出**最靠右**出现的那个。

- **输入格式**：多组数据。每组一行：M和字符串（M=0结束）。
- **输出格式**：每组一行：`最长长度 最右出现位置`。若不存在，输出 `none`。
- **约束**：字符串长度 ≤ 40000，M至少为1。

### 解题思路
使用**字符串Hash + 二分答案**：
1. **滚动哈希**：预处理字符串后缀的哈希值，使得任意子串的哈希值可O(1)计算。
2. **二分长度**：对答案长度L进行二分。check函数判断是否存在长度≥L的、出现≥M次的子串。
3. **check函数**：计算所有长度为L的子串的哈希值，排序后扫描，若同一个哈希值连续出现≥M次则合法。同时记录最右出现位置。
4. **hash_cmp**：当哈希值相同时，按起始位置排序（保证"最右"优先级）。

### 算法方法
**滚动哈希（Rolling Hash）+ 二分答案（Binary Search）**：使用固定基数的多项式哈希，O(1)求子串哈希值。通过对哈希值排序，将相同子串聚集在一起，统计出现次数。二分枚举长度，找到最大可行长度。

### 复杂度分析
- **时间复杂度**：O(N log²N)，二分logN轮，每轮计算N个子串哈希并排序 O(N log N)。
- **空间复杂度**：O(N)，存储哈希值和后缀数组。

```cpp
// 例题20  口吃的外星人（Stammering Aliens, SWERC 2009, UVa12206）
// 陈锋
// 题目：求长度最长的、出现至少M次的子串，输出长度和最右出现位置
// 算法：滚动哈希 + 二分答案 + 排序统计
#include <algorithm>
#include <cstdio>
#include <iostream>
#include <vector>
using namespace std;
typedef unsigned long long ULL;
const int MAXN = 40000 + 8;
const ULL x = 123;  // 哈希基数（大于字母表大小的质数）
ULL H[MAXN], PX[MAXN], Hash[MAXN];  // H: 后缀哈希, PX: x的幂, Hash: 子串哈希

void init_PX() {  // 预计算 x 的幂次
  PX[0] = 1;
  for (int i = 1; i < MAXN; i++) PX[i] = x * PX[i - 1];
}

int N, sa[MAXN];  // N: 字符串长度, sa: 后缀起始位置数组

void init_hash(const string& s) {  // 预计算后缀哈希值
  N = s.length(), H[N] = 0;
  for (int i = N - 1; i >= 0; i--) H[i] = (s[i] - 'a' + 1) + H[i + 1] * x;
}

bool hash_cmp(int a, int b) {  // 自定义排序：哈希值优先，其次位置
  if (Hash[a] != Hash[b]) return Hash[a] < Hash[b];
  return a < b;
}

// 检查是否存在长度≥L的子串，出现至少M次，并记录最右位置pos
bool ok(int L, int M, int& pos) {
  for (int i = 0; i <= N - L; i++)
    sa[i] = i, Hash[i] = H[i] - H[i + L] * PX[L];  // 计算子串[i, i+L-1]的哈希
  sort(sa, sa + N - L + 1, hash_cmp);  // 按哈希排序：相同子串聚集
  pos = -1;
  for (int i = 0, c = 0; i <= N - L; i++) {
    if (i == 0 || Hash[sa[i]] != Hash[sa[i - 1]]) c = 0;  // 新子串，重置计数
    if (++c >= M) pos = max(pos, sa[i]);  // 出现≥M次 → 更新最右位置
  }
  return pos >= 0;
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  init_PX();
  string word;
  for (int t = 0, pos, M; cin >> M >> word && M; t++) {
    init_hash(word);
    if (!ok(1, M, pos)) { puts("none"); continue; }  // 长度1都无法满足
    int l = 1, r = N + 1;
    while (l + 1 < r) {  // 二分查找最大长度
      int m = l + (r - l) / 2;
      if (ok(m, M, pos)) l = m;  // 可行，尝试更大的长度
      else r = m;
    }
    ok(l, M, pos);  // 最后确认
    printf("%d %d\n", l, pos);
  }
  return 0;
}
// Accepted 880ms 1613 C++ 5.3.0 2020-12-14 13:07:48 25845792
```

## 例题19  生命的形式（Life Forms, UVa 11107）

### 题目描述
给定N个DNA序列（字符串，仅含小写字母），求**最长的子串**，使得该子串在**超过N/2个**不同的序列中出现过。输出所有满足条件的最长子串（按字典序）。

- **输入格式**：多组数据。每组第一行为N（N=0结束），接下来N行每行一个DNA序列。
- **输出格式**：每组输出所有满足条件的最长子串，每组数据间用空行分隔。若不存在，输出 `?`。
- **约束**：N ≤ 100，每个序列长度 ≤ 1000。

### 解题思路
使用**后缀数组 + 二分答案**：
1. **后缀数组构建**：将所有序列用不同的分隔符连接（分隔符大于字母范围且互不相同），构建合并字符串的后缀数组和height数组。
2. **height分组**：height[i]表示排名第i和第i-1的后缀的最长公共前缀(LCP)。按height≥L将后缀分成若干组，每组内的后缀的公共前缀长度至少为L。
3. **check函数**：对于长度L，扫描height数组，每当height[R] < L时，检查当前组是否包含超过N/2个不同序列中的后缀。使用`flag`数组标记来自哪些序列。
4. **二分答案**：对最大长度进行二分，找到最大值L，然后输出所有长度为L的满足条件的子串。
5. **idx数组**：记录每个字符位置属于哪个原始序列。

### 算法方法
**后缀数组（Suffix Array）+ height数组 + 二分答案**：后缀数组用于快速查找子串和计算LCP。height数组用于分组，将具有公共前缀的后缀聚集在一起。二分答案确定最大长度。

### 复杂度分析
- **时间复杂度**：O(Σlen × log Σlen)，其中Σlen为所有序列总长度。后缀数组构建O(n log n)，二分log n轮，每轮扫描O(n)。
- **空间复杂度**：O(Σlen)，存储后缀数组及辅助数组。

```cpp
// 例题19  生命的形式（Life Forms, UVa 11107）
// 陈锋
// 题目：找在超过一半的序列中都出现过的最长子串
// 算法：后缀数组 + height数组分组 + 二分答案
#include <algorithm>
#include <cstdio>
#include <cstring>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
typedef long long LL;

// 后缀数组模板（倍增法，O(n log n)）
template <int SZ>
struct SuffixArray {
  int s[SZ];          // 原始字符数组（最后一个字符必须是0）
  int sa[SZ];         // 后缀数组：sa[i] = 排名第i的后缀起始位置
  int rank[SZ];       // 名次数组：rank[i] = 后缀i的排名
  int height[SZ];     // height数组：height[i] = LCP(sa[i], sa[i-1])
  int t[SZ], t2[SZ], c[SZ];  // 辅助数组
  int n;              // 实际字符个数

  void clear() { n = 0, fill_n(sa, SZ, 0); }

  // m为字符集大小（最大字符值+1）
  void build_sa(int m) {
    int i, *x = t, *y = t2;
    // 第一步：基数排序，对单个字符排序
    for (i = 0; i < m; i++) c[i] = 0;
    for (i = 0; i < n; i++) c[x[i] = s[i]]++;
    for (i = 1; i < m; i++) c[i] += c[i - 1];
    for (i = n - 1; i >= 0; i--) sa[--c[x[i]]] = i;
    // 倍增：对长度为2k的子串排序
    for (int k = 1; k <= n; k <<= 1) {
      int p = 0;
      // y[i] = 第二关键字排名第i的后缀起始位置
      for (i = n - k; i < n; i++) y[p++] = i;
      for (i = 0; i < n; i++)
        if (sa[i] >= k) y[p++] = sa[i] - k;
      // 基数排序第一关键字
      for (i = 0; i < m; i++) c[i] = 0;
      for (i = 0; i < n; i++) c[x[y[i]]]++;
      for (i = 0; i < m; i++) c[i] += c[i - 1];
      for (i = n - 1; i >= 0; i--) sa[--c[x[y[i]]]] = y[i];
      swap(x, y);
      p = 1; x[sa[0]] = 0;
      for (i = 1; i < n; i++)
        x[sa[i]] = y[sa[i - 1]] == y[sa[i]] && y[sa[i - 1] + k] == y[sa[i] + k] ? p - 1 : p++;
      if (p >= n) break;
      m = p;
    }
  }

  void build_height() {  // 构建height数组：O(n)
    for (int i = 0; i < n; i++) rank[sa[i]] = i;
    for (int i = 0, k = 0; i < n; i++) {
      if (k) k--;
      int j = sa[rank[i] - 1];
      while (s[i + k] == s[j + k]) k++;
      height[rank[i]] = k;
    }
  }
};

const int MAXL = 1000 + 8, MAXN = 100 + 4;
int idx[MAXL * MAXN], flag[MAXN], N;  // idx: 位置→序列编号, flag: 标记哪些序列被覆盖
char buf[MAXL];
SuffixArray<MAXL * MAXN> sa;

// 判断分组[L,R)是否包含超过N/2个不同序列
bool good(int L, int R) {
  if (R - L <= N / 2) return false;
  fill_n(flag, MAXN, 0);
  int cnt = 0;
  _for(i, L, R) {
    int x = idx[sa.sa[i]];  // 该后缀属于哪个序列
    if (x != N && !flag[x]) flag[x] = 1, cnt++;
  }
  return cnt > N / 2;
}

void print_sub(int L, int R) {  // 输出子串 s[L, R)
  _for(i, L, R) printf("%c", sa.s[i] - 1 + 'a');
  puts("");
}

// 检查是否存在长度为len的满足条件的子串，print=true时输出
bool print_sol(int len, bool print = false) {
  for (int L = 0, R = 1; R <= sa.n; R++) {
    if (R == sa.n || sa.height[R] < len) {  // height断点：新组开始
      if (good(L, R)) {
        if (!print) return true;
        print_sub(sa.sa[L], sa.sa[L] + len);  // 输出第一个后缀的前len个字符
      }
      L = R;  // 新组从R开始
    }
  }
  return false;
}

void solve(int maxLen) {
  if (!print_sol(1)) { puts("?"); return; }  // 长度为1都不满足
  int L = 1, R = maxLen, M;
  while (L < R) {  // 二分最大长度
    M = L + (R - L + 1) / 2;
    if (print_sol(M)) L = M;
    else R = M - 1;
  }
  print_sol(L, true);  // 输出所有最长子串
}

void add(int ch, int i) { idx[sa.n] = i, sa.s[sa.n++] = ch; }  // 添加字符（属于序列i）

int main() {
  for (int t = 0; scanf("%d", &N) == 1 && N; t++) {
    if (t) puts("");
    int maxl = 0;
    sa.n = 0;
    _for(i, 0, N) {
      scanf("%s", buf);
      int sz = strlen(buf);
      maxl = max(maxl, sz);
      _for(j, 0, sz) add(buf[j] - 'a' + 1, i);  // 映射到[1,26]
      add(100 + i, N);  // 分隔符（各序列使用不同分隔符，互不相同）
    }
    add(0, N);  // 字符串结束符
    if (N == 1)
      puts(buf);  // 特殊情况：N=1，输出整个字符串
    else
      sa.build_sa(N + 100), sa.build_height(), solve(maxl);
  }
  return 0;
}
// Accepted 70ms 3250 C++5.3.0 2020-12-1412:59:10 25845774
```

## 例题21  扩展成回文（Extend to Palindrome, UVa11475）

### 题目描述
给定一个字符串S，在S的**末尾追加最少的字符**，使得结果字符串变为回文串。输出最终的回文串。

- **输入格式**：多组数据。每组一行一个字符串S。
- **输出格式**：每组一行，输出扩展后的回文串。
- **约束**：|S| ≤ 10^5。

### 解题思路
问题等价于：找到S的**最长回文后缀**，然后将回文后缀之前的部分反转后追加到S末尾。使用 **Manacher算法**：
1. **Manacher预处理**：将字符串插入`$`和`#`分隔符，计算每个位置的回文半径`P[i]`。
2. **找最长回文后缀**：遍历所有位置i，如果 `P[i] + i == 总长度`（即该回文串的右端到达字符串末尾），则该回文串是后缀。记录 `ans = max(ans, P[i] - 1)`（`P[i]-1`为原始字符串中的回文长度）。
3. **构造答案**：先输出原始字符串S，再输出 `S[0 .. L-ans-1]` 的反转（即回文后缀之前部分的反转）。

### 算法方法
**Manacher（马拉车算法）**：线性时间求字符串的所有回文子串信息。核心是利用已知回文对称性避免重复计算，维护当前最右回文边界和中心。每个位置的回文半径O(1)摊销计算。

### 复杂度分析
- **时间复杂度**：O(N)，Manacher算法为线性时间。
- **空间复杂度**：O(N)，转换后的字符串长度为2N+2，回文半径数组同样大小。

```cpp
// 例题21  扩展成回文（Extend to Palindrome, UVa11475）
// 陈锋
// 题目：在字符串末尾追加最少字符使其成为回文串
// 算法：Manacher找最长回文后缀，将前缀反转追加到末尾
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 1e5 + 4;
char S[MAXN], T[MAXN * 2];  // S: 原始串, T: 转换后的带分隔符串
int P[MAXN * 2];            // P[i]: 以i为中心的回文半径

// Manacher算法：计算每个位置的回文半径
void manacher(const char *s, int len) {
  int l = 0;
  // 预处理：在每字符间插入分隔符 '#', 首尾加边界符
  T[l++] = '$', T[l++] = '#';  // '$' 是左边界保护符
  for(int i = 0; i < len; i++) T[l++] = s[i], T[l++] = '#';
  T[l] = 0;  // 字符串结束符

  int r = 0, c = 0;  // r: 最右回文边界, c: 对应的回文中心
  for(int i = 0; i < l; i++) {
    int &p = P[i];
    // 利用对称性：i关于c的对称点 2*c-i 的回文半径
    p = r > i ? min(P[2 * c - i], r - i) : 1;
    // 中心扩展
    while(T[i + p] == T[i - p]) p++;
    if(i + p > r) r = i + p, c = i;  // 更新最右边界和中心
  }
}

int main() {
  while(scanf("%s", S) == 1) {
    int ans = 0, L = strlen(S);
    manacher(S, L);
    // 找最长回文后缀：回文右端到达字符串末尾
    for(int i = 0; i < 2 * L + 2; i++)
      if(P[i] + i == 2 * L + 2)  // 回文延伸到末尾
        ans = max(ans, P[i] - 1);  // P[i]-1 = 原始串中的回文长度
    printf("%s", S);  // 先输出原串
    // 将回文后缀之前的部分反转输出
    for(int i = L - ans - 1; i >= 0; i--) printf("%c", S[i]);
    puts("");
  }
  return 0;
}
// 24183083 11475 Extend to Palindrome  Accepted  C++11 0.010 2019-11-12 07:25:40
```
