# 2.1 基本计数方法

## 例题2  数三角形（Triangle Counting, UVa11401）

```cpp
// 例题2  数三角形（Triangle Counting, UVa11401）
// Rujia Liu
#include <bits/stdc++.h>
using namespace std;

using LL = long long;  // int存不下
int main() {
  vector<LL> f(1e6 + 4);
  for (LL x = 4; x < (LL)f.size(); x++)
    f[x] = f[x - 1] + ((x - 1) * (x - 2) / 2 - (x - 1) / 2) / 2;  // 递推
  for (int n; cin >> n && n >= 3;) cout << f[n] << endl;
  return 0;
}
// 25877025 11401 Triangle Counting Accepted C++ 0.020 2020-12-23 01:22:22
```

## 例题1  象棋中的皇后（Chess Queen, UVa 11538）

```cpp
// 例题1  象棋中的皇后（Chess Queen, UVa 11538）
// Rujia Liu
#include<iostream>
#include<algorithm>
using namespace std;

int main() {
  unsigned long long n, m; // 最大可以保存2^64-1>1.8*10^19
  while(cin >> n >> m) {
    if(!n && !m) break;
    if(n > m) swap(n, m); // 这样就避免了对n<=m和n>m两种情况分类讨论
    cout << n*m*(m+n-2)+2*n*(n-1)*(3*m-n-1)/3 << endl;
  }
  return 0;
}
// 25877028 11538 Chess Queen Accepted C++ 0.000 2020-12-23 01:22:44
```

## 例题3  拉拉队（Cheerleaders, UVa 11806）

```cpp
// 例题3  拉拉队（Cheerleaders, UVa 11806）
// 陈锋
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
typedef long long LL;
const int MOD = 1000007, MAXC = 400 + 4;
int M, N, K;
LL C[MAXC][MAXC];
void init() {
  C[1][0] = C[1][1] = 1;
  for (int n = 2; n < MAXC; n++) {
    C[n][0] = 1;
    for (int k = 1; k <= n; k++)
      C[n][k] = (C[n - 1][k - 1] + C[n - 1][k]) % MOD;
  }
}
inline LL CK(int m, int n) { return C[m * n][K]; } // get C(m*n, k)

LL solve() {
  if (K < 2 || K > M * N) return 0;
  LL S = C[M * N][K];
  /*S -= (2*CK(M, N-1) + 2*CK(M-1, N))%MOD; // A,B,C,D
    S += (4*CK(M-1,N-1) + CK(M-2, N) + CK(M,N-2))%MOD; // AB,AC,AD,BC,BD,CD
    S -= (2*CK(M-2,N-1) + 2*CK(M-1, N-2))%MOD; // ABC, ABD, ACD, BCD
    S += CK(M-2, N-2); // ABCD */
  for (int b = 1; b < 16; b++) { // 3210 LRTB
    int cnt = 0, m = M, n = N;
    if (b & 8) --m, ++cnt;
    if (b & 4) --m, ++cnt;
    if (b & 2) --n, ++cnt;
    if (b & 1) --n, ++cnt;
    LL x = C[m * n][K];
    if (cnt % 2) x = -x;
    S = (S + MOD + x) % MOD;
  }
  return S;
}

int main() {
  int T;

  init();
  ios::sync_with_stdio(false), cin.tie(0);
  cin >> T;
  for (int t = 1; t <= T; t++) {
    cin >> M >> N >> K;
    printf("Case %d: %lld\n", t, solve());
  }
  return 0;
}
// 21079866 11806 Cheerleaders  Accepted  C++11 0.000 2018-04-04 06:06:31
```
