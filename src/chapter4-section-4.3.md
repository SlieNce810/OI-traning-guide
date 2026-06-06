# 4.3 二维几何常用算法

## 例题14  找边界（Find the Border, NEERC 2004, Codeforces Gym100536F）

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
  int n, m, face_cnt;
  double x[maxn], y[maxn];
  vector<Edge> edges;
  vector<int> G[maxn];
  int vis[maxn * 2]; // 每条边是否已经访问过
  int left[maxn * 2]; // 左面的编号
  int prev[maxn * 2]; // 相同起点的上一条边（即顺时针旋转碰到的下一条边）的编号

  vector<Polygon> faces;
  double area[maxn]; // 每个polygon的面积

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n; i++) G[i].clear();
    edges.clear();
    faces.clear();
  }

  // 有向线段from->to的极角
  double getAngle(int from, int to) {
    return atan2(y[to] - y[from], x[to] - x[from]);
  }

  void AddEdge(int from, int to) {
    edges.push_back((Edge) {from, to, getAngle(from, to)});
    edges.push_back((Edge) {to, from, getAngle(to, from)});
    m = edges.size();
    G[from].push_back(m - 2);
    G[to].push_back(m - 1);
  }

  // 找出faces并计算面积
  void Build() {
    for (int u = 0; u < n; u++) {
      // 给从u出发的各条边按极角排序
      int d = G[u].size();
      for (int i = 0; i < d; i++)
        for (int j = i + 1; j < d; j++) // 这里偷个懒，假设从每个点出发的线段不会太多
          if (edges[G[u][i]].ang > edges[G[u][j]].ang) swap(G[u][i], G[u][j]);
      for (int i = 0; i < d; i++)
        prev[G[u][(i + 1) % d]] = G[u][i];
    }

    memset(vis, 0, sizeof(vis));
    face_cnt = 0;
    for (int u = 0; u < n; u++)
      for (int i = 0; i < G[u].size(); i++) {
        int e = G[u][i];
        if (!vis[e]) { // 逆时针找圈
          face_cnt++;
          Polygon poly;
          for (;;) {
            vis[e] = 1; left[e] = face_cnt;
            int from = edges[e].from;
            poly.push_back(Point(x[from], y[from]));
            e = prev[e ^ 1];
            if (e == G[u][i]) break;
            assert(vis[e] == 0);
          }
          faces.push_back(poly);
        }
      }

    for (int i = 0; i < faces.size(); i++) {
      area[i] = PolygonArea(faces[i]);
    }
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
