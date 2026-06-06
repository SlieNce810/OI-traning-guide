# 4.3 二维几何常用算法

## 例题14  找边界（Find the Border, NEERC 2004, Codeforces Gym100536F）

### 题目描述
给定平面上一个简单多边形（可能自交），多边形的各边之间可能相交。多边形上的交点将各边分割成小线段。要求找出这个折线图形的外边界——即多边形加上内部所有边之后，所围成区域的最大外轮廓。

**输入格式**：输入包含多组测试数据，以n=0结束。每组第一行包含整数n（3 ≤ n ≤ 100），表示多边形顶点数。接下来n行，每行两个整数x y（-10000 ≤ x, y ≤ 10000），表示多边形顶点坐标。顶点按顺序给出，相邻顶点之间有一条线段，最后一个顶点与第一个顶点之间也有一条线段。

**输出格式**：对于每组测试数据，第一行输出边界多边形的顶点数m，接下来m行按逆时针顺序输出边界多边形的顶点坐标，每行x y，保留4位小数。顶点从最左下角的点开始输出。

### 解题思路
问题实质是找出包含所有线段后的"外轮廓"。可以使用**平面直线图（PSLG）**来系统处理：

1. **构建PSLG**：将所有线段求交点，将原始线段分割为更小的边。每个交点作为一个顶点，每小段作为一条边。这构成了平面的一个细分（subdivision）。

2. **找出所有面**：在PSLG中，以每条边为起点，按照特定的转向规则（总是选择"最右转"的边）遍历，可以找出所有的面。每个面对应一个封闭的多边形。

3. **识别无限面**：对于无界的面（即外轮廓），其有向面积为负（因为按逆时针遍历时面积为正，而无限面边界是顺时针的）。取面积最小的面（即最大的负面积），反转其方向得到外轮廓。

4. **简化边界**：去除边界上三点共线的中间点。

### 算法方法
- **PSLG数据结构**：存储所有顶点坐标、有向边及其极角、邻接表（每个顶点出发的边按极角排序）。
- **边排序**：从每个顶点出发的所有边按极角排序，使prev[e]指向顺时针旋转遇到的下一条边。
- **面遍历**：从未访问的边出发，每次选择prev[e^1]（e的反向边的前一条边，即逆时针旋转），直到回到起点，形成一个面。
- **点去重**：使用sort+unique处理接近重合的点，注意需要使用特殊的小于运算符。

### 复杂度分析
- **时间复杂度**：O(N³)。N ≤ 100，交点最多O(N²)个。构建交点需要O(N²)时间，对每条线段由交点产生的子段O(N²)条，每条边排序O(N² log N²)。面遍历O(E)。
- **空间复杂度**：O(N²)，存储顶点和边。

```cpp
// 例题14  找边界（Find the Border, NEERC 2004, Codeforces Gym100536F）
// 刘汝佳
// 注意：本题可以直接使用“卷包裹”法求出外轮廓。本程序只是为了演示PSLG的实现
#include <vector>
#include <cassert>
#include <cmath>
#include <cstring>
#include <cstdio>
#include <algorithm>

using namespace std;

const double eps = 1e-8;
double dcmp(double x) {
  if (fabs(x) < eps) return 0;
  return x < 0 ? -1 : 1;
}

struct Point {
  double x, y;
  Point(double x = 0, double y = 0): x(x), y(y) { }
};

typedef Point Vector;
Vector operator + (const Vector& A, const Vector& B) 
{ return Vector(A.x + B.x, A.y + B.y); }
Vector operator - (const Point& A, const Point& B) 
{ return Vector(A.x - B.x, A.y - B.y); }
Vector operator * (const Vector& A, double p) 
{ return Vector(A.x * p, A.y * p); }

// 理论上这个“小于”运算符是错的，因为可能有三个点a, b, c, a和b很接近（即a<b好b<a都不成立），
// b和c很接近，但a和c不接近
// 所以使用这种“小于”运算符的前提是能排除上述情况
bool operator < (const Point& a, const Point& b)
{ return dcmp(a.x - b.x) < 0 || (dcmp(a.x - b.x) == 0 && dcmp(a.y - b.y) < 0); }
bool operator == (const Point& a, const Point &b)
{ return dcmp(a.x - b.x) == 0 && dcmp(a.y - b.y) == 0;}

double Dot(const Vector& A, const Vector& B) { return A.x * B.x + A.y * B.y; }
double Cross(const Vector& A, const Vector& B) { return A.x * B.y - A.y * B.x; }
double Length(const Vector& A) { return sqrt(Dot(A, A)); }
typedef vector<Point> Polygon;

Point GetLineIntersection(const Point& P, const Vector& v, const Point& Q, const Vector& w) {
  Vector u = P - Q;
  double t = Cross(w, u) / Cross(v, w);
  return P + v * t;
}

bool SegmentProperIntersection(const Point& a1, const Point& a2, 
  const Point& b1, const Point& b2) {
  double c1 = Cross(a2 - a1, b1 - a1), c2 = Cross(a2 - a1, b2 - a1),
         c3 = Cross(b2 - b1, a1 - b1), c4 = Cross(b2 - b1, a2 - b1);
  return dcmp(c1) * dcmp(c2) < 0 && dcmp(c3) * dcmp(c4) < 0;
}

bool OnSegment(const Point& p, const Point& a1, const Point& a2) {
  return dcmp(Cross(a1 - p, a2 - p)) == 0 && dcmp(Dot(a1 - p, a2 - p)) < 0;
}

// 多边形的有向面积
double PolygonArea(const Polygon& poly) {
  double area = 0;
  int n = poly.size();
  for (int i = 1; i < n - 1; i++)
    area += Cross(poly[i] - poly[0], poly[(i + 1) % n] - poly[0]);
  return area / 2;
}

struct Edge {
  int from, to; // 起点，终点，左边的面编号
  double ang;
};

const int maxn = 10000 + 10; // 最大边数

// 平面直线图（PSLG）实现
struct PSLG {
  int n, m, face_cnt;          // 顶点数、边数、面数
  double x[maxn], y[maxn];     // 顶点坐标
  vector<Edge> edges;          // 所有有向边
  vector<int> G[maxn];         // 邻接表：从每个顶点出发的边编号
  int vis[maxn * 2];           // 每条边是否已经访问过（用于面遍历）
  int left[maxn * 2];          // 每条边左侧的面编号
  int prev[maxn * 2];          // 从同一起点出发的、顺时针旋转碰到的下一条边

  vector<Polygon> faces;       // 所有面的多边形
  double area[maxn];           // 每个面的面积

  void init(int n) {           // 初始化
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    edges.clear();
    faces.clear();
  }

  double getAngle(int from, int to) {  // 边from->to的极角
    return atan2(y[to] - y[from], x[to] - x[from]);
  }

  void AddEdge(int from, int to) {    // 添加无向边（实际添加两条有向边）
    edges.push_back((Edge) {from, to, getAngle(from, to)});  // 正向边
    edges.push_back((Edge) {to, from, getAngle(to, from)});  // 反向边
    m = edges.size();
    G[from].push_back(m - 2);         // 正向边编号
    G[to].push_back(m - 1);           // 反向边编号
  }

  void Build() {  // 构建面
    // 每个顶点出发的边按极角排序，建立顺时针旋转关系
    for (int u = 0; u < n; u++) {
      int d = G[u].size();
      for (int i = 0; i < d; i++)      // 冒泡排序（简单情况足够）
        for (int j = i + 1; j < d; j++)
          if (edges[G[u][i]].ang > edges[G[u][j]].ang) swap(G[u][i], G[u][j]);
      for (int i = 0; i < d; i++)       // prev[下一条边] = 当前边
        prev[G[u][(i + 1) % d]] = G[u][i];
    }

    memset(vis, 0, sizeof(vis));
    face_cnt = 0;
    for (int u = 0; u < n; u++)
      for (int i = 0; i < G[u].size(); i++) {
        int e = G[u][i];
        if (!vis[e]) {  // 逆时针找圈：每次走 prev[e^1]（从反向边出发的顺时针下一条）
          face_cnt++;
          Polygon poly;
          for (;;) {
            vis[e] = 1; left[e] = face_cnt;    // 标记边已访问
            int from = edges[e].from;
            poly.push_back(Point(x[from], y[from]));
            e = prev[e ^ 1];                    // e^1 是反向边编号
            if (e == G[u][i]) break;
            assert(vis[e] == 0);
          }
          faces.push_back(poly);
        }
      }

    for (int i = 0; i < faces.size(); i++)
      area[i] = PolygonArea(faces[i]);
  }
};

PSLG g;
const int maxp = 100 + 5;
int n, c;
Point P[maxp], V[maxp * (maxp - 1) / 2 + maxp];
// 在V数组里找到点p
int ID(const Point& p) { return lower_bound(V, V + c, p) - V; }

// 假定poly没有相邻点重合的情况，只需要删除三点共线的情况
Polygon simplify(const Polygon& poly) {
  Polygon ans;
  int n = poly.size();
  for (int i = 0; i < n; i++) {
    Point a = poly[i];
    Point b = poly[(i + 1) % n];
    Point c = poly[(i + 2) % n];
    if (dcmp(Cross(a - b, c - b)) != 0) ans.push_back(b);
  }
  return ans;
}

void build_graph() {
  c = n;
  for (int i = 0; i < n; i++)
    V[i] = P[i];

  vector<double> dist[maxp]; // dist[i][j]是第i条线段上的第j个点离起点（P[i]）的距离
  for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)
      if (SegmentProperIntersection(P[i], P[(i + 1) % n], P[j], P[(j + 1) % n])) {
        Point p = GetLineIntersection(P[i], P[(i + 1) % n] - P[i], P[j], P[(j + 1) % n] - P[j]);
        V[c++] = p;
        dist[i].push_back(Length(p - P[i]));
        dist[j].push_back(Length(p - P[j]));
      }

  // 为了保证“很接近的点”被看作同一个，这里使用了sort+unique的方法
  // 必须使用前面提到的“理论上是错误”的小于运算符，否则不能保证“很接近的点”在排序后连续排列
  // 另一个常见的处理方式是把坐标扩大很多倍（比如100000倍），然后四舍五入变成整点（计算完毕后再还原），用少许的精度损失换来鲁棒性和速度。
  sort(V, V + c);
  c = unique(V, V + c) - V;

  g.init(c); // c是平面图的点数
  for (int i = 0; i < c; i++) {
    g.x[i] = V[i].x;
    g.y[i] = V[i].y;
  }
  for (int i = 0; i < n; i++) {
    Vector v = P[(i + 1) % n] - P[i];
    double len = Length(v);
    dist[i].push_back(0);
    dist[i].push_back(len);
    sort(dist[i].begin(), dist[i].end());
    int sz = dist[i].size();
    for (int j = 1; j < sz; j++) {
      Point a = P[i] + v * (dist[i][j - 1] / len);
      Point b = P[i] + v * (dist[i][j] / len);
      if (a == b) continue;
      g.AddEdge(ID(a), ID(b));
    }
  }

  g.Build();

  Polygon poly;
  for (int i = 0; i < g.faces.size(); i++)
    if (g.area[i] < 0) { // 对于连通图，惟一一个面积小于零的面是无限面
      poly = g.faces[i];
      reverse(poly.begin(), poly.end()); // 对于内部区域来说，无限面多边形的各个顶点是顺时针的
      poly = simplify(poly); // 无限面多边形上可能会有相邻共线点
      break;
    }

  int m = poly.size();
  printf("%d\n", m);

  // 挑选坐标最小的点作为输出的起点
  int start = 0;
  for (int i = 0; i < m; i++)
    if (poly[i] < poly[start]) start = i;
  for (int i = start; i < m; i++)
    printf("%.4lf %.4lf\n", poly[i].x, poly[i].y);
  for (int i = 0; i < start; i++)
    printf("%.4lf %.4lf\n", poly[i].x, poly[i].y);
}

int main() {
  freopen("find.in", "r", stdin);
  freopen("find.out", "w", stdout);

  while (scanf("%d", &n) == 1 && n) {
    for (int i = 0, x, y; i < n; i++)
      scanf("%d%d", &x, &y), P[i] = Point(x, y);
    build_graph();
  }
  return 0;
}
// 102094879	Dec/23/2020 14:54UTC+8	chenwz	F - Find the Border	GNU C++11	Accepted	31 ms	2100 KB
```

## 例题12  丛林警戒队（Jungle Outpost, NEERC 2010, LA4992/UVa1475）

### 题目描述
在丛林中有n个警戒岗哨，它们构成了一个凸n边形的顶点。敌军将要轰炸这些岗哨，但只能一次连续炸掉其中m个相邻的岗哨（m < n）。你的指挥部（总部）位于凸多边形内部的安全区域。问最少需要炸掉多少个相邻岗哨（即m的最小值），才能保证无论如何选择轰炸起始位置，总部都能被摧毁（即总部落入被炸掉岗哨后的剩余多边形之外）。

**输入格式**：输入包含多组测试数据，以n=0结束。每组第一行包含整数n（3 ≤ n ≤ 50000），表示岗哨数。接下来n行，每行两个整数x y，按顺序给出凸多边形顶点坐标。所有坐标绝对值不超过10000。

**输出格式**：对于每组测试数据，输出一行整数m，表示最少需要炸掉的相邻岗哨数量。

### 解题思路
问题等价于：对于凸n边形，去掉连续m个顶点后，剩余的点能否围住总部？答案单调：如果炸掉m个岗哨能保证摧毁总部，那么炸掉m+1个一定也能。

1. **二分答案**：对m进行二分查找，范围[1, n-3]（炸掉n-2个只剩2个点，一定无法围住总部，所以n-3一定可以）。

2. **半平面交判定**：对于给定的m，总部能被炸掉m个岗哨后摧毁，等价于：存在连续的m个岗哨，使得剩下n-m个岗哨构成的半平面交为空。具体地，每条边(p[i], p[(i+m+1)%n])定义了一个半平面（边的左边是剩余区域），如果这n个半平面的交集为空，则总部一定在安全区域之外。

3. **实现细节**：对每条边(p[i], p[(i+m+1)%n])，方向向量为p[i]-p[(i+m+1)%n]（即向内），对应的半平面为直线左边。如果半平面交为空，则check(m)返回true。

### 算法方法
- **半平面交**：使用双端队列维护当前有效半平面的交集，按极角排序后依次处理。
- **二分搜索**：在[1, n-3]上二分查找最小的m。
- **平行边处理**：遇到平行且同向的边时，保留更内侧（更严格）的那条。

### 复杂度分析
- **时间复杂度**：O(n log n)。二分需要O(log n)次check，每次check调用半平面交O(n)，总O(n log n)。n ≤ 50000。
- **空间复杂度**：O(n)，存储多边形顶点和半平面。

```cpp
// 例题12  丛林警戒队（Jungle Outpost, NEERC 2010, LA4992/UVa1475）
// Rujia Liu
#include<cstdio>
#include<cmath>
#include<vector>
#include<algorithm>
using namespace std;

struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

Vector operator + (const Vector& A, const Vector& B) { return Vector(A.x+B.x, A.y+B.y); }
Vector operator - (const Point& A, const Point& B) { return Vector(A.x-B.x, A.y-B.y); }
Vector operator * (const Vector& A, double p) { return Vector(A.x*p, A.y*p); }
double Dot(const Vector& A, const Vector& B) { return A.x*B.x + A.y*B.y; }
double Cross(const Vector& A, const Vector& B) { return A.x*B.y - A.y*B.x; }
double Length(const Vector& A) { return sqrt(Dot(A, A)); }
Vector Normal(const Vector& A) { double L = Length(A); return Vector(-A.y/L, A.x/L); }

double PolygonArea(vector<Point> p) {
  int n = p.size();
  double area = 0;
  for(int i = 1; i < n-1; i++)
    area += Cross(p[i]-p[0], p[i+1]-p[0]);
  return area/2;
}

// 有向直线。它的左边就是对应的半平面
struct Line {
  Point P;    // 直线上任意一点
  Vector v;   // 方向向量
  double ang; // 极角，即从x正半轴旋转到向量v所需要的角（弧度）
  Line() {}
  Line(Point P, Vector v):P(P),v(v){ ang = atan2(v.y, v.x); }
  bool operator < (const Line& L) const {
    return ang < L.ang;
  }
};

// 点p在有向直线L的左边（线上不算）
bool OnLeft(const Line& L, const Point& p) {
  return Cross(L.v, p-L.P) > 0;
}

// 二直线交点，假定交点惟一存在
Point GetLineIntersection(const Line& a, const Line& b) {
  Vector u = a.P-b.P;
  double t = Cross(b.v, u) / Cross(a.v, b.v);
  return a.P+a.v*t;
}

const double eps = 1e-6;

// 半平面交主过程
vector<Point> HalfplaneIntersection(vector<Line>& L) {
  int n = L.size();
  sort(L.begin(), L.end()); // 按极角排序
  
  int first, last;         // 双端队列的第一个元素和最后一个元素的下标
  vector<Point> p(n);      // p[i]为q[i]和q[i+1]的交点
  vector<Line> q(n);       // 双端队列
  vector<Point> ans;       // 结果

  q[first=last=0] = L[0];  // 双端队列初始化为只有一个半平面L[0]
  for(int i = 1; i < n; i++) {
    while(first < last && !OnLeft(L[i], p[last-1])) last--;
    while(first < last && !OnLeft(L[i], p[first])) first++;
    q[++last] = L[i];
    if(fabs(Cross(q[last].v, q[last-1].v)) < eps) { // 两向量平行且同向，取内侧的一个
      last--;
      if(OnLeft(q[last], L[i].P)) q[last] = L[i];
    }
    if(first < last) p[last-1] = GetLineIntersection(q[last-1], q[last]);
  }
  while(first < last && !OnLeft(q[first], p[last-1])) last--; // 删除无用平面
  if(last - first <= 1) return ans; // 空集
  p[last] = GetLineIntersection(q[last], q[first]); // 计算首尾两个半平面的交点

  // 从deque复制到输出中
  for(int i = first; i <= last; i++) ans.push_back(p[i]);
  return ans;
}

const int maxn = 50000 + 10;
int n;
Point P[maxn];

// 连续m个点是否可以保证炸到总部
bool check(int m) {
  vector<Line> lines;
  for(int i = 0; i < n; i++)
    lines.push_back(Line(P[(i+m+1)%n], P[i]-P[(i+m+1)%n]));
  return HalfplaneIntersection(lines).empty();
}

int solve() {
  if(n == 3) return 1;
  int L = 1, R = n-3, M; // 炸n-3个点一定可以摧毁
  while(L < R) {
    M = L + (R-L)/2;
    if(check(M)) R = M; else L = M+1;
  }
  return L;
}

int main() {
  while(scanf("%d", &n) == 1 && n) {
    for(int i = 0; i < n; i++) {
      int x, y;
      scanf("%d%d", &x, &y);
      P[i] = Point(x, y);
    }
    printf("%d\n", solve());
  }
  return 0;
}
// 25877781	1475	Jungle Outpost	Accepted	C++	3.650	2020-12-23 06:48:05
```

## 例题11  铁人三项（Triathlon, NEERC 2000, POJ1755）

### 题目描述
铁人三项比赛包含游泳、自行车和跑步三个项目。已知n位选手在三个项目中的速度V[i]（游泳）、U[i]（自行车）、W[i]（跑步）。比赛总距离固定为1个单位，但可以自由分配三个项目的距离（比例x, y, z，满足x + y + z = 1，且x, y, z > 0）。对于每位选手，问是否存在一种距离分配方案，使得该选手获得冠军（总时间严格小于其他所有选手）。

**输入格式**：输入包含多组测试数据，以n=0结束。每组第一行包含整数n（1 ≤ n ≤ 100），表示选手数。接下来n行，每行三个整数V U W，分别表示游泳、自行车、跑步的速度。所有速度为正整数，不超过10000。

**输出格式**：对于每位选手，按输入顺序输出一行，如果存在使其获胜的距离分配方案，输出"Yes"，否则输出"No"。

### 解题思路
选手i获胜的条件：存在(x, y)满足 x + y < 1, x > 0, y > 0，且对于所有j ≠ i：

`x/V[i] + y/U[i] + (1-x-y)/W[i] < x/V[j] + y/U[j] + (1-x-y)/W[j]`

将每个不等式转化为ax + by + c > 0的形式，这定义了一个半平面。问题转化为：n-1个半平面与约束三角形(x>0, y>0, x+y<1)的交集是否非空。如果交集非空，则选手i有获胜方案。

### 算法方法
- **半平面交**：将每个"i比j快"的不等式转化为有向直线（半平面左侧为可行域），使用双端队列求所有半平面的交集。
- **不等式变换**：`a = (k/V[j] - k/W[j]) - (k/V[i] - k/W[i])` 等，乘以k=10000防止浮点溢出。
- **边界约束**：x>0, y>0, -x-y+1>0 三个半平面定义可行三角形。
- **平凡判定**：如果存在一个选手j在三个项目上都不慢于i，则i无法获胜。

### 复杂度分析
- **时间复杂度**：O(n² log n)。对每位选手，需要与其他n-1位构造半平面O(n)，半平面交O(n log n)。n位选手总O(n² log n)。n ≤ 100。
- **空间复杂度**：O(n)，存储半平面和交点。

```cpp
// 例题11  铁人三项（Triathlon, NEERC 2000, POJ1755）
// Rujia Liu
#include<cstdio>
#include<cmath>
#include<vector>
#include<algorithm>
using namespace std;

struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

Vector operator + (const Vector& A, const Vector& B) { return Vector(A.x+B.x, A.y+B.y); }
Vector operator - (const Point& A, const Point& B) { return Vector(A.x-B.x, A.y-B.y); }
Vector operator * (const Vector& A, double p) { return Vector(A.x*p, A.y*p); }
double Dot(const Vector& A, const Vector& B) { return A.x*B.x + A.y*B.y; }
double Cross(const Vector& A, const Vector& B) { return A.x*B.y - A.y*B.x; }
double Length(const Vector& A) { return sqrt(Dot(A, A)); }
Vector Normal(const Vector& A) { double L = Length(A); return Vector(-A.y/L, A.x/L); }

double PolygonArea(vector<Point> p) {
  int n = p.size();
  double area = 0;
  for(int i = 1; i < n-1; i++)
    area += Cross(p[i]-p[0], p[i+1]-p[0]);
  return area/2;
}

// 有向直线。它的左边就是对应的半平面
struct Line {
  Point P;    // 直线上任意一点
  Vector v;   // 方向向量
  double ang; // 极角，即从x正半轴旋转到向量v所需要的角（弧度）
  Line() {}
  Line(Point P, Vector v):P(P),v(v){ ang = atan2(v.y, v.x); }
  bool operator < (const Line& L) const {
    return ang < L.ang;
  }
};

// 点p在有向直线L的左边（线上不算）
bool OnLeft(const Line& L, const Point& p) {
  return Cross(L.v, p-L.P) > 0;
}

// 二直线交点，假定交点惟一存在
Point GetLineIntersection(const Line& a, const Line& b) {
  Vector u = a.P-b.P;
  double t = Cross(b.v, u) / Cross(a.v, b.v);
  return a.P+a.v*t;
}

const double INF = 1e8;
const double eps = 1e-6;

// 半平面交主过程
vector<Point> HalfplaneIntersection(vector<Line> L) {
  int n = L.size();
  sort(L.begin(), L.end()); // 按极角排序
  
  int first, last;         // 双端队列的第一个元素和最后一个元素的下标
  vector<Point> p(n);      // p[i]为q[i]和q[i+1]的交点
  vector<Line> q(n);       // 双端队列
  vector<Point> ans;       // 结果

  q[first=last=0] = L[0];  // 双端队列初始化为只有一个半平面L[0]
  for(int i = 1; i < n; i++) {
    while(first < last && !OnLeft(L[i], p[last-1])) last--;
    while(first < last && !OnLeft(L[i], p[first])) first++;
    q[++last] = L[i];
    if(fabs(Cross(q[last].v, q[last-1].v)) < eps) { // 两向量平行且同向，取内侧的一个
      last--;
      if(OnLeft(q[last], L[i].P)) q[last] = L[i];
    }
    if(first < last) p[last-1] = GetLineIntersection(q[last-1], q[last]);
  }
  while(first < last && !OnLeft(q[first], p[last-1])) last--; // 删除无用平面
  if(last - first <= 1) return ans; // 空集
  p[last] = GetLineIntersection(q[last], q[first]); // 计算首尾两个半平面的交点

  // 从deque复制到输出中
  for(int i = first; i <= last; i++) ans.push_back(p[i]);
  return ans;
}

const int maxn = 100 + 10;
int V[maxn], U[maxn], W[maxn];
int main() {
  int n;
  while(scanf("%d", &n) == 1 && n) {
    for(int i = 0; i < n; i++) scanf("%d%d%d", &V[i], &U[i], &W[i]);
    for(int i = 0; i < n; i++) {
      int ok = 1;
      double k = 10000;
      vector<Line> L;
      for(int j = 0; j < n; j++) if(i != j) {
        if(V[i] <= V[j] && U[i] <= U[j] && W[i] <= W[j]) { ok = 0; break; }
        if(V[i] >= V[j] && U[i] >= U[j] && W[i] >= W[j]) continue;
        // x/V[i]+y/U[i]+(1-x-y)/W[i] < x/V[j]+y/U[j]+(1-x-y)/W[j]
        // ax+by+c>0
        double a = (k/V[j]-k/W[j]) - (k/V[i]-k/W[i]);
        double b = (k/U[j]-k/W[j]) - (k/U[i]-k/W[i]);
        double c = k/W[j] - k/W[i];
        Point P;
        Vector v(b, -a);
        if(fabs(a) > fabs(b)) P = Point(-c/a, 0);
        else P = Point(0, -c/b);
        L.push_back(Line(P, v));
      }
      if(ok) {
        // x>0, y>0, x+y<1 ==> -x-y+1>0
        L.push_back(Line(Point(0, 0), Vector(0, -1)));
        L.push_back(Line(Point(0, 0), Vector(1, 0)));
        L.push_back(Line(Point(0, 1), Vector(-1, 1)));
        vector<Point> poly = HalfplaneIntersection(L);
        if(poly.empty()) ok = 0;
      }
      if(ok) printf("Yes\n"); else printf("No\n");
    }
  }
  return 0;
}
// Accepted 47ms 604kB 3818 G++2020-12-23 14:47:19|O22226821
```

## 例题13  怪物陷阱（Monster Trap, Aizu 2003, POJ2048）

### 题目描述
平面上有n条线段作为"墙"，起点为(0, 0)，终点为(1e5, 1e5)。你需要判断是否存在一条从起点到终点的路径，路径不穿过任何墙（但可以接触线段端点）。

问题可以重新表述为：给定若干线段以及起点和终点，判断起点和终点是否在同一连通区域内。如果存在一条不穿过任何线段内部的路径，则返回"yes"（安全），否则返回"no"（被围住）。

**输入格式**：输入包含多组测试数据，以n=0结束。每组第一行包含整数n（1 ≤ n ≤ 100），表示线段数。接下来n行，每行四个浮点数x1 y1 x2 y2，表示线段两端点坐标。所有坐标绝对值不超过100。

**输出格式**：对于每组测试数据，如果存在安全路径输出"yes"，否则输出"no"。

### 解题思路
1. **图论建模**：将起点、终点以及所有线段的端点（不在其他线段中间的点）作为图的顶点。如果两个顶点之间的连线不与任何线段规范相交，则在它们之间连一条边。

2. **线段预处理**：将每条线段向两端略微延长eps=1e-6，这样可以正确处理端点在墙上的情况。

3. **连通性判断**：在构造的图上，从起点(0,0)开始DFS/BFS，检查是否能到达终点(1e5,1e5)。能到达则安全。

### 算法方法
- **顶点选择**：起点、终点以及所有不在任何一条线段内部（OnSegment）的线段端点。
- **构图**：对于每对顶点，检查其连线是否与任何线段规范相交（SegmentProperIntersection），不相交则连边。
- **DFS搜索**：从起点(0)出发，搜索终点(1)。

### 复杂度分析
- **时间复杂度**：O(n³)。顶点数O(n)，所有点对O(n²)，每对需要O(n)检查是否与线段相交。n ≤ 100。
- **空间复杂度**：O(n²)，邻接矩阵存储图。

```cpp
// 例题13  怪物陷阱（Monster Trap, Aizu 2003, POJ2048）
// Rujia Liu
#include<iostream>
#include<vector>
#include<cmath>
#include<cstring>
#include<algorithm>
using namespace std;

const double eps = 1e-12;
double dcmp(double x) {
  if(fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}

struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

Vector operator + (const Point& A, const Point& B) {
  return Vector(A.x+B.x, A.y+B.y);
}

Vector operator - (const Point& A, const Point& B) {
  return Vector(A.x-B.x, A.y-B.y);
}

Vector operator * (const Point& A, double v) {
  return Vector(A.x*v, A.y*v);
}

Vector operator / (const Point& A, double v) {
  return Vector(A.x/v, A.y/v);
}

double Cross(const Vector& A, const Vector& B) {
  return A.x*B.y - A.y*B.x;
}

double Dot(const Vector& A, const Vector& B) {
  return A.x*B.x + A.y*B.y;
}

double Length(const Vector& A) {
  return sqrt(Dot(A,A));
}

bool operator < (const Point& p1, const Point& p2) {
  return p1.x < p2.x || (p1.x == p2.x && p1.y < p2.y);
}

bool operator == (const Point& p1, const Point& p2) {
  return p1.x == p2.x && p1.y == p2.y;
}

bool SegmentProperIntersection(const Point& a1, const Point& a2, const Point& b1, const Point& b2) {
  double c1 = Cross(a2-a1,b1-a1), c2 = Cross(a2-a1,b2-a1),
  c3 = Cross(b2-b1,a1-b1), c4=Cross(b2-b1,a2-b1);
  return dcmp(c1)*dcmp(c2)<0 && dcmp(c3)*dcmp(c4)<0;
}

bool OnSegment(const Point& p, const Point& a1, const Point& a2) {
  return dcmp(Cross(a1-p, a2-p)) == 0 && dcmp(Dot(a1-p, a2-p)) < 0;
}

const int maxv = 200 + 5;
int V;
int G[maxv][maxv], vis[maxv];

bool dfs(int u) {
  if(u == 1) return true; // 1是终点
  vis[u] = 1;
  for(int v = 0; v < V; v++)
    if(G[u][v] && !vis[v] && dfs(v)) return true;
  return false;
}

const int maxn = 100 + 5;
int n;
Point p1[maxn], p2[maxn];

// 在任何一条线段的中间（在端点不算）
bool OnAnySegment(Point p) {
  for(int i = 0; i < n; i++)
    if(OnSegment(p, p1[i], p2[i])) return true;
  return false;
}

// 与任何一条线段规范相交
bool IntersectWithAnySegment(Point a, Point b) {
  for(int i = 0; i < n; i++)
    if(SegmentProperIntersection(a, b, p1[i], p2[i])) return true;
  return false;
}

bool find_path() {
  // 构图
  vector<Point> vertices;
  vertices.push_back(Point(0, 0)); // 起点
  vertices.push_back(Point(1e5, 1e5)); // 终点
  for(int i = 0; i < n; i++) {
    if(!OnAnySegment(p1[i])) vertices.push_back(p1[i]);
    if(!OnAnySegment(p2[i])) vertices.push_back(p2[i]);
  }
  V = vertices.size();
  memset(G, 0, sizeof(G));
  memset(vis, 0, sizeof(vis));
  for(int i = 0; i < V; i++)
    for(int j = i+1; j < V; j++)
      if(!IntersectWithAnySegment(vertices[i], vertices[j]))
        G[i][j] = G[j][i] = 1;
  return dfs(0);
}

int main() {
  while(cin >> n && n) {
    for(int i = 0; i < n; i++) {
      double x1, y1, x2, y2;
      cin >> x1 >> y1 >> x2 >> y2;
      Point a = Point(x1, y1);
      Point b = Point(x2, y2);
      Vector v = b - a;
      v = v / Length(v);
      p1[i] = a - v * 1e-6;
      p2[i] = b + v * 1e-6;
    }
    if(find_path()) cout << "no\n"; else cout << "yes\n";
  }
  return 0;
}
```

## 例题8  点集划分（The Great Divide, UVa 10256）

### 题目描述
给定平面上红色和蓝色两个点集，问是否存在一条直线能够将红色点和蓝色点完全分开（即所有红点在直线一侧，所有蓝点在另一侧）。

**输入格式**：输入包含多组测试数据，以"0 0"结束。每组第一行包含两个整数n和m（1 ≤ n, m ≤ 500），分别表示红色和蓝色点的数量。接下来n行每行两个浮点数x y，表示红色点坐标。再接下来m行每行两个浮点数x y，表示蓝色点坐标。所有坐标绝对值不超过1000。

**输出格式**：对于每组测试数据，如果存在一条直线可以分离两个点集，输出"Yes"，否则输出"No"。

### 解题思路
这个问题等价于判断两个点集的凸包是否相交：

1. **凸包缩并**：如果存在分离直线，那么可以找到一条与两个凸包都相切的直线将它们分开。因此，两个点集可分离当且仅当它们的凸包不相交（也不包含对方）。

2. **凸包相交判断**：
   - 检查凸包A的每个顶点是否在凸包B内部或边界上
   - 检查凸包B的每个顶点是否在凸包A内部或边界上
   - 检查凸包A和B的各边是否规范相交

3. **特殊情况**：如果某个点集只包含1个点，它的凸包退化为点；如果某点集共线，凸包退化为线段。此时需要特判。

### 算法方法
- **凸包**：Andrew算法（单调链算法），先按x后y排序，然后构造下凸壳和上凸壳，再合并。
- **点在多边形内**：使用winding number算法，通过叉积符号累加判断点的位置。
- **线段规范相交**：双向叉积异侧判断。

### 复杂度分析
- **时间复杂度**：O((N+M)log(N+M)) + O(NM)。凸包构造O(N log N + M log M)，相交判断O(NM)。N,M ≤ 500。
- **空间复杂度**：O(N+M)，存储点坐标和凸包顶点。

```cpp
// 例题8  点集划分（The Great Divide, UVa 10256）
// Rujia Liu
#include<cstdio>
#include<vector>
#include<cmath>
#include<algorithm>
using namespace std;

const double eps = 1e-10;
double dcmp(double x) {
  if(fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}

struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

Vector operator - (const Point& A, const Point& B) {
  return Vector(A.x-B.x, A.y-B.y);
}

double Cross(const Vector& A, const Vector& B) {
  return A.x*B.y - A.y*B.x;
}

double Dot(const Vector& A, const Vector& B) {
  return A.x*B.x + A.y*B.y;
}

bool operator < (const Point& p1, const Point& p2) {
  return p1.x < p2.x || (p1.x == p2.x && p1.y < p2.y);
}

bool operator == (const Point& p1, const Point& p2) {
  return p1.x == p2.x && p1.y == p2.y;
}

bool SegmentProperIntersection(const Point& a1, const Point& a2, const Point& b1, const Point& b2) {
  double c1 = Cross(a2-a1,b1-a1), c2 = Cross(a2-a1,b2-a1),
  c3 = Cross(b2-b1,a1-b1), c4=Cross(b2-b1,a2-b1);
  return dcmp(c1)*dcmp(c2)<0 && dcmp(c3)*dcmp(c4)<0;
}

bool OnSegment(const Point& p, const Point& a1, const Point& a2) {
  return dcmp(Cross(a1-p, a2-p)) == 0 && dcmp(Dot(a1-p, a2-p)) < 0;
}

// 点集凸包
// 如果不希望在凸包的边上有输入点，把两个 <= 改成 <
// 如果不介意点集被修改，可以改成传递引用
vector<Point> ConvexHull(vector<Point> p) {
  // 预处理，删除重复点
  sort(p.begin(), p.end());
  p.erase(unique(p.begin(), p.end()), p.end());

  int n = p.size();
  int m = 0;
  vector<Point> ch(n+1);
  for(int i = 0; i < n; i++) {
    while(m > 1 && Cross(ch[m-1]-ch[m-2], p[i]-ch[m-2]) <= 0) m--;
    ch[m++] = p[i];
  }
  int k = m;
  for(int i = n-2; i >= 0; i--) {
    while(m > k && Cross(ch[m-1]-ch[m-2], p[i]-ch[m-2]) <= 0) m--;
    ch[m++] = p[i];
  }
  if(n > 1) m--;
  ch.resize(m);
  return ch;
}

int IsPointInPolygon(const Point& p, const vector<Point>& poly){
  int wn = 0;
  int n = poly.size();
  for(int i = 0; i < n; i++){
    const Point& p1 = poly[i];
    const Point& p2 = poly[(i+1)%n];
    if(p1 == p || p2 == p || OnSegment(p, p1, p2)) return -1; // 在边界上
    int k = dcmp(Cross(p2-p1, p-p1));
    int d1 = dcmp(p1.y - p.y);
    int d2 = dcmp(p2.y - p.y);
    if(k > 0 && d1 <= 0 && d2 > 0) wn++;
    if(k < 0 && d2 <= 0 && d1 > 0) wn--;
  }
  if (wn != 0) return 1; // 内部
  return 0; // 外部
}

bool ConvexPolygonDisjoint(const vector<Point> ch1, const vector<Point> ch2) {
  int c1 = ch1.size();
  int c2 = ch2.size();
  for(int i = 0; i < c1; i++)
    if(IsPointInPolygon(ch1[i], ch2) != 0) return false; // 内部或边界上
  for(int i = 0; i < c2; i++)
    if(IsPointInPolygon(ch2[i], ch1) != 0) return false; // 内部或边界上
  for(int i = 0; i < c1; i++)
    for(int j = 0; j < c2; j++)
      if(SegmentProperIntersection(ch1[i], ch1[(i+1)%c1], ch2[j], ch2[(j+1)%c2])) return false;
  return true;
}

int main() {
  int n, m;
  while(scanf("%d%d", &n, &m) == 2 && n > 0 && m > 0) {
    vector<Point> P1, P2;
    double x, y;
    for(int i = 0; i < n; i++) {
      scanf("%lf%lf", &x, &y);
      P1.push_back(Point(x, y));
    }
    for(int i = 0; i < m; i++) {
      scanf("%lf%lf", &x, &y);
      P2.push_back(Point(x, y));
    }
    if(ConvexPolygonDisjoint(ConvexHull(P1), ConvexHull(P2)))
      printf("Yes\n");
    else
      printf("No\n");
  }
  return 0;
}
// 25877756	10256	The Great Divide	Accepted	C++	0.090	2020-12-23 06:41:59
```

## 例题6  包装木板（Board Wrapping, UVa 10652）

### 题目描述
你需要用一张矩形的包装纸将n块矩形木板包裹起来。每块木板由其中心坐标(x, y)、宽度w、高度h以及逆时针旋转角度j（度数）来描述。包装纸是轴对齐的，且必须是一个矩形。求这些木板所占面积总和与包装纸最小面积之比的百分数。

**输入格式**：第一行是整数T（T ≤ 30），表示测试数据组数。每组数据第一行是整数n（1 ≤ n ≤ 600），表示木板数量。接下来n行，每行包含 x y w h j（所有数值为浮点数），其中(x,y)是中心坐标，w是宽度，h是高度，j是逆时针旋转角度（度数）。坐标绝对值不超过1000，w和h为正数。

**输出格式**：对于每组测试数据，输出一行形如"X.Y %"的百分数，保留1位小数。

### 解题思路
将所有木板视为旋转后的矩形，问题等价于求这些矩形所有顶点的凸包面积：

1. **矩形顶点计算**：对于每块木板，计算其四个顶点的坐标。矩形中心为o，半宽半高分别为w/2和h/2，旋转角度为-j（顺时针，因为输入是逆时针旋转但计算顶点时需反向）。每个顶点 = o + Rotate(角点向量, -j)。

2. **凸包面积**：使用Andrew算法求所有顶点的凸包，然后用叉积公式计算凸包多边形的有向面积。

3. **比值计算**：包装纸面积 = 凸包面积，木板总面积 = Σ w*h。答案为 (总面积 / 凸包面积) × 100。

### 算法方法
- **向量旋转**：Rotate函数实现2D旋转变换。
- **凸包（Andrew算法）**：先按x后y排序，构造下凸壳（从左到右），再构造上凸壳（从右到左）。
- **多边形面积**：以第一个顶点为基准，对所有三角形叉积求和。

### 复杂度分析
- **时间复杂度**：O(N log N)，N = 4n ≤ 2400个点。排序O(N log N)，凸包构造O(N)。T ≤ 30，总约72000个点。
- **空间复杂度**：O(N)，存储所有顶点和凸包。

```cpp
// 例题6  包装木板（Board Wrapping, UVa 10652）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

const double PI = acos(-1.0);
double torad(double deg) { return deg / 180 * PI; }

struct Point {
  double x, y;
  Point(double x = 0, double y = 0): x(x), y(y) { }
};
istream& operator>>(istream& is, Point& p) { return is >> p.x >> p.y; }
ostream& operator<<(ostream& os, const Point& p) { return os << p.x << " " << p.y; }
typedef Point Vector;

Vector operator + (const Vector& A, const Vector& B) { return Vector(A.x + B.x, A.y + B.y); }
Vector operator - (const Point& A, const Point& B) { return Vector(A.x - B.x, A.y - B.y); }
double Cross(const Vector& A, const Vector& B) { return A.x * B.y - A.y * B.x; }
Vector Rotate(const Vector& A, double rad)
{ return Vector(A.x * cos(rad) - A.y * sin(rad), A.x * sin(rad) + A.y * cos(rad));}
bool operator < (const Point& p1, const Point& p2)
{ return p1.x < p2.x || (p1.x == p2.x && p1.y < p2.y);}
bool operator == (const Point& p1, const Point& p2)
{return p1.x == p2.x && p1.y == p2.y;}

// 点集凸包 如果不希望在凸包的边上有输入点，把两个 <= 改成 < 如果不介意点集被修改，可以改成传递引用
vector<Point> ConvexHull(vector<Point> p) {
  // 预处理，删除重复点
  sort(p.begin(), p.end());
  p.erase(unique(p.begin(), p.end()), p.end());

  int n = p.size();
  int m = 0;
  vector<Point> ch(n + 1);
  for (int i = 0; i < n; i++) {
    while (m > 1 && Cross(ch[m - 1] - ch[m - 2], p[i] - ch[m - 2]) <= 0) m--;
    ch[m++] = p[i];
  }
  int k = m;
  for (int i = n - 2; i >= 0; i--) {
    while (m > k && Cross(ch[m - 1] - ch[m - 2], p[i] - ch[m - 2]) <= 0) m--;
    ch[m++] = p[i];
  }
  if (n > 1) m--;
  ch.resize(m);
  return ch;
}

// 多边形的有向面积
double PolygonArea(const vector<Point>& p) {
  double area = 0;
  int n = p.size();
  for (int i = 1; i < n - 1; i++)
    area += Cross(p[i] - p[0], p[i + 1] - p[0]);
  return area / 2;
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T; cin >> T;
  for (int t = 0, n; t < T; t++) {
    double area1 = 0;
    cin >> n;
    vector<Point> P;
    for (int i = 0; i < n; i++) {
      Point o;
      double w, h, j, ang;
      cin >> o >> w >> h >> j;
      ang = -torad(j);
      P.push_back(o + Rotate(Vector(-w / 2, -h / 2), ang));
      P.push_back(o + Rotate(Vector(w / 2, -h / 2), ang));
      P.push_back(o + Rotate(Vector(-w / 2, h / 2), ang));
      P.push_back(o + Rotate(Vector(w / 2, h / 2), ang));
      area1 += w * h;
    }
    double area2 = PolygonArea(ConvexHull(P));
    printf("%.1lf %%\n", area1 * 100 / area2);
  }
  return 0;
}
// 24480925  10652 Board Wrapping  Accepted  C++11 0.010 2020-01-28 14:38:30
```

## 例题7  飞机场（Airport, UVa 11168）

### 题目描述
平面上有n个城镇（点），需要修建一个飞机场（直线跑道）。飞机场是一条直线，所有居民到飞机场的距离定义为点到直线的垂直距离。求使得所有居民到机场距离之和最小的直线，并输出最小总距离（所有居民到直线的距离之和的平均值）。

**输入格式**：第一行是整数T（T ≤ 65），表示测试数据组数。每组数据第一行是整数n（1 ≤ n ≤ 10000），表示城镇数量。接下来n行，每行两个整数x y，表示城镇坐标。所有坐标绝对值不超过10000。

**输出格式**：对于每组测试数据，输出一行"Case #X: Y"，其中X为测试编号，Y为最小总平均距离，保留3位小数。

### 解题思路
关键观察：最优直线一定经过所有点的凸包的一条边。因为：

1. **中位数原理**：所有点沿直线垂线方向的距离之和最小，当直线两侧点数尽可能平衡时。对于凸包来说，最优直线不会穿过任何点，而是沿着某条凸包边。

2. **距离公式**：对于直线ax+by+c=0，所有点(xi, yi)到直线的有向距离之和为|a·Σxi + b·Σyi + n·c| / sqrt(a²+b²)。先预处理所有点的x坐标和Sx以及y坐标和Sy。

3. **凸包简化**：先求所有点的凸包。如果凸包退化为点（n=1），答案为0；如果退化为线段（所有点共线），答案为0。否则，遍历凸包的每条边，计算以此边所在直线为机场时的总距离。

4. **距离计算优化**：对于凸包边(a0, a)，方向向量D = a - a0。点到直线的距离公式可推导为：`|(Sx - a0.x * n) * D.y - (Sy - a0.y * n) * D.x| / |D| / n`。

### 算法方法
- **凸包**：Andrew算法求凸包。
- **代数优化**：利用所有点坐标之和Sx、Sy，避免对每个点重复计算，将O(n)降为O(1)。
- **距离简化**：使用叉积公式简化点到直线的距离计算。

### 复杂度分析
- **时间复杂度**：O(N log N)。凸包构造需要排序O(N log N)，遍历凸包每条边O(N)。N ≤ 10000。
- **空间复杂度**：O(N)，存储点和凸包。

```cpp
// 例题7  飞机场（Airport, UVa 11168）
// 李劲逸,陈锋 - 不用解析几何知识的版本
#include<bits/stdc++.h>
using namespace std;
const double eps = 1e-7;

struct Point {
  double x, y;
  Point(double a = 0, double b = 0) : x(a), y(b) {}
};
typedef Point Vector;
istream& operator>>(istream& is, Point& p) { return is >> p.x >> p.y; }
ostream& operator<<(ostream& os, const Point& p) { return os << p.x << " " << p.y; }
Vector operator + (const Point& A, const Point& B)
{return Vector(A.x + B.x, A.y + B.y);}
Vector operator - (const Point& A, const Point& B)
{return Vector(A.x - B.x, A.y - B.y);}
bool operator < (const Point& p1, const Point& p2)
{ return p1.x < p2.x || (p1.x == p2.x && p1.y < p2.y);}
bool operator == (const Point& p1, const Point& p2)
{ return p1.x == p2.x && p1.y == p2.y;}
double Cross(const Vector& A, const Vector& B) { return A.x * B.y - A.y * B.x; }
double Dot(const Vector& A, const Vector& B) { return A.x * B.x + A.y * B.y; }
double Length(const Vector& A) { return sqrt(Dot(A, A)); }

// 点集凸包， 如果不希望在凸包的边上有输入点，把两个 <= 改成 <
// 如果不介意点集被修改，可以改成传递引用
vector<Point> ConvexHull(vector<Point> p) {
  sort(p.begin(), p.end()); // 预处理，删除重复点
  p.erase(unique(p.begin(), p.end()), p.end());
  int n = p.size();
  int m = 0;
  vector<Point> ch(n + 1);
  for (int i = 0; i < n; i++) {
    while (m > 1 && Cross(ch[m - 1] - ch[m - 2], p[i] - ch[m - 2]) <= 0) m--;
    ch[m++] = p[i];
  }
  int k = m;
  for (int i = n - 2; i >= 0; i--) {
    while (m > k && Cross(ch[m - 1] - ch[m - 2], p[i] - ch[m - 2]) <= 0) m--;
    ch[m++] = p[i];
  }
  if (n > 1) m--;
  ch.resize(m);
  return ch;
}

double solve(vector<Point> &A) {
  int n = A.size();
  if (n == 1) return 0; // 凸包退化成点或线段，则答案为0
  Point s;
  for (int i = 0; i < n; i++) s = s + A[i]; // 所有点x和y坐标之和
  A = ConvexHull(A), A.push_back(A[0]);
  double ans = 1e18;
  for (size_t i = 1; i < A.size(); i++) {
    const Point& a0 = A[i - 1], a = A[i]; // 作为备选直线
    Vector D = a - a0; // 点到直线的距离都是平行四边形面积➗D的长度
    ans = min(fabs((s.x - a0.x * n) * D.y - (s.y - a0.y * n) * D.x) / Length(D), ans);
  }
  return ans / n;
}

int main() {
  int T; cin >> T;
  for (int kase = 1, n; kase <= T; kase++) {
    cin >> n;
    vector<Point> A(n);
    for (int i = 0; i < n; i++) cin >> A[i];
    printf("Case #%d: %.3lf\n", kase, solve(A));
  }
  return 0;
}
// 26040910 11168 Airport Accepted  C++ 0.030 2021-01-31 14:21:05
```

## 例题15  块和圆盘（Pieces and Discs, UVa 12296）

### 题目描述
有一个L×W的矩形木板。先用n条直线对木板进行切割，将木板分成若干块（碎片）。然后进行m次查询，每次查询给定一个圆（圆心坐标和半径），问这个圆覆盖了哪些碎片，输出被覆盖碎片的面积列表（按升序排列）。

**输入格式**：输入包含多组测试数据，以n=m=L=W=0结束。每组数据：
- 第一行：n m L W（1 ≤ n,m ≤ 20，1 ≤ L,W ≤ 100）
- 接下来n行，每行x1 y1 x2 y2，表示一条切割线段的端点坐标。
- 接下来m行，每行x y R，表示查询圆的圆心和半径。

所有坐标和半径均为整数，0 < R ≤ 1000。

**输出格式**：对于每组数据的每个查询，输出一行：覆盖的碎片数，然后按升序输出这些碎片的面积（保留2位小数）。每组数据之间输出空行。

### 解题思路
1. **多边形切割**：使用CutPolygon函数，用有向直线A→B切割多边形，返回直线左侧的部分。通过切割可以逐步细分出所有碎片。

2. **初始碎片**：从一个包含整个木板的矩形(0,0)→(L,0)→(L,W)→(0,W)开始。

3. **每次切割**：对当前所有碎片，用切割线段及其反向线段分别切割，得到左侧和右侧碎片。保留面积≥3个顶点的碎片（即有效多边形）。

4. **查询**：对于每个查询圆，判断每个碎片是否与圆相交：
   - 圆心在碎片内部
   - 圆包含碎片的某个顶点
   - 圆与碎片的某条边相交
   - 圆的边界穿过碎片（取边中点检测）

### 算法方法
- **多边形切割**（Sutherland-Hodgman变种）：对多边形的每条边，判断起点在直线哪侧，并将与直线的交点作为新顶点。
- **点在多边形内**：winding number算法。
- **圆与线段相交**：联立直线参数方程和圆方程，判断解参数是否在(0,1)内。
- **点在圆内**：比较距离平方与半径平方。

### 复杂度分析
- **时间复杂度**：O(2^N × N² × M × N)。n ≤ 20，碎片数最多约2^N/2。每次查询O(碎片数×碎片边长)。
- **空间复杂度**：O(2^N)，存储所有碎片多边形。

```cpp
// 例题15  块和圆盘（Pieces and Discs, UVa 12296）
// Rujia Liu
#include<cstdio>
#include<cmath>
#include<vector>
#include<algorithm>

using namespace std;

const double eps = 1e-8;
double dcmp(double x) {
  if(fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}

struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

typedef vector<Point> Polygon;

Vector operator + (Vector A, Vector B) {
  return Vector(A.x+B.x, A.y+B.y);
}

Vector operator - (Point A, Point B) {
  return Vector(A.x-B.x, A.y-B.y);
}

Vector operator * (Vector A, double p) {
  return Vector(A.x*p, A.y*p);
}

double Dot(Vector A, Vector B) { return A.x*B.x + A.y*B.y; }
double Cross(Vector A, Vector B) { return A.x*B.y - A.y*B.x; }
double Length2(Vector A) { return Dot(A, A); }

Point GetLineIntersection(Point P, Vector v, Point Q, Vector w) {
  Vector u = P-Q;
  double t = Cross(w, u) / Cross(v, w);
  return P+v*t;
}

bool OnSegment(Point p, Point a1, Point a2) {
  return dcmp(Cross(a1-p, a2-p)) == 0 && dcmp(Dot(a1-p, a2-p)) < 0;
}

// 多边形的有向面积
double PolygonArea(Polygon poly) {
  double area = 0;
  int n = poly.size();
  for(int i = 1; i < n-1; i++)
    area += Cross(poly[i]-poly[0], poly[(i+1)%n]-poly[0]);
  return area/2;
}

// cut with directed line A->B, return the left part
// may return a single point or a line segment
Polygon CutPolygon(Polygon poly, Point A, Point B) {
  Polygon newpoly;
  int n = poly.size();
  for(int i = 0; i < n; i++) {
    Point C = poly[i];
    Point D = poly[(i+1)%n];
    if(dcmp(Cross(B-A, C-A)) >= 0) newpoly.push_back(C);
    if(dcmp(Cross(B-A, C-D)) != 0) {
      Point ip = GetLineIntersection(A, B-A, C, D-C);
      if(OnSegment(ip, C, D)) newpoly.push_back(ip);
    }
  }
  return newpoly;
}

int isPointInPolygon(Point p, Polygon v){
  int wn = 0;
  int n = v.size();
  for(int i = 0; i < n; i++){
    if(OnSegment(p, v[i], v[(i+1)%n])) return -1; // 在边界上
    int k = dcmp(Cross(v[(i+1)%n]-v[i], p-v[i]));
    int d1 = dcmp(v[i].y - p.y);
    int d2 = dcmp(v[(i+1)%n].y - p.y);
    if(k > 0 && d1 <= 0 && d2 > 0) wn++;
    if(k < 0 && d2 <= 0 && d1 > 0) wn--;
  }
  if (wn != 0) return 1; // 内部
  return 0; // 外部
}

// 点在圆心内。圆周上不算
bool isInCircle(Point p, Point center, double R) {
  return dcmp(Length2(p-center) - R*R) < 0;
}

// 直线AB和圆心为C，半径为r的圆的交点
// 返回交点个数，t1, t2分别为两个交点在直线方程中的参数，p1和p2为交点本身
int getLineCircleIntersection(Point A, Point B, Point C, double r, double& t1, double& t2){
  // 初始方程：(A.x + t(B.x - A.x) - C.x)^2 + (A.y + t(B.y - A.y) - C.y)^2 = r^2
  // 整理得：(at + b)^2 + (ct + d)^2 = r^2
  double a = B.x - A.x;
  double b = A.x - C.x;
  double c = B.y - A.y;
  double d = A.y - C.y;
  // 展开得：(a^2 + c^2)t^2 + 2(ab + cd)t + b^2 + d^2 - r^2 = 0，即et^2 + ft + g = 0
  double e = a * a + c * c;
  double f = 2 * (a * b + c * d);
  double g = b * b + d * d - r * r;
  double delta = f * f - 4 * e * g; // 判别式
  if(dcmp(delta) < 0) return 0; // 相离
  if(dcmp(delta) == 0){ // 相切
    t1 = t2 = -f / (2 * e);
    return 1;
  }
  t1 = (-f - sqrt(delta)) / (2 * e);
  t2 = (-f + sqrt(delta)) / (2 * e);
  return 2;
}

// 圆和线段是否相交（相切不算）。线段不考虑端点
bool CircleIntersectSegment(Point A, Point B, Point p, double R) {
  double t1, t2;
  int c = getLineCircleIntersection(A, B, p, R, t1, t2);
  if(c <= 1) return false;
  if(dcmp(t1) > 0 && dcmp(t1-1) < 0) return true; // 端点在圆上
  if(dcmp(t2) > 0 && dcmp(t2-1) < 0) return true;
  return false;
}

/////////// 题目相关
vector<Polygon> pieces, new_pieces;

void cut(int x1, int y1, int x2, int y2) {
  new_pieces.clear();
  for(int i = 0; i < pieces.size(); i++) {
    Polygon left = CutPolygon(pieces[i], Point(x1, y1), Point(x2, y2));
    Polygon right = CutPolygon(pieces[i], Point(x2, y2), Point(x1, y1));
    if(left.size() >= 3) new_pieces.push_back(left);
    if(right.size() >= 3) new_pieces.push_back(right);
  }
  pieces = new_pieces;
}

bool DiscIntersectPolygon(Polygon poly, Point p, double R) {
  if(isPointInPolygon(p, poly) != 0) return true;
  if(isInCircle(poly[0], p, R)) return true;
  int n = poly.size();
  for(int i = 0; i < n; i++) {
    if(CircleIntersectSegment(poly[i], poly[(i+1)%n], p, R)) {
      return true; // 不考虑线段端点
    }
    if(isInCircle((poly[i]+poly[(i+1)%n])*0.5, p, R)) {
      return true; // 两个端点都在圆上
    }
  }
  return false;
}

void query(Point p, int R) {
  vector<double> ans;
  for(int i = 0; i < pieces.size(); i++) {
    if(DiscIntersectPolygon(pieces[i], p, R)) {
      ans.push_back(fabs(PolygonArea(pieces[i])));
    }
  }
  printf("%d", ans.size());
  sort(ans.begin(), ans.end());
  for(int i = 0; i < ans.size(); i++)
    printf(" %.2lf", ans[i]);
  printf("\n");
}

int main() {
  int n, m, L, W;
  while(scanf("%d%d%d%d", &n, &m, &L, &W) == 4 && n) {
    pieces.clear();

    Polygon bbox;
    bbox.push_back(Point(0, 0));
    bbox.push_back(Point(L, 0));
    bbox.push_back(Point(L, W));
    bbox.push_back(Point(0, W));
    pieces.push_back(bbox);

    for(int i = 0; i < n; i++) {
      int x1, y1, x2, y2;
      scanf("%d%d%d%d", &x1, &y1, &x2, &y2);
      cut(x1, y1, x2, y2);
    }

    for(int i = 0; i < m; i++) {
      int x, y, R;
      scanf("%d%d%d", &x, &y, &R);
      query(Point(x, y), R);
    }
    printf("\n");
  }  
  return 0;
}
// 25877800	12296	Pieces and Discs	Accepted	C++	0.020	2020-12-23 06:53:42
```

## 例题10  离海最远的点（Most Distant Point from the Sea, Tokyo 2007, UVa1396）

### 题目描述
给定一个凸n边形表示一个海岛（海岸线），求岛上距离大海最远的点的距离。即求在凸多边形内部，到多边形任意边距离的最小值最大的点，并输出这个最大最小距离。

**输入格式**：输入包含多组测试数据，以n=0结束。每组第一行包含整数n（3 ≤ n ≤ 100），表示多边形顶点数。接下来n行，每行两个整数x y（-10000 ≤ x, y ≤ 10000），按逆时针顺序给出凸多边形顶点坐标。

**输出格式**：对于每组测试数据，输出一行浮点数，表示离海最远的距离，精确到小数点后6位。

### 解题思路
问题本质是求凸多边形的最大内切圆半径：在多边形内部找一个最大的圆，使其完全包含在多边形内。

1. **二分答案**：二分搜索最大距离d。对于给定的d，判断是否存在一个点在多边形内部，且到所有边的距离都≥d。

2. **半平面交判定**：对于每条边，将其向多边形内部平移d距离，得到一个新的半平面。如果所有平移后的半平面的交集非空，则说明存在到所有边距离≥d的点。

3. **半平面平移**：对于凸多边形的每条边(p[i], p[(i+1)%n])，向多边形内部（法向量方向）平移d。新直线方向不变，基准点变为p[i] + Normal(v) * d。

4. **预处理**：需要确保多边形顶点按逆时针排列。如果面积（用叉积算）为负，则翻转顶点顺序。

### 算法方法
- **二分搜索**：在[0, 20000]（最大可能距离）上二分。
- **半平面交**：双端队列维护当前有效的半平面交集，处理后得到多边形交集。
- **直线平移**：使用法向量沿内侧平移。

### 复杂度分析
- **时间复杂度**：O(n log n × log(20000/eps))。二分约30次迭代（eps=1e-6），每次O(n log n)。
- **空间复杂度**：O(n)，存储半平面和交点。

```cpp
// 例题10  离海最远的点（Most Distant Point from the Sea, Tokyo 2007, UVa1396）
// 刘汝佳
#include <cmath>
#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

struct Point {
  double x, y;
  Point(double x = 0, double y = 0): x(x), y(y) { }
};

typedef Point Vector;
Vector operator + (const Vector& A, const Vector& B) { return Vector(A.x + B.x, A.y + B.y); }
Vector operator - (const Point& A, const Point& B) { return Vector(A.x - B.x, A.y - B.y); }
Vector operator * (const Vector& A, double p) { return Vector(A.x * p, A.y * p); }
double Dot(const Vector& A, const Vector& B) { return A.x * B.x + A.y * B.y; }
double Cross(const Vector& A, const Vector& B) { return A.x * B.y - A.y * B.x; }
double Length(const Vector& A) { return sqrt(Dot(A, A)); }
Vector Normal(const Vector& A) { double L = Length(A); return Vector(-A.y / L, A.x / L); }

double PolygonArea(vector<Point> p) {
  int n = p.size();
  double area = 0;
  for (int i = 1; i < n - 1; i++)
    area += Cross(p[i] - p[0], p[i + 1] - p[0]);
  return area / 2;
}

// 有向直线。它的左边就是对应的半平面
struct Line {
  Point P;    // 直线上任意一点
  Vector v;   // 方向向量
  double ang; // 极角，即从x正半轴旋转到向量v所需要的角（弧度）
  Line() {}
  Line(const Point& P, const Vector& v): P(P), v(v) { ang = atan2(v.y, v.x); }
  bool operator < (const Line& L) const {
    return ang < L.ang;
  }
};

// 点p在有向直线L的左边（线上不算）
bool OnLeft(const Line& L, const Point& p) {
  return Cross(L.v, p - L.P) > 0;
}

// 二直线交点，假定交点惟一存在
Point GetLineIntersection(const Line& a, const Line& b) {
  Vector u = a.P - b.P;
  double t = Cross(b.v, u) / Cross(a.v, b.v);
  return a.P + a.v * t;
}

const double INF = 1e8, eps = 1e-6;

// 半平面交主过程
vector<Point> HalfplaneIntersection(vector<Line> L) {
  int n = L.size();
  sort(L.begin(), L.end()); // 按极角排序

  int first, last;         // 双端队列的第一个元素和最后一个元素的下标
  vector<Point> p(n);      // p[i]为q[i]和q[i+1]的交点
  vector<Line> q(n);       // 双端队列
  vector<Point> ans;       // 结果

  q[first = last = 0] = L[0]; // 双端队列初始化为只有一个半平面L[0]
  for (int i = 1; i < n; i++) {
    while (first < last && !OnLeft(L[i], p[last - 1])) last--;
    while (first < last && !OnLeft(L[i], p[first])) first++;
    q[++last] = L[i];
    if (fabs(Cross(q[last].v, q[last - 1].v)) < eps) { // 两向量平行且同向，取内侧的一个
      last--;
      if (OnLeft(q[last], L[i].P)) q[last] = L[i];
    }
    if (first < last) p[last - 1] = GetLineIntersection(q[last - 1], q[last]);
  }
  while (first < last && !OnLeft(q[first], p[last - 1])) last--; // 删除无用平面
  if (last - first <= 1) return ans; // 空集
  p[last] = GetLineIntersection(q[last], q[first]); // 计算首尾两个半平面的交点

  // 从deque复制到输出中
  for (int i = first; i <= last; i++) ans.push_back(p[i]);
  return ans;
}

int main() {
  for (int n, x, y; scanf("%d", &n) == 1 && n;) {
    vector<Vector> p, v, normal;
    for (int i = 0; i < n; i++) scanf("%d%d", &x, &y), p.push_back(Point(x, y));
    if (PolygonArea(p) < 0) reverse(p.begin(), p.end());

    for (int i = 0; i < n; i++)
      v.push_back(p[(i + 1) % n] - p[i]), normal.push_back(Normal(v[i]));
    double left = 0, right = 20000;
    while (right - left > eps) {
      vector<Line> L;
      double mid = left + (right - left) / 2;
      for (int i = 0; i < n; i++) L.push_back(Line(p[i] + normal[i]*mid, v[i]));
      vector<Point> poly = HalfplaneIntersection(L);
      if (poly.empty()) right = mid; else left = mid;
    }
    printf("%.6lf\n", left);
  }
  return 0;
}
// 25877776	1396	Most Distant Point from the Sea	Accepted	C++	0.000	2020-12-23 06:47:13
```

## 例题9  正方形（Squares, Seoul 2009, UVa1453）

### 题目描述
平面上有n个轴对齐的正方形。每个正方形由其左下角坐标(x, y)和边长w确定（因此正方形的四个顶点分别为(x,y)、(x+w,y)、(x,y+w)、(x+w,y+w)）。求这些正方形所有顶点构成集合的直径（即最远点对的距离）。

输出直径的平方值。

**输入格式**：第一行是整数T（T ≤ 10），表示测试数据组数。每组数据第一行是整数n（1 ≤ n ≤ 100000），表示正方形数量。接下来n行，每行三个整数x y w（0 ≤ x, y, w ≤ 10000），分别表示正方形左下角的x、y坐标和边长。

**输出格式**：对于每组测试数据，输出一行整数，表示直径的平方。

### 解题思路
1. **顶点提取**：每个正方形贡献4个顶点：左下(x, y)、右下(x+w, y)、左上(x, y+w)、右上(x+w, y+w)。将所有4n个点收集起来。

2. **直径与凸包**：平面点集的直径一定在凸包上，且最远点对一定是对踵点。使用旋转卡壳（Rotating Calipers）算法求解。

3. **旋转卡壳**：
   - 先求所有点的凸包（Andrew算法）。
   - 用两条平行线夹住凸包，旋转平行线。
   - 对每条凸包边，找出与该边距离最远的对踵点。
   - 计算对踵点对的距离，取最大值。

4. **整数运算**：本题使用整数坐标，所有计算用整数完成，避免浮点误差。

### 算法方法
- **凸包**：Andrew算法，O(N log N)。
- **旋转卡壳**：对凸包的每条边，寻找与该边面积最大的对踵点。判断条件为叉积 `Cross(p[u+1]-p[u], p[v+1]-p[v]) ≤ 0`（意味着对踵点不再增加）。
- **距离平方**：直接使用整数平方和`Dist2`避免开方。

### 复杂度分析
- **时间复杂度**：O(N log N)。凸包构造O(N log N)，旋转卡壳O(N)。N = 4n，最多400000。
- **空间复杂度**：O(N)，存储顶点和凸包。

```cpp
// 例题9  正方形（Squares, Seoul 2009, UVa1453）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

struct Point {
  int x, y;
  Point(int x = 0, int y = 0) : x(x), y(y) {}
};

typedef Point Vector;
istream& operator>>(istream& is, Point& p) { return is >> p.x >> p.y; }
ostream& operator<<(ostream& os, const Point& p) {
  return os << p.x << " " << p.y;
}

Vector operator-(const Point& A, const Point& B) {
  return Vector(A.x - B.x, A.y - B.y);
}
int Cross(const Vector& A, const Vector& B) { return A.x * B.y - A.y * B.x; }
int Dot(const Vector& A, const Vector& B) { return A.x * B.x + A.y * B.y; }
int Dist2(const Point& A, const Point& B) {
  return (A.x - B.x) * (A.x - B.x) + (A.y - B.y) * (A.y - B.y);
}
bool operator<(const Point& p1, const Point& p2) {
  return p1.x < p2.x || (p1.x == p2.x && p1.y < p2.y);
}
bool operator==(const Point& p1, const Point& p2) {
  return p1.x == p2.x && p1.y == p2.y;
}

vector<Point> ConvexHull(vector<Point>& p) {  // 点集凸包
  sort(p.begin(), p.end());                   // 预处理，删除重复点
  p.erase(unique(p.begin(), p.end()), p.end());

  int n = p.size();
  int m = 0;
  vector<Point> ch(n + 1);
  for (int i = 0; i < n; i++) {
    while (m > 1 && Cross(ch[m - 1] - ch[m - 2], p[i] - ch[m - 2]) <= 0) m--;
    ch[m++] = p[i];
  }
  int k = m;
  for (int i = n - 2; i >= 0; i--) {
    while (m > k && Cross(ch[m - 1] - ch[m - 2], p[i] - ch[m - 2]) <= 0) m--;
    ch[m++] = p[i];
  }
  if (n > 1) m--;
  ch.resize(m);
  return ch;
}

int diameter2(vector<Point>& points) {  // 返回点集直径的平方
  vector<Point> p = ConvexHull(points);
  int n = p.size();
  if (n == 1) return 0;
  if (n == 2) return Dist2(p[0], p[1]);
  p.push_back(p[0]);  // 免得取模
  int ans = 0;
  for (int u = 0, v = 1; u < n; u++) {
    for (;;) {  // 一条直线贴住边p[u]-p[u+1]
      // 当Area(p[u], p[u+1], p[v+1]) <= Area(p[u], p[u+1], p[v])时停止旋转
      // 即Cross(p[u+1]-p[u], p[v+1]-p[u]) - Cross(p[u+1]-p[u], p[v]-p[u]) <= 0
      // 根据Cross(A,B) - Cross(A,C) = Cross(A,B-C)
      // 化简得Cross(p[u+1]-p[u], p[v+1]-p[v]) <= 0
      int diff = Cross(p[u + 1] - p[u], p[v + 1] - p[v]);
      if (diff <= 0) {
        ans = max(ans, Dist2(p[u], p[v]));  // u和v是对踵点
        if (diff == 0)
          ans = max(ans, Dist2(p[u], p[v + 1]));  // diff == 0时u和v+1也是对踵点
        break;
      }
      v = (v + 1) % n;
    }
  }
  return ans;
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T;
  cin >> T;
  for (int t = 0, n; t < T; t++) {
    cin >> n;
    vector<Point> ps;
    for (int i = 0, x, y, w; i < n; i++) {
      cin >> x >> y >> w;
      ps.push_back(Point(x, y)), ps.push_back(Point(x + w, y));
      ps.push_back(Point(x, y + w)), ps.push_back(Point(x + w, y + w));
    }
    printf("%d\n", diameter2(ps));
  }
  return 0;
}
// 25845984 1453 Squares Accepted C++ 0.130 2020-12-14 06:26:23
```
