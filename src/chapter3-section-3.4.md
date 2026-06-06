# 3.4 字符串（2）

## 例题20  口吃的外星人（Stammering Aliens, SWERC 2009, UVa12206）

```cpp
// 例题20  口吃的外星人（Stammering Aliens, SWERC 2009, UVa12206）
// 陈锋
#include <algorithm>
#include <cstdio>
#include <iostream>
#include <vector>
using namespace std;
typedef unsigned long long ULL;
const int MAXN = 40000 + 8;
const ULL x = 123;
ULL H[MAXN], PX[MAXN], Hash[MAXN];
void init_PX() {
  PX[0] = 1;
  for (int i = 1; i < MAXN; i++) PX[i] = x * PX[i - 1];
}
int N, sa[MAXN];
void init_hash(const string& s) {
  N = s.length(), H[N] = 0;
  for (int i = N - 1; i >= 0; i--) H[i] = (s[i] - 'a' + 1) + H[i + 1] * x;
}
bool hash_cmp(int a, int b) {
  if (Hash[a] != Hash[b]) return Hash[a] < Hash[b];
  return a < b;
}
bool ok(int L, int M, int& pos) {  // 是否有长度至少len的substr出现M次以上
  for (int i = 0; i <= N - L; i++)
    sa[i] = i, Hash[i] = H[i] - H[i + L] * PX[L];
  sort(sa, sa + N - L + 1, hash_cmp); // 对所有后缀按照hash排序
  pos = -1;
  for (int i = 0, c = 0; i <= N - L; i++) {
    if (i == 0 || Hash[sa[i]] != Hash[sa[i - 1]]) c = 0;
    if (++c >= M) pos = max(pos, sa[i]);
  }
  return pos >= 0;
}
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  init_PX();
  string word;
  for (int t = 0, pos, M; cin >> M >> word && M; t++) {
    init_hash(word);
    if (!ok(1, M, pos)) { puts("none"); continue; }
    int l = 1, r = N + 1;
    while (l + 1 < r) {
      int m = l + (r - l) / 2;
      if (ok(m, M, pos)) l = m;
      else r = m;
    }
    ok(l, M, pos);
    printf("%d %d\n", l, pos);
  }
  return 0;
}
// Accepted 880ms 1613 C++ 5.3.0 2020-12-14 13:07:48 25845792
```

## 例题19  生命的形式（Life Forms, UVa 11107）

```cpp
// 例题19  生命的形式（Life Forms, UVa 11107）
// 陈锋
#include <algorithm>
#include <cstdio>
#include <cstring>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
typedef long long LL;

template <int SZ>
struct SuffixArray {
  int s[SZ];  // 原始字符数组（最后一个字符应必须是0，而前面的字符必须非0）
  int sa[SZ];      // 后缀数组
  int rank[SZ];    // 名次数组. rank[0]一定是n-1，即最后一个字符
  int height[SZ];  // height数组
  int t[SZ], t2[SZ], c[SZ];  // 辅助数组
  int n;                     // 字符个数

  void clear() { n = 0, fill_n(sa, SZ, 0); }

  // m为最大字符值加1。调用之前需设置好s和n
  void build_sa(int m) {
    int i, *x = t, *y = t2;
    for (i = 0; i < m; i++) c[i] = 0;
    for (i = 0; i < n; i++) c[x[i] = s[i]]++;
    for (i = 1; i < m; i++) c[i] += c[i - 1];
    for (i = n - 1; i >= 0; i--) sa[--c[x[i]]] = i;
    for (int k = 1; k <= n; k <<= 1) {
      int p = 0;
      for (i = n - k; i < n; i++) y[p++] = i;
      for (i = 0; i < n; i++)
        if (sa[i] >= k) y[p++] = sa[i] - k;
      for (i = 0; i < m; i++) c[i] = 0;
      for (i = 0; i < n; i++) c[x[y[i]]]++;
      for (i = 0; i < m; i++) c[i] += c[i - 1];
      for (i = n - 1; i >= 0; i--) sa[--c[x[y[i]]]] = y[i];
      swap(x, y);
      p = 1;
      x[sa[0]] = 0;
      for (i = 1; i < n; i++)
        x[sa[i]] = y[sa[i - 1]] == y[sa[i]] && y[sa[i - 1] + k] == y[sa[i] + k]
                       ? p - 1 : p++;
      if (p >= n) break;
      m = p;
    }
  }

  void build_height() {
    for (int i = 0; i < n; i++) rank[sa[i]] = i;
    for (int i = 0, k = 0; i < n; i++) {
      if (k) k--;
      int j = sa[rank[i] - 1];
      while (s[i + k] == s[j + k]) k++;
      height[rank[i]] = k;
    }
  }
};

const int MAXL = 1000 + 8, MAXN = 100 + 4;
int idx[MAXL * MAXN], flag[MAXN], N;
char buf[MAXL];
SuffixArray<MAXL * MAXN> sa;

bool good(int L, int R) {
  if (R - L <= N / 2) return false;
  fill_n(flag, MAXN, 0);
  int cnt = 0;
  _for(i, L, R) {
    int x = idx[sa.sa[i]];
    if (x != N && !flag[x]) flag[x] = 1, cnt++;
  }
  return cnt > N / 2;
}

void print_sub(int L, int R) {  // print s[L,R)
  _for(i, L, R) printf("%c", sa.s[i] - 1 + 'a');
  puts("");
}

bool print_sol(int len, bool print = false) {
  for (int L = 0, R = 1; R <= sa.n; R++) {
    if (R == sa.n || sa.height[R] < len) {  // 新开一段
      if (good(L, R)) {
        if (!print) return true;
        print_sub(sa.sa[L], sa.sa[L] + len);
      }
      L = R;
    }
  }
  return false;
}

void solve(int maxLen) {
  if (!print_sol(1)) {
    puts("?");
    return;
  }
  int L = 1, R = maxLen, M;
  while (L < R) {
    M = L + (R - L + 1) / 2;
    if (print_sol(M)) L = M;
    else R = M - 1;
  }
  print_sol(L, true);
}

// 给字符串加上一个字符，属于字符串i
void add(int ch, int i) { idx[sa.n] = i, sa.s[sa.n++] = ch; }

int main() {
  for (int t = 0; scanf("%d", &N) == 1 && N; t++) {
    if (t) puts("");
    int maxl = 0;
    sa.n = 0;
    _for(i, 0, N) {
      scanf("%s", buf);
      int sz = strlen(buf);
      maxl = max(maxl, sz);
      _for(j, 0, sz) add(buf[j] - 'a' + 1, i);
      add(100 + i, N);
    }
    add(0, N);
    if (N == 1)
      puts(buf);
    else
      sa.build_sa(N + 100), sa.build_height(), solve(maxl);
  }
  return 0;
}
// Accepted 70ms 3250 C++5.3.0 2020-12-1412:59:10 25845774
```

## 例题21  扩展成回文（Extend to Palindrome, UVa11475）

```cpp
// 例题21  扩展成回文（Extend to Palindrome, UVa11475）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 1e5 + 4;
char S[MAXN], T[MAXN * 2];
int P[MAXN * 2];
void manacher(const char *s, int len) {
  int l = 0;
  T[l++] = '$', T[l++] = '#';
  for(int i = 0; i < len; i++) T[l++] = s[i], T[l++] = '#';
  T[l] = 0;
  int r = 0, c = 0;
  for(int i = 0; i < l; i++) {
    int &p = P[i];
    p = r > i ? min(P[2 * c - i], r - i) : 1;
    while(T[i + p] == T[i - p]) p++;
    if(i + p > r) r = i + p, c = i;
  }
}
int main() {
  while(scanf("%s", S) == 1) {
    int ans = 0, L = strlen(S);
    manacher(S, L);
    for(int i = 0; i < 2 * L + 2; i++)
      if(P[i] + i == 2 * L + 2) ans = max(ans, P[i] - 1); //此回文串是作为后缀出现的，更新答案
    printf("%s", S);
    for(int i = L - ans - 1; i >= 0; i--) printf("%c", S[i]);
    puts("");
  }
  return 0;
}
// 24183083 11475 Extend to Palindrome  Accepted  C++11 0.010 2019-11-12 07:25:40
```
