# 5.2 深度优先遍历

## 例题9  飞机调度（Now or Later, LA 3211）

```cpp
// 例题9  飞机调度（Now or Later, LA 3211）
// Rujia Liu
#include<cstdio>
#include<vector>
#include<cstring>
using namespace std;

const int maxn = 2000 + 10;

struct TwoSAT {
  int n;
  vector<int> G[maxn*2];
  bool mark[maxn*2];
  int S[maxn*2], c;

  bool dfs(int x) {
    if (mark[x^1]) return false;
    if (mark[x]) return true;
    mark[x] = true;
    S[c++] = x;
    for (int i = 0; i < G[x].size(); i++)
      if (!dfs(G[x][i])) return false;
    return true;
  }

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n*2; i++) G[i].clear();
    memset(mark, 0, sizeof(mark));
  }

  // x = xval or y = yval
  void add_clause(int x, int xval, int y, int yval) {
    x = x * 2 + xval;
    y = y * 2 + yval;
    G[x^1].push_back(y);
    G[y^1].push_back(x);
  }

  bool solve() {
    for(int i = 0; i < n*2; i += 2)
      if(!mark[i] && !mark[i+1]) {
        c = 0;
        if(!dfs(i)) {
          while(c > 0) mark[S[--c]] = false;
          if(!dfs(i+1)) return false;
        }
      }
    return true;
  }
};

///////// 题目相关
#include<algorithm>

TwoSAT solver;

int n, T[maxn][2];

bool test(int diff) {
  solver.init(n);
    for(int i = 0; i < n; i++) for(int a = 0; a < 2; a++)
      for(int j = i+1; j < n; j++) for(int b = 0; b < 2; b++)
        if(abs(T[i][a] - T[j][b]) < diff) solver.add_clause(i, a^1, j, b^1);
  return solver.solve();
}

int main() {
  while(scanf("%d", &n) == 1 && n) {
    int L = 0, R = 0;
    for(int i = 0; i < n; i++) for(int a = 0; a < 2; a++) {
      scanf("%d", &T[i][a]);
      R = max(R, T[i][a]);
    }
    while(L < R) {
      int M = L + (R-L+1)/2;
      if(test(M)) L = M; else R = M-1;
    }
    printf("%d\n", L);
  }
  return 0;
}
// 25878101	1146	Now or later	Accepted	C++	0.540	2020-12-23 08:06:28
```

## 例题5  圆桌骑士（Knights of the Round Table, CERC2005, LA 3523/SPOJ	KNIGHTS

```cpp
// 例题5  圆桌骑士（Knights of the Round Table, CERC2005, LA 3523/SPOJ	KNIGHTS
// 陈锋
#include <bits/stdc++.h>
using namespace std;
struct Edge { int u, v; };
const int NN = 1000 + 10;
int pre[NN], iscut[NN], bccno[NN], dfs_clock, bcc_cnt; // 割顶的bccno无意义
vector<int> G[NN], bcc[NN];

stack<Edge> S;
int dfs(int u, int fa) {
  int lowu = pre[u] = ++dfs_clock, child = 0;
  for (int i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    Edge e = (Edge) {u, v};
    if (!pre[v]) { // 没有访问过v
      S.push(e);
      child++;
      int lowv = dfs(v, u);
      lowu = min(lowu, lowv); // 用后代的low函数更新自己
      if (lowv >= pre[u]) {
        iscut[u] = true, bcc[++bcc_cnt].clear();
        while (true) {
          Edge x = S.top(); S.pop();
          if (bccno[x.u] != bcc_cnt)
            bcc[bcc_cnt].push_back(x.u), bccno[x.u] = bcc_cnt;
          if (bccno[x.v] != bcc_cnt)
            bcc[bcc_cnt].push_back(x.v); bccno[x.v] = bcc_cnt;
          if (x.u == u && x.v == v) break;
        }
      }
    }
    else if (pre[v] < pre[u] && v != fa) {
      S.push(e), lowu = min(lowu, pre[v]); // 用反向边更新自己
    }
  }
  if (fa < 0 && child == 1) iscut[u] = 0;
  return lowu;
}

void find_bcc(int n) { // 调用结束后S保证为空，所以不用清空
  fill_n(pre, n + 1, 0), fill_n(iscut, n + 1, 0), fill_n(bccno, n + 1, 0);
  dfs_clock = bcc_cnt = 0;
  for (int i = 0; i < n; i++)
    if (!pre[i]) dfs(i, -1);
}

int odd[NN], color[NN];
bool bipartite(int u, int b) {
  for (int i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    if (bccno[v] != b) continue;
    if (color[v] == color[u]) return false;
    if (!color[v]) {
      color[v] = 3 - color[u];
      if (!bipartite(v, b)) return false;
    }
  }
  return true;
}

int A[NN][NN];
int main() {
  for (int kase = 0, u, v, n, m; scanf("%d%d", &n, &m) == 2 && n; ) {
    for (int i = 0; i < n; i++) G[i].clear();
    memset(A, 0, sizeof(A));
    for (int i = 0; i < m; i++) {
      scanf("%d%d", &u, &v), u--, v--;
      A[u][v] = A[v][u] = 1;
    }
    for (int u = 0; u < n; u++)
      for (int v = u + 1; v < n; v++)
        if (!A[u][v]) G[u].push_back(v), G[v].push_back(u);

    find_bcc(n);
    memset(odd, 0, sizeof(odd));
    for (int i = 1; i <= bcc_cnt; i++) {
      memset(color, 0, sizeof(color));
      for (int j = 0; j < bcc[i].size(); j++)
        bccno[bcc[i][j]] = i; // 主要是处理割顶
      int u = bcc[i][0];
      color[u] = 1;
      if (!bipartite(u, i))
        for (int j = 0; j < bcc[i].size(); j++) odd[bcc[i][j]] = 1;
    }
    int ans = n;
    for (int i = 0; i < n; i++) if (odd[i]) ans--;
    printf("%d\n", ans);
  }
  return 0;
}
// Accepted 310ms 7987kB 2556 C++(gcc 8.3)2020-12-1416:05:37  27093919
```

## 例题10  宇航员分组（Astronauts, LA3713/UVa1391） CERC2006

```cpp
// 例题10  宇航员分组（Astronauts, LA3713/UVa1391） CERC2006
// 陈锋
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;

const int maxn = 100000 + 5;

struct TwoSAT {
  int n;
  vector<int> G[maxn * 2];
  bool mark[maxn * 2];
  int S[maxn * 2], c;

  bool dfs(int x) {
    if (mark[x ^ 1]) return false;
    if (mark[x]) return true;
    mark[x] = true;
    S[c++] = x;
    for (int i = 0; i < G[x].size(); i++)
      if (!dfs(G[x][i])) return false;
    return true;
  }

  void init(int n) {
    this->n = n;
    for (int i = 0; i < n * 2; i++) G[i].clear();
    memset(mark, 0, sizeof(mark));
  }

  // x = xval or y = yval
  void add_clause(int x, int xval, int y, int yval) {
    x = x * 2 + xval, y = y * 2 + yval;
    G[x ^ 1].push_back(y), G[y ^ 1].push_back(x);
  }

  bool solve() {
    for (int i = 0; i < n * 2; i += 2)
      if (!mark[i] && !mark[i + 1]) {
        c = 0;
        if (!dfs(i)) {
          while (c > 0) mark[S[--c]] = false;
          if (!dfs(i + 1)) return false;
        }
      }
    return true;
  }
};

#include <algorithm> //题目相关
int n, m, total_age, age[maxn];
int is_young(int x) { return age[x] * n < total_age; }
TwoSAT solver;
int main() {
  while (scanf("%d%d", &n, &m) == 2 && n) {
    total_age = 0;
    for (int i = 0; i < n; i++) scanf("%d", &age[i]), total_age += age[i];
    solver.init(n);
    for (int i = 0, a, b; i < m; i++) {
      scanf("%d%d", &a, &b), a--, b--;
      if (a == b) continue;
      solver.add_clause(a, 1, b, 1);    //不能同去任务C
      if (is_young(a) == is_young(b))   //同类宇航员
        solver.add_clause(a, 0, b, 0);  //不能同去任务A或者任务B
    }
    if (!solver.solve()) {
      puts("No solution.");
      continue;
    }
    for (int i = 0; i < n; i++)  // 看看x[i]的值
      if (solver.mark[i * 2])
        puts("C");  // false:去任务C
      else if (is_young(i))
        puts("B");  // true:年轻宇航员去任务B
      else
        puts("A");  // true: 年长宇航员去任务A
  }
  return 0;
}
// 5878107	1391	Astronauts	Accepted	C++	0.230	2020-12-23 08:07:31
```

## 例题7  等价性证明（Proving Equivalences, NWERC2008, LA4287/HDU2767）

```cpp
// 例题7  等价性证明（Proving Equivalences, NWERC2008, LA4287/HDU2767）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

const int NN = 20000 + 10;

vector<int> G[NN];
int pre[NN], lowlink[NN], sccno[NN], dfs_clock, scc_cnt;
stack<int> S;
void dfs(int u) {
  int &lu = lowlink[u];
  pre[u] = lu = ++dfs_clock, S.push(u);
  for (size_t i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    if (!pre[v]) dfs(v), lu = min(lu, lowlink[v]);
    else if (!sccno[v]) lu = min(lu, pre[v]);
  }
  if (lu == pre[u]) {
    scc_cnt++;
    for (int x = -1; x != u; S.pop()) x = S.top(), sccno[x] = scc_cnt;
  }
}

void find_scc(int n) {
  dfs_clock = scc_cnt = 0;
  fill_n(sccno, n, 0), fill_n(pre, n, 0);
  for (int i = 0; i < n; i++)
    if (!pre[i]) dfs(i);
}

int in0[NN], out0[NN];
int main() {
  int T, n, m;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%d", &n, &m);
    for (int i = 0; i < n; i++) G[i].clear();
    for (int i = 0, u, v; i < m; i++) {
      scanf("%d%d", &u, &v), u--, v--;
      G[u].push_back(v);
    }

    find_scc(n);
    fill_n(in0 + 1, scc_cnt, 1), fill_n(out0 + 1, scc_cnt, 1);
    for (int u = 0; u < n; u++)
      for (size_t i = 0; i < G[u].size(); i++) {
        int v = G[u][i];
        if (sccno[u] != sccno[v]) in0[sccno[v]] = out0[sccno[u]] = 0;
      }
    int a = 0, b = 0;
    for (int i = 1; i <= scc_cnt; i++) {
      if (in0[i]) a++;
      if (out0[i]) b++;
    }
    int ans = max(a, b);
    if (scc_cnt == 1) ans = 0;
    printf("%d\n", ans);
  }
  return 0;
}
// Accepted 187ms 5424kB 1665 G++2020-12-14 16:11:27 34870207
```

## 例题6  井下矿工（Mining Your Own Business, World Finals 2011, LA 5135/SPOJ BUSINESS）

```cpp
// 例题6  井下矿工（Mining Your Own Business, World Finals 2011, LA 5135/SPOJ BUSINESS）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int NN = 1e5 + 8;
typedef long long LL;
int Low[NN], Pre[NN], DfsClock, IsCut[NN], BccNo;
vector<int> G[NN], Bcc[NN];

stack<int> S;
void clear(int &n) {
  for (int i = 1; i <= n; ++i)
    G[i].clear(), Pre[i] = 0, IsCut[i] = 0;
  n = BccNo = DfsClock = 0;
}

void tarjan(int u, int root) {
  Pre[u] = Low[u] = ++DfsClock, S.push(u);
  int child = 0;
  for (auto v : G[u]) {
    if (!Pre[v]) {
      tarjan(v, root);
      Low[u] = min(Low[u], Low[v]), child++;
      if (Low[v] == Pre[u]) {
        Bcc[++BccNo].clear();
        for (int x = 0; x != v; S.pop()) Bcc[BccNo].push_back(x = S.top());
        Bcc[BccNo].push_back(u);
      }
      if (u != root && Low[v] >= Pre[u]) IsCut[u] = 1;
    }
    else
      Low[u] = min(Low[u], Pre[v]);
  }
  if (u == root && child > 1) IsCut[u] = 1;
}
int main() {
  for (int kase = 1, n, m; ~scanf("%d", &m) && m; ++kase) {
    clear(n);
    for (int i = 1, x, y; i <= m; ++i) {
      scanf("%d%d", &x, &y);
      n = max(n, max(x, y));
      G[x].push_back(y), G[y].push_back(x);
    }
    for (int i = 1; i <= n; ++i) if (!Pre[i]) tarjan(i, i);
    printf("Case %d:", kase);
    LL ans1 = 0, ans2 = 1;
    for (int i = 1; i <= BccNo; ++i) {
      int cutCnt = 0, sz = Bcc[i].size();
      for (auto v : Bcc[i]) if (IsCut[v]) cutCnt++;
      if (cutCnt == 0) ans1 += 2, ans2 *= 1LL * sz * (sz - 1) / 2;
      else if (cutCnt == 1) ans1++, ans2 *= sz - 1;
    }
    printf(" %lld %lld\n", ans1, ans2);
  }
  return 0;
}
//  Accepted 170ms 20480kB 1710 C++14(gcc 8.3)2020-12-14 16:07:37 27093931
```

## 例题8  最大团（The Largest Clique, UVa 11324）

```cpp
// 例题8  最大团（The Largest Clique, UVa 11324）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
const int NN = 1000 + 10;
vector<int> G[NN];
int pre[NN], lowlink[NN], sccno[NN], dfs_clock, scc_cnt;
stack<int> S;
void dfs(int u) {
  int& lu = lowlink[u];
  pre[u] = lu = ++dfs_clock, S.push(u);
  for (size_t i = 0; i < G[u].size(); i++) {
    int v = G[u][i];
    if (!pre[v])
      dfs(v), lu = min(lu, lowlink[v]);
    else if (!sccno[v])
      lu = min(lu, pre[v]);
  }
  if (lu == pre[u]) {
    scc_cnt++;
    for (int x = -1; x != u; S.pop()) sccno[x = S.top()] = scc_cnt;
  }
}

void find_scc(int n) {
  dfs_clock = scc_cnt = 0;
  fill_n(sccno, n, 0), fill_n(pre, n, 0);
  for (int i = 0; i < n; i++)
    if (!pre[i]) dfs(i);
}

int SccSz[NN], TG[NN][NN], D[NN];
int dp(int u) {
  int& ans = D[u];
  if (ans >= 0) return ans;
  ans = SccSz[u];
  for (int v = 1; v <= scc_cnt; v++)
    if (u != v && TG[u][v]) ans = max(ans, dp(v) + SccSz[u]);
  return ans;
}

int main() {
  int T, n, m;
  scanf("%d", &T);
  while (T--) {
    scanf("%d%d", &n, &m);
    for (int i = 0; i < n; i++) G[i].clear();
    for (int i = 0, u, v; i < m; i++) {
      scanf("%d%d", &u, &v), u--, v--;
      G[u].push_back(v);
    }

    find_scc(n);  // 找强连通分量
    memset(TG, 0, sizeof(TG));
    memset(SccSz, 0, sizeof(SccSz));
    for (int i = 0; i < n; i++) {
      SccSz[sccno[i]]++;  // 累加强连通分量大小（结点数）
      for (size_t j = 0; j < G[i].size(); j++)
        TG[sccno[i]][sccno[G[i][j]]] = 1;  // 构造SCC图
    }

    int ans = 0;
    memset(D, -1, sizeof(D));           // 初始化动态规划记忆化数组
    for (int i = 1; i <= scc_cnt; i++)  // 注意，SCC编号为1~scc_cnt
      ans = max(ans, dp(i));
    printf("%d\n", ans);
  }
  return 0;
}
// Accepted 80ms 1740 C++5.3.0 2020-12-14 16:16:29 25846267
```
