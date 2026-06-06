# 3.3 字符串（1）

## 例题15  周期（Period, SEERC 2004, Codeforces Gym101461A）

```cpp
// 例题15  周期（Period, SEERC 2004, Codeforces Gym101461A）
// 陈锋
#include <cstdio>
const int NN = 1e6 + 4;
char P[NN];
int F[NN];

int main() {
  freopen("period.in", "r", stdin);
  freopen("period.out", "w", stdout);

  for (int n, kase = 1; scanf("%d", &n) == 1 && n; kase++) {
    scanf("%s", P);
    F[0] = 0, F[1] = 0;  // 递推边界初值
    for (int i = 1; i < n; i++) {
      int j = F[i];
      while (j && P[i] != P[j]) j = F[j];
      F[i + 1] = (P[i] == P[j] ? j + 1 : 0);
    }

    printf("Test case #%d\n", kase);
    for (int i = 2; i <= n; i++)
      if (F[i] > 0 && i % (i - F[i]) == 0) printf("%d %d\n", i, i / (i - F[i]));
    printf("\n");
  }
  return 0;
}
// 102087071  Dec/23/2020 12:10UTC+8  chenwz  A - Period  GNU C++11  Accepted  46 ms  4800 KB
```

## UVa11019 Matrix Matcher

```cpp
// UVa11019 Matrix Matcher
// Rujia Liu
#include<cstring>
#include<queue>
#include<cstdio>
#include<map>
#include<string>
using namespace std;

const int SIGMA_SIZE = 26;
const int MAXNODE = 10000 + 10;

void process_match(int pos, int v); // AC自动机每找到一个匹配会调用一次，结束位置为pos，val为v

struct AhoCorasickAutomata {
  int ch[MAXNODE][SIGMA_SIZE];
  int f[MAXNODE];    // fail函数
  int val[MAXNODE];  // 每个字符串的结尾结点都有一个非0的val
  int last[MAXNODE]; // 输出链表的下一个结点
  int sz;

  void init() {
    sz = 1;
    memset(ch[0], 0, sizeof(ch[0]));
  }

  // 字符c的编号
  int idx(char c) {
    return c-'a';
  }

  // 插入字符串。v必须非0
  void insert(char *s, int v) {
    int u = 0, n = strlen(s);
    for(int i = 0; i < n; i++) {
      int c = idx(s[i]);
      if(!ch[u][c]) {
        memset(ch[sz], 0, sizeof(ch[sz]));
        val[sz] = 0;
        ch[u][c] = sz++;
      }
      u = ch[u][c];
    }
    val[u] = v;
  }

  // 递归打印以结点j结尾的所有字符串
  void report(int pos, int j) {
    if(j) {
      process_match(pos, val[j]);
      report(pos, last[j]);
    }
  }

  // 在T中找模板
  int find(char* T) {
    int n = strlen(T);
    int j = 0; // 当前结点编号，初始为根结点
    for(int i = 0; i < n; i++) { // 文本串当前指针
      int c = idx(T[i]);
      while(j && !ch[j][c]) j = f[j]; // 顺着细边走，直到可以匹配
      j = ch[j][c];
      if(val[j]) report(i, j);
      else if(last[j]) report(i, last[j]); // 找到了！
    }
  }

  // 计算fail函数
  void getFail() {
    queue<int> q;
    f[0] = 0;
    // 初始化队列
    for(int c = 0; c < SIGMA_SIZE; c++) {
      int u = ch[0][c];
      if(u) { f[u] = 0; q.push(u); last[u] = 0; }
    }
    // 按BFS顺序计算fail
    while(!q.empty()) {
      int r = q.front(); q.pop();
      for(int c = 0; c < SIGMA_SIZE; c++) {
        int u = ch[r][c];
        if(!u) continue;
        q.push(u);
        int v = f[r];
        while(v && !ch[v][c]) v = f[v];
        f[u] = ch[v][c];
        last[u] = val[f[u]] ? f[u] : last[f[u]];
      }
    }
  }

};

AhoCorasickAutomata ac;

const int maxn = 1000 + 10;
const int maxm = 1000 + 10;
const int maxx = 100 + 10;
const int maxy = 100 + 10;
char text[maxn][maxm], P[maxx][maxy];

int repr[maxx]; // repr[i]为模板第i行的“代表元”
int next[maxx]; // next[i]为模板中与第i行相等的下一个行编号
int len[maxx]; // 模板各行的长度

int tr; // 当前文本行编号
int cnt[maxn][maxm];
void process_match(int pos, int v) {
  int pr = repr[v - 1]; // 匹配到得模板行编号
  int c = pos - len[pr] + 1;
  while(pr >= 0) {
    if(tr >= pr) // P的行pr出现在在T的tr行，起始列编号为c
      cnt[tr - pr][c]++;
    pr = next[pr];
  }
}

int main() {
  int T, n, m, x, y;
  scanf("%d", &T);
  while(T--) {
    scanf("%d%d", &n, &m);
    for(int i = 0; i < n; i++)
      scanf("%s", text[i]);

    scanf("%d%d", &x, &y);
    ac.init();
    for(int i = 0; i < x; i++) {
      scanf("%s", P[i]);
      len[i] = strlen(P[i]);
      repr[i] = i;
      next[i] = -1;
      for(int j = 0; j < i; j++)
        if(strcmp(P[i], P[j]) == 0) {
          repr[i] = j;
          next[i] = next[j];
          next[j] = i;
          break;
        }
      if(repr[i] == i) ac.insert(P[i], i+1);
    }
    ac.getFail();

    memset(cnt, 0, sizeof(cnt));
    for(tr = 0; tr < n; tr++)
      ac.find(text[tr]);

    int ans = 0;
    for(int i = 0; i < n-x+1; i++)
      for(int j = 0; j < m-y+1; j++)
        if(cnt[i][j] == x) ans++;
    printf("%d\n", ans);
  }
  return 0;
}
```

## UVa11468 Substring

```cpp
// UVa11468 Substring
// 陈锋
#include <bits/stdc++.h>
using namespace std;

const int SIGMA_SIZE = 64;
const int MAXNODE = 500;   // 结点总数
const int MAXS = 20 + 10;  // 模板个数

int idx[256], n;
double prob[SIGMA_SIZE];

struct AhoCorasickAutomata {
  int ch[MAXNODE][SIGMA_SIZE];
  int f[MAXNODE];      // fail函数
  int match[MAXNODE];  // 是否包含某一个字符串
  int sz;              // 结点总数

  void init() {
    sz = 1;
    memset(ch[0], 0, sizeof(ch[0]));
  }

  void insert(const char *s) {  // 插入字符串
    int u = 0, n = strlen(s);
    for (int i = 0; i < n; i++) {
      int c = idx[s[i]];
      if (!ch[u][c]) {
        memset(ch[sz], 0, sizeof(ch[sz]));
        match[sz] = 0;
        ch[u][c] = sz++;
      }
      u = ch[u][c];
    }
    match[u] = 1;
  }

  void getFail() {  // 计算fail函数
    queue<int> q;
    f[0] = 0;
    for (int c = 0; c < SIGMA_SIZE; c++) {  // 初始化队列
      int u = ch[0][c];
      if (u) {
        f[u] = 0;
        q.push(u);
      }
    }
    while (!q.empty()) {  // 按BFS顺序计算fail
      int r = q.front();
      q.pop();
      for (int c = 0; c < SIGMA_SIZE; c++) {
        int u = ch[r][c];
        if (!u) {
          ch[r][c] = ch[f[r]][c];
          continue;
        }
        q.push(u);
        int v = f[r];
        while (v && !ch[v][c]) v = f[v];
        f[u] = ch[v][c];
        match[u] |= match[f[u]];
      }
    }
  }

  void dump() {
    printf("sz = %d\n", sz);
    for (int i = 0; i < sz; i++)
      printf("%d: %d %d %d\n", i, ch[i][0], ch[i][1], match[i]);
    printf("\n");
  }
};

AhoCorasickAutomata ac;

double d[MAXNODE][105];
int vis[MAXNODE][105];
double getProb(int u, int L) {
  if (!L) return 1.0;
  if (vis[u][L]) return d[u][L];
  vis[u][L] = 1;
  double &ans = d[u][L];
  ans = 0.0;
  for (int i = 0; i < n; i++)
    if (!ac.match[ac.ch[u][i]]) ans += prob[i] * getProb(ac.ch[u][i], L - 1);
  return ans;
}

char s[30][30];

int main() {
  int T;
  scanf("%d", &T);
  for (int kase = 1, k, L; kase <= T; kase++) {
    scanf("%d", &k);
    for (int i = 0; i < k; i++) scanf("%s", s[i]);
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
      char ch[9];
      scanf("%s%lf", ch, &prob[i]), idx[ch[0]] = i;
    }
    ac.init();
    for (int i = 0; i < k; i++) ac.insert(s[i]);
    ac.getFail();
    scanf("%d", &L);
    memset(vis, 0, sizeof(vis));
    printf("Case #%d: %.6lf\n", kase, getProb(0, L));
  }
  return 0;
}
// Accepted 310ms 2374 C++ 5.3.0 2020-12-14 11:44:03 25845650
```

## 例题14 strcmp()函数（“strcmp()” Anyone?, UVa11732）

```cpp
// 例题14 strcmp()函数（“strcmp()” Anyone?, UVa11732）
// 詹益瑞,陈锋
#include<bits/stdc++.h>
using namespace std;
typedef long long LL;
const int SZ = 4e6 + 5, SIGMA = 70;
struct Trie {
  int ch[SZ][SIGMA], cnt[SZ], val[SZ], sz = 0;
  int idx(char c) {
    if (isdigit(c)) return c - '0';
    if (c >= 'A' && c <= 'Z') return c - 'A' + 10;
    return c - 'a' + 38;
  }
  int newNode() {
    fill_n(ch[sz], SIGMA, 0), cnt[sz] = 0, val[sz] = 0;
    return sz++;
  }
  void insert(const char* s) {
    int len = strlen(s), u = 0;
    for (int i = 0; i < len; ++i) {
      int c = idx(s[i]), &uc = ch[u][c];
      if (!uc) uc = newNode();
      u = uc, cnt[u]++;
    }
    val[u]++; // 单词结束点
  }
  LL query(const char* s) {
    LL x = 0;
    int len = strlen(s), u = 0;
    for (int i = 0; i < len; ++i) {
      int c = idx(s[i]);
      if (!ch[u][c]) return x;
      // 不等的2个串的相同部分每个字符比较2次，最后一位不同的还有一次
      u = ch[u][c], x += cnt[u] * 2;
    }
    return x + val[u];
  }
  void init() { sz = 0, newNode(); }
};


Trie trie;
char s[1004];
int main() {
  for (int n, kase = 1; scanf("%d", &n) && n; kase++) {
    trie.init();
    LL ans = 0;
    for (int i = 1; i <= n; ++i)
      scanf("%s", s), ans += trie.query(s), trie.insert(s);
    ans += n * (n - 1) / 2; // 最后再补上每两个串的结尾比较一次
    printf("Case %d: %lld\n", kase, ans);
  }
  return 0;
}
// 26047697 11732 "strcmp()" Anyone?  Accepted  C++ 0.810 2021-02-02 06:31:12
```

## 例题13  背单词（Remember the Word, UVa1401）

```cpp
// 例题13  背单词（Remember the Word, UVa1401）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int maxnode = 4000 * 100 + 10, sigma_size = 26;

// 字母表为全体小写字母的Trie
struct Trie {
  int ch[maxnode][sigma_size];
  int val[maxnode];
  int sz; // 结点总数
  void clear() { sz = 1; memset(ch[0], 0, sizeof(ch[0])); } // 初始时只有一个根结点
  int idx(char c) { return c - 'a'; } // 字符c的编号

  // 插入字符串s，附加信息为v。注意v必须非0，因为0代表“本结点不是单词结点”
  void insert(const char *s, int v) {
    int u = 0, n = strlen(s);
    for (int i = 0; i < n; i++) {
      int c = idx(s[i]);
      if (!ch[u][c]) { // 结点不存在
        memset(ch[sz], 0, sizeof(ch[sz]));
        val[sz] = 0;  // 中间结点的附加信息为0
        ch[u][c] = sz++; // 新建结点
      }
      u = ch[u][c]; // 往下走
    }
    val[u] = v; // 字符串的最后一个字符的附加信息为v
  }

  // 找字符串s的长度不超过len的前缀
  void find_prefixes(const char *s, int len, vector<int>& ans) {
    int u = 0;
    for (int i = 0; i < len; i++) {
      if (s[i] == '\0') break;
      int c = idx(s[i]);
      if (!ch[u][c]) break;
      u = ch[u][c];
      if (val[u] != 0) ans.push_back(val[u]); // 找到一个前缀
    }
  }
};

// 文本串最大长度, 单词最大个数
const int TL = 3e5 + 4, WC = 4000 + 4, MOD = 20071027;
int D[TL], WLen[WC];
Trie trie;
int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  string text, word;
  for (int kase = 1, S; cin >> text >> S; kase++) {
    trie.clear();
    for (int i = 1; i <= S; i++)
      cin >> word, WLen[i] = word.length(), trie.insert(word.c_str(), i);
    int L = text.length();
    fill_n(D, L, 0), D[L] = 1;
    for (int i = L - 1; i >= 0; i--) {
      vector<int> p;
      trie.find_prefixes(text.c_str() + i, L - i, p);
      for (size_t j = 0; j < p.size(); j++)
        D[i] = (D[i] + D[i + WLen[p[j]]]) % MOD;
    }
    printf("Case %d: %d\n", kase, D[0]);
  }
  return 0;
}
// Accepted 80ms 1784 C++ 5.3.0 2020-12-1411:33:14 25845627
```

## UVa1449 Dominating Patterns

```cpp
// UVa1449 Dominating Patterns
// 刘汝佳
#include <bits/stdc++.h>
using namespace std;

const int SIGMA_SIZE = 26, MAXNODE = 11000, MAXS = 150 + 10;
map<string, int> ms;
struct AhoCorasickAutomata {
  int ch[MAXNODE][SIGMA_SIZE];
  int f[MAXNODE];     // fail函数
  int val[MAXNODE];   // 每个字符串的结尾结点都有一个非0的val
  int last[MAXNODE];  // 输出链表的下一个结点
  int cnt[MAXS];
  int sz;

  void init() {
    sz = 1;
    memset(ch[0], 0, sizeof(ch[0]));
    memset(cnt, 0, sizeof(cnt));
    ms.clear();
  }

  // 字符c的编号
  int idx(char c) { return c - 'a'; }

  // 插入字符串。v必须非0
  void insert(char* s, int v) {
    int u = 0, n = strlen(s);
    for (int i = 0; i < n; i++) {
      int c = idx(s[i]);
      if (!ch[u][c]) {
        memset(ch[sz], 0, sizeof(ch[sz]));
        val[sz] = 0, ch[u][c] = sz++;
      }
      u = ch[u][c];
    }
    val[u] = v, ms[string(s)] = v;
  }

  // 递归打印以结点j结尾的所有字符串
  void print(int j) {
    if (j) cnt[val[j]]++, print(last[j]);
  }

  // 在T中找模板
  void find(char* T) {
    int n = strlen(T), j = 0;      // 当前结点编号，初始为根结点
    for (int i = 0; i < n; i++) {  // 文本串当前指针
      int c = idx(T[i]);
      while (j && !ch[j][c]) j = f[j];  // 顺着细边走，直到可以匹配
      j = ch[j][c];
      if (val[j]) print(j);
      else if (last[j]) print(last[j]);  // 找到了！
    }
  }

  // 计算fail函数
  void getFail() {
    queue<int> q;
    f[0] = 0;
    // 初始化队列
    for (int c = 0; c < SIGMA_SIZE; c++) {
      int u = ch[0][c];
      if (u) f[u] = 0, q.push(u), last[u] = 0;
    }
    // 按BFS顺序计算fail
    while (!q.empty()) {
      int r = q.front();
      q.pop();
      for (int c = 0; c < SIGMA_SIZE; c++) {
        int u = ch[r][c];
        if (!u) continue;
        q.push(u);
        int v = f[r];
        while (v && !ch[v][c]) v = f[v];
        f[u] = ch[v][c];
        last[u] = val[f[u]] ? f[u] : last[f[u]];
      }
    }
  }
};

AhoCorasickAutomata ac;

char text[1000001], P[MAXS][80];
int main() {
  for (int n; scanf("%d", &n) == 1 && n;) {
    ac.init();
    for (int i = 1; i <= n; i++) scanf("%s", P[i]), ac.insert(P[i], i);
    ac.getFail();
    scanf("%s", text), ac.find(text);
    int best = *max_element(ac.cnt + 1, ac.cnt + n + 1);
    printf("%d\n", best);
    for (int i = 1; i <= n; i++)
      if (ac.cnt[ms[string(P[i])]] == best) printf("%s\n", P[i]);
  }
  return 0;
}
// Accepted 20ms 2349 C++5.3.0 2020-12-1411:41:37 25845648
```
