# 5.2 深度优先遍历

## 例题9  飞机调度（Now or Later, LA 3211）

### 题目描述
有 `n` 架飞机需要降落，每架飞机有两个可选的降落时间：早降落时间 `E[i]` 和晚降落时间 `L[i]`。你需要为每架飞机选择一个降落时间，使得任意两架飞机的降落时间之差尽可能大（即最小时间间隔最大化）。求这个最大的最小时间间隔。`n ≤ 2000`，时间范围 `[0, 10^7]`。

**输入格式**：多组数据，每组第一行为 `n`，接下来 `n` 行每行两个整数 `E[i] L[i]`。`n=0` 时结束。**输出格式**：对每组数据，输出一个整数表示最大的最小时间间隔。

### 解题思路
**二分答案 + 2-SAT 判定**：最大化最小值是典型的二分答案问题。

**二分框架**：对于猜测的最小间隔 `diff`，判定是否存在一种时间分配方案使得任意两架飞机的降落时间之差不小于 `diff`。

**2-SAT 建模**：每架飞机 `i` 有两个布尔变量：`x[i]=0` 表示选择早降落时间 `E[i]`，`x[i]=1` 表示选择晚降落时间 `L[i]`。

**冲突检测**：枚举两架飞机 `i` 和 `j` 以及各自的赋值 `a` 和 `b`（a,b ∈ {0,1}）。如果 `|T[i][a] - T[j][b]| < diff`，则这两个选择不能同时成立，添加 2-SAT 约束：`¬(x[i]=a ∧ x[j]=b)`，等价于 `(x[i]=a^1) ∨ (x[j]=b^1)`。

对每个二分值 `diff` 运行 2-SAT 判定：
- 如果存在解，说明 `diff` 可行，二分上界上移（或下界上移）。
- 如果无解，说明 `diff` 不可行，二分上界下移。

### 算法方法
- **二分答案（Binary Search）**：二分枚举最小时间间隔 `diff`。
- **2-SAT（Two-Satisfiability）**：基于 DFS 的 2-SAT 判定算法。为每对发生冲突的飞机和时间选择添加逻辑约束。

### 复杂度分析
- **时间复杂度**：`O(log(Range) × (n + n²)) = O(n² log M)`。二分 `log(10^7)` ≈ 24 次。每次判定需要 `O(n²)` 枚举冲突对并添加约束，2-SAT 的 DFS 是 `O(n+m)` 其中 m 为约束数。
- **空间复杂度**：`O(n²)`。2-SAT 图中最多 `O(n²)` 条约束边（但实际冲突边可能较少）。

```cpp
// 例题9  飞机调度（Now or Later, LA 3211）
// 解题思路：二分答案 + 2-SAT 判定——最大化最小时间间隔
// Rujia Liu
#include<cstdio>
#include<vector>
#include<cstring>
using namespace std;

const int maxn = 2000 + 10;

// 2-SAT 求解器：基于 DFS 的回溯搜索
struct TwoSAT {
  int n;
  vector<int> G[maxn*2];    // 隐含图：每个变量 x 有两个结点（x*2 和 x*2+1）
  bool mark[maxn*2];         // 标记已选定的赋值
  int S[maxn*2], c;          // 栈：记录当前搜索路径上的赋值，用于回溯

  // DFS 尝试将 x 设为 true
  bool dfs(int x) {
    if (mark[x^1]) return false;  // x 的否定已经被标记，冲突
    if (mark[x]) return true;     // x 已经被标记，成功
    mark[x] = true;               // 标记 x 为 true
    S[c++] = x;                   // 入栈（用于回溯时取消标记）
    for (int i = 0; i < G[x].size(); i++)
      if (!dfs(G[x][i])) return false; // 递归处理所有蕴含的后继
    return true;
  }

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n*2; i++) G[i].clear();
    memset(mark, 0, sizeof(mark));
  }

  // 添加约束：x = xval OR y = yval
  void add_clause(int x, int xval, int y, int yval) {
    x = x * 2 + xval;
    y = y * 2 + yval;
    G[x^1].push_back(y);   // ¬x → y
    G[y^1].push_back(x);   // ¬y → x
  }

  bool solve() {
    for(int i = 0; i < n*2; i += 2)
      if(!mark[i] && !mark[i+1]) { // 变量 i 还没有被赋值
        c = 0;
        if(!dfs(i)) {               // 尝试 x[i]=0
          while(c > 0) mark[S[--c]] = false; // 回溯：取消所有标记
          if(!dfs(i+1)) return false; // 尝试 x[i]=1，若仍失败则无解
        }
      }
    return true;
  }
};

///////// 题目相关
#include<algorithm>

TwoSAT solver;

int n, T[maxn][2]; // T[i][0]=E[i], T[i][1]=L[i]

// 判定：是否存在方案使得所有飞机的最小时间间隔 ≥ diff
bool test(int diff) {
  solver.init(n);
  for(int i = 0; i < n; i++) for(int a = 0; a < 2; a++)        // 枚举飞机 i 选择 a
    for(int j = i+1; j < n; j++) for(int b = 0; b < 2; b++)    // 枚举飞机 j 选择 b
      if(abs(T[i][a] - T[j][b]) < diff)                         // 如果两个选择冲突（时间间隔不足）
        solver.add_clause(i, a^1, j, b^1);                     // 添加约束：不能同时选择
  return solver.solve();
}

int main() {
  while(scanf("%d", &n) == 1 && n) {
    int L = 0, R = 0;
    for(int i = 0; i < n; i++) for(int a = 0; a < 2; a++) {
      scanf("%d", &T[i][a]);
      R = max(R, T[i][a]);    // 二分上界为最大时间
    }
    // 二分答案：最大化最小间隔
    while(L < R) {
      int M = L + (R-L+1)/2;
      if(test(M)) L = M; else R = M-1;
    }
    printf("%d\n", L);
  }
  return 0;
}
// 25878101	1146	Now or later	Accepted	C++	0.540	2020-12-23 08:06:28
```

## 例题5  圆桌骑士（Knights of the Round Table, CERC2005, LA 3523/SPOJ KNIGHTS）

### 题目描述
亚瑟王的圆桌旁有 `n` 个骑士，其中某些骑士之间有仇恨关系。国王希望安排尽可能多的骑士围坐在一张圆桌旁，要求：
1. 圆桌上的人数必须是奇数（至少 3 人）。
2. 相邻的骑士之间不能有仇恨关系。

问有多少骑士永远不可能被安排到任何一张合法的圆桌上？`n ≤ 1000`。

**输入格式**：多组数据，每组第一行 `n m`（n 个骑士，m 对仇恨关系），接下来 m 行每行两个整数表示一对仇恨关系。n=m=0 时结束。**输出格式**：对每组数据输出一个整数，表示永远无法参与圆桌会议的骑士数量。

### 解题思路
**补图建模**：建立骑士之间的"友好关系"图：两个骑士之间如果没有仇恨，则连一条边。原问题转化为在无向图中找所有属于某个奇圈（长度为奇数的环）的顶点。

**关键定理**：一个无向图中，一个顶点属于某个奇圈当且仅当它属于某个**点双连通分量（BCC）**，并且该 BCC 不是一个二分图（二分图的充要条件是不含奇圈）。

**算法步骤**：
1. 读入仇恨关系，构建补图（友好关系图）。
2. 使用 **Tarjan 算法** 找出所有的点双连通分量（BCC）。
3. 对每个 BCC，使用二分图判定（DFS 染色）检查它是否为二分图：
   - 如果不是二分图（即含有奇圈），则 BCC 中的所有顶点都可以参与圆桌会议。
   - 如果是二分图（无奇圈），则 BCC 中的顶点都不能参与。
4. 最终答案 = n - 可以参与圆桌会议的骑士数量。

**割顶的特殊处理**：一个割顶可能属于多个 BCC，只要它所属的任意一个 BCC 含有奇圈，这个割顶就可以参与圆桌会议。

### 算法方法
- **点双连通分量分解（BCC Decomposition）**：使用 Tarjan 算法（基于 DFS 和 low 函数），通过栈维护边来找出所有 BCC。
- **二分图判定（Bipartite Check）**：通过 DFS 二染色检查 BCC 是否为二分图。

### 复杂度分析
- **时间复杂度**：`O(n + m')`，其中 `m'` 是补图的边数。每个顶点/边在 DFS 中被访问常数次。最坏情况 `m' = O(n²)`。
- **空间复杂度**：`O(n + m')`。需要存储补图的邻接表和 BCC 列表。

```cpp
// 例题5  圆桌骑士（Knights of the Round Table, CERC2005, LA 3523/SPOJ KNIGHTS）
// 解题思路：补图+点双连通分量(BCC)+二分图判定(奇圈=非二分图)
// 陈锋
#include <bits/stdc++.h>
using namespace std;
struct Edge { int u, v; };
const int NN = 1000 + 10;
int pre[NN], iscut[NN], bccno[NN], dfs_clock, bcc_cnt; // bccno标记顶点所属的BCC编号
vector<int> G[NN], bcc[NN];  // G:补图(友好关系), bcc[i]:第i个BCC中的顶点列表

stack<Edge> S;  // 存储边，用于提取BCC

// Tarjan算法求BCC：基于DFS
int dfs(int u, int fa) {
  int lowu = pre[u] = ++dfs_clock, child = 0;  // 初始化时间戳和low值
  for (int i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    Edge e = (Edge) {u, v};
    if (!pre[v]) { // v未被访问：树边
      S.push(e);   // 边入栈
      child++;
      int lowv = dfs(v, u);               // 递归访问v
      lowu = min(lowu, lowv);             // 用子结点的low更新
      if (lowv >= pre[u]) {               // u是割顶（或根）
        iscut[u] = true, bcc[++bcc_cnt].clear();  // 新BCC
        while (true) {
          Edge x = S.top(); S.pop();       // 从栈中弹出边
          if (bccno[x.u] != bcc_cnt)
            bcc[bcc_cnt].push_back(x.u), bccno[x.u] = bcc_cnt; // 记录顶点所属BCC
          if (bccno[x.v] != bcc_cnt)
            bcc[bcc_cnt].push_back(x.v); bccno[x.v] = bcc_cnt;
          if (x.u == u && x.v == v) break; // 弹出了树边，BCC提取完毕
        }
      }
    }
    else if (pre[v] < pre[u] && v != fa) { // 反向边（回边）
      S.push(e), lowu = min(lowu, pre[v]); // 用反向边更新low
    }
  }
  if (fa < 0 && child == 1) iscut[u] = 0;  // 根结点特判：只有一个孩子不算割顶
  return lowu;
}

// 找出所有BCC
void find_bcc(int n) {
  fill_n(pre, n + 1, 0), fill_n(iscut, n + 1, 0), fill_n(bccno, n + 1, 0);
  dfs_clock = bcc_cnt = 0;
  for (int i = 0; i < n; i++)
    if (!pre[i]) dfs(i, -1);
}

int odd[NN], color[NN];    // odd[i]=1表示骑士i可以参与圆桌会议
// 二分图判定：对BCC b进行DFS二染色
bool bipartite(int u, int b) {
  for (int i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    if (bccno[v] != b) continue;    // 只考虑BCC b内的顶点
    if (color[v] == color[u]) return false; // 相邻顶点同色→不是二分图（有奇圈）
    if (!color[v]) {
      color[v] = 3 - color[u];       // 染成另一种颜色（1↔2交替）
      if (!bipartite(v, b)) return false;
    }
  }
  return true;
}

int A[NN][NN]; // 仇恨关系矩阵
int main() {
  for (int kase = 0, u, v, n, m; scanf("%d%d", &n, &m) == 2 && n; ) {
    for (int i = 0; i < n; i++) G[i].clear();
    memset(A, 0, sizeof(A));
    for (int i = 0; i < m; i++) {
      scanf("%d%d", &u, &v), u--, v--;
      A[u][v] = A[v][u] = 1;        // 记录仇恨关系
    }
    // 构建补图：没有仇恨关系的就是友好关系
    for (int u = 0; u < n; u++)
      for (int v = u + 1; v < n; v++)
        if (!A[u][v]) G[u].push_back(v), G[v].push_back(u);

    find_bcc(n);                    // 求出所有BCC
    memset(odd, 0, sizeof(odd));
    for (int i = 1; i <= bcc_cnt; i++) {
      memset(color, 0, sizeof(color));
      for (int j = 0; j < bcc[i].size(); j++)
        bccno[bcc[i][j]] = i;       // 重新设置割顶的bccno（用于二分图判定）
      int u = bcc[i][0];
      color[u] = 1;
      if (!bipartite(u, i))         // 如果BCC i不是二分图（含奇圈）
        for (int j = 0; j < bcc[i].size(); j++) odd[bcc[i][j]] = 1; // BCC内所有顶点都可参与
    }
    int ans = n;
    for (int i = 0; i < n; i++) if (odd[i]) ans--; // 不可参与的骑士数
    printf("%d\n", ans);
  }
  return 0;
}
// Accepted 310ms 7987kB 2556 C++(gcc 8.3)2020-12-1416:05:37  27093919
```

## 例题10  宇航员分组（Astronauts, LA3713/UVa1391） CERC2006

### 题目描述
有 `n` 个宇航员，每个宇航员有一个年龄。需要将他们分配到三个任务 A、B、C 中：
1. 每个宇航员恰好分配一个任务。
2. 任务 C 没有限制。
3. 任务 A 只能由年长的宇航员执行，任务 B 只能由年轻的宇航员执行。年长/年轻定义为：年龄乘以 n 是否 ≥ 总年龄。
4. 有 `m` 对宇航员之间有矛盾，不能分配同一个任务。

求任意一组合法的分配方案。如果无解，输出 "No solution."。`n ≤ 100000`, `m ≤ 100000`。

**输入格式**：多组数据，每组第一行 `n m`，接下来一行 `n` 个整数（年龄），接下来 `m` 行每行两个整数表示矛盾的宇航员编号。n=m=0 时结束。**输出格式**：对每个宇航员输出其分配到的任务（A/B/C）。

### 解题思路
**2-SAT 建模**：每个宇航员 `i` 有一个布尔变量 `x[i]`：
- `x[i] = 0`（false）：宇航员去任务 C。
- `x[i] = 1`（true）：宇航员去任务 A（年长者）或任务 B（年轻者）。

**约束分析**：
1. **矛盾约束**：如果宇航员 `a` 和 `b` 有矛盾，他们不能同时去任务 C：`x[a]=1 ∨ x[b]=1`。
2. **同类约束**：如果 `a` 和 `b` 是同类（都是年长者或都是年轻者），他们不能同时不去 C（即不能分别去 A/B）：`x[a]=0 ∨ x[b]=0`。

**分类**：
- 年长者：`x[i]=1` → 任务 A
- 年轻者：`x[i]=1` → 任务 B
- 所有：`x[i]=0` → 任务 C

两类宇航员的任务 A 和任务 B 本质上是对称的，只是将 `x[i]=1` 映射到不同的任务名。

### 算法方法
- **2-SAT（Two-Satisfiability）**：基于 DFS 回溯的 2-SAT 求解器。

### 复杂度分析
- **时间复杂度**：`O(n + m)`。每组约束对应 2 条边添加到隐含图中，2-SAT 的 DFS 是线性时间。
- **空间复杂度**：`O(n + m)`。隐含图有 `2n` 个顶点和最多 `4m` 条边。

```cpp
// 例题10  宇航员分组（Astronauts, LA3713/UVa1391） CERC2006
// 解题思路：2-SAT建模——每个宇航员选C(0)或A/B(1)，根据年龄类别分到A或B
// 陈锋
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;

const int maxn = 100000 + 5;

struct TwoSAT {
  int n;
  vector<int> G[maxn * 2];  // 隐含图
  bool mark[maxn * 2];       // 已标记的赋值
  int S[maxn * 2], c;        // 回溯栈

  bool dfs(int x) {
    if (mark[x ^ 1]) return false;  // 冲突：x的否定已被标记
    if (mark[x]) return true;
    mark[x] = true;
    S[c++] = x;
    for (int i = 0; i < G[x].size(); i++)
      if (!dfs(G[x][i])) return false;
    return true;
  }

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n * 2; i++) G[i].clear();
    memset(mark, 0, sizeof(mark));
  }

  // 添加约束：x = xval 或 y = yval
  void add_clause(int x, int xval, int y, int yval) {
    x = x * 2 + xval, y = y * 2 + yval;
    G[x ^ 1].push_back(y), G[y ^ 1].push_back(x);
  }

  bool solve() {
    for (int i = 0; i < n * 2; i += 2)
      if (!mark[i] && !mark[i + 1]) {
        c = 0;
        if (!dfs(i)) {
          while (c > 0) mark[S[--c]] = false;
          if (!dfs(i + 1)) return false;
        }
      }
    return true;
  }
};

#include <algorithm>
int n, m, total_age, age[maxn];
int is_young(int x) { return age[x] * n < total_age; } // 判断是否年轻：年龄 < 平均年龄
TwoSAT solver;
int main() {
  while (scanf("%d%d", &n, &m) == 2 && n) {
    total_age = 0;
    for (int i = 0; i < n; i++) scanf("%d", &age[i]), total_age += age[i];
    solver.init(n);
    for (int i = 0, a, b; i < m; i++) {
      scanf("%d%d", &a, &b), a--, b--;
      if (a == b) continue;
      solver.add_clause(a, 1, b, 1);    // 约束1：不能同去任务C（即必须有一人去A或B）
      if (is_young(a) == is_young(b))   // 约束2：同类宇航员
        solver.add_clause(a, 0, b, 0);  // 不能同去任务A或者任务B
    }
    if (!solver.solve()) {
      puts("No solution.");
      continue;
    }
    // 输出方案
    for (int i = 0; i < n; i++)
      if (solver.mark[i * 2])           // x[i]=0 (false)
        puts("C");                       // → 去任务C
      else if (is_young(i))             // x[i]=1 (true)，年轻者
        puts("B");                       // → 去任务B
      else                              // x[i]=1 (true)，年长者
        puts("A");                       // → 去任务A
  }
  return 0;
}
// 5878107	1391	Astronauts	Accepted	C++	0.230	2020-12-23 08:07:31
```

## 例题7  等价性证明（Proving Equivalences, NWERC2008, LA4287/HDU2767）

### 题目描述
有 `n` 个命题和 `m` 个已知的蕴含关系 `u → v`（若 u 成立则 v 成立）。问至少还需要添加多少条蕴含关系，才能使所有命题两两之间可以相互推导（即这 n 个命题成为逻辑等价的）。`n ≤ 20000`, `m ≤ 50000`。

**输入格式**：第一行为测试数据组数 `T`。每组数据第一行 `n m`，接下来 `m` 行每行 `u v`（1 ≤ u, v ≤ n）。**输出格式**：对每组数据输出一个整数，表示最少需要添加的蕴含关系数量。

### 解题思路
**SCC 缩点 + 入度/出度分析**：原图是一个有向图。命题之间"相互推导"等价于图是强连通的。

**算法步骤**：
1. 使用 **Kosaraju/Tarjan 算法** 找出所有强连通分量（SCC），将每个 SCC 缩成一个点。
2. 缩点后得到一个 **DAG**（有向无环图）。
3. 在 DAG 中：
   - 统计入度为 0 的结点数 `a`
   - 统计出度为 0 的结点数 `b`
4. 最少需要添加 `max(a, b)` 条边才能使 DAG 强连通（如果 SCC 数量为 1，答案为 0）。

**原理**：从每个入度为 0 的点引边到每个出度为 0 的点，最终形成一个大环，需要 `max(a, b)` 条边。注意：如果整个图已经是一个 SCC，答案为 0。

### 算法方法
- **强连通分量分解（SCC Decomposition）**：使用 Tarjan 算法（DFS + lowlink）。
- **DAG 缩点（Condensation）**：将每个 SCC 作为一个新结点，根据原图中的跨 SCC 边建立 DAG。

### 复杂度分析
- **时间复杂度**：`O(T × (n + m))`。Tarjan 算法 O(n+m)，缩点和统计入/出度 O(n+m)。
- **空间复杂度**：`O(n + m)`。邻接表存储 O(n+m)，栈和辅助数组 O(n)。

```cpp
// 例题7  等价性证明（Proving Equivalences, NWERC2008, LA4287/HDU2767）
// 解题思路：SCC缩点+DAG入度/出度分析→最少加边数=max(入0数,出0数)
// 陈锋
#include <bits/stdc++.h>
using namespace std;

const int NN = 20000 + 10;

vector<int> G[NN];
int pre[NN], lowlink[NN], sccno[NN], dfs_clock, scc_cnt;
stack<int> S;

// Tarjan 算法求 SCC
void dfs(int u) {
  int &lu = lowlink[u];
  pre[u] = lu = ++dfs_clock, S.push(u);   // 初始化时间戳和low，入栈
  for (size_t i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    if (!pre[v])
      dfs(v), lu = min(lu, lowlink[v]);    // 树边：用子结点的low更新
    else if (!sccno[v])
      lu = min(lu, pre[v]);               // 回边：用反向边的pre值更新
  }
  if (lu == pre[u]) {                     // 发现SCC的根
    scc_cnt++;
    for (int x = -1; x != u; S.pop())
      x = S.top(), sccno[x] = scc_cnt;    // 弹出栈中元素，赋予SCC编号
  }
}

void find_scc(int n) {
  dfs_clock = scc_cnt = 0;
  fill_n(sccno, n, 0), fill_n(pre, n, 0);
  for (int i = 0; i < n; i++)
    if (!pre[i]) dfs(i);
}

int in0[NN], out0[NN];   // in0[i]=1 表示SCC i入度为0; out0[i]=1 表示SCC i出度为0
int main() {
  int T, n, m;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%d", &n, &m);
    for (int i = 0; i < n; i++) G[i].clear();
    for (int i = 0, u, v; i < m; i++) {
      scanf("%d%d", &u, &v), u--, v--;
      G[u].push_back(v);                     // 建图
    }

    find_scc(n);                             // 第一步：求SCC

    // 第二步：统计每个SCC的入度和出度
    fill_n(in0 + 1, scc_cnt, 1), fill_n(out0 + 1, scc_cnt, 1); // 初始假设都为0
    for (int u = 0; u < n; u++)
      for (size_t i = 0; i < G[u].size(); i++) {
        int v = G[u][i];
        if (sccno[u] != sccno[v])            // 跨SCC的边
          in0[sccno[v]] = out0[sccno[u]] = 0; // 标记这两个SCC有入/出度
      }
    int a = 0, b = 0;
    for (int i = 1; i <= scc_cnt; i++) {
      if (in0[i]) a++;                        // 统计入度为0的SCC
      if (out0[i]) b++;                       // 统计出度为0的SCC
    }
    int ans = max(a, b);
    if (scc_cnt == 1) ans = 0;               // 已经是强连通图，不需要加边
    printf("%d\n", ans);
  }
  return 0;
}
// Accepted 187ms 5424kB 1665 G++2020-12-14 16:11:27 34870207
```

## 例题6  井下矿工（Mining Your Own Business, World Finals 2011, LA 5135/SPOJ BUSINESS）

### 题目描述
有一个地下矿井，包含 `n` 个隧道（双向通道）。煤矿塌方的机制是：某个通道会坍塌，导致与其相邻的两个岔路口无法连通。你需要在某些岔路口设置安全出口（逃生井），确保无论哪个隧道坍塌，每个岔路口都能到达至少一个安全出口。要求：安全出口数量最少，并且输出方案数（最小安全出口数量下有多少种不同的设置方案）。`n ≤ 10^5`。

**输入格式**：多组数据，每组第一行 `m`（隧道数），接下来 `m` 行每行两个整数表示隧道连接的两个路口编号。`m=0` 时结束。**输出格式**：对每组数据，输出 `Case k: ans1 ans2`，其中 `ans1` 是最少安全出口数，`ans2` 是不同方案数。

### 解题思路
**点双连通分量（BCC）分析**：该问题可以建模为在无向图中选择一些顶点（安置安全出口），使得删除任意一条边后，每个顶点都能到达至少一个安全出口。关键观察：坍塌只影响"点双连通分量"内部的连通性。

**对每个 BCC 分析**（使用 Tarjan 算法找出所有 BCC）：
1. **BCC 不含割顶**（整个 BCC 就是一个连通分量）：
   - 需要 2 个安全出口（任意选 2 个顶点）。
   - 方案数 = `C(sz, 2) = sz × (sz-1) / 2`。

2. **BCC 恰好包含 1 个割顶**：
   - 需要一个安全出口（放在非割顶的任意顶点）。
   - 方案数 = `sz - 1`（排除割顶后剩余顶点数）。

3. **BCC 包含 2 个或更多割顶**：
   - 不需要额外安全出口（因为可以通过割顶逃到其他 BCC，而其他 BCC 已经处理了）。

### 算法方法
- **点双连通分量分解（BCC Decomposition）**：使用 Tarjan 算法，基于 DFS 和 `Low[v] == Pre[u]` 判定。
- **组合计数**：对每种 BCC 类型计算方案数。

### 复杂度分析
- **时间复杂度**：`O(n + m)`。Tarjan BCC 分解是线性时间。
- **空间复杂度**：`O(n + m)`。存储图、BCC 列表和辅助数组。

```cpp
// 例题6  井下矿工（Mining Your Own Business, World Finals 2011, LA 5135/SPOJ BUSINESS）
// 解题思路：BCC分解+割顶分析——根据每个BCC中割顶数量决定安全出口数和放置方案
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int NN = 1e5 + 8;
typedef long long LL;
int Low[NN], Pre[NN], DfsClock, IsCut[NN], BccNo;
vector<int> G[NN], Bcc[NN];

stack<int> S;
void clear(int &n) {
  for (int i = 1; i <= n; ++i)
    G[i].clear(), Pre[i] = 0, IsCut[i] = 0;  // 清空图和相关数组
  n = BccNo = DfsClock = 0;
}

// Tarjan 算法求 BCC 和割顶
void tarjan(int u, int root) {
  Pre[u] = Low[u] = ++DfsClock, S.push(u);   // 初始化时间戳，入栈
  int child = 0;
  for (auto v : G[u]) {
    if (!Pre[v]) {                           // 树边：v未访问
      tarjan(v, root);
      Low[u] = min(Low[u], Low[v]), child++;  // 更新low
      if (Low[v] == Pre[u]) {                // 发现BCC（注意这里是==，不是>=）
        Bcc[++BccNo].clear();
        for (int x = 0; x != v; S.pop()) Bcc[BccNo].push_back(x = S.top()); // 弹出到v
        Bcc[BccNo].push_back(u);             // u也属于该BCC
      }
      if (u != root && Low[v] >= Pre[u]) IsCut[u] = 1; // 判断割顶（非根）
    }
    else
      Low[u] = min(Low[u], Pre[v]);          // 回边：更新low
  }
  if (u == root && child > 1) IsCut[u] = 1;  // 根结点特判：两个及以上子树才是割顶
}

int main() {
  for (int kase = 1, n, m; ~scanf("%d", &m) && m; ++kase) {
    clear(n);                                // 清空上一组数据
    for (int i = 1, x, y; i <= m; ++i) {
      scanf("%d%d", &x, &y);
      n = max(n, max(x, y));                 // 动态计算最大顶点编号
      G[x].push_back(y), G[y].push_back(x);   // 无向边
    }
    for (int i = 1; i <= n; ++i) if (!Pre[i]) tarjan(i, i); // 对每个连通分量求BCC
    printf("Case %d:", kase);
    LL ans1 = 0, ans2 = 1;                   // ans1:最少安全出口数, ans2:方案数
    for (int i = 1; i <= BccNo; ++i) {
      int cutCnt = 0, sz = Bcc[i].size();
      for (auto v : Bcc[i]) if (IsCut[v]) cutCnt++; // 统计该BCC中的割顶数量

      if (cutCnt == 0)                       // 无割顶：整个图就是一个BCC
        ans1 += 2, ans2 *= 1LL * sz * (sz - 1) / 2; // 需2个出口，任选2个
      else if (cutCnt == 1)                  // 1个割顶：需要1个出口
        ans1++, ans2 *= sz - 1;              // sz-1个非割顶顶点可作出口
      // cutCnt >= 2：不需要出口
    }
    printf(" %lld %lld\n", ans1, ans2);
  }
  return 0;
}
//  Accepted 170ms 20480kB 1710 C++14(gcc 8.3)2020-12-14 16:07:37 27093931
```

## 例题8  最大团（The Largest Clique, UVa 11324）

### 题目描述
给定一个 `n` 个顶点 `m` 条边的有向图。定义 **团（Clique）** 为一组顶点，其中任意两个顶点 u、v 都满足：存在一条从 u 到 v 和一条从 v 到 u 的有向路径（注意：不要求直接相连，只要求可达）。求最大的团的大小。`n ≤ 1000`, `m ≤ 50000`。

**输入格式**：第一行为测试数据组数 `T`。每组数据第一行 `n m`，接下来 `m` 行每行两个整数 `u v`（1 ≤ u, v ≤ n）。**输出格式**：对每组数据，输出一个整数表示最大团的大小。

### 解题思路
**SCC 缩点 + DAG 上的最长路**：本题中的"团"定义恰好等价于：从原图的角度看，如果所有顶点都位于同一个**强连通分量（SCC）** 中，则它们两两之间都有双向路径。但更一般地，在缩点后的 **DAG** 中，一条路径上的所有 SCC 的并集也满足"团"的定义（路径上前面的 SCC 可以到达后面的 SCC）。

**算法步骤**：
1. 使用 **Tarjan 算法** 找出所有 SCC。
2. 将每个 SCC 缩成一个点，构建 **SCC 缩点图**（DAG），每个 SCC 的权值为其中包含的顶点数。
3. 在 DAG 上做 **DP 求最长路**：`dp[u] = SccSz[u] + max(dp[v])`，其中 `v` 是 `u` 在 DAG 中的后继结点。
4. 答案是 `max(dp[i])`（对所有 SCC i）。

**DP 含义**：`dp[u]` 表示从 SCC u 出发能够访问到的最大顶点总数。经过 SCC 缩点后，原图变成了 DAG，DAG 上可以用简单的记忆化搜索求最长路。

### 算法方法
- **强连通分量分解（SCC Decomposition）**：Tarjan 算法。
- **DAG 上的动态规划（DP on DAG）**：记忆化搜索求最长路径。

### 复杂度分析
- **时间复杂度**：`O(T × (n + m))`。Tarjan O(n+m)，DP O(n + m')，其中 m' 是 SCC 缩点图的最大边数 ≤ m。
- **空间复杂度**：`O(n²)`（TG 矩阵）或 `O(n + m)`（若用邻接表）。TG 矩阵为 O(n²) 因为需要判断 SCC 间是否有边。

```cpp
// 例题8  最大团（The Largest Clique, UVa 11324）
// 解题思路：SCC缩点+DAG最长路DP——缩点后每个SCC的权值为其大小
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int NN = 1000 + 10;
vector<int> G[NN];                       // 原图的邻接表
int pre[NN], lowlink[NN], sccno[NN], dfs_clock, scc_cnt;
stack<int> S;

// Tarjan 求 SCC
void dfs(int u) {
  int& lu = lowlink[u];
  pre[u] = lu = ++dfs_clock, S.push(u);   // 初始化时间戳
  for (size_t i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    if (!pre[v])
      dfs(v), lu = min(lu, lowlink[v]);    // 树边
    else if (!sccno[v])
      lu = min(lu, pre[v]);               // 回边
  }
  if (lu == pre[u]) {                     // 找到SCC的根
    scc_cnt++;
    for (int x = -1; x != u; S.pop()) sccno[x = S.top()] = scc_cnt; // 弹出SCC
  }
}

void find_scc(int n) {
  dfs_clock = scc_cnt = 0;
  fill_n(sccno, n, 0), fill_n(pre, n, 0);
  for (int i = 0; i < n; i++)
    if (!pre[i]) dfs(i);
}

int SccSz[NN], TG[NN][NN], D[NN];        // SccSz:SCC大小, TG:SCC缩点图的邻接矩阵, D:DP记忆化

// 记忆化搜索：从SCC u出发的最长路径（可访问的顶点总数）
int dp(int u) {
  int& ans = D[u];
  if (ans >= 0) return ans;               // 已计算，直接返回
  ans = SccSz[u];                         // 至少包含当前SCC的所有顶点
  for (int v = 1; v <= scc_cnt; v++)
    if (u != v && TG[u][v])               // 如果存在u→v的边
      ans = max(ans, dp(v) + SccSz[u]);   // 选择最优的后继
  return ans;
}

int main() {
  int T, n, m;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%d", &n, &m);
    for (int i = 0; i < n; i++) G[i].clear();
    for (int i = 0, u, v; i < m; i++) {
      scanf("%d%d", &u, &v), u--, v--;
      G[u].push_back(v);                  // 建图
    }

    find_scc(n);                          // 第一步：求SCC
    memset(TG, 0, sizeof(TG));            // 初始化缩点图
    memset(SccSz, 0, sizeof(SccSz));
    for (int i = 0; i < n; i++) {
      SccSz[sccno[i]]++;                  // 第二步：统计每个SCC的大小
      for (size_t j = 0; j < G[i].size(); j++)
        TG[sccno[i]][sccno[G[i][j]]] = 1; // 第三步：构造SCC缩点图（DAG）
    }

    int ans = 0;
    memset(D, -1, sizeof(D));             // 初始化DP数组（-1表示未计算）
    for (int i = 1; i <= scc_cnt; i++)    // SCC编号从1到scc_cnt
      ans = max(ans, dp(i));              // 第四步：DP求DAG最长路
    printf("%d\n", ans);
  }
  return 0;
}
// Accepted 80ms 1740 C++5.3.0 2020-12-14 16:16:29 25846267
```
