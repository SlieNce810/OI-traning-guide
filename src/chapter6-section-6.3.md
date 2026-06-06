# 6.3 暴力法专题

## LA2659 Sudoku/POJ3076 SEERC2006

```cpp
// LA2659 Sudoku/POJ3076 SEERC2006
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<vector>

using namespace std;

const int maxr = 5000;
const int maxn = 2000;
const int maxnode = 20000;

// 行编号从1开始，列编号为1~n，结点0是表头结点; 结点1~n是各列顶部的虚拟结点
struct DLX {
  int n, sz; // 列数，结点总数
  int S[maxn]; // 各列结点数

  int row[maxnode], col[maxnode]; // 各结点行列编号
  int L[maxnode], R[maxnode], U[maxnode], D[maxnode]; // 十字链表

  int ansd, ans[maxr]; // 解

  void init(int n) { // n是列数
    this->n = n;

    // 虚拟结点
    for(int i = 0 ; i <= n; i++) {
      U[i] = i; D[i] = i; L[i] = i-1, R[i] = i+1;
    }
    R[n] = 0; L[0] = n;

    sz = n + 1;
    memset(S, 0, sizeof(S));
  }

  void addRow(int r, vector<int> columns) {
    int first = sz;
    for(int i = 0; i < columns.size(); i++) {
      int c = columns[i];
      L[sz] = sz - 1; R[sz] = sz + 1; D[sz] = c; U[sz] = U[c];
      D[U[c]] = sz; U[c] = sz;
      row[sz] = r; col[sz] = c;
      S[c]++; sz++;
    }
    R[sz - 1] = first; L[first] = sz - 1;
  }

  // 顺着链表A，遍历除s外的其他元素
  #define FOR(i,A,s) for(int i = A[s]; i != s; i = A[i]) 

  void remove(int c) {
    L[R[c]] = L[c];
    R[L[c]] = R[c];
    FOR(i,D,c)
      FOR(j,R,i) { U[D[j]] = U[j]; D[U[j]] = D[j]; --S[col[j]]; }
  }

  void restore(int c) {
    FOR(i,U,c)
      FOR(j,L,i) { ++S[col[j]]; U[D[j]] = j; D[U[j]] = j; }
    L[R[c]] = c;
    R[L[c]] = c;
  }

  // d为递归深度
  bool dfs(int d) {
    if (R[0] == 0) { // 找到解
      ansd = d; // 记录解的长度
      return true;
    }

    // 找S最小的列c
    int c = R[0]; // 第一个未删除的列
    FOR(i,R,0) if(S[i] < S[c]) c = i;

    remove(c); // 删除第c列
    FOR(i,D,c) { // 用结点i所在行覆盖第c列
      ans[d] = row[i];
      FOR(j,R,i) remove(col[j]); // 删除结点i所在行能覆盖的所有其他列
      if(dfs(d+1)) return true;
      FOR(j,L,i) restore(col[j]); // 恢复结点i所在行能覆盖的所有其他列
    }
    restore(c); // 恢复第c列

    return false;
  }

  bool solve(vector<int>& v) {
    v.clear();
    if(!dfs(0)) return false;
    for(int i = 0; i < ansd; i++) v.push_back(ans[i]);
    return true;
  }

};

////////////// 题目相关
#include<cassert>

DLX solver;

const int SLOT = 0;
const int ROW = 1;
const int COL = 2;
const int SUB = 3;

// 行/列的统一编解码函数。从1开始编号
int encode(int a, int b, int c) {
  return a*256+b*16+c+1;
}

void decode(int code, int& a, int& b, int& c) {
  code--;
  c = code%16; code /= 16;
  b = code%16; code /= 16;
  a = code;
}

char puzzle[16][20];

bool read() {
  for(int i = 0; i < 16; i++)
    if(scanf("%s", puzzle[i]) != 1) return false;
  return true;
}

int main() {
  int kase = 0;
  while(read()) {
    if(++kase != 1) printf("\n");
    solver.init(1024);
    for(int r = 0; r < 16; r++)
      for(int c = 0; c < 16; c++) 
        for(int v = 0; v < 16; v++)
          if(puzzle[r][c] == '-' || puzzle[r][c] == 'A'+v) {
            vector<int> columns;
            columns.push_back(encode(SLOT, r, c));
            columns.push_back(encode(ROW, r, v));
            columns.push_back(encode(COL, c, v));
            columns.push_back(encode(SUB, (r/4)*4+c/4, v));
            solver.addRow(encode(r, c, v), columns);
          }

    vector<int> ans;
    assert(solver.solve(ans));

    for(int i = 0; i < ans.size(); i++) {
      int r, c, v;
      decode(ans[i], r, c, v);
      puzzle[r][c] = 'A'+v;
    }
    for(int i = 0; i < 16; i++)
      printf("%s\n", puzzle[i]);
  }
  return 0;
}
// Accepted 641ms 904kB 3295 G++2020-12-23 17:11:54|O22227210
```

## LA3789/UVa12112 Iceman

```cpp
// LA3789/UVa12112 Iceman
// Rujia Liu
#include<cstdio>
#include<cstring>
#include<string>
#include<map>
#include<queue>
using namespace std;

int n, m, target;
map<string, string> sol;
queue<string> q;

bool icy[256];
char link_l[256], link_r[256], clear_l[256], clear_r[256];

void init(){
  memset(icy, 0, sizeof(icy));
  icy['O'] = icy['['] = icy[']'] = icy['='] = true;
  memset(link_l, ' ', sizeof(link_l));
  link_l['O'] = ']'; link_l['['] = '=';
  memset(link_r, ' ', sizeof(link_r));
  link_r['O'] = '['; link_r[']'] = '=';
  memset(clear_l, ' ', sizeof(clear_l));
  clear_l[']'] = 'O'; clear_l['='] = '['; clear_l['O'] = 'O'; clear_l['['] = '[';
  memset(clear_r, ' ', sizeof(clear_r));
  clear_r['['] = 'O'; clear_r['='] = ']'; clear_r['O'] = 'O'; clear_r[']'] = ']';
}

string fall(string s){
  int k, r, p;
  for(int i = n-1; i >=0; i--)
    for(int j = 0; j < m; j++){
      char ch = s[i*m+j];
      if(ch == 'O' || ch == '@'){
        for(k = i+1; k < n; k++) if(s[k*m+j] != '.') break;
        s[i*m+j] = '.'; s[(k-1)*m+j] = ch;
      }else if(ch == '['){
        for(r = j+1; r < m; r++) if(s[i*m+r] == 'X' || s[i*m+r] == ']') break;
        if(s[i*m+r] == ']'){
          for(k = i+1; k < n; k++){
            bool found = false;
            for(p = j; p <= r; p++) if(s[k*m+p] != '.'){ found = true; break; }
            if(found) break;
          }
          for(p = j; p <= r; p++) s[i*m+p] = '.';
          for(p = j+1; p < r; p++) s[(k-1)*m+p] = '=';                        
          s[(k-1)*m+j] = '['; s[(k-1)*m+r] = ']';
        }
        j = r;
      }
    }
  return s;
}

int h(string s){
  int a, b, x = s.find('@');
  a = x%m - target%m; if(a < 0) a = -a;
  if(x/m > target/m) b = x/m - target/m; else b = (x/m < target/m ? 1 : 0);    
  return a > b ? a : b;
}

bool expand(string s, char cmd){
  string seq = sol[s] + cmd;   
  int x = s.find('@');
  s[x] = '.';
  if(cmd == '<' || cmd == '>'){
    s[x] = '@';
    int p = (cmd == '<' ? x+m-1 : x+m+1);
    if(s[p] == 'X') return false;
    else if(s[p] == '.'){
      s[p] = 'O';
      if(icy[s[p-1]]) s[p-1] = link_r[s[p-1]]; 
      if(s[p-1] != '.') s[p] = link_l[s[p]]; 
      if(icy[s[p+1]]) s[p+1] = link_l[s[p+1]];
      if(s[p+1] != '.') s[p] = link_r[s[p]];
    }else{
      s[p] = '.';
      if(icy[s[p-1]]) s[p-1] = clear_r[s[p-1]];
      if(icy[s[p+1]]) s[p+1] = clear_l[s[p+1]];
    }
  }else{
    int p = (cmd == 'L' ? x-1 : x+1);
    if(s[p] == '.') s[p] = '@';
    else{
      if(s[p] == 'O'){
        int k;
        if(cmd == 'L' && s[p-1] == '.'){
            for(k = p-1; k > 0; k--) if(s[k-1] != '.' || s[k+m] == '.') break;
            s[p] = '.'; s[k] = 'O'; s[x] = '@';
        }
        if(cmd == 'R' && s[p+1] == '.'){
            for(k = p+1; k < n*m; k++) if(s[k+1] != '.' || s[k+m] == '.') break;
            s[p] = '.'; s[k] = 'O'; s[x] = '@';
        }
      }
      if(s[p] != '.'){
        if(s[p-m] == '.' && s[x-m] == '.') s[p-m] = '@'; else s[x] = '@';
      }
   }
  }  
  s = fall(s);
  if(h(s) + seq.length() > 15) return false;
  if(s.find('@') == target){ printf("%s\n", seq.c_str()); return true; }
  if(!sol.count(s)){ sol[s] = seq; q.push(s); }
  return false;
}

int main(){
  int caseno = 0;
  init();
  while(scanf("%d%d", &n, &m) == 2){
    if(!n) break;
    char map[20][20];  
    for(int i = 0; i < n; i++) scanf("%s", map[i]);
    string s = "";
    for(int i = 0; i < n; i++)
      for(int j = 0; j < m; j++){
        if(map[i][j] == '#'){ target = i*m + j; map[i][j] = '.'; }
        s += map[i][j];
      }
    q.push(s);
    sol.clear();
    sol[s] = "";
    printf("Case %d: ", ++caseno);
    while(!q.empty()){
      string s = q.front();
      q.pop();
      if(expand(s, '<')) break; if(expand(s, '>')) break;
      if(expand(s, 'L')) break; if(expand(s, 'R')) break;
    }
    while(!q.empty()) q.pop();        
  }
}
// 25878414	12112	Iceman	Accepted	C++	0.040	2020-12-23 09:13:13
```

## UVa1085 House of Cards

```cpp
// UVa1085 House of Cards
// 刘汝佳
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<vector>
using namespace std;

const int UP = 0, FLOOR = 1, DOWN = 2, maxn = 20;
int n, deck[maxn*2];
struct State {
  int card[8], type[8]; // 两张相同的FLOOR牌代表一张真实的FLOOR牌
  int hold[2], pos, score; // MAX游戏者(即Axel)的得分
  State child() const {
    State s;
    memcpy(&s, this, sizeof(s));
    s.pos = pos + 1;
    return s;
  }

  State() {
    for(int i = 0; i < 8; i++) {
      card[i] = deck[i];
      type[i] = i % 2 == 0 ? UP : DOWN;
    }
    hold[0] = hold[1] = score = 0;
    pos = 8;
  }

  bool isFinal() {
    if(pos == 2*n) {
      score += hold[0] + hold[1];
      hold[0] = hold[1] = 0;
      return true;
    }
    return false;
  }

  int getScore(int c1, int c2, int c3) const {
    int S = abs(c1) + abs(c2) + abs(c3);
    int cnt = 0;
    if(c1 > 0) cnt++; if(c2 > 0) cnt++; if(c3 > 0) cnt++;
    return cnt >= 2 ? S : -S;
  }

  void expand(int player, vector<State>& ret) const {
    int cur = deck[pos];

    // 决策1：拿在手里
    if(hold[player] == 0) {
      State s = child();
      s.hold[player] = cur;
      ret.push_back(s);
    }

    // 决策2：摆楼面牌
    for(int i = 0; i < 7; i++) if(type[i] == DOWN && type[i+1] == UP) {
      // 用当前的牌
      State s = child();
      s.score += getScore(card[i], card[i+1], cur);
      s.type[i] = s.type[i+1] = FLOOR;
      s.card[i] = s.card[i+1] = cur;
      ret.push_back(s);
      
      if(hold[player] != 0) {
        // 用手里的牌
        State s = child();
        s.score += getScore(card[i], card[i+1], hold[player]);
        s.type[i] = s.type[i+1] = FLOOR; 
        s.card[i] = s.card[i+1] = hold[player];
        s.hold[player] = cur;
        ret.push_back(s);
      }
    }

    // 决策3：新的山峰
    if(hold[player] != 0)
      for(int i = 0; i < 7; i++) if(type[i] == FLOOR && type[i+1] == FLOOR && card[i] == card[i+1]) {
        State s = child();
        s.score += getScore(card[i], hold[player], cur);
        s.type[i] = UP; s.type[i+1] = DOWN; 
        s.card[i] = cur; s.card[i+1] = hold[player]; s.hold[player] = 0;
        ret.push_back(s);

        swap(s.card[i], s.card[i+1]);
        ret.push_back(s);
      }
  }
};

// 带alpha-beta剪枝的对抗搜索
int alphabeta(State& s, int player, int alpha, int beta) {
  if(s.isFinal()) return s.score; // 终态

  vector<State> children;
  s.expand(player, children); // 扩展子结点

  int n = children.size();
  for(int i = 0; i < n; i++) {
    int v = alphabeta(children[i], player^1, alpha, beta);
    if(!player) alpha = max(alpha, v); else beta = min(beta, v);
    if(beta <= alpha) break; // alpha-beta剪枝
  }
  return !player ? alpha : beta;
}
const int INF = 1e9;

int main() {
  int kase = 0;
  char P[10];
  while(scanf("%s", P) == 1 && P[0] != 'E') {
    scanf("%d", &n);
    for(int i = 0; i < n*2; i++) {
      char ch;
      scanf("%d%c", &deck[i], &ch);
      if(ch == 'B') deck[i] = -deck[i];
    }
    State initial;
    int first_player = deck[0] > 0 ? 0 : 1, score = alphabeta(initial, first_player, -INF, INF);
    if(P[0] == 'B') score = -score;
    printf("Case %d: ", ++kase);
    if(score == 0) printf("Axel and Birgit tie\n");
    else if(score > 0) printf("%s wins %d\n", P, score);
    else printf("%s loses %d\n", P, -score);
  }
  return 0;
}
// 25878419	1085	House of Cards	Accepted	C++	0.470	2020-12-23 09:14:12
```
