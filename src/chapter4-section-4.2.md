# 4.2 与圆和球有关的计算问题

> **学习目标**：将圆与直线的几何问题转化为一元二次方程求解，掌握判别式与参数方程的计算框架

## 理论基础

### 为什么需要学这个？

圆看起来很简单——一个中心一个半径，画出来就是那个完美的曲线。但一旦遇到"求圆与直线的交点"、"判断两个圆的位置关系"、甚至"给一个定点和两条直线，求一个和它们都相切的圆"这类问题，几何直观就不够用了。你总不能拿着圆规和直尺在草稿纸上画吧？

好在数学已经帮我们准备好了工具：参数方程和二次方程。直线上的点可以表示成 `P + t*v`，圆上的点满足 `(x - cx)² + (y - cy)² = r²`，把前者代入后者就得到了一个关于参数 `t` 的一元二次方程。解出 `t`，交点就到手了。这个"代入—展开—用判别式"的三步套路，几乎能处理所有涉及圆的几何问题。

学完这一节，你会发现：那些看起来复杂的圆问题，不过是二次方程求根的一个包装罢了。

### 核心概念

**1. 圆与直线的交点 — 判别式 Δ**

直线参数式 `P + t*V` 代入圆方程 `|P + t*V - C|² = r²`，展开得 `e*t² + f*t + g = 0`，其中 `e = |V|²`，`f = 2*V·(P-C)`，`g = |P-C|² - r²`。

```cpp
double a = L.v.x, b = L.p.x - C.c.x, c = L.v.y, d = L.p.y - C.c.y;
double e = a*a + c*c, f = 2*(a*b + c*d), g = b*b + d*d - C.r*C.r;
double delta = f*f - 4*e*g;
if (dcmp(delta) < 0) return 0;        // Δ < 0 → 相离
if (dcmp(delta) == 0) {               // Δ = 0 → 相切
    t1 = t2 = -f/(2*e); sol.push_back(L.point(t1)); return 1;
}
// Δ > 0 → 两个交点
t1 = (-f - sqrt(delta))/(2*e); sol.push_back(L.point(t1));
t2 = (-f + sqrt(delta))/(2*e); sol.push_back(L.point(t2)); return 2;
```

判别式是灵魂：**Δ 的正负直接决定了位置关系**。不用画图，不用量距离，一个 `delta` 就告诉你一切。

**2. 两圆的交点与位置关系**

两圆的距离判断更直观——直接比较圆心距和半径：
```
圆心距 d = Length(C1.c - C2.c)
d > r1+r2  → 相离（两圆不相交）
d < |r1-r2| → 内含（一个圆完全在另一个内部）
d == 0 且 r1==r2 → 重合
```
求交点时，用余弦定理计算偏移角 `da = acos((r1² + d² - r2²) / (2*r1*d))`，从圆心连线极角 `a` 出发，向两侧偏转 `a ± da` 即得两个交点。

**两圆位置关系的五种分类**：设两圆半径分别为 r1 ≥ r2，圆心距为 d。位置关系由 d 与 r1±r2 的大小关系精确决定：① **外离**：d > r1+r2，两圆无公共点，且一个圆完全在另一个圆外部；② **外切**：d = r1+r2，两圆恰好在一个点接触（外部相切）；③ **相交**：|r1-r2| < d < r1+r2，两圆有两个交点；④ **内切**：d = |r1-r2|（且 d > 0），一圆内切于另一圆内部；⑤ **内含**：0 ≤ d < |r1-r2|，一圆完全包含在另一圆内部且无交点，特别地 d=0 且 r1=r2 时两圆重合。五种关系的判别本质上是二次方程判别式在不同区间上的退化——当 d 从大到小变化时，两圆交点从 0 个变为 2 个再变为 0 个。

**公切线数量与两圆位置的关系**：两圆的公切线条数完全由位置关系决定：外离时 4 条（2 条外公切线 + 2 条内公切线），外切时 3 条（2 条外公切线 + 1 条内公切线退化为过切点的公切线），相交时 2 条（仅外公切线），内切时 1 条（仅 1 条外公切线），内含时 0 条（无公切线）。记忆口诀："外离四，外切三，相交二，内切一，内含零"。求外公切线的关键是将小圆半径 r2 替换为 r1-r2，从大圆圆心向"缩小的圆"引切线——由此将两圆公切线转化为点与圆的切线问题。

**3. 切线与弧长**

过圆外一点 P 到圆的切线：切点、圆心、给定点构成直角三角形。切线方向与圆心-P 连线的夹角 `ang = asin(r / dist)`，切线方向就是 `Rotate(u, ±ang)`。弧长 = `r * rad`（弧度制下的圆心角乘以半径），扇形面积 = `r² * rad / 2`。公切线的切点计算本质上就是解圆与偏移后直线的交点问题——将直线向法向量方向平移 r 或 -r 即可。

**4. 三角形外接圆半径公式 R = abc / (4S) 的推导**

这个优雅的公式是竞赛中手算外接圆半径的利器。推导步骤：设三角形三边长为 a、b、c，面积为 S。由正弦定理 `a / sinA = 2R`，得 `sinA = a / (2R)`。代入面积公式 `S = (1/2)bc·sinA`，消去 sinA 得 `S = (1/2)bc · a/(2R) = abc / (4R)`，整理即得 `R = abc / (4S)`。这个推导的关键洞察是：外接圆半径 R 是沟通"边"（a、b、c）与"面积"（S）的桥梁——正弦定理把 R 和边联系起来，面积公式把边和角联系起来，两者结合消去角度便得到纯边与面积的 R 表达式。在程序中，S 可以通过三边长的海伦公式 `S = √(p(p-a)(p-b)(p-c))`（其中 `p = (a+b+c)/2`）来求，也可以用叉积面积公式。

### 知识脉络

```
直线参数方程 P+t*V
    ├── 代入圆方程 → 一元二次 → 判别式 Δ 判位置（相离/相切/两交点）
    ├── 两圆判断：圆心距直接比较半径关系
    │       └── 余弦定理求交点极角偏移 da
    └── 切线：asin(r/dist) 求夹角方向，直线平移 r 求相切圆
```

### 快速上手模板

```cpp
struct Line {
    Point p; Vector v;
    Point point(double t) const { return p + v * t; }
    Line move(double d) const {  // 沿法向量平移 d（用于处理相切条件）
        return Line(p + Normal(v)*d, v);
    }
};

struct Circle {
    Point c; double r;
    Point point(double a) const  // 圆上极角为 a 的点
    { return Point(c.x+cos(a)*r, c.y+sin(a)*r); }
};

// 直线与圆求交 — 基于判别式 Δ，返回交点数 (0/1/2)
int getLineCircleIntersection(const Line& L, const Circle& C,
                               double& t1, double& t2, vector<Point>& sol);

// 圆与圆求交 — 基于余弦定理的极角偏移，返回交点数 (-1重合/0/1/2)
int getCircleCircleIntersection(const Circle& C1, const Circle& C2,
                                 vector<Point>& sol);

// 过定点作圆的切线 — asin(r/dist) 求夹角
int getTangents(const Point& p, const Circle& C, Vector* v);
```

这两个求交函数是本章解决所有圆相关问题的核心工具。遇到"求交点"的问题，先判断该用直线参数式还是余弦定理法。

**本书跨章节连接**：圆的判别式方法本质上是将几何问题代数化——用二次方程的判别式代替"画图和量距离"的直觉判断，这与第 4.1 节的向量代数风格一脉相承。涉及二分答案的判定型问题（如"存在某个距离 d 满足条件"）时，圆问题常与第 4.3 节的**半平面交+二分**组合出现——将约束转化为半平面后用二分内切圆半径来判定。公切线的计算依赖于第 4.1 节中的向量旋转和法向量操作。
## 例题4  二维几何110合一！（2D Geometry 110 in 1!, UVa12304）

### 题目描述
实现二维计算几何中的6个基本操作，接受命令式输入并输出结果。6个子问题涵盖了圆与三角形、圆与点、圆与直线、圆与圆之间的各种基本几何关系。

**子问题列表**：
1. **CircumscribedCircle**：给定三角形三个顶点，求其外接圆的圆心和半径。
2. **InscribedCircle**：给定三角形三个顶点，求其内切圆的圆心和半径。
3. **TangentLineThroughPoint**：给定一个圆和圆外一点，求过该点作圆的两条切线的角度（以度为单位，范围为[0, 180)）。
4. **CircleThroughAPointAndTangentToALineWithRadius**：给定一点、一直线和半径r，求所有满足"过该点且与定直线相切、半径为r"的圆的圆心坐标。
5. **CircleTangentToTwoLinesWithRadius**：给定两条直线和半径r，求所有满足"与两条直线都相切、半径为r"的圆的圆心坐标。
6. **CircleTangentToTwoDisjointCirclesWithRadius**：给定两个不相交的圆和半径r，求所有满足"与两个圆都外切、半径为r"的圆的圆心坐标。

**输入格式**：每行以命令字符串开头，后跟对应参数。所有点坐标和半径均为浮点数。输入以EOF结束。最多约110个命令。命令与参数格式：
- `CircumscribedCircle x1 y1 x2 y2 x3 y3`
- `InscribedCircle x1 y1 x2 y2 x3 y3`
- `TangentLineThroughPoint xc yc r xp yp`
- `CircleThroughAPointAndTangentToALineWithRadius xp yp x1 y1 x2 y2 r`
- `CircleTangentToTwoLinesWithRadius x1 y1 x2 y2 x3 y3 x4 y4 r`
- `CircleTangentToTwoDisjointCirclesWithRadius x1 y1 r1 x2 y2 r2 r`

**输出格式**：每种命令有对应的输出格式，使用`[...]`包裹列表，元素之间用逗号分隔，浮点数保留6位小数。

### 解题思路
这是一个综合性的二维几何工具集，将6个基本几何问题统一到一个框架中：

1. **外接圆**：三角形三条边的垂直平分线交于一点（外心）。通过解两条垂直平分线的交点得到圆心，半径为圆心到任意顶点的距离。使用代数方法：设三角形顶点相对于p1的坐标为(Bx, By)和(Cx, Cy)，通过垂直平分线方程解出圆心坐标。

2. **内切圆**：三角形三个角的平分线交于一点（内心）。内心到三边距离相等，即内切圆半径。内切圆圆心坐标可表示为三角形的加权重心：`(a*A + b*B + c*C) / (a+b+c)`，其中a、b、c为对边长度。

3. **过定点作圆的切线**：利用反正弦函数 `asin(r/d)` 计算切线方向与圆心-定点连线的夹角，然后旋转得到两条切线方向。

4. **过定点且与定直线相切、半径为r的圆**：将直线向两侧平移r，问题转化为求以定点为圆心、r为半径的圆与平移后直线的交点。

5. **与两条直线相切、半径为r的圆**：将两条直线各自向两侧平移r，求平移后四条直线的两两交点，共最多4个解。

6. **与两圆外切、半径为r的圆**：将两圆半径各增加r，求两扩大后圆的交点。若不相交则无解。

### 算法方法
- **圆/直线结构体**：封装圆（圆心+半径）和直线（点+方向向量）的基本操作，如直线的平移、圆上点的参数表示等。
- **直线与圆求交**：联立参数方程和圆的方程，化为一元二次方程求解，用判别式delta判断交点数。
- **圆与圆求交**：利用余弦定理计算交点的极角偏移量，然后从圆心极角出发得到交点坐标。
- **直线平移**：沿法向量方向平移直线，用于处理相切条件。

### 复杂度分析
- **时间复杂度**：每个子问题O(1)，所有操作均为常数时间的几何计算（解二次方程、反三角函数等）。总复杂度O(Q)，Q为命令数（≤110）。
- **空间复杂度**：O(1)，每个命令只需常数空间存储临时结果。

```cpp
// 例题4  二维几何110合一！（2D Geometry 110 in 1!, UVa12304）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

const double eps = 1e-6;
int dcmp(double x) {
  if (fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}

const double PI = acos(-1);

struct Point {
  double x, y;
  Point(double x = 0, double y = 0): x(x), y(y) { }
  Point& operator=(const Point& p) {
    x = p.x, y = p.y;
    return *this;
  }
};
istream& operator>>(istream& is, Point& p) { return is >> p.x >> p.y; }
typedef Point Vector;

Vector operator + (const Vector& A, const Vector& B) { return Vector(A.x + B.x, A.y + B.y); }
Vector operator - (const Point& A, const Point& B) { return Vector(A.x - B.x, A.y - B.y); }
Vector operator * (const Vector& A, double p) { return Vector(A.x * p, A.y * p); }
Vector operator / (const Vector& A, double p) { return Vector(A.x / p, A.y / p); }
bool operator < (const Point& a, const Point& b) {
  return a.x < b.x || (a.x == b.x && a.y < b.y);
}
bool operator == (const Point& a, const Point &b) {
  return dcmp(a.x - b.x) == 0 && dcmp(a.y - b.y) == 0;
}
double Dot(const Vector& A, const Vector& B) { return A.x * B.x + A.y * B.y; }
double Length(const Vector& A) { return sqrt(Dot(A, A)); }
double Angle(const Vector& A, const Vector& B) { return acos(Dot(A, B) / Length(A) / Length(B)); }
double Cross(const Vector& A, const Vector& B) { return A.x * B.y - A.y * B.x; }
Vector Rotate(const Vector& A, double rad) {
  return Vector(A.x * cos(rad) - A.y * sin(rad), A.x * sin(rad) + A.y * cos(rad));
}
Vector Normal(const Vector& A) {
  double L = Length(A);
  return Vector(-A.y / L, A.x / L);
}
Point GetLineIntersection(const Point& P, const Point& v, const Point& Q, const Point& w) {
  Vector u = P - Q;
  double t = Cross(w, u) / Cross(v, w);
  return P + v * t;
}
// 求点P到直线AB的垂足
Point GetLineProjection(const Point& P, const Point& A, const Point& B) {
  Vector v = B - A;                                        // 直线方向向量
  return A + v * (Dot(v, P - A) / Dot(v, v));              // 参数t = (v·AP) / (v·v)
}
double DistanceToLine(const Point& P, const Point& A, const Point& B) {
  Vector v1 = B - A, v2 = P - A;
  return fabs(Cross(v1, v2)) / Length(v1); // 如果不取绝对值，得到的是有向距离
}

// 直线结构体：p为直线上一点，v为方向向量
struct Line {
  Point p;
  Vector v;
  Line(const Point& p, const Vector& v): p(p), v(v) { }
  Point point(double t) const {        // 直线上参数为t的点
    return p + v * t;
  }
  Line move(double d) const {          // 将直线沿法向量方向平移d
    return Line(p + Normal(v) * d, v); // Normal(v)是v的单位法向量
  }
};

// 圆结构体：c为圆心，r为半径
struct Circle {
  Point c;
  double r;
  Circle(const Point& c, double r): c(c), r(r) {}
  Point point(double a) const {        // 圆上极角为a的点
    return Point(c.x + cos(a) * r, c.y + sin(a) * r);
  }
};

Point GetLineIntersection(const Line& a, const Line& b) {
  return GetLineIntersection(a.p, a.v, b.p, b.v);
}

double angle(const Vector& v) {
  return atan2(v.y, v.x);
}

// 求直线L与圆C的交点，返回交点数(0/1/2)，参数t1,t2存储交点参数值，sol存储交点坐标
int getLineCircleIntersection(const Line& L, const Circle& C, double& t1, double& t2, vector<Point>& sol) {
  double a = L.v.x, b = L.p.x - C.c.x, c = L.v.y, d = L.p.y - C.c.y;
  // 联立直线参数方程和圆方程：|L.p + t*L.v - C.c|² = C.r²
  // 展开得 e*t² + f*t + g = 0
  double e = a * a + c * c, f = 2 * (a * b + c * d), g = b * b + d * d - C.r * C.r;
  double delta = f * f - 4 * e * g; // 判别式
  if (dcmp(delta) < 0) return 0; // 相离，无交点
  if (dcmp(delta) == 0) { // 相切，一个交点
    t1 = t2 = -f / (2 * e); sol.push_back(L.point(t1));
    return 1;
  }
  // 相交，两个交点
  t1 = (-f - sqrt(delta)) / (2 * e); sol.push_back(L.point(t1));
  t2 = (-f + sqrt(delta)) / (2 * e); sol.push_back(L.point(t2));
  return 2;
}

// 求圆C1与圆C2的交点，返回交点数（-1表示重合，0/1/2）
int getCircleCircleIntersection(const Circle& C1, const Circle& C2, vector<Point>& sol) {
  double d = Length(C1.c - C2.c);  // 圆心距
  if (dcmp(d) == 0) {               // 同心圆
    if (dcmp(C1.r - C2.r) == 0) return -1; // 重合，无穷多交点
    return 0;                       // 内含，无交点
  }
  if (dcmp(C1.r + C2.r - d) < 0) return 0;       // 相离
  if (dcmp(fabs(C1.r - C2.r) - d) > 0) return 0; // 内含

  double a = angle(C2.c - C1.c);                    // 圆心连线的极角
  // 利用余弦定理求交点的极角偏移量
  double da = acos((C1.r * C1.r + d * d - C2.r * C2.r) / (2 * C1.r * d));
  Point p1 = C1.point(a - da), p2 = C1.point(a + da);

  sol.push_back(p1);
  if (p1 == p2) return 1;  // 相切
  sol.push_back(p2);
  return 2;                 // 两交点
}

/******************* Problem 1 **********************/
// 求三角形的外接圆
Circle CircumscribedCircle(const Point& p1, const Point& p2, const Point& p3) {
  double Bx = p2.x - p1.x, By = p2.y - p1.y;  // p2相对于p1的坐标
  double Cx = p3.x - p1.x, Cy = p3.y - p1.y;  // p3相对于p1的坐标
  double D = 2 * (Bx * Cy - By * Cx);          // 行列式的2倍
  // 解垂直平分线方程得到圆心坐标（相对于p1的偏移+ p1的坐标）
  double cx = (Cy * (Bx * Bx + By * By) - By * (Cx * Cx + Cy * Cy)) / D + p1.x;
  double cy = (Bx * (Cx * Cx + Cy * Cy) - Cx * (Bx * Bx + By * By)) / D + p1.y;
  Point p = Point(cx, cy);                    // 外心坐标
  return Circle(p, Length(p1 - p));            // 半径=外心到顶点距离
}

/******************* Problem 2 **********************/
// 求三角形的内切圆
Circle InscribedCircle(const Point& p1, const Point& p2, const Point& p3) {
  double a = Length(p2 - p3);  // p1对边（边p2p3）的长度
  double b = Length(p3 - p1);  // p2对边的长度
  double c = Length(p1 - p2);  // p3对边的长度
  // 内心坐标为加权重心：(a*A + b*B + c*C) / (a+b+c)，权重为对边长度
  Point p = (p1 * a + p2 * b + p3 * c) / (a + b + c);
  return Circle(p, DistanceToLine(p, p1, p2));  // 半径=内心到任一边的距离
}

/******************* Problem 3 **********************/
// 过点p到圆C的切线。v[i]是第i条切线的向量。返回切线条数
int getTangents(const Point& p, const Circle& C, Vector* v) {
  Vector u = C.c - p;                        // 圆心指向定点p的反方向
  double dist = Length(u);                   // 点到圆心距离
  if (dist < C.r) return 0;                  // 点在圆内，无切线
  else if (dcmp(dist - C.r) == 0) {          // p在圆上，只有一条切线
    v[0] = Rotate(u, PI / 2);                // 切线方向=半径方向旋转90度
    return 1;
  } else {                                   // 点在圆外，有两条切线
    double ang = asin(C.r / dist);            // 切线方向与u的夹角
    v[0] = Rotate(u, -ang);                   // 第一条切线方向
    v[1] = Rotate(u, +ang);                   // 第二条切线方向
    return 2;
  }
}

/******************* Problem 4 **********************/
// 过定点且与定直线相切、半径为r的圆：求满足条件的圆心
vector<Point> CircleThroughPointTangentToLineGivenRadius(const Point& p, const Line& L, double r) {
  vector<Point> ans;
  double t1, t2;
  // 将直线向两侧平移r，与以p为圆心、r为半径的圆求交点
  // 平移后直线到原直线的距离=r，所以圆心到原直线距离也=r（相切）
  getLineCircleIntersection(L.move(-r), Circle(p, r), t1, t2, ans);
  getLineCircleIntersection(L.move(r), Circle(p, r), t1, t2, ans);
  return ans;
}

/******************* Problem 5 **********************/
// 与两条直线都相切、半径为r的圆：求满足条件的圆心
vector<Point> CircleTangentToLinesGivenRadius(const Line& a, const Line& b, double r) {
  vector<Point> ans;
  Line L1 = a.move(-r), L2 = a.move(r);  // a的两条平行线（距离±r）
  Line L3 = b.move(-r), L4 = b.move(r);  // b的两条平行线（距离±r）
  // 四条直线的两两交点即为圆心（因为圆心到每条直线距离=r）
  ans.push_back(GetLineIntersection(L1, L3));
  ans.push_back(GetLineIntersection(L1, L4));
  ans.push_back(GetLineIntersection(L2, L3));
  ans.push_back(GetLineIntersection(L2, L4));
  return ans;
}

/******************* Problem 6 **********************/
// 与两个不相交的圆外切、半径为r的圆：求满足条件的圆心
vector<Point> CircleTangentToTwoDisjointCirclesWithRadius(const Circle& c1, const Circle& c2, double r) {
  vector<Point> ans;
  Vector v = c2.c - c1.c;                          // 两圆圆心连线
  double dist = Length(v);                          // 圆心距
  // 外切条件：新圆心到两圆圆心距离分别为c1.r+r和c2.r+r
  // 即新圆心在以c1.c为圆心、c1.r+r为半径的圆1'和圆2'的交点上
  int d = dcmp(dist - c1.r - c2.r - r * 2);        // 判断圆1'和圆2'是否可能相交
  if (d > 0) return ans;                            // 两扩大圆相离，无解
  getCircleCircleIntersection(Circle(c1.c, c1.r + r), Circle(c2.c, c2.r + r), ans);
  return ans;
}

// 格式化输出函数
double lineAngleDegree(const Vector& v) {
  double ang = angle(v) * 180.0 / PI;    // 弧度转角度
  while (dcmp(ang) < 0) ang += 360.0;    // 保证非负
  while (dcmp(ang - 180) >= 0) ang -= 180.0;  // 映射到[0, 180)
  return ang;
}

void format(Circle c) {
  printf("(%.6lf,%.6lf,%.6lf)\n", c.c.x, c.c.y, c.r);  // 圆心和半径
}

void format(vector<double> ans) {  // 角度列表
  int n = ans.size();
  sort(ans.begin(), ans.end());    // 升序排列
  printf("[");
  if (n) {
    printf("%.6lf", ans[0]);
    for (int i = 1; i < n; i++) printf(",%.6lf", ans[i]);
  }
  printf("]\n");
}

void format(vector<Point> ans) {  // 点坐标列表
  int n = ans.size();
  sort(ans.begin(), ans.end());    // 按x后y升序排列
  printf("[");
  if (n) {
    printf("(%.6lf,%.6lf)", ans[0].x, ans[0].y);
    for (int i = 1; i < n; i++) printf(",(%.6lf,%.6lf)", ans[i].x, ans[i].y);
  }
  printf("]\n");
}

// 从两点构造直线
Line getLine(const Point& p1, const Point& p2) {
  return Line(p1, p2 - p1);  // p1为基准点，p2-p1为方向向量
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  for (string cmd; cin >> cmd;) {  // 循环读取命令
    double r1, r2, r;
    Point p1, p2, p3, p4, pc, pp;
    if (cmd == "CircumscribedCircle") {
      cin >> p1 >> p2 >> p3;
      format(CircumscribedCircle(p1, p2, p3));
    }
    if (cmd == "InscribedCircle") {
      cin >> p1 >> p2 >> p3;
      format(InscribedCircle(p1, p2, p3));
    }
    if (cmd == "TangentLineThroughPoint") {
      cin >> pc >> r >> pp;
      Vector v[2];                               // 存储切线方向向量
      vector<double> ans;                        // 存储切线角度
      int cnt = getTangents(pp, Circle(pc, r), v);  // 求切线条数
      for (int i = 0; i < cnt; i++) ans.push_back(lineAngleDegree(v[i]));  // 转为角度
      format(ans);                              // 排序后输出角度列表
    }
    if (cmd == "CircleThroughAPointAndTangentToALineWithRadius") {
      cin >> pp >> p1 >> p2 >> r;
      format(CircleThroughPointTangentToLineGivenRadius(pp, getLine(p1, p2), r));
    }
    if (cmd == "CircleTangentToTwoLinesWithRadius") {
      cin >> p1 >> p2 >> p3 >> p4 >> r;
      format(CircleTangentToLinesGivenRadius(getLine(p1, p2), getLine(p3, p4), r));
    }
    if (cmd == "CircleTangentToTwoDisjointCirclesWithRadius") {
      cin >> p1 >> r1 >> p2 >> r2 >> r;
      Circle c1(p1, r1), c2(p2, r2);
      format(CircleTangentToTwoDisjointCirclesWithRadius(c1, c2, r));
    }
  }
  return 0;
}
// 24480641 12304 2D Geometry 110 in 1! Accepted  C++11 0.000 2020-01-28 13:40:23
```

## 例题5  圆盘问题（Viva Confetti, Kanazawa 2002, UVa1308）

### 题目描述
有N个彩色圆形纸片，依次随机掉落平铺在桌面上。后落下的纸片会覆盖先落下的纸片。问从正上方俯视，能够看到多少种不同的颜色？即有多少个圆至少有一部分没有被后面的圆完全遮挡。

**输入格式**：输入包含多组测试数据，以N=0结束。每组第一行包含一个整数N（1 ≤ N ≤ 100），表示圆的数量。接下来N行，每行包含三个浮点数x y r，表示一个圆的圆心坐标和半径。圆的掉落顺序就是输入的顺序，即第1个最先落下，第N个最后落下。所有圆互不重合，圆心坐标和半径均为正数，绝对值不超过1000。

**输出格式**：对于每组测试数据，输出一行整数，表示能从上方看到的颜色数（即有多少个圆至少部分可见）。

### 解题思路
问题的核心是判断每个圆是否有部分没有被后面的圆遮挡。关键在于：只需要检查每个圆的圆弧段——如果某段圆环上没有被任何后落下的圆覆盖，则该圆可见。

1. **区间覆盖思想**：对于圆i，考虑其圆周上[0, 2π)的角度区间。圆j（j > i，即落在圆i之后）会遮住圆i的一部分圆弧。圆i与圆j的交点将圆周分割成若干弧段。

2. **获取所有分割点**：对于每个圆i，计算它与所有其他圆（包括前面的和后面的）的交点。每个交点对应圆i圆周上的一个极角。将这些极角排序，得到圆i被分割后的弧段列表。同时加入0和2π作为边界。

3. **检查弧段中点**：对于每个相邻极角之间的弧段，取其中点作为检测点。该点对应圆i圆周上的一个位置。为了检测该点是否被覆盖，稍微将该点向圆内和圆外偏移eps（处理边界情况），然后查询覆盖该点的最上层(topmost)圆。

4. **topmost查询**：对于给定点P，从最后一个圆（最上层）开始遍历，找到第一个包含P的圆。如果这个圆就是圆i自身，说明该弧段未被覆盖，圆i可见。

5. **去重**：使用vis数组标记哪些圆可见。

### 算法方法
- **圆与圆的交点（极角形式）**：计算圆i和圆j的交点在圆i圆周上对应的极角，使用余弦定理计算偏移角da，将a±da加入分割点列表。
- **角度归一化**：NormalizeAngle函数将角度归一化到[center-π, center+π)范围，避免角度跨过0/2π边界的问题。
- **弧段中点检测**：对每个分割后的弧段，取中点（mid = (rad[j] + rad[j+1])/2），分别在圆内(radius - eps)和圆外(radius + eps)检测，以处理边界重叠的情况。
- **贪心查询最上层圆**：从后往前遍历，找到第一个覆盖检测点的圆。

### 复杂度分析
- **时间复杂度**：O(N³)。外层遍历N个圆，每个圆要与N-1个其他圆求交点O(N²)。产生的分割点约O(N)个。对于每个分割点弧段，调用topmost需要O(N)时间。总计O(N²) × O(N) = O(N³)。N ≤ 100，约10⁶次操作。
- **空间复杂度**：O(N²)，主要存储每个圆的分割极角列表。最多100×200个极角点。

```cpp
// 例题5  圆盘问题（Viva Confetti, Kanazawa 2002, UVa1308）
// 陈锋
#include <cmath>
#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
using namespace std;

const double eps = 5 * 1e-13;               // 高精度浮点比较阈值
int dcmp(double x) {
  if (fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;  // 三态比较
}
const double PI = acos(-1), TWO_PI = PI * 2;  // π和2π

// 将角度rad归一化到[center-π, center+π)范围内
// center默认为π，即归一化到[0, 2π)
double NormalizeAngle(double rad, double center = PI) {
  return rad - TWO_PI * floor((rad + PI - center) / TWO_PI);
}
struct Point {
  double x, y;
  Point(double x = 0, double y = 0): x(x), y(y) { }
};

istream& operator>>(istream& is, Point& p) { return is >> p.x >> p.y; }

typedef Point Vector;
Vector operator + (const Vector& A, const Vector& B) { return Vector(A.x + B.x, A.y + B.y); }
Vector operator - (const Point&A, const Point&B) { return Vector(A.x - B.x, A.y - B.y); }
Vector operator * (const Vector& A, double p) { return Vector(A.x * p, A.y * p); }
Vector operator / (const Vector& A, double p) { return Vector(A.x / p, A.y / p); }
double Dot(const Vector& A, const Vector& B) { return A.x * B.x + A.y * B.y; }
double Length(const Vector& A) { return sqrt(Dot(A, A)); }
double angle(const Vector& v) { return atan2(v.y, v.x); }

// 求两圆交点相对于圆1圆心的极角，结果存入rad向量
void getCircleCircleIntersection(const Point&c1, double r1, const Point&c2, double r2, vector<double>& rad) {
  double d = Length(c1 - c2);                     // 圆心距
  if (dcmp(d) == 0) return; // 不管是内含还是重合，都不相交（同心圆无交点）
  if (dcmp(r1 + r2 - d) < 0) return;              // 相离
  if (dcmp(fabs(r1 - r2) - d) > 0) return;       // 内含
  double a = angle(c2 - c1);                       // 圆心连线的极角
  // 余弦定理求交点极角偏移量
  double da = acos((r1 * r1 + d * d - r2 * r2) / (2 * r1 * d));
  rad.push_back(NormalizeAngle(a - da));           // 交点1的极角
  rad.push_back(NormalizeAngle(a + da));           // 交点2的极角
}

const int maxn = 100 + 5;
int N;
Point center[maxn];      // 圆心数组
double radius[maxn];     // 半径数组
bool vis[maxn];          // 标记哪些圆可见

// 查询覆盖点p的最上层圆（即从最后一个掉落的圆往前查）
int topmost(const Point& p) {
  for (int i = N - 1; i >= 0; i--)                 // 从后往前（从上往下）
    if (Length(center[i] - p) < radius[i]) return i; // 点p在圆i内部
  return -1;                                        // 无圆覆盖此点
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  while (cin >> N && N) {
    for (int i = 0; i < N; i++)cin >> center[i] >> radius[i];  // 读入圆
    fill_n(vis, N + 1, 0);                                     // 初始化可见标记

    for (int i = 0; i < N; i++) {
      vector<double> rad; // 圆i的圆周被切割成的各个弧段的端点极角
      rad.push_back(0), rad.push_back(TWO_PI);  // 起点0和终点2π
      // 求圆i与其他所有圆的交点，分割圆周
      for (int j = 0; j < N; j++)
        getCircleCircleIntersection(center[i], radius[i], center[j], radius[j], rad);
      sort(rad.begin(), rad.end());             // 按极角升序排序

      for (size_t j = 0; j < rad.size(); j++) {
        double mid = (rad[j] + rad[j + 1]) / 2.0; // 圆弧中点相对于圆i圆心的极角
        for (int side = -1; side <= 1; side += 2) {
          // 往圆内(side=1即-eps)或圆外(side=-1即+eps)稍微偏移，检测弧段是否被覆盖
          double r2 = radius[i] - side * eps; // 往里面或者外面稍微一动一点点
          // 计算检测点的坐标（圆心 + 极角mid、半径r2）
          int t = topmost(Point(center[i].x + cos(mid) * r2, center[i].y + sin(mid) * r2));
          if (t >= 0) vis[t] = true;          // 标记覆盖该弧段的圆为可见
        }
      }
    }
    int ans = 0;
    for (int i = 0; i < N; i++) if (vis[i]) ans++;  // 统计可见圆数量
    cout << ans << "\n";
  }
  return 0;
}
// 25877748	1308	Viva Confetti	Accepted	C++	0.000	2020-12-23 06:39:24
```
