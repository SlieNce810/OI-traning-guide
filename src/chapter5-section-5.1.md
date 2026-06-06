# 5.1 基础题目选讲

## 例题4  猜序列（Guess, Seoul 2008, LA 4255/UVa1423）

### 题目描述
给定一个长度为 `n` 的序列 `a[1..n]`，你不知道具体数值。但你知道对于所有 `1 ≤ i ≤ j ≤ n` 的区间，区间和 `S[i,j] = a[i] + a[i+1] + ... + a[j]` 的符号（正号 `+`、负号 `-` 或零 `0`）。要求还原出该序列（输出任意一组满足约束的序列）。序列元素取值范围：`[-10, 10]`。`n ≤ 10`。

**输入格式**：第一行是测试数据组数 `T`。每组数据第一行为 `n`，接着是一个长度为 `n(n+1)/2` 的字符串，按行优先顺序给出所有区间符号（从上三角矩阵展开）。**输出格式**：对每组数据，输出一行 `n` 个整数（序列值）。

### 解题思路

**关键思维转换：从"区间和符号"到"前缀和比较"**

设 `sum[k] = a[1] + ... + a[k]`，`sum[0] = 0`。

那么 `S[i,j] = sum[j] - sum[i-1]`。区间和的符号就变成了两个前缀和的大小关系：
- `+` 表示 `sum[j] > sum[i-1]`
- `-` 表示 `sum[j] < sum[i-1]`
- `0` 表示 `sum[j] == sum[i-1]`

问题变成：**给定 sum[0..n] 之间的大小关系，求一组满足所有约束的 sum 值。**

**三步法求解：**

**第一步：合并相等约束（用并查集）**

所有 `S[i,j] == 0` 意味着 `sum[j]` 等于 `sum[i-1]`。用并查集把相等的前缀和索引合并到同一个"代表元"中。

**第二步：建图表达大小关系（> 和 <）**

对于每个 `+`：`sum[j] > sum[i-1]` → 在代表元之间连边 `rep(i-1) → rep(j)`  

对于每个 `-`：`sum[j] < sum[i-1]` → 连边 `rep(j) → rep(i-1)`

现在得到了一张有向图，节点是代表元，边表示"小于"关系。

**第三步：拓扑排序赋值**

对这张图进行拓扑排序。如果能找到拓扑序（无环），按顺序依次赋值 0, 1, 2, ... 就得到所有代表元的 sum 值。

最后，还原原序列：`a[i] = sum[i] - sum[i-1]`

**为什么答案是任意合法的？** 题目要求输出"任意一组"满足约束的序列。因为 n ≤ 10，差值在 [-10,10] 范围内的连续整数必然是合法的。

**给初学者的直观理解**：
- `+` 约束说"这段区间的和是正的" → sum 曲线是在上升
- `-` 约束说"这段区间的和是负的" → sum 曲线是在下降
- `0` 约束说"这段区间的和为 0" → sum 曲线是平的
画出 sum[0..n] 作为纵轴的曲线，拓扑排序就是在给定升降信息后，画一条可能的曲线。

### 算法方法
- **并查集（Disjoint Set Union）**：合并 `'0'` 约束中的相等前缀和结点。
- **拓扑排序（Topological Sort）**：基于 DFS 的拓扑排序，对代表元构成的 DAG 进行排序，按拓扑序赋值。

### 复杂度分析
- **时间复杂度**：`O(T × n²)`。每组测试数据需要构造 O(n²) 条边，拓扑排序 O(n²)。`n ≤ 10`。
- **空间复杂度**：`O(n²)`。邻接矩阵 G 存储最多 `(n+1)²` 个元素，并查集 O(n)。

```cpp
// 例题4  猜序列（Guess, Seoul 2008, LA 4255/UVa1423）
// 解题思路：前缀和建模 + 并查集合并相等结点 + 拓扑排序确定偏序
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<vector>
#include<algorithm>
using namespace std;
const int maxn = 10 + 5;

int n, G[maxn][maxn]; // 有向图邻接矩阵：G[a][b]=1 表示 sum[a] < sum[b]，即 a→b
int c[maxn];           // c[u] = 0:未访问, -1:正在访问（在递归栈中）, 1:已完成访问
vector<int> topo;      // 存储拓扑排序的结果（逆序）

// DFS 拓扑排序：检测 DAG 中的环，同时记录拓扑序
bool dfs(int u){
  c[u] = -1;    // 标记为正在访问（进入递归栈）
  for(int v = 0; v <= n; v++) if(G[u][v]) {
    if(c[v]<0) return false;     // 遇到正在访问的结点，说明存在环
    else if(!c[v]) dfs(v);       // 递归访问未访问的后继结点
  }
  c[u] = 1; topo.push_back(u);   // 标记为已完成，加入拓扑序列（逆序）
  return true;
}

bool toposort(){
  topo.clear();
  memset(c, 0, sizeof(c));       // 初始化访问标记
  for(int u = 0; u <= n; u++) if(!c[u])
    if(!dfs(u)) return false;    // 如果发现环，拓扑排序失败
  reverse(topo.begin(), topo.end()); // 反转得到正确的拓扑序
  return true;
}

// 并查集：用于合并有 '0' 约束（前缀和相等）的结点
int pa[maxn];
int findset(int x) { return pa[x] != x ? pa[x] = findset(pa[x]) : x; }

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    char input[100], S[11][11];
    scanf("%d%s", &n, input);
    int idx = 0;
    // 初始化并查集：0~n 共 n+1 个前缀和结点
    for(int i = 0; i <= n; i++) pa[i] = i;
    for(int i = 1; i <= n; i++)
      for(int j = i; j <= n; j++) {
        S[i][j] = input[idx++];
        if(S[i][j] == '0') pa[j] = i-1; // sum[j]-sum[i-1]=0，因此j和i-1是等价结点
      }

    // 根据符号构造有向图：在代表元之间连边
    memset(G, 0, sizeof(G));
    for(int i = 1; i <= n; i++)
      for(int j = i; j <= n; j++) {
        if(S[i][j] == '-') G[findset(j)][findset(i-1)] = 1; // sum[j]-sum[i-1] < 0 → sum[j] < sum[i-1]
        if(S[i][j] == '+') G[findset(i-1)][findset(j)] = 1; // sum[j]-sum[i-1] > 0 → sum[i-1] < sum[j]
      }
    toposort();     // 对代表元图进行拓扑排序
    int sum[maxn], cur = 0;
    for(int i = 0; i <= n; i++) sum[topo[i]] = cur++; // 按照拓扑序依次赋值：0, 1, 2, ...

    // 恢复原序列：a[i] = sum[i] - sum[i-1]
    for(int i = 1; i <= n; i++) {
      sum[i] = sum[findset(i)];                         // 用代表元的值替代
      if(i > 1) printf(" ");
      printf("%d", sum[i] - sum[i-1]);                  // 注意：sum[0] 未必等于 0
    }
    printf("\n");
  }
  return 0;
}
// 25878073	1423	Guess	Accepted	C++	0.000	2020-12-23 07:58:02
```

## 例题2  独轮车（The Monocycle, UVa 10047）

### 题目描述
有一个 `R × C` 的网格地图，每个格子可以是空地 `.` 或障碍物 `#`。一辆独轮车从起点 `S` 出发，要到达终点 `T`。独轮车的轮子有 5 种颜色（记为 0~4，初始为颜色 0——绿色），每次前进一格车轮颜色变为 `(color+1) % 5`。独轮车面向 4 个方向之一（北/西/南/东，记为 0~3），初始朝北。

每次操作可以：
1. **左转** 90 度（耗时 1 秒，颜色不变）
2. **右转** 90 度（耗时 1 秒，颜色不变）
3. **前进** 1 格（耗时 1 秒，颜色变化）

车轮不得进入障碍物格子。目标状态：到达终点 `T` 且车轮颜色为绿色（颜色 0，与起点相同），方向不限。求最短耗时。`R, C ≤ 25`。

### 解题思路
**状态空间图上的 BFS**：由于车轮有方向和颜色两个额外维度，不能直接在原始网格上 BFS。将状态定义为 `(r, c, dir, color)`，共有 `R × C × 4 × 5` 个状态。

**状态转移**：
1. 左转：`(r, c, (dir+1)%4, color)`，代价 1
2. 右转：`(r, c, (dir+3)%4, color)`，代价 1
3. 前进：`(r+dr[dir], c+dc[dir], dir, (color+1)%5)`，代价 1（需确保目标格子为空地）

由于所有边的权值均为 1，使用 BFS 即可找到最短路径。在搜索过程中，每当到达一个状态 `(tr, tc, *, 0)`（到达终点且颜色为 0），用当前距离更新答案。

**注意事项**：由于所有边权为 1，BFS 自然保证第一次扩展到的状态就是最短距离。但不同方向到达同一目标颜色时可能有多条路径，取最小值即可。

### 算法方法
- **BFS（广度优先搜索）**：在扩展的状态图上进行无权最短路径搜索。状态为 `(r, c, dir, color)` 四元组。

### 复杂度分析
- **时间复杂度**：`O(R × C × 4 × 5) = O(R·C)`。每个状态最多入队一次，每个状态最多扩展 3 个后继状态。
- **空间复杂度**：`O(R × C × 4 × 5)`。需要存储距离数组 `d[maxr][maxc][4][5]` 和访问标记。

```cpp
// 例题2  独轮车（The Monocycle, UVa 10047）
// 解题思路：状态空间图上的 BFS——状态(r,c,dir,color)的最短路径
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<queue>
#include<algorithm>
using namespace std;

const int INF = 1000000000;
const int maxr = 25 + 5;
const int maxc = 25 + 5;
int R, C, sr, sc, tr, tc;
char maze[maxr][maxc];

// 状态：位置(r,c)、方向dir(0=北,1=西,2=南,3=东)、车轮颜色color(0~4，0=绿色)
struct State {
  int r, c, dir, color;
  State(int r, int c, int dir, int color):r(r),c(c),dir(dir),color(color) {}
};

const int dr[] = {-1,0,1,0}; // 方向偏移量：北(north)、西(west)、南(south)、东(east)
const int dc[] = {0,-1,0,1};
int d[maxr][maxc][4][5], vis[maxr][maxc][4][5]; // d存储最短距离，vis标记是否访问

int ans;
queue<State> Q;

// 尝试将状态(r,c,dir,color,耗时v)加入队列
void update(int r, int c, int dir, int color, int v) {
  if(r < 0 || r >= R || c < 0 || c >= C) return;           // 越界检查
  if(maze[r][c] == '.' && !vis[r][c][dir][color]) {         // 空地且未访问
    Q.push(State(r, c, dir, color));                        // 入队
    vis[r][c][dir][color] = 1;                               // 标记已访问
    d[r][c][dir][color] = v;                                  // 记录距离
    if(r == tr && c == tc && color == 0) ans = min(ans, v); // 到达终点且颜色为绿色，更新答案
  }
}

void bfs(State st) {
  d[st.r][st.c][st.dir][st.color] = 0;   // 起点距离为 0
  vis[st.r][st.c][st.dir][st.color] = 1; // 标记起点
  Q.push(st);
  while(!Q.empty()) {
    st = Q.front(); Q.pop();
    int v = d[st.r][st.c][st.dir][st.color] + 1; // 下一步的耗时

    // 三种操作：
    update(st.r, st.c, (st.dir+1)%4, st.color, v);      // 左转：方向+1，颜色不变
    update(st.r, st.c, (st.dir+3)%4, st.color, v);      // 右转：方向+3 ≡ 方向-1，颜色不变
    update(st.r+dr[st.dir], st.c+dc[st.dir],            // 前进：沿当前方向移动
           st.dir, (st.color+1)%5, v);                   // 车轮颜色变为(color+1)%5
  }
}

int main() {
  int kase = 0;
  while(scanf("%d%d", &R, &C) == 2 && R && C) {
    for(int i = 0; i < R; i++) {
      scanf("%s", maze[i]);
      for(int j = 0; j < C; j++)
        if(maze[i][j] == 'S') { sr = i; sc = j; }      // 记录起点位置
        else if(maze[i][j] == 'T') { tr = i; tc = j; }  // 记录终点位置
    }
    maze[sr][sc] = maze[tr][tc] = '.';                  // 将起点和终点标记为空地
    ans = INF;
    memset(vis, 0, sizeof(vis));
    bfs(State(sr, sc, 0, 0));                           // 起始状态：起点，朝北(0)，绿色(0)

    if(kase > 0) printf("\n");
    printf("Case #%d\n", ++kase);
    if(ans == INF) printf("destination not reachable\n");
    else printf("minimum time = %d sec\n", ans);
  }
}
// 25878076	10047	The Monocycle	Accepted	C++	0.000	2020-12-23 07:58:30
```

## 例题3  项链（The Necklace, UVa 10054）

### 题目描述
一条项链由 `n` 颗珠子串成。每颗珠子有两种颜色（分别位于珠子的两端）。珠子可以翻转，即珠子 `(a,b)` 的两端可以调换。现在需要将所有珠子串成一圈，要求相邻珠子的相接处颜色相同。问是否存在一种合法的串法，如果存在则输出任意一种方案。

**输入格式**：第一行为测试数据组数 `T`。每组数据：第一行 `n`（珠子数），接下来 `n` 行每行两个整数 `u v`（珠子的两种颜色，1 ≤ u, v ≤ 50）。**输出格式**：对每组数据，输出 `Case #k`，然后按顺序输出每条边（珠子），每行两个整数表示珠子两端的颜色（顺序同输出顺序串联）。

### 解题思路

**模型转换**：每颗珠子 = 一条连接两种颜色的无向边。问题转化为：**在无向图中找一条经过每条边恰好一次的回路**——这就是**欧拉回路**。

**欧拉回路存在的条件**：
1. 所有顶点的度数为偶数（每进必出）
2. 图连通（所有非零度顶点在同一连通分量）

**算法（递归 DFS + 删边）—— 为什么有效？**

从任意顶点出发，沿还没走过的边 DFS：
1. 来到一个顶点 u，找一条还没用过的边 (u, v)
2. 删除这条边（标记已使用）
3. 递归处理 v
4. **递归返回后**，把边 (u, v) 记录到结果列表

**关键理解**：结果是反向的！因为递归回溯时才记录边——最后完成递归的边在列表最前面。所以输出时需要**逆序输出**。

**为什么这样能得到欧拉回路？**

想象你走到死胡同（所有边都走过了），递归开始回溯。回溯时记录边，意味着"最后走的边最先被记录"。逆序输出后，"最先记录的边最先输出"——这恰好是"从起点出发时先走的边先输出"的正确顺序。

**举例**（三角形 ABC，3 条边 AB、BC、CA）：
1. 从 A 出发：走 AB，删边 AB，递归 B
2. 在 B：走 BC，删边 BC，递归 C
3. 在 C：走 CA，删边 CA，递归 A
4. 在 A：无边可走，回溯到 C，记录 CA
5. 回溯到 B，记录 BC
6. 回溯到 A，记录 AB
7. 结果列表 = [CA, BC, AB]，逆序输出 = AB → BC → CA（完美回路！）

**最终判定**：边数必须等于 n（使用了所有珠子），且回路闭合（最后一条边的终点 = 第一条边的起点）。

### 算法方法
- **欧拉回路（Eulerian Circuit）**：无向图中的欧拉回路。采用递归 DFS 删除边的方式来构造。

### 复杂度分析
- **时间复杂度**：`O(maxColor² + n)`，其中 `maxColor = 50`。每个顶点遍历最多 50 个颜色，每条边访问一次即被删除。
- **空间复杂度**：`O(maxColor²)`。邻接矩阵存储最多 50×50 = 2500 个元素。

```cpp
// 例题3  项链（The Necklace, UVa 10054）
// 解题思路：珠子=边，颜色=顶点，问题转化为无向图的欧拉回路
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<vector>
using namespace std;
const int maxcolor = 50;
int n, G[maxcolor+1][maxcolor+1], deg[maxcolor+1]; // G:邻接矩阵(可重边), deg:度数

struct Edge {
  int from, to;
  Edge(int from, int to):from(from),to(to) {}
};

vector<Edge> ans;     // 存储欧拉回路中的边（反向顺序）
// 欧拉回路递归构造：从顶点u出发走欧拉回路，边回溯边记录
void euler(int u){
  for(int v = 1; v <= maxcolor; v++) if(G[u][v]) {
    G[u][v]--; G[v][u]--;   // 删除使用过的无向边（由于是无向图，两个方向都要减）
    euler(v);                // 递归处理下一个顶点
    ans.push_back(Edge(u, v)); // 回溯时记录边（所以结果是反向的）
  }
}

int main() {
  int T;
  scanf("%d", &T);
  for(int kase = 1; kase <= T; kase++) {
    scanf("%d", &n);
    memset(G, 0, sizeof(G));
    memset(deg, 0, sizeof(deg));
    int start = -1;                                  // 欧拉回路的起始顶点（任意度数非零顶点即可）
    for(int i = 0; i < n; i++) {
      int u, v;
      scanf("%d%d", &u, &v);
      G[u][v]++; G[v][u]++;                          // 无向图：两边都要加
      deg[u]++; deg[v]++;                            // 累计度数
      start = u;                                     // 记录一个起始顶点
    }

    // 判断欧拉回路是否存在：检查所有度数是否为偶数
    bool solved = true;
    for(int i = 1; i <= maxcolor; i++)
      if(deg[i] % 2 == 1) { solved = false; break; } // 存在奇度顶点→无欧拉回路

    if(solved) {
      ans.clear();
      euler(start);
      // 验证：边数正确且回路闭合（起始顶点=终止顶点）
      if(ans.size() != n || ans[0].to != ans[ans.size()-1].from) solved = false;
    }

    printf("Case #%d\n", kase);
    if(!solved)
      printf("some beads may be lost\n");
    else
      for(int i = ans.size()-1; i >= 0; i--) printf("%d %d\n", ans[i].from, ans[i].to); // 逆序输出得到正确顺序

    if(kase < T) printf("\n");
  }
  return 0;
}
// 25878077	10054	The Necklace	Accepted	C++	0.230	2020-12-23 07:58:44
```

## 例题1  大火蔓延的迷宫（Fire!, UVa 11624）

### 题目描述
在一个 `R × C` 的网格迷宫中，`J` 表示 Joe 的起始位置，`F` 表示火的起始位置（可能有多处），`.` 表示空地，`#` 表示墙壁。火每分钟向四个方向（上下左右）蔓延一格，Joe 每分钟也可以向四个方向移动一格。Joe 不能走入墙壁或被火烧到的格子。Joe 需要在被火烧到之前到达迷宫的任意边界格子并逃出。问 Joe 能否逃出以及最短逃出时间。`R, C ≤ 1000`。

**输入格式**：第一行为测试数据组数 `T`。每组数据第一行为 `R C`，接下来 `R` 行每行一个长度为 `C` 的字符串（只含 `J`、`F`、`.`、`#`）。**输出格式**：对每组数据，输出最短逃出时间，如果不能逃出则输出 `IMPOSSIBLE`。

### 解题思路
**双源 BFS**：问题本质是判断 Joe 能否在火到达之前到达边界。需要分别计算两个距离：

1. **Joe 的 BFS**（kind=0）：以 Joe 的起始位置为起点，计算 Joe 到达每个空地的最短时间 `d[r][c][0]`。
2. **火的 BFS**（kind=1）：以所有火的起始位置为起点，计算火蔓延到每个空地的最短时间 `d[r][c][1]`。

**判定Joe能否逃出**：遍历迷宫的四个边界。对于每个边界格子 `(r, c)`：
- 必须是空地（`.` 或在读入后被修改为空地的 `J`/`F` 位置）。
- Joe 必须能够到达该格子（`vis[r][c][0] == 1`）。
- Joe 到达的时间必须严格小于火到达的时间（`d[r][c][0] < d[r][c][1]`），或火无法到达该格子（`vis[r][c][1] == 0`）。

**注意事项**：Joe 的逃出时间 = `d[r][c][0] + 1`，因为到达边界格子后还需要一步逃出迷宫。

### 算法方法
- **双源 BFS（Breadth-First Search）**：两次 BFS 分别计算 Joe 和火的蔓延距离。所有边权为 1，使用标准队列 BFS。

### 复杂度分析
- **时间复杂度**：`O(T × R × C)`。每个格子对于每种 BFS 最多入队一次，每条边被考虑常数次。
- **空间复杂度**：`O(R × C)`。需要两个二维数组（分别存储 Joe 和火的距离/访问标记）。

```cpp
// 例题1  大火蔓延的迷宫（Fire!, UVa 11624）
// 解题思路：双源BFS——分别计算Joe和火到每个格子的最短时间
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<queue>
#include<algorithm>
using namespace std;

const int INF = 1000000000;
const int maxr = 1000 + 5;
const int maxc = 1000 + 5;
int R, C;
char maze[maxr][maxc];              // 存储迷宫

struct Cell {
  int r, c;
  Cell(int r, int c):r(r),c(c) {}
};

const int dr[] = {-1,1,0,0};        // 四个方向：上、下、左、右
const int dc[] = {0,0,-1,1};
int d[maxr][maxc][2], vis[maxr][maxc][2]; // d[][][0]:Joe的距离, d[][][1]:火的距离

queue<Cell> Q;
// kind=0: Joe的BFS; kind=1: 火的BFS
void bfs(int kind) {
  while(!Q.empty()) {
    Cell cell = Q.front(); Q.pop();
    int r = cell.r, c = cell.c;
    for(int dir = 0; dir < 4; dir++) {
      int nr = r + dr[dir], nc = c + dc[dir];
      // 检查边界、空地且未访问
      if(nr >= 0 && nr < R && nc >= 0 && nc < C && maze[nr][nc] == '.' && !vis[nr][nc][kind]) {
        Q.push(Cell(nr, nc));                         // 入队
        vis[nr][nc][kind] = 1;                         // 标记已访问
        d[nr][nc][kind] = d[r][c][kind] + 1;           // 距离+1
      }
    }
  }
}

int ans;
// 检查边界格子(r,c)：Joe能否在此处逃出
void check(int r, int c) {
  if(maze[r][c] != '.' || !vis[r][c][0]) return;     // 必须是Joe可达的边界格子
  if(!vis[r][c][1] || d[r][c][0] < d[r][c][1])        // Joe必须先于火到达（或火不到达）
    ans = min(ans, d[r][c][0] + 1);                    // 加1步逃出迷宫
}

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    scanf("%d%d", &R, &C);
    int jr, jc;
    vector<Cell> fires;                               // 存储所有火源的位置
    for(int i = 0; i < R; i++) {
      scanf("%s", maze[i]);
      for(int j = 0; j < C; j++)
        if(maze[i][j] == 'J') { jr = i; jc = j; maze[i][j] = '.'; }         // 记录Joe位置，改为空地
        else if(maze[i][j] == 'F') { fires.push_back(Cell(i,j)); maze[i][j] = '.'; } // 记录火源，改为空地
    }
    memset(vis, 0, sizeof(vis));

    // 第一轮 BFS: Joe 的距离
    vis[jr][jc][0] = 1; d[jr][jc][0] = 0;
    Q.push(Cell(jr, jc));
    bfs(0);

    // 第二轮 BFS: 所有火源同时作为起点
    for(int i = 0; i < fires.size(); i++) {
      vis[fires[i].r][fires[i].c][1] = 1;
      d[fires[i].r][fires[i].c][1] = 0;
      Q.push(fires[i]);
    }
    bfs(1);

    // 检查四个边界上的每一个格子
    ans = INF;
    for(int i = 0; i < R; i++) { check(i,0); check(i,C-1); }  // 左右边界
    for(int i = 0; i < C; i++) { check(0,i); check(R-1,i); }  // 上下边界
    if(ans == INF) printf("IMPOSSIBLE\n"); else printf("%d\n", ans);
  }
  return 0;
}
// 25878084	11624	Fire!	Accepted	C++	0.420	2020-12-23 08:00:22
```
