# 1.3 高效算法设计举例

## 例题25  侏罗纪（Jurassic Remains, NEERC 2003, Codeforces Gym101388J）

```cpp
// 例题25  侏罗纪（Jurassic Remains, NEERC 2003, Codeforces Gym101388J）
// Rujia Liu
#include<cstdio>
#include<map>
using namespace std;

const int maxn = 24;
map<int,int> table;

int bitcount(int x) { return x == 0 ? 0 : bitcount(x/2) + (x&1); }

int main() {
  int n, A[maxn];
  char s[1000];

  freopen("jurassic.in", "r", stdin);
  freopen("jurassic.out","w",stdout);

  while(scanf("%d", &n) == 1 && n) {
    // 输入并计算每个字符串对应的位向量
    for(int i = 0; i < n; i++) {
      scanf("%s", s);
      A[i] = 0;
      for(int j = 0; s[j] != '\0'; j++) A[i] ^= (1<<(s[j]-'A'));
    }
    // 计算前n1个元素的所有子集的xor值
    // table[x]保存的是xor值为x的，bitcount尽量大的子集
    table.clear();
    int n1 = n/2, n2 = n-n1;
    for(int i = 0; i < (1<<n1); i++) {
      int x = 0;
      for(int j = 0; j < n1; j++) if(i & (1<<j)) x ^= A[j];
      if(!table.count(x) || bitcount(table[x]) < bitcount(i)) table[x] = i;
    }
    // 枚举后n2个元素的所有子集，并在table中查找
    int ans = 0;
    for(int i = 0; i < (1<<n2); i++) {
      int x = 0;
      for(int j = 0; j < n2; j++) if(i & (1<<j)) x ^= A[n1+j];
      if(table.count(x)&&bitcount(ans)<bitcount(table[x])+bitcount(i)) ans = (i<<n1)^table[x];
    }
    // 输出结果
    printf("%d\n", bitcount(ans));
    for(int i = 0; i < n; i++) if(ans & (1<<i)) printf("%d ", i+1);
    printf("\n");
  }
  return 0;
}
// 102052000	Dec/22/2020 22:56UTC+8	chenwz	J - Jurassic Remains	GNU C++11	Accepted	31 ms	300 KB
```

## 例题22  最大子矩阵（City Game, SEERC 2004, LA3029/POJ1964）

```cpp
// 例题22  最大子矩阵（City Game, SEERC 2004, LA3029/POJ1964）
// 刘汝佳
#include <algorithm>
#include <cstdio>
using namespace std;

const int maxn = 1000;
int mat[maxn][maxn], up[maxn][maxn], left[maxn][maxn], right[maxn][maxn];
int main() {
  int T;
  scanf("%d", &T);
  while (T--) {
    int m, n;
    scanf("%d%d", &m, &n);
    for (int i = 0; i < m; i++)
      for (int j = 0; j < n; j++) {
        int ch = getchar();
        while (ch != 'F' && ch != 'R') ch = getchar();
        mat[i][j] = ch == 'F' ? 0 : 1;
      }

    int ans = 0;
    for (int i = 0; i < m; i++) {  //从上到下逐行处理
      int lo = -1, ro = n;
      for (int j = 0; j < n; j++)  //从左到右扫描，维护up和left
        if (mat[i][j] == 1) {
          up[i][j] = left[i][j] = 0;
          lo = j;
        } else {
          up[i][j] = i == 0 ? 1 : up[i - 1][j] + 1;
          left[i][j] = i == 0 ? lo + 1 : max(left[i - 1][j], lo + 1);
        }
      for (int j = n - 1; j >= 0; j--)  //从右到左扫描，维护right并更新答案
        if (mat[i][j] == 1) {
          right[i][j] = n;
          ro = j;
        } else {
          right[i][j] = i == 0 ? ro - 1 : min(right[i - 1][j], ro - 1);
          ans = max(ans, up[i][j] * (right[i][j] - left[i][j] + 1));
        }
    }
    printf("%d\n", ans * 3);  //输出最大面积乘以3后的结果
  }
  return 0;
}
// Accepted 32ms 15988kB 1252 G++ 2020-12-08 21:55:10 22197363
```

## 例题21  子序列（Subsequence, SEERC 2006, POJ3061）

```cpp
// 例题21  子序列（Subsequence, SEERC 2006, POJ3061）
// 陈锋
#include <algorithm>
#include <cstdio>
using namespace std;

const int maxn = 1e5 + 8;
int A[maxn], B[maxn], T;
int main() {
  scanf("%d", &T);
  for (int n, S; scanf("%d%d", &n, &S) == 2 && T--;) {
    for (int i = 1; i <= n; i++) scanf("%d", &A[i]);
    B[0] = 0;
    for (int i = 1; i <= n; i++) B[i] = B[i - 1] + A[i];
    int ans = n + 1, i = 1;
    for (int j = 1; j <= n; j++) {
      if (B[i - 1] > B[j] - S) continue;  // (1)没有满足条件的i，换下一个j
      while (B[i] <= B[j] - S) i++;  // (2)求满足B[i-1]<=B[j]-S的最大i
      ans = min(ans, j - i + 1);
    }
    printf("%d\n", ans == n + 1 ? 0 : ans);
  }
  return 0;
}
// Accepted 79ms 1104kB 731 G++2020-12-24 10:55:33 22229063
```

## 例题23  遥远的银河（Distant Galaxy, Shanghai 2006, POJ3141/LA3695）

```cpp
// 例题23  遥远的银河（Distant Galaxy, Shanghai 2006, POJ3141/LA3695）
// Rujia Liu
#include<cstdio>
#include<algorithm>
using namespace std;

struct Point {
  int x, y;
  bool operator < (const Point& rhs) const {
    return x < rhs.x;
  }
};

const int maxn = 100 + 10;
Point P[maxn];
int n, m, y[maxn], on[maxn], on2[maxn], left[maxn];

int solve() {
  sort(P, P+n);
  sort(y, y+n);
  m = unique(y, y+n) - y; // 所有不同的y坐标的个数
  if(m <= 2) return n; // 最多两种不同的y

  int ans = 0;
  for(int a = 0; a < m; a++)
    for(int b = a+1; b < m; b++) {
      int ymin = y[a], ymax = y[b]; // 计算上下边界分别为ymin和ymax时的解

      // 计算left, on, on2
      int k = 0;
      for(int i = 0; i < n; i++) {
        if(i == 0 || P[i].x != P[i-1].x) { // 一条新的竖线
          k++;
          on[k] = on2[k] = 0;
          left[k] = k == 0 ? 0 : left[k-1] + on2[k-1] - on[k-1];
        } 
        if(P[i].y > ymin && P[i].y < ymax) on[k]++;
        if(P[i].y >= ymin && P[i].y <= ymax) on2[k]++;
      }
      if(k <= 2) return n; // 最多两种不同的x

      int M = 0;
      for(int j = 1; j <= k; j++) {
        ans = max(ans, left[j]+on2[j]+M);
        M = max(M, on[j]-left[j]);
      }
    }
  return ans;
}

int main() {
  int kase = 0;
  while(scanf("%d", &n) == 1 && n) {
    for(int i = 0; i < n; i++) { scanf("%d%d", &P[i].x, &P[i].y); y[i] = P[i].y; }
    printf("Case %d: %d\n", ++kase, solve());
  }
  return 0;
}
// Accepted 16ms 352kB 1338 G++2020-12-22 22:50:02 22226059
```

## UVa10755 Garbage heap

```cpp
// UVa10755 Garbage heap
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<algorithm>
#define FOR(i,s,t)  for(int i = (s); i <= (t); ++i)
using namespace std;

void expand(int i, int& b0, int& b1, int& b2) {
  b0 = i&1; i >>= 1;
  b1 = i&1; i >>= 1;
  b2 = i&1;
}

int sign(int b0, int b1, int b2) {
  return (b0 + b1 + b2) % 2 == 1 ? 1 : -1;
}

const int maxn = 30;
const long long INF = 1LL << 60;

long long S[maxn][maxn][maxn];

long long sum(int x1, int x2, int y1, int y2, int z1, int z2) {
  int dx = x2-x1+1, dy = y2-y1+1, dz = z2-z1+1;
  long long s = 0;
  for(int i = 0; i < 8; i++) {
    int b0, b1, b2;
    expand(i, b0, b1, b2);
    s -= S[x2-b0*dx][y2-b1*dy][z2-b2*dz] * sign(b0, b1, b2);
  }
  return s;
}

int main() {
  int T;
  scanf("%d", &T);
  while(T--) {
    int a, b, c, b0, b1, b2;
    scanf("%d%d%d", &a, &b, &c);
    memset(S, 0, sizeof(S));
    FOR(x,1,a) FOR(y,1,b) FOR(z,1,c) scanf("%lld", &S[x][y][z]);
    FOR(x,1,a) FOR(y,1,b) FOR(z,1,c) FOR(i,1,7){
      expand(i, b0, b1, b2);
      S[x][y][z] += S[x-b0][y-b1][z-b2] * sign(b0, b1, b2);
    }
    long long ans = -INF;
    FOR(x1,1,a) FOR(x2,x1,a) FOR(y1,1,b) FOR(y2,y1,b) {
      long long M = 0;
      FOR(z,1,c) {
        long long s = sum(x1,x2,y1,y2,1,z);
        ans = max(ans, s - M);
        M = min(M, s);
      }
    }
    printf("%lld\n", ans);
    if(T) printf("\n");
  }
  return 0;
}
// 25875865	10755	Garbage Heap	Accepted	C++	0.210	2020-12-22 14:49:13
```

## 例题18  开放式学分制（Open Credit System, UVa 11078）

```cpp
// 例题18  开放式学分制（Open Credit System, UVa 11078）
// 陈锋
#include <cassert>
#include <cstdio>
#include <algorithm>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
const int MAXN = 1e5 + 4;
int A[MAXN];
int main() {
  int n, T;
  scanf("%d", &T);
  while (T--) {
    scanf("%d", &n);
    _for(i, 0, n) scanf("%d", &(A[i]));
    int m = A[0], ans = A[0] - A[1];  // maxA[i]
    _for(i, 1, n) // m is max{A0, A1, A_{i-1}}      
      ans = max(m - A[i], ans), m = max(A[i], m);
    printf("%d\n", ans);
  }
  return 0;
}
// 18756057	11078	Open Credit System	Accepted	C++11	0.060	2017-02-10 14:12:42
```

## 例题17  年龄排序（Age Sort, UVa 11462）

```cpp
// 例题17  年龄排序（Age Sort, UVa 11462）
// 陈锋
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
const int MAXN = 100;
int main() {
  int n, a, cnt[MAXN + 4];
  while (scanf("%d", &n) == 1 && n) {
    fill_n(cnt, MAXN + 4, 0);
    _for(i, 0, n) scanf("%d", &a), ++cnt[a];
    _for(i, 0, MAXN) _for(j, 0, cnt[i])
      printf("%d%s", i, (i == MAXN - 1 && j == cnt[i] - 1) ? "" : " ");
    puts("");
  }
}
// 25875806	11462	Age Sort	Accepted	C++	0.250	2020-12-22 14:38:05
```

## 例题19  计算器谜题（Calculator Conundrum, UVa 11549）

```cpp
// 例题19  计算器谜题（Calculator Conundrum, UVa 11549）
// 陈锋
#include <iostream>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
LL K, M;
LL next(LL x) {
  LL ans = x * x;
  while (ans >= M) ans /= 10;
  return ans;
}
int main() {
  int T, n;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%lld", &n, &K);
    M = 1;
    _for(i, 0, n) M *= 10;
    LL ans = K, k1 = K, k2 = K;
    do {
      k1 = next(k1), ans = max(ans, k1);
      k2 = next(k2), ans = max(ans, k2);
      k2 = next(k2), ans = max(ans, k2);
    } while (k1 != k2);
    printf("%lld\n", ans);
  }
}
// 21699036 11549 Calculator Conundrum Accepted C++11 0.050 2018-07-28 07:37:08
```

## UVa1398 Meteor (整数版本, 更快)

```cpp
// UVa1398 Meteor (整数版本, 更快)
// 刘汝佳
#include <algorithm>
#include <cstdio>
using namespace std;
// 0<x+at<w
void update(int x, int a, int w, int& L, int& R) {
  if (a == 0) {
    if (x <= 0 || x >= w) R = L - 1;  // 无解
  } else if (a > 0) {
    L = max(L, -x * 2520 / a);
    R = min(R, (w - x) * 2520 / a);
  } else {
    L = max(L, (w - x) * 2520 / a);
    R = min(R, -x * 2520 / a);
  }
}
const int maxn = 1e5 + 8;

struct Event {
  int x;
  int type;
  bool operator<(const Event& a) const {
    return x < a.x || (x == a.x && type > a.type);  // 先处理右端点
  }
} events[maxn * 2];

int main() {
  int T;
  scanf("%d", &T);
  while (T--) {
    int w, h, n, e = 0;
    scanf("%d%d%d", &w, &h, &n);
    for (int i = 0; i < n; i++) {
      int x, y, a, b;
      scanf("%d%d%d%d", &x, &y, &a, &b);
      // 0<x+at<w, 0<y+bt<h, t>=0
      int L = 0, R = 1e9;
      update(x, a, w, L, R);
      update(y, b, h, L, R);
      if (R > L) {
        events[e++] = (Event){L, 0};
        events[e++] = (Event){R, 1};
      }
    }
    sort(events, events + e);
    int cnt = 0, ans = 0;
    for (int i = 0; i < e; i++) {
      if (events[i].type == 0)
        ans = max(ans, ++cnt);
      else
        cnt--;
    }
    printf("%d\n", ans);
  }
  return 0;
}
// 28685849 UVa1398 Accepted 50ms 1246	C++
```
