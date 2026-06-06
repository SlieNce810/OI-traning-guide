# 2.4 组合游戏

## 例题17  Treblecross游戏（Treblecross, UVa 10561）

### 题目描述
在一行有n个格子的直线上玩一个游戏。初始状态由字符串给出，每个格子要么是'X'（已被占据），要么是'.'（空位）。两个玩家轮流在任意一个空位放置一个'X'。第一个在自己的回合后使得出现连续三个'X'的玩家获胜。给定初始状态，判断先手是必胜还是必败。如果是必胜，输出所有必胜的第一步走法（即放置'X'的位置，1-indexed）。

**输入**：第一行T（T ≤ 100），测试组数。每组一行，一个字符串仅含'X'和'.'。

**输出**：如果先手必败，输出"LOSING"加一个空行。如果必胜，输出"WINNING"，下一行输出所有必胜第一步（升序，空格分隔）。

### 解题思路

**游戏分析**：当某个玩家在位置i放'X'后，位置i-2, i-1, i, i+1, i+2的格子都不能再放'X'了（否则另一个玩家可以立即形成三连）。这些格子称为"禁区"。

因此游戏可以看作是：在连续的"."段上玩子游戏，每个子游戏就是一个独立的长度为L的空格段。不同子游戏之间互不影响。

**SG函数（Sprague-Grundy）**：
- 定义g[i]为长度为i的连续空位的SG值
- g[0] = 0（没有空位）
- g[1] = g[2] = g[3] = 1（长度为1/2/3时放中间即可）
- 对于i≥4，如果在位置j放'X'，游戏分裂为两个子游戏：左边j-2个空格，右边i-j-3个空格（因为j周围的2个位置也变为禁区）
- g[i] = mex{ g[j-2] ^ g[i-j-3] | 所有合法位置j }

**判定胜负**：
1. 首先检查是否有连续3个X——如果有，游戏已经结束
2. 检查是否有玩家可以一步取胜——如果两个X距离≤2，先手在中间放X即可
3. 否则，将所有连续空格段的SG值异或起来。若结果为0，后手胜；否则先手胜

**找所有必胜第一步**：对每个空位i，假设在那里下子，检查新状态SG值是否为0（即留给对手必败态）。

### 算法方法
- **博弈论/SG函数**：Sprague-Grundy定理，将游戏分解为子游戏的Nim和
- **Mex运算**：预计算g数组

### 复杂度分析
- **时间复杂度**：预处理O(N²)计算SG，N≤200；每组询问O(n²)验证所有走法
- **空间复杂度**：O(N)，g数组

```cpp
// 例题17  Treblecross游戏（Treblecross, UVa 10561）
// 刘汝佳
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;

const int NN = 200;
int g[NN + 10];  // g[i]: 长度为i的连续空格的SG值

// 判断当前状态下先手是否必胜（不包含已经结束的情况）
bool winning(const char* state) {
  int n = strlen(state);
  // 检查是否已经出现连续3个X（某方已输）
  for (int i = 0; i < n - 2; i++)
    if (state[i] == 'X' && state[i + 1] == 'X' && state[i + 2] == 'X')
      return false;  // 已经输掉了

  int no[NN + 1];  // no[i]=1表示格子i是禁区（离某个'X'的距离≤2）
  fill_n(no, NN + 1, 0);
  no[n] = 1;  // 哨兵：标记字符串末端，方便分段
  for (int i = 0; i < n; i++) {
    if (state[i] != 'X') continue;
    // 检查'X'周围的格子
    for (int d = -2; d <= 2; d++)
      if (i + d >= 0 && i + d < n) {
        if (d != 0 && state[i + d] == 'X')
          return true;  // 有两个距离不超过2的'X'，一步即可取胜（在中间放一个）
        no[i + d] = 1;  // 标记为禁区
      }
  }

  int sg = 0;  // 总的SG异或值
  for (int i = 0, start = -1; i <= n; i++) {  // 遍历到哨兵
    if (start < 0 && !no[i]) start = i;       // 新的一段连续空格开始
    if (no[i] && start >= 0) sg ^= g[i - start];  // 当前段结束，异或其SG值
    if (no[i]) start = -1;  // 重置段起点
  }
  return sg != 0;  // SG异或非0则先手必胜
}

// 求最小未出现的非负整数（mex运算）
int mex(vector<int>& s) {
  if (s.empty()) return 0;
  sort(s.begin(), s.end());
  if (s[0] != 0) return 0;
  for (int i = 1; i < s.size(); i++)
    if (s[i] > s[i - 1] + 1) return s[i - 1] + 1;
  return s[s.size() - 1] + 1;
}

// 预计算SG值g[i]（长度≤NN的所有空格的SG值）
void init() {
  g[0] = 0, g[1] = g[2] = g[3] = 1;  // 边界值
  for (int i = 4; i <= NN; i++) {
    vector<int> s;
    s.push_back(g[i - 3]);              // 在位置0放X（最左边）
    s.push_back(g[i - 4]);              // 在位置1放X
    if (i >= 5) s.push_back(g[i - 5]);  // 在位置2放X
    // 在位置j(3≤j≤i-4)放X，分为左右两个子游戏
    for (int j = 3; j < i - 3; j++)
      s.push_back(g[j - 2] ^ g[i - j - 3]);  // 左j-2个，右i-j-3个
    g[i] = mex(s);  // mex值
  }
}

int main() {
  init();  // 预计算SG值
  int T;
  scanf("%d", &T);
  while (T--) {
    char state[NN + 10];
    scanf("%s", state);
    int n = strlen(state);
    if (!winning(state))
      puts("LOSING\n");  // 先手必败
    else {
      puts("WINNING");
      vector<int> moves;
      // 枚举所有第一步走法
      for (int i = 0; i < n; i++)
        if (state[i] == '.') {
          state[i] = 'X';  // 尝试在此下子
          if (!winning(state)) moves.push_back(i + 1);  // 如果对手必败，则这一步必胜
          state[i] = '.';  // 恢复
        }
      // 输出所有必胜第一步（已按1-indexed存储）
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

### 题目描述
有n堆石子，每堆有a_i个石子。两个玩家轮流操作，每次操作可以选择一堆石子，拿走至少一半（向上取整）的石子。即从一堆有x个石子的堆中，可以拿走⌈x/2⌉到x-1个石子（至少留一个）。不能操作的人输。判断先手是必胜还是必败。

**输入**：第一行T（T ≤ 100）。每组第一行n（1 ≤ n ≤ 100）。第二行n个整数a_i（1 ≤ a_i ≤ 10^18）。

**输出**：如果先手必胜，输出"YES"；否则输出"NO"。

### 解题思路

**SG函数的发现**：
这是典型的"分裂游戏"变体。定义SG(x)为有一堆x个石子的SG值。

分析递归关系：
- SG(0) = 0（无法操作）
- 对于x > 0，可以从x走到x'，其中⌈x/2⌉ ≤ x' < x（即拿走至少一半后剩下x'个）
- SG(x) = mex{SG(x') | ⌈x/2⌉ ≤ x' < x}

**关键规律**（通过打表发现）：
- 如果x是偶数：SG(x) = x/2
- 如果x是奇数：SG(x) = SG((x-1)/2)（递归到一半再加到整的奇数）

更简洁的实现：
当x是偶数时直接返回x/2；当x是奇数时递归SG(x/2)（整数除法向下取整）。

这是因为：对于奇数x，所有的操作都等价于从x的二进制表示中看，操作会减少数值。实际上SG(x)等于x在二进制下的某种变换。

**证明思路**：
可以发现SG函数满足：
SG(2k) = k（偶数直接一半）
SG(2k+1) = SG(k)（奇数递归到k）

这可以通过验证mex性质来证明。

总游戏的SG值 = SG(a_1) ^ SG(a_2) ^ … ^ SG(a_n)（Nim和，即异或）

先手必胜当且仅当总SG值≠0。

### 算法方法
- **博弈论/SG函数**：独立游戏的Nim和
- **递归/打表**：发现SG函数的简洁规律

### 复杂度分析
- **时间复杂度**：O(n·log a_max)，每个a_i递归O(log a_i)次
- **空间复杂度**：O(log a_max)，递归深度

```cpp
// 例题16  石子游戏（Playing with Stones, Jakarta 2010, UVa1482）
// Rujia Liu
#include <iostream>
using namespace std;

// 计算一堆有x个石子的SG值
// 规律：偶数SG(x)=x/2，奇数SG(x)=SG(x/2)
long long SG(long long x){
  // x为偶数时直接返回x/2，奇数时递归x/2（整数除法向下取整）
  return x%2==0 ? x/2 : SG(x/2);
}

int main() {
  int T;
  cin >> T;
  while (T--){
    int n;
    long long a, v = 0;  // v: 所有堆SG值的异或和
    cin >> n;
    for(int i = 0; i < n; i++) {
      cin >> a;
      v ^= SG(a);  // Nim和：异或各堆的SG值
    }
    // SG异或非0则先手必胜（Nim定理）
    if(v) cout << "YES\n";
    else cout << "NO\n";
  }
  return 0;
}
// 25877087  1482  Playing With Stones  Accepted  C++  0.000  2020-12-23 02:08:00
```
