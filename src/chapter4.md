# 第4章 几何问题

## 4.1 二维几何基础

### 例题2  好看的一笔画（That Nice Euler Circuit, Shanghai 2004, LA3263）

```cpp
// 例题2  好看的一笔画（That Nice Euler Circuit, Shanghai 2004, LA3263）
// 陈锋
#include <cmath>
#include <cstdio>
#include <iostream>
#include <vector>
#include <set>
using namespace std;
#define _for(i,a,b) for( int i=(a); i<(int)(b); ++i)

typedef long long LL;
const double eps = 1e-10;
int dcmp(double x) { if (fabs(x) < eps) return 0; return x < 0 ? -1 : 1; }
int dcmp(double x, double y) { return dcmp(x - y); }

struct Point {
  double x, y;
  Point(double x = 0, double y = 0) : x(x), y(y) {}
  Point& operator=(const Point& p) {
    x = p.x, y = p.y;
    return *this;
  }
};
typedef Point Vector;

Vector operator+(const Vector& A, const Vector& B) { return Vector(A.x + B.x, A.y + B.y); }
Vector operator-(const Point& A, const Point& B) { return Vector(A.x - B.x, A.y - B.y); }
Vector operator*(const Vector& A, double p) { return Vector(A.x * p, A.y * p); }
bool operator==(const Point& a, const Point& b) { return a.x == b.x && a.y == b.y; }
bool operator<(const Point& p1, const Point& p2) {
  if (p1.x != p2.x) return p1.x < p2.x;
  return p1.y < p2.y;
}
double Dot(const Vector& A, const Vector& B) { return A.x * B.x + A.y * B.y; }
double Length(const Vector& A) { return sqrt(Dot(A, A)); }
double Angle(const Vector& A, const Vector& B) { return acos(Dot(A, B) / Length(A) / Length(B)); }
double Cross(const Vector& A, const Vector& B) { return A.x * B.y - A.y * B.x; }
Vector Rotate(Vector A, double rad) { return Vector(A.x * cos(rad) - A.y * sin(rad), A.x * sin(rad) + A.y * cos(rad)); }
Vector Normal(Vector A) {
  double L = Length(A);
  return Vector(-A.y / L, A.x / L);
}

bool SegmentProperIntersection(const Point& a1, const Point& a2, const Point& b1, const Point& b2) {
  double c1 = Cross(a2 - a1, b1 - a1), c2 = Cross(a2 - a1, b2 - a1),
         c3 = Cross(b2 - b1, a1 - b1), c4 = Cross(b2 - b1, a2 - b1);
  return dcmp(c1) * dcmp(c2) < 0 && dcmp(c3) * dcmp(c4) < 0;
}

Point GetLineIntersection(Point P, Vector v, Point Q, Vector w) {
  Vector u = P - Q;
  double t = Cross(w, u) / Cross(v, w);
  return P + v * t;
}

bool OnSegment(const Point& p, const Point& a1, const Point& a2) {
  return dcmp(Cross(a1 - p, a2 - p)) == 0 && dcmp(Dot(a1 - p, a2 - p)) < 0;
}

istream& operator>>(istream& is, Point& p) { return is >> p.x >> p.y; }
ostream& operator<<(ostream& os, const Point& p) { return os << p.x << " " << p.y; }

int main() {
  int N;
  for (int t = 1; cin >> N && N; t++) {
    Point p;
    set<Point> all_points;
    vector<Point> ps;
    _for(i, 0, N) cin >> p, ps.push_back(p), all_points.insert(p);
    int E = --N;
    _for(i, 0, N) _for(j, i + 1, N) 
      if (SegmentProperIntersection(ps[i], ps[i + 1], ps[j], ps[j + 1]))
        all_points.insert(GetLineIntersection(ps[i], ps[i + 1] - ps[i], ps[j], ps[j + 1] - ps[j]));

    for(set<Point>::iterator si = all_points.begin(); si != all_points.end(); si++)
      _for(i, 0, N) if (OnSegment(*si, ps[i], ps[i + 1])) E++;
    int F = E + 2 - all_points.size(); // V+F-E=2, 点，面，边
    printf("Case %d: There are %d pieces.\n", t, F);
  }
  return 0;
}
// Accepted 422ms 1300kB 3093 G++ 2020-12-14 14:16:59 22208849
```

### 例题1  Morley定理（Morley’s Theorem, UVa 11178）

```cpp
// 例题1  Morley定理（Morley’s Theorem, UVa 11178）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
struct Point {
  double x, y;
  Point(double x = 0, double y = 0) : x(x), y(y) {}
};

typedef Point Vector;
Vector operator+(const Vector& A, const Vector& B) {
  return Vector(A.x + B.x, A.y + B.y);
}
Vector operator-(const Point& A, const Point& B) {
  return Vector(A.x - B.x, A.y - B.y);
}
Vector operator*(const Vector& A, double p) { return Vector(A.x * p, A.y * p); }
double Dot(const Vector& A, const Vector& B) { return A.x * B.x + A.y * B.y; }
double Length(const Vector& A) { return sqrt(Dot(A, A)); }
double Angle(const Vector& A, const Vector& B) {
  return acos(Dot(A, B) / Length(A) / Length(B));
}
double Cross(const Vector& A, const Vector& B) { return A.x * B.y - A.y * B.x; }
Point GetLineIntersection(const Point& P, const Point& v, const Point& Q, const Point& w) {
  Vector u = P - Q;
  double t = Cross(w, u) / Cross(v, w);
  return P + v * t;
}
Vector Rotate(const Vector& A, double rad) {
  return Vector(A.x * cos(rad) - A.y * sin(rad), A.x * sin(rad) + A.y * cos(rad));
}
istream& operator>>(istream& is, Point& p) { return is >> p.x >> p.y; }
ostream& operator<<(ostream& os, const Point& p) { return os << p.x << " " << p.y; }
Point getD(Point A, Point B, Point C) {
  Vector v1 = C - B;
  double a1 = Angle(A - B, v1);
  v1 = Rotate(v1, a1 / 3);

  Vector v2 = B - C;
  double a2 = Angle(A - C, v2);
  v2 = Rotate(v2, -a2 / 3);

  return GetLineIntersection(B, v1, C, v2);
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T;
  cin >> T;
  for (Point A, B, C; T--;) {
    cin >> A >> B >> C;
    Point D = getD(A, B, C), E = getD(B, C, A), F = getD(C, A, B);
    printf("%.6lf %.6lf %.6lf %.6lf %.6lf %.6lf\n", 
      D.x, D.y, E.x, E.y, F.x, F.y);
  }
  return 0;
}
// 24480472 11178 Morley's Theorem  Accepted  C++11 0.020 2020-01-28 13:07:20
```

### 例题3  狗的距离（Dog Distance, UVa 11796）

```cpp
// 例题3  狗的距离（Dog Distance, UVa 11796）
// Rujia Liu
#include<cstdio>
#include<cmath>
#include<algorithm>
using namespace std;

const double eps = 1e-8;
int dcmp(double x) { if(fabs(x) < eps) return 0; else return x < 0 ? -1 : 1; }

const double PI = acos(-1.0);
double torad(double deg) { return deg/180 * PI; }

struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

Vector operator + (const Vector& A, const Vector& B) { return Vector(A.x+B.x, A.y+B.y); }
Vector operator - (const Point& A, const Point& B) { return Vector(A.x-B.x, A.y-B.y); }
Vector operator * (const Vector& A, double p) { return Vector(A.x*p, A.y*p); }
Vector operator / (const Vector& A, double p) { return Vector(A.x/p, A.y/p); }

bool operator < (const Point& a, const Point& b) {
  return a.x < b.x || (a.x == b.x && a.y < b.y);
}

bool operator == (const Point& a, const Point &b) {
  return dcmp(a.x-b.x) == 0 && dcmp(a.y-b.y) == 0;
}

Point read_point() {
  double x, y;
  scanf("%lf%lf", &x, &y);
  return Point(x, y);
};

double Dot(const Vector& A, const Vector& B) { return A.x*B.x + A.y*B.y; }
double Length(const Vector& A) { return sqrt(Dot(A, A)); }
double Cross(const Vector& A, const Vector& B) { return A.x*B.y - A.y*B.x; }

double DistanceToSegment(const Point& P, const Point& A, const Point& B) {
  if(A == B) return Length(P-A);
  Vector v1 = B - A, v2 = P - A, v3 = P - B;
  if(dcmp(Dot(v1, v2)) < 0) return Length(v2);
  else if(dcmp(Dot(v1, v3)) > 0) return Length(v3);
  else return fabs(Cross(v1, v2)) / Length(v1);
}

const int maxn = 60;
int T, A, B;
Point P[maxn], Q[maxn];
double Min, Max;

void update(Point P, Point A, Point B) {
  Min = min(Min, DistanceToSegment(P, A, B));
  Max = max(Max, Length(P-A));
  Max = max(Max, Length(P-B));
}

int main() {
  scanf("%d", &T);
  for(int kase = 1; kase <= T; kase++) {
    scanf("%d%d", &A, &B);
    for(int i = 0; i < A; i++) P[i] = read_point();
    for(int i = 0; i < B; i++) Q[i] = read_point();

    double LenA = 0, LenB = 0;
    for(int i = 0; i < A-1; i++) LenA += Length(P[i+1]-P[i]);
    for(int i = 0; i < B-1; i++) LenB += Length(Q[i+1]-Q[i]);

    int Sa = 0, Sb = 0;
    Point Pa = P[0], Pb = Q[0];
    Min = 1e9, Max = -1e9;
    while(Sa < A-1 && Sb < B-1) {
      double La = Length(P[Sa+1] - Pa); // 甲到下一拐点的距离
      double Lb = Length(Q[Sb+1] - Pb); // 乙到下一拐点的距离
      double T = min(La/LenA, Lb/LenB); // 取合适的单位，可以让甲和乙的速度分别是LenA和LenB
      Vector Va = (P[Sa+1] - Pa)/La*T*LenA; // 甲的位移向量
      Vector Vb = (Q[Sb+1] - Pb)/Lb*T*LenB; // 乙的位移向量
      update(Pa, Pb, Pb+Vb-Va); // 求解“简化版”，更新最小最大距离
      Pa = Pa + Va;
      Pb = Pb + Vb;
      if(Pa == P[Sa+1]) Sa++;
      if(Pb == Q[Sb+1]) Sb++;
    }
    printf("Case %d: %.0lf\n", kase, Max-Min);
  }
  return 0;
}
// 25877735	11796	Dog Distance	Accepted	C++	0.010	2020-12-23 06:37:09
```

## 4.2 与圆和球有关的计算问题

### 例题4  二维几何110合一！（2D Geometry 110 in 1!, UVa12304）

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
Point GetLineProjection(const Point& P, const Point& A, const Point& B) {
  Vector v = B - A;
  return A + v * (Dot(v, P - A) / Dot(v, v));
}
double DistanceToLine(const Point& P, const Point& A, const Point& B) {
  Vector v1 = B - A, v2 = P - A;
  return fabs(Cross(v1, v2)) / Length(v1); // 如果不取绝对值，得到的是有向距离
}

struct Line {
  Point p;
  Vector v;
  Line(const Point& p, const Vector& v): p(p), v(v) { }
  Point point(double t) const {
    return p + v * t;
  }
  Line move(double d) const {
    return Line(p + Normal(v) * d, v);
  }
};

struct Circle {
  Point c;
  double r;
  Circle(const Point& c, double r): c(c), r(r) {}
  Point point(double a) const {
    return Point(c.x + cos(a) * r, c.y + sin(a) * r);
  }
};

Point GetLineIntersection(const Line& a, const Line& b) {
  return GetLineIntersection(a.p, a.v, b.p, b.v);
}

double angle(const Vector& v) {
  return atan2(v.y, v.x);
}

int getLineCircleIntersection(const Line& L, const Circle& C, double& t1, double& t2, vector<Point>& sol) {
  double a = L.v.x, b = L.p.x - C.c.x, c = L.v.y, d = L.p.y - C.c.y;
  double e = a * a + c * c, f = 2 * (a * b + c * d), g = b * b + d * d - C.r * C.r;
  double delta = f * f - 4 * e * g; // 判别式
  if (dcmp(delta) < 0) return 0; // 相离
  if (dcmp(delta) == 0) { // 相切
    t1 = t2 = -f / (2 * e); sol.push_back(L.point(t1));
    return 1;
  }
  // 相交
  t1 = (-f - sqrt(delta)) / (2 * e); sol.push_back(L.point(t1));
  t2 = (-f + sqrt(delta)) / (2 * e); sol.push_back(L.point(t2));
  return 2;
}

int getCircleCircleIntersection(const Circle& C1, const Circle& C2, vector<Point>& sol) {
  double d = Length(C1.c - C2.c);
  if (dcmp(d) == 0) {
    if (dcmp(C1.r - C2.r) == 0) return -1; // 重合，无穷多交点
    return 0;
  }
  if (dcmp(C1.r + C2.r - d) < 0) return 0;
  if (dcmp(fabs(C1.r - C2.r) - d) > 0) return 0;

  double a = angle(C2.c - C1.c);
  double da = acos((C1.r * C1.r + d * d - C2.r * C2.r) / (2 * C1.r * d));
  Point p1 = C1.point(a - da), p2 = C1.point(a + da);

  sol.push_back(p1);
  if (p1 == p2) return 1;
  sol.push_back(p2);
  return 2;
}

/******************* Problem 1 **********************/

Circle CircumscribedCircle(const Point& p1, const Point& p2, const Point& p3) {
  double Bx = p2.x - p1.x, By = p2.y - p1.y;
  double Cx = p3.x - p1.x, Cy = p3.y - p1.y;
  double D = 2 * (Bx * Cy - By * Cx);
  double cx = (Cy * (Bx * Bx + By * By) - By * (Cx * Cx + Cy * Cy)) / D + p1.x;
  double cy = (Bx * (Cx * Cx + Cy * Cy) - Cx * (Bx * Bx + By * By)) / D + p1.y;
  Point p = Point(cx, cy);
  return Circle(p, Length(p1 - p));
}

/******************* Problem 2 **********************/

Circle InscribedCircle(const Point& p1, const Point& p2, const Point& p3) {
  double a = Length(p2 - p3);
  double b = Length(p3 - p1);
  double c = Length(p1 - p2);
  Point p = (p1 * a + p2 * b + p3 * c) / (a + b + c);
  return Circle(p, DistanceToLine(p, p1, p2));
}

/******************* Problem 3 **********************/

// 过点p到圆C的切线。v[i]是第i条切线的向量。返回切线条数
int getTangents(const Point& p, const Circle& C, Vector* v) {
  Vector u = C.c - p;
  double dist = Length(u);
  if (dist < C.r) return 0;
  else if (dcmp(dist - C.r) == 0) { // p在圆上，只有一条切线
    v[0] = Rotate(u, PI / 2);
    return 1;
  } else {
    double ang = asin(C.r / dist);
    v[0] = Rotate(u, -ang);
    v[1] = Rotate(u, +ang);
    return 2;
  }
}

/******************* Problem 4 **********************/

vector<Point> CircleThroughPointTangentToLineGivenRadius(const Point& p, const Line& L, double r) {
  vector<Point> ans;
  double t1, t2;
  getLineCircleIntersection(L.move(-r), Circle(p, r), t1, t2, ans);
  getLineCircleIntersection(L.move(r), Circle(p, r), t1, t2, ans);
  return ans;
}

/******************* Problem 5 **********************/

vector<Point> CircleTangentToLinesGivenRadius(const Line& a, const Line& b, double r) {
  vector<Point> ans;
  Line L1 = a.move(-r), L2 = a.move(r);
  Line L3 = b.move(-r), L4 = b.move(r);
  ans.push_back(GetLineIntersection(L1, L3));
  ans.push_back(GetLineIntersection(L1, L4));
  ans.push_back(GetLineIntersection(L2, L3));
  ans.push_back(GetLineIntersection(L2, L4));
  return ans;
}

/******************* Problem 6 **********************/

vector<Point> CircleTangentToTwoDisjointCirclesWithRadius(const Circle& c1, const Circle& c2, double r) {
  vector<Point> ans;
  Vector v = c2.c - c1.c;
  double dist = Length(v);
  int d = dcmp(dist - c1.r - c2.r - r * 2);
  if (d > 0) return ans;
  getCircleCircleIntersection(Circle(c1.c, c1.r + r), Circle(c2.c, c2.r + r), ans);
  return ans;
}

// formatting
double lineAngleDegree(const Vector& v) {
  double ang = angle(v) * 180.0 / PI;
  while (dcmp(ang) < 0) ang += 360.0;
  while (dcmp(ang - 180) >= 0) ang -= 180.0;
  return ang;
}

void format(Circle c) {
  printf("(%.6lf,%.6lf,%.6lf)\n", c.c.x, c.c.y, c.r);
}

void format(vector<double> ans) {
  int n = ans.size();
  sort(ans.begin(), ans.end());
  printf("[");
  if (n) {
    printf("%.6lf", ans[0]);
    for (int i = 1; i < n; i++) printf(",%.6lf", ans[i]);
  }
  printf("]\n");
}

void format(vector<Point> ans) {
  int n = ans.size();
  sort(ans.begin(), ans.end());
  printf("[");
  if (n) {
    printf("(%.6lf,%.6lf)", ans[0].x, ans[0].y);
    for (int i = 1; i < n; i++) printf(",(%.6lf,%.6lf)", ans[i].x, ans[i].y);
  }
  printf("]\n");
}

// Line getLine(double x1, double y1, double x2, double y2) {
//   Point p1(x1, y1), p2(x2, y2);
//   return Line(p1, p2 - p1);
// }

Line getLine(const Point& p1, const Point& p2) {
  return Line(p1, p2 - p1);
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  for (string cmd; cin >> cmd;) {
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
      Vector v[2];
      vector<double> ans;
      int cnt = getTangents(pp, Circle(pc, r), v);
      for (int i = 0; i < cnt; i++) ans.push_back(lineAngleDegree(v[i]));
      format(ans);
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

### 例题5  圆盘问题（Viva Confetti, Kanazawa 2002, UVa1308）

```cpp
// 例题5  圆盘问题（Viva Confetti, Kanazawa 2002, UVa1308）
// 陈锋
#include <cmath>
#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
using namespace std;

const double eps = 5 * 1e-13;
int dcmp(double x) {
  if (fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}
const double PI = acos(-1), TWO_PI = PI * 2;

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

// 交点相对于圆1的极角保存在rad中
void getCircleCircleIntersection(const Point&c1, double r1, const Point&c2, double r2, vector<double>& rad) {
  double d = Length(c1 - c2);
  if (dcmp(d) == 0) return; // 不管是内含还是重合，都不相交
  if (dcmp(r1 + r2 - d) < 0) return;
  if (dcmp(fabs(r1 - r2) - d) > 0) return;
  double a = angle(c2 - c1), da = acos((r1 * r1 + d * d - r2 * r2) / (2 * r1 * d));
  rad.push_back(NormalizeAngle(a - da)), rad.push_back(NormalizeAngle(a + da));
}

const int maxn = 100 + 5;
int N;
Point center[maxn];
double radius[maxn];
bool vis[maxn];

// 覆盖点p的最上层的圆
int topmost(const Point& p) {
  for (int i = N - 1; i >= 0; i--)
    if (Length(center[i] - p) < radius[i]) return i;
  return -1;
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  while (cin >> N && N) {
    for (int i = 0; i < N; i++)cin >> center[i] >> radius[i];
    fill_n(vis, N + 1, 0);
    for (int i = 0; i < N; i++) {
      vector<double> rad; // 考虑圆i被切割成的各个圆弧。把圆周当做区间来处理，起点是0，终点是2PI
      rad.push_back(0), rad.push_back(TWO_PI);
      for (int j = 0; j < N; j++)
        getCircleCircleIntersection(center[i], radius[i], center[j], radius[j], rad);
      sort(rad.begin(), rad.end());

      for (size_t j = 0; j < rad.size(); j++) {
        double mid = (rad[j] + rad[j + 1]) / 2.0; // 圆弧中点相对于圆i圆心的极角
        for (int side = -1; side <= 1; side += 2) {
          double r2 = radius[i] - side * eps; // 往里面或者外面稍微一动一点点
          int t = topmost(Point(center[i].x + cos(mid) * r2, center[i].y + sin(mid) * r2));
          if (t >= 0) vis[t] = true;
        }
      }
    }
    int ans = 0;
    for (int i = 0; i < N; i++) if (vis[i]) ans++;
    cout << ans << "\n";
  }
  return 0;
}
// 25877748	1308	Viva Confetti	Accepted	C++	0.000	2020-12-23 06:39:24
```

## 4.3 二维几何常用算法

### 例题14  找边界（Find the Border, NEERC 2004, Codeforces Gym100536F）

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

### 例题12  丛林警戒队（Jungle Outpost, NEERC 2010, LA4992/UVa1475）

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

### 例题11  铁人三项（Triathlon, NEERC 2000, POJ1755）

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

### 例题13  怪物陷阱（Monster Trap, Aizu 2003, POJ2048）

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

### 例题8  点集划分（The Great Divide, UVa 10256）

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

### 例题6  包装木板（Board Wrapping, UVa 10652）

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

### 例题7  飞机场（Airport, UVa 11168）

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

### 例题15  块和圆盘（Pieces and Discs, UVa 12296）

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

### 例题10  离海最远的点（Most Distant Point from the Sea, Tokyo 2007, UVa1396）

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

### 例题9  正方形（Squares, Seoul 2009, UVa1453）

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

## 4.4 三维几何基础

### 例题20  黄金屋顶（The Golden Ceiling，ACM/ICPC, Greater New York 2011, LA5808）

```cpp
// 例题20  黄金屋顶（The Golden Ceiling，ACM/ICPC, Greater New York 2011, LA5808）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;
const double EPS = 0.0001;
struct Point3 {
  double x, y, z;
  Point3(double _x = 0, double _y = 0, double _z = 0) : x(_x), y(_y), z(_z) {}
};
typedef Point3 Vector3;
Vector3 operator + (const Vector3& A, const Vector3& B) 
{ return Vector3(A.x + B.x, A.y + B.y, A.z + B.z); }
Vector3 operator - (const Point3& A, const Point3& B) 
{ return Vector3(A.x - B.x, A.y - B.y, A.z - B.z); }
Vector3 operator * (const Vector3& A, double p) 
{ return Vector3(A.x * p, A.y * p, A.z * p); }
double dot(const Point3& A, const Point3& B) 
{ return A.x * B.x + A.y * B.y + A.z * B.z; }
double length(const Point3& A) { return sqrt(dot(A, A)); }
// 线段p1-p2和平面PV·V = D的交点
Point3 LinePlaneIntersection(const Point3& p1, const Point3& p2, const Vector3& PV, double D) {
  double v1 = dot(p1, PV) - D, v2 = dot(p2, PV) - D, denom = v1 - v2;
  return p1 * (-v2 / denom) + p2 * (v1 / denom);
}

// 这些顶点组成的多边形位于平面PV-D下方的多边形面积
double area_under(const vector<Point3>& ps, const Vector3& PV, double D) {
  vector<Point3> poly;
  for (size_t i = 0; i < ps.size(); i++) {
    const Point3 &p = ps[i], &np = ps[(i + 1) % ps.size()];
    double v = dot(PV, p) - D, nv = dot(PV, np) - D;
    if (v <= EPS) poly.push_back(p); // v在平面下方或者经过平面
    if (v * nv < EPS && fabs(v) > EPS && fabs(nv) > EPS) // vi和nxt_vi形成的边和平面相交
      poly.push_back(LinePlaneIntersection(np, p, PV, D)); // 边和平面的交点
  }
  double s = 0; // 多边形都是和xy平面平行的
  for (size_t j = 1; j + 1 < poly.size() ; j++) {
    Point3 v1 = poly[j] - poly[0], v2 = poly[j + 1] - poly[0];
    s += v1.x * v2.y - v2.x * v1.y;
  }
  return fabs(s) / 2.0;
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  Point3 VS[8]; // 八个顶点
  Vector3 PV; // 平面向量 {A, B, C}
  double D, L, W, H;
  int T; cin >> T;
  for (int t = 1, N; t <= T ; t++) {
    cin >> N >> L >> W >> H;
    cin >> PV.x >> PV.y >> PV.z >> D;
    for (int i = 0; i < 8 ; i++) { // 立方体各个顶点坐标   //   1 ---- 3
      Point3& p = VS[i];                                 //  /|     /|  z
      if (i & 1) p.z = H;                                // 5 ---- 7 |  |
      if (i & 2) p.y = W;                                // | 0 ---| 2  .-- y
      if (i & 4) p.x = L;                                // |/     |/  /
    }                                                    // 4 ---- 6  x
    vector<Point3> top_vs = {VS[1], VS[3], VS[7], VS[5]}, 
                   bottom_vs = {VS[0], VS[2], VS[6], VS[4]};
    double top_area = all_of(top_vs.begin(), top_vs.end(), 
         [&](const Point3 & p) {return dot(PV, p) >= D;})
         ? 0.0 : area_under(top_vs, PV, D); // 平面和顶面没有公共点?

    double bottom_area = all_of(bottom_vs.begin(), bottom_vs.end(), 
         [&](const Point3 & p) {return dot(PV, p) <= D;})
         ? L * W : area_under(bottom_vs, PV, D);// 底面4个点都在平面PV-D下面?
    double cos_phi = PV.z / length(PV); // 平面法向量和z轴夹角的cos
    double ans = top_area + (bottom_area - top_area) / cos_phi;
    printf("%d %.0lf\n", t, ceil(ans));
  }
  return 0;
}
// Accepted 1488kB 3187 G++2020-12-14 15:26:13 34869914
```

### 例题19  压纸器（Paperweight, World Finals 2010, UVa1100）

```cpp
// 例题19  压纸器（Paperweight, World Finals 2010, UVa1100）
// 刘汝佳
#include<cstdio>
#include<cmath>
using namespace std;

const double eps = 1e-8;
int dcmp(double x) {
  if(fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}

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
double Angle(const Vector3& A, const Vector3& B) { return acos(Dot(A, B) / Length(A) / Length(B)); }
Vector3 Cross(const Vector3& A, const Vector3& B) { return Vector3(A.y*B.z - A.z*B.y, A.z*B.x - A.x*B.z, A.x*B.y - A.y*B.x); }
double Area2(const Point3& A, const Point3& B, const Point3& C) { return Length(Cross(B-A, C-A)); }
double Volume6(const Point3& A, const Point3& B, const Point3& C, const Point3& D) { return Dot(D-A, Cross(B-A, C-A)); }

bool read_point3(Point3& p) {
  if(scanf("%lf%lf%lf", &p.x, &p.y, &p.z) != 3) return false;
  return true;
}

// 点p到平面p0-n的距离。n必须为单位向量
double DistanceToPlane(const Point3& p, const Point3& p0, const Vector3& n) {
  return fabs(Dot(p-p0, n)); // 如果不取绝对值，得到的是有向距离
}

// 点p在平面p0-n上的投影。n必须为单位向量
Point3 GetPlaneProjection(const Point3& p, const Point3& p0, const Vector3& n) {
  return p-n*Dot(p-p0, n);
}

// 点P到直线AB的距离
double DistanceToLine(const Point3& P, const Point3& A, const Point3& B) {
  Vector3 v1 = B - A, v2 = P - A;
  return Length(Cross(v1, v2)) / Length(v1);
}

// p1和p2是否在线段a-b的同侧
bool SameSide(const Point3& p1, const Point3& p2, const Point3& a, const Point3& b) {
  return dcmp(Dot(Cross(b-a, p1-a), Cross(b-a, p2-a))) >= 0;
}

// 点在三角形P0, P1, P2中
bool PointInTri(const Point3& P, const Point3& P0, const Point3& P1, const Point3& P2) {
  return SameSide(P, P0, P1, P2) && SameSide(P, P1, P0, P2) && SameSide(P, P2, P0, P1);
}

// 四面体的重心
Point3 Centroid(const Point3& A, const Point3& B, const Point3& C, const Point3& D) {
   return (A + B + C + D)/4.0;
}

#include<algorithm>
using namespace std;

// 判断P是否在三角形A, B, C中，并且到三条边的距离都至少为mindist。保证P, A, B, C共面
bool InsideWithMinDistance(const Point3& P, const Point3& A, const Point3& B, const Point3& C, double mindist) {
  if(!PointInTri(P, A, B, C)) return false;
  if(DistanceToLine(P, A, B) < mindist) return false;
  if(DistanceToLine(P, B, C) < mindist) return false;
  if(DistanceToLine(P, C, A) < mindist) return false;
  return true;
}

// 判断P是否在凸四边形ABCD（顺时针或逆时针）中，并且到四条边的距离都至少为mindist。保证P, A, B, C, D共面
bool InsideWithMinDistance(const Point3& P, const Point3& A, const Point3& B, const Point3& C, const Point3& D, double mindist) {
  if(!PointInTri(P, A, B, C)) return false;
  if(!PointInTri(P, C, D, A)) return false;
  if(DistanceToLine(P, A, B) < mindist) return false;
  if(DistanceToLine(P, B, C) < mindist) return false;
  if(DistanceToLine(P, C, D) < mindist) return false;
  if(DistanceToLine(P, D, A) < mindist) return false;
  return true;
}

int main() {
  for(int kase = 1; ; kase++) {
    Point3 P[5], F;
    for(int i = 0; i < 5; i++)
      if(!read_point3(P[i])) return 0;
    read_point3(F);

    // 求重心坐标
    Point3 c1 = Centroid(P[0], P[1], P[2], P[3]);
    Point3 c2 = Centroid(P[0], P[1], P[2], P[4]);
    double vol1 = fabs(Volume6(P[0], P[1], P[2], P[3])) / 6.0;
    double vol2 = fabs(Volume6(P[0], P[1], P[2], P[4])) / 6.0;
    Point3 centroid = (c1 * vol1 + c2 * vol2) / (vol1 + vol2);

    // 枚举放置方案
    double mindist = 1e9, maxdist = -1e9;
    for(int i = 0; i < 5; i++)
      for(int j = i+1; j < 5; j++)
        for(int k = j+1; k < 5; k++) {
          // 找出另外两个点的下标a和b
          int vis[5] = {0};          
          vis[i] = vis[j] = vis[k] = 1;
          int a, b;
          for(a = 0; a < 5; a++) if(!vis[a]) { b = 10-i-j-k-a; break; }

          // 判断a和b是否在平面i-j-k的异侧
          int d1 = dcmp(Volume6(P[i], P[j], P[k], P[a]));
          int d2 = dcmp(Volume6(P[i], P[j], P[k], P[b]));
          if(d1 * d2 < 0) continue; // 是，则放置方案不合法

          Vector3 n = Cross(P[j]-P[i], P[k]-P[i]); // 法向量
          n = n / Length(n); // 单位化

          Point3 proj = GetPlaneProjection(centroid, P[i], n); // 重心在平面i-j-k上的投影
          bool ok = InsideWithMinDistance(proj, P[i], P[j], P[k], 0.2);
          if(!ok) {
            if(d1 == 0) { // i-j-k-a四点共面。i和j一定为ABC三个顶点之一，k和a是D或者E
              if(!InsideWithMinDistance(proj, P[i], P[k], P[j], P[a], 0.2)) continue;
            } else if(d2 == 0) { // i-j-k-b四点共面。i和j一定为ABC三个顶点之一，k和b是D或者E
              if(!InsideWithMinDistance(proj, P[i], P[k], P[j], P[b], 0.2)) continue;
            } else
              continue;
          }

          // 更新答案
          double dist = DistanceToPlane(F, P[i], n);
          mindist = min(mindist, dist);
          maxdist = max(maxdist, dist);
        }
    printf("Case %d: %.5lf %.5lf\n", kase, mindist, maxdist);
  }
  return 0;
}
// Accepted 5230 C++5.3.0 2020-12-14 15:22:46 25846093
```

### 例题16  三维三角形（3D Triangles, UVa 11275）

```cpp
// 例题16  三维三角形（3D Triangles, UVa 11275）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

struct Point3 {
  double x, y, z;
  Point3(double x = 0, double y = 0, double z = 0): x(x), y(y), z(z) { }
};
istream& operator>>(istream& is, Point3& p) { return is >> p.x >> p.y >> p.z; }

typedef Point3 Vector3;

Vector3 operator + (const Vector3& A, const Vector3& B) { return Vector3(A.x + B.x, A.y + B.y, A.z + B.z); }
Vector3 operator - (const Point3& A, const Point3& B) { return Vector3(A.x - B.x, A.y - B.y, A.z - B.z); }
Vector3 operator * (const Vector3& A, double p) { return Vector3(A.x * p, A.y * p, A.z * p); }
Vector3 operator / (const Vector3& A, double p) { return Vector3(A.x / p, A.y / p, A.z / p); }

const double eps = 1e-8;
int dcmp(double x) {
  if (fabs(x) < eps) return 0; else return x < 0 ? -1 : 1;
}

double Dot(const Vector3& A, const Vector3& B) { return A.x * B.x + A.y * B.y + A.z * B.z; }
double Length(const Vector3& A) { return sqrt(Dot(A, A)); }
double Angle(const Vector3& A, const Vector3& B) { return acos(Dot(A, B) / Length(A) / Length(B)); }
Vector3 Cross(const Vector3& A, const Vector3& B) { return Vector3(A.y * B.z - A.z * B.y, A.z * B.x - A.x * B.z, A.x * B.y - A.y * B.x); }
double Area2(const Point3& A, const Point3& B, const Point3& C) { return Length(Cross(B - A, C - A)); }

// p1和p2是否在线段a-b的同侧
bool SameSide(const Point3& p1, const Point3& p2, const Point3& a, const Point3& b) {
  return dcmp(Dot(Cross(b - a, p1 - a), Cross(b - a, p2 - a))) >= 0;
}

// 点在三角形P0, P1, P2中
bool PointInTri(const Point3& P, const Point3& P0, const Point3& P1, const Point3& P2) {
  return SameSide(P, P0, P1, P2) && SameSide(P, P1, P0, P2) && SameSide(P, P2, P0, P1);
}

// 三角形P0P1P2是否和线段AB相交
bool TriSegIntersection(const Point3& P0, const Point3& P1, const Point3& P2, const Point3& A, const Point3& B, Point3& P) {
  Vector3 n = Cross(P1 - P0, P2 - P0);
  if (dcmp(Dot(n, B - A)) == 0) return false; // 线段A-B和平面P0P1P2平行或共面
  else { // 平面A和直线P1-P2有惟一交点
    double t = Dot(n, P0 - A) / Dot(n, B - A);
    if (dcmp(t) < 0 || dcmp(t - 1) > 0) return false; // 不在线段AB上
    P = A + (B - A) * t; // 交点
    return PointInTri(P, P0, P1, P2);
  }
}

bool TriTriIntersection(Point3* T1, Point3* T2) {
  Point3 P;
  for (int i = 0; i < 3; i++) {
    if (TriSegIntersection(T1[0], T1[1], T1[2], T2[i], T2[(i + 1) % 3], P)) return true;
    if (TriSegIntersection(T2[0], T2[1], T2[2], T1[i], T1[(i + 1) % 3], P)) return true;
  }
  return false;
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T; cin >> T;
  while (T--) {
    Point3 T1[3], T2[3];
    for (int i = 0; i < 3; i++) cin >> T1[i];
    for (int i = 0; i < 3; i++) cin >> T2[i];
    cout << (TriTriIntersection(T1, T2) ? 1 : 0) << endl;
  }
  return 0;
}
// 24483577   11275   3D Triangles  Accepted  C++11   0.120   2020-01-29 07:36:36
```

### 例题18  行星（Asteroids, NEERC 2009, UVa1438）

```cpp
// 例题18  行星（Asteroids, NEERC 2009, UVa1438）
// 陈锋
#include <vector>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

const double eps = 1e-8;
int dcmp(double x) {
  if (fabs(x) < eps) return 0;
  return x < 0 ? -1 : 1;
}

struct Point3 {
  double x, y, z;
  Point3(double x = 0, double y = 0, double z = 0): x(x), y(y), z(z) { }
};
istream& operator>>(istream& is, Point3& p) { return is >> p.x >> p.y >> p.z; }

typedef Point3 Vector3;

Vector3 operator + (const Vector3& A, const Vector3& B) 
{ return Vector3(A.x + B.x, A.y + B.y, A.z + B.z); }
Vector3 operator - (const Point3& A, const Point3& B) 
{ return Vector3(A.x - B.x, A.y - B.y, A.z - B.z); }
Vector3 operator * (const Vector3& A, double p) 
{ return Vector3(A.x * p, A.y * p, A.z * p); }
Vector3 operator / (const Vector3& A, double p) 
{ return Vector3(A.x / p, A.y / p, A.z / p); }
bool operator == (const Point3& a, const Point3& b)
{ return dcmp(a.x - b.x) == 0 && dcmp(a.y - b.y) == 0 && dcmp(a.z - b.z) == 0;}
double Dot(const Vector3& A, const Vector3& B) { return A.x * B.x + A.y * B.y + A.z * B.z; }
double Length(const Vector3& A) { return sqrt(Dot(A, A)); }
double Angle(const Vector3& A, const Vector3& B) 
{ return acos(Dot(A, B) / Length(A) / Length(B)); }
Vector3 Cross(const Vector3& A, const Vector3& B) 
{ return Vector3(A.y*B.z - A.z*B.y, A.z*B.x - A.x*B.z, A.x*B.y - A.y*B.x); }
double Area2(const Point3& A, const Point3& B, const Point3& C) 
{ return Length(Cross(B - A, C - A)); }
double Volume6(const Point3& A, const Point3& B, const Point3& C, const Point3& D) 
{ return Dot(D - A, Cross(B - A, C - A)); }
Point3 Centroid(const Point3& A, const Point3& B, const Point3& C, const Point3& D) 
{ return (A + B + C + D) / 4.0; }
double rand01() { return rand() / (double)RAND_MAX; }
double randeps() { return (rand01() - 0.5) * eps; }
Point3 add_noise(const Point3& p) 
{ return Point3(p.x + randeps(), p.y + randeps(), p.z + randeps()); }

struct Face {
  int v[3];
  Face(int a, int b, int c) { v[0] = a; v[1] = b; v[2] = c; }
  Vector3 Normal(const vector<Point3>& P) const {
    return Cross(P[v[1]] - P[v[0]], P[v[2]] - P[v[0]]);
  }
  // f是否能看见P[i]
  int CanSee(const vector<Point3>& P, int i) const {
    return Dot(P[i] - P[v[0]], Normal(P)) > 0;
  }
};

// 增量法求三维凸包
// 注意：没有考虑各种特殊情况（如四点共面）。实践中，请在调用前对输入点进行微小扰动
vector<Face> CH3D(const vector<Point3>& P) {
  int n = P.size();
  vector<vector<int> > vis(n);
  for (int i = 0; i < n; i++) vis[i].resize(n);

  vector<Face> cur;
  cur.push_back(Face(0, 1, 2)); // 由于已经进行扰动，前三个点不共线
  cur.push_back(Face(2, 1, 0));
  for (int i = 3; i < n; i++) {
    vector<Face> next;
    // 计算每条边的“左面”的可见性
    for (size_t j = 0; j < cur.size(); j++) {
      Face& f = cur[j];
      int res = f.CanSee(P, i);
      if (!res) next.push_back(f);
      for (int k = 0; k < 3; k++) vis[f.v[k]][f.v[(k + 1) % 3]] = res;
    }
    for (size_t j = 0; j < cur.size(); j++)
      for (int k = 0; k < 3; k++) {
        int a = cur[j].v[k], b = cur[j].v[(k + 1) % 3];
        if (vis[a][b] != vis[b][a] && vis[a][b]) // (a,b)是分界线，左边对P[i]可见
          next.push_back(Face(a, b, i));
      }
    cur = next;
  }
  return cur;
}

struct ConvexPolyhedron {
  int n;
  vector<Point3> P, P2;
  vector<Face> faces;

  bool read() {
    if (!(cin >> n)) return false;
    P.resize(n), P2.resize(n);
    for (int i = 0; i < n; i++) cin >> P[i], P2[i] = add_noise(P[i]);
    faces = CH3D(P2);
    return true;
  }

  Point3 centroid() {
    Point3 C = P[0];
    double totv = 0;
    Point3 tot(0, 0, 0);
    for (size_t i = 0; i < faces.size(); i++) {
      Point3 p1 = P[faces[i].v[0]], p2 = P[faces[i].v[1]], p3 = P[faces[i].v[2]];
      double v = -Volume6(p1, p2, p3, C);
      totv += v;
      tot = tot + Centroid(p1, p2, p3, C) * v;
    }
    return tot / totv;
  }

  double mindist(Point3 C) {
    double ans = 1e30;
    for (size_t i = 0; i < faces.size(); i++) {
      Point3 p1 = P[faces[i].v[0]], p2 = P[faces[i].v[1]], p3 = P[faces[i].v[2]];
      ans = min(ans, fabs(-Volume6(p1, p2, p3, C) / Area2(p1, p2, p3)));
    }
    return ans;
  }
};

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  ConvexPolyhedron P1, P2;
  while (P1.read() && P2.read()) {
    Point3 C1 = P1.centroid();
    double d1 = P1.mindist(C1);
    Point3 C2 = P2.centroid();
    double d2 = P2.mindist(C2);
    printf("%.8lf\n", d1 + d2);
  }
  return 0;
}
// Accepted 4465 C++ 5.3.02020-12-14 15:12:15 25846070
```

### 例题17  Ardenia王国（Ardenia, CERC 2010, UVa1469）

```cpp
// 例题17  Ardenia王国（Ardenia, CERC 2010, UVa1469）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

struct Point3 {
  int x, y, z;
  Point3(int x = 0, int y = 0, int z = 0) : x(x), y(y), z(z) {}
};
istream& operator>>(istream& is, Point3& p) { return is >> p.x >> p.y >> p.z; }

typedef Point3 Vector3;

Vector3 operator+(const Vector3& A, const Vector3& B) {
  return Vector3(A.x + B.x, A.y + B.y, A.z + B.z);
}
Vector3 operator-(const Point3& A, const Point3& B) {
  return Vector3(A.x - B.x, A.y - B.y, A.z - B.z);
}
Vector3 operator*(const Vector3& A, int p) {
  return Vector3(A.x * p, A.y * p, A.z * p);
}
bool operator==(const Point3& a, const Point3& b) {
  return a.x == b.x && a.y == b.y && a.z == b.z;
}
int Dot(const Vector3& A, const Vector3& B) {
  return A.x * B.x + A.y * B.y + A.z * B.z;
}
int Length2(const Vector3& A) { return Dot(A, A); }
Vector3 Cross(const Vector3& A, const Vector3& B) {
  return Vector3(A.y * B.z - A.z * B.y, A.z * B.x - A.x * B.z,
                 A.x * B.y - A.y * B.x);
}

typedef long long LL;
LL gcd(LL a, LL b) { return b ? gcd(b, a % b) : a; }
LL lcm(LL a, LL b) { return a / gcd(a, b) * b; }
struct Rat {
  LL a, b;
  Rat(LL a = 0) : a(a), b(1) {}
  Rat(LL x, LL y) : a(x), b(y) {
    if (b < 0) a = -a, b = -b;
    LL d = gcd(a, b);
    if (d < 0) d = -d;
    a /= d, b /= d;
  }
};

Rat operator+(const Rat& A, const Rat& B) {
  LL x = lcm(A.b, B.b);
  return Rat(A.a * (x / A.b) + B.a * (x / B.b), x);
}
Rat operator-(const Rat& A, const Rat& B) { return A + Rat(-B.a, B.b); }
Rat operator*(const Rat& A, const Rat& B) { return Rat(A.a * B.a, A.b * B.b); }
void updatemin(Rat& A, const Rat& B) {
  if (A.a * B.b > B.a * A.b) A.a = B.a, A.b = B.b;
}

// 点P到线段AB的距离的平方
Rat Rat_Dist2ToSeg(const Point3& P, const Point3& A, const Point3& B) {
  if (A == B) return Length2(P - A);
  Vector3 v1 = B - A, v2 = P - A, v3 = P - B;
  if (Dot(v1, v2) < 0) return Length2(v2);
  if (Dot(v1, v3) > 0) return Length2(v3);
  return Rat(Length2(Cross(v1, v2)), Length2(v1));
}

// 求异面直线p1+su和p2+tv的公垂线对应的s。如果平行/重合，返回false
bool Rat_LineDistance3D(const Point3& p1, const Vector3& u, const Point3& p2,
                        const Vector3& v, Rat& s) {
  LL b = (LL)Dot(u, u) * Dot(v, v) - (LL)Dot(u, v) * Dot(u, v);
  if (b == 0) return false;
  LL a = (LL)Dot(u, v) * Dot(v, p1 - p2) - (LL)Dot(v, v) * Dot(u, p1 - p2);
  s = Rat(a, b);
  return true;
}

void Rat_GetPointOnLine(const Point3& A, const Point3& B, const Rat& t, Rat& x,
                        Rat& y, Rat& z) {
  x = Rat(A.x) + Rat(B.x - A.x) * t;
  y = Rat(A.y) + Rat(B.y - A.y) * t;
  z = Rat(A.z) + Rat(B.z - A.z) * t;
}

Rat Rat_Distance2(const Rat& x1, const Rat& y1, const Rat& z1, const Rat& x2,
                  const Rat& y2, const Rat& z2) {
  return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) + (z1 - z2) * (z1 - z2);
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T;
  cin >> T;
  for (Point3 A, B, C, D; cin >> A >> B >> C >> D, T--;) {
    Rat s, t, ans = Rat(1e9);
    bool ok = false;
    if (Rat_LineDistance3D(A, B - A, C, D - C, s))
      if (s.a > 0 && s.a < s.b && Rat_LineDistance3D(C, D - C, A, B - A, t))
        if (t.a > 0 && t.a < t.b) {
          ok = true;  // 异面直线/相交直线
          Rat x1, y1, z1, x2, y2, z2;
          Rat_GetPointOnLine(A, B, s, x1, y1, z1),
              Rat_GetPointOnLine(C, D, t, x2, y2, z2);
          ans = Rat_Distance2(x1, y1, z1, x2, y2, z2);
        }
    if (!ok) {  // 平行直线/重合直线
      updatemin(ans, Rat_Dist2ToSeg(A, C, D)),
          updatemin(ans, Rat_Dist2ToSeg(B, C, D));
      updatemin(ans, Rat_Dist2ToSeg(C, A, B)),
          updatemin(ans, Rat_Dist2ToSeg(D, A, B));
    }
    cout << ans.a << " " << ans.b << endl;
  }
  return 0;
}
// Accepted 360ms 3795 C++ 5.3.0 2020-12-14 15:05:59 25846056
```
