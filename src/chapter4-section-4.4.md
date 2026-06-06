# 4.4 三维几何基础

## 例题20  黄金屋顶（The Golden Ceiling，ACM/ICPC, Greater New York 2011, LA5808）

### 题目描述
有一个L×W×H的长方体房间。需要在房间内部按照给定的法向量(A, B, C)和D（定义平面方程 Ax + By + Cz = D）建造一个斜面屋顶。该平面可能穿过长方体。求平面在长方体上方（满足 Ax + By + Cz ≥ D 的部分）的面积，即从上方俯视时看到的"黄金屋顶"实际面积（考虑斜面倾斜角度）。

**输入格式**：第一行是整数T（≤10），表示测试数据组数。每组数据包含两行：
- 第一行：N L W H（N为数据编号，1 ≤ L,W,H ≤ 10000）
- 第二行：A B C D，表示平面Ax+By+Cz=D的参数（A,B,C不全为0，D为整数）

**输出格式**：对于每组测试数据，输出一行"编号 面积"，面积为整数（向上取整），即平面在长方体上方的实际面积。

### 解题思路
1. **求平面与长方体顶面的交**：先计算平面与长方体顶面(z=H)的交。如果长方体顶面的所有4个顶点都在平面下方（dot(PV, p) ≤ D），则顶面没有屋顶部分（面积=0）。否则，用area_under函数计算顶面在平面下方的部分面积，即被平面截去的部分。

2. **求平面与长方体底面的交**：类似地计算底面(z=0)在平面下方的部分面积。如果底面4个顶点都在平面下方，则整个底面都在屋顶下（area = L×W）。否则计算实际面积。

3. **面积修正**：由于斜面有倾斜，实际斜面面积 = bottom_area + (top_area - bottom_area) / cos(φ)，其中φ是平面法向量与z轴的夹角。cos(φ) = C / |(A,B,C)|。

4. **多边形面积**：用叉积计算多边形在xy平面上的投影面积。

### 算法方法
- **area_under**：将原始多边形（如矩形顶面/底面）与平面求交，得到在平面下方的部分多边形，计算其在xy平面上的投影面积。
- **平面求交**：通过凸多边形裁剪获得平面以下的部分。
- **叉积面积**：利用 `Σ[(xi+1 - x0)(yi - y0) - (yi+1 - y0)(xi - x0)] / 2` 计算多边形面积。

### 复杂度分析
- **时间复杂度**：O(1)。所有操作均为常数时间（处理固定的8个顶点）。
- **空间复杂度**：O(1)。

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

### 题目描述
给定一个由5个点A、B、C、D、E组成的凸多面体（A、B、C是三角形底面，D和E是另外两个顶点，构成底面为三角形ABC的四棱锥和五棱锥的组合），其实是一个以ABC为底面、D和E为顶点的双棱锥。压纸器放置在水平桌面上，由一个三角面（三角形）或四边形面作为支撑面。

给定桌面上的一个固定点F。压纸器可以以不同的面作为底面放置。对于每种合法的放置方式，计算点F到放置后的桌面的距离。求所有合法放置方式中，F到桌面距离的最小值和最大值（桌面即支撑面所在平面）。

**输入格式**：输入含有多组测试数据，EOF结束。每组6行，前5行每行三个浮点数，给出5个顶点的坐标，第6行给出固定点F的坐标。

**输出格式**：对于每组测试数据，输出"Case X: min max"，保留5位小数。

### 解题思路
1. **合法放置条件**：压纸器以某三个点或四个点所在的面为底面放置在桌面上。一个面可以合法作为底面，当且仅当所有其他顶点都在该面的同侧（上方）。

2. **重心底座投影**：对于每个合法的底面，计算整个压纸器重心在该底面上的投影点。该投影点必须落在支撑面内部，且到支撑面各边的距离不小于0.2（稳定性要求）。

3. **枚举底面**：对于每3个点组成的三角形面（和可能的4点共面的四边形），判断是否合法底面。

4. **四面体/五面体重心**：整体重心通过将多面体分解为两个以ABC为底面的四面体，然后按体积加权平均。

5. **点到平面距离**：对每个合法放置，计算F点到支撑面的垂直距离。

### 算法方法
- **体积计算**：6倍体积 = `Dot(D-A, Cross(B-A, C-A))`（四面体的有向体积）。
- **重心**：四面体重心 = (A+B+C+D)/4.0。
- **共面判断**：用Volume6判断点是否在平面上。
- **点在三角形内**：用同侧法SameSide判断。
- **投影**：GetPlaneProjection计算点在平面上的投影。

### 复杂度分析
- **时间复杂度**：O(1)。固定5个点，枚举所有3点组合和4点组合，总共约C(5,3)=10种三角形面+最多C(5,4)=5种四边形面。
- **空间复杂度**：O(1)。

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

### 题目描述
给定两个三维空间中的三角形（各由3个顶点给出），判断它们是否相交。如果两个三角形有公共点（无论是内部相交、边界接触还是顶点重合），都视为相交。

**输入格式**：第一行是整数T（T ≤ 100），表示测试数据组数。每组数据包含两行，每行9个浮点数 x1 y1 z1 x2 y2 z2 x3 y3 z3，表示一个三角形的三个顶点坐标。所有坐标绝对值不超过100。

**输出格式**：对于每组测试数据，如果两个三角形相交输出1，否则输出0。

### 解题思路
三维空间中两个三角形相交的判定，可以简化为：检查三角形1的每条边是否与三角形2相交，以及三角形2的每条边是否与三角形1相交。

1. **线段与三角形相交**：对于三角形(P0, P1, P2)和线段AB：
   - 先计算三角形所在平面的法向量 n = Cross(P1-P0, P2-P0)
   - 若 n · (B-A) = 0，则线段与三角形平面平行或共面（本题忽略共面情况）
   - 否则，计算线段AB与三角形平面的交点参数 t = n·(P0-A) / n·(B-A)
   - 若 0 ≤ t ≤ 1，则交点在线段AB上，再判断交点是否在三角形内部

2. **点在三角形内**：使用同侧法（SameSide）。对三角形三条边分别判断点P与第三个顶点是否在线段同一侧。同一侧通过向量叉积的点积符号判断：`Dot(Cross(v, q-a), Cross(v, p-a)) ≥ 0`。

3. **双向检查**：对三角形1的三条边分别检查是否与三角形2相交，同时对三角形2的三条边检查是否与三角形1相交。

### 算法方法
- **叉积**：三维叉积计算平面的法向量，用于判断方向。
- **同侧法（SameSide）**：判断两点在三维线段同侧，使用叉积-点积组合。
- **参数方程求交**：线段AB参数化为 A + t·(B-A)，与平面求交点参数t。

### 复杂度分析
- **时间复杂度**：O(1)。每个测试只需6次线段-三角形相交判断，每次O(1)。总O(T)。
- **空间复杂度**：O(1)。

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

### 题目描述
给定两个凸多面体（小行星），分别由各自的顶点集合定义。两个凸多面体可能静止或沿各自的方向匀速运动（但本题简化版本两个行星都是静止的）。求它们之间的最近距离。

简化版本：两个静止凸多面体之间的最短距离。即求两个三维凸包之间的最短距离。

**输入格式**：输入包含多组测试数据。每组两个凸多面体的数据，每个凸多面体第一行是整数n（3 ≤ n ≤ 60），表示顶点数，接下来n行每行三个浮点数x y z，表示顶点坐标。输入以EOF结束。所有坐标绝对值不超过10000。

**输出格式**：对于每组测试数据，输出两个凸多面体之间的最短距离，保留8位小数。

### 解题思路
1. **三维凸包构造**：使用增量法构造三维凸包。先将输入点加入随机微小扰动（避免共面等退化情况），然后逐步将点加入当前凸包。

2. **增量法核心**：维护当前凸包的面集合。对于新点P：
   - 检查P对每个面的可见性（点乘面法向量>0表示P在该面的外侧）
   - 不可见的面保留
   - 可见与不可见面之间的边是"分界线"，这些边与P形成新的三角形面

3. **重心到面距离**：两个凸多面体之间的最短距离 = 凸多面体1的重心到其表面的最短距离 + 凸多面体2的重心到其表面的最短距离。这基于两个凸多面体是独立且不一定相交的假设。

4. **重心计算**：将凸多面体分解为以某固定点（如第一个顶点）为公共顶点的多个四面体，按体积加权求重心。

5. **点到面距离**：distance = |volume6| / area2，即6倍体积除以2倍面积。

### 算法方法
- **增量法3D凸包**：O(N²)时间复杂度，对N ≤ 60足够。
- **可见性判断**：Face.CanSee判断点是否在面的外侧。
- **扰动处理**：添加微小随机扰动避免退化（四点共面等）。
- **体积/面积**：Volume6计算6倍四面体体积，Area2计算2倍三角形面积。

### 复杂度分析
- **时间复杂度**：O(N²)，每次增量构造凸包需遍历所有当前面O(N)，共N次。N ≤ 60。
- **空间复杂度**：O(N)，存储顶点和凸包面。

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

### 题目描述
在三维空间中给定两条线段AB和CD（端点坐标均为整数），求这两条线段之间的最短距离。

**输入格式**：第一行是整数T（T ≤ 1000），表示测试数据组数。每组数据包含一行，12个整数 xA yA zA xB yB zB xC yC zC xD yD zD，分别表示线段AB和CD的端点坐标。所有坐标绝对值不超过1000。

**输出格式**：对于每组测试数据，输出两个整数a b（用空格分隔），表示最短距离的平方的分数表示 a/b（最简分数）。例如距离的平方=4/25输出"4 25"。

### 解题思路
三维空间中两条线段的最短距离问题，需要分情况讨论：

1. **异面直线（含相交直线）**：如果两条线段所在直线不平行且不重合，则存在唯一的公垂线。通过解参数方程得到公垂线的参数s和t：
   - 线段AB：P = A + s·(B-A)，其中0 ≤ s ≤ 1
   - 线段CD：Q = C + t·(D-C)，其中0 ≤ t ≤ 1
   - 公垂线条件：(Q-P)·(B-A) = 0 且 (Q-P)·(D-C) = 0
   - 解得s和t，如果都在[0,1]内，则最短距离为|Q-P|

2. **平行直线或重合直线**：如果线段所在直线平行或重合，最短距离一定在某条线段端点处取得。枚举4个端点：A到线段CD的距离、B到线段CD的距离、C到线段AB的距离、D到线段AB的距离，取最小值。

3. **点到线段距离**：对于点P到线段AB的距离，与二维情况类似但扩展到三维：
   - 若垂足落在线段内，则距离 = |Cross(B-A, P-A)| / |B-A|
   - 否则取端点距离的较小值

### 算法方法
- **分数运算**：使用自定义Rat类进行精确有理数运算（加、减、乘、比较），最终输出最简分数。
- **公垂线参数**：通过叉积和点积求解公垂线方程。
- **整数运算**：所有几何运算使用整数（平方距离和叉积的平方），避免浮点误差。最终用分数表示距离平方。

### 复杂度分析
- **时间复杂度**：O(1)，每次测试常数次操作。T ≤ 1000。
- **空间复杂度**：O(1)。

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
