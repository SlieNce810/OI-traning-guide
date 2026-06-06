# 2.6 置换及其应用

## 例题23  Leonardo的笔记本（Leonardo's Notebook , NWERC 2006, Codeforces Gym100722I）

```cpp
// 例题23  Leonardo的笔记本（Leonardo's Notebook , NWERC 2006, Codeforces Gym100722I）
// Rujia Liu
#include<cstdio>
#include<cstring>
int main() {
  char B[30];
  int vis[30], cnt[30], T;
  scanf("%d", &T);
  while(T--) {
    scanf("%s", B);
    memset(vis, 0, sizeof(vis));
    memset(cnt, 0, sizeof(cnt));
    for(int i = 0; i < 26; i++)
      if(!vis[i]) { // 找一个从i开始的循环
        int j = i, n = 0;
        do {
          vis[j] = 1; // 标记j为“已访问”
          j = B[j] - 'A';
          n++;
        } while(j != i);
        cnt[n]++;
      }
    int ok = 1;
    for(int i = 2; i <= 26; i++)
      if(i%2 == 0 && cnt[i]%2 == 1) ok = 0;
    if(ok) printf("Yes\n"); else printf("No\n");
  }
  return 0;
}
// 102084408 	Dec/23/2020 10:33UTC+8 	chenwz 	I - Leonardo's Notebook 	GNU C++11 	Accepted 	15 ms 	0 KB
```

## 例题22  项链和手镯（Arif in Dhaka(First Love Part 2), UVa 10294）

```cpp
// 例题22  项链和手镯（Arif in Dhaka(First Love Part 2), UVa 10294）
// 陈锋
#include <cstdio>
typedef long long LL;
const int NN = 100;
int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }

int main() {
  for (int n, t; scanf("%d%d", &n, &t) == 2 && n;) {
    LL pow[NN], a = 0, b = 0;
    pow[0] = 1;
    for (int i = 1; i <= n; i++) pow[i] = pow[i - 1] * t;
    for (int i = 0; i < n; i++) a += pow[gcd(i, n)];
    if (n % 2 == 1)
      b = n * pow[(n + 1) / 2];
    else
      b = n / 2 * (pow[n / 2 + 1] + pow[n / 2]);
    printf("%lld %lld\n", a / n, (a + b) / 2 / n);
  }
  return 0;
}
// Accepted 583 C++5.3.0 2020-12-12 17:34:43 25839147
```

## 例题24  排列统计（Find the Permutations, UVa 11077）

```cpp
// 例题24  排列统计（Find the Permutations, UVa 11077）
// 刘汝佳
#include <cstdio>
#include <cstring>
const int maxn = 30;
unsigned long long f[maxn][maxn];
int main() {
  memset(f, 0, sizeof(f));
  f[1][0] = 1;
  for (int i = 2; i <= 21; i++)
    for (int j = 0; j < i; j++) {
      f[i][j] = f[i - 1][j];
      if (j > 0) f[i][j] += f[i - 1][j - 1] * (i - 1);
    }
  int n, k;
  while (scanf("%d%d", &n, &k) == 2 && n) printf("%llu\n", f[n][k]);
  return 0;
}
// Accepted 435 C++5.3.0 2020-12-12 20:34:55 25839718
```
