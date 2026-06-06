# 5.5 二分图匹配

## 例题25  固定分区内存管理（Fixed Partition Memory Management, World Finals 2001, LA 2238/UVa1006）

### 题目描述
一个计算机系统有 `m` 个固定大小的内存分区（region），需要运行 `n` 个程序。每个程序在不同的内存分区中运行时间不同（运行时间取决于分区的大小与程序需求）。程序在分区中按先后顺序执行（先到先运行，不能抢占），目标是调度这 `n` 个程序到这 `m` 个分区中，使得**平均回转时间**（程序从提交到完成的总时间）最小。输出最小平均回转时间及具体调度方案。

**输入格式**：多组数据。每组第一行 `m n`（m=0,n=0 结束），接下来 `m` 行分区大小，接下来 `n` 个程序的数据：每行 `k s1 t1 s2 t2 ...`（程序有 k 种不同的 size-time 配置）。**输出格式**：对每组数据，输出 `Case X`、平均回转时间和每个程序的具体运行计划。

### 解题思路
**二分图最大权匹配（KM 算法）**：将问题建模为二分图匹配：左边是 `n` 个程序，右边是 `m × n` 个"槽位"（每个分区的每个位置）。

**槽位含义**：`Y(r, pos)` 表示分区 r 中的第 pos 个位置（0-indexed）。如果程序 p 被分配到 Y(r, pos)，它将是分区的第 pos+1 个程序（倒数第 pos 个），其完成时间为 `(pos+1) * runtime[p][r]`。

**边权设计**：由于目标是**最小**化总完成时间，而 KM 是求**最大**权匹配。将边权取相反数：`W[p][r*n+pos] = -(pos+1) * runtime[p][r]`，然后运行 KM 求最大权匹配。

**虚拟程序**：左边有 `n × (m-1)` 个虚拟程序，它们到所有槽位的边权设为 1（表示这些槽位为空）。

### 算法方法
- **Kuhn-Munkres（KM）算法**：求二分图最大权完美匹配。基于顶标（label）和相等子图的匈牙利算法增广。

### 复杂度分析
- **时间复杂度**：`O((n*m)³)`。KM 算法 O(V³)，其中 V = n*m ≤ 500。
- **空间复杂度**：`O(V²)`。存储权值矩阵 W[V][V]。

```cpp
// 例题25  固定分区内存管理（Fixed Partition Memory Management, World Finals 2001, LA 2238/UVa1006）
// 解题思路：二分图最大权匹配(KM)——左边程序，右边(分区,位置)槽位，权值取负求最小完成时间
// Rujia Liu
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;

const int maxn = 500 + 5;  // 顶点的最大数目
const int INF = 1e9;

// 最大权匹配
struct KM {
  int n;                   // 左右顶点个数
  vector<int> G[maxn];     // 邻接表
  int W[maxn][maxn];       // 权值
  int Lx[maxn], Ly[maxn];  // 顶标
  int left[maxn];  // left[i]为右边第i个点的匹配点编号，-1表示不存在
  bool S[maxn], T[maxn];  // S[i]和T[i]为左/右第i个点是否已标记

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    memset(W, 0, sizeof(W));
  }

  void AddEdge(int u, int v, int w) { G[u].push_back(v), W[u][v] = w; }

  bool match(int u) {
    S[u] = true;
    for (int i = 0; i < G[u].size(); i++) {
      int v = G[u][i];
      if (Lx[u] + Ly[v] == W[u][v] && !T[v]) {
        T[v] = true;
        if (left[v] == -1 || match(left[v])) {
          left[v] = u;
          return true;
        }
      }
    }
    return false;
  }

  void update() {
    int a = INF;
    for (int u = 0; u < n; u++)
      if (S[u])
        for (int i = 0; i < G[u].size(); i++) {
          int v = G[u][i];
          if (!T[v]) a = min(a, Lx[u] + Ly[v] - W[u][v]);
        }
    for (int i = 0; i < n; i++) {
      if (S[i]) Lx[i] -= a;
      if (T[i]) Ly[i] += a;
    }
  }

  void solve() {
    for (int i = 0; i < n; i++) {
      Lx[i] = *max_element(W[i], W[i] + n), left[i] = -1, Ly[i] = 0;
    }
    for (int u = 0; u < n; u++) {
      for (;;) {
        for (int i = 0; i < n; i++) S[i] = T[i] = false;
        if (match(u))
          break;
        else
          update();
      }
    }
  }
};

KM solver;

const int maxp = 50 + 5;  // 程序(program)的最大数目
const int maxr = 10 + 5;  // 区域(region)的最大数目
int n, m;                 // 程序数目和区域数目
int runtime[maxp][maxr];  // runtime[p][r]为程序p在区域r中的运行时间

// 打印具体方案
void print_solution() {
  // 起始时刻、分配到得区域编号、总回转时间
  int start[maxp], region_number[maxp], total = 0;
  for (int r = 0; r < m; r++) {
    vector<int>
        programs;  // 本region执行的所有程序，按照逆序排列（“倒数”第pos个程序）
    for (int pos = 0; pos < n; pos++) {
      int right = r * n + pos, left = solver.left[right];
      if (left >= n) break;  // 匹配到虚拟结点，说明本region已经没有更多程序了
      programs.push_back(left), region_number[left] = r;
      total -= solver.W[left][right];  // 权值取过相反数
    }
    reverse(programs.begin(), programs.end());
    for (size_t i = 0, time = 0; i < programs.size(); i++)
      start[programs[i]] = time, time += runtime[programs[i]][r];
  }

  printf("Average turnaround time = %.2lf\n", (double)total / n);
  for (int p = 0; p < n; p++)
    printf("Program %d runs in region %d from %d to %d\n", p + 1,
           region_number[p] + 1, start[p],
           start[p] + runtime[p][region_number[p]]);
  printf("\n");
}

int main() {
  for (int kase = 1; scanf("%d%d", &m, &n) == 2 && m && n; kase++) {
    solver.init(m * n);
    int size[maxr];
    for (int r = 0; r < m; r++) scanf("%d", &size[r]);
    for (int p = 0; p < n; p++) {
      int s[10], t[10], k;
      scanf("%d", &k);
      for (int i = 0; i < k; i++) scanf("%d%d", &s[i], &t[i]);
      for (int r = 0; r < m; r++) {  // 计算程序p在内存区域r中的运行时间
        int& time = runtime[p][r];
        time = INF;
        if (size[r] < s[0]) continue;
        for (int i = 0; i < k; i++)
          if (i == k - 1 || size[r] < s[i + 1]) {
            time = t[i];
            break;
          }

        // 连边X(p) -> Y(r,pos)
        for (int pos = 0; pos < n; pos++)
          solver.AddEdge(p, r * n + pos,
                         -(pos + 1) * time);  // 本题要求最小值，权值要取相反数
      }
    }

    // 补完其他边
    for (int i = n; i < n * m; i++)
      for (int j = 0; j < n * m; j++) solver.AddEdge(i, j, 1);
    solver.solve();
    printf("Case %d\n", kase);
    print_solution();
  }
  return 0;
}
// Accepted 940ms 3795 C++5.3.0 2020-12-1418:34:10 25846819
```

## 例题29  出租车（Taxi Cab Scheme, NWERC 2004, LA 3126/POJ2060）

### 题目描述
一个出租车公司接到 `n` 个订单。每个订单包含：出发时间（HH:MM）、出发坐标、目的坐标。出租车每完成一个订单后，可以立即去接下一个人（如果能按时赶到：到达时间必须严格早于下一个订单的出发时间）。求最少需要多少辆出租车才能完成所有订单。`n ≤ 500`。

**输入格式**：第一行为测试数据组数 `T`。每组数据第一行 `n`，接下来 `n` 行每行 `HH:MM x1 y1 x2 y2`。**输出格式**：对每组数据输出最少出租车数量。

### 解题思路
**DAG 最小路径覆盖**：将每个订单看作一个结点。订单 i 完成后可以去接订单 j 当且仅当：`T2[i] + dist(i的终点, j的起点) < T1[j]`（至少提前 1 分钟）。满足条件的 i→j 连一条有向边。

问题转化为：在有向无环图（DAG）中求**最小路径覆盖**（用最少的路径覆盖所有顶点）。

**定理**：DAG 的最小路径覆盖 = n - 最大匹配数（在对应的二分图中）。二分图构造：左边有 n 个点（出发），右边有 n 个点（到达）。如果原 DAG 中存在边 i→j，则在二分图中添加边 i(左)→j(右)。最大匹配的每一对表示"订单 i 之后接着做订单 j"，每对匹配节省一辆出租车。

**答案**：`n - max_matching`。

### 算法方法
- **DAG 最小路径覆盖**：转化为二分图最大匹配问题。
- **匈牙利算法（Hungarian Algorithm）**：求二分图最大基数匹配。

### 复杂度分析
- **时间复杂度**：`O(T × n³)`。匈牙利算法 O(V × E)，邻接矩阵实现 O(n³)。
- **空间复杂度**：`O(n²)`。

```cpp
// 例题29  出租车（Taxi Cab Scheme, NWERC 2004, LA 3126/POJ2060）
// 解题思路：DAG最小路径覆盖→二分图最大匹配——i→j可达则连边，最小出租车数=n-最大匹配
// 陈锋
// 陈锋
#include <cstdio>
#include <cstring>
#include <vector>
#include <algorithm>
using namespace std;

const int maxn = 500 + 5;  // 单侧顶点的最大数目

// 二分图最大基数匹配，邻接矩阵写法
struct BPM {
  int n, m;           // 左右顶点个数
  int G[maxn][maxn];  // 邻接表
  int left[maxn];  // left[i]为右边第i个点的匹配点编号，-1表示不存在
  bool T[maxn];  // T[i]为右边第i个点是否已标记

  void init(int n, int m) {
    this->n = n, this->m = m;
    memset(G, 0, sizeof(G));
  }

  bool match(int u) {
    for (int v = 0; v < m; v++)
      if (G[u][v] && !T[v]) {
        T[v] = true;
        if (left[v] == -1 || match(left[v])) {
          left[v] = u;
          return true;
        }
      }
    return false;
  }

  // 求最大匹配
  int solve() {
    fill_n(left, m + 1, -1);
    int ans = 0;
    for (int u = 0; u < n; u++) {  // 从左边结点u开始增广
      fill_n(T, m + 1, false);
      if (match(u)) ans++;
    }
    return ans;
  }
};

BPM solver;
int X1[maxn], Y1[maxn], X2[maxn], Y2[maxn], T1[maxn], T2[maxn];
inline int dist(int a, int b, int c, int d) { return abs(a - c) + abs(b - d); }

int main() {
  int T;
  scanf("%d", &T);
  for (int t = 0, n; t < T; t++) {
    scanf("%d", &n);
    for (int i = 0, h, m; i < n; i++) {
      scanf("%d:%d%d%d%d%d", &h, &m, &X1[i], &Y1[i], &X2[i], &Y2[i]);
      T1[i] = h * 60 + m, T2[i] = T1[i] + dist(X1[i], Y1[i], X2[i], Y2[i]);
    }
    solver.init(n, n);
    for (int i = 0; i < n; i++)
      for (int j = i + 1; j < n; j++)
        if (T2[i] + dist(X2[i], Y2[i], X1[j], Y1[j]) < T1[j])
          solver.G[i][j] = 1;  // 至少要提前1分钟到达
    printf("%d\n", n - solver.solve());
  }
  return 0;
}
// Accepted 188ms 1332kB 1704 G++2020-12-14 18:19:37 22209579
```

## 例题28  保守的老师（Guardian of Decency, NWERC 2005, LA 3415/POJ2771）

### 题目描述
一位保守的老师要带学生出游，但有些男女学生不能分在同一个房间。具体规则：男女学生不能分到同一房间如果满足：身高差 ≤ 40 cm、喜欢相同的音乐、喜欢不同的运动。老师希望挑选尽可能多的学生出游，且这些人中任何一男一女之间都不能有"冲突"。问最多能带多少学生。`n ≤ 500`。

**输入格式**：第一行为测试数据组数 `T`。每组数据第一行 `n`，接下来 `n` 行每行 `height gender music sport`。**输出格式**：对每组数据输出最多能带的学生数量。

### 解题思路
**二分图最大独立集**：由于冲突规则只涉及一男一女（同性之间无限制），原问题可建模为二分图问题。

**建模**：将所有男生放在左边，所有女生放在右边。如果男生 i 和女生 j 之间存在冲突（满足身高差 ≤ 40、同音乐、不同运动），则连边。

**最大独立集定理**：在二分图中，最大独立集 = 顶点总数 - 最大匹配。

**答案**：`male_count + female_count - max_matching`。

### 算法方法
- **匈牙利算法（Hungarian Algorithm）**：求二分图最大基数匹配。
- **二分图最大独立集**：`|V| - 最大匹配`。

### 复杂度分析
- **时间复杂度**：`O(T × n³)`。匈牙利算法 O(V × E)，邻接矩阵 O(n³)。
- **空间复杂度**：`O(n²)`。

```cpp
// 例题28  保守的老师（Guardian of Decency, NWERC 2005, LA 3415/POJ2771）
// 解题思路：二分图最大独立集——男生→女生冲突边，最大独立集=总人数-最大匹配
// 陈锋
// 陈锋
#include <cstdio>
#include <cstring>
#include <vector>
#include <algorithm>
using namespace std;

const int maxn = 500 + 5; // 单侧顶点的最大数目

// 二分图最大基数匹配，邻接矩阵写法
struct BPM {
  int n, m;               // 左右顶点个数
  int G[maxn][maxn];      // 邻接表
  int left[maxn];         // left[i]为右边第i个点的匹配点编号，-1表示不存在
  bool T[maxn];           // T[i]为右边第i个点是否已标记

  void init(int n, int m) {
    this->n = n, this->m = m;
    memset(G, 0, sizeof(G));
  }

  bool match(int u) {
    for (int v = 0; v < m; v++) if (G[u][v] && !T[v]) {
        T[v] = true;
        if (left[v] == -1 || match(left[v])) {
          left[v] = u;
          return true;
        }
      }
    return false;
  }

  // 求最大匹配
  int solve() {
    int ans = 0;
    fill_n(left, m + 1, -1);
    for (int u = 0; u < n; u++) { // 从左边结点u开始增广
      fill_n(T, m + 1, false);
      if (match(u)) ans++;
    }
    return ans;
  }
};

BPM solver;

#include<iostream>
#include<string>
struct Student {
  int h;
  string music, sport;
  Student(int h = 0, const string& music = "", const string& sport = "")
    : h(h), music(music), sport(sport) {}
};

bool conflict(const Student& a, const Student& b) {
  return abs(a.h - b.h) <= 40 && a.music == b.music && a.sport != b.sport;
}

int main() {
  int T; cin >> T;
  for (int t = 0, n; cin >> n, t < T; t++) {
    vector<Student> male, female;
    Student s;
    for (int i = 0; i < n; i++) {
      string gender;
      cin >> s.h >> gender >> s.music >> s.sport;
      if (gender[0] == 'M') male.push_back(s);
      else female.push_back(s);
    }
    int x = male.size(), y = female.size();
    solver.init(x, y);
    for (int i = 0; i < x; i++)
      for (int j = 0; j < y; j++)
        if (conflict(male[i], female[j])) solver.G[i][j] = 1;
    printf("%d\n", x + y - solver.solve());
  }
  return 0;
}
// Accepted 1641ms 1728kB 1908 G++ 2020-12-14 18:16:47 22209571
```

## 例题26  女士的选择（Ladies' Choice, SWERC 2007, LA3989/UVa1175）

### 题目描述
有 `n` 个单身男士和 `n` 个单身女士。每个男士对所有女士有一个严格的偏好排名；每个女士对所有男士也有一个严格的偏好排名。要通过婚姻匹配算法（Gale-Shapley）找到一组稳定的婚姻匹配。"稳定"意味着不存在这样一对男女：他们彼此喜欢对方超过自己当前的配偶。求男士最优的稳定匹配方案。`n ≤ 1000`。

**输入格式**：第一行为测试数据组数 `T`。每组数据第一行 `n`，接下来 `n` 行（男士的偏好列表），接下来 `n` 行（女士的偏好列表）。**输出格式**：对每个男士输出他的妻子编号。

### 解题思路
**Gale-Shapley 稳定婚姻算法**：
1. 初始化：所有男士未订婚。
2. 重复：选择一个未订婚的男士 `m`，他向自己的偏好列表中还没被拒绝过的排名最高的女士 `w` 求婚。
   - 如果 `w` 还没有未婚夫，则 `m` 和 `w` 订婚。
   - 如果 `w` 已有未婚夫 `m'`，比较 `m` 和 `m'` 在 `w` 心中的排名。如果 `w` 更喜欢 `m`，则抛弃 `m'`（`m'` 重新进入未订婚队列），与 `m` 订婚；否则拒绝 `m`（`m` 继续向下一个偏好求婚）。
3. 直到所有男士都订婚。

**时间复杂度**：每个男士最多向 n 个女士求婚，总求婚次数 O(n²)。

### 算法方法
- **Gale-Shapley 稳定婚姻算法（Stable Marriage Problem）**：男士主动求婚的版本，产生男士最优的稳定匹配。

### 复杂度分析
- **时间复杂度**：`O(T × n²)`。总求婚次数最多 n²。
- **空间复杂度**：`O(n²)`。存储偏好排名矩阵。

```cpp
// 例题26  女士的选择（Ladies' Choice, SWERC 2007, LA3989/UVa1175）
// 解题思路：Gale-Shapley稳定婚姻算法——男士最优匹配，男士按偏好求婚，女士择优选择
// Rujia Liu
#include<cstdio>
#include<queue>
using namespace std;

const int maxn = 1000 + 10;
int pref[maxn][maxn], order[maxn][maxn], nxt[maxn], future_husband[maxn], future_wife[maxn];
queue<int> q; // 未订婚的男士队列

void engage(int man, int woman) {
  int m = future_husband[woman];
  if(m) {
    future_wife[m] = 0; // 抛弃现任未婚夫（如果有的话）
    q.push(m); // 加入未订婚男士队列
  }
  future_wife[man] = woman;
  future_husband[woman] = man;
}

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    int n;
    scanf("%d", &n);

    for(int i = 1; i <= n; i++) {
      for(int j = 1; j <= n; j++)
        scanf("%d", &pref[i][j]); // 编号为i的男士第j喜欢的人
      nxt[i] = 1; // 接下来应向排名为1的女士求婚
      future_wife[i] = 0; // 没有未婚妻
      q.push(i);
    }

    for(int i = 1; i <= n; i++) {
      for(int j = 1; j <= n; j++) {
        int x;
        scanf("%d", &x);
        order[i][x] = j; // 在编号为i的女士心目中，编号为x的男士的排名
      }
      future_husband[i] = 0; // 没有未婚夫
    }

    while(!q.empty()) {
      int man = q.front(); q.pop();
      int woman = pref[man][nxt[man]++];
      if(!future_husband[woman]) engage(man, woman); // woman没有未婚夫，直接订婚
      else if(order[woman][man] < order[woman][future_husband[woman]]) engage(man, woman); // 换未婚夫
      else q.push(man); // 下次再来
    }
    while(!q.empty()) q.pop();

    for(int i = 1; i <= n; i++) printf("%d\n", future_wife[i]);
    if(T) printf("\n");
  }
  return 0;
}
// 25878224	1175	Ladies' Choice	Accepted	C++	0.190	2020-12-23 08:37:23
```

## 例题23  蚂蚁（Ants, NEERC 2008, LA 4043/POJ3565）

### 题目描述
平面上有 `n` 个白点（蚂蚁窝）和 `n` 个黑点（苹果树），所有点互不重合且不存在三点共线。现在要建立 `n` 条线段，每条线段连接一个白点和一个黑点，使得所有线段互不相交。求一种匹配方案。`n ≤ 100`。

**输入格式**：第一行为 `n`，接下来 `n` 行白点坐标，再 `n` 行黑点坐标。**输出格式**：对每个白点输出它所连接的黑点编号。

### 解题思路
**KM 算法求最小权完美匹配**：线段不相交的充要条件是匹配的权值（欧几里得距离之和）最小。

**证明思路**：如果有两条线段相交，交换端点后总长度一定减小（三角不等式）。因此，总长度最小的匹配必然无边相交。

**KM 实现**：
- 左边 n 个白点，右边 n 个黑点。
- 边权 W[i][j] = -dist(白点i, 黑点j)（取负号将最小权匹配转为最大权匹配）。
- 运行 KM 算法求最大权完美匹配，输出匹配结果。

### 算法方法
- **Kuhn-Munkres（KM）算法**：求二分图最大权完美匹配，通过取负将最小匹配转为最大匹配。

### 复杂度分析
- **时间复杂度**：`O(n³)`。KM 算法 O(V³)，n ≤ 100。
- **空间复杂度**：`O(n²)`。

```cpp
// 例题23  蚂蚁（Ants, NEERC 2008, LA 4043/POJ3565）
// 解题思路：KM求最小权完美匹配——总距离最小的匹配必有不相交性质，边权取负转化为最大权匹配
// 陈锋
// 陈锋
#include <cstdio>
#include <cstring>
#include <cmath>
#include <algorithm>
#include <cassert>
using namespace std;

const double INF = 1e30;
template<size_t SZ>
struct KM {
  double W[SZ][SZ]; // 权值
  double Lx[SZ], Ly[SZ];   // 顶标
  int n, left[SZ];          // left[i]为右边第i个点的匹配点编号
  bool S[SZ], T[SZ];   // S[i]和T[i]为左/右第i个点是否已标记

  bool eq(double a, double b) { return fabs(a - b) < 1e-9; }

  void init(size_t _n) {
    assert(_n < SZ);
    this->n = _n;
  }

  bool match(int i) {
    S[i] = true;
    for (int j = 1; j <= n; j++) if (eq(Lx[i] + Ly[j], W[i][j]) && !T[j]) {
        T[j] = true;
        if (!left[j] || match(left[j])) {
          left[j] = i;
          return true;
        }
      }
    return false;
  }

  void update() {
    double a = INF;
    for (int i = 1; i <= n; i++) if (S[i])
        for (int j = 1; j <= n; j++) if (!T[j])
            a = min(a, Lx[i] + Ly[j] - W[i][j]);
    for (int i = 1; i <= n; i++) {
      if (S[i]) Lx[i] -= a;
      if (T[i]) Ly[i] += a;
    }
  }

  void solve() {
    for (int i = 1; i <= n; i++) {
      left[i] = Lx[i] = Ly[i] = 0;
      for (int j = 1; j <= n; j++)
        Lx[i] = max(Lx[i], W[i][j]);
    }
    for (int i = 1; i <= n; i++) {
      for (;;) {
        for (int j = 1; j <= n; j++) S[j] = T[j] = 0;
        if (match(i)) break; else update();
      }
    }
  }
};

const int NN = 100 + 10;
KM<NN> solver;
int main() {
  for (int kase = 1, n; scanf("%d", &n) == 1; kase++) {
    if (kase > 1) printf("\n");
    solver.init(n);
    int x1[NN], y1[NN], x2[NN], y2[NN];
    for (int i = 1; i <= n; i++)
      scanf("%d%d", &x1[i], &y1[i]);
    for (int i = 1; i <= n; i++)
      scanf("%d%d", &x2[i], &y2[i]);
    for (int i = 1; i <= n; i++) // ant colony
      for (int j = 1; j <= n; j++) // apple tree
        solver.W[j][i] = -sqrt((double)(x1[i] - x2[j]) * (x1[i] - x2[j]) + (double)(y1[i] - y2[j]) * (y1[i] - y2[j]));
    solver.solve(); // 最大权匹配
    for (int i = 1; i <= n; i++) printf("%d\n", solver.left[i]);
  }
  return 0;
}
// Accepted 113ms 2066 C++11 5.3.02020-02-0212:09:15
```

## 例题24  少林决胜（Golden Tiger Claw, UVa 11383）

### 题目描述
给定一个 `n × n` 的权值矩阵 `W[i][j]`。定义“金虎爪”为：选择 n 个行标号 `row[i]` 和 n 个列标号 `col[j]`，满足 `row[i] + col[j] ≥ W[i][j]`（对所有 i, j）。求使得 `Σ row[i] + Σ col[j]` 最小的金虎爪方案。`n ≤ 500`。

**输入格式**：多组数据，每组第一行 `n`，接下来 `n × n` 个整数（矩阵 W）。**输出格式**：输出最小行标和、各行标号、各列标号、总最小值。

### 解题思路
**KM 算法定理的直接应用**：KM 算法求解二分图最大权匹配时会生成一组顶标 `Lx[i]` 和 `Ly[j]`，满足：
- `Lx[i] + Ly[j] ≥ W[i][j]`（对所有 i, j）
- 存在一组完美匹配使得 `Lx[i] + Ly[j] = W[i][j]`（对匹配中的边）
- `Σ Lx[i] + Σ Ly[j]` 是所有可行顶标方案中最小的。

这正是题目要求的金虎爪！直接运行 KM 算法，输出 `Lx` 和 `Ly` 即可。

**KM 顶标含义**：`Lx[i]` 初始化为 `max(W[i][j])`，`Ly[j]` 初始化为 0。在增广过程中通过 `update()` 调整顶标，最终得到的就是最优解。

### 算法方法
- **Kuhn-Munkres（KM）算法**：求解二分图最大权匹配，同时输出最优顶标。

### 复杂度分析
- **时间复杂度**：`O(n³)`。KM 算法 O(V³)，n ≤ 500。
- **空间复杂度**：`O(n²)`。

```cpp
// 例题24  少林决胜（Golden Tiger Claw, UVa 11383）
// 解题思路：KM定理的直接应用——KM的最优顶标Lx、Ly满足金虎爪条件且和最小
// 陈锋
// 陈锋
#include <bits/stdc++.h>
using namespace std;

const int INF = 1e9;
template<size_t SZ>
struct KM {
  int n;                  // 左右顶点个数
  vector<int> G[SZ];    // 邻接表
  int W[SZ][SZ];      // 权值
  int Lx[SZ], Ly[SZ]; // 顶标
  int left[SZ];         // left[i]为右边第i个点的匹配点编号，-1表示不存在
  bool S[SZ], T[SZ];  // S[i]和T[i]为左/右第i个点是否已标记

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    memset(W, 0, sizeof(W));
  }

  void AddEdge(int u, int v, int w) {
    G[u].push_back(v), W[u][v] = w;
  }

  bool match(int u) {
    S[u] = true;
    for (size_t i = 0; i < G[u].size(); i++) {
      int v = G[u][i];
      if (Lx[u] + Ly[v] == W[u][v] && !T[v]) {
        T[v] = true;
        if (left[v] == -1 || match(left[v])) {
          left[v] = u;
          return true;
        }
      }
    }
    return false;
  }

  void update() {
    int a = INF;
    for (int u = 0; u < n; u++) if (S[u])
        for (size_t i = 0; i < G[u].size(); i++) {
          int v = G[u][i];
          if (!T[v]) a = min(a, Lx[u] + Ly[v] - W[u][v]);
        }
    for (int i = 0; i < n; i++) {
      if (S[i]) Lx[i] -= a;
      if (T[i]) Ly[i] += a;
    }
  }

  void solve() {
    for (int i = 0; i < n; i++) {
      Lx[i] = *max_element(W[i], W[i] + n);
      left[i] = -1;
      Ly[i] = 0;
    }
    for (int u = 0; u < n; u++) {
      for (;;) {
        for (int i = 0; i < n; i++) S[i] = T[i] = false;
        if (match(u)) break; else update();
      }
    }
  }
};

const int maxn = 500 + 5; // 顶点的最大数目
KM<maxn> km;
int main() {
  for (int n, w; scanf("%d", &n) == 1; ) {
    km.init(n);
    for (int i = 0; i < n; i++)
      for (int j = 0; j < n; j++)
        scanf("%d", &w), km.AddEdge(i, j, w);
    km.solve();
    int sum = 0;
    for (int i = 0; i < n - 1; i++) printf("%d ", km.Lx[i]), sum += km.Lx[i];
    printf("%d\n", km.Lx[n - 1]);
    for (int i = 0; i < n - 1; i++) printf("%d ", km.Ly[i]), sum += km.Ly[i];
    printf("%d\n", km.Ly[n - 1]);
    printf("%d\n", sum + km.Lx[n - 1] + km.Ly[n - 1]);
  }
  return 0;
}
// Accepted 80ms 2072 C++11 5.3.02020-02-02 12:23:15
```

## 例题27  我是SAM（SAM I AM, UVa 11419）

### 题目描述
在一个 `R × C` 的网格中，有一些格子中有敌人。SAM 的大炮可以发射炮弹，一发炮弹可以消灭一整行或一整列上的所有敌人。求最少需要发射多少发炮弹才能消灭所有敌人，并输出具体方案（哪些行和哪些列需要开炮）。`R, C ≤ 1000`。

**输入格式**：多组数据。每组第一行 `R C N`（N 个敌人），接下来 `N` 行 `r c`。`R=C=N=0` 时结束。**输出格式**：对每组数据，第一行输出最少炮弹数，然后依次输出需要开炮的行和列。

### 解题思路
**二分图最小顶点覆盖**：将每行作为左边结点、每列作为右边结点。每个敌人 `(r, c)` 对应一条边 `r(左)→c(右)`。消灭所有敌人等价于用最少的顶点覆盖所有边——即 **最小顶点覆盖（Minimum Vertex Cover）**。

**König 定理**：在二分图中，最小顶点覆盖数 = 最大匹配数。

**方案构造**（最小覆盖集）：
1. 先求最大匹配，标记所有匹配边。
2. 从所有左侧未盖点出发，在交错图中遍历（沿着非匹配边→匹配边交替走）。
3. 最小覆盖集 = 左侧未标记的顶点 + 右侧已标记的顶点。

### 算法方法
- **匈牙利算法（Hungarian Algorithm）**：求二分图最大匹配。
- **König 定理**：从最大匹配构造最小顶点覆盖。

### 复杂度分析
- **时间复杂度**：`O(R × C)`。匈牙利算法 O(V × E)，邻接表实现。
- **空间复杂度**：`O(R + C + N)`。

```cpp
// 例题27  我是SAM（SAM I AM, UVa 11419）
// 解题思路：二分图最小顶点覆盖=最大匹配(König定理)——行→左，列→右，敌人=边
// 陈锋
// 陈锋
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;

const int maxn = 1000 + 5;  // 单侧顶点的最大数目

// 二分图最大基数匹配
struct BPM {
  int n, m;             // 左右顶点个数
  vector<int> G[maxn];  // 邻接表
  int left[maxn];  // left[i]为右边第i个点的匹配点编号，-1表示不存在
  bool T[maxn];  // T[i]为右边第i个点是否已标记

  int right[maxn];  // 求最小覆盖用
  bool S[maxn];     // 求最小覆盖用

  void init(int n, int m) {
    this->n = n, this->m = m;
    for (int i = 0; i < n; i++) G[i].clear();
  }

  void AddEdge(int u, int v) { G[u].push_back(v); }

  bool match(int u) {
    S[u] = true;
    for (size_t i = 0; i < G[u].size(); i++) {
      int v = G[u][i];
      if (!T[v]) {
        T[v] = true;
        if (left[v] == -1 || match(left[v])) {
          left[v] = u, right[u] = v;
          return true;
        }
      }
    }
    return false;
  }

  // 求最大匹配
  int solve() {
    fill_n(left, m + 1, -1), fill_n(right, n + 1, -1);
    int ans = 0;
    for (int u = 0; u < n; u++) {  // 从左边结点u开始增广
      fill_n(S, n + 1, false), fill_n(T, m + 1, false);
      if (match(u)) ans++;
    }
    return ans;
  }

  // 求最小覆盖。X和Y为最小覆盖中的点集
  int mincover(vector<int>& X, vector<int>& Y) {
    int ans = solve();
    fill_n(S, n + 1, false), fill_n(T, m + 1, false);
    for (int u = 0; u < n; u++) if (right[u] == -1) match(u); // 从所有X未盖点出发增广
    for (int u = 0; u < n; u++) if (!S[u]) X.push_back(u); // X中的未标记点
    for (int v = 0; v < m; v++) if (T[v]) Y.push_back(v); // Y中的已标记点
    return ans;
  }
};

BPM solver;
int main() {
  for (int R, C, N; scanf("%d%d%d", &R, &C, &N) == 3 && R && C && N;) {
    solver.init(R, C);
    for (int i = 0, r, c; i < N; i++)
      scanf("%d%d", &r, &c), r--, c--, solver.AddEdge(r, c);
    vector<int> X, Y;
    int ans = solver.mincover(X, Y);
    printf("%d", ans);
    for (size_t i = 0; i < X.size(); i++) printf(" r%d", X[i] + 1);
    for (size_t i = 0; i < Y.size(); i++) printf(" c%d", Y[i] + 1);
    printf("\n");
  }
  return 0;
}
// Accepted 20ms 2047 C++5.3.0 2020-12-14 18:14:53 25846729
```
