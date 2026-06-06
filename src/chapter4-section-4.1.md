# 4.1 二维几何基础

## 例题2  好看的一笔画（That Nice Euler Circuit, Shanghai 2004, LA3263）

### 题目描述
给定平面上一条折线（由N个顶点依次连接而成），折线的各边可能相交。求这条折线将平面分成了多少个区域（面片）。

**输入格式**：输入包含多组测试数据，每组以N=0结束。每组第一行是一个整数N（N ≤ 300），表示折线的顶点数。接下来N行，每行两个整数 x y，表示第i个顶点的坐标，坐标绝对值不超过300。折线从第一个顶点开始，依次连接相邻的N-1条线段，即(0,1), (1,2), ..., (N-2, N-1)。

**输出格式**：对于每组测试数据，输出一行 `Case X: There are Y pieces.`，其中X是测试数据编号（从1开始），Y是平面被分割成的区域数。

### 解题思路

**问题本质**：一条折线（可能自交）把平面"切开"成了几块？这是一个经典的平面图计数问题。

**核心工具：欧拉定理**（平面图的欧拉公式）

对于平面的任意平面图（边不相交的图），有：**V - E + F = 2**

其中：
- **V = 顶点数（Vertex）**：所有线段端点 + 所有交点
- **E = 边数（Edge）**：平面上被交点分割成的所有小段
- **F = 面数（Face）**：被分割成的区域数（包括最外面的"无限面"）

**但是这个折线自交了！** 所以不能直接用原始折线当平面图。需要先把所有交点和交点分割后的小段提取出来。

**步骤 1：找所有交点，一并作为顶点（V）**

枚举所有不相邻的线段对 `(i→i+1, j→j+1)`（相邻线段共享端点，不算"相交"）。

如果两条线段规范相交（交点严格在两条线段内部），用直线求交公式算出交点坐标，加入到顶点集合中。使用 `set<Point>` 自动去重。

**最终 V = 原始 N 个顶点 + 所有新增交点**。

**步骤 2：计算边数（E）—— 每条原始线段被交点分割成多段**

初始化 E = N - 1（折线有 N-1 条原始线段）。

对于顶点的集合中**每个顶点**（包括原始顶点和交点），检查它是否落在某条原始线段上（且不是端点）：
- 如果是：说明该顶点把这条线段"切断"成两段 → **E++**
- 直观理解：一条线段上每多一个点，就多一段

**步骤 3：代入欧拉定理**：F = E - V + 2

**给初学者的直观理解**：

拿一个三角形（N=3, V=3, E=3）：F = 3 - 3 + 2 = 2（内部 1 个面 + 外部 1 个面）。

如果三角形内部画一条对角线：V 增加 1（交点），E 增加 3（原线段被切断每段+1，对角新线断成两段），F = (3+3) - (3+1) + 2 = 4（分成了 4 块）。

这就是欧拉定理的威力——不用数区域，只数顶点和边就能算出面数！

### 算法方法
- **向量叉积**：`Cross(a2-a1, b1-a1)` 用于判断点b1在向量a1→a2的哪一侧，正负号反映方向。
- **规范相交判断**：使用叉积符号 `dcmp(c1)*dcmp(c2) < 0` 判断两端点在直线的异侧，双向判断确保线段规范相交。
- **直线求交**：参数方程 `P + t*v = Q + s*w`，通过 `t = Cross(w, P-Q) / Cross(v, w)` 解出参数t。
- **点在线上判断**：先判断叉积为0（三点共线），再判断点积<0（P在A和B之间）。
- **集合去重**：使用 `set<Point>` 对顶点自动排序去重，确保欧拉定理中的V正确。

### 复杂度分析
- **时间复杂度**：O(N³)。枚举所有线段对需要O(N²)时间；对于每个交点（最坏O(N²)个），需要遍历所有N条线段判断点是否在线段上，需要O(N²·N) = O(N³)时间。由于N ≤ 300，最坏约27×10⁶次操作，在可接受范围内。
- **空间复杂度**：O(N²)。顶点集合最多包含N个原始顶点 + C(N,2)个交点，即O(N²)个点。折线顶点存储O(N)。

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
const double eps = 1e-10;                // 浮点数精度阈值
int dcmp(double x) { if (fabs(x) < eps) return 0; return x < 0 ? -1 : 1; }  // 浮点数三态比较
int dcmp(double x, double y) { return dcmp(x - y); }

// 二维点/向量结构体
struct Point {
  double x, y;
  Point(double x = 0, double y = 0) : x(x), y(y) {}
  Point& operator=(const Point& p) {
    x = p.x, y = p.y;
    return *this;
  }
};
typedef Point Vector;

// 向量基本运算
Vector operator+(const Vector& A, const Vector& B) { return Vector(A.x + B.x, A.y + B.y); }  // 加法
Vector operator-(const Point& A, const Point& B) { return Vector(A.x - B.x, A.y - B.y); }     // 减法
Vector operator*(const Vector& A, double p) { return Vector(A.x * p, A.y * p); }              // 数乘
bool operator==(const Point& a, const Point& b) { return a.x == b.x && a.y == b.y; }          // 相等
bool operator<(const Point& p1, const Point& p2) {  // 排序比较（先x后y，用于set）
  if (p1.x != p2.x) return p1.x < p2.x;
  return p1.y < p2.y;
}
double Dot(const Vector& A, const Vector& B) { return A.x * B.x + A.y * B.y; }  // 点积：A·B = |A||B|cosθ
double Length(const Vector& A) { return sqrt(Dot(A, A)); }                       // 向量模长
double Angle(const Vector& A, const Vector& B) { return acos(Dot(A, B) / Length(A) / Length(B)); } // 夹角
double Cross(const Vector& A, const Vector& B) { return A.x * B.y - A.y * B.x; } // 叉积：A×B = |A||B|sinθ
Vector Rotate(Vector A, double rad) { return Vector(A.x * cos(rad) - A.y * sin(rad), A.x * sin(rad) + A.y * cos(rad)); } // 向量旋转
Vector Normal(Vector A) {  // 单位法向量（逆时针旋转90°）
  double L = Length(A);
  return Vector(-A.y / L, A.x / L);
}

// 判断两线段是否规范相交（交点严格在两条线段内部，不相交于端点）
bool SegmentProperIntersection(const Point& a1, const Point& a2, const Point& b1, const Point& b2) {
  double c1 = Cross(a2 - a1, b1 - a1), c2 = Cross(a2 - a1, b2 - a1),  // b1、b2在直线a1a2两侧
         c3 = Cross(b2 - b1, a1 - b1), c4 = Cross(b2 - b1, a2 - b1);  // a1、a2在直线b1b2两侧
  return dcmp(c1) * dcmp(c2) < 0 && dcmp(c3) * dcmp(c4) < 0;          // 双向异侧判定
}

// 求直线P+t*v与Q+s*w的交点（参数方程法）
Point GetLineIntersection(Point P, Vector v, Point Q, Vector w) {
  Vector u = P - Q;                         // P到Q的向量
  double t = Cross(w, u) / Cross(v, w);     // 解参数方程得t值
  return P + v * t;                          // 代入t得到交点
}

// 判断点P是否在线段a1a2上（不含端点）
bool OnSegment(const Point& p, const Point& a1, const Point& a2) {
  return dcmp(Cross(a1 - p, a2 - p)) == 0 && dcmp(Dot(a1 - p, a2 - p)) < 0;  // 共线且在线段内部
}

istream& operator>>(istream& is, Point& p) { return is >> p.x >> p.y; }
ostream& operator<<(ostream& os, const Point& p) { return os << p.x << " " << p.y; }

int main() {
  int N;
  for (int t = 1; cin >> N && N; t++) {
    Point p;
    set<Point> all_points;   // 所有顶点集合（折线顶点+交点），set自动去重
    vector<Point> ps;         // 折线顶点序列
    _for(i, 0, N) cin >> p, ps.push_back(p), all_points.insert(p);  // 读入顶点
    int E = --N;              // 初始边数E = 折线段数 = N-1（--N后N即为段数）
    // 枚举所有线段对，找出规范相交的交点
    _for(i, 0, N) _for(j, i + 1, N) 
      if (SegmentProperIntersection(ps[i], ps[i + 1], ps[j], ps[j + 1]))  // 规范相交
        all_points.insert(GetLineIntersection(ps[i], ps[i + 1] - ps[i], ps[j], ps[j + 1] - ps[j])); // 交点加入顶点集

    // 统计边数：每个顶点每落在线段上一次，该线段被断开一次，边数+1
    for(set<Point>::iterator si = all_points.begin(); si != all_points.end(); si++)
      _for(i, 0, N) if (OnSegment(*si, ps[i], ps[i + 1])) E++;
    // 欧拉定理 V - E + F = 2 => F = E + 2 - V
    int F = E + 2 - all_points.size(); // V+F-E=2, 点，面，边
    printf("Case %d: There are %d pieces.\n", t, F);
  }
  return 0;
}
// Accepted 422ms 1300kB 3093 G++ 2020-12-14 14:16:59 22208849
```

## 例题1  Morley定理（Morley's Theorem, UVa 11178）

### 题目描述
给定三角形ABC的三个顶点坐标，求其Morley三角形的三个顶点D、E、F的坐标。

Morley定理指出：任意三角形的每个内角的三等分线中，靠近每边的两条三等分线的交点构成一个等边三角形（Morley三角形）。具体来说，对于三角形ABC，顶点D是由B处∠ABC靠近BC边的三等分线与C处∠ACB靠近CB边的三等分线的交点；类似地E对应B、F对应C。

**输入格式**：第一行是整数T（T ≤ 100），表示测试数据组数。接下来T行，每行包含6个浮点数 xA yA xB yB xC yC，表示三角形三个顶点的坐标，坐标绝对值不超过1000。

**输出格式**：对于每组测试数据，输出一行包含6个浮点数 xD yD xE yE xF yF，表示Morley三角形的三个顶点坐标，精确到小数点后6位。

### 解题思路

**Morley 定理描述（对初学者的简化版）**：任意三角形的每个内角分成三等份，靠近每条边的两条三等分线的交点，构成一个等边三角形。

**问题**：给定三角形 ABC 的三个顶点坐标，求这个等边三角形的三个顶点 D、E、F。

**1. 构造 D 点的计算步骤**

以顶点 B 为例（求出在 B 附近的三等分线交点）：

① B 处的角 ∠ABC 是向量 BA 与 BC 的夹角
② 将 BC 方向（v1 = C - B）向 BA 方向旋转 ∠ABC/3，得到 B 处的三等分线方向

③ 类似地，C 处：将 CB 方向（v2 = B - C）向 CA 方向旋转 ∠ACB/3，得到 C 处的三等分线方向

④ 两条三等分线的交点 = D

**2. 向量旋转的方向约定**

- 逆时针旋转 = 正角度（+rad）
- 顺时针旋转 = 负角度（-rad）

对于 B 处：BC 到 BA 是逆时针方向 → 旋转 +∠ABC/3
对于 C 处：CB 到 CA 是顺时针方向 → 旋转 -∠ACB/3

**3. 对称性利用**

E 和 F 的计算完全相同，只需将三角形顶点循环轮换：
- D = getD(A, B, C)（B 和 C 处三等分线交点）
- E = getD(B, C, A)（C 和 A 处三等分线交点）
- F = getD(C, A, B)（A 和 B 处三等分线交点）

**4. 核心技术：直线求交**

两条直线 `P + t·v` 和 `Q + s·w` 的交点：
`t = Cross(w, P-Q) / Cross(v, w)`
代入后 `交点 = P + t·v`

这个公式来自解参数方程（两直线方向不平行时，Cross(v,w) ≠ 0）。叉积越大→两条直线越接近垂直→交点越明确。

**初学者提示**：本题的核心是用向量运算代替纯几何推导——只要理解了"旋转方向向量"和"求直线交点"这两个基本操作，就能算出答案。

### 算法方法
- **向量旋转**：使用旋转矩阵 `(x' = xcosθ - ysinθ, y' = xsinθ + ycosθ)`，逆时针旋转θ弧度。
- **角度计算**：通过点积求余弦值 `cosθ = (A·B) / (|A|·|B|)`，再通过 `acos()` 反算角度。
- **直线求交**：对于直线 `P + t·v` 和 `Q + s·w`，通过叉积求参数t：`t = Cross(w, P-Q) / Cross(v, w)`。
- 核心技巧：将几何构造问题参数化，转化为向量运算，避免复杂的纯几何推导。

### 复杂度分析
- **时间复杂度**：O(T)，每组数据执行3次getD调用，每次涉及常数次向量运算（旋转、夹角、求交），总计O(1)。T组数据总复杂度O(T)。
- **空间复杂度**：O(1)，仅需存储三个输入点、三个输出点及少量中间向量，不随输入规模增长。

```cpp
// 例题1  Morley定理（Morley's Theorem, UVa 11178）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
// 二维点/向量结构体
struct Point {
  double x, y;
  Point(double x = 0, double y = 0) : x(x), y(y) {}
};

typedef Point Vector;
// 向量加法
Vector operator+(const Vector& A, const Vector& B) {
  return Vector(A.x + B.x, A.y + B.y);
}
// 向量减法
Vector operator-(const Point& A, const Point& B) {
  return Vector(A.x - B.x, A.y - B.y);
}
// 向量数乘
Vector operator*(const Vector& A, double p) { return Vector(A.x * p, A.y * p); }
// 向量点积：A·B = |A||B|cosθ
double Dot(const Vector& A, const Vector& B) { return A.x * B.x + A.y * B.y; }
// 向量模长
double Length(const Vector& A) { return sqrt(Dot(A, A)); }
// 两向量夹角（弧度）
double Angle(const Vector& A, const Vector& B) {
  return acos(Dot(A, B) / Length(A) / Length(B));  // cosθ = 点积/(|A|*|B|)
}
// 向量叉积：A×B = |A||B|sinθ，正值表示B在A的逆时针方向
double Cross(const Vector& A, const Vector& B) { return A.x * B.y - A.y * B.x; }
// 求直线P+t*v与Q+s*w的交点
Point GetLineIntersection(const Point& P, const Point& v, const Point& Q, const Point& w) {
  Vector u = P - Q;                       // P到Q的向量
  double t = Cross(w, u) / Cross(v, w);   // 叉积法求解参数t
  return P + v * t;                        // 代入参数方程得到交点
}
// 向量逆时针旋转rad弧度
Vector Rotate(const Vector& A, double rad) {
  return Vector(A.x * cos(rad) - A.y * sin(rad), A.x * sin(rad) + A.y * cos(rad));
}
istream& operator>>(istream& is, Point& p) { return is >> p.x >> p.y; }
ostream& operator<<(ostream& os, const Point& p) { return os << p.x << " " << p.y; }

// 求Morley三角形中对应顶点A的那个顶点D
// 参数：三角形三个顶点A、B、C
// 返回：B处∠ABC靠近BC的三等分线与C处∠ACB靠近CB的三等分线的交点
Point getD(Point A, Point B, Point C) {
  Vector v1 = C - B;                     // 边BC的方向向量
  double a1 = Angle(A - B, v1);           // ∠ABC的大小（向量BA与BC的夹角）
  v1 = Rotate(v1, a1 / 3);               // v1向A方向旋转∠ABC/3，得到B处的三等分线方向

  Vector v2 = B - C;                     // 边CB的方向向量
  double a2 = Angle(A - C, v2);           // ∠ACB的大小（向量CA与CB的夹角）
  v2 = Rotate(v2, -a2 / 3);              // v2向A方向旋转-∠ACB/3（顺时针），得到C处的三等分线方向

  return GetLineIntersection(B, v1, C, v2);  // 两条三等分线的交点即D
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);  // 加速I/O
  int T;
  cin >> T;
  for (Point A, B, C; T--;) {
    cin >> A >> B >> C;
    // 循环对称：轮换顶点参数即可求得三个Morley顶点
    Point D = getD(A, B, C), E = getD(B, C, A), F = getD(C, A, B);
    printf("%.6lf %.6lf %.6lf %.6lf %.6lf %.6lf\n", 
      D.x, D.y, E.x, E.y, F.x, F.y);
  }
  return 0;
}
// 24480472 11178 Morley's Theorem  Accepted  C++11 0.020 2020-01-28 13:07:20
```

## 例题3  狗的距离（Dog Distance, UVa 11796）

### 题目描述
甲、乙两条狗分别沿着两条折线路径匀速前进，已知它们的起点、路径折线以及它们同时到达终点的约束。求在整个运动过程中，两条狗之间距离的最大值和最小值。

**输入格式**：第一行是一个整数T（T ≤ 100），表示测试数据组数。每组数据的第一行包含两个整数A和B（2 ≤ A, B ≤ 60），分别表示甲和乙的路径顶点数。接下来A行，每行两个整数x, y，表示甲的路径顶点坐标。再接下来B行，每行两个整数x, y，表示乙的路径顶点坐标。所有坐标绝对值不超过1000。甲和乙分别从各自第一个顶点出发，沿折线移动到最后一个顶点，速度各自恒定但两者的速度可能不同（速度取决于各自的路径总长度，因为两者同时到达终点）。

**输出格式**：对于每组测试数据，输出一行 `Case X: Y`，其中X是测试编号，Y是最大距离与最小距离之差，四舍五入到整数。

### 解题思路

**问题**：两条狗沿折线匀速运动，同时出发同时到达终点，求它们之间距离的最大值和最小值。

**关键挑战**：两条狗速度不同（各自路径总长不同，除以相同时间），且路径是折线（方向会变）。

**1. 归一化时间**：统一速度

设甲狗路径总长 LenA，乙狗路径总长 LenB，同时出发同时到达。
把速度定义为路径长度：**甲速度 = LenA，乙速度 = LenB**。这样在 "1 个单位时间" 内，两条狗恰好各走完全程。

这个归一化让每条狗在每一段上的速度都统一为各自的 Len，避免了复杂的变速计算。

**2. 分段运动 + 双指针推进**

用两个指针 Sa、Sb 分别追踪甲、乙当前在哪一段。
在每一时刻，甲乙各自到下一拐点需要的时间分别 = 剩余距离 / 速度。

取两者中较小的时间 T（在 T 时间内，两者都沿直线匀速运动）：
```
T = min(当前段剩余距离甲 / LenA, 当前段剩余距离乙 / LenB)
```

**3. 相对运动简化（最巧妙的步骤）**

在 T 时间内：
- 甲的位移 Va = 方向 × (T × LenA)
- 乙的位移 Vb = 方向 × (T × LenB)

如果以甲为参照（假设甲静止），乙的相对位移 = Vb - Va。

**问题转化为**：在 T 时间内，甲静止在 Pa，乙从 Pb 匀速移动到 Pb + (Vb-Va)。求动点 Pa 到线段 [Pb, Pb+Vb-Va] 的距离范围。

**4. 更新最值**

- 最小距离：点 Pa 到线段 [Pb, Pb+Vb-Va] 的最短距离（垂足距离或端点距离）
- 最大距离：点 Pa 到线段两端点距离的最大值

**5. 推进和处理拐点**

移动 T 时间后，甲和乙到达新位置。如果某一狗到达了拐点（恰好在线段端点），推进其指针到下一段。

重复直到两者都到达终点。

**给初学者的关键理解**：这段代码最精妙的地方是把"两个动点"的问题转化为"一个静止、一个移动"的问题（相对运动），同时通过归一化时间让分段变得可行。

### 算法方法
- **点到线段距离**：分为三种情况——垂足落在线段上（用叉积算垂直距离）、垂足偏向一端（用端点到P的距离）。
- **归一化时间**：利用"同时到达终点"的约束，将不同的速度统一到公共的时间轴上。
- **双指针推进**：模拟两个动点的运动，每当到达拐点就推进对应指针。

### 复杂度分析
- **时间复杂度**：O(A + B)。双指针Sa和Sb各自从0推进到终点，每个指针最多移动A-1或B-1次，每次操作O(1)。总时间复杂度为O(A + B)，每组最多约120次迭代。T ≤ 100，总操作约12000次。
- **空间复杂度**：O(max(A, B))，需要存储两条折线的顶点坐标，最大60个点。

```cpp
// 例题3  狗的距离（Dog Distance, UVa 11796）
// Rujia Liu
#include<cstdio>
#include<cmath>
#include<algorithm>
using namespace std;

const double eps = 1e-8;                // 浮点数比较精度
int dcmp(double x) { if(fabs(x) < eps) return 0; else return x < 0 ? -1 : 1; }  // 三态比较

const double PI = acos(-1.0);
double torad(double deg) { return deg/180 * PI; }  // 角度转弧度

// 二维点/向量结构体
struct Point {
  double x, y;
  Point(double x=0, double y=0):x(x),y(y) { }
};

typedef Point Vector;

// 向量基本运算
Vector operator + (const Vector& A, const Vector& B) { return Vector(A.x+B.x, A.y+B.y); }
Vector operator - (const Point& A, const Point& B) { return Vector(A.x-B.x, A.y-B.y); }
Vector operator * (const Vector& A, double p) { return Vector(A.x*p, A.y*p); }
Vector operator / (const Vector& A, double p) { return Vector(A.x/p, A.y/p); }

// 点排序（先x后y）
bool operator < (const Point& a, const Point& b) {
  return a.x < b.x || (a.x == b.x && a.y < b.y);
}

// 点相等判断（含浮点误差）
bool operator == (const Point& a, const Point &b) {
  return dcmp(a.x-b.x) == 0 && dcmp(a.y-b.y) == 0;
}

Point read_point() {  // 读取一个点
  double x, y;
  scanf("%lf%lf", &x, &y);
  return Point(x, y);
};

double Dot(const Vector& A, const Vector& B) { return A.x*B.x + A.y*B.y; }  // 点积
double Length(const Vector& A) { return sqrt(Dot(A, A)); }                   // 模长
double Cross(const Vector& A, const Vector& B) { return A.x*B.y - A.y*B.x; } // 叉积

// 求点P到线段AB的最短距离
double DistanceToSegment(const Point& P, const Point& A, const Point& B) {
  if(A == B) return Length(P-A);                // 退化为点，直接求两点距离
  Vector v1 = B - A, v2 = P - A, v3 = P - B;    // 线段方向向量、P到两端的向量
  // 判断垂足位置
  if(dcmp(Dot(v1, v2)) < 0) return Length(v2);  // 垂足在A的外侧，距离为PA
  else if(dcmp(Dot(v1, v3)) > 0) return Length(v3);  // 垂足在B的外侧，距离为PB
  else return fabs(Cross(v1, v2)) / Length(v1);  // 垂足在线段上，用平行四边形面积/底边=高
}

const int maxn = 60;
int T, A, B;
Point P[maxn], Q[maxn];  // 两条折线的顶点
double Min, Max;          // 全局最小和最大距离

// 更新最小、最大距离：点P到线段AB的最近距离，以及P到A、B的距离
void update(Point P, Point A, Point B) {
  Min = min(Min, DistanceToSegment(P, A, B));  // 更新最小距离（点到线段）
  Max = max(Max, Length(P-A));                  // 更新最大距离（到端点A）
  Max = max(Max, Length(P-B));                  // 更新最大距离（到端点B）
}

int main() {
  scanf("%d", &T);
  for(int kase = 1; kase <= T; kase++) {
    scanf("%d%d", &A, &B);
    for(int i = 0; i < A; i++) P[i] = read_point();  // 读入甲路径
    for(int i = 0; i < B; i++) Q[i] = read_point();  // 读入乙路径

    double LenA = 0, LenB = 0;
    for(int i = 0; i < A-1; i++) LenA += Length(P[i+1]-P[i]);  // 甲路径总长
    for(int i = 0; i < B-1; i++) LenB += Length(Q[i+1]-Q[i]);  // 乙路径总长

    int Sa = 0, Sb = 0;               // 双指针：当前所在的线段编号
    Point Pa = P[0], Pb = Q[0];        // 当前的位置
    Min = 1e9, Max = -1e9;             // 初始化极值
    while(Sa < A-1 && Sb < B-1) {      // 两者都未到达终点
      double La = Length(P[Sa+1] - Pa); // 甲到下一拐点的距离
      double Lb = Length(Q[Sb+1] - Pb); // 乙到下一拐点的距离
      // 归一化时间：取到达各自下一拐点所需时间的最小值
      // 速度统一为各自路径总长，使得两者同时到达终点
      double T = min(La/LenA, Lb/LenB); // 取合适的单位，可以让甲和乙的速度分别是LenA和LenB
      // 计算T时间内各自位移向量
      Vector Va = (P[Sa+1] - Pa)/La*T*LenA; // 甲的位移向量
      Vector Vb = (Q[Sb+1] - Pb)/Lb*T*LenB; // 乙的位移向量
      // 相对运动简化：甲视为静止，乙相对于甲运动
      update(Pa, Pb, Pb+Vb-Va); // 求解"简化版"，更新最小最大距离
      Pa = Pa + Va;              // 甲到达新位置
      Pb = Pb + Vb;              // 乙到达新位置
      // 检查是否到达拐点，到达则推进指针
      if(Pa == P[Sa+1]) Sa++;    // 甲到达下一拐点
      if(Pb == Q[Sb+1]) Sb++;    // 乙到达下一拐点
    }
    printf("Case %d: %.0lf\n", kase, Max-Min);  // 输出最大最小距离之差
  }
  return 0;
}
// 25877735	11796	Dog Distance	Accepted	C++	0.010	2020-12-23 06:37:09
```
