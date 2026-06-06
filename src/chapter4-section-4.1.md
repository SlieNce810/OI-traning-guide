# 4.1 二维几何基础

> **学习目标**：掌握二维向量运算体系与浮点精度处理策略，用代数语言精确描述几何关系

## 理论基础

### 为什么需要学这个？

想象一下：给你一个三角形和一条线段，让你判断它们是否相交。如果纯用几何直觉——画图、量距离、看位置——不仅效率低，代码也写不出一行。计算几何的核心思想，就是把"看图说话"转化为"代数运算"。向量就是这中间的语言翻译官：两点相减得到方向，叉积判断左右，点积衡量远近，旋转矩阵改变方向——这些看似简单的操作，组合起来就能描述平面上的任何几何关系。

等你掌握了这些基本工具，就会发现：之前让人头疼的"点是否在多边形内"、"线段是否相交"、"多边形面积"这些问题，全都可以用三四行公式搞定。更重要的是，这些工具是你后面学习凸包、半平面交、旋转卡壳等高级算法的地基——地基不牢，后面的高楼根本建不起来。

### 核心概念

**1. 向量与基本运算**

向量本质上是一个从原点出发的有向箭头，用 `Vector(x, y)` 表示。两个点 A 和 B 相减 `B - A` 就得到了从 A 指向 B 的向量。

最小的代码骨架：
```cpp
struct Point { double x, y; };
typedef Point Vector;
Vector operator-(const Point& A, const Point& B) { return Vector(A.x-B.x, A.y-B.y); }
```

真正的威力在点积和叉积：
- **点积** `Dot(A, B) = A.x*B.x + A.y*B.y = |A||B|cosθ`：判断两向量夹角。正→锐角，零→垂直，负→钝角。配合 `acos` 可直接算角度。
- **叉积** `Cross(A, B) = A.x*B.y - A.y*B.x = |A||B|sinθ`：判断方向与面积。正→B 在 A 逆时针方向，零→共线，负→顺时针。几何意义是平行四边形有向面积的 2 倍。

**右手定则**是理解叉积符号的直观工具：伸出右手，四指从 A 弯向 B（沿较小夹角方向），若拇指朝上（指向屏幕外/z轴正方向），则 `Cross(A,B) > 0`，B 在 A 的逆时针方向；若拇指朝下，则 `Cross(A,B) < 0`，B 在 A 的顺时针方向。在二维平面中，叉积退化为标量，其符号恰好对应 z 分量的正负——`Cross(A,B)` 就是三维叉积 `A×B` 的 z 分量值。这也解释了为什么"逆时针为正"：在标准右手坐标系中，从 x 轴转向 y 轴时拇指指向 z 轴正方向。

**2. 点线面关系判断**

所有线段相关判断都归结为两个函数的组合：
- **OnSegment(P, A, B)**：先 `Cross(A-P, B-P) == 0`（三点共线），再 `Dot(A-P, B-P) < 0`（P 在中间），两步确认 P 在线段 AB 上。
- **SegmentProperIntersection**：线段 AB 与 CD 规范相交 = A、B 在直线 CD 两侧 **且** C、D 在直线 AB 两侧。用 `dcmp(c1)*dcmp(c2) < 0` 的异侧判断。

一条线段、一条直线、一个多边形——归根到底都是向量运算的不同组合。

**3. 浮点精度：eps 的艺术**

几何计算绕不过浮点误差。`0.1 + 0.2 != 0.3` 是每个竞赛选手都会踩的坑。标准做法：
```cpp
const double eps = 1e-10;
int dcmp(double x) { if (fabs(x) < eps) return 0; return x < 0 ? -1 : 1; }
```
- `eps` 不能太小（10⁻¹² 会误判共线），也不能太大（10⁻⁶ 会误判相交）。**经验值 10⁻⁸ 到 10⁻¹⁰ 最常用**。
- 比较 `a == b` 写成 `dcmp(a-b) == 0`，`a < b` 写成 `dcmp(a-b) < 0`。
- 排序用 `operator<` 时不要在内部加 eps——可能导致 `a<b`、`b<c`、`c<a` 的传递性失效。

**浮点比较的三个层次**：第一层是**绝对误差**（`fabs(a-b) < eps`），即 `dcmp` 的做法，适用于数值范围已知且不大的情况。第二层是**相对误差**（`fabs(a-b) / max(fabs(a), fabs(b)) < eps`），当比较的数值本身可能很大时更可靠——10000.00 和 10000.01 的绝对差为 0.01，但相对差仅 10⁻⁶，比固定 ε 更有意义。第三层是**ULP比较**（Unit in the Last Place），直接比较两个浮点数二进制表示的最后一位之差，需要操作内存表示（如 `memcmp`），在几何竞赛中很少使用，但它是最接近"机器级精确"的比较方式。竞赛编程中 99% 的情况使用第一层（`dcmp`）即可，但理解后两层有助于在极端数据下定位精度问题。

**4. 欧拉定理 V - E + F = 2**

这是几何数数的"核武器"。任意平面图（边不相交），顶点数 V、边数 E、面数 F 满足 `V - E + F = 2`。你不需要数面，只需数顶点和边，代入公式直接得到答案。本章例题 2 就是经典应用题：把自交折线的交点全部找出来当顶点，原边被交点分割后重新数边数，代公式算出区域数。

**5. 向量旋转公式的推导**

旋转矩阵 `Rotate(A, θ)` 的公式 `(x·cosθ - y·sinθ, x·sinθ + y·cosθ)` 是怎么来的？有两种等价推导方式。**复数法**：将向量 A 看作复数 `z = x + iy`，逆时针旋转 θ 等价于乘以单位复数 `e^(iθ) = cosθ + i·sinθ`，即 `(x+iy)(cosθ+i·sinθ) = (x·cosθ - y·sinθ) + i(x·sinθ + y·cosθ)`，实部虚部分别对应 x' 和 y'。**三角恒等式法**：设 A 的极角为 α，则 `x = r·cosα, y = r·sinα`。旋转后极角变为 α+θ，代入和角公式得 `x' = r·cos(α+θ) = r(cosα·cosθ - sinα·sinθ) = x·cosθ - y·sinθ`，同理 `y' = r·sin(α+θ) = x·sinθ + y·cosθ`。两种观点殊途同归，复数视角更简洁地体现了"旋转即乘法"的本质。

### 知识脉络

```
向量基本运算（点积、叉积）
    ├── 点线关系判断（OnSegment、求交、规范相交）
    │       └── 浮点精度处理（dcmp + eps）
    │               └── 基础几何操作（距离、角度、面积）
    └── 图论组合（欧拉定理 V-E+F=2）
```

所有高级算法都建立在这几个基础操作之上。先学会"点积和叉积能做什么"，再用它们解决"点是否在线段上"、"线段是否相交"等具体问题。

**本书跨章节连接**：几何中的**二分判定策略**与第 1.2 节的二分答案方法一脉相承——在几何判定问题中（如"是否存在满足距离约束的点"），二分搜索负责缩小搜索范围，几何的计算操作用来判定可行性。本章的向量运算体系是所有后续几何章节（4.2 圆、4.3 凸包/半平面交、4.4 三维几何）的共同基础。欧拉定理 V-E+F=2 则在第 3.2 节的图论类问题中有类似的结构——用拓扑不变量代替直接计数。

### 快速上手模板

竞赛中最常用的二维几何结构体。这个模板是本章所有例题的地基，建议熟记并手写练习至少三遍：

```cpp
#include <cmath>
const double eps = 1e-10;
int dcmp(double x) { if (fabs(x) < eps) return 0; return x < 0 ? -1 : 1; }

struct Point {
    double x, y;
    Point(double x = 0, double y = 0) : x(x), y(y) {}
};
typedef Point Vector;

// 向量四则运算
Vector operator+(const Vector& A, const Vector& B) { return Vector(A.x+B.x, A.y+B.y); }
Vector operator-(const Point& A, const Point& B)  { return Vector(A.x-B.x, A.y-B.y); }
Vector operator*(const Vector& A, double p)        { return Vector(A.x*p, A.y*p); }
Vector operator/(const Vector& A, double p)        { return Vector(A.x/p, A.y/p); }
bool operator<(const Point& a, const Point& b)
{ return a.x < b.x || (a.x == b.x && a.y < b.y); }

// 核心运算
double Dot(const Vector& A, const Vector& B)   { return A.x*B.x + A.y*B.y; }
double Length(const Vector& A)                  { return sqrt(Dot(A, A)); }
double Cross(const Vector& A, const Vector& B) { return A.x*B.y - A.y*B.x; }

// 高频功能：旋转、角度、法向量
Vector Rotate(Vector A, double rad)
{ return Vector(A.x*cos(rad)-A.y*sin(rad), A.x*sin(rad)+A.y*cos(rad)); }
double Angle(const Vector& A, const Vector& B)
{ return acos(Dot(A,B) / Length(A) / Length(B)); }
Vector Normal(Vector A) { double L = Length(A); return Vector(-A.y/L, A.x/L); }

// 直线求交：P+t*v 与 Q+s*w → t = Cross(w,P-Q)/Cross(v,w)
Point GetLineIntersection(Point P, Vector v, Point Q, Vector w)
{ Vector u = P-Q; double t = Cross(w,u)/Cross(v,w); return P+v*t; }
```

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
