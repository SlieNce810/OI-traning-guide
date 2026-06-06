# 1.1 思维的体操

## 例题4  墓地雕塑（Graveyard, NEERC 2006, CodeForces Gym100287G）

```cpp
// 例题4  墓地雕塑（Graveyard, NEERC 2006, CodeForces Gym100287G）
// Rujia Liu
#include<cstdio>
#include<cmath>
using namespace std;

int main() {
  freopen("graveyard.in", "r", stdin);
  freopen("graveyard.out","w",stdout);

  for(int n, m; scanf("%d%d", &n, &m) == 2; ) {
    double ans = 0.0;
    for(int i = 1; i < n; i++) {
      double pos = (double)i / n * (n+m); //计算每个需要移动的雕塑的坐标
      ans += fabs(pos - floor(pos+0.5)) / (n+m); //累加移动距离
    }
    printf("%.4lf\n", ans*10000); //等比例扩大坐标
  }
  return 0;
}
// 102052134 Dec/22/2020 22:58UTC+8 chenwz G - Graveyard GNU C++11 Accepted 60 ms 0 KB
```

## 例题6  立方体成像（Image Is Everything, World Finals 2004, UVa1030）

```cpp
// 例题6  立方体成像（Image Is Everything, World Finals 2004, UVa1030）
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<cmath>
#include<algorithm>
using namespace std;

#define REP(i,n) for(int i = 0; i < (n); i++)

const int maxn = 10;
int n;
char pos[maxn][maxn][maxn];
char view[6][maxn][maxn];

char read_char() {
  char ch;
  for(;;) {
    ch = getchar();
    if((ch >= 'A' && ch <= 'Z') || ch == '.') return ch;
  }
}

void get(int k, int i, int j, int len, int &x, int &y, int &z)
{
  if (k == 0) { x = len; y = j; z = i; } 
  if (k == 1) { x = n - 1 - j; y = len; z = i; }
  if (k == 2) { x = n - 1 - len; y = n - 1 - j; z = i; }
  if (k == 3) { x = j; y = n - 1 - len; z = i; }
  if (k == 4) { x = n - 1 - i; y = j; z = len; }
  if (k == 5) { x = i; y = j; z = n - 1 - len; }
}

int main() {
  while(scanf("%d", &n) == 1 && n) {
    REP(i,n) REP(k,6) REP(j,n) view[k][i][j] = read_char();
    REP(i,n) REP(j,n) REP(k,n) pos[i][j][k] = '#';

    REP(k,6) REP(i,n) REP(j,n) if (view[k][i][j] == '.')
      REP(p,n) {
        int x, y, z;
        get(k, i, j, p, x, y, z);
        pos[x][y][z] = '.';
      }

    for(;;) {
      bool done = true;
      REP(k,6) REP(i,n) REP(j,n) if (view[k][i][j] != '.') {
        REP(p,n) {
          int x, y, z;
          get(k, i, j, p, x, y, z);
          if (pos[x][y][z] == '.') continue;
          if (pos[x][y][z] == '#') {
            pos[x][y][z] = view[k][i][j];
            break;
          }
          if (pos[x][y][z] == view[k][i][j]) break;
          pos[x][y][z] = '.';
          done = false;
        }
      }
      if(done) break;
    }

    int ans = 0;
    REP(i,n) REP(j,n) REP(k,n)
      if (pos[i][j][k] != '.') ans ++;

    printf("Maximum weight: %d gram(s)\n", ans);
  }
  return 0;
}
// 25875758 1030 Image Is Everything Accepted C++ 0.000 2020-12-22 14:26:41
```

## 例题5  蚂蚁（Piotr’s Ants, UVa 10881）

```cpp
// 例题5  蚂蚁（Piotr’s Ants, UVa 10881）
// Rujia Liu
#include <algorithm>
#include <cstdio>
using namespace std;
const int maxn = 10000 + 5;

struct Ant {
  int id;  // 输入顺序
  int p;   // 位置
  int d;   // 朝向。 -1: 左; 0:转身中; 1:右
  bool operator<(const Ant& a) const { return p < a.p; }
} before[maxn], after[maxn];
const char dirName[][10] = {"L", "Turning", "R"};
int order[maxn];  //输入的第i只蚂蚁是终态中的左数第order[i]只蚂蚁
int main() {
  int K; scanf("%d", &K);
  for (int kase = 1, L, T, n; kase <= K; kase++) {
    scanf("%d%d%d", &L, &T, &n);
    for (int i = 0, p, d; i < n; i++) {
      char c;
      scanf("%d %c", &p, &c);
      d = (c == 'L' ? -1 : 1);
      // 相撞后可以看做对穿而过,这里id是未知的
      before[i] = (Ant){i, p, d}, after[i] = (Ant){0, p + T * d, d};
    }
    printf("Case #%d:\n", kase);
    sort(before, before + n);  //计算order数组
    for (int i = 0; i < n; i++)
      order[before[i].id] = i;  // 第一次从左到右所有的蚂蚁的相对位置没有变化
    sort(after, after + n);          //计算终态
    for (int i = 0; i < n - 1; i++)  //修改碰撞中的蚂蚁的方向
      if (after[i].p == after[i + 1].p) after[i].d = after[i + 1].d = 0;
    for (int i = 0; i < n; i++) {
      int a = order[i];
      if (after[a].p < 0 || after[a].p > L)
        puts("Fell off");
      else
        printf("%d %s\n", after[a].p, dirName[after[a].d + 1]);
    }
    printf("\n");
  }
  return 0;
}
// 25879739 10881 Piotr's Ants Accepted C++ 0.010 2020-12-23 15:21:04
```

## 例题1  勇者斗恶龙（The Dragon of Loowater, UVa 11292）

```cpp
// 例题1  勇者斗恶龙（The Dragon of Loowater, UVa 11292）
// Waterloo Local Contest, 2007.9.29
// Rujia Liu
#include<cstdio>
#include<algorithm>       // 因为用到了sort
using namespace std;

const int maxn = 20000 + 5;
int A[maxn], B[maxn];
int main() {
  int n, m;
  while(scanf("%d%d", &n, &m) == 2 && n && m) {
    for(int i = 0; i < n; i++) scanf("%d", &A[i]);
    for(int i = 0; i < m; i++) scanf("%d", &B[i]);
    sort(A, A+n);
    sort(B, B+m);
    int cur = 0;         // 当前需要砍掉的头的编号
    int cost = 0;        // 当前总费用
    for(int i = 0; i < m; i++)
      if(B[i] >= A[cur]) {
        cost += B[i];           // 雇佣该骑士
        if(++cur == n) break;   // 如果头已经砍完，及时退出循环
      }
    if(cur < n) printf("Loowater is doomed!\n");
    else printf("%d\n", cost);
  }
  return 0;
}
// 25875724	11292	Dragon of Loowater	Accepted	C++	0.000	2020-12-22 14:20:28
```

## 例题3  分金币（Spreading the Wealth, UVa 11300）

```cpp
// 例题3  分金币（Spreading the Wealth, UVa 11300）
// Rujia Liu
#include<cstdio>
#include<algorithm>
using namespace std;

const int maxn = 1000000 + 10;
long long A[maxn], C[maxn], tot, M;
int main() {
  int n;
  while(scanf("%d", &n) == 1) { // 输入数据大，scanf比cin快 
    tot = 0;
    for(int i = 1; i <= n; i++) { scanf("%lld", &A[i]); tot += A[i]; } // 用%lld输入long long
    M = tot / n;
    C[0] = 0; 
    for(int i = 1; i < n; i++) C[i] = C[i-1] + A[i] - M; // 递推C数组
    sort(C, C+n);
    long long x1 = C[n/2], ans = 0; // 计算x1
    for(int i = 0; i < n; i++) ans += abs(x1 - C[i]); 
    // 把x1代入，计算转手的总金币数
    printf("%lld\n", ans);
  }
  return 0;
}
// 25875737	11300	Spreading the Wealth	Accepted	C++	0.120	2020-12-22 14:22:29
```

## 例题2  突击战（Commando War, UVa 11729）

```cpp
// 例题2  突击战（Commando War, UVa 11729）
// 陈锋
#include <algorithm>
#include <cstdio>
#include <iostream>
#include <vector>
using namespace std;

struct Job {
  int j, b;
  bool operator<(const Job& x) const {
    return j > x.j;  // 运算符重载。不要忘记const修饰符
  }
};

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  for (int n, b, j, kase = 1; cin >> n && n; kase++) {
    vector<Job> v(n);
    for (int i = 0; i < n; i++) cin >> v[i].b >> v[i].j;
    sort(v.begin(), v.end());  //使用Job类的 < 运算符排序
    int ans = 0;
    for (int i = 0, s = 0; i < n; i++) {
      s += v[i].b;                 //当前任务的开始执行时间
      ans = max(ans, s + v[i].j);  //任务执行完毕时的最晚时间
    }
    printf("Case %d: %d\n", kase, ans);
  }
  return 0;
}
// 25875729	11729	Commando War	Accepted	C++	0.000	2020-12-22 14:21:50
```
