# 6.4 几何专题

计算几何是算法竞赛中的重要专题，涉及点、线、多边形、圆、空间变换等多种几何对象的计算。本章涵盖了从二维到三维的多个经典几何问题。

## LA2397/UVa1060 Collecting Luggage

### 题目描述
在一个凸多边形（n ≤ 100）的行李传送带上，一件行李以恒定速度vl沿多边形边界顺时针运行。人站在起点startp处，以恒定速度vp沿直线跑动（可以穿过多边形内部但不能穿过边界）。人在时刻0从起点出发，行李也在时刻0从多边形上某点出发。问人最早能在什么时刻拿到行李。

人和行李都在同一平面内移动，人需要走到行李所在位置。求最早相遇时间，输出格式为`Time = M:SS`（四舍五入到秒）。

### 解题思路
使用二分答案 + 最短路的方法：
1. **二分时间t**：判断人在时刻t是否能拿到行李
2. **行李位置**：根据t计算行李在传送带上的位置（使用弧长参数化）
3. **构图**：多边形顶点 + 人起点 + 行李位置作为节点，若两点间连线不穿过多边形边界且不穿过内部，则连边（边权为欧氏距离）
4. **Dijkstra最短路**：从起点到行李位置的最短距离是否≤ vp×t

"不穿过多边形内部"的判断：
- 线段不能和多边形的边规范相交
- 线段的中点不应在多边形内部
- 线段上不能有中间节点（即直接连接两节点的线段）

### 算法方法
**二分答案 + Dijkstra最短路 + 计算几何**：
- 几何判定函数：`isBlocked(a,b)`判断两个节点间是否可以直接走
- 行李位置计算：通过弧长参数化（`fmod(vl×t, perimeter)`）
- 二分终止条件：四舍五入到秒（当L和R的秒数相同时停止）

### 复杂度分析
- **时间复杂度**：O(log(T/eps) × (n³))，每次check需要O(n²)建图+O(n²log n) Dijkstra。log约30次迭代
- **空间复杂度**：O(n²)，邻接表存储图

```cpp
// LA2397/UVa1060 Collecting Luggage
// Rujia Liu
// 题目：取行李 - 人在凸多边形传送带旁，二分答案+Dijkstra求最早相遇时间
#include<cstdio>
#include<cstdlib>
#include<cmath>
#include<cstring>
#include<vector>
#include<queue>
#include<algorithm>
using namespace std;

const double eps = 1e-10;
// 浮点数比较：0=相等, 1=大于, -1=小于
int dcmp(double x) {
  if(fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}

// 二维点/向量
struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

// 向量运算
Vector operator + (const Vector& A, const Vector& B) { return Vector(A.x+B.x, A.y+B.y); }
Vector operator - (const Point& A, const Point& B) { return Vector(A.x-B.x, A.y-B.y); }
Vector operator * (const Vector& A, double p) { return Vector(A.x*p, A.y*p); }

bool operator < (const Point& a, const Point& b) {
  return a.x < b.x || (a.x == b.x && a.y < b.y);
}

bool operator == (const Point& a, const Point &b) {
  return dcmp(a.x-b.x) == 0 && dcmp(a.y-b.y) == 0;
}

// 向量点积和叉积
double Dot(const Vector& A, const Vector& B) { return A.x*B.x + A.y*B.y; }
double Cross(const Vector& A, const Vector& B) { return A.x*B.y - A.y*B.x; }
double Length(Vector A) { return sqrt(Dot(A, A)); }

// 判断线段a1-a2和b1-b2是否规范相交（端点不算）
bool SegmentProperIntersection(const Point& a1, const Point& a2, const Point& b1, const Point& b2) {
  double c1 = Cross(a2-a1, b1-a1), c2 = Cross(a2-a1, b2-a1),
         c3 = Cross(b2-b1, a1-b1), c4 = Cross(b2-b1, a2-b1);
  return dcmp(c1)*dcmp(c2) < 0 && dcmp(c3)*dcmp(c4) < 0;  // 严格异侧
}

// 判断点p是否在线段a1-a2上（不含端点）
bool OnSegment(const Point& p, const Point& a1, const Point& a2) {
  return dcmp(Cross(a1-p, a2-p)) == 0 && dcmp(Dot(a1-p, a2-p)) < 0;
}

// 射线法判断点是否在多边形内
// 返回值：-1=边界上, 1=内部, 0=外部
int isPointInPolygon(const Point& p, Point* poly, int n){
  int wn = 0;  // 绕数
  for(int i = 0; i < n; i++){
    const Point& p1 = poly[i];
    const Point& p2 = poly[(i+1)%n];
    if(p1 == p || p2 == p || OnSegment(p, p1, p2)) return -1;  // 在边界上
    int k = dcmp(Cross(p2-p1, p-p1));
    int d1 = dcmp(p1.y - p.y);
    int d2 = dcmp(p2.y - p.y);
    if(k > 0 && d1 <= 0 && d2 > 0) wn++;
    if(k < 0 && d2 <= 0 && d1 > 0) wn--;
  }
  if(wn != 0) return 1;  // 内部
  return 0;  // 外部
}

const int maxn = 100 + 10;
const int INF = 1000000000;

// 图的边
struct Edge {
  int from, to;
  double dist;
};

// 优先队列节点
struct HeapNode {
  double d;
  int u;
  bool operator < (const HeapNode& rhs) const {
    return d > rhs.d;  // 小顶堆
  }
};

// Dijkstra最短路算法
struct Dijkstra {
  int n, m;
  vector<Edge> edges;
  vector<int> G[maxn];  // G[i]存储以i为起点的边在edges中的下标
  bool done[maxn];      // done[i]=已确定最短路
  double d[maxn];       // d[i]=从起点到i的最短距离
  int p[maxn];          // p[i]=最短路上到达i的边编号

  void init(int n) {
    this->n = n;
    for(int i = 0; i < n; i++) G[i].clear();
    edges.clear();
  }

  void AddEdge(int from, int to, double dist) {
    edges.push_back((Edge){from, to, dist});
    m = edges.size();
    G[from].push_back(m-1);
  }

  void dijkstra(int s) {
    priority_queue<HeapNode> Q;
    for(int i = 0; i < n; i++) d[i] = INF;
    d[s] = 0;
    memset(done, 0, sizeof(done));
    Q.push((HeapNode){0, s});
    while(!Q.empty()) {
      HeapNode x = Q.top(); Q.pop();
      int u = x.u;
      if(done[u]) continue;
      done[u] = true;
      for(int i = 0; i < G[u].size(); i++) {
        Edge& e = edges[G[u][i]];
        if(d[e.to] > d[u] + e.dist) {
          d[e.to] = d[u] + e.dist;
          p[e.to] = G[u][i];
          Q.push((HeapNode){d[e.to], e.to});
        }
      }
    }
  }
};

int n;
Point startp, belt[maxn];  // belt[0..n-1]=多边形顶点, belt[n]=起点, belt[n+1]=行李位置
double vl, vp, perimeter, len[maxn];  // len[i]=边i的长度
Dijkstra solver;

// 判断节点a和b之间是否能直接走（不被多边形挡住）
bool isBlocked(int a, int b) {
  // 检查1：线段上不能有其他节点（即a-b不能穿越banana节点）
  for(int i = 0; i < n+2; i++)
    if(i != a && i != b && OnSegment(belt[i], belt[a], belt[b])) return true;
  // 检查2：线段不能和多边形的边规范相交
  for(int i = 0; i < n; i++)
    if(SegmentProperIntersection(belt[i], belt[(i+1)%n], belt[a], belt[b])) return true;
  // 检查3：线段的中点不能在多边形内部
  Point midp = (belt[a] + belt[b]) * 0.5;
  if(isPointInPolygon(midp, belt, n) == 1) return true;
  return false;
}

// 判断是否可以在时刻t拿到行李
bool check(double t) {
  solver.init(n+2);  // 0~n-1=传送带顶点, n=起点, n+1=行李位置

  // 计算行李在时刻t的位置（弧长参数化）
  double dist = fmod(vl * t, perimeter);  // 模周长取余
  for(int i = 0; i < n; i++) {
    if(len[i] >= dist) {
      // 行李在边i上，距离起点为dist的位置
      belt[n+1] = belt[i] + (belt[(i+1)%n] - belt[i]) * (dist / len[i]);
      break;
    }
    dist -= len[i];
  }

  // 构图：添加所有可行边
  for(int i = 0; i < n+2; i++)
    for(int j = i+1; j < n+2; j++) {
      double d = Length(belt[i] - belt[j]);
      if(d > eps && isBlocked(i, j)) continue;  // 被挡住的边不添加
      solver.AddEdge(i, j, d);
      solver.AddEdge(j, i, d);
    }
  solver.dijkstra(n);  // 以起点为源
  return solver.d[n+1] <= vp * t;  // 最短路距离 ≤ 人能走的距离
}

// 将小数时间转换为秒（四舍五入）
int getSecond(double t) {
  return (int)floor(t * 60 + 0.5);
}

int main() {
  int kase = 0;
  while(scanf("%d", &n) == 1 && n > 0) {
    // 读入多边形顶点
    for(int i = 0; i < n; i++) scanf("%lf%lf", &belt[i].x, &belt[i].y);
    scanf("%lf%lf%lf%lf", &startp.x, &startp.y, &vl, &vp);
    // 计算周长和边长度
    perimeter = 0;
    double closest = 1e9;
    for(int i = 0; i < n; i++) {
      closest = min(closest, Length(startp - belt[i]));  // 人到最近顶点的距离
      len[i] = Length(belt[i] - belt[(i+1)%n]);
      perimeter += len[i];
    }
    belt[n] = startp;  // 起点作为节点n

    // 二分搜索时间
    // 上界：人走到最近顶点再走半周长的时间（最坏情况）
    double L = 0, R = (closest + perimeter / 2) / vp;
    // 当L和R四舍五入到"秒"不同时继续二分
    while(getSecond(L) != getSecond(R)) {
      double M = L + (R-L)/2;
      if(check(M)) R = M; else L = M;
    }
    int t = getSecond(L);
    printf("Case %d: Time = %d:%02d\n", ++kase, t / 60, t % 60);
  }
  return 0;
}
// 25878459	1060	Collecting Luggage	Accepted	C++	0.200	2020-12-23 09:19:12
```

## LA3532/UVa1367 Nuclear Plants

### 题目描述
在一个N×M的矩形场地上，要建设核电站。有两种核电站：
- 小型电站（ks个）：影响半径为0.58
- 大型电站（kl个）：影响半径为1.31

任意两个电站不能建在同一位置。求在所有电站的圆形影响范围之外的场地区域的总面积。

### 解题思路
这是一个求多个圆的并集在矩形范围内的面积的经典问题。使用**一般曲边图形面积算法**：

所求图形（不能种菜的区域，即圆的影响区域与矩形相交部分）的边界由**圆弧**和**直线段**构成。使用格林公式的离散形式：对于每条边界段a→b，累加：
- `Cross(a, b) / 2`：直线段a→b左边的面积
- `r² × (θ - sinθ) / 2`：圆弧段对应的弓形面积

边界确定：
1. **圆弧部分**：每个圆被其他圆和矩形边界分割成若干弧段，找到中点不在其他圆内且在矩形内的弧段
2. **直线段部分**：矩形四条边被圆分割成若干段，找到中点在某圆内部的线段

### 算法方法
**曲边图形面积算法（格林公式）**：
- `getCircleCircleIntersection()`：计算圆-圆交点极角
- `getLineCircleIntersection()`：计算直线-圆交点极角
- `visible()`：判断弧中点是否在所求图形边界上
- 排序各分割点，遍历相邻区间，判断中点可见性
- 用极角参数化圆弧，积分计算扇/弓形面积

### 复杂度分析
- **时间复杂度**：O(n³)，每个圆的交点数量O(n)，排序O(n log n)，共O(n²)。n = ks+kl
- **空间复杂度**：O(n)，存储交点和分割点

```cpp
// LA3532/UVa1367 Nuclear Plants
// 刘汝佳
// 题目：核电站 - 求多个圆在矩形范围内的并集面积
#include<cstdio>
#include<cmath>
#include<cstring>
#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

const double eps = 5 * 1e-13;
int dcmp(double x) {
  if(fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}

const double PI = acos(-1);
const double TWO_PI = PI * 2;

// 将角度规范化到[center-PI, center+PI)范围内
double NormalizeAngle(double rad, double center = PI) {
  return rad - TWO_PI * floor((rad + PI - center) / TWO_PI);
}

// 二维点/向量
struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

Vector operator + (Vector A, Vector B) { return Vector(A.x+B.x, A.y+B.y); }
Vector operator - (Point A, Point B) { return Vector(A.x-B.x, A.y-B.y); }
Vector operator * (Vector A, double p) { return Vector(A.x*p, A.y*p); }
Vector operator / (Vector A, double p) { return Vector(A.x/p, A.y/p); }

// 字典序比较（不严格偏序，需保证无三点近似共线的情况）
bool operator < (const Point& a, const Point& b) {
  return dcmp(a.x - b.x) < 0 || (dcmp(a.x - b.x) == 0 && dcmp(a.y - b.y) < 0);
}

bool operator == (Point A, Point B) {
  return dcmp(A.x - B.x) == 0 && dcmp(A.y - B.y) == 0;
}

double Dot(Vector A, Vector B) { return A.x*B.x + A.y*B.y; }
double Length(Vector A) { return sqrt(Dot(A, A)); }
double Cross(Vector A, Vector B) { return A.x*B.y - A.y*B.x; }

double angle(Vector v) {
  return atan2(v.y, v.x);
}

bool OnSegment(const Point& p, const Point& a1, const Point& a2) {
  return dcmp(Cross(a1-p, a2-p)) == 0 && dcmp(Dot(a1-p, a2-p)) < 0;
}

// 计算圆c1(r1)和圆c2(r2)的交点相对于c1圆心的极角
void getCircleCircleIntersection(Point c1, double r1, Point c2, double r2, vector<double>& rad) {
  double d = Length(c1 - c2);
  if(dcmp(d) == 0) return;  // 同心圆/重合
  if(dcmp(r1 + r2 - d) < 0) return;  // 外离
  if(dcmp(fabs(r1-r2) - d) > 0) return;  // 内含

  double a = angle(c2 - c1);  // c2相对于c1的极角
  double da = acos((r1*r1 + d*d - r2*r2) / (2*r1*d));
  rad.push_back(NormalizeAngle(a-da));
  rad.push_back(NormalizeAngle(a+da));
}

// 点P到直线AB的投影
Point GetLineProjection(Point P, Point A, Point B) {
  Vector v = B-A;
  return A + v * (Dot(v, P-A) / Dot(v, v));
}

// 直线AB和圆心C、半径r的圆的交点（相对于圆心的极角）
void getLineCircleIntersection(Point A, Point B, Point C, double r, vector<double>& rad){
  Point p = GetLineProjection(C, A, B);  // 圆心到直线的投影
  double a = angle(p - C);               // 投影点相对于圆心的极角
  double d = Length(p - C);              // 圆心到直线的距离
  if(dcmp(d - r) > 0) return;           // 不相交
  if(dcmp(d) == 0) {
    // 过圆心
    rad.push_back(NormalizeAngle(angle(A - B)));
    rad.push_back(NormalizeAngle(angle(B - A)));
  }
  double da = acos(d / r);  // 半张角
}

/////////// 题目相关
const int maxn = 200 + 5;
int n, N, M;  // n=圆总数, N×M=场地大小
Point P[maxn];  // 圆心坐标
double R[maxn]; // 圆的半径

// 获取圆no上极角为rad的点的坐标
Point getPoint(int no, double rad) {
  return Point(P[no].x + cos(rad)*R[no], P[no].y + sin(rad)*R[no]);
}

// 判断第no个圆的极角rad处的点是否在"所见图形"的边界上
// （即该点不在场地外、不在其他圆内，且相同圆只取编号最小的）
bool visible(int no, double rad) {
  Point p = getPoint(no, rad);
  if(p.x < 0 || p.y < 0 || p.x > N || p.y > M) return false;  // 在场地外
  for(int i = 0; i < n; i++) {
    // 相同圆心和半径的圆，只保留编号最小的
    if(P[no] == P[i] && dcmp(R[no] - R[i]) == 0 && i < no) return false;
    // 在其他圆内部
    if(dcmp(Length(p - P[i]) - R[i]) < 0) return false;
  }
  return true;
}

// 判断场地边界上的点p是否在"所见图形"外部
bool visible(Point p) {
  for(int i = 0; i < n; i++) {
    if(dcmp(Length(p - P[i]) - R[i]) <= 0) return false;  // 在某圆内部
  }
  return true;
}

// 求圆的并在(0,0)-(N,M)内的面积（不能种菜的区域）
// 使用一般曲边图形的面积算法。所求图形的边界由圆弧和直线段构成。
// 算法：对于边界上的每一段a→b，累加Cross(a,b)/2（直线段贡献）
//      和 r²×(θ-sinθ)/2（圆弧段贡献）
double getArea() {
  Point b[4];  // 矩形四个顶点
  b[0] = Point(0, 0);
  b[1] = Point(N, 0);
  b[2] = Point(N, M);
  b[3] = Point(0, M);
  double area = 0;

  // 第一部分：圆弧边界
  for(int i = 0; i < n; i++) {
    vector<double> rad;
    rad.push_back(0);       // 极角起点
    rad.push_back(PI*2);    // 极角终点

    // 圆与矩形边界的交点
    for(int j = 0; j < 4; j++)
      getLineCircleIntersection(b[j], b[(j+1)%4], P[i], R[i], rad);

    // 圆与圆的交点
    for(int j = 0; j < n; j++)
      getCircleCircleIntersection(P[i], R[i], P[j], R[j], rad);
    
    sort(rad.begin(), rad.end());
    // 遍历相邻极角区间
    for(int j = 0; j < rad.size()-1; j++) 
      if(rad[j+1] - rad[j] > eps) {
        double mid = (rad[j] + rad[j+1]) / 2.0;  // 弧中点极角
        if(visible(i, mid)) {
          // 圆弧在图形边界上，累加贡献
          area += Cross(getPoint(i, rad[j]), getPoint(i, rad[j+1])) / 2.0;
          double a = rad[j+1] - rad[j];
          area += R[i] * R[i] * (a - sin(a)) / 2.0;  // 弓形面积
        }
      }
  }

  // 第二部分：直线段边界（矩形四条边在圆内部的线段）
  for(int i = 0; i < 4; i++) {
    Vector v = b[(i+1)%4] - b[i];
    double len = Length(v);

    vector<double> dist;  // 边界上分割点到起点的距离
    dist.push_back(0);
    dist.push_back(len);
    for(int j = 0; j < n; j++) {
      vector<double> rad;
      getLineCircleIntersection(b[i], b[(i+1)%4], P[j], R[j], rad);
      for(int k = 0; k < rad.size(); k++) {
        Point p = getPoint(j, rad[k]);
        dist.push_back(Length(p - b[i]));
      }
    }

    sort(dist.begin(), dist.end());
    vector<Point> points;
    for(int j = 0; j < dist.size(); j++)
      points.push_back(b[i] + v * (dist[j] / len));

    // 遍历相邻线段
    for(int j = 0; j < dist.size()-1; j++) {
      Point midp = (points[j] + points[j+1]) / 2.0;
      // 线段中点在圆内部→该线段在图形边界上
      if(!visible(midp)) area += Cross(points[j], points[j+1]) / 2.0;
    }
  }

  return N*M - area;  // 场地总面积减去不能种菜的区域
}

int main() {
  int ks, kl;
  while(scanf("%d%d%d%d", &N, &M, &ks, &kl) == 4 && N && M) {
    // 读入小型电站
    for(int i = 0; i < ks; i++) { scanf("%lf%lf", &P[i].x, &P[i].y); R[i] = 0.58; }
    sort(P, P+ks);  // 去重（同一位置）
    ks = unique(P, P+ks) - P;
    // 读入大型电站
    for(int i = 0; i < kl; i++) { scanf("%lf%lf", &P[ks+i].x, &P[ks+i].y); R[ks+i] = 1.31; }
    sort(P+ks, P+ks+kl);  // 去重
    n = unique(P+ks, P+ks+kl) - P;
    printf("%.2lf\n", getArea());
  }
  return 0;
}
// Accepted 220ms 5686 C++5.3.0 2020-12-14 15:34:52 25846126
```

## LA3809/UVa1065 Raising the Roof

### 题目描述
给定n个三维点（n ≤ 300）和m个三角形（m ≤ 1000），三角形由三个顶点编号指定（编号从1到n）。这些三角形构成了一个"屋顶"曲面（多面体表面），保证三角形之间不相交（至少在原空间中）。求该屋顶曲面在XY平面上的投影面积（考虑重叠部分只算一次，取z最高的三角形）。

### 解题思路
这是三维空间到二维平面的投影面积计算。核心思想是将三维三角形投影到XY平面后，使用**扫描线算法**计算"取最高处"的投影面积。

1. **X方向离散化**：收集所有三角形边的投影交点的X坐标，排序去重
2. **扫描线**：在相邻X坐标之间，问题退化为计算二维"y-z"条带中，取最高的投影线段
3. **Y方向遍历**：对每条扫描线，计算穿过该线的三角形边的Y坐标，按Y递增处理事件
4. **确定最高三角形**：在每个Y区间内确定z最高的三角形编号
5. **面积累加**：该区间的实际投影面积 = 投影梯形面积 × 面积比例系数（area_ratio）

面积比例系数：`area_ratio = |法向量| / |法向量.z|`，用于从投影面积还原实际曲面面积。

### 算法方法
**三维扫描线算法**：
- 离散化X坐标 → 扫描线处理
- 每条扫描线计算穿过的三角形边 → Y事件排序
- 事件处理：进入/离开三角形，维护"inside"集合
- 在Y区间内确定z最高的三角形 → 累加面积
- 面积比例还原

### 复杂度分析
- **时间复杂度**：O(m² + m log m × 离散区间数)，最坏O(m² log m)
- **空间复杂度**：O(m)，存储三角形和事件

```cpp
// LA3809/UVa1065 Raising the Roof
// Rujia Liu
// 题目：屋顶面积 - 三维三角形集在XY平面投影的"最高处"曲面面积
#include <cmath>
#include <cstdio>
#define REP(i, n) for (int i = 0; i < (n); ++i)

const double eps = 1e-8;
int dcmp(double x) {
  if (fabs(x) < eps) return 0;
  return x < 0 ? -1 : 1;
}

// 三维点（使用整数坐标，减少精度误差）
struct Point3 {
  int x, y, z;
  Point3(int x = 0, int y = 0, int z = 0) : x(x), y(y), z(z) {}
};

typedef Point3 Vector3;

Vector3 operator-(const Point3& A, const Point3& B) {
  return Vector3(A.x - B.x, A.y - B.y, A.z - B.z);
}

int Dot(const Vector3& A, const Vector3& B) {
  return A.x * B.x + A.y * B.y + A.z * B.z;
}
double Length(const Vector3& A) { return sqrt(Dot(A, A)); }

// 三维叉积
Vector3 Cross(const Vector3& A, const Vector3& B) {
  return Vector3(A.y * B.z - A.z * B.y, A.z * B.x - A.x * B.z,
                 A.x * B.y - A.y * B.x);
}

#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <vector>
using namespace std;

const int maxn = 300 + 10, maxt = 1000 + 10;
Point3 p[maxn];         // 顶点坐标（编号1~n）
int n, m;               // n=顶点数, m=三角形数
int t[maxt][3];         // t[i][0..2]=三角形i的三个顶点编号
Vector3 normal[maxt];   // 三角形i的法向量
double d[maxt];         // 三角形i的点法式常数：Dot(normal[i], p) = d
double area_ratio[maxt]; // 面积比例系数：|normal| / |normal.z|

// 初始化：计算每个三角形的法向量和参数
// 忽略竖直平面内的三角形（normal.z==0），因其投影面积为0
void init() {
  for (int i = 0; i < m; i++) {
    Point3 p0 = p[t[i][0]], p1 = p[t[i][1]], p2 = p[t[i][2]];
    normal[i] = Cross(p1 - p0, p2 - p0);
    d[i] = Dot(normal[i], p0);
    if (normal[i].z != 0)
      area_ratio[i] = fabs((double)Length(normal[i]) / normal[i].z);
  }
}

// 计算三角形idx在(x,y)处的z坐标（通过平面方程反解）
inline double getTriangleZ(int idx, double x, double y) {
  return (d[idx] - normal[idx].x * x - normal[idx].y * y) / normal[idx].z;
}

// Y方向事件：某三角形的一条边与扫描线x=xx的交点
struct Event {
  int id;     // 三角形编号
  double y;   // 交点的y坐标
  Event(int id, double y) : id(id), y(y) {}
  bool operator<(const Event& rhs) const { return y < rhs.y; }
};

// 主算法：计算屋顶曲面的总投影面积
double solve() {
  // 第一步：离散化X坐标
  vector<double> sx;
  for (int i = 1; i <= n; i++) sx.push_back(p[i].x);
  
  // 收集所有三角形边在XY平面的投影的交点的X坐标
  REP(i, m) REP(j, m) REP(a, 3) REP(b, 3) {
    Point3 pa = p[t[i][a]], pb = p[t[i][(a + 1) % 3]];
    Point3 qa = p[t[j][b]], qb = p[t[j][(b + 1) % 3]];
    int dpx = pb.x - pa.x, dpy = pb.y - pa.y;
    int dqx = qb.x - qa.x, dqy = qb.y - qa.y;
    int deno = dpx * dqy - dpy * dqx;
    if (deno == 0) continue;  // 平行
    // 解参数方程求交点
    double t = (double)(dqy * (qa.x - pa.x) + dqx * (pa.y - qa.y)) / deno;
    double s = (double)(dpy * (qa.x - pa.x) + dpx * (pa.y - qa.y)) / deno;
    if (t > 1 || t < 0 || s > 1 || s < 0) continue;
    sx.push_back(pa.x + t * dpx);
  }
  
  sort(sx.begin(), sx.end());
  sx.erase(unique(sx.begin(), sx.end()), sx.end());  // 去重

  double ans = 0;
  
  // 第二步：在相邻X坐标之间进行扫描
  for (int i = 0; i < sx.size() - 1; i++) {
    double xx = (sx[i] + sx[i + 1]) / 2;  // 扫描线X坐标取中点
    
    // 收集所有穿过扫描线的三角形边的Y事件
    vector<Event> events;
    REP(j, m) if (normal[j].z != 0) REP(a, 3) {
      Point3 pa = p[t[j][a]], pb = p[t[j][(a + 1) % 3]];
      if (pa.x == pb.x) continue;  // 竖直线（投影到XY平面）
      if (!(min(pa.x, pb.x) <= sx[i] && max(pa.x, pb.x) >= sx[i + 1]))
        continue;  // 不在当前X条带内
      double y = pa.y + (pb.y - pa.y) * (xx - pa.x) / (pb.x - pa.x);
      events.push_back(Event(j, y));
    }
    if (events.empty()) continue;

    // 按Y递增处理事件（进入/离开三角形）
    int inside[maxt];  // inside[k]=1表示三角形k在扫描线上可见
    fill_n(inside, maxt, 0);
    sort(events.begin(), events.end());
    
    for (int j = 0; j < events.size() - 1; j++) {
      inside[events[j].id] ^= 1;  // 切换进入/离开状态
      if (fabs(events[j].y - events[j + 1].y) < eps)
        continue;  // Y相同的事件一起处理

      // 投影梯形的面积 = 宽 × 高
      double proj_are = (sx[i + 1] - sx[i]) * (events[j + 1].y - events[j].y);

      // 确定当前Y区间内z最高的三角形
      int top = -1;
      double topz = -1e9, yy = (events[j].y + events[j + 1].y) / 2;
      for (int k = 0; k < m; k++)
        if (inside[k]) {
          double zz = getTriangleZ(k, xx, yy);
          if (zz > topz) topz = zz, top = k;
        }

      // 累加面积（投影面积 × 比例系数 = 实际曲面面积）
      if (top >= 0) ans += area_ratio[top] * proj_are;
    }
  }
  return ans;
}

int main() {
  int kase = 0;
  while (scanf("%d%d", &n, &m) == 2 && n > 0) {
    for (int i = 1; i <= n; i++)
      scanf("%d%d%d", &p[i].x, &p[i].y, &p[i].z);
    for (int i = 0; i < m; i++)
      scanf("%d%d%d", &t[i][0], &t[i][1], &t[i][2]);
    init();
    double ans = solve();
    printf("Case %d: %.2lf\n\n", ++kase, ans);
  }
  return 0;
}
// Accepted 490ms 4467 C++ 5.3.0 2020-12-14 15:43:47O25846165
```

## LA4125/UVa1075 Painter

### 题目描述
给定n（n ≤ 100,000）个三角形，它们在XY平面上可能重叠。要求计算三角形的最大重叠深度（即某点最多被多少个三角形覆盖）。

三角形由三个整数坐标点给出（坐标范围为-100000到100000），三角形不会退化。

### 解题思路
使用**扫描线算法** + **multimap维护活跃三角形**：
1. 将三角形按X坐标排序产生"事件"（每个三角形的三个顶点都是事件）
2. 从左到右扫描，维护当前扫描线x=curx上与扫描线相交的三角形边的有序集合（按Y排序的multimap）
3. 每条扫描线上，按Y增序遍历三角形边：
   - 遇到三角形的最左点：插入两条边（左侧边和右侧边）
   - 遇到三角形的中间点：删除左腰边，插入底边
   - 遇到三角形的最右点：删除剩余两条边
4. 计算每条扫描线上的重叠深度：新插入边时更新深度（前驱的depth+1）
5. 同时检测三角形边是否相交（若相交则报告ERROR）

### 算法方法
**扫描线 + multimap维护Y排序**：
1. 事件排序：按X坐标递增，同X按顶点编号v递增（0=左点, 1=中点, 2=右点）
2. 深度计算：新插入的线段深度=前驱线段深度+1
3. 相交检测：插入时检查与前驱/后继是否相交；删除时检查前驱和后继是否相交
4. 边界虚拟线段：两个无限大的虚拟线段（Y=-INF和Y=+INF）作为边界

### 复杂度分析
- **时间复杂度**：O(n log n)，每个三角形插入/删除O(log n)（multimap操作），事件数3n
- **空间复杂度**：O(n)，存储三角形、事件和扫描线

```cpp
// LA4125/UVa1075 Painter
// 刘汝佳
// 题目：画家阴影 - 计算n个三角形在XY平面上的最大重叠深度
#include <cstdio>
#include <cstdlib>
#include <map>
#include<algorithm>
using namespace std;

typedef long long LL;

// 二维整数点
struct Point {
  int x, y;
  Point(int x = 0, int y = 0):x(x),y(y){}
  void read() { scanf("%d%d", &x, &y); }
  bool operator < (const Point& p) const {
    return x < p.x || x == p.x && y < p.y;
  }
  Point operator - (const Point& rhs) const {
    return Point(x - rhs.x, y - rhs.y);
  }
};

// 整数比较（符号函数）
int icmp(LL x) {
  if(x == 0) return 0;
  return x > 0 ? 1 : -1;
}

// 叉积（使用LL防止溢出）
inline LL Cross(Point p, Point p1, Point p2) {
  return (LL)(p1.x - p.x) * (LL)(p2.y - p.y) - (LL)(p1.y - p.y)*(LL)(p2.x - p.x);
}

// 线段相交判定（含端点）
// 包含快速排斥实验的优化
inline bool SegmentIntersection(const Point& a1, const Point& a2, const Point& b1, const Point& b2) {
  // 快速排斥实验
  if(min(a1.x, a2.x) > max(b1.x, b2.x)) return false;
  if(min(a1.y, a2.y) > max(b1.y, b2.y)) return false;
  if(max(a1.x, a2.x) < min(b1.x, b2.x)) return false;
  if(max(a1.y, a2.y) < min(b1.y, b2.y)) return false;
  // 跨立实验
  LL c1 = Cross(a1, a2, b1), c2 = Cross(a1, a2, b2);
  if(icmp(c1) * icmp(c2) > 0) return false;
  LL c3 = Cross(b1, b2, a1), c4 = Cross(b1, b2, a2);
  return icmp(c3) * icmp(c4) <= 0;
}

int curx;  // 当前扫描线X坐标
const double eps = 1e-6;

// 三角形的一条边（线段）
struct Segment {
  Point p1, p2;  // 端点
  int no;         // 所属三角形编号
  double d;       // 斜率
  Segment(Point p1, Point p2, int no):p1(p1),p2(p2),no(no) {
    d = (p2.y - p1.y) / (p2.x + eps - p1.x);
  }
  // 计算该线段在扫描线x=curx上的Y坐标
  double y() const { return p1.y + d * (curx + eps - p1.x); }
  // 按Y坐标排序（用于multimap）
  bool operator < (const Segment& rhs) const { return y() < rhs.y(); }
};

// 判断两条线段是否相交（跳过同三角形的边）
inline bool Intersect(const Segment& a, const Segment& b) {
  if(a.no == b.no) return false;
  return SegmentIntersection(a.p1, a.p2, b.p1, b.p2);
}

bool error;      // 是否检测到相交线段（应报ERROR）
int max_depth;   // 最大重叠深度

const int INF = 200000;

// 扫描线类
struct Scanline {
  multimap<Segment, int> line;  // 线段→深度映射
  typedef multimap<Segment, int>::iterator Pos;
  
  void init() {
    line.clear();
    // 添加两条虚拟边界线段，防止越界
    line.insert(make_pair(Segment(Point(-INF,-INF), Point(INF,-INF), -1), 1));
    line.insert(make_pair(Segment(Point(-INF, INF), Point(INF, INF), -1), 0));
  }
  
  inline Pos Prev(const Pos& p) const { return --Pos(p); }
  inline Pos Next(const Pos& p) const { return ++Pos(p); }
  
  // 插入线段s，深度为d。检测与相邻线段是否相交
  inline Pos Insert(const Segment& s, int d = 0) {
    Pos x = line.insert(make_pair(s, d));
    if(Intersect(x->first, Prev(x)->first) || Intersect(x->first, Next(x)->first))
      error = true;
    return x;
  }  
  
  // 删除迭代器x指向的线段。检测前驱和后继是否相交
  inline void Erase(const Pos& x) {
    if(Intersect(Prev(x)->first, Next(x)->first)) error = true;
    line.erase(x);
  }
} scanline;

// 三角形结构
struct Triangle {
  int no;       // 编号
  Point P[3];   // 三个顶点
  Scanline::Pos p12, p13, p23;  // 三条边的扫描线迭代器
  
  void read(int no) {
    this->no = no;
    for(int i = 0; i < 3; i++) scanf("%d%d", &P[i].x, &P[i].y);
    sort(P, P+3);  // 按X排序：P[0]最左, P[2]最右
  }
  
  // 更新x1（较低边）和x2（较高边）的深度
  void updateDepth(const Scanline::Pos& x1, Scanline::Pos& x2) {
    int d = scanline.Prev(x1)->second + 1;  // 深度=前驱深度+1
    max_depth = max(max_depth, d);          // 更新最大深度
    x1->second = d;      // 较低边设为d
    x2->second = d - 1;  // 较高边设为d-1
  }
  
  // 处理三角形的第v个顶点（0=左, 1=中, 2=右）
  void process(int v) {
    if(v == 0) {  // 左端点：插入左腰(P[0]→P[2])和右腰(P[0]→P[1])
      p12 = scanline.Insert(Segment(P[0], P[1], no));
      p13 = scanline.Insert(Segment(P[0], P[2], no));
      // 判断哪条边在扫描线上Y坐标较低，先更新低的
      scanline.Next(p12) == p13 ? updateDepth(p12, p13) : updateDepth(p13, p12);
    }
    else if(v == 1) {  // 中间点：删除左腰，插入底边(P[1]→P[2])
      p23 = scanline.Insert(Segment(P[1], P[2], no), p12->second);
      scanline.Erase(p12);
    }
    else {  // 右端点：删除剩余两条边
      scanline.Erase(p13);
      scanline.Erase(p23);
    }
  }
};

// 扫描线事件
struct Event {
  int x, t, v;  // X坐标, 三角形编号, 顶点编号(0/1/2)
  Event(){}
  Event(int x, int t, int v):x(x),t(t),v(v){}
  bool operator < (const Event& rhs) const {
    return x < rhs.x || x == rhs.x && v < rhs.v;  // 先X后顶点顺序
  }
};

const int maxn = 100000 + 10;
Triangle tri[maxn];
Event events[maxn*3];

int main() {
  int n, kase = 0;
  while(scanf("%d",&n) == 1 && n >= 0) {
    error = false;
    max_depth = 1;
    scanline.init();
    
    // 读入三角形并生成事件
    for(int i = 0; i < n; i++) {
      tri[i].read(i);
      for(int j = 0; j < 3; j++)
        events[i*3+j] = Event(tri[i].P[j].x, i, j);
    }
    sort(events, events + n*3);
    
    // 扫描线处理所有事件
    for(int i = 0; i < n*3; i++) {
      curx = events[i].x;
      tri[events[i].t].process(events[i].v);
      if(error) break;  // 检测到相交则停止
    }
    
    if(!error) printf("Case %d: %d shades\n", ++kase, max_depth);
    else printf("Case %d: ERROR\n", ++kase);
  }
  return 0;
}
// Accepted 710ms 4355 C++5.3.0 2020-12-14 15:46:00 25846168
```

## UVa1077 The Sky is the Limit

### 题目描述
给定n（n ≤ 100）座"山"，每座山是一个等腰三角形（底边在水平线y=0上），由底边中心X坐标、高度H和底边宽度B描述。山脉可能会重叠。求所有山的**上轮廓线**（从上方观察，可见的山体轮廓）的总长度。

### 解题思路
使用**扫描线 + 离散化**的方法：
1. **X坐标离散化**：收集所有山的顶点X坐标和三角形边之间的所有交点的X坐标
2. **排序去重**：得到所有需要计算的X位置
3. **扫描**：在每个离散X坐标处，计算该垂线与所有山的交点中最高的点的Y坐标
4. **累加长度**：相邻最高点之间的欧氏距离之和即为轮廓线长度

关键在于第一步：需要找到所有山的三角形边两两之间规范相交的交点，这些交点的X坐标也需要加入离散化集合，否则轮廓线在这些点处可能发生方向变化。

### 算法方法
**扫描线 + 交点枚举**：
- 离散化X坐标：顶点X + 三角形边交点X
- 扫描每个X截面：求该垂线与所有山边的最高交点
- 轮廓线长度：相邻截面最高点之间的折线段长度之和

### 复杂度分析
- **时间复杂度**：O(n² + n² log n)，n≤100。山边交点O(n²)=O(10000)，离散化O(n² log n)，扫描O(c×n)其中c为离散点数量O(n²)
- **空间复杂度**：O(n²)，存储离散X坐标

```cpp
// UVa1077 The Sky is the Limit
// 刘汝佳
// 题目：天际线 - 计算n座等腰三角形山脉的上轮廓线总长度
#include<cstdio>
#include<cmath>
#include<algorithm>
using namespace std;

const double eps = 1e-10;
int dcmp(double x) {
  if(fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}

struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

Vector operator + (const Vector& A, const Vector& B) { return Vector(A.x+B.x, A.y+B.y); }
Vector operator - (const Point& A, const Point& B) { return Vector(A.x-B.x, A.y-B.y); }
Vector operator * (const Vector& A, double p) { return Vector(A.x*p, A.y*p); }

bool operator < (const Point& a, const Point& b) {
  return a.x < b.x || (a.x == b.x && a.y < b.y);
}

bool operator == (const Point& a, const Point &b) {
  return dcmp(a.x-b.x) == 0 && dcmp(a.y-b.y) == 0;
}

double Dot(const Vector& A, const Vector& B) { return A.x*B.x + A.y*B.y; }
double Cross(const Vector& A, const Vector& B) { return A.x*B.y - A.y*B.x; }
double Length(const Vector& A) { return sqrt(Dot(A, A)); }

// 两条直线的交点
Point GetLineIntersection(const Point& P, const Vector& v, const Point& Q, const Vector& w) { 
  Vector u = P-Q;
  double t = Cross(w, u) / Cross(v, w);
  return P + v*t;
}

// 判断两线段是否规范相交
bool SegmentProperIntersection(const Point& a1, const Point& a2, const Point& b1, const Point& b2) {
  double c1 = Cross(a2-a1, b1-a1), c2 = Cross(a2-a1, b2-a1),
         c3 = Cross(b2-b1, a1-b1), c4 = Cross(b2-b1, a2-b1);
  return dcmp(c1)*dcmp(c2)<0 && dcmp(c3)*dcmp(c4)<0;
}

const int maxn = 100 + 10;
Point P[maxn], L[maxn][2][2];  // L[i][a][b]: 第i座山的第a条边(0=左边,1=右边)的第b个端点
double x[maxn*maxn];           // 离散化的X坐标

int main() {
  int n, kase = 0;
  while(scanf("%d", &n) == 1 && n) {
    int c = 0;
    for(int i = 0; i < n; i++) {
      double X, H, B;
      scanf("%lf%lf%lf", &X, &H, &B);
      // 山的三个顶点：左下角, 山顶, 右下角
      L[i][0][0] = Point(X - B*0.5, 0);   // 左下
      L[i][0][1] = L[i][1][0] = Point(X, H);  // 山顶
      L[i][1][1] = Point(X + B*0.5, 0);   // 右下
      
      // 收集三个顶点的X坐标
      x[c++] = X - B*0.5;  // 左下
      x[c++] = X;          // 山顶
      x[c++] = X + B*0.5;  // 右下
    }
    
    // 收集所有山边之间的交点
    for(int i = 0; i < n; i++) for(int a = 0; a < 2; a++)
      for(int j = i+1; j < n; j++) for(int b = 0; b < 2; b++) {
        Point P1 = L[i][a][0], P2 = L[i][a][1];
        Point P3 = L[j][b][0], P4 = L[j][b][1];
        if(SegmentProperIntersection(P1, P2, P3, P4))
          x[c++] = GetLineIntersection(P1, P2-P1, P3, P4-P3).x;
      }

    // 离散化：排序并去重
    sort(x, x+c);
    c = unique(x, x+c) - x;

    double ans = 0;
    Point lastp;
    // 在每个离散X坐标处计算最高点
    for(int k = 0; k < c; k++) {
      Point P(x[k], 0);        // 扫描线底部
      Vector V(0, 1);          // 方向：垂直向上
      double maxy = -1;
      
      // 找所有山在该垂线上的最高交点
      for(int i = 0; i < n; i++) for(int a = 0; a < 2; a++) {
        Point P1 = L[i][a][0], P2 = L[i][a][1];
        Point intersection = GetLineIntersection(P, V, P1, P2-P1);
        // 交点必须在三角形边的范围内
        if(dcmp(intersection.x - P1.x) >= 0 && dcmp(intersection.x - P2.x) <= 0)
          maxy = max(maxy, intersection.y);
      }
      
      Point newp(x[k], maxy);
      // 累加相邻最高点之间的距离（忽略y=0的底边部分）
      if(k > 0 && (dcmp(lastp.y) > 0 || dcmp(maxy) > 0))
        ans += Length(newp - lastp);
      lastp = newp;
    }

    printf("Case %d: %.0lf\n\n", ++kase, ans);
  }
  return 0;
}
// Accepted 10ms 2973 C++5.3.0 2020-12-1415:32:51 25846121
```

## LA5129/HDU3838 Affine Mess

### 题目描述
给定三个原始点A、B、C和三个变换后的点A'、B'、C'（均为整数坐标，xi,yi∈[-10,10]）。已知变换是一个仿射变换（affine transformation），即X方向：x' = s·x + d_x，Y方向：y' = s·y + d_y，其中s是缩放因子（整数），d_x, d_y是平移量。但注意旋转（旋转后取整）也可能发生。

具体来说，变换过程为：
1. 绕原点旋转θ角度（θ是{arctan(ry/rx) : rx,ry ∈ [-10,10]且互质}中的某个值）
2. 旋转后四舍五入取整（捕捉到整数坐标）
3. X和Y方向独立进行线性变换x'=s·x+dx, y'=s·y+dy

已知输入的三对点（原始点和变换后的点），但**对应关系未知**（即不知道哪个原始点变成了哪个变换后的点）。求可能的变换方案数。

### 解题思路
穷举法 + 线性方程求解：
1. **枚举旋转**：可能的旋转角度有80个（但旋转180度等价于缩放(-1,-1)，只需40个），每个角度计算旋转后的整数坐标（四舍五入）
2. **枚举对应关系**：3个点有3!=6种对应关系
3. **求解线性方程**：对X和Y方向独立求解s和d（已知p,s→x,d的对应关系）
   - 联立两个方程：(p-q)·s = x-y，解出s
   - 如果p=q则需要x=y，否则无解
   - 如果3个方程推出多个不同的s，矛盾
4. **计数**：X方向解数×Y方向解数=总解数

### 算法方法
**枚举验证**：
- 旋转角度集合：40个（10个ry∈[-10,10]，对应10个rx，以及对称情况）
- 旋转后取整：`floor(值 + 0.5)`
- 线性方程求解：`solve(p,q,r,x,y,z)`
  - 返回0=无解, 1=唯一解, 2=无穷多解

### 复杂度分析
- **时间复杂度**：O(40×6×3) = O(720)，枚举旋转×枚举排列×解线性方程
- **空间复杂度**：O(1)，常数空间

```cpp
// LA5129/HDU3838 Affine Mess
// 刘汝佳
// 题目：仿射变换 - 给定三点映射关系（对应未知），求可能的变换方案数
#include<cstdio>
#include<cmath>
#include<vector>
#include<algorithm>
using namespace std;

/*
  求解下列线性方程组的整数解个数：
  p*s + d = x
  q*s + d = y
  r*s + d = z
  其中s=缩放系数，d=平移量

  解法：联立(1)+(2)得 (p-q)*s = x-y
  i) p=q时必须有x=y，否则无解
  ii) p≠q时s=(x-y)/(p-q)，必须整除
  
  同理联立(2)+(3)和(3)+(1)
  i) 多个方程推出的s必须一致
  ii) 三个方程都等价→无穷多解(返回2)
  iii) s=0无解
*/
int solve(int p, int q, int r, int x, int y, int z) {
  int a[] = {p, q, r};
  int b[] = {x, y, z};
  vector<int> ans;
  for(int i = 0; i < 3; i++) {
    int P = a[i], Q = a[(i+1)%3], X = b[i], Y = b[(i+1)%3];
    if(P == Q) {
      if(X != Y) return 0;  // p=q但x≠y，无解
    }
    else if((X - Y) % (P - Q) != 0) return 0;  // 不能整除
    else ans.push_back((X - Y) / (P - Q));
  }
  if(ans.empty()) return 2;  // 三个方程等价，无穷多解
  sort(ans.begin(), ans.end());
  if(ans[0] != ans.back() || ans[0] == 0) return 0;  // s不一致或s=0
  return 1;
}

int x[3], y[3];    // 变换前的点
int x2[3], y2[3];  // 变换后的点
int ix[3], iy[3];  // 旋转+捕捉后的中间点

int main() {
  int kase = 0;
  for(;;) {
    int ok = 0;
    for(int i = 0; i < 3; i++) {
      scanf("%d%d", &x[i], &y[i]);
      if(x[i] != 0 || y[i] != 0) ok = 1;
    }
    if(!ok) break;  // 全0终止
    
    for(int i = 0; i < 3; i++) scanf("%d%d", &x2[i], &y2[i]);
    int ans = 0;  // 可行方案总数

    // 枚举旋转角度
    // 注意旋转180度等价于缩放(-1,-1)，所以只枚举40个方向（而非80个）
    for(int i = 0; i < 40; i++) {
      int rx, ry;  // 旋转方向向量
      if(i < 20) { rx = 10; ry = i - 10; }  // (10,-10)到(10,9)
      else { rx = 30 - i; ry = 10; }         // (10,10)到(-9,10)

      // 计算旋转后的坐标并取整（捕捉到整数格点）
      double len = sqrt(rx*rx + ry*ry);
      double cosa = rx / len;  // cos(θ)
      double sina = ry / len;  // sin(θ)
      int ix[3], iy[3];
      for(int j = 0; j < 3; j++) {
        // 旋转公式：(x',y') = (x·cos-y·sin, x·sin+y·cos)，然后四舍五入
        ix[j] = (int)floor(x[j] * cosa - y[j] * sina + 0.5);
        iy[j] = (int)floor(x[j] * sina + y[j] * cosa + 0.5);
      }

      // 枚举3个点的对应关系（6种排列）
      int p[3] = {0, 1, 2};
      do {
        int cnt1 = solve(ix[0], ix[1], ix[2], x2[p[0]], x2[p[1]], x2[p[2]]);
        int cnt2 = solve(iy[0], iy[1], iy[2], y2[p[0]], y2[p[1]], y2[p[2]]);
        ans += cnt1 * cnt2;  // X和Y方向独立，方案数相乘
      } while(next_permutation(p, p+3));
    }

    printf("Case %d: ", ++kase);
    if(ans == 0) printf("no solution\n");
    else if(ans == 1) printf("equivalent solutions\n");
    else printf("inconsistent solutions\n");
  }
  return 0;
}
```

## UVa12303 Composite Transformations

### 题目描述
给定n个三维点（n ≤ 50,000）和m个平面（m ≤ 50,000），以及T个三维空间变换操作（T ≤ 500）。变换操作有三种：
- `T a b c`：平移(a, b, c)
- `S a b c`：缩放(a, b, c)
- `R a b c theta`：绕方向向量(a,b,c)旋转theta度

要求将所有点和所有平面对应用所有变换操作（按顺序），输出变换后的点坐标和平面方程的系数。

### 解题思路
使用**4×4齐次变换矩阵**统一处理所有变换：
- **点变换**：将点(x,y,z)表示为齐次坐标(x,y,z,1)，左乘变换矩阵
- **平面变换**：平面ax+by+cz+d=0需要特殊处理——在平面上取三个不共线的点，分别变换，再用变换后的三点重新确定平面方程

每种基本变换都对应一个4×4矩阵：
- **平移**：单位矩阵 + v[0][3]=a, v[1][3]=b, v[2][3]=c
- **缩放**：v[0][0]=a, v[1][1]=b, v[2][2]=c
- **旋转**：罗德里格斯旋转公式的矩阵形式

利用矩阵乘法的结合律，先计算所有变换的复合矩阵mat = M[T-1]×...×M[0]，然后一次性应用于所有点和平面。

### 算法方法
**齐次坐标 + 4×4变换矩阵**：
1. 构建每种基本变换的4×4矩阵
2. 矩阵连乘得到复合变换矩阵
3. 点变换：P' = mat × (P,1)
4. 平面变换：采样三个点变换后重组平面方程

### 复杂度分析
- **时间复杂度**：O(T + n + m)，T次矩阵乘法O(1)，n次点变换O(n)，m×3次点变换O(m)
- **空间复杂度**：O(n+m)，存储点和平面

```cpp
// UVa12303 Composite Transformations
// 刘汝佳
// 题目：复合三维变换 - 使用4×4齐次变换矩阵统一处理平移、缩放、旋转
#include<cstdio>
#include<cmath>
#include<cstdlib>
#include<cstring>
#include<cassert>
using namespace std;

const double PI = acos(-1.0);

// 三维点/向量
struct Point3 {
  double x, y, z;
  Point3(double x=0, double y=0, double z=0):x(x),y(y),z(z) { }
};

typedef Point3 Vector3;

Vector3 operator + (const Vector3& A, const Vector3& B) {
  return Vector3(A.x+B.x, A.y+B.y, A.z+B.z);
}

Vector3 operator - (const Point3& A, const Point3& B) {
  return Vector3(A.x-B.x, A.y-B.y, A.z-B.z);
}

Vector3 operator * (const Vector3& A, double p) {
  return Vector3(A.x*p, A.y*p, A.z*p);
}

Vector3 operator / (const Vector3& A, double p) {
  return Vector3(A.x/p, A.y/p, A.z/p);
}

double Dot(const Vector3& A, const Vector3& B) { return A.x*B.x + A.y*B.y + A.z*B.z; }
double Length(const Vector3& A) { return sqrt(Dot(A, A)); }
Vector3 Cross(const Vector3& A, const Vector3& B) {
  return Vector3(A.y*B.z - A.z*B.y, A.z*B.x - A.x*B.z, A.x*B.y - A.y*B.x);
}

// 三维平面：ax + by + cz + d = 0
struct Plane {
  double a, b, c, d;
  Plane() {}
  
  // 用三点确定平面（三点不共线）
  Plane(Point3* P) {
    Vector3 V = Cross(P[1]-P[0], P[2]-P[0]);  // 法向量
    V = V / Length(V);  // 单位化
    a = V.x; b = V.y; c = V.z;
    d = -Dot(V, P[0]);  // d = -(a·x0 + b·y0 + c·z0)
  }
  
  // 在平面上随机采样一个点（用于变换后重建平面）
  Point3 sample() const {
    double v1 = rand() / (double)RAND_MAX;
    double v2 = rand() / (double)RAND_MAX;
    if(a != 0) return Point3(-(d+v1*b+v2*c)/a, v1, v2);
    if(b != 0) return Point3(v1, -(d+v1*a+v2*c)/b, v2);
    if(c != 0) return Point3(v1, v2, -(d+v1*a+v2*b)/c);
    assert(0);  // 非法平面
  }
};

// 4×4齐次变换矩阵
struct Matrix4x4 {
  double v[4][4];

  // 矩阵乘法
  inline Matrix4x4 operator * (const Matrix4x4 &rhs) const {
    Matrix4x4 ans;   
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++) {
            ans.v[i][j] = 0;
            for (int k = 0; k < 4; k++)
                ans.v[i][j] += v[i][k] * rhs.v[k][j];
        }
    return ans;
  }

  // 变换点：右乘列向量(x, y, z, 1}
  inline Point3 transform(Point3 P) const {
    double p[4] = {P.x, P.y, P.z, 1}, ans[4] = {0};
    for(int i = 0; i < 4; i++)
      for(int k = 0; k < 4; k++)
        ans[i] += v[i][k] * p[k];
    return Point3(ans[0], ans[1], ans[2]);  // ans[3]应为1
  }

  // 初始化为单位矩阵
  void loadIdentity() {
    memset(v, 0, sizeof(v));
    v[0][0] = v[1][1] = v[2][2] = v[3][3] = 1;
  }

  // 平移矩阵：T(a,b,c)
  void loadTranslate(double a, double b, double c) {
    loadIdentity();
    v[0][3] = a; v[1][3] = b; v[2][3] = c;
  }

  // 缩放矩阵：S(a,b,c)
  void loadScale(double a, double b, double c) {
    loadIdentity();
    v[0][0] = a; v[1][1] = b; v[2][2] = c;
  }

  // 旋转矩阵：绕单位方向向量L旋转deg度
  // 使用罗德里格斯旋转公式（Rodrigues' rotation formula）
  void loadRotation(double a, double b, double c, double deg) {
    loadIdentity();
    double rad = deg / 180 * PI;
    double sine = sin(rad), cosine = cos(rad);
    Vector3 L(a, b, c);
    L = L / Length(L);  // 归一化方向向量
    // 罗德里格斯公式的矩阵形式：
    // R = cosθ·I + (1-cosθ)·L·L^T + sinθ·[L]×
    v[0][0] = cosine + L.x * L.x * (1.0 - cosine);
    v[0][1] = L.x * L.y * (1 - cosine) - L.z * sine;
    v[0][2] = L.x * L.z * (1 - cosine) + L.y * sine;
    v[1][0] = L.y * L.x * (1 - cosine) + L.z * sine;
    v[1][1] = cosine + L.y * L.y * (1 - cosine);
    v[1][2] = L.y * L.z * (1 - cosine) - L.x * sine;
    v[2][0] = L.z * L.x * (1 - cosine) - L.y * sine;
    v[2][1] = L.z * L.y * (1 - cosine) + L.x * sine;
    v[2][2] = cosine + L.z * L.z * (1 - cosine);
  }
};

const int maxn = 50000 + 10;
const int maxp = 50000 + 10;
Point3 P[maxn];        // 原始点
Plane planes[maxp];    // 原始平面

int main() {
  int n, m, T;
  scanf("%d%d%d", &n, &m, &T);
  
  // 读入点
  for(int i = 0; i < n; i++)
    scanf("%lf%lf%lf", &P[i].x, &P[i].y, &P[i].z);
  // 读入平面
  for(int i = 0; i < m; i++)
    scanf("%lf%lf%lf%lf", &planes[i].a, &planes[i].b, &planes[i].c, &planes[i].d);

  // 计算复合变换矩阵
  // P' = M[T-1] × ... × M[1] × M[0] × P
  // 利用结合律：mat = M[T-1] × ... × M[0]，然后P' = mat × P
  Matrix4x4 mat;
  mat.loadIdentity();
  for(int i = 0; i < T; i++) {
    char op[100];
    double a, b, c, theta;
    scanf("%s%lf%lf%lf", op, &a, &b, &c);
    Matrix4x4 M;
    if(op[0] == 'T') M.loadTranslate(a, b, c);
    else if(op[0] == 'S') M.loadScale(a, b, c);
    else if(op[0] == 'R') { scanf("%lf", &theta); M.loadRotation(a, b, c, theta); }
    mat = M * mat;  // 注意左乘顺序：后面的变换在左边
  }

  // 变换所有点
  for(int i = 0; i < n; i++) {
    Point3 ans = mat.transform(P[i]);
    printf("%.2lf %.2lf %.2lf\n", ans.x, ans.y, ans.z);
  }
  
  // 变换所有平面
  // 平面不能直接左乘变换矩阵，需要在平面上采3个点变换后重新计算
  for(int i = 0; i < m; i++) {
    Point3 A[3];
    for(int j = 0; j < 3; j++) A[j] = mat.transform(planes[i].sample());
    Plane pl(A);  // 用变换后的三点重建平面
    printf("%.2lf %.2lf %.2lf %.2lf\n", pl.a, pl.b, pl.c, pl.d);
  }
  return 0;
}
// Accepted 70ms 4465 C++5.3.0 2020-12-14 15:31:02 25846118
```
