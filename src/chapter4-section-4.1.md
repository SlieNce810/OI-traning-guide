# 4.1 二维几何基础

## 例题2  好看的一笔画（That Nice Euler Circuit, Shanghai 2004, LA3263）

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

## 例题1  Morley定理（Morley’s Theorem, UVa 11178）

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

## 例题3  狗的距离（Dog Distance, UVa 11796）

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
