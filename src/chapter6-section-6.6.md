# 6.6 浅谈代码设计与静态查错

本章通过两个综合性较强的题目展示良好的代码设计和静态查错方法。良好的代码结构（模块化、清晰的命名、合理的抽象）能显著减少bug，静态查错（肉眼走查、边界检查）比动态调试更高效。

## LA4488/UVa12233 Final Combat

### 题目描述
一个回合制战斗游戏，有4位英雄（Y, H, L, M）和最终boss（SY）。每回合英雄可以选择以下操作之一：
1. **蓄力**：积攒气力（q1[Hero]）
2. **武艺攻击**：消耗精力（jing）进行普通攻击，造成wad[Hero]伤害
3. **法术攻击**：消耗气力（qi）进行法术攻击，造成ssd[Hero]伤害
4. **玉润**：消耗神（shen）恢复精力
5. **疏尔过**：恢复神
6. 不做任何操作

boss会在固定时间（XXT, SYT）发动技能，造成伤害或减少伤害。英雄有精力上限、神上限、速度等属性。

游戏最多进行12个回合。玩家需要选择3个英雄分别占据1, 2, 3号位出战。求是否存在一种英雄排列方式，使得在某个回合数（≤12）内3位英雄的总伤害达到SY_jing（boss的血量）。

### 解题思路
使用**状态记忆化的动态规划搜索**：
- 状态包含：当前回合t，当前精力j，当前气力q，当前神s
- 状态空间压缩：j≤maxjing[Hero], q≤100, s≤maxshen[Hero]，编码为整数h=j*110000+q*1000+s
- DP函数`dfs(t, j, q, s)`：返回从该状态到第MaxT回合末能造成的最大伤害
- 记忆化：`map<int,int> Hash[t]`记录第t回合不同状态的最优解

转移时枚举6种操作，同时考虑boss在特定回合的技能效果（减精/加气）。每回合结束自动回气。

### 算法方法
**状态压缩DP + 记忆化搜索**：
1. 状态编码：将(精,气,神)编码为整数key
2. 转移方程：枚举当前回合可执行的操作
3. 英雄排列枚举：4×3×2=24种（从4个英雄中选3个排列）
4. 回合枚举：1~12回合，取最早能打败boss的回合数

代码结构清晰：
- 变量命名富有含义（jing=精, qi=气, shen=神, su=速等）
- 数据结构与游戏世界观一致
- 使用map实现记忆化，状态空间可预测

### 复杂度分析
- **时间复杂度**：O(MaxT × 24 × 状态数 × 转移数)。状态数约SumPa×101×SumShen≈1e7，但实际可达状态远少，因为map只存储访问过的状态
- **空间复杂度**：O(MaxT × 状态数)，使用map按需存储

```cpp
// LA4488/UVa12233 Final Combat
// Rujia Liu
// 题目：最终决战 - 回合制RPG战斗，状态DP求最优策略
#include<iostream>
#include<vector>
#include<map>
#include<string>
#include<algorithm>
using namespace std;

const int MAXTIME = 12;                     // 最大回合数
const int INF = 100000000;                  // 无穷大
const string name[] = {"Y", "H", "L", "M"}; // 四位英雄的名字

// 全局游戏参数
int SY_jing;          // 最终boss的血量（精力）
int XX_su;            // XX技能速度
int SY_su;            // SY技能速度
int yurun_jing;       // 玉润技能恢复的精力值
int yurun_shen;       // 玉润技能消耗的神值
int shuerguo_shen;    // 疏尔过技能恢复的神值

// 各英雄的属性
int maxjing[4];       // 精力上限
int maxshen[4];       // 神上限
int su[4];            // 速度
int d1x[4], d2x[4];  // XX技能的效果参数
int d1s[4], d2s[4];  // SY技能的效果参数
int wad[4];           // 武艺攻击伤害
int ssd[4];           // 法术攻击伤害
int ssq[4];           // 法术攻击气消耗
int ssp[4];           // 法术攻击属性（1=消耗精力）
int q1[4];            // 每回合恢复气力
int q2[4];            // 技能额外恢复气力
int jing[4];          // 初始精力
int qi[4];            // 初始气力
int shen[4];          // 初始神

// DP搜索参数
int MaxT;             // 最大回合数（枚举）
int Hero;             // 当前英雄编号
int Pos;              // 当前英雄的站位（1/2/3）
int HeroT;            // 英雄行动间隔
int XXT, SYT;         // boss技能间隔

map<int,int> Hash[MAXTIME + 1];  // Hash[t][state] = 最大伤害，按回合记忆化

// DFS搜索函数
// t: 当前回合, j: 当前精力, q: 当前气力(0~100), s: 当前神
// 返回值：从当前状态到终局能造成的最大伤害
int dfs(int t, int j, int q, int s) {
  if(j <= 0) return -INF;  // 精力耗尽，无效状态
  if(t > MaxT) return 0;   // 超出最大回合，没有后续伤害
  
  // 状态归一化（不超出上限）
  j = min(j, maxjing[Hero]);
  q = min(q, 100);
  s = min(s, maxshen[Hero]);
  
  // 编码状态为整数（用于哈希）
  int h = j * 110000 + q * 1000 + s;
  
  // 记忆化查表
  if(Hash[t].count(h)) return Hash[t][h];
  
  // 计算boss本回合技能效果
  int dj = 0, dq = 0;  // 精力和气力变化
  if(t % XXT == 0) {  // XX技能触发
    if((t / XXT) % 4 == Pos) { dj -= d1x[Hero]; dq += q2[Hero]; }  // 当前站位受伤害
    if((t / XXT) % 4 == 0) dj -= d2x[Hero];  // 全体伤害
  }
  if(t % SYT == 0) {  // SY技能触发
    if((t / SYT) % 4 == Pos) { dj -= d1s[Hero]; dq += q2[Hero]; }
    if((t / SYT) % 4 == 0) dj -= d2s[Hero];
  }
  
  Hash[t][h] = -INF;  // 初始化（防止重复访问死循环）
  int& ans = Hash[t][h];
  
  if(t == MaxT) {  // 最后一回合：只能造成最终伤害
    ans = 0;
    if (t % HeroT != 0) return 0;  // 本轮不是英雄行动回合
    
    // 武艺攻击
    if(j > wad[Hero]) ans = max(ans, wad[Hero]);
    // 法术攻击（如果有足够气力）
    if(q >= ssq[Hero]) {
      int dj2 = (ssp[Hero] == 1 ? -ssd[Hero] : 0);  // 法术消耗精力
      if(j + dj2 > 0) ans = max(ans, ssd[Hero]);
    }
  } else {  // 非最后一回合
    if (t % HeroT != 0)  // 不是英雄行动回合，只有boss的效果和自动回气
      return ans = dfs(t+1, j+dj, q+dq, s);
    
    // 选项1：自动回气（蓄力）
    ans = max(ans, dfs(t+1, j+dj, q+dq+q1[Hero], s));
    
    // 选项2：武艺攻击
    ans = max(ans, dfs(t+1, j+dj-wad[Hero], q+dq+q1[Hero], s) + wad[Hero]);
    
    // 选项3：玉润（消耗神恢复精力）
    if(s >= yurun_shen && j < maxjing[Hero])
      ans = max(ans, dfs(t+1, min(j+yurun_jing, maxjing[Hero])+dj, q+dq, s-yurun_shen));
    
    // 选项4：疏尔过（恢复神）
    if(s < maxshen[Hero])
      ans = max(ans, dfs(t+1, j+dj, q+dq, s+shuerguo_shen));
    
    // 选项5：法术攻击
    if(q >= ssq[Hero]) {
      int dj2 = (ssp[Hero] == 1 ? -ssd[Hero] : 0);
      ans = max(ans, dfs(t+1, j+dj+dj2, q+dq-ssq[Hero], s) + ssd[Hero]);
    }
  }
  return ans;
}

int d[4][4];       // d[hero][pos] = 该英雄在该站位能造成的最大伤害
vector<string> ans; // 可行的英雄排列方案

// 搜索给定最大回合数maxt下的最优方案
int solve(int maxt) {
  // 枚举所有英雄在各站位的表现
  for(int h = 0; h < 4; h++)
    for(int p = 1; p <= 3; p++) {
      MaxT = maxt; Hero = h; Pos = p;
      HeroT = 5 - su[h];  // 英雄行动间隔 = 5-速度
      for(int t = 1; t <= maxt; t++) Hash[t].clear();  // 清空记忆化表
      d[h][p] = dfs(1, jing[h], qi[h], shen[h]);  // 从回合1开始
    }
  
  ans.clear();
  // 枚举三位英雄的排列（4选3排列 = 4×3×2 = 24种）
  for(int h1 = 0; h1 < 4; h1++)
    for(int h2 = 0; h2 < 4; h2++) if(h2 != h1)
      for(int h3 = 0; h3 < 4; h3++) if(h3 != h1 && h3 != h2)
        if(d[h1][1] + d[h2][2] + d[h3][3] >= SY_jing)  // 总伤害达到boss血量
          ans.push_back(name[h1] + name[h2] + name[h3]);
  
  sort(ans.begin(), ans.end());
  return ans.size();
}

int main() {
  int caseno = 0;
  while(cin >> SY_jing && SY_jing) {
    cin >> XX_su >> SY_su >> yurun_jing >> yurun_shen >> shuerguo_shen;
    
    // 读入4位英雄的属性
    for(int i = 0; i < 4; i++)
      cin >> maxjing[i] >> maxshen[i] >> su[i]
          >> d1x[i] >> d2x[i] >> d1s[i] >> d2s[i]
          >> wad[i] >> ssd[i] >> ssq[i] >> ssp[i]
          >> q1[i] >> q2[i] >> jing[i] >> qi[i] >> shen[i];
    
    XXT = 5 - XX_su;  // boss的XX技能间隔
    SYT = 5 - SY_su;  // boss的SY技能间隔
    
    cout << "Case " << ++caseno << ": ";
    
    // 尝试1~12回合，取最早可行的方案
    for(int i = 1; i <= MAXTIME; i++)
      if(solve(i)) {
        cout << i;
        for(int j = 0; j < ans.size(); j++) cout << " " << ans[j];
        break;
      }
    
    if(ans.size() == 0) cout << -1;  // 无法击败boss
    cout << endl << endl;
  }
  return 0;
}
// 25878492	12233	Final Combat	Accepted	C++	0.130	2020-12-23 09:26:25
```

## UVa10966 3KP-Bash Project

### 题目描述
实现一个简化的Bash shell模拟器，支持以下命令：
- **cd** `<path>`：切换当前工作目录
- **touch** `<path>` [-h] [-n size]：创建/修改文件
- **mkdir** `<path>` [-h]：创建目录
- **find** `<path>` [-r] [-h]：查找文件/目录
- **ls** [path] [-r] [-h] [-s] [-S] [-f] [-d]：列出目录内容
- **pwd**：打印当前工作目录
- **exit**：退出当前会话
- **grep** `"pattern"`：通过管道过滤前一个命令的输出

支持管道操作 `|`，管道右侧只能是grep命令。

文件系统特性：
- 支持绝对路径（以/开头）和相对路径
- 支持`.`（当前目录）和`..`（父目录）
- 文件名限制：仅含字母、数字和`.`，长度≤255，不能以`..`开头
- hidden属性：`-h`开关标记的文件在默认列表时不显示
- 支持递归搜索（`-r`）

### 解题思路
这是一个**模拟系统实现**的典型题目，关键是合理的代码设计：
1. **数据结构设计**：用`vector<File>`存储文件系统，每个File有parent指针、子目录列表等
2. **模块化函数**：每个功能抽象为独立函数
   - `getDirNode(path)`：路径解析，返回目录节点
   - `splitFileName(fullpath, filename)`：分离路径和文件名
   - `findFileEx()`：递归/非递归文件搜索
   - `formatFiles()`：格式化输出
   - `parseArgs()`：解析命令行参数和开关
3. **管道实现**：先运行第一个命令得到输出文本，然后对后续grep逐行过滤
4. **统一的错误处理**：每种错误有明确的错误消息常量

### 算法方法
**模拟器设计模式**：
1. 清晰的数据模型：`struct File`包含所有文件属性
2. 统一的命令行解析框架：`runCommand` + `parseArgs`
3. 管道链式处理：`runCommandLine`拆分管道符 → 逐段执行
4. 编解码路径：`getAbsolutePath` / `split` / `trim`
5. 错误信息集中管理：常量字符串

代码设计亮点：
- 子函数仅处理自己的任务，依赖关系清晰
- 错误处理一致，不会漏报
- 使用sstream进行格式化和解析
- multimap实现(实际上用的是map)路径和状态

### 复杂度分析
- **时间复杂度**：每条命令O(n×depth)，n为文件系统节点数，depth为递归深度
- **空间复杂度**：O(n)，n为文件系统中文件/目录总数

```cpp
// UVa10966 3KP-Bash Project
// Rujia Liu
// 题目：3KP-Bash模拟器 - 实现简化Shell，支持文件操作和管道grep
#include<iostream>
#include<string>
#include<vector>
#include<algorithm>
#include<sstream>
#include<cstring>
using namespace std;

typedef unsigned long long LL;
typedef vector<int> VI;
typedef vector<string> VS;

// 错误消息常量（集中管理，便于修改和静态查错）
const string ERROR_BAD_USAGE = "bad usage\n";
const string ERROR_NO_COMMAND = "no such command\n";
const string ERROR_DIR_NOT_FOUND = "path not found\n";
const string ERROR_DIR_FOUND = "a directory with the same name exists\n";
const string ERROR_DIR_OR_FILE_FOUND = "file or directory with the same name exists\n";
const string ERROR_FILE_NOT_FOUND = "file not found\n";
const string ERROR_EMPTY = "[empty]\n";

// 字符串分割函数：按分隔符delim分割字符串s
VS split(string s, char delim=' ') {
  if(delim != ' ')
    for(int i = 0; i < s.length(); i++) if(s[i] == delim) s[i] = ' ';
  stringstream ss(s);
  VS ret;
  string x;
  while(ss >> x) ret.push_back(x);
  return ret;
}

// 安全地将字符串转为整数
int get_int(string s, LL& v) {
  stringstream ss(s);
  if(ss >> v) return 1;
  return 0;
}

// 去除字符串首尾空白符
string trim(string s) {
  int L, R;
  for(L = 0; L < s.length(); L++) if(!isspace(s[L])) break;
  for(R = s.length()-1; R > L; R--) if(!isspace(s[R])) break;
  return s.substr(L, R-L+1);
}

// 文件/目录节点的数据结构
struct File {
  int parent;          // 父目录编号（0为根目录的parent=0）
  string name;         // 文件名
  string fullpath;     // 缓存：完整路径（用于排序和输出）
  LL size;             // 文件大小
  bool dir;            // 是否为目录
  bool hidden;         // 是否隐藏
  vector<int> subdir;  // 子文件/子目录列表
  
  File(int parent=0, string name="", LL size=0, bool dir=true, bool hidden=false)
    :parent(parent), name(name), size(size), dir(dir), hidden(hidden) {}
};

vector<File> fs;  // 文件系统（索引0为根目录）
int curDir;       // 当前工作目录节点编号

// 比较函数：按完整路径字典序排序
bool comp(const int& x, const int& y) {
  return fs[x].fullpath < fs[y].fullpath;
}

// 比较函数：按文件大小升序
bool comps(const int& x, const int& y) {
  return fs[x].size < fs[y].size || (fs[x].size == fs[y].size && fs[x].fullpath < fs[y].fullpath);
}

// 比较函数：按文件大小降序
bool compS(const int& x, const int& y) {
  return fs[x].size > fs[y].size || (fs[x].size == fs[y].size && fs[x].fullpath < fs[y].fullpath);
}

// 在目录node中查找名为name的文件/目录，返回节点编号或-1
int findFileInDirectory(int node, string name) {
  VI& subdir = fs[node].subdir;
  for(int i = 0; i < subdir.size(); i++)
    if(fs[subdir[i]].name == name) return subdir[i];
  return -1;
}

// 拼接路径和文件名
string joinPath(string path, string name) {
  if(path[path.size()-1] != '/') path += "/";
  return path + name;
}

// 获取节点node的绝对路径（递归，利用缓存的fullpath）
string getAbsolutePath(int node) {
  if(!node) return "/";
  return joinPath(getAbsolutePath(fs[node].parent), fs[node].name);
}

// 在目录node中创建文件（普通或目录）
int createFileInDirectory(int node, string name, LL size, bool dir, bool hidden) {
  fs.push_back(File(node, name, size, dir, hidden));
  int x = fs.size()-1;  
  fs[x].fullpath = joinPath(getAbsolutePath(node), name);  // 缓存完整路径
  fs[node].subdir.push_back(x);
  return x;
}

// 路径解析：将path解析为目录节点编号。支持绝对路径和相对路径
// 返回值：目录节点编号，-1表示路径不存在
int getDirNode(string path) {
  if(!path.length()) return curDir;          // 空路径→当前目录
  int node = curDir;  // 默认从当前目录开始（相对路径）
  if(path[0] == '/') node = 0;               // 绝对路径从根开始
  
  VS dirs = split(path, '/');
  for(int i = 0; i < dirs.size(); i++) {
    if(dirs[i] == ".") continue;             // 忽略"."
    else if(dirs[i] == "..") {
      if(!node) return -1;                   // 根目录没有父目录
      node = fs[node].parent;                // 上跳到父目录
    } else {
      int x = findFileInDirectory(node, dirs[i]);
      if(x == -1 || !fs[x].dir) return -1;   // 不存在或不是目录
      node = x;
    }
  }
  return node;
}

// 检查文件名是否合法
// 合法条件：长度1~255，只含字母数字和'.'，不能是"."或含".."
int isValidFileName(string name) {
  if(name.length() == 0 || name.length() > 255) return 0;
  if(name == "." || name.find("..") != string::npos) return 0;
  for(int i = 0; i < name.length(); i++)
    if(!isdigit(name[i]) && !isalpha(name[i]) && name[i] != '.') return 0;
  return 1;
}

// 将fullpath分离为目录部分和文件名部分
// 返回值：目录节点编号，-1表示路径不对
// filename：输出参数，分离出的文件名
int splitFileName(string fullpath, string& filename) {
  int n = fullpath.length();
  for(int i = fullpath.length()-1; i >= 0; i--) {
    if(fullpath[i] == '/') {  // 找到最后一个'/'
      filename = fullpath.substr(i+1);  // 文件名部分
      string dir = fullpath.substr(0, i);  // 目录部分
      if(dir == "") return 0;  // 相对于根目录
      return getDirNode(dir);
    }
  }
  // 没有'/'，整个路径就是文件名（相对于当前目录）
  filename = fullpath;
  return curDir;
}

// 初始化新的Bash会话：清空文件系统，创建根目录
void newSession() {
  fs.clear();
  fs.push_back(File());
  curDir = 0;
}

// 递归文件搜索：在node中搜索匹配filename的文件
// recur=true: 递归搜索子目录
// hidden=true: 包含隐藏文件
// f=true: 包含普通文件; d=true: 包含目录
void findFileEx(VI& out, int node, string filename, bool recur, bool hidden,
                bool f=true, bool d=true) {
  VI& subdir = fs[node].subdir;
  for(int i = 0; i < subdir.size(); i++) {
    int x = subdir[i];
    // 递归搜索子目录
    if(fs[x].dir && recur) findFileEx(out, x, filename, recur, hidden, f, d);
    // 跳过不显示隐藏文件的情况
    if(fs[x].hidden && !hidden) continue;
    // 匹配文件名或列出全部
    if(filename == "" || fs[x].name == filename) {
      if((fs[x].dir && d) || (!fs[x].dir && f)) out.push_back(x);
    }
  }
}

// 格式化文件列表输出
string formatFiles(const VI& out) {
  stringstream ss;
  for(int i = 0; i < out.size(); i++) {
    ss << fs[out[i]].fullpath << " " << fs[out[i]].size;
    if(fs[out[i]].hidden) ss << " " << "hidden";
    if(fs[out[i]].dir) ss << " " << "dir";
    ss << "\n";
  }
  return ss.str();
}

// 解析命令行参数：将开关（-x）和值（-n）分离出来
// params：参数字符串数组
// args：输出，不含'-'的正规参数列表
// sw[]：输出，开关标记数组（ASCII码索引）
// v：输出，-n参数的值
bool parseArgs(VS params, VS& args, bool* sw, LL &v) {
  LL v2;
  for(int i = 0; i < params.size(); i++)
    if(params[i][0] == '-') {  // 开关参数
      if(isalpha(params[i][1])) sw[params[i][1]] = 1;  // 字母开关
      else if(get_int(params[i].substr(1), v2)) v = v2;  // 数字开关（-n）
      else return false;  // 非法开关
    }
    else args.push_back(params[i]);  // 正规参数
  return true;
}

// 运行单个命令（不含管道），返回标准输出或错误消息
string runCommand(const VS& cmd) {
  VS params(cmd.begin()+1, cmd.end()), args;  // cmd[0]=命令名
  bool sw[256];       // 开关标记：sw['r'], sw['h'], sw['s']等
  LL v = 0;           // -n参数值
  memset(sw, 0, sizeof(sw));
  
  if(!parseArgs(params, args, sw, v)) return ERROR_BAD_USAGE;
  
  int node;
  string filename;
  
  if(cmd[0] == "cd") {  // 切换目录
    if(args.size() != 1) return ERROR_BAD_USAGE;
    if((node = getDirNode(args[0])) == -1) return ERROR_DIR_NOT_FOUND;
    curDir = node;
    return "";
  }
  
  if(cmd[0] == "touch") {  // 创建/修改文件
    if(args.size() != 1) return ERROR_BAD_USAGE;
    if((node = splitFileName(args[0], filename)) == -1) return ERROR_DIR_NOT_FOUND;
    if(!isValidFileName(filename)) return ERROR_BAD_USAGE;

    int x = findFileInDirectory(node, filename);
    if(x != -1 && fs[x].dir) return ERROR_DIR_FOUND;  // 同名目录已存在
    if(x == -1) createFileInDirectory(node, filename, v, false, sw['h']);
    else { fs[x].size = v; fs[x].hidden = sw['h']; }  // 更新已有文件
    return "";
  }
  
  if(cmd[0] == "mkdir") {  // 创建目录
    if(args.size() != 1) return ERROR_BAD_USAGE;
    if((node = splitFileName(args[0], filename)) == -1) return ERROR_DIR_NOT_FOUND;
    if(!isValidFileName(filename)) return ERROR_BAD_USAGE;

    int x = findFileInDirectory(node, filename);
    if(x != -1) return ERROR_DIR_OR_FILE_FOUND;  // 同名已在
    createFileInDirectory(node, filename, 0, true, sw['h']);
    return "";
  }
  
  if(cmd[0] == "find") {  // 搜索文件
    if(args.size() != 1) return ERROR_BAD_USAGE;
    if((node = splitFileName(args[0], filename)) == -1) return ERROR_DIR_NOT_FOUND;
    
    VI out;
    findFileEx(out, node, filename, sw['r'], sw['h']);
    if(out.size() == 0) return ERROR_FILE_NOT_FOUND;
    sort(out.begin(), out.end(), comp);
    return formatFiles(out);
  }
  
  if(cmd[0] == "ls") {  // 列出目录内容
    if(args.size() > 1) return ERROR_BAD_USAGE;
    node = curDir;
    if(args.size() == 1)
      if((node = getDirNode(args[0])) == -1) return ERROR_DIR_NOT_FOUND;
    
    VI out;
    findFileEx(out, node, "", sw['r'], sw['h'], !sw['d'], !sw['f']);
    if(out.size() == 0) return ERROR_EMPTY;
    
    // 按指定方式排序
    if(sw['s']) sort(out.begin(), out.end(), comps);        // 按大小升序
    else if(sw['S']) sort(out.begin(), out.end(), compS);   // 按大小降序
    else sort(out.begin(), out.end(), comp);                // 按路径字典序
    
    return formatFiles(out);
  }
  
  if(cmd[0] == "pwd") {  // 打印工作目录
    if(args.size() != 0) return ERROR_BAD_USAGE;
    return getAbsolutePath(curDir) + "\n";
  }
  
  if(cmd[0] == "exit") {  // 退出会话
    if(args.size() != 0) return ERROR_BAD_USAGE;
    newSession();
    return "";
  }
  
  if(cmd[0] == "grep") return ERROR_BAD_USAGE;  // grep必须在管道右侧
  return ERROR_NO_COMMAND;  // 未知命令
}

// 运行整个命令行（支持管道 |）
string runCommandLine(string cmd) {
  // 按管道符'|'拆分命令（考虑引号内的'|'不算）
  int n = cmd.length();
  int start = 0, inq = 0;
  VS commands;
  for(int i = 0; i <= n; i++)
    if(i == n || (cmd[i] == '|' && !inq)) {
      commands.push_back(cmd.substr(start, i-start));
      start = i+1;
    }
    else if(cmd[i] == '"') inq = !inq;  // 切换引号状态
  
  if(!commands.size()) return "";

  // 运行第一个命令
  string lastoutput = runCommand(split(commands[0]));
  string line, s, ret;
  
  // 链式处理后续grep命令
  for(int i = 1; i < commands.size(); i++) {
    stringstream ss(commands[i]);
    if(!(ss >> s) || s != "grep") return ERROR_BAD_USAGE;
    getline(ss, s);
    s = trim(s);
    // 提取grep的搜索模式
    if(s.length() < 2 || s[0] != '"' || s[s.length()-1] != '"')
      return ERROR_BAD_USAGE;
    s = s.substr(1, s.length()-2);  // 去掉引号
    
    // 逐行过滤前一个命令的输出
    stringstream input(lastoutput);
    ret = "";
    while(getline(input, line)) {
      if(line.find(s) != string::npos) ret += line + "\n";
    }
    lastoutput = ret;
  }
  return lastoutput;
}

int main() {
  string cmd;
  newSession();
  while(getline(cin, cmd)) {
    cout << runCommandLine(cmd);
  }
  return 0;
}
// 25878498	10966	3KP-BASH Project	Accepted	C++	0.120	2020-12-23 09:27:17
```
