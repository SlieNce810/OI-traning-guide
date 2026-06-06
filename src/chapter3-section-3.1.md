# 3.1 基础数据结构回顾

## 例题6  合作网络（Corporative Network, Codeforces Gym 101461B）

```cpp
// 例题6  合作网络（Corporative Network, Codeforces Gym 101461B）
// Rujia Liu
#include <algorithm>
#include <iostream>
#include <string>
using namespace std;
const int maxn = 20000 + 10;
int pa[maxn], d[maxn];
int findset(int x) {
  if (pa[x] == x) return x;
  int root = findset(pa[x]);
  d[x] += d[pa[x]];
  return pa[x] = root;
}

int main() {
  freopen("network.in", "r", stdin);
  freopen("network.out", "w", stdout);
  ios_base::sync_with_stdio(false);
  int T;
  cin >> T;
  for (int kase = 0, n, u, v; kase < T; kase++) {
    string cmd;
    cin >> n;
    for (int i = 1; i <= n; i++) pa[i] = i, d[i] = 0;
    while (cin >> cmd && cmd[0] != 'O') {
      if (cmd[0] == 'E') cin >> u, findset(u), cout << d[u] << endl;
      if (cmd[0] == 'I') cin >> u >> v, pa[u] = v, d[u] = abs(u - v) % 1000;
    }
  }
  return 0;
}
// 102162738 Dec/24/2020 11:38UTC+8 B - Corporative Network GNU C++11 Accepted 343 ms 300 KB
```

## 例题3  阿格斯（Argus, Beijing 2004, POJ2051）

```cpp
// 例题3  阿格斯（Argus, Beijing 2004, POJ2051）
// 陈锋
#include<cstdio>
#include<queue>
using namespace std;

struct Item { // 优先队列中的元素
  int QNum, Period, Time;
  // 重要！优先级比较函数。优先级高的先出队
  bool operator < (const Item& a) const { // 这里的const必不可少，请读者注意
    if (Time != a.Time) return Time > a.Time;
    return QNum > a.QNum;
  }
};

int main() {
  priority_queue<Item> pq;
  char s[20];
  for (Item item; scanf("%s", s) && s[0] != '#'; pq.push(item)) {
    scanf("%d%d", &item.QNum, &item.Period);
    item.Time = item.Period; // 初始化“下一次事件的时间”为它的周期
  }
  int K;
  scanf("%d" , &K);
  while (K--) {
    Item r = pq.top(); // 取下一个事件
    pq.pop();
    printf("%d\n" , r.QNum);
    r.Time += r.Period; // 更新该触发器的“下一个事件”的时间
    pq.push(r); // 重新插入优先队列
  }
  return 0;
}
// Accepted 32ms 552kB 819 G++2020-12-1316:59:02 22207509
```

## 例题5  易爆物（X-Plosives, UVa1160）

```cpp
// 例题5  易爆物（X-Plosives, UVa1160）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
typedef long long LL;
const int MAXN = 100000 + 4;
int Pa[MAXN];

int findPa(int u) {
  return Pa[u] == u ? u : (Pa[u] = findPa(Pa[u]));
}

int main() {
  int u, v;
  while (true) {
    _rep(i, 0, MAXN) Pa[i] = i;
    int ans = 0;
    while (true) {
      if (scanf("%d", &u) != 1) return 0;
      if (u == -1) break;
      scanf("%d", &v);
      int pu = findPa(u), pv = findPa(v);
      if (pu == pv)
        ans++;
      else
        Pa[pu] = v;
    }
    printf("%d\n", ans);
  }
  return 0;
}
// Accepted 751 C++5.3.0 2020-12-1319:42:07 25843348
```

## 例题2  一道简单题（Easy Problem from Rujia Liu?, UVa 11991）

```cpp
// 例题2  一道简单题（Easy Problem from Rujia Liu?, UVa 11991）
// Rujia Liu
#include<cstdio>
#include<vector>
#include<map>
using namespace std;

map<int, vector<int> > a; // 最后两个>不要连写，否则会被误认为>>

int main() {
  int n, m, x, y;
  while(scanf("%d%d", &n, &m) == 2) {
    a.clear();
    for(int i = 0; i < n; i++) {
      scanf("%d", &x); if(!a.count(x)) a[x] = vector<int>();
      a[x].push_back(i+1);
    }
    while(m--) {
      scanf("%d%d", &x, &y);
      if(!a.count(y) || a[y].size() < x) printf("0\n");
      else printf("%d\n", a[y][x-1]);
    }
  }
  return 0;
}
// 25877211  11991  Easy Problem from Rujia Liu?  Accepted  C++  0.040  2020-12-23 03:44:34
```

## 例题1  猜猜数据结构（I Can Guess the Data Structure!, UVa 11995）

```cpp
// 例题1  猜猜数据结构（I Can Guess the Data Structure!, UVa 11995）
// Rujia Liu
#include<cstdio>
#include<queue>
#include<stack>
#include<cstdlib>
using namespace std;

const int maxn = 1000 + 10;
int n, t[maxn], v[maxn];

int check_stack() {
  stack<int> s;
  for(int i = 0; i < n; i++) {
    if(t[i] == 2) {
      if(s.empty()) return 0;
      int x = s.top(); s.pop();
      if(x != v[i]) return 0;
    }
    else s.push(v[i]);
  }
  return 1;
}

int check_queue() {
  queue<int> s;
  for(int i = 0; i < n; i++) {
    if(t[i] == 2) {
      if(s.empty()) return 0;
      int x = s.front(); s.pop();
      if(x != v[i]) return 0;
    }
    else s.push(v[i]);
  }
  return 1;
}

int check_pq() {
  priority_queue<int> s;
  for(int i = 0; i < n; i++) {
    if(t[i] == 2) {
      if(s.empty()) return 0;
      int x = s.top(); s.pop();
      if(x != v[i]) return 0;
    }
    else s.push(v[i]);
  }
  return 1;
}

int main() {
  while(scanf("%d", &n) == 1) {
    for(int i = 0; i < n; i++) scanf("%d%d", &t[i], &v[i]);
    int s = check_stack();
    int q = check_queue();
    int pq = check_pq();
    if(!s && !q && !pq) printf("impossible\n");
    else if(s && !q && !pq) printf("stack\n");
    else if(!s && q && !pq) printf("queue\n");
    else if(!s && !q && pq) printf("priority queue\n");
    else printf("not sure\n");
  }
  return 0;
}
// 25877209  11995  I Can Guess the Data Structure!  Accepted  C++  0.010  2020-12-23 03:44:22
```

## 例题4  K个最小和（K Smallest Sums, UVa 11997）

```cpp
// 例题4  K个最小和（K Smallest Sums, UVa 11997）
// http://codeforces.com/gym/100048 C
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
typedef long long LL;
const int MAXK = 768, INF = 1e6 + 4;
int K, A[MAXK], B[MAXK];
struct Item {
  int sum, b;  // A[a] + B[b], b
  Item(int _sum, int _b) : sum(_sum), b(_b) {}
  bool operator<(const Item& i) const { return sum > i.sum; };
};

void merge() {  // AxB -> A
  priority_queue<Item> Q;
  _for(i, 0, K) Q.push(Item(A[i] + B[0], 0));
  _for(i, 0, K) {
    Item it = Q.top();
    Q.pop(), A[i] = it.sum;
    if (it.b < K - 1)
      Q.emplace(Item(it.sum + B[it.b + 1] - B[it.b], it.b + 1));
  }
}

void read_array(int *p) {
  _for(i, 0, K) scanf("%d", &(p[i]));
  sort(p, p + K);
}

int main() {
  while (scanf("%d", &K) == 1) {
    read_array(A);
    _for(i, 1, K) read_array(B), merge();
    _for(i, 0, K) printf("%d%c", A[i], i < K - 1 ? ' ' : '\n');
  }
  return 0;
}
// 18787064 11997 K Smallest Sums Accepted  C++11 0.110 2017-02-16 08:15:10
```
