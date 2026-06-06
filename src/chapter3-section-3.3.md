# 3.3 字符串（1）

> **学习目标**：从暴力匹配的问题出发，理解 KMP 失配函数的核心洞察，进而建立"把匹配过程当作自动机"的思维视角。

## 理论基础

### 为什么需要学这个？

想象一下，你在一个长度为一百万的文本串中找一个长度为十万的模式串。如果每次匹配失败都把模式串右移一位重新比，最坏要比较一亿次。这个 O(NM) 的暴力不是"慢"，而是"压根跑不完"。KMP 的精妙之处在于：它利用了**已经匹配过的那些字符所蕴含的信息**。换句话说，当你发现"匹配到位置 j 时失败了"，你不应该忘记前面 j-1 个字符已经匹配成功这件事——这里面藏着"我可以安全跳过多少位置"的答案。理解这个核心直觉之后，KMP 就不再是一串 `while(j && P[i]!=P[j]) j=F[j]` 需要死记硬背的咒语，而是一段有理有据的逻辑。

### 核心概念

#### 1. 失配函数 F[i]：前缀与后缀的"重叠"程度

**一句话定义**：`F[i]` 表示模式串前缀 `P[0..i-1]` 的最长**真**前后缀相等的长度（真前后缀 ≠ 整个字符串自身）。

**最小示例**：`P = "ababc"`。对于前缀 `"aba"`（长度3），最长相等真前后缀是 `"a"`，长度 1。对于前缀 `"abab"`，是 `"ab"`，长度 2。

**本质理解**：当你站在模式串的第 j 个字符处匹配失败时，`F[j]` 告诉你：**前面 j 个字符中，前 F[j] 个字符和后 F[j] 个字符是相同的**。这意味着你可以直接把模式串的"比较窗口"向前滑动 `j - F[j]` 个位置，而从 `F[j]` 处继续比较——因为那一段已经确定匹配了。

**与朴素对比**：朴素匹配失败后无条件回退 i 指针（文本指针）并置 j=0。KMP 失败后 i 不动，j 跳到 `F[j-1]`（或 `F[j]`，取决于实现），i 只进不退，保证总复杂度 O(N+M)。

#### 2. 自动机视角：KMP 就是一台 DFA

**一句话定义**：把模式串的每个前缀看作一个状态，失配函数就是状态机的失败转移边。

**本质理解**：KMP 构建过程本身也是一次"模式串自我匹配"。对于状态（前缀长度）i，当读入字符 `P[i]` 时发生什么？如果 `P[i] == P[j]`，状态前进到 `j+1`；否则沿 `F[j]` 回退到更短的"可能匹配"状态。这和一个自动机读入字符后根据转移边跳转的本质完全一致。**AC 自动机就是将这个思想推广到了多模式串**——它把多个模式串的失配关系织成了一张完整的转移图。

**自动机的严格对应**：KMP 可以形式化为一个确定有限自动机（DFA）。状态集合 = {0, 1, 2, ..., m}（m 为模式串长度，状态 j 表示"已匹配 j 个字符"）。输入字母表 = 文本和模式串的字符集。转移函数 δ(j, c) 定义为：如果 P[j] == c，δ(j, c) = j+1；否则 δ(j, c) = δ(F[j], c)，即沿失配边回退后重试。接受状态为 m（完整匹配）。这个自动机在文本串上只前进不后退——每读一个字符 O(1) 时间内完成状态转移，总 O(n) 扫描完成匹配。之所以状态数只有 O(m)，正是因为 F 数组将看似 O(m²) 的状态转移压缩到了线性——每个状态 j 沿 F 链最多回退 O(1) 次均摊。

#### 3. 失配跳转的直观解释：为什么不重新匹配？

**关键问题**：KMP 匹配文本 T[i] 时，模式当前在位置 j，但 T[i] ≠ P[j]。为什么不把模式串右移一位从 j=0 重新开始比较？

**直观回答**：因为你已经知道 T[i-j .. i-1] 这 j 个字符和 P[0..j-1] 完全匹配。F[j] 表示 P[0..j-1] 的最长相等真前后缀的长度。这意味着 P 的前 F[j] 个字符 = P 的后 F[j] 个字符 = T 的最后 F[j] 个已匹配字符。所以当你把模式右移 j-F[j] 位后，模式的前 F[j] 个字符就自动和 T 的最后 F[j] 个已匹配字符对齐了——**这一段不需要重新比较**。你只需要从 P[F[j]] 开始继续和 T[i] 比较。这就是为什么 j 跳转到 F[j] 而非 0。非零的 F[j] 意味着你已经"赚"了 F[j] 个字符的匹配工作。

#### 4. next 数组递推求法中的边界处理

**核心技巧**：next 数组有两种常用定义。定义一：F[i] 表示前缀 P[0..i-1] 的最长真前后缀长度（常用在循环节判定中）。定义二：next[i] 表示失配时跳转的目标位置（next[0] = -1, next[1] = 0）。两种定义的关系是 next[i] = F[i-1]（当 i > 0）。

**递推过程中的三个关键边界**：(1) `F[0] = F[1] = 0`——空前缀和单字符前缀没有真前后缀是定义好的基态；(2) 递推时 `int j = F[i]` 的 j 可能为 0，此时 `while(j && P[i] != P[j])` 的条件 j 为非零才进入回退，j=0 时如果 P[i]≠P[0]，F[i+1] 正确为 0；(3) 匹配流程中 "j == m" 时重置 `j = F[j]`（或 `j = F[j-1]` 取决于 F 的定义）保证了重叠匹配的正确性——一次匹配完成后不是从头开始，而是从失配函数的返回值继续，以确保不会遗漏重叠出现的模式串。

### 知识脉络

```
暴力O(NM) ──→ 观察: 失败后已知信息被浪费
                   │
                   ▼
           失配函数 F[i] = 最长相等前后缀
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
    KMP 匹配  循环节检测   自动机推广
 (i不回退)   (i % (i-F[i])==0)  ──→ AC自动机(多模式串)
```

**本书跨章节连接**：KMP 的**失配函数/自动机视角**在第 5.2 节（图论）中自然推广为 **AC 自动机**——多个模式串的失配关系织成一张完整的 DFA 转移图。将匹配过程视为自动机状态转移的思路，也在第 3.5 节（后缀自动机）中被推向极致——把字符串的所有子串压缩成一个最小自动机。理解 KMP 的自动机本质，是后续掌握 AC 自动机和 SAM 的前提。

### 快速上手模板

```cpp
// KMP 失配函数（border array）
void getFail(char *P, int *F) {
    int m = strlen(P);
    F[0] = F[1] = 0;  // 空前缀和单字符前缀无真前后缀
    for (int i = 1; i < m; i++) {
        int j = F[i];
        while (j && P[i] != P[j]) j = F[j];  // 回退
        F[i+1] = (P[i] == P[j] ? j + 1 : 0);
    }
}

// KMP 匹配
void kmp(char *T, char *P, int *F) {
    int n = strlen(T), m = strlen(P);
    getFail(P, F);
    for (int i = 0, j = 0; i < n; i++) {
        while (j && T[i] != P[j]) j = F[j];
        if (T[i] == P[j]) j++;
        if (j == m) { /* 匹配成功, 位置 i-m+1 */ j = F[j]; }
    }
}
```

## 例题15  周期（Period, SEERC 2004, Codeforces Gym101461A）

### 题目描述
给定一个长度为n的字符串S（仅含大写字母），对于每个前缀 `S[0..i-1]`（i = 2, 3, ..., n），判断该前缀是否由某个更短的子串重复K次构成（K ≥ 2）。如果存在，输出前缀长度i和重复次数K。

- **输入格式**：多组测试数据。每组第一行为n（n=0时结束），第二行为字符串S。
- **输出格式**：对于每组数据，输出 `Test case #编号`，然后按i从小到大输出满足条件的前缀信息：`i K`。
- **约束**：n ≤ 10^6。

### 解题思路
这是KMP算法中失配函数（prefix function / fail数组）的经典应用。KMP的`F[i]`（或写为`next[i]`）表示字符串前i个字符构成的前缀中，**最长相等前后缀的长度**。

对于长度为i的前缀：
1. 若 `F[i] > 0` 且 `i % (i - F[i]) == 0`，则说明该前缀可以由长度为 `i - F[i]` 的循环节重复K次构成。
2. 重复次数 `K = i / (i - F[i])`。

**原理**：一个字符串有长度为`p = i - F[i]`的循环节的充要条件是 `i % p == 0` 且 `F[i] >= i - p`。当`F[i]`等于`i-p`的整数倍时，后续字符恰好重复前面的模式。

### 算法方法
**KMP（前缀函数 / Prefix Function）**：计算每个位置的最长相等前后缀长度。利用`F[i]`数组判断前缀是否存在循环节。KMP失配函数的计算复杂度为O(n)，是本算法的核心。

### 复杂度分析
- **时间复杂度**：O(N)，KMP的失配函数计算为线性时间。每个位置判断一次。
- **空间复杂度**：O(N)，需存储字符串和F数组（大小N）。

```cpp
// 例题15  周期（Period, SEERC 2004, Codeforces Gym101461A）
// 陈锋
// 题目：对于字符串S的每个前缀，判断是否由某个循环节重复K次构成
// 算法：KMP失配函数 F[i] 判断循环节：若 i % (i-F[i]) == 0 则存在循环节
#include <cstdio>
const int NN = 1e6 + 4;
char P[NN];   // 模式串（输入的字符串）
int F[NN];    // KMP失配函数/前缀函数：F[i] = 前i个字符的最长相等前后缀长度

int main() {
  freopen("period.in", "r", stdin);
  freopen("period.out", "w", stdout);

  for (int n, kase = 1; scanf("%d", &n) == 1 && n; kase++) {
    scanf("%s", P);
    F[0] = 0, F[1] = 0;  // 边界：空前缀和单字符前缀没有真前后缀
    // 计算失配函数 F[i+1]：表示前i+1个字符的最长相等前后缀
    for (int i = 1; i < n; i++) {
      int j = F[i];  // 前i个字符的最长相等前后缀长度
      while (j && P[i] != P[j]) j = F[j];  // 失配：回溯到更短的可能匹配位置
      F[i + 1] = (P[i] == P[j] ? j + 1 : 0);  // 匹配成功则长度+1，否则为0
    }

    printf("Test case #%d\n", kase);
    for (int i = 2; i <= n; i++)
      // 判断前缀长度i是否有循环节：
      // F[i] > 0：存在至少一个非空的真前后缀相等
      // i % (i-F[i]) == 0：循环节长度 i-F[i] 能整除i
      if (F[i] > 0 && i % (i - F[i]) == 0)
        printf("%d %d\n", i, i / (i - F[i]));  // 前缀长度, 循环次数
    printf("\n");
  }
  return 0;
}
// 102087071  Dec/23/2020 12:10UTC+8  chenwz  A - Period  GNU C++11  Accepted  46 ms  4800 KB
```

## UVa11019 Matrix Matcher

### 题目描述
给定一个 n×m 的文本矩阵 T 和一个 x×y 的模式矩阵 P，求 T 中 P 出现的次数。匹配要求是 P 的每一行作为连续子串出现在 T 的对应行中，且所有匹配行的起始列相同（即 P 作为一个矩形子矩阵"覆盖"在 T 上）。

- **输入格式**：第一行为测试组数。每组数据：n m（文本矩阵），然后是 n 行文本；x y（模式矩阵），然后是 x 行模式。
- **输出格式**：每组输出一行一个整数。
- **约束**：n,m ≤ 1000, x,y ≤ 100。

### 解题思路
这是**二维模式匹配**问题，核心思路是**行匹配+列验证**：
1. **AC自动机处理模式行**：将模式P的每一行作为模式串插入AC自动机。对于重复的行使用"代表元"链（repr和next数组），避免重复插入。
2. **逐行扫描文本**：对文本T的每一行，用AC自动机查找所有匹配的模式行。每匹配到一个模式行pr（结束列pos），在位置 `(当前行-pr, pos-len[pr]+1)` 计数+1。
3. **统计答案**：遍历所有可能位置，若某位置计数==x（模式矩阵行数），则说明模式矩阵完整出现在该位置，答案+1。

### 算法方法
**AC自动机（Aho-Corasick）**：用于多模式串匹配。将所有模式行插入AC自动机，BFS建立fail指针。扫描文本行时，利用fail指针实现O(总长度)的匹配。结合二维坐标验证完成矩阵匹配。

### 复杂度分析
- **时间复杂度**：O(n×m + x×y)，AC自动机构建O(x×y)，匹配O(n×m)（每字符最多一次转移）。
- **空间复杂度**：O(x×y×26 + n×m)，AC自动机节点数≤x×y。

```cpp
// UVa11019 Matrix Matcher
// Rujia Liu
// 题目：在文本矩阵中查找模式矩阵的匹配次数
// 算法：AC自动机行匹配 + 二维坐标验证（逐行扫描，列对齐计数）
#include<cstring>
#include<queue>
#include<cstdio>
#include<map>
#include<string>
using namespace std;

const int SIGMA_SIZE = 26;
const int MAXNODE = 10000 + 10;

void process_match(int pos, int v); // 匹配回调：位置pos处匹配到值为v的模式

struct AhoCorasickAutomata {
  int ch[MAXNODE][SIGMA_SIZE];  // 转移表（Trie边）
  int f[MAXNODE];               // fail函数：失配时跳转的节点
  int val[MAXNODE];             // 单词终点标记（非0）
  int last[MAXNODE];            // 输出链表：沿fail链上一个终点节点
  int sz;                       // 当前节点数

  void init() { sz = 1; memset(ch[0], 0, sizeof(ch[0])); }
  int idx(char c) { return c-'a'; }

  // 插入模式串s，标记值为v（必须非0）
  void insert(char *s, int v) {
    int u = 0, n = strlen(s);
    for(int i = 0; i < n; i++) {
      int c = idx(s[i]);
      if(!ch[u][c]) {
        memset(ch[sz], 0, sizeof(ch[sz]));
        val[sz] = 0;
        ch[u][c] = sz++;
      }
      u = ch[u][c];
    }
    val[u] = v;
  }

  // 递归输出以节点j结尾、沿last链的所有模式
  void report(int pos, int j) {
    if(j) { process_match(pos, val[j]); report(pos, last[j]); }
  }

  // 在文本T中查找所有匹配的模式串
  void find(char* T) {
    int n = strlen(T), j = 0;
    for(int i = 0; i < n; i++) {
      int c = idx(T[i]);
      while(j && !ch[j][c]) j = f[j];  // 失配回溯
      j = ch[j][c];
      if(val[j]) report(i, j);         // 匹配到单词结尾
      else if(last[j]) report(i, last[j]); // 沿last链输出
    }
  }

  // BFS构建fail指针
  void getFail() {
    queue<int> q;
    f[0] = 0;
    for(int c = 0; c < SIGMA_SIZE; c++) {
      int u = ch[0][c];
      if(u) { f[u] = 0; q.push(u); last[u] = 0; }
    }
    while(!q.empty()) {
      int r = q.front(); q.pop();
      for(int c = 0; c < SIGMA_SIZE; c++) {
        int u = ch[r][c];
        if(!u) continue;
        q.push(u);
        int v = f[r];
        while(v && !ch[v][c]) v = f[v];
        f[u] = ch[v][c];
        last[u] = val[f[u]] ? f[u] : last[f[u]];  // 输出链表
      }
    }
  }
};

AhoCorasickAutomata ac;

const int maxn = 1000 + 10, maxm = 1000 + 10, maxx = 100 + 10, maxy = 100 + 10;
char text[maxn][maxm], P[maxx][maxy];
int repr[maxx];  // repr[i]: 模式第i行的代表行（去重）
int next[maxx];  // next[i]: 与第i行相等的下一行编号（链表）
int len[maxx];   // 模式各行长度
int tr;          // 当前文本行编号
int cnt[maxn][maxm];  // 匹配计数

// 匹配回调：pos为列位置，v为模式行编号
void process_match(int pos, int v) {
  int pr = repr[v - 1];          // 去重后的模式行编号
  int c = pos - len[pr] + 1;     // 匹配起始列
  while(pr >= 0) {
    if(tr >= pr) cnt[tr - pr][c]++;  // 累加：确保不超出边界
    pr = next[pr];                   // 处理重复行
  }
}

int main() {
  int T, n, m, x, y;
  scanf("%d", &T);
  while(T--) {
    scanf("%d%d", &n, &m);
    for(int i = 0; i < n; i++) scanf("%s", text[i]);

    scanf("%d%d", &x, &y);
    ac.init();
    for(int i = 0; i < x; i++) {
      scanf("%s", P[i]);
      len[i] = strlen(P[i]);
      repr[i] = i; next[i] = -1;
      // 去重：查找前面是否有相同行
      for(int j = 0; j < i; j++)
        if(strcmp(P[i], P[j]) == 0) {
          repr[i] = j; next[i] = next[j]; next[j] = i; break;
        }
      if(repr[i] == i) ac.insert(P[i], i+1);  // 只插入代表性行
    }
    ac.getFail();

    memset(cnt, 0, sizeof(cnt));
    for(tr = 0; tr < n; tr++) ac.find(text[tr]);  // 逐行匹配

    int ans = 0;
    for(int i = 0; i < n-x+1; i++)
      for(int j = 0; j < m-y+1; j++)
        if(cnt[i][j] == x) ans++;  // 所有x行都匹配到该位置
    printf("%d\n", ans);
  }
  return 0;
}
```

## UVa11468 Substring

### 题目描述
给定K个禁止模式串（由字母数字组成）和N个可用字符及其概率。从可用字符中按给定概率随机生成一个长度为L的字符串。求**生成的字符串不包含任何禁止模式串的概率**。

- **输入格式**：T组数据。每组：K（模式数），K行模式串；N（可用字符数），N行每行一个字符和概率；L（生成长度）。
- **输出格式**：`Case #编号: 概率`（6位小数）。
- **约束**：K ≤ 20，各模式长度≤20，N ≤ 62，L ≤ 100。

### 解题思路
使用**AC自动机 + 概率DP**：
1. **AC自动机**：将所有禁止模式串插入，建立fail指针。`match[u]`标记节点u是否代表某个禁止模式的终点（含沿fail链传递）。
2. **DP状态**：`d[u][l]`表示当前在AC自动机的节点u，还需生成l个字符，最终不包含禁止模式的概率。
3. **状态转移**：遍历所有可用字符c（概率prob[c]），若目标节点`v = ch[u][c]`不匹配禁止模式，则 `d[u][l] += prob[c] * d[v][l-1]`。
4. **记忆化搜索**：使用 `vis[u][l]` 标记已计算的状态，递归计算。
5. 注意AC自动机的优化：`getFail`中将失配转移直接填入`ch`表（`ch[r][c] = ch[f[r]][c]`），避免匹配时的while循环。

### 算法方法
**AC自动机（Trie图优化）+ 概率DP（记忆化搜索）**：AC自动机构建Trie图，match标记沿fail传递危险性。DP在自动机状态空间中进行概率计算，记忆化搜索避免重复计算。

### 复杂度分析
- **时间复杂度**：O(Trie节点数 × L × N)。Trie节点数≤400，L≤100，N≤62。
- **空间复杂度**：O(Trie节点数 × L)，DP表和vis表。

```cpp
// UVa11468 Substring
// 陈锋
// 题目：按概率随机生成字符串，求不包含禁止子串的概率
// 算法：AC自动机（Trie图优化）+ 概率DP（记忆化搜索）
#include <bits/stdc++.h>
using namespace std;

const int SIGMA_SIZE = 64;
const int MAXNODE = 500;     // 节点总数
const int MAXS = 20 + 10;    // 模式串个数

int idx[256], n;             // idx: 字符到编号的映射, n: 可用字符数
double prob[SIGMA_SIZE];     // 每个字符的概率

struct AhoCorasickAutomata {
  int ch[MAXNODE][SIGMA_SIZE];  // 转移表（Trie图优化：失配直接填入）
  int f[MAXNODE];               // fail函数
  int match[MAXNODE];           // 是否代表禁止模式（含沿fail传递）
  int sz;                       // 节点总数

  void init() { sz = 1; memset(ch[0], 0, sizeof(ch[0])); }

  void insert(const char *s) {  // 插入禁止模式串
    int u = 0, n = strlen(s);
    for (int i = 0; i < n; i++) {
      int c = idx[s[i]];
      if (!ch[u][c]) {
        memset(ch[sz], 0, sizeof(ch[sz]));
        match[sz] = 0;
        ch[u][c] = sz++;
      }
      u = ch[u][c];
    }
    match[u] = 1;  // 标记为禁止模式终点
  }

  void getFail() {  // BFS建立fail指针（Trie图优化）
    queue<int> q;
    f[0] = 0;
    for (int c = 0; c < SIGMA_SIZE; c++) {
      int u = ch[0][c];
      if (u) { f[u] = 0; q.push(u); }
    }
    while (!q.empty()) {
      int r = q.front(); q.pop();
      for (int c = 0; c < SIGMA_SIZE; c++) {
        int u = ch[r][c];
        if (!u) { ch[r][c] = ch[f[r]][c]; continue; }  // Trie图：直接填入失配转移
        q.push(u);
        int v = f[r];
        while (v && !ch[v][c]) v = f[v];
        f[u] = ch[v][c];
        match[u] |= match[f[u]];  // 沿fail链传递危险性
      }
    }
  }
};

AhoCorasickAutomata ac;
double d[MAXNODE][105];  // DP数组：d[u][l] = 在节点u还需生成l个字符的安全概率
int vis[MAXNODE][105];   // 记忆化标记

// 记忆化搜索：在节点u还需生成L个字符，最终安全的概率
double getProb(int u, int L) {
  if (!L) return 1.0;  // 不需要生成任何字符，一定安全
  if (vis[u][L]) return d[u][L];
  vis[u][L] = 1;
  double &ans = d[u][L];
  ans = 0.0;
  for (int i = 0; i < n; i++)
    if (!ac.match[ac.ch[u][i]])  // 转移到的节点不是危险节点
      ans += prob[i] * getProb(ac.ch[u][i], L - 1);
  return ans;
}

char s[30][30];

int main() {
  int T;
  scanf("%d", &T);
  for (int kase = 1, k, L; kase <= T; kase++) {
    scanf("%d", &k);
    for (int i = 0; i < k; i++) scanf("%s", s[i]);
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
      char ch[9];
      scanf("%s%lf", ch, &prob[i]);
      idx[ch[0]] = i;  // 建立字符到编号的映射
    }
    ac.init();
    for (int i = 0; i < k; i++) ac.insert(s[i]);
    ac.getFail();
    scanf("%d", &L);
    memset(vis, 0, sizeof(vis));
    printf("Case #%d: %.6lf\n", kase, getProb(0, L));
  }
  return 0;
}
// Accepted 310ms 2374 C++ 5.3.0 2020-12-14 11:44:03 25845650
```

## 例题14 strcmp()函数（"strcmp()" Anyone?, UVa11732）

### 题目描述
给定n个字符串，模拟标准库的`strcmp`函数对这些字符串两两比较的总比较次数。`strcmp(s1, s2)`的比较规则为：逐字符比较，直到遇到不同字符或字符串结束。每次字符比较算一次操作。

- **输入格式**：多组数据。每组第一行为n（n=0结束），接下来n行每行一个字符串（仅含数字和大小写字母）。
- **输出格式**：`Case #编号: 总比较次数`。
- **约束**：n ≤ 4000，字符串总长度 ≤ 4×10^6。

### 解题思路
直接枚举所有n(n-1)/2对字符串比较不可行（n²级别）。利用**Trie统计**优化：
1. **Trie存储**：将所有字符串插入Trie，每个节点`cnt[u]`记录经过该节点的字符串数。
2. **逐个统计**：对于每个字符串s，在Trie中沿着s的路径行走：
   - 走在公共前缀上的每个节点，该节点的`cnt`个字符串都与s有公共前缀，每个公共字符被比较2次（s一次，对方一次）
   - 当遇到第一个不同字符处（Trie中没有对应分支），还需要一次不等比较
   - 单词结尾的`val[u]`个字符串与当前s完全相同，需要额外的结尾比较
3. **公式**：设遍历过程中经过的节点u，累计 `cnt[u] * 2`。遇到`val[u]`时加上`val[u]`。最后补上所有对的结尾比较：`n*(n-1)/2`。

### 算法方法
**Trie（字典树/前缀树）**：利用Trie统计公共前缀。每个节点记录经过该节点的字符串个数，从而在遍历时累加与当前字符串共享前缀的字符串对的比较次数。

### 复杂度分析
- **时间复杂度**：O(总字符串长度)，每个字符在插入和查询时各访问一次。
- **空间复杂度**：O(总字符串长度 × 62)，每个字符最多对应Trie中的一个节点。

```cpp
// 例题14 strcmp()函数（"strcmp()" Anyone?, UVa11732）
// 詹益瑞,陈锋
// 题目：模拟两两strcmp比较的总字符比较次数
// 算法：Trie统计公共前缀，按路径累加比较次数
#include<bits/stdc++.h>
using namespace std;
typedef long long LL;
const int SZ = 4e6 + 5, SIGMA = 70;  // 10数字+26大写+26小写=62 < 70

struct Trie {
  int ch[SZ][SIGMA], cnt[SZ], val[SZ], sz = 0;

  // 字符到编号的映射：0-9→0-9, A-Z→10-35, a-z→36-61
  int idx(char c) {
    if (isdigit(c)) return c - '0';
    if (c >= 'A' && c <= 'Z') return c - 'A' + 10;
    return c - 'a' + 36;  // 注意：38已更正为36
  }

  int newNode() {
    fill_n(ch[sz], SIGMA, 0);  // 初始化子节点
    cnt[sz] = 0;               // 经过次数清零
    val[sz] = 0;               // 结尾次数清零
    return sz++;
  }

  void insert(const char* s) {
    int len = strlen(s), u = 0;
    for (int i = 0; i < len; ++i) {
      int c = idx(s[i]), &uc = ch[u][c];
      if (!uc) uc = newNode();  // 创建新节点
      u = uc;
      cnt[u]++;  // 经过该节点的字符串数+1
    }
    val[u]++;  // 该节点结尾的字符串数+1
  }

  // 计算字符串s与Trie中已有字符串的比较次数
  LL query(const char* s) {
    LL x = 0;
    int len = strlen(s), u = 0;
    for (int i = 0; i < len; ++i) {
      int c = idx(s[i]);
      if (!ch[u][c]) return x;  // 没有更多公共前缀 → 后续比较不产生
      u = ch[u][c];
      // 在公共前缀上的每个字符，与cnt[u]个其他字符串比较2次
      x += cnt[u] * 2;
    }
    return x + val[u];  // 加上与完全相同字符串的结尾比较
  }

  void init() { sz = 0, newNode(); }
};

Trie trie;
char s[1004];

int main() {
  for (int n, kase = 1; scanf("%d", &n) && n; kase++) {
    trie.init();
    LL ans = 0;
    for (int i = 1; i <= n; ++i) {
      scanf("%s", s);
      ans += trie.query(s);   // 先查询：计算当前串与所有已插入串的比较次数
      trie.insert(s);          // 再插入：将当前串加入Trie
    }
    ans += n * (n - 1) / 2;  // 补上每对字符串的结尾比较1次（= "\\0" vs c 的1次）
    printf("Case %d: %lld\n", kase, ans);
  }
  return 0;
}
// 26047697 11732 "strcmp()" Anyone?  Accepted  C++ 0.810 2021-02-02 06:31:12
```

## 例题13  背单词（Remember the Word, UVa1401）

### 题目描述
给定一个由小写字母组成的文本串S（长度≤300000）和一个包含不超过4000个单词的字典。求将S分割为字典中单词的**不同分割方案数**（模20071027）。每种分割方案要求S的每个部分都是字典中的某个单词。

- **输入格式**：多组数据。每组先给文本串S和单词数W，然后W行每行一个单词。
- **输出格式**：`Case #编号: 方案数`。
- **约束**：|S| ≤ 300000, W ≤ 4000, 每个单词长度不超过100。

### 解题思路
使用**Trie + 动态规划**：
1. **Trie存储字典**：将所有单词插入Trie中，每个单词在终点节点存储其长度信息（用val[u]=单词编号）。
2. **DP定义**：`D[i]`表示从位置i开始的后缀S[i..L-1]的分割方案数。目标为D[0]。
3. **状态转移**：从后向前扫描文本串。对每个位置i，在Trie中查找以S[i]开始的所有单词前缀。找到单词时，`D[i] = (D[i] + D[i + wordLen]) % MOD`。
4. **find_prefixes**：在Trie中贪心匹配，返回所有在i位置匹配到的单词，避免了对每个位置枚举所有单词。

### 算法方法
**Trie（字典树/前缀树）+ 动态规划（DP）**：Trie用于快速查找以某个位置开始的所有单词前缀，避免逐一枚举字典中的每个单词。DP采用从后向前递推，利用已经计算好的子问题结果。

### 复杂度分析
- **时间复杂度**：O(|S| × L_max)，其中L_max=100为最长单词长度。对每个文本位置最多在Trie中匹配L_max步。
- **空间复杂度**：O(4000×100×26 + |S|) ≈ O(10^7)，Trie节点数最多约400000个。

```cpp
// 例题13  背单词（Remember the Word, UVa1401）
// 陈锋
// 题目：将文本串分割为字典中单词的不同方案数（模20071027）
// 算法：Trie存储字典 + 从后向前的DP
#include <bits/stdc++.h>
using namespace std;
const int maxnode = 4000 * 100 + 10, sigma_size = 26;

// 字母表为全体小写字母的Trie
struct Trie {
  int ch[maxnode][sigma_size];  // 子节点指针
  int val[maxnode];             // 单词编号（非0表示单词结尾）
  int sz;                        // 当前节点总数
  void clear() { sz = 1; memset(ch[0], 0, sizeof(ch[0])); }  // 初始时只有一个根节点
  int idx(char c) { return c - 'a'; }  // 字符c的编号（0~25）

  // 插入字符串s，附加信息v（单词编号，必须非0）
  void insert(const char *s, int v) {
    int u = 0, n = strlen(s);
    for (int i = 0; i < n; i++) {
      int c = idx(s[i]);
      if (!ch[u][c]) {                     // 子节点不存在则创建
        memset(ch[sz], 0, sizeof(ch[sz]));
        val[sz] = 0;                       // 中间节点的附加信息为0
        ch[u][c] = sz++;
      }
      u = ch[u][c];                        // 向下走
    }
    val[u] = v;  // 单词结尾节点存储单词编号
  }

  // 查找以s开始的、长度不超过len的所有单词前缀
  void find_prefixes(const char *s, int len, vector<int>& ans) {
    int u = 0;
    for (int i = 0; i < len; i++) {
      if (s[i] == '\0') break;
      int c = idx(s[i]);
      if (!ch[u][c]) break;               // Trie中没有对应字符，不可能匹配更长的前缀
      u = ch[u][c];
      if (val[u] != 0) ans.push_back(val[u]);  // 找到一个单词
    }
  }
};

const int TL = 3e5 + 4, WC = 4000 + 4, MOD = 20071027;
int D[TL], WLen[WC];  // D: DP数组, WLen: 每个单词的长度
Trie trie;

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  string text, word;
  for (int kase = 1, S; cin >> text >> S; kase++) {
    trie.clear();
    for (int i = 1; i <= S; i++)
      cin >> word, WLen[i] = word.length(), trie.insert(word.c_str(), i);
    int L = text.length();
    fill_n(D, L, 0), D[L] = 1;  // 空后缀有1种方案（边界条件）
    // 从后向前DP
    for (int i = L - 1; i >= 0; i--) {
      vector<int> p;
      trie.find_prefixes(text.c_str() + i, L - i, p);  // 查找以i开始的所有单词
      for (size_t j = 0; j < p.size(); j++)
        D[i] = (D[i] + D[i + WLen[p[j]]]) % MOD;  // 加上跳过该单词后的方案数
    }
    printf("Case %d: %d\n", kase, D[0]);  // 输出整个文本串的分割方案数
  }
  return 0;
}
// Accepted 80ms 1784 C++ 5.3.0 2020-12-1411:33:14 25845627
```

## UVa1449 Dominating Patterns

### 题目描述
给定N个模式串和一个文本串T。求在T中出现次数最多的所有模式串，即"优势模式"（出现次数最多的所有并列第一）。注意：模式可能有重复，相同字符串只算一个模式。

- **输入格式**：多组数据。每组：N（N=0结束），接下来N行模式串，然后一行文本串T。
- **输出格式**：第一行输出最高出现次数，然后按输入顺序输出所有达到该次数的模式串。
- **约束**：N ≤ 150，每个模式串长度≤70，|T| ≤ 10^6。

### 解题思路
使用**AC自动机 + 计数统计**：
1. **AC自动机**：将所有模式串插入AC自动机，BFS建立fail指针和last输出链表。
2. **多模式匹配**：扫描文本串T，利用fail指针快速转移。每匹配到一个模式串终点，沿last链表递归输出所有匹配模式并计数。
3. **去重处理**：使用`map<string, int>`将重复的字符串映射到同一编号，计数时按编号累加。
4. **结果输出**：`max_element`找最大计数，然后按输入顺序输出所有达到最大计数的模式串。

### 算法方法
**AC自动机（Aho-Corasick）**：标准的多模式匹配算法。通过Trie + fail指针在O(|T|)时间内完成所有模式的匹配。last指针构成输出链表，用于快速回溯所有匹配的模式串终点。

### 复杂度分析
- **时间复杂度**：O(Σ|Pi| + |T| + 匹配次数)。AC自动机匹配部分为线性时间。
- **空间复杂度**：O(Σ|Pi| × 26)，AC自动机节点数与所有模式串总长度成正比。

```cpp
// UVa1449 Dominating Patterns
// 刘汝佳
// 题目：在文本中找出现次数最多的所有模式串
// 算法：AC自动机多模式匹配 + map去重计数
#include <bits/stdc++.h>
using namespace std;

const int SIGMA_SIZE = 26, MAXNODE = 11000, MAXS = 150 + 10;
map<string, int> ms;  // 字符串到编号的映射（去重）

struct AhoCorasickAutomata {
  int ch[MAXNODE][SIGMA_SIZE];  // Trie边
  int f[MAXNODE];               // fail指针
  int val[MAXNODE];             // 模式串编号（非0表示终点）
  int last[MAXNODE];            // 输出链表：沿fail的上一终点
  int cnt[MAXS];                // 每种模式的出现次数
  int sz;                       // 节点总数

  void init() {
    sz = 1;
    memset(ch[0], 0, sizeof(ch[0]));
    memset(cnt, 0, sizeof(cnt));
    ms.clear();
  }

  int idx(char c) { return c - 'a'; }

  // 插入模式串s，编号为v
  void insert(char* s, int v) {
    int u = 0, n = strlen(s);
    for (int i = 0; i < n; i++) {
      int c = idx(s[i]);
      if (!ch[u][c]) {
        memset(ch[sz], 0, sizeof(ch[sz]));
        val[sz] = 0;
        ch[u][c] = sz++;
      }
      u = ch[u][c];
    }
    val[u] = v;
    ms[string(s)] = v;  // 记录映射（重复串映射到同一编号）
  }

  // 沿last链表累加计数
  void print(int j) {
    if (j) cnt[val[j]]++, print(last[j]);
  }

  // 在文本T中匹配所有模式
  void find(char* T) {
    int n = strlen(T), j = 0;
    for (int i = 0; i < n; i++) {
      int c = idx(T[i]);
      while (j && !ch[j][c]) j = f[j];  // 失配回溯
      j = ch[j][c];
      if (val[j]) print(j);             // 匹配到单词终点
      else if (last[j]) print(last[j]); // 沿输出链表
    }
  }

  // BFS构建fail指针
  void getFail() {
    queue<int> q;
    f[0] = 0;
    for (int c = 0; c < SIGMA_SIZE; c++) {
      int u = ch[0][c];
      if (u) { f[u] = 0; q.push(u); last[u] = 0; }
    }
    while (!q.empty()) {
      int r = q.front(); q.pop();
      for (int c = 0; c < SIGMA_SIZE; c++) {
        int u = ch[r][c];
        if (!u) continue;
        q.push(u);
        int v = f[r];
        while (v && !ch[v][c]) v = f[v];
        f[u] = ch[v][c];
        last[u] = val[f[u]] ? f[u] : last[f[u]];  // 建立输出链表
      }
    }
  }
};

AhoCorasickAutomata ac;
char text[1000001], P[MAXS][80];

int main() {
  for (int n; scanf("%d", &n) == 1 && n;) {
    ac.init();
    for (int i = 1; i <= n; i++) scanf("%s", P[i]), ac.insert(P[i], i);
    ac.getFail();
    scanf("%s", text);
    ac.find(text);
    int best = *max_element(ac.cnt + 1, ac.cnt + n + 1);  // 最大出现次数
    printf("%d\n", best);
    for (int i = 1; i <= n; i++)
      if (ac.cnt[ms[string(P[i])]] == best) printf("%s\n", P[i]);
  }
  return 0;
}
// Accepted 20ms 2349 C++5.3.0 2020-12-1411:41:37 25845648
```
