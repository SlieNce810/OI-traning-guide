# 6.3 暴力法专题

暴力法并非简单的"穷举所有可能"，而是通过巧妙的搜索策略、剪枝技术和数据结构（如DLX、A*、alpha-beta剪枝）使暴力搜索在可接受的时间内找到解。本章介绍三个典型例子。

> **学习目标**：掌握把搜索约束转化为精确覆盖矩阵的方法论，以及DLX、迭代加深、估价函数三大暴力法武器。

## 理论基础

### 为什么需要学这个？

很多同学对"暴力法"有误解——以为就是for循环套for循环然后祈祷出结果。真正的暴力法是一门精密艺术：你要先把问题转化为"在超大的解空间中找某一个特殊点"，然后用各种技巧把这个搜索空间压扁、剪掉、加速。

本节展示的是三类最核心的"聪明暴力"技术：

1. **Dancing Links（舞蹈链）**：当问题可以建模为"每个约束都必须恰好覆盖一次"时，DLX用双向链表实现 O(1) 的"删列-恢复列"操作，配合贪心选择约束最紧的列（MRV启发式），把数独的搜索分支从天文数字压到毫秒级。
2. **迭代加深与估价函数**：当解的存在深度不确定时，用"先试深度1，不行试深度2"的策略，配合启发式函数提前剪枝，既能像BFS一样找到最短解，又像DFS一样省内存。
3. **Alpha-Beta剪枝**：零和博弈中，"我最大化而对手最小化"的结构天然形成上下界约束，当某个分支的下界已经超过上界时，无需继续搜索。

学完这节，你将能够对付三类经典问题：精确覆盖（数独/N皇后）、最短操作序列搜索（类似推箱子）、和双人博弈（棋类）。关键是掌握"把问题建模为搜索问题"的思维转换。

### 核心概念

**精确覆盖的矩阵模型**：将原问题表示为行=决策、列=约束的0-1矩阵。选择若干行，使得每列恰好被一个1覆盖。16×16数独的矩阵有4096行（每种(r,c,v)的填法）、1024列（格子256 + 行约束256 + 列约束256 + 宫约束256），每行恰好4个1。

```
朴素想法：对每个空格枚举16种字母 → 16^256，不可计算
DLX：转化为精确覆盖 → 在4096×1024稀疏矩阵上回溯 → 毫秒级
```

*DLX的妙处在于双向链表的cover/uncover操作完全对称，一行代码来、一行代码回，回溯不丢任何信息。*

**Dancing Links双向链表的对称性**：`remove(c)` 从水平链表中摘掉列c，再摘掉该列所有行覆盖的其他列；`restore(c)` 按反序一一恢复。这两个操作互为严格逆操作，使得回溯时状态恢复完美无瑕。

**迭代加深与估价函数**：设定搜索深度上限maxDepth，从1开始递增。每一步计算估计剩余代价 h(state)，若 `当前步数 + h(state) > maxDepth` 则提前剪枝。关键是 h(state) 必须满足"可采纳性"——永远不大于真实剩余代价，否则可能错过最优解。

**DLX算法中选择列的策略（MRV启发式）**：在DLX的每一层递归中，选择哪个列进行覆盖对搜索效率至关重要。朴素的顺序选列会导致分支因子巨大。标准做法是使用**最小剩余值（MRV, Minimum Remaining Values）启发式**：遍历当前所有未覆盖的列，选择包含"1"的个数最少的列作为下一层覆盖的目标。这个策略的效果是双重的：第一，当前候选行最少，意味着该层的分支数最小化；第二，"约束最紧"的列优先处理，能更早发现矛盾从而剪枝。在16×16数独中，使用MRV可以将分支因子从平均16降至约2-3，这是DLX能在毫秒级解决16×16数独的关键。具体实现时，在dfs()函数开头遍历 R[0] 到 0 的循环链表，用 S[col]（该列的节点数）比较大小即可找到最紧的列 c。注意：不需要对所有列排序，每次只选S值最小的那一个就足够——因为下一层递归时会重新选择。

**迭代加深与A*算法的关系（IDA*）**：迭代加深A*（IDA*, Iterative Deepening A*）是A*算法与迭代加深搜索的融合，专门解决A*在状态空间巨大时内存爆炸的问题。A*需要维护一个优先队列（open list）存储所有待扩展的状态，当解空间深度较大时内存不可控。IDA*舍弃了优先队列，改用"深度界限+启发式剪枝"的方式：每次迭代设定一个成本界限 threshold，使用DFS搜索所有 f(n) = g(n) + h(n) ≤ threshold 的节点，若找不到解则提高 threshold 到下一轮搜索中遇到的最小超出值。IDA*保留了A*的"可采纳启发式保证最优解"的性质，同时拥有DFS的线性空间复杂度 O(d)。实践中，IDA*特别适合以下场景：状态转移代价为整数且搜索深度可控（如15-puzzle拼图问题、推箱子等），因为 threshold 的递增步长至少为1，不会产生无意义的浮点数微调。IDA*与普通迭代加深的关键区别在于：普通迭代加深只限制深度，而IDA*用启发式函数重定向搜索方向，在同一深度界限内优先探索更有希望的分支。

### 知识脉络

```
精确覆盖问题 → 行=决策, 列=约束的0-1矩阵
    → DLX: 双向循环链表 + O(1)列删除恢复 + MRV启发式
        → 数独建模: 每个(r,c,v)填法覆盖4个约束

双人零和博弈 → Minimax搜索
    → Alpha-Beta剪枝: α(MAX下界) ≥ β(MIN上界)时剪枝
        → 有效分支因子从 b 降到约 √b

最短操作序列 → BFS/DFS + 状态去重
    → IDA*: 迭代加深 + 可采纳启发式估价函数
        → 像BFS一样找最短解, 像DFS一样省内存
```

> **跨章关联**：本节的三类暴力技术各有跨章渊源——DLX的精确覆盖模型在**2.4节**有基础性的矩阵建模介绍，DLX用链表替代了朴素回溯中的数组扫描；IDA*的迭代加深思想是**1.2节**搜索剪枝策略的深度融合，"设置深度界限+启发式估价"将盲目搜索升级为目标导向搜索；Alpha-Beta剪枝的上下界约束本质上是**5.5节**二分图匹配中"贪心选择+回溯修正"思想在博弈树上的推广——每次分支都试图确定一个"可信的得分区间"。

### 快速上手模板

```cpp
// DLX精确覆盖核心框架
struct DLX {
  int n, sz, S[maxn], row[maxnode], col[maxnode];
  int L[maxnode], R[maxnode], U[maxnode], D[maxnode];
  int ans[maxr], ansd;

  void init(int cols) { /* 建立列头节点 0~n 的双向循环链表 */ }

  void remove(int c) {  // 覆盖列c
    L[R[c]] = L[c]; R[L[c]] = R[c];
    FOR(i, D, c) FOR(j, R, i)    // 遍历该列每行
      { U[D[j]] = U[j]; D[U[j]] = D[j]; --S[col[j]]; }
  }
  void restore(int c) {  // 恢复列c（严格逆操作）
    FOR(i, U, c) FOR(j, L, i)  // 反序遍历
      { ++S[col[j]]; U[D[j]] = j; D[U[j]] = j; }
    L[R[c]] = c; R[L[c]] = c;
  }

  bool dfs(int d) {
    if (R[0] == 0) { ansd = d; return true; }  // 所有列已覆盖
    int c = R[0];  // MRV: 选列中1最少的那列
    FOR(i, R, 0) if (S[i] < S[c]) c = i;
    remove(c);
    FOR(i, D, c) {  // 枚举覆盖该列的每行
      ans[d] = row[i];
      FOR(j, R, i) remove(col[j]);  // 删除该行覆盖的其余列
      if (dfs(d + 1)) return true;
      FOR(j, L, i) restore(col[j]); // 回溯恢复
    }
    restore(c);
    return false;
  }
};
```

核心要点：
1. `FOR(i, A, s)` 宏用于遍历链表中除s外的元素
2. remove/restore的对称性是DLX正确性的基石
3. MRV启发式选列使分支因子最小化

## LA2659 Sudoku/POJ3076 SEERC2006

### 题目描述
求解16×16的数独（Sudoku）。数独的规则：
- 每行填入A~P（共16个字母）各恰好一次
- 每列填入A~P各恰好一次
- 每个4×4的小宫格填入A~P各恰好一次

部分格子已预先填入字母，其余为'-'表示待填充。输入可能包含多组数据，要求输出完整的数独解。

### 解题思路
16×16数独是精确覆盖问题（Exact Cover）的经典实例，可以用Donald Knuth提出的DLX（Dancing Links X）算法求解。

将数独转化为精确覆盖问题：
- **行**（候选决策）：在(r,c)位置填入字母v（共16×16×16=4096种可能）
- **列**（约束条件）：
  - SLOT约束：每个格子必须填一个字母（16×16=256列）
  - ROW约束：每行每字母恰好一次（16×16=256列）
  - COL约束：每列每字母恰好一次（16×16=256列）
  - SUB约束：每个4×4宫格每字母恰好一次（16×16=256列）
- 共计1024列，每行恰好覆盖4列

对于已填写的格子，可以直接将其对应的行加入DLX必选集合。

### 算法方法
**DLX（Dancing Links X）精确覆盖算法**：
1. **十字链表**：用双向循环链表表示稀疏矩阵，支持O(1)的列删除/恢复
2. **启发式选择**：每次选择包含1最少的列（MRV启发式），大幅减少分支
3. **回溯搜索**：选中一行，删除该行覆盖的所有列，递归求解；失败则恢复

编码方式：`encode(type, a, b) = type*256 + a*16 + b + 1`，将三维坐标(r,c,v)映射到一个行编号。

### 复杂度分析
- **时间复杂度**：DLX期望时间远小于O(4^(n²))，对于16×16数独通常毫秒级
- **空间复杂度**：O(行×4) = O(4096×4) = O(16384)节点，约16K节点

```cpp
// LA2659 Sudoku/POJ3076 SEERC2006
// Rujia Liu
// 题目：16×16数独 - 使用DLX精确覆盖算法求解
#include<cstdio>
#include<cstring>
#include<vector>
using namespace std;

const int maxr = 5000;        // 最大行数（4^3 + 若干）
const int maxn = 2000;        // 最大列数（4×256 = 1024）
const int maxnode = 20000;    // 最大节点数（每行4个节点 × 4096行）

// DLX（Dancing Links X）精确覆盖算法实现
// 行编号从1开始，列编号为1~n，结点0是表头结点
// 结点1~n是各列顶部的虚拟结点
struct DLX {
  int n, sz;  // 列数，当前结点总数

  int S[maxn];     // S[c] = 第c列当前包含的结点数
  int row[maxnode], col[maxnode]; // 各结点的行、列编号
  int L[maxnode], R[maxnode];     // 左右指针（水平链表）
  int U[maxnode], D[maxnode];     // 上下指针（垂直链表）

  int ansd, ans[maxr];  // 解：长度和选中的行列表

  void init(int n) {  // n是列数
    this->n = n;

    // 初始化表头结点和列顶虚拟结点
    for(int i = 0 ; i <= n; i++) {
      U[i] = i; D[i] = i;      // 垂直方向自环
      L[i] = i-1, R[i] = i+1;  // 水平方向连接
    }
    R[n] = 0; L[0] = n;  // 循环链表闭合

    sz = n + 1;  // 当前已使用n+1个节点（0~n）
    memset(S, 0, sizeof(S));
  }

  // 添加一行：该行覆盖的列编号列表为columns
  void addRow(int r, vector<int> columns) {
    int first = sz;  // 该行第一个节点的编号
    for(int i = 0; i < columns.size(); i++) {
      int c = columns[i];
      // 水平链接：连接前一个节点和下一个节点
      L[sz] = sz - 1; R[sz] = sz + 1;
      // 垂直链接：插入列c的链表头部
      D[sz] = c; U[sz] = U[c];
      D[U[c]] = sz; U[c] = sz;
      row[sz] = r; col[sz] = c;
      S[c]++;  // 列c结点计数+1
      sz++;
    }
    // 该行最后一个节点的R指向第一个节点，形成循环
    R[sz - 1] = first; L[first] = sz - 1;
  }

  // 宏定义：顺着链表A遍历除s外的其他元素
  #define FOR(i,A,s) for(int i = A[s]; i != s; i = A[i]) 

  // 删除列c及其覆盖的所有行
  void remove(int c) {
    L[R[c]] = L[c];  // 从表头链表中移除列c
    R[L[c]] = R[c];
    // 遍历列c中的每个节点
    FOR(i,D,c)
      // 遍历节点i所在行的每个节点
      FOR(j,R,i) {
        U[D[j]] = U[j];  // 从垂直链表中移除j
        D[U[j]] = D[j];
        --S[col[j]];     // 对应列的计数减1
      }
  }

  // 恢复列c及其覆盖的所有行（与remove逆操作）
  void restore(int c) {
    // 按remove的反序恢复（先垂直，再水平）
    FOR(i,U,c)
      FOR(j,L,i) {
        ++S[col[j]];
        U[D[j]] = j;
        D[U[j]] = j;
      }
    L[R[c]] = c;
    R[L[c]] = c;
  }

  // d为递归深度（已选行数）
  bool dfs(int d) {
    if (R[0] == 0) {  // 所有列都被覆盖——找到解
      ansd = d;        // 记录解的长度
      return true;
    }

    // MRV启发式：选择包含1最少的列c（最小剩余值）
    int c = R[0];  // 从第一列开始
    FOR(i,R,0) if(S[i] < S[c]) c = i;

    remove(c);  // 删除第c列
    // 遍历覆盖列c的每一行
    FOR(i,D,c) {
      ans[d] = row[i];  // 选中该行
      // 删除该行覆盖的所有其他列
      FOR(j,R,i) remove(col[j]);
      if(dfs(d+1)) return true;  // 递归求解
      // 回溯：恢复被删除的所有列
      FOR(j,L,i) restore(col[j]);
    }
    restore(c);  // 恢复列c

    return false;
  }

  bool solve(vector<int>& v) {
    v.clear();
    if(!dfs(0)) return false;
    for(int i = 0; i < ansd; i++) v.push_back(ans[i]);
    return true;
  }
};

////////////// 题目相关
#include<cassert>

DLX solver;

// 约束类型常量
const int SLOT = 0;  // 位置约束：每个格子必须填一个字母
const int ROW  = 1;  // 行约束：每行各字母恰好一次
const int COL  = 2;  // 列约束：每列各字母恰好一次
const int SUB  = 3;  // 宫格约束：每4×4宫格各字母恰好一次

// 编码函数：将(type, a, b)编码为行/列编号（1-indexed）
// a, b ∈ [0, 15], type ∈ {0,1,2,3}
int encode(int a, int b, int c) {
  return a * 256 + b * 16 + c + 1;  // 1 ~ 4096
}

// 解码函数：从行编号解码出(r, c, v)
void decode(int code, int& a, int& b, int& c) {
  code--;
  c = code % 16; code /= 16;  // c = v (字母编号)
  b = code % 16; code /= 16;  // b = c (列编号)
  a = code;                    // a = r (行编号)
}

char puzzle[16][20];  // 输入/输出网格（含'\0'结束符）

bool read() {
  for(int i = 0; i < 16; i++)
    if(scanf("%s", puzzle[i]) != 1) return false;
  return true;
}

int main() {
  int kase = 0;
  while(read()) {
    if(++kase != 1) printf("\n");  // 多组数据间空行
    
    // 初始化DLX：1024列 = 256×4种约束
    solver.init(1024);
    
    // 添加所有可能的行（决策）
    for(int r = 0; r < 16; r++)
      for(int c = 0; c < 16; c++) 
        for(int v = 0; v < 16; v++)
          // 如果该位为空('-')或与输入不矛盾
          if(puzzle[r][c] == '-' || puzzle[r][c] == 'A'+v) {
            vector<int> columns;
            columns.push_back(encode(SLOT, r, c));               // 格子约束
            columns.push_back(encode(ROW, r, v));                // 行约束
            columns.push_back(encode(COL, c, v));                // 列约束
            columns.push_back(encode(SUB, (r/4)*4 + c/4, v));   // 宫格约束
            solver.addRow(encode(r, c, v), columns);  // 行编号=encode(r,c,v)
          }

    vector<int> ans;
    assert(solver.solve(ans));  // 确保有解

    // 根据选中的行解码出答案
    for(int i = 0; i < ans.size(); i++) {
      int r, c, v;
      decode(ans[i], r, c, v);
      puzzle[r][c] = 'A' + v;
    }
    // 输出答案
    for(int i = 0; i < 16; i++)
      printf("%s\n", puzzle[i]);
  }
  return 0;
}
// Accepted 641ms 904kB 3295 G++2020-12-23 17:11:54|O22227210
```

## LA3789/UVa12112 Iceman

### 题目描述
在一个n×m的网格中，游戏角色需要将一块冰推到目标位置。网格包含：
- `.`：空地
- `#`：目标位置（视为空地）
- `O`：冰块（可被推动）
- `[`和`]`：冰块的左右两端
- `=`：连接`[`和`]`的中间部分
- `@`：玩家（推动者）
- `X`：墙壁（不可通过）

操作：玩家可以在四个方向（L=左移, R=右移, <=推左, >=推右）上移动一格。推冰块后，冰块会受重力影响下落。目标是让玩家(`@`)到达目标位置(`#`)。求最短操作序列（不超过15步，否则输出无解）。

### 解题思路
使用BFS进行状态空间搜索，同时用A*启发式算法剪枝：
- **状态表示**：将整个网格编码为字符串（n×m个字符）
- **状态转移**：玩家移动+冰块受重力下落（`fall`函数）
- **启发式函数h(s)**：曼哈顿距离的近似（考虑重力因素）
- **剪枝条件**：当前步数+启发值 > 15（最大深度限制）

物理规则模拟（`expand`函数）：
- 玩家移动：推冰块或自身移动
- 推冰块的连锁反应：相邻冰块也可能被推动
- 重力下落：所有`O`和`@`在不接触支撑时下落

### 算法方法
**BFS + A*启发式搜索 + 物理模拟**：
1. **状态编码**：字符串编码网格，用map记录访问状态和路径
2. **物理模拟**：`fall()`函数处理重力下落，`expand()`处理玩家操作
3. **IDA*思想**：如果`h(s)+步骤数>15`则剪枝
4. **四种操作**：`L`（左移）、`R`（右移）、`<`（推左）、`>`（推右）

### 复杂度分析
- **时间复杂度**：O(4^15 × n×m)，但启发式剪枝大幅减少状态，实际运行很快
- **空间复杂度**：O(n×m × 状态数)，使用map存储访问状态

```cpp
// LA3789/UVa12112 Iceman
// Rujia Liu
// 题目：推冰块 - 在网格中推动冰块使玩家到达目标，最多15步
#include<cstdio>
#include<cstring>
#include<string>
#include<map>
#include<queue>
using namespace std;

int n, m, target;            // target: 目标位置（一维坐标）
map<string, string> sol;     // sol[状态] = 到达该状态的操作序列
queue<string> q;             // BFS队列

// 以下是各种字符的属性查找表（加速模拟）
bool icy[256];               // icy[ch] = ch是否为"冰"类字符
char link_l[256], link_r[256];   // 左边/右边连接规则
char clear_l[256], clear_r[256]; // 左边/右边清除规则

// 初始化字符属性查找表
void init(){
  memset(icy, 0, sizeof(icy));
  icy['O'] = icy['['] = icy[']'] = icy['='] = true;  // 这些字符属于"冰"

  memset(link_l, ' ', sizeof(link_l));
  link_l['O'] = ']'; link_l['['] = '=';  // 左边连接字符

  memset(link_r, ' ', sizeof(link_r));
  link_r['O'] = '['; link_r[']'] = '=';  // 右边连接字符

  memset(clear_l, ' ', sizeof(clear_l));
  clear_l[']'] = 'O'; clear_l['='] = '['; clear_l['O'] = 'O'; clear_l['['] = '[';

  memset(clear_r, ' ', sizeof(clear_r));
  clear_r['['] = 'O'; clear_r['='] = ']'; clear_r['O'] = 'O'; clear_r[']'] = ']';
}

// 重力下落模拟：所有O和@在无支撑时向下掉落
string fall(string s){
  int k, r, p;
  // 从下往上扫描（因为下落是向下的）
  for(int i = n-1; i >= 0; i--)
    for(int j = 0; j < m; j++){
      char ch = s[i*m + j];
      if(ch == 'O' || ch == '@'){
        // 找到下方第一个非空格子
        for(k = i+1; k < n; k++) if(s[k*m + j] != '.') break;
        s[i*m + j] = '.';          // 原位置清空
        s[(k-1)*m + j] = ch;       // 落到支撑位置上方
      }else if(ch == '['){  // 处理横放的冰块组[=...=]
        // 找到配对的']
        for(r = j+1; r < m; r++) if(s[i*m + r] == 'X' || s[i*m + r] == ']') break;
        if(s[i*m + r] == ']'){
          // 检查下方是否有支撑
          for(k = i+1; k < n; k++){
            bool found = false;
            for(p = j; p <= r; p++) if(s[k*m + p] != '.'){ found = true; break; }
            if(found) break;
          }
          // 整体下落
          for(p = j; p <= r; p++) s[i*m + p] = '.';
          for(p = j+1; p < r; p++) s[(k-1)*m + p] = '=';
          s[(k-1)*m + j] = '['; s[(k-1)*m + r] = ']';
        }
        j = r;  // 跳过已处理的部分
      }
    }
  return s;
}

// 启发式函数：估算从当前状态到目标的最短距离
int h(string s){
  int a, b, x = s.find('@');
  a = x % m - target % m;    // 水平距离
  if(a < 0) a = -a;
  // 垂直距离：需要考虑下落
  if(x/m > target/m) b = x/m - target/m;
  else b = (x/m < target/m ? 1 : 0);
  return a > b ? a : b;  // 取较大值作为下界
}

// 扩展状态：执行操作cmd
bool expand(string s, char cmd){
  string seq = sol[s] + cmd;   // 当前操作序列
  int x = s.find('@');
  s[x] = '.';  // 暂时移除玩家

  if(cmd == '<' || cmd == '>'){  // 推操作
    s[x] = '@';
    int p = (cmd == '<' ? x+m-1 : x+m+1);  // 被推位置（左/右）
    if(s[p] == 'X') return false;   // 墙，无法推
    else if(s[p] == '.'){           // 空位，推入冰块
      s[p] = 'O';
      // 更新冰块连接关系
      if(icy[s[p-1]]) s[p-1] = link_r[s[p-1]]; 
      if(s[p-1] != '.') s[p] = link_l[s[p]]; 
      if(icy[s[p+1]]) s[p+1] = link_l[s[p+1]];
      if(s[p+1] != '.') s[p] = link_r[s[p]];
    }else{  // 已有冰块，挤走
      s[p] = '.';
      if(icy[s[p-1]]) s[p-1] = clear_r[s[p-1]];
      if(icy[s[p+1]]) s[p+1] = clear_l[s[p+1]];
    }
  }else{  // 移动操作 L/R
    int p = (cmd == 'L' ? x-1 : x+1);  // 目标位置
    if(s[p] == '.') s[p] = '@';        // 空位，直接移动
    else{
      if(s[p] == 'O'){  // 遇到冰块，尝试推动
        int k;
        if(cmd == 'L' && s[p-1] == '.'){
            for(k = p-1; k > 0; k--) if(s[k-1] != '.' || s[k+m] == '.') break;
            s[p] = '.'; s[k] = 'O'; s[x] = '@';
        }
        if(cmd == 'R' && s[p+1] == '.'){
            for(k = p+1; k < n*m; k++) if(s[k+1] != '.' || s[k+m] == '.') break;
            s[p] = '.'; s[k] = 'O'; s[x] = '@';
        }
      }
      if(s[p] != '.'){  // 无法穿过，尝试跳跃
        if(s[p-m] == '.' && s[x-m] == '.') s[p-m] = '@'; else s[x] = '@';
      }
   }
  }  
  s = fall(s);  // 模拟重力下落

  // A*剪枝：当前步数+启发值 > 15，剪枝
  if(h(s) + seq.length() > 15) return false;
  // 检查是否到达目标
  if(s.find('@') == target){ printf("%s\n", seq.c_str()); return true; }
  // 记录新状态
  if(!sol.count(s)){ sol[s] = seq; q.push(s); }
  return false;
}

int main(){
  int caseno = 0;
  init();
  while(scanf("%d%d", &n, &m) == 2){
    if(!n) break;
    char map[20][20];  
    for(int i = 0; i < n; i++) scanf("%s", map[i]);
    string s = "";
    // 编码网格为字符串，'#'替换为'.'并记录目标位置
    for(int i = 0; i < n; i++)
      for(int j = 0; j < m; j++){
        if(map[i][j] == '#'){ target = i*m + j; map[i][j] = '.'; }
        s += map[i][j];
      }
    q.push(s);
    sol.clear();
    sol[s] = "";
    printf("Case %d: ", ++caseno);
    
    // BFS搜索
    while(!q.empty()){
      string s = q.front();
      q.pop();
      // 尝试四种操作
      if(expand(s, '<')) break; if(expand(s, '>')) break;
      if(expand(s, 'L')) break; if(expand(s, 'R')) break;
    }
    while(!q.empty()) q.pop();  // 清空队列
  }
}
// 25878414	12112	Iceman	Accepted	C++	0.040	2020-12-23 09:13:13
```

## UVa1085 House of Cards

### 题目描述
"House of Cards"是一款纸牌游戏。两个玩家Axel和Birgit轮流行动。初始有8张牌摆成一排（交替方向UP/DOWN），随后轮流从牌堆中抽牌（共2n张牌减8张剩余）。

每回合，当前玩家可以选择：
1. **拿在手里**：将当前牌保留在手中（只能同时保留一张）
2. **摆"楼面牌"**：用当前牌（或手中的牌）覆盖相邻的两张方向相对的牌（DOWN+UP），计算得分
3. **新山峰**：在两张相同的FLOOR牌之间建立一个山峰（UP+DOWN），需要手中有一张牌

得分规则：比较三张牌的绝对值之和S。如果至少2张牌是正数（红色），得+S分；否则得-S分。

用alpha-beta剪枝的对抗搜索求出两个玩家都采取最优策略时Axel的最终得分。

### 解题思路
这是经典的零和博弈问题，使用带alpha-beta剪枝的Minimax搜索：
- **状态**：8张牌的牌面和方向、手持牌、当前牌堆位置、累计分数
- **Max层**（Axel）：最大化得分
- **Min层**（Birgit）：最小化得分
- **剪枝**：当beta ≤ alpha时停止搜索该分支

牌的符号表示：正数=红色（+分），负数=黑色（-分）。

### 算法方法
**Alpha-Beta剪枝的Minimax搜索**：
1. **State结构**：表示游戏状态（牌面、方向、手持牌等）
2. **expand()**：生成所有合法的子状态
3. **alphabeta()**：递归搜索，alpha-beta区间剪枝
4. **isFinal()**：判断终态（牌堆耗尽），结算分数

### 复杂度分析
- **时间复杂度**：O(b^d)，b为分支因子（每步约3-8种选择），d为剩余步数2n-8。但alpha-beta剪枝将有效分支因子降至约√b
- **空间复杂度**：O(d)，递归深度=剩余牌数≈2n-8

```cpp
// UVa1085 House of Cards
// 刘汝佳
// 题目：纸牌屋 - 零和博弈，使用Alpha-Beta剪枝的Minimax搜索
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<vector>
using namespace std;

const int UP = 0, FLOOR = 1, DOWN = 2, maxn = 20;
int n, deck[maxn*2];  // deck[]: 牌堆，正数=红色，负数=黑色

struct State {
  int card[8], type[8];  // 8张牌的牌面和方向
  // type[i]: UP=0=朝上, FLOOR=1=楼面（平放）, DOWN=2=朝下
  // 两张相同的FLOOR牌代表一张真实的FLOOR牌
  int hold[2];    // 两个玩家的手持牌（0表示空手）
  int pos;        // 牌堆当前读取位置
  int score;      // MAX游戏者（Axel）的累计得分

  // 生成子状态：牌堆前进一位
  State child() const {
    State s;
    memcpy(&s, this, sizeof(s));
    s.pos = pos + 1;
    return s;
  }

  // 初始化：前8张牌交替UP/DOWN
  State() {
    for(int i = 0; i < 8; i++) {
      card[i] = deck[i];
      type[i] = i % 2 == 0 ? UP : DOWN;  // 偶数列UP，奇数列DOWN
    }
    hold[0] = hold[1] = score = 0;
    pos = 8;  // 牌堆从第8张开始
  }

  // 判断是否为终态（牌堆耗尽）
  bool isFinal() {
    if(pos == 2*n) {
      score += hold[0] + hold[1];  // 结算手持牌
      hold[0] = hold[1] = 0;
      return true;
    }
    return false;
  }

  // 计算三张牌的得分
  // c1, c2, c3: 牌值（正=红, 负=黑）
  int getScore(int c1, int c2, int c3) const {
    int S = abs(c1) + abs(c2) + abs(c3);
    int cnt = 0;
    if(c1 > 0) cnt++; if(c2 > 0) cnt++; if(c3 > 0) cnt++;
    return cnt >= 2 ? S : -S;  // ≥2张红色→正分，否则负分
  }

  // 扩展player的所有合法子状态到ret中
  void expand(int player, vector<State>& ret) const {
    int cur = deck[pos];  // 当前抽到的牌

    // 决策1：拿在手里（前提：手上没牌）
    if(hold[player] == 0) {
      State s = child();
      s.hold[player] = cur;
      ret.push_back(s);
    }

    // 决策2：摆楼面牌（覆盖相邻DOWN+UP组合）
    for(int i = 0; i < 7; i++) if(type[i] == DOWN && type[i+1] == UP) {
      // 用当前抽到的牌覆盖
      State s = child();
      s.score += getScore(card[i], card[i+1], cur);
      s.type[i] = s.type[i+1] = FLOOR;
      s.card[i] = s.card[i+1] = cur;
      ret.push_back(s);
      
      if(hold[player] != 0) {
        // 用手里的牌覆盖（当前牌留在手中）
        State s = child();
        s.score += getScore(card[i], card[i+1], hold[player]);
        s.type[i] = s.type[i+1] = FLOOR; 
        s.card[i] = s.card[i+1] = hold[player];
        s.hold[player] = cur;  // 手里换成新抽的牌
        ret.push_back(s);
      }
    }

    // 决策3：建立新山峰（在两FLOOR之间放UP+DOWN）
    if(hold[player] != 0)
      for(int i = 0; i < 7; i++) 
        if(type[i] == FLOOR && type[i+1] == FLOOR && card[i] == card[i+1]) {
          // 手中牌+当前牌组成山峰
          State s = child();
          s.score += getScore(card[i], hold[player], cur);
          s.type[i] = UP; s.type[i+1] = DOWN; 
          s.card[i] = cur; s.card[i+1] = hold[player]; s.hold[player] = 0;
          ret.push_back(s);

          // 山峰方向也可以反过来
          swap(s.card[i], s.card[i+1]);
          ret.push_back(s);
        }
  }
};

// 带alpha-beta剪枝的对抗搜索（Minimax）
// player=0: MAX层（Axel）, player=1: MIN层（Birgit）
int alphabeta(State& s, int player, int alpha, int beta) {
  if(s.isFinal()) return s.score;  // 终态：返回累计得分

  vector<State> children;
  s.expand(player, children);  // 生成所有合法后继状态

  int n = children.size();
  for(int i = 0; i < n; i++) {
    int v = alphabeta(children[i], player^1, alpha, beta);
    // MAX层：更新alpha（下界）
    if(!player) alpha = max(alpha, v);
    // MIN层：更新beta（上界）
    else beta = min(beta, v);
    // 剪枝条件：beta ≤ alpha
    if(beta <= alpha) break;
  }
  return !player ? alpha : beta;
}

const int INF = 1e9;

int main() {
  int kase = 0;
  char P[10];
  while(scanf("%s", P) == 1 && P[0] != 'E') {
    scanf("%d", &n);
    // 读入牌堆（含颜色标记B=黑色）
    for(int i = 0; i < n*2; i++) {
      char ch;
      scanf("%d%c", &deck[i], &ch);
      if(ch == 'B') deck[i] = -deck[i];  // 黑色→负数
    }
    State initial;
    // 先手玩家由第一张牌的颜色决定：红色→Axel, 黑色→Birgit
    int first_player = deck[0] > 0 ? 0 : 1;
    int score = alphabeta(initial, first_player, -INF, INF);
    // 如果当前玩家P是Birgit，得分取反
    if(P[0] == 'B') score = -score;
    printf("Case %d: ", ++kase);
    if(score == 0) printf("Axel and Birgit tie\n");
    else if(score > 0) printf("%s wins %d\n", P, score);
    else printf("%s loses %d\n", P, -score);
  }
  return 0;
}
// 25878419	1085	House of Cards	Accepted	C++	0.470	2020-12-23 09:14:12
```
