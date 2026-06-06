# 2.4 组合游戏

## 例题17  Treblecross游戏（Treblecross, UVa 10561）

```cpp
// 例题17  Treblecross游戏（Treblecross, UVa 10561）
// 刘汝佳
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;

const int NN = 200;
int g[NN + 10];

bool winning(const char* state) {
  int n = strlen(state);
  for (int i = 0; i < n - 2; i++)
    if (state[i] == 'X' && state[i + 1] == 'X' && state[i + 2] == 'X')
      return false;  // 已经输掉了

  int no[NN + 1];  // no[i] = 1: 下标为i的格子是“禁区”（离某个'X'的距离不超过2）
  fill_n(no, NN + 1, 0);
  no[n] = 1;  // 哨兵
  for (int i = 0; i < n; i++) {
    if (state[i] != 'X') continue;
    for (int d = -2; d <= 2; d++)
      if (i + d >= 0 && i + d < n) {
        if (d != 0 && state[i + d] == 'X')
          return true;  // 有两个距离不超过2的'X'，一步即可取胜
        no[i + d] = 1;
      }
  }

  int sg = 0;                                 // 当前块的起点坐标
  for (int i = 0, start = -1; i <= n; i++) {  // 注意要循环到“哨兵”为止
    if (start < 0 && !no[i]) start = i;       // 新的块
    if (no[i] && start >= 0) sg ^= g[i - start];  // 当前块结束
    if (no[i]) start = -1;
  }
  return sg != 0;
}

int mex(vector<int>& s) {
  if (s.empty()) return 0;
  sort(s.begin(), s.end());
  if (s[0] != 0) return 0;
  for (int i = 1; i < s.size(); i++)
    if (s[i] > s[i - 1] + 1) return s[i - 1] + 1;
  return s[s.size() - 1] + 1;
}

void init() {  // 预处理计算g数组
  g[0] = 0, g[1] = g[2] = g[3] = 1;
  for (int i = 4; i <= NN; i++) {
    vector<int> s;
    s.push_back(g[i - 3]);              // 最左边（下标为0的格子）
    s.push_back(g[i - 4]);              // 下标为1的格子
    if (i >= 5) s.push_back(g[i - 5]);  // 下标为2的格子
    for (int j = 3; j < i - 3; j++)     // 下标为3~i-3的格子
      s.push_back(g[j - 2] ^ g[i - j - 3]);  // 左边有j-2个，右边有i-j-3个格子
    g[i] = mex(s);
  }
}

int main() {
  init();
  int T;
  scanf("%d", &T);
  while (T--) {
    char state[NN + 10];
    scanf("%s", state);
    int n = strlen(state);
    if (!winning(state))
      puts("LOSING\n");
    else {
      puts("WINNING");
      vector<int> moves;
      for (int i = 0; i < n; i++)
        if (state[i] == '.') {
          state[i] = 'X';
          if (!winning(state)) moves.push_back(i + 1);
          state[i] = '.';
        }
      printf("%d", moves[0]);
      for (int i = 1; i < moves.size(); i++) printf(" %d", moves[i]);
      puts("");
    }
  }
  return 0;
}
// Accepted 2240 C++5.3.0 2020-12-12 17:23:57 25839095
```

## 例题16  石子游戏（Playing with Stones, Jakarta 2010, UVa1482）

```cpp
// 例题16  石子游戏（Playing with Stones, Jakarta 2010, UVa1482）
// Rujia Liu
#include <iostream>
using namespace std;

long long SG(long long x){
  return x%2==0 ? x/2 : SG(x/2);
}

int main() {
  int T;
  cin >> T;
  while (T--){
    int n;
    long long a, v = 0;
    cin >> n;
    for(int i = 0; i < n; i++) {
      cin >> a;
      v ^= SG(a);
    }
    if(v) cout << "YES\n";
    else cout << "NO\n";
  }
  return 0;
}
// 25877087  1482  Playing With Stones  Accepted  C++  0.000  2020-12-23 02:08:00
```
