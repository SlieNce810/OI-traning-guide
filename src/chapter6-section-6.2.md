# 6.2 嵌套和分块数据结构

## 「SCOI2005」王室联邦

```cpp
// 「SCOI2005」王室联邦
// 陈锋
#include <iostream>
#include <stack>
#include <vector>
using namespace std;

typedef long long LL;
const int NN = 1000 + 4;
vector<int> G[NN];
stack<int> S;
int N, B, BCnt, BId[NN], Cap[NN];  //块的个数，每个点所属块编号，每个块的中心

void dfs(int u, int fa) {
  size_t sz = S.size();
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs(v, u);
    if (S.size() >= sz + B) {  //新增点可以分块
      Cap[++BCnt] = u;         //新增块中心点为u
      while (S.size() > sz) BId[S.top()] = BCnt, S.pop();
    }
  }
  S.push(u);
  if (u == 1)  // root特殊处理，未分块的点都放入以root为中心的块
    while (!S.empty()) BId[S.top()] = BCnt, S.pop();
}

int main() {
  ios::sync_with_stdio(false), cin.tie(nullptr);
  cin >> N >> B, BCnt = 0;
  for (int i = 1, u, v; i < N; i++) {
    cin >> u >> v;
    G[u].push_back(v), G[v].push_back(u);
  }
  dfs(1, -1);
  cout << BCnt << endl;
  for (int i = 1; i <= N; i++) cout << BId[i] << (i == N ? "\n" : " ");
  for (int i = 1; i <= BCnt; i++) cout << Cap[i] << (i == BCnt ? "\n" : " ");
  return 0;
}
// 46047872 「SCOI2005」王室联邦 答案正确 100 3 504 1000 C++ 2020-12-13 23:33:34
```

## UVa11297 - Census

```cpp
// UVa11297 - Census
// 陈锋
#include<stdio.h>
#include<algorithm>
#include<cstring>
using namespace std;
const int NN = 508, INF = 1e9;
struct SegTree2D {
  struct Node {
    int Max, Min;
    void update(const Node& nd) {
      Max = max(Max, nd.Max), Min = min(Min, nd.Min);
    }
  } NS[NN][NN * 4]; //第一维表示是用矩阵的第几行建立的线段树

  Node qAns;
  void maintain(int c, int o) {
    Node& nd = NS[c][o], ld = NS[c][2 * o], rd = NS[c][2 * o + 1];
    nd.Max = max(ld.Max, rd.Max), nd.Min = min(ld.Min, rd.Min);
  }

  void build(int c, int o, int l, int r) {
    Node& nd = NS[c][o];
    if (l == r) {
      scanf("%d", &nd.Min), nd.Max = nd.Min;
      return ;
    }
    int mid = (l + r) / 2, lc = o * 2, rc = o * 2 + 1;
    build(c, lc, l, mid), build(c, rc, mid + 1, r);
    maintain(c, o);
  }

  void query(int c, int o, int l, int r, int qL, int qR) {
    if (l == qL && r == qR) {
      qAns.update(NS[c][o]);
      return;
    }
    int qM = (qL + qR) / 2, lc = o * 2, rc = o * 2 + 1;
    if (qM >= r) query(c, lc, l, r, qL, qM);
    else if (qM < l) query(c, rc, l, r, qM + 1, qR);
    else query(c, lc, l, qM, qL, qM), query(c, rc, qM + 1, r, qM + 1, qR);
  }

  void modify(int c, int x, int val, int o, int l, int r) {
    Node& nd = NS[c][o];
    if (l == r && l == x) {
      nd.Max = nd.Min = val;
      return ;
    }
    int m = (l + r) / 2, lc = o * 2, rc = o * 2 + 1;
    if (m >= x) modify(c, x, val, lc, l, m);
    else if (m < x) modify(c, x, val, rc,  m + 1, r);
    maintain(c, o);
  }
};
SegTree2D ST;
int main() {
  char op[10];
  for (int m, n, x1, y1, x2, y2, v; scanf("%d", &n) != EOF;) {
    for (int x = 1; x <= n; x++) ST.build(x, 1, 1, n);
    scanf("%d", &m);
    while (m--) {
      scanf("%s", op);
      if (op[0] == 'q') {
        ST.qAns.Max = -INF, ST.qAns.Min = INF;
        scanf("%d%d%d%d", &x1, &y1, &x2, &y2);
        for (int x = x1; x <= x2; x++) ST.query(x, 1, y1, y2, 1, n);
        printf("%d %d\n", ST.qAns.Max, ST.qAns.Min);
      }
      if (op[0] == 'c')
        scanf("%d%d%d", &x1, &y1, &v), ST.modify(x1, y1, v, 1, 1, n);
    }
  }
  return 0;
}
// 25858184 11297 Census  Accepted  C++ 0.430 2020-12-17 09:28:06
```

## UVa11990 "Dynamic" Inversion

```cpp
// UVa11990 "Dynamic" Inversion
// 刘汝佳
#include<cstdio>
#include<vector>
#include<algorithm>
#include<cassert>
using namespace std;

inline int lowbit(int x) { return x&-x; }

struct Node {
  Node *ch[2]; // 左右子树
  int v; // 值
  int s; // 结点总数。有删除标记的结点未统计在内
  int d; // 删除标记
  Node():d(0) {}
  int ch_s(int d) { return ch[d] == NULL ? 0 : ch[d]->s; }
};

// 名次树，懒删除实现
struct RankTree {
  int n, next;
  int *v;
  Node *nodes, *root;
  RankTree(int n, int* A):n(n) {
    nodes = new Node[n];
    next = 0;
    v = new int[n];
    for(int i = 0; i < n; i++) v[i] = A[i];
    sort(v, v+n);
    root = build(0, n-1);
    delete[] v;
  }

  Node* build(int L, int R) {
    if(L > R) return NULL;
    int M = L + (R-L) / 2;
    int u = next++;
    nodes[u].v = v[M];
    nodes[u].ch[0] = build(L, M-1);
    nodes[u].ch[1] = build(M+1, R);
    nodes[u].s = nodes[u].ch_s(0) + nodes[u].ch_s(1) + 1;
    return &nodes[u];
  }

  // type = 0：统计比v小的元素个数
  // type = 1：统计比v大的元素个数  
  int count(int v, int type) {
    Node* u = root;
    int cnt = 0;
    while(u != NULL) {
      if(u->v == v) { cnt += u->ch_s(type); break; }
      int c = (v < u->v ? 0 : 1);
      if(c != type) cnt += u->s - u->ch_s(c);
      u = u->ch[c];
    }
    return cnt;
  }

  // 要保证v在树中且尚未删除
  void erase(int v) {
    Node* u = root;
    while(u != NULL) {
      u->s--;
      if(u->v == v) { assert(u->d == 0); u->d = 1; return; }
      int c = (v < u->v ? 0 : 1);
      u = u->ch[c];
    }
    assert(0);
  }

  ~RankTree() {
    delete[] nodes;
  }
};

// 嵌套名次树的Fenwick树
struct FenwickRankTree {
  int n;
  vector<RankTree*> C;

  void init(int n, int* A) {
    this->n = n;
    C.resize(n+1); // 存放在C[1]~C[n]
    for(int i = 1; i <= n; i++) {
      C[i] = new RankTree(lowbit(i), A+i-lowbit(i)+1);
    }
  }

  void clear() { for(int i = 1; i <= n; i++) delete C[i]; }

  // 统计A[1], A[2], ..., A[x]有多少个元素比v大(x<=n)
  int count(int x, int v, int type) {
    int ret = 0;
    while(x > 0) {
      ret += C[x]->count(v, type); x -= lowbit(x);
    }
    return ret;
  }

  // 删除A[x]=v
  void erase(int x, int v) {
    while(x <= n) {
      C[x]->erase(v); x += lowbit(x);
    }
  }
};

// 普通Fenwick树
struct FenwickTree {
  int n;
  vector<int> C;

  void init(int n) {
    this->n = n;
    C.resize(n+1);
    fill(C.begin(), C.end(), 0);
  }

  // 计算A[1]+A[2]+...+A[x] (x<=n)
  int sum(int x) {
    int ret = 0;
    while(x > 0) {
      ret += C[x]; x -= lowbit(x);
    }
    return ret;
  }

  // A[x] += d (1<=x<=n)
  void add(int x, int d) {
    while(x <= n) {
      C[x] += d; x += lowbit(x);
    }
  }
};

const int maxn = 200000 + 5;
const int maxm = 100000 + 5;
typedef long long LL;

int n, m, A[maxn], B[maxn], pos[maxn];
FenwickRankTree frt;
FenwickTree f; // 用来求逆序对数以及求已删除的元素有多少个比v小

LL inversion_pairs() {
  LL ans = 0;
  f.init(n);
  for(int i = n; i >= 1; i--) {
    ans += f.sum(A[i]-1);
    f.add(A[i], 1);
  }
  return ans;
}

int main() {
  while(scanf("%d%d", &n, &m) == 2) {
    for(int i = 1; i <= n; i++) {
      scanf("%d", &A[i]);
      pos[B[i] = A[i]] = i;
    }
    LL cnt = inversion_pairs();
    frt.init(n, A);
    f.init(n);
    for(int i = 0; i < m; i++) {
      printf("%lld\n", cnt);
      int x;
      scanf("%d", &x);
      f.add(x, 1);
      int a = frt.count(pos[x]-1, x, 1); // x左边有a个比x大
      int b = x-1; // 一共有x-1个数比x小
      int c = f.sum(x-1); // 删了c个比x小的
      int d = frt.count(pos[x]-1, x, 0);  // 现在左边有d个比x小
      b -= c + d;  // 还剩b个
      cnt -= a + b; // 逆序对减少a+b个
      frt.erase(pos[x], x);
    }
  }
  return 0;
}
// 25878364	11990	``Dynamic'' Inversion	Accepted	C++	0.900	2020-12-23 09:02:59
```

## UVa12003 Array Transformer

```cpp
// UVa12003 Array Transformer
// 刘汝佳
#include<cstdio>
#include<algorithm>
using namespace std;

const int maxn = 300000 + 10;
const int SIZE = 4096;

int n, m, u, A[maxn], block[maxn/SIZE+1][SIZE];

void init() {
  scanf("%d%d%d", &n, &m, &u);
  int b = 0, j = 0;
  for(int i = 0; i < n; i++) {
    scanf("%d", &A[i]);
    block[b][j] = A[i];
    if(++j == SIZE) { b++; j = 0; }
  }
  for(int i = 0; i < b; i++) sort(block[i], block[i]+SIZE);
  if(j) sort(block[b], block[b]+j);
}

int query(int L, int R, int v) {
  int lb = L/SIZE, rb = R/SIZE; // L和R所在块编号
  int k = 0;
  if(lb == rb) {
    for(int i = L; i <= R; i++) if(A[i] < v) k++;
  } else {
    for(int i = L; i < (lb+1)*SIZE; i++) if(A[i] < v) k++; // 第一块
    for(int i = rb*SIZE; i <= R; i++) if(A[i] < v) k++; // 最后一块
    for(int b = lb+1; b < rb; b++) // 中间的完整块
      k += lower_bound(block[b], block[b]+SIZE, v) - block[b];
  }
  return k;
}

void change(int p, int x) {
  if(A[p] == x) return;
  int old = A[p], pos = 0, *B = &block[p/SIZE][0]; // B就是p所在的块
  A[p] = x;

  while(B[pos] < old) pos++; B[pos] = x; // 找到x在块中的位置
  if(x > old) // x太大，往后交换
    while(pos < SIZE-1 && B[pos] > B[pos+1]) { swap(B[pos+1], B[pos]); pos++; }
  else // 往前交换
    while(pos > 0 && B[pos] < B[pos-1]) { swap(B[pos-1], B[pos]); pos--; }
}

int main() {
  init();
  while(m--) {
    int L, R, v, p;
    scanf("%d%d%d%d", &L, &R, &v, &p); L--; R--; p--;
    int k = query(L, R, v);
    change(p, (long long)u * k / (R-L+1));
  }
  for(int i = 0; i < n; i++) printf("%d\n", A[i]);
  return 0;
}
// 25878377	12003	Array Transformer	Accepted	C++	0.530	2020-12-23 09:05:32
```
