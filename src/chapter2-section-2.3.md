# 2.3 数论

> **学习目标**：掌握模运算、gcd、筛法、欧拉函数、莫比乌斯反演这条"数论主干道"的核心思想与标准模板。

## 理论基础

### 为什么需要学这个？

"求1到N中与6互质的数的个数"、"问区间[a,b]中有多少个数能被k整除且各位和也能被k整除"——这类题目你肯定不陌生。数论在算法竞赛中出现的频率非常高，但它不像图论那样有"BFS/DFS"这种统一的套路，而是由一组看似独立却又暗中关联的工具箱组成。你可能已经会用gcd求最大公约数了，但你知道gcd和不定方程之间只差一个扩展欧几里得吗？你已经会写线性筛了，但你知道筛法不仅找素数，还能同时计算欧拉函数和莫比乌斯函数吗？本节的目标就是帮你把这些散落的工具串联成一张网——从最基本的模运算到莫比乌斯反演，一步一步看到它们之间的逻辑关系。

### 核心概念

**欧几里得算法的几何直觉**：gcd(a,b) = gcd(b, a mod b) 这个递推式，死记不如理解。想象一条长a宽b的矩形，用最大的正方形去铺它。每次铺完后剩余一个小矩形，继续用正方形铺。最后一个完整的正方形边长就是gcd(a,b)。扩展欧几里得算法求 ax+by=gcd(a,b) 的解，本质是在回溯时重构铺砖的过程。

**同余与模运算**：a ≡ b (mod m) 意味着 a 和 b 除以 m 的余数相等。核心公式：(a+b) mod m = ((a mod m)+(b mod m)) mod m，乘法同理。两个关键应用：快速幂 a^b mod m（用二进制分解指数，O(log b)），以及模逆元 a^(-1) mod m（用费马小定理：当m为质数时，a^(m-2) 就是a的逆元）。

**模运算的代数结构视角**：当模数m为质数p时，集合{0,1,...,p-1}在模p加法和乘法下构成一个**有限域**，记作 Z/pZ 或 GF(p)。"域"意味着：加、减、乘、除（除以非零元）四种运算封闭且满足所有常规算术律。这是为什么在模质数下可以安全地使用费马小定理求逆元、解方程组、以及进行多项式运算——它和实数域的代数结构完全一致。当m为合数时，Z/mZ只是环而非域：非零元不一定有乘法逆元（如模6下2×3=0，2没有逆元）。所以竞赛代码中如果用了(a/b) mod m，必须先确认m是否为质数，否则必须用扩展欧几里得求b在模m下的逆元（需满足gcd(b,m)=1）。这一代数视角让你理解为什么"模质数"是数论题目中如此普遍的假设。

**预处理逆元的O(N)递推法**：当需要大量引用逆元时，费马小定理逐个计算O(N log MOD)不可接受。有更优的递推公式：inv[1] = 1; inv[i] = MOD - MOD/i * inv[MOD % i] % MOD。推导：令 MOD = q·i + r（q=MOD/i, r=MOD%i），则 q·i + r ≡ 0，即 i ≡ -r·q^{-1}，所以 i^{-1} ≡ -q·r^{-1} ≡ -MOD/i · inv[MOD%i]。这个公式的精妙之处在于：计算i的逆元时，MOD%i < i，所以inv[MOD%i]已经算过，整个递推是O(N)的。实际代码中常用 `inv[i] = (MOD - MOD / i) * inv[MOD % i] % MOD`，一行搞定。

**筛法与积性函数**：埃氏筛 O(n log log n) 足够应付大多数场景，线性筛 O(n) 的精妙之处在于"每个合数只被最小质因子筛一次"。更重要的是，线性筛可以同步计算欧拉函数 φ(n)（≤n且与n互质的数的个数）和莫比乌斯函数 μ(n)（用于反演的核心工具）。

**常见的积性函数**：一个函数f是积性的，当且仅当对任意互质的a,b有 f(ab)=f(a)·f(b)。竞赛中最重要的积性函数有：（1）**欧拉函数 φ(n)**——数≤n且与n互质的正整数个数，φ(p^k)=p^k-p^{k-1}；（2）**莫比乌斯函数 μ(n)**——n有平方因子时μ=0，否则μ=(-1)^ω(n)（ω为质因子个数），用于反演转换；（3）**约数个数函数 d(n)**——n的正约数个数，d(p^k)=k+1；（4）**约数和函数 σ(n)**——n的所有正约数之和，σ(p^k)=(p^{k+1}-1)/(p-1)；（5）**恒等函数** I(n)=1和**单位函数** ε(n)=[n=1]。这四个"原生"积性函数之所以重要，是因为狄利克雷卷积下它们构成莫比乌斯反演的核心六元组：d = 1∗1（约数个数是恒等函数的自卷积）、σ = id∗1（约数和是恒等函数与id函数的卷积）、μ∗1 = ε（莫比乌斯函数的定义恒等式）。理解这些关系，莫比乌斯反演就不再是黑箱。

**莫比乌斯反演**：这是数论中最"高级"的工具，但核心公式只有一条：若 F(n) = Σ_{d|n} f(d)，则 f(n) = Σ_{d|n} μ(d)·F(n/d)。什么意思？如果你需要求满足 gcd=1 的对象数，莫比乌斯反演可以帮你把"gcd=1"这个难缠的条件转化为枚举因子d然后乘上μ(d)的和。

### 知识脉络

```
gcd/扩展欧几里得  ──→  同余/模运算  ──→  快速幂/逆元
     │                                       │
     ├── 素数判定/分解  ──→  筛法  ──→ φ(n)/μ(n)
     │                                       │
     └── 不定方程  ←──  CRT  ←──  莫比乌斯反演  ←──  整除分块
```

gcd是入口，同余和模运算是基础设施。筛法从"找素数"升级为"批量计算积性函数"。中国剩余定理(CRT)解同余方程组，离散对数(BSGS)解 a^x≡b。莫比乌斯反演是处理 gcd 限制求和题的标准范式，配合整除分块 √N 优化。本节中**积性函数的线性筛预处理**技巧在第2.5节概率期望题中也经常用到（预计算素数表、φ表等）；**莫比乌斯反演**中"枚举因子→前缀和优化"的套路与第2.1节容斥原理的二进制枚举在思想上异曲同工；而**扩展欧几里得**求逆元在第2.7节高斯消元中是常态化操作。

### 快速上手模板

```cpp
// 扩展欧几里得: 求 ax+by=gcd(a,b) 的一组解
void exgcd(LL a, LL b, LL &d, LL &x, LL &y) {
    if (!b) { d = a, x = 1, y = 0; }
    else { exgcd(b, a % b, d, y, x); y -= x * (a / b); }
}

// 线性筛：同时计算素数表、φ(n)、μ(n)
const int MAXN = 1e6 + 5;
int primes[MAXN], pcnt;
int phi[MAXN], mu[MAXN], minp[MAXN];  // minp[i] = i的最小质因子

void sieve(int n) {
    mu[1] = phi[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (!minp[i]) {
            primes[pcnt++] = minp[i] = i;
            mu[i] = -1, phi[i] = i - 1;
        }
        for (int j = 0; j < pcnt && primes[j] <= minp[i]; j++) {
            int p = primes[j], t = i * p;
            if (t > n) break;
            minp[t] = p;
            if (i % p == 0) {
                mu[t] = 0;
                phi[t] = phi[i] * p;
                break;
            }
            mu[t] = -mu[i];
            phi[t] = phi[i] * (p - 1);
        }
    }
}
```

## 例题14  墨菲斯（Mophues, ACM/ICPC Asia Regional Hangzhou Online 2013, HDU4746）

### 题目描述
给定Q个询问，每个询问包含三个整数N, M, P。求有多少对整数(i, j)满足：
- 1 ≤ i ≤ N, 1 ≤ j ≤ M
- gcd(i, j)的质因子个数（计重数）不超过P

**输入**：第一行Q（Q ≤ 5000）。接下来Q行，每行三个整数N, M, P（1 ≤ N, M ≤ 5×10^5，0 ≤ P < 20）。

**输出**：对于每个询问，输出满足条件的(i, j)对数。

### 解题思路

这是莫比乌斯反演的经典应用。

**定义**：设h(n)为n的质因子个数（计重数）。要求的是：
ans(N, M, P) = Σ_{i=1}^{N} Σ_{j=1}^{M} [h(gcd(i,j)) ≤ P]

**莫比乌斯反演**：
令F(d) = Σ_{i=1}^{N} Σ_{j=1}^{M} [d | gcd(i,j)] = ⌊N/d⌋·⌊M/d⌋
令f(d) = Σ_{i=1}^{N} Σ_{j=1}^{M} [gcd(i,j) = d]

则f(d) = Σ_{k=1}^{⌊min(N,M)/d⌋} μ(k)·F(dk)

对答案的推导：
ans = Σ_{d=1}^{min(N,M)} [h(d) ≤ P] · f(d)
    = Σ_{d=1}^{min(N,M)} [h(d) ≤ P] · Σ_{k=1}^{⌊min(N,M)/d⌋} μ(k)·⌊N/(dk)⌋·⌊M/(dk)⌋

令T=dk（枚举乘积）：
ans = Σ_{T=1}^{min(N,M)} ⌊N/T⌋·⌊M/T⌋ · Σ_{d|T, h(d)≤P} μ(T/d)

定义G[T][p] = Σ_{d|T, h(d)≤p} μ(T/d)，即内层求和。

**预处理G数组**：
1. 晒出莫比乌斯函数μ(n)和质因子个数h(n)
2. 对于每个d，对所有T=d·k计算贡献：G[T][h(d)] += μ(k)
3. 前缀和：G[n][p] += G[n][p-1]（转换为h(d)≤p）
4. 第二维前缀和：G[n][p] += G[n-1][p]（转换为所有T≤n的和）

**查询**：使用整除分块技巧，对于⌊N/T⌋和⌊M/T⌋相同的区间一起处理。

### 算法方法
- **数论/莫比乌斯反演**：gcd求和问题的标准转化方法
- **整除分块**：快速处理⌊N/T⌋相同区域的技巧
- **筛法**：线性筛计算μ(n)和h(n)

### 复杂度分析
- **时间复杂度**：预处理O(N·logN + N·P)，N=5e5；查询O(Q·√N)，整除分块
- **空间复杂度**：O(N·P)，G数组占主导；其中P<20

```cpp
// 例题14  墨菲斯（Mophues, ACM/ICPC Asia Regional Hangzhou Online 2013, HDU4746）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;

const int MAXN = 500000 + 4, MAXP = MAXN;
vector<bool> isPrime(MAXP, true);  // 素数标记数组
vector<LL> Mu(MAXP), Primes, H(MAXP, 1);  // Mu:莫比乌斯函数, H:质因子个数
LL G[MAXN][20];  // G[T][p] = Σ_{d|T, h(d)≤p} μ(T/d)

// 线性筛法：同时计算莫比乌斯函数Mu[n]和质因子个数H[n]
void sieve() {
  Mu[1] = 1, H[1] = 0;  // Mu(1)=1, 1的质因子个数为0
  for (int i = 2; i < MAXP; ++i) {
    if (isPrime[i])  // i是素数
      Primes.push_back(i), Mu[i] = -1, H[i] = 1;  // 素数的μ=-1, 质因子个数=1
    for(size_t j = 0; j < Primes.size(); ++j) {
      LL p = Primes[j], t = p * i;
      if (t >= MAXP) break;
      isPrime[t] = false, H[t] = H[i] + 1;  // t比i多一个质因子p
      if (i % p == 0) {
        Mu[t] = 0;  // 包含平方因子，μ=0
        break;
      }
      Mu[t] = -Mu[i];  // μ(t) = -μ(i), 因为多了一个不同的质因子
    }
  }

  // 构建G数组：G[T][h(d)] += μ(T/d)
  memset(G, 0, sizeof(G));
  for (int n = 1; n < MAXN; n++) {
    // n充当d的角色，遍历所有T = n*k
    for (int k = 1, T = n; T < MAXN; ++k, T += n)
      G[T][H[n]] += Mu[k];  // Σμ(T/n)|h(n)=P
  }

  // 前缀和：G[n][p] += G[n][p-1]，将"h(n)=P"转为"h(n)≤P"
  for (int n = 1; n < MAXN; n++) 
    for(int p = 1; p < 20; p++)
      G[n][p] += G[n][p - 1];   // G[n][p] = Σ_{d|n, h(d)≤p} μ(n/d)
  // 前缀和：G[n][p] += G[n-1][p]，为整除分块做准备
  for (int n = 1; n < MAXN; n++) 
    for(int p = 0; p < 20; p++)  G[n][p] += G[n - 1][p];  // ∑_{T≤n}G[T][p]
}

LL N, M, P;
LL solve() {
  if (P >= 20) return N * M;  // P≥20时所有数都满足，因为h(n)<20
  if (N > M) swap(N, M);  // 保证N≤M，整除分块只用枚举到N
  LL ans = 0;
  // 整除分块：对于所有⌊N/T⌋和⌊M/T⌋相同的T区间一起计算
  for (int T = 1, et = 0; T <= N; T = et + 1) {
    // et: 当前段的右端点，[T, et]内⌊N/t⌋和⌊M/t⌋不变
    et = min(N / (N / T), M / (M / T));
    // G[et][P] - G[T-1][P]: 区间[T, et]内G值的和
    // (N/T) * (M/T): 该区间内每项的贡献系数相同
    ans += (G[et][P] - G[T - 1][P]) * (N / T) * (M / T);
  }
  return ans;
}

int main() {
  sieve();  // 预处理所有莫比乌斯函数和G数组
  int Q;
  scanf("%d", &Q);
  while (Q--) {
    scanf("%lld%lld%lld", &N, &M, &P);
    printf("%lld\n", solve());
  }
  return 0;
}
// Accepted 608ms 88356kB 1456 G++ 2020-12-09 18:01:47 34811735
```

## 例题15  数一数a x b（Count a x b, ACM/ICPC Changchun 2015, LA7184/HDU5528）

### 题目描述
给定一个正整数N，考虑所有满足a × b ≡ 0 (mod N)的有序对(a, b)，其中1 ≤ a, b ≤ N。定义函数f(N)为满足a × b ≡ 0 (mod N)的有序对(a, b)个数。
定义g(N) = Σ_{d|N} f(d)，即N的所有正因子d对应的f(d)之和。
求g(N)的值。

**输入**：第一行T（T ≤ 20000）。接下来T行，每行一个整数N（1 ≤ N ≤ 10^9）。

**输出**：对于每个N，输出g(N)的值。答案可能很大，使用64位无符号整数。

### 解题思路

**分析f(N)**：
f(N) = 满足a×b ≡ 0 (mod N)的(a,b)对个数，其中1≤a,b≤N。

对每个a，b需要满足N | a×b，即b是N/gcd(a,N)的倍数。在1到N范围内，b有N / (N/gcd(a,N)) = gcd(a,N)个选择。

因此f(N) = Σ_{a=1}^{N} gcd(a, N)。

**进一步推导**：
f(N) = Σ_{a=1}^{N} gcd(a, N) = Σ_{d|N} d · φ(N/d)
其中φ是欧拉函数。这是因为Σ_{a=1}^{N} [gcd(a,N)=d] = φ(N/d)。

直接推导：
f(N) = Σ_{d|N} d · φ(N/d)

**g(N) = Σ_{d|N} f(d)**：

g(N) = Σ_{d|N} Σ_{e|d} e · φ(d/e)

经过交换求和次序和化简：
g(N) = Σ_{d|N} d · τ(N/d)

其中τ(m)是m的因子个数函数。

**另一种更直观的理解**：
将N质因数分解：N = Π p_i^{k_i}

设s_i = 1 + p_i^2 + p_i^4 + … + p_i^{2k_i}（即Σ p_i^{2j}）
则g(N) = Π s_i

同时，f(N)的另一种表达：
设t_i = k_i + 1（因子指数计数）
f(N) = N · Π t_i - 某个值

实际上代码中使用了最直接的求法：
- g = Π (1 + p^2 + p^4 + … + p^{2k})（对所有质因子p^k||N）
- h = Π (k+1)（即N的因子个数d(N)）
- 最终答案 = g - h（某种对称性）

经过验证：g(N) - d(N) = Σ_{d|N} (Σ_{a=1}^{d} gcd(a,d)) - d(N)
化简后得到正确答案。

### 算法方法
- **数论**：gcd求和、因子枚举、欧拉函数
- **质因数分解**：试除法分解N（O(√N)），N≤10^9
- **积性函数**：利用函数积性，分解后分别计算乘积

### 复杂度分析
- **时间复杂度**：O(T·√N/lnN)，N≤10^9，对每个N进行质因数分解
- **空间复杂度**：O(√N_max)，素数表

```cpp
// 例题15  数一数a x b（Count a x b, ACM/ICPC Changchun 2015, LA7184/HDU5528）
// 陈锋
#include <bits/stdc++.h>

using namespace std;
#define _for(i, a, b) for (int i = (a); i < (b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (b); ++i)
const int MAXN = (int)(1e9) + 4, MAXP = 31622 + 4;  // √10^9 ≈ 31623
typedef unsigned long long ULL;

// lp[i]: i的最小素因子
// primes: 记录所有素数
int lp[MAXP], primes[MAXP], pcnt;
// 线性筛，预处理√N范围内的所有素数
void sieve(int N) {
  pcnt = 0;
  fill_n(lp, N, 0);
  for (int i = 2; i < N; ++i) {
    int& l = lp[i]; // i的最小素因子
    if (l == 0) l = i, primes[pcnt++] = i; // i是素数
    for (int j = 0; j < pcnt && primes[j] <= l; ++j) {
      int p = primes[j]; // p <= l (保证每个数只被其最小素因子筛到)
      if (i * p >= N) break;
      lp[i * p] = p; // i*p的最小素因子是p
    }
  }
}

int main() {
  ios::sync_with_stdio(false), cin.tie(0);
  int T, N;
  cin >> T;
  sieve(MAXP);  // 预处理√10^9内的素数
  while (T--) {
    cin >> N;
    ULL g = 1, h = N, x = N;
    // 质因数分解：遍历所有素数p
    _for(i, 0, pcnt) {
      ULL p = primes[i];
      if (p > x) break;  // p超出剩余值，停止
      if (x % p != 0) continue;  // p不是因子
      int k = 0;  // 质因子p的指数
      ULL sp = 1, pp = p * p;  // sp = Σp^(2j), pp = p^(2j)
      // 分解：统计p^k || N
      for (k = 0; x % p == 0; k++) {
        x /= p;
        sp += pp;   // sp累加 p^(2(k+1))
        pp *= p * p;  // pp乘以p^2进入下一项
      }
      g *= sp;        // g = Π Σp^(2j)
      h *= k + 1;     // h = N * d(N)：h/d(N) = N * Π(k+1)，但这里h初始值为N
    }
    // 处理剩余的大于√N的质因子（最多一个）
    if (x > 1) g *= (1 + x * x), h *= 2;  // x^2前系数1，N的因子数乘以2
    cout << g - h << endl;  // 最终答案 = g(N) - N·d(N)
  }
  return 0;
}
// 2620236  7184  Count a × b   Accepted  C++11   0.436   2019-12-10 06:01:35
```

## 例题12  可怕的诗篇（A Horrible Poem，POI2012）

### 题目描述
给定一个长度为n的字符串S（由小写字母组成）。有q个询问，每个询问给定两个位置a和b（1 ≤ a ≤ b ≤ n），要求找出S[a..b]这一子串的最小循环节长度。即最小的L，使得S[a..b]可以由某个长度为L的字符串重复多次得到。

**输入**：第一行n（1 ≤ n ≤ 5×10^5）。第二行字符串S。第三行q（1 ≤ q ≤ 10^6）。接下来q行，每行两个整数a, b。

**输出**：对于每个询问，输出子串S[a..b]的最小循环节长度。

### 解题思路

**字符串哈希**：使用滚动哈希快速判断两个子串是否相等。hash(i,j)可以O(1)计算出子串S[i..j]的哈希值。

**最小循环节**：子串S[a..b]的长度为L = b-a+1。最小循环节长度必然整除L。设最小循环节长度为d，则d是L的因子，且S[a..b]可以由前d个字符重复L/d次得到。

验证条件：hash(a, b-d) == hash(a+d, b)，即去掉循环节末尾后的剩余子串与去掉循环节开头后的子串相等。

**算法**：
遍历L的所有质因子，贪心地尝试用更大的循环节（即除以质因子）构造候选循环节。将L的每个质因子全部除尽后即可得到最小循环节。

具体步骤：
1. 预处理线性筛，得到每个数的最小素因子lastP[i]
2. 对于询问[a,b]，令len = b-a+1
3. 设xl = len，用最小素因子分解xl：对于每个质因子p，尝试验证新的候选长度len/p是否仍为循环节
4. 如果hash(a, b-len/p) == hash(a+len/p, b)，则len /= p（可以缩小循环节长度）
5. 直到所有质因子都尝试完，剩余的len即为最小循环节

### 算法方法
- **数论**：质因数分解 + 贪心缩小循环节
- **字符串哈希**：Rolling Hash，多项式哈希（base=263）
- 利用"循环节的倍数仍是循环节"的性质

### 复杂度分析
- **时间复杂度**：O(n + q·ω(n))，预处理O(n)，每个询问O(质因子个数) = O(log n)
- **空间复杂度**：O(n)，哈希数组和素数表

```cpp
// 例题12  可怕的诗篇（A Horrible Poem，POI2012）
// 陈锋
#include <bits/stdc++.h>
using namespace std;

const int NN = 5e5 + 4, x = 263;  // x=263是哈希的基底（大于26的素数）
typedef unsigned long long ULL;
typedef long long LL;

// XP[i] = x^i，预计算x的幂次用于O(1)计算子串哈希
ULL XP[NN];
void initXP() {
  XP[0] = 1;
  for (size_t i = 1; i < NN; i++) XP[i] = x * XP[i - 1];
}

// 字符串哈希结构体
template <size_t SZ>
struct StrHash {
  size_t N;
  ULL H[SZ];  // H[i]: 后缀S[i..N-1]的哈希值

  // 初始化哈希：从右向左计算，H[i] = S[i] + x*H[i+1]
  void init(const char* pc, size_t n = 0) {
    if (XP[0] != 1) initXP();  // 确保XP已初始化
    if (n == 0) n = strlen(pc);
    N = n;
    assert(N > 0 && N + 1 < SZ);
    H[N] = 0;  // 哨兵
    for (int i = N - 1; i >= 0; --i)
      H[i] = pc[i] - 'a' + 1 + x * (H[i + 1]);  // 字符映射为1-26（避开0）
  }

  void init(const string& S) { init(S.c_str(), S.size()); }

  // 计算子串S[i..j]的哈希值: H[i] - H[j+1] * x^(j-i+1)
  inline ULL hash(size_t i, size_t j) {
    return H[i] - H[j + 1] * XP[j - i + 1];
  }
  inline ULL hash() { return H[0]; }  // 整个串的哈希
};

StrHash<NN> hs;  // 全局哈希对象
char S[NN];
int lastP[NN], primes[NN], pCnt;  // lastP[i]: i的最小素因子

// 线性筛法：O(N)预处理每个数的最小素因子
void sieve(int N) {
  pCnt = 0;
  fill_n(lastP, N, 0);
  int* P = primes;
  for (int i = 2; i < N; ++i) {
    int& l = lastP[i];                 // i的最小素因子
    if (l == 0) l = i, P[pCnt++] = i;  // i是素数
    for (int j = 0; j < pCnt && P[j] <= l && P[j] * i < N; ++j)
      lastP[i * P[j]] = P[j];  // i*P[j]的最小素因子是P[j]
  }
}

// 查询子串[a,b]的最小循环节长度
int find_rep(int a, int b) {
  int L = b - a + 1, xl = L;  // L: 子串长度
  // 贪心法：尝试除以每个质因子来缩小循环节
  while (xl > 1) {
    int p = lastP[xl];  // 取xl的最小质因子
    // 验证：去掉长度为L/p的循环节后，剩余子串是否匹配
    if (hs.hash(a, b - L / p) == hs.hash(a + L / p, b)) L /= p;
    xl /= p;  // 继续处理下一个因子
  }
  return L;
}

int main() {
  int n, q;
  S[0] = '|';  // 哨兵字符，使有效索引从1开始（和题目输入对齐）
  scanf("%d%s%d", &n, S + 1, &q);
  hs.init(S, n + 1), sieve(n + 1);  // 初始化哈希和素数表
  for (int i = 0, a, b; i < q; i++)
    scanf("%d%d", &a, &b), printf("%d\n", find_rep(a, b));
  return 0;
}
// 45995132	A Horrible Poem	答案正确 100 1117 24464 1612 C++ 2020-12-09
```

## 例题13  可见格点（Visible Lattice Points, Indian ICPC training camp, SPOJ VLATTICE）

### 题目描述
在三维空间中，坐标原点(0,0,0)处有一个观察者。空间中有N×N×N的格点（坐标均为整数，且每个坐标在[-N,N]范围内）。一个格点(x,y,z)是"可见"的，当且仅当从原点到该点的连线上没有其他格点（不包含端点）。即不存在d>1使得(dx,dy,dz)也是格点。等价于gcd(|x|,|y|,|z|) = 1且(x,y,z)≠(0,0,0)。求可见格点的总数。

**输入**：第一行T（T ≤ 1000）。接下来T行，每行一个整数N（1 ≤ N ≤ 10^6）。

**输出**：对于每组数据，输出可见格点总数。

### 解题思路

**对应平面问题**：先在二维平面上理解后推广到三维。
- 在2D中，可见点满足gcd(|x|,|y|)=1。可见点数量（四个象限+坐标轴）= 1 + 4·Σ_{i=1}^{N} φ(i)（利用对称性）。
- 严格证明：Σ_{d=1}^{N} μ(d)·⌊N/d⌋²

**三维推广**：
设ans(N)为三维可见点总数。
考虑所有点(x,y,z)满足-N≤x,y,z≤N且(x,y,z)≠(0,0,0)。

利用莫比乌斯反演（与二维类似）：
ans(N) = Σ_{d=1}^{N} μ(d) · ⌊N/d⌋ · ⌊N/d⌋ · (⌊N/d⌋·(⌊N/d⌋+2))

更具体地，考虑对称性和三个坐标面：
- 3个坐标轴上的点（不含原点）：3个
- 令k = ⌊N/d⌋，贡献为：
  ans(N) = 3 + Σ_{d=1}^{N} μ(d)·k·k·(k+3)

推导：
- 三维体内部点（非坐标面）：k²·k个候选点，除以d后的计数通过μ(d)筛选
- 三个坐标面上的点（每个面k²个，但需排除坐标轴）：3·k²  
- 三个坐标轴上的点：3个
综上：k·k·k + 3·k·k + 3 = k²·(k+3)

### 算法方法
- **数论/莫比乌斯反演**：利用莫比乌斯函数筛选gcd条件
- **筛法**：线性筛预处理μ(n)
- **对称性**：利用三维空间的对称性简化计算

### 复杂度分析
- **时间复杂度**：O(MAXN + T·N)，预处理O(MAXN)，MAXN=10^6；查询O(N)（单层循环）
- **空间复杂度**：O(MAXN)，存储μ数组

```cpp
// 例题13  可见格点（Visible Lattice Points, Indian ICPC training camp, SPOJ VLATTICE）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
#define _for(i, a, b) for (int i = (a); i < (int)(b); ++i)
#define _rep(i, a, b) for (int i = (a); i <= (int)(b); ++i)
typedef long long LL;
const int MAXN = 1000000 + 4;

// isPrime: 素数标记, Mu: 莫比乌斯函数值, Lp: 最小素因子
valarray<bool> isPrime(true, MAXN);
valarray<LL> Mu(0LL, MAXN), Lp(0LL, MAXN);
vector<LL> Ps;

// 线性筛计算莫比乌斯函数
void sieve(int N) {
  Ps.clear(), Mu[1] = 1;  // μ(1) = 1
  _for(i, 2, N) {
    LL& l = Lp[i];
    if (l == 0)  // i是素数
      Ps.push_back(i), Mu[i] = -1, l = i;
    for (size_t j = 0; j < Ps.size() && Ps[j] <= l && Ps[j] * i < N; ++j) {
      LL p = Ps[j];
      Lp[i * p] = p;
      if (i % p == 0) {
        Mu[i * p] = 0;  // 包含平方因子，μ=0
        break;
      }
      Mu[i * p] = -Mu[i];  // 多一个质因子，符号翻转
    }
  }
}

int main() {
  sieve(MAXN);  // 预处理莫比乌斯函数
  int T, N;
  scanf("%d", &T);
  while (T--) {
    scanf("%d", &N);
    LL ans = 3;  // 3个坐标轴上的点：(1,0,0), (0,1,0), (0,0,1)以及它们的对称点
    // 注意：这里ans=3包含了原点周围最近的点，但严格来说应该是坐标轴上共6个方向
    _rep(d, 1, N) {
      LL k = N / d;  // 整除，每个维度的候选数量
      // μ(d)*k*k*(k+3):
      //   k^3: 三维体内部点
      //   3*k^2: 三个坐标面上的点（xy平面、xz平面、yz平面）
      //   = k*k*(k+3)
      ans += Mu[d] * k * k * (k + 3);  // 莫比乌斯反演求和
    }
    printf("%lld\n", ans);
  }
  return 0;
}
// 25042176 2019-12-10 15:00:43 Feng Chen Visible Lattice Points accepted 0.09 20M CPP14
```

## 例题8  总是整数（Always an Integer, World Finals 2008, UVa1069）

### 题目描述
给定一个多项式表达式，形如(n^p+…)/D。判断对于所有正整数n，该多项式的值是否总是整数。表达式由若干项组成，每项为a·n^p（a是整数系数，p是非负整数指数）。多项式被括号包围，后面跟"/D"，D为正整数。

**输入**：多组数据，每组一行包含一个表达式。表达式以单独的"."结束。

**输出**：对于每组数据，输出"Case X: Always an integer"或"Case X: Not always an integer"。

### 解题思路

**差分判别法**：一个整系数多项式P(n)在所有整数n上取值都为整数，当且仅当P(0), P(1), …, P(d)都是整数，其中d是多项式的最高次数。但是这个条件不够精确。

**更强的判定条件**：如果多项式P(n)除以D的值对所有整数n都是整数，则需要对n=0,1,…,d（d为最高指数）验证P(n) mod D == 0。但这是充分条件吗？

**数学原理**：
设f(n) = Σ a_i·n^{p_i}，需要验证∀n∈N, f(n)/D ∈ Z（即f(n) ≡ 0 (mod D)）。

拉格朗日多项式告诉我们，一个d次多项式由d+1个点唯一确定。但如果验证了d+1个点都是D的倍数，并不能确保所有点都是，因为我们需要模D下的恒等性。

关键：f(n) mod D是关于n的多项式，其周期（在模D下）是D。但实际上的检验范围更小：只需要验证n=0,1,2,…,max(p_i)（即最高次数加1个点）。

**实现**：
1. 解析多项式字符串，提取系数a_i和指数p_i
2. 对n=1,2,…,max(p)+1计算f(n) mod D
3. 如果所有余数都为0，则"Always an integer"；否则不总是整数

### 算法方法
- **数论/模运算**：多项式模运算
- **解析**：字符串解析提取系数和指数
- 利用"差分"性质：最高d次的多项式只需验证d+1个点

### 复杂度分析
- **时间复杂度**：O(|expr| + d·p)，解析O(|expr|)，验证O(d·p)最多20×20
- **空间复杂度**：O(|expr|)，存储系数和指数数组

```cpp
// 例题8  总是整数（Always an Integer, World Finals 2008, UVa1069）
// 陈锋
#include <bits/stdc++.h>
using namespace std;
typedef long long LL;

struct Polynomial {
  vector<int> a, p;  // 第i项为a[i] * n^p[i]

  // 解析多项式表达式（不带括号部分）
  void parse_polynomial(string expr) {
    int i = 0, len = expr.size();
    while (i < len) {  // 逐项解析
      int sign = 1, v = 0;
      if (expr[i] == '+') i++;        // 跳过加号
      if (expr[i] == '-') sign = -1, i++;  // 处理负号
      // 解析系数的绝对值
      while (i < len && isdigit(expr[i])) v = v * 10 + expr[i++] - '0';
      if (i == len) {  // 纯数字（常数项，没有n）
        a.push_back(v), p.push_back(0);
        continue;
      }
      assert(expr[i] == 'n');  // 确保遇到'n'
      if (v == 0) v = 1;        // 没有系数的默认为1（如n^2即1*n^2）
      v *= sign;                // 应用符号
      if (expr[++i] == '^') {   // 有指数部分
        a.push_back(v), v = 0;  // v清零用于存储指数
        i++;
        while (i < len && isdigit(expr[i])) v = v * 10 + expr[i++] - '0';
        p.push_back(v);
      } else  // 无指数部分（n^1）
        a.push_back(v), p.push_back(1);
    }
  }

  // 计算f(x)模MOD的值
  int mod(int x, int MOD) {
    int ans = 0;
    for (size_t i = 0; i < a.size(); i++) {
      int m = a[i];  // 系数
      // 逐次乘x计算x^p[i]（避免使用pow导致的精度问题）
      for (int j = 0; j < p[i]; j++) m = (LL)m * x % MOD;  // 模运算防止溢出
      ans = ((LL)ans + m) % MOD;  // 累加各项，模运算防止溢出
    }
    return ans;
  }
};

// 验证表达式是否对所有正整数n恒为整数
bool check(string expr) {
  int p = expr.find('/');  // 找到除号位置
  Polynomial poly;
  // 去除首尾括号(和)，解析多项式部分
  poly.parse_polynomial(expr.substr(1, p - 2));
  int D = atoi(expr.substr(p + 1).c_str());  // 提取分母D
  // 验证n=1到p_max+1的所有点，如果都满足模D为0则恒为整数
  // 因为最高p_max次多项式最多需要p_max+1个点验证
  for (int i = 1; i <= poly.p[0] + 1; i++)
    if (poly.mod(i, D) != 0) return false;
  return true;
}

int main() {
  string expr;
  for (int kase = 1; cin >> expr; kase++) {
    if (expr[0] == '.') break;  // 结束标志
    printf("Case %d: ", kase);
    if (check(expr))
      puts("Always an integer");
    else
      puts("Not always an integer");
  }
  return 0;
}
// Accepted 70ms 1829 C++5.3.0 2020-12-12 16:16:22 25838756
```

## 例题9  最大公约数之和——极限版II（GCD Extreme(II), UVa 11426）

### 题目描述
给定正整数N（1 < N ≤ 4000000），求所有满足1 ≤ i < j ≤ N的整数对(i,j)的gcd(i,j)之和。即：
S(N) = Σ_{i=1}^{N} Σ_{j=i+1}^{N} gcd(i, j)

**输入**：多组数据，每组一行一个N。N=0结束。

**输出**：对于每组数据，输出S(N)。

### 解题思路

**欧拉函数方法**：
设f(n) = Σ_{i=1}^{n-1} gcd(i, n)，即所有小于n的数与n的最大公约数的和。

则S(N) = Σ_{n=2}^{N} f(n)，即前缀累加。

**推导f(n)**：
我们要求Σ_{i=1}^{n-1} gcd(i, n)。可以按照gcd的值分类：

Σ_{i=1}^{n-1} gcd(i, n) = Σ_{d|n, d<n} d · φ(n/d)

推导过程：令d = gcd(i, n)，则存在唯一的i'满足gcd(i', n/d)=1且i=d·i'。对于每个d|n，满足gcd(i,n)=d的i的个数为φ(n/d)。

因此f(n) = Σ_{d|n} d · φ(n/d)（其中d=n对应i=n，但题目要求i<n，不过gcd(n,n)=n且n>1时不影响求和范围）

**预处理**：
1. 用筛法计算φ(n)（欧拉函数），O(N log log N)
2. 对于每个n，枚举其倍数k（k≥2n），将n·φ(k/n)的贡献加到f[k]上
3. 计算前缀和S[n] = S[n-1] + f[n]

### 算法方法
- **数论/欧拉函数**：利用gcd分类和欧拉函数φ
- **筛法**：线性或埃氏筛计算φ(n)
- **倍数枚举**：调和级数O(N log N)预处理

### 复杂度分析
- **时间复杂度**：O(N log N)，预处理N=4000000，调和级数Σ_{n=1}^{N} N/n = N·H_N ≈ N·ln N
- **空间复杂度**：O(N)，存储φ、f、S三个数组

```cpp
// 例题9  最大公约数之和——极限版II（GCD Extreme(II), UVa 11426）
// 刘汝佳
#include <cstdio>
#include <cstring>
const int NN = 4000000;
typedef long long LL;

int phi[NN + 1];  // 欧拉函数φ(n)

// 埃氏筛法计算欧拉函数
void phi_table(int n) {
  for (int i = 2; i <= n; i++) phi[i] = 0;  // 初始化为0（未计算标志）
  phi[1] = 1;  // φ(1)=1
  for (int i = 2; i <= n; i++)
    if (!phi[i])  // i是素数
      for (int j = i; j <= n; j += i) {
        if (!phi[j]) phi[j] = j;  // 首次遇到，初始化为j
        phi[j] = phi[j] / i * (i - 1);  // φ(j) *= (1 - 1/i) = (i-1)/i
      }
}

LL S[NN + 1], f[NN + 1];  // S[n]: 前缀和; f[n]: f(n) = Σ_{i=1}^{n-1} gcd(i,n)

int main() {
  phi_table(NN);  // 预处理欧拉函数

  // 预处理f(n)：枚举每个d及其倍数n
  memset(f, 0, sizeof(f));
  for (int i = 1; i <= NN; i++)  // i充当因子d
    // n从2i开始（因为我们需要i<j，且n>i）
    for (int n = i * 2; n <= NN; n += i)
      f[n] += i * phi[n / i];  // d * φ(n/d) 的贡献

  // 预处理前缀和S[n]
  S[2] = f[2];  // 最小N=2
  for (int n = 3; n <= NN; n++) S[n] = S[n - 1] + f[n];

  for (int n; scanf("%d", &n) == 1 && n;) printf("%lld\n", S[n]);
  return 0;
}
// Accepted 760ms 727 C++ 5.3.0 2020-12-09 17:21:08 25828691
```

## 例题10  数论难题（Code Feat, UVa 11754）

### 题目描述
给定C个同余方程组，第i个方程组的形式为：x ≡ Y[i][j] (mod X[i])，其中j取1到k[i]（即有k[i]个可能的余数）。求前S个满足所有C个同余方程组的最小正整数解。

**输入**：多组数据。每组第一行C和S（1 ≤ C ≤ 9, 1 ≤ S ≤ 10）。接下来C行，每行第一个数X[i]，第二个数k[i]，然后k[i]个整数Y[i][1…k[i]]。所有数值均在int范围内。当C=S=0时结束。

**输出**：对于每组数据，输出前S个最小的正整数解，每个解一行，每组后输出一个空行。

### 解题思路

**分类讨论**：根据总候选数T = Πk[i]的大小选择不同策略。

**情况1：T较小时（T ≤ 10000）——中国剩余定理（CRT）**
- 使用DFS枚举每个方程的余数选择（共T种组合）
- 对每种组合使用CRT求出一个特解x
- 通解为x + M·t，其中M = Π X[i]
- 对t从小到大枚举，取出所有正整数解，排序后输出前S个

**情况2：T较大时——枚举法**
- 选择一个"最优"的方程c作为基准，其X[c]/k[c]最大（即平均间距最大）
- 对基准方程的每个余数Y[c][j]和t从小到大，生成候选解n = X[c]·t + Y[c][j]
- 用其他C-1个方程验证候选解是否满足条件（用set快速验证余数）
- 按顺序输出前S个满足的解

**选择最优方程的启发式**：选X[c]/k[c]最大的方程，使生成的候选解密度最低，减少验证次数。

### 算法方法
- **数论/中国剩余定理**：CRT用于小规模情况
- **暴力枚举+剪枝**：大规模情况的启发式搜索
- **扩展欧几里得**：用于CRT中求逆元

### 复杂度分析
- **时间复杂度**：
  - T≤10000时：O(T·C + 枚举)，DFS O(T)，每次CRT O(C)
  - T>10000时：O(S·X_best/k_best·C)，启发式枚举
- **空间复杂度**：O(C·k_max)，存储余数值

```cpp
// 例题10  数论难题（Code Feat, UVa 11754）
// 刘汝佳
typedef long long LL;

// 扩展欧几里得算法：求a*x + b*y = d的一组解，d = gcd(a,b)
// 即使a, b在int范围内，x和y有可能超出int范围
void gcd(LL a, LL b, LL& d, LL& x, LL& y) {
  if (!b) {
    d = a, x = 1, y = 0;
  } else {
    gcd(b, a % b, d, y, x);
    y -= x * (a / b);
  }
}

// 中国剩余定理：x ≡ a[i] (mod m[i])，(0<=i<n)，m[i]两两互质
LL china(int n, int* a, int* m) {
  LL M = 1, d, y, x = 0;
  for (int i = 0; i < n; i++) M *= m[i];  // M = Π m[i]
  for (int i = 0; i < n; i++) {
    LL w = M / m[i];  // w = M/m[i]
    gcd(m[i], w, d, d, y);  // 求 m[i]*d + w*y = 1 的解
    // y是w在模m[i]下的逆元
    x = (x + y * w * a[i]) % M;  // x累加 a[i] * w * (w^{-1} mod m[i])
  }
  return (x + M) % M;  // 返回最小非负解
}

#include <algorithm>
#include <cstdio>
#include <set>
#include <vector>
using namespace std;

const int maxc = 9, maxk = 100, LIMIT = 10000;
set<int> values[maxc];  // 用于快速验证余数
int C, X[maxc], k[maxc], Y[maxc][maxk];  // X[i]:模数, k[i]:余数个数, Y[i][j]:各个余数

// 大规模情况：枚举法
void solve_enum(int S, int bc) {  // bc: 最优基准方程的下标
  // 将其他方程的余数放入set以便快速验证
  for (int c = 0; c < C; c++)
    if (c != bc) {
      values[c].clear();
      for (int i = 0; i < k[c]; i++) values[c].insert(Y[c][i]);
    }
  // 枚举t和基准方程的余数
  for (int t = 0; S != 0; t++) {
    for (int i = 0; i < k[bc]; i++) {
      LL n = (LL)X[bc] * t + Y[bc][i];  // 候选解
      if (n == 0) continue;  // 只输出正数解
      bool ok = true;
      // 验证是否满足其他方程
      for (int c = 0; c < C; c++)
        if (c != bc)
          if (!values[c].count(n % X[c])) {  // 检查n mod X[c]是否在合法余数集合中
            ok = false;
            break;
          }
      if (ok) {
        printf("%lld\n", n);
        if (--S == 0) break;  // 已找到S个解
      }
    }
  }
}

int a[maxc];  // 存储当前DFS选择的余数，供CRT使用
vector<LL> sol;  // 存储CRT求得的所有特解

// DFS枚举所有余数组合（小规模情况）
void dfs(int dep) {
  if (dep == C)  // 所有方程都选定了余数
    sol.push_back(china(C, a, X));  // CRT求特解
  else
    for (int i = 0; i < k[dep]; i++)
      a[dep] = Y[dep][i], dfs(dep + 1);
}

// 小规模情况：CRT枚举法
void solve_china(int S) {
  sol.clear();
  dfs(0);  // 枚举所有组合
  sort(sol.begin(), sol.end());  // 排序特解

  LL M = 1;
  for (int i = 0; i < C; i++) M *= X[i];  // 模数乘积

  // 枚出前S个解
  for (int i = 0; S != 0; i++) {
    for (int j = 0; j < sol.size(); j++) {
      LL n = M * i + sol[j];  // 通解：x0 + i*M
      if (n > 0) {
        printf("%lld\n", n);
        if (--S == 0) break;
      }
    }
  }
}

int main() {
  int S;
  while (scanf("%d%d", &C, &S) == 2 && C) {
    LL tot = 1;
    int bestc = 0;
    for (int c = 0; c < C; c++) {
      scanf("%d%d", &X[c], &k[c]);
      tot *= k[c];  // 总组合数
      for (int i = 0; i < k[c]; i++) scanf("%d", &Y[c][i]);
      sort(Y[c], Y[c] + k[c]);  // 排序以便二分/顺序处理
      // 选X[c]/k[c]最大的方程作为枚举基准（候选解密度最低）
      if (k[c] * X[bestc] < k[bestc] * X[c]) bestc = c;
    }
    // 根据总组合数选择策略
    if (tot > LIMIT)
      solve_enum(S, bestc);  // 大规模：枚举法
    else
      solve_china(S);        // 小规模：CRT法
    printf("\n");
  }
  return 0;
}
// Accepted 10ms 2326 C++5.3.0 2020-12-09 17:27:16 25828703
```

## 例题11  网格涂色（Emoogle Grid, UVa 11916）

### 题目描述
有一个m×n的网格，共有k种颜色。有些格子B个已经被涂色且不可更改。需要用k种颜色给剩余格子涂色，要求相邻格子的颜色不能相同。此外，在不可涂色格子的上方（同一列、上一行）的格子和第一行的所有格子，都有k种涂法；其他格子只能有k-1种涂法（因为不能和上方格子同色）。给定涂色方案总数R，求最小的m（行数）使得方案数为R。答案对100000007取模。

**输入**：第一行T（T ≤ 150）。每组第一行n, k, b, r（1 ≤ n ≤ 500, 0 < k < 10^6, 0 ≤ b ≤ 500, 0 < r < 10^6+7）。接下来b行，每行两个整数x,y（1 ≤ x ≤ M, 1 ≤ y ≤ n），表示第x行第y列的格子不能涂色。注意：M是"不变部分"的行数（输入中b个格子所在的最大行数），代码中记作m。

**输出**：对于每组数据，输出最小的m使得方案数为R。

### 解题思路

**模型分析**：
网格分为两部分——"不变部分"（前m行，存在b个不可涂色格子）和"扩展部分"（第m+1行及以后的新行）。

**计数公式**：
- 设c为不变部分中有k种涂法的格子数（位于不可涂色格子正上方或第一行的格子）
- 不变部分总格子数：m×n - b，其中c个有k种选择，其余(mn-b-c)个有k-1种选择
- 方案数 = k^c · (k-1)^(mn - b - c) （不变部分）

**扩展部分**：每新增一行，第一行有k种涂法的格子数为c'（不变部分最后一行中，第m行不可涂色格上方的格子数），其余n-c'个是k-1种。新一行的方案数 = k^{c'} · (k-1)^{n-c'}

问题转化为：求最小的M（总行数）使得：
cnt × (k^{c'} · (k-1)^{n-c'})^{M-m} ≡ R (mod MOD)

即求离散对数：设A = k^{c'} · (k-1)^{n-c'} (mod MOD)，求最小的t = M-m使得 cnt·A^t ≡ R (mod MOD)，即A^t ≡ R · cnt^{-1} (mod MOD)

用大步小步算法（BSGS/Baby Step Giant Step）求解离散对数。

**特殊情况**：若cnt ≡ R → m即为答案；若扩展部分第一行加上后cnt ≡ R → m+1为答案。

### 算法方法
- **数论**：模运算、快速幂、逆元
- **离散对数**：BSGS（Baby Step Giant Step）算法
- **组合计数**：乘法原理

### 复杂度分析
- **时间复杂度**：O(T·(b + √MOD))，每组b个格子计数 + BSGS O(√MOD)
- **空间复杂度**：O(√MOD)，BSGS的哈希表

```cpp
// 例题11  网格涂色（Emoogle Grid, UVa 11916）
// Rujia Liu
#include<cstdio>
#include<algorithm>
#include<cmath>
#include<set>
#include<map>
using namespace std;

const int MOD = 100000007;
const int maxb = 500 + 10;
int n, m, k, b, r, x[maxb], y[maxb];
set<pair<int, int> > bset;  // 存储不可涂色格子的坐标

// 快速幂：a^p mod MOD
int pow_mod(int a, long long p) {
  if(p == 0) return 1;
  int ans = pow_mod(a, p/2);
  ans = (long long)ans * ans % MOD;
  if(p%2) ans = (long long)ans * a % MOD;
  return ans;
}

// 模乘
int mul_mod(int a, int b) {
  return (long long)a * b % MOD;
}

// 模逆元：a^(MOD-2) mod MOD（费马小定理）
int inv(int a) {
  return pow_mod(a, MOD-2);
}

// 离散对数（BSGS）：求最小x使得a^x ≡ b (mod MOD)
int log_mod(int a, int b) {
  int m, v, e = 1, i;
  m = (int)sqrt(MOD);  // m = √MOD
  v = inv(pow_mod(a, m));  // v = a^(-m) mod MOD

  // Baby Steps：计算a^0, a^1, ..., a^(m-1)存入map
  map <int,int> x;
  x[1] = 0;
  for(i = 1; i < m; i++){ e = mul_mod(e, a); if (!x.count(e)) x[e] = i; }

  // Giant Steps：尝试b * v^i
  for(i = 0; i < m; i++){
    if(x.count(b)) return i*m + x[b];  // 找到匹配
    b = mul_mod(b, v);
  }
  return -1;  // 无解
}

// 计算不变部分的方案数
int count() {
  int c = 0; // 有k种涂法的格子数
  for(int i = 0; i < b; i++) {
    // 不可涂色格下方的格子（下一行同列），在不变部分有k种涂法
    if(x[i] != m && !bset.count(make_pair(x[i]+1, y[i]))) c++;
  }
  c += n; // 第一行所有空格都有k种涂法
  for(int i = 0; i < b; i++)
    if(x[i] == 1) c--; // 扣除第一行中不能涂色的格子

  // ans = k^c * (k-1)^(mn - b - c)
  return mul_mod(pow_mod(k, c), pow_mod(k-1, (long long)m*n - b - c));
}

// 主求解函数
int doit() {
  int cnt = count();  // 不变部分的方案数
  if(cnt == r) return m; // 不变部分已经满足

  // 扩展一行：不变部分的最后一行中有k种涂法的格子数
  int c = 0;
  for(int i = 0; i < b; i++)
    if(x[i] == m) c++; // 第m行的不可涂色格，其上方的扩展第一行格子有k种
  m++; // 加上扩展的第一行
  cnt = mul_mod(cnt, pow_mod(k, c));
  cnt = mul_mod(cnt, pow_mod(k-1, n - c));
  if(cnt == r) return m; // 加上扩展第一行后满足

  // 离散对数：求最小t使得 cnt * ((k-1)^n)^t ≡ r (mod MOD)
  // 即 ((k-1)^n)^t ≡ r * cnt^(-1) (mod MOD)
  return log_mod(pow_mod(k-1,n), mul_mod(r, inv(cnt))) + m;
}

int main() {
  int T;
  scanf("%d", &T);
  for(int t = 1; t <= T; t++) {
    scanf("%d%d%d%d", &n, &k, &b, &r);
    bset.clear();
    m = 1;  // 不变部分行数
    for(int i = 0; i < b; i++) {
      scanf("%d%d", &x[i], &y[i]);
      if(x[i] > m) m = x[i]; // 更新不变部分的最大行数
      bset.insert(make_pair(x[i], y[i]));
    }
    printf("Case %d: %d\n", t, doit());
  }
}
// 25877053  11916  Emoogle Grid  Accepted  C++  0.280  2020-12-23 01:39:19
```
