# 2.2 递推关系

## 例题4  多叉树遍历（Exploring Pyramids, NEERC 2005, Codeforces Gym101334E）

```cpp
// 例题4  多叉树遍历（Exploring Pyramids, NEERC 2005, Codeforces Gym101334E）
// Rujia Liu
#include<cstdio>
#include<cstring>
using namespace std;

const int maxn = 300 + 10;
const int MOD = 1000000000;
typedef long long LL;

char S[maxn];
int d[maxn][maxn];

int dp(int i, int j) {
  if(i == j) return 1;
  if(S[i] != S[j]) return 0;
  int& ans = d[i][j];
  if(ans >= 0) return ans;
  ans = 0;
  for(int k = i+2; k <= j; k++) if(S[i] == S[k])
    ans = (ans + (LL)dp(i+1,k-1) * (LL)dp(k,j)) % MOD;
  return ans;
}

int main() {
  freopen("exploring.in", "r", stdin);
  freopen("exploring.out", "w", stdout);
  while(scanf("%s", S) == 1) {
    memset(d, -1, sizeof(d));
    printf("%d\n", dp(0, strlen(S)-1));
  }
  return 0;
}
// 102083028 	Dec/23/2020 09:32UTC+8 	chenwz 	E - Exploring Pyramids 	GNU C++11 	Accepted 	61 ms 	300 KB 
```

## 例题7  串并联网络（Series-Parallel Networks, UVa 10253）

```cpp
// 例题7  串并联网络（Series-Parallel Networks, UVa 10253）
// Rujia Liu
#include<cstdio>
#include<cstring>

long long C(long long n, long long m) {
  double ans = 1;
  for(int i = 0; i < m; i++)
    ans *= n-i;
  for(int i = 0; i < m; i++)
    ans /= i+1;
  return (long long)(ans + 0.5);
}

const int maxn = 30 + 5;
long long f[maxn], d[maxn][maxn]; //d(i,j)表示每棵树最多包含i个叶子，一共有j个叶子的方案数

int main() {
  f[1] = 1;
  memset(d, 0, sizeof(d));

  int n = 30;
  for(int i = 0; i <= n; i++) d[i][0] = 1;
  for(int i = 1; i <= n; i++) { d[i][1] = 1; d[0][i] = 0; }

  for(int i = 1; i <= n; i++) {
    for(int j = 2; j <= n; j++) {
      d[i][j] = 0;
      for(int p = 0; p*i <= j; p++)
        d[i][j] += C(f[i]+p-1, p) * d[i-1][j-p*i];
    }
    f[i+1] = d[i][i+1];
  }

  while(scanf("%d", &n) == 1 && n)
    printf("%lld\n", n == 1 ? 1 : 2*f[n]);
  return 0;
}
// 25877044  10253  Series-Parallel Networks  Accepted  C++  0.000  2020-12-23 01:33:19
```

## 例题6  葛伦堡博物馆（Glenbow Museum, World Finals 2008, UVa1073）

```cpp
// 例题6  葛伦堡博物馆（Glenbow Museum, World Finals 2008, UVa1073）
// Rujia Liu
#include<cstdio>
#include<cstring>
const int maxn = 1000;

long long d[maxn+1][5][2], ans[maxn+1];

int main() {
  memset(d, 0, sizeof(d));
  for(int k = 0; k < 2; k++) {
    d[1][0][k] = 1;
    for(int i = 2; i <= maxn; i++)
      for(int j = 0; j < 5; j++) {
        d[i][j][k] = d[i-1][j][k];
        if(j > 0) d[i][j][k] += d[i-1][j-1][k];
      }
  }

  memset(ans, 0, sizeof(ans));
  for(int i = 1; i <= maxn; i++) {
    if(i < 4 || i % 2 == 1) continue;
    int R = (i+4)/2;    
    ans[i] = d[R][3][0] + d[R][4][1] + d[R][4][0];
  }

  int n, kase = 1;
  while(scanf("%d", &n) == 1 && n)
    printf("Case %d: %lld\n", kase++, ans[n]);
  return 0;
}
// 25877043  1073  Glenbow Museum  Accepted  C++  0.000  2020-12-23 01:32:37
```

## 例题5  数字和与倍数（Investigating Div-Sum Property, UVa 11361）

```cpp
// 例题5  数字和与倍数（Investigating Div-Sum Property, UVa 11361）
// Rujia Liu
#include<cstdio>
#include<cstring>
using namespace std;

int MOD; // 题目中叫k，改名为MOD可以让代码更清晰
int pow10[10];

// 整数n除以MOD的余数，返回0~MOD-1
int mod(int n) {
  return (n % MOD + MOD) % MOD;
}

// 共d个数字，数字之和除以k的余数为m1，整数本身除以k的余数为m2
int memo[11][90][90];
int f(int d, int m1, int m2) {
  if(d == 0) return m1 == 0 && m2 == 0 ? 1 : 0;

  int& ans = memo[d][m1][m2];
  if(ans >= 0) return ans;
  ans = 0;
  for(int x = 0; x <= 9; x++)
    ans += f(d-1, mod(m1-x), mod(m2-x*pow10[d-1]));
  return ans;
}

// 统计0~n-1中满足条件的整数个数（和书上的分析有一点出入，但没有本质区别）
int sumf(int n) {
  char digits[11];
  sprintf(digits, "%d", n);
  int nd = strlen(digits);

  int base = 0; // 当前区间的左边界
  int sumd = 0; // 当前区间的左边界的数字和
  int ans = 0;
  for(int i = 0; i < nd; i++) { // 有i个数字(i>=0)
    int na = nd - 1 - i; // 星号的个数
    for(int d = 0; d < digits[i] - '0'; d++) {
      int cnt = f(na, mod(-sumd - d), mod(-base - d*pow10[na]));
      ans += cnt;
    }
    base += (digits[i] - '0') * pow10[na];
    sumd += (digits[i] - '0');
  }
  return ans;
}

int main() {
  pow10[0] = 1;
  for(int i = 1; i <= 9; i++) pow10[i] = pow10[i-1] * 10;

  int T;
  scanf("%d", &T);
  while(T--) {
    int a, b;
    scanf("%d%d%d", &a, &b, &MOD);
    memset(memo, -1, sizeof(memo));
    if(MOD > 85) printf("0\n"); // 数字和最多为1+9*9=82，如果MOD大于此值，一定无解
    else printf("%d\n", sumf(b+1) - sumf(a));
  }
  return 0;
}
// 25877033 	11361 	Investigating Div-Sum Property 	Accepted 	C++11 	0.020 	2020-12-23 01:24:34
```
