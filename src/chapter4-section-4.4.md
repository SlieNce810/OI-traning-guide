# 4.4 三维几何基础

## 例题20  黄金屋顶（The Golden Ceiling，ACM/ICPC, Greater New York 2011, LA5808）

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

## 例题19  压纸器（Paperweight, World Finals 2010, UVa1100）

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

## 例题16  三维三角形（3D Triangles, UVa 11275）

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

## 例题18  行星（Asteroids, NEERC 2009, UVa1438）

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

## 例题17  Ardenia王国（Ardenia, CERC 2010, UVa1469）

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
