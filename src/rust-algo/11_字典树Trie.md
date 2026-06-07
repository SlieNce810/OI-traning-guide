# 11 - 字典树 (Trie)

> 专门处理字符串前缀匹配的树形结构。你已经在 5/28 的题目中用过了！

## 一、基础知识

### 1.1 核心定义

**字典树**（Trie，也称前缀树）是一种多叉树，每个节点代表一个字符，从根到某节点的路径构成一个字符串的前缀。根节点为空，叶节点或带标记的节点表示一个完整单词的结束。

它天然支持前缀匹配——查找"以某个前缀开头"的所有字符串只需走到前缀对应的节点，然后遍历其子树。

### 1.2 工作原理

Trie 的每个节点通常包含：
- 一个长度为 26（或 256）的子节点数组/哈希表
- 一个布尔标记表示"是否有单词在此结束"
- （可选）一个计数值表示以该前缀开头的单词个数

操作：
- **插入**：逐字符向下走，若节点不存在则创建
- **查找**：逐字符向下走，若中途缺失则不存在
- **前缀查询**：走到前缀末尾节点，检查子树

所有操作的时间复杂度为 O(L)，L 为字符串长度，与存入的单词总数无关。

### 1.3 适用场景与前提

| 场景 | 说明 |
|------|------|
| 自动补全/搜索建议 | 根据前缀列出所有可能单词 |
| 拼写检查 | 快速判断单词是否存在 |
| 字典序排序 | Trie 的 DFS 按字母序输出 |
| 求两字符串的最长公共前缀 | 走到分叉处即可 |
| IP 路由最长前缀匹配 | 路由表存储的方式 |

**前提**：字符集可控（如仅小写字母 / 数字）。若字符集过大（如 Unicode），子节点数组会占用大量内存，应改用 HashMap 存储子节点。

### 1.4 优缺分析

**优点：**
- 前缀查询 O(L)，与数据量无关
- 公共前缀只存储一次，节省空间（比存储所有完整字符串更省）
- 天然支持字典序遍历

**缺点：**
- 最坏空间 O(总字符数 × 字母表大小），浅而宽的 Trie 非常耗内存
- 单字符查找比哈希表慢（需要多次指针跳转）
- 删除操作复杂（需要清理不再使用的节点链）

## 二、算法本质

**大白话：字典树就像一本真正的字典——按字母顺序排列，公共前缀共享同一条路径。**

存储 "apple", "app", "apply" 的字典树：

```
        root
         |
         a
         |
         p
         |
         p (标记: "app" 结束)
         |
         l      ← "apple" 和 "apply" 共享前缀 "appl"
        / \
       e   y
  (apple)  (apply)
```

**注意：** "apple" 和 "apply" 共享 "appl" 四个字符的路径，直到最后一个字符才分叉。这就是 Trie 的核心——公共前缀只存一次。

**核心优势：**
- 查找一个长度为 m 的字符串只需要 O(m)，与存了多少个字符串无关
- 天然支持前缀查询

## 三、Trie 的实现

### 基于数组的实现（推荐，更快）

```rust
struct Trie {
    children: [Option<Box<Trie>>; 26],
    is_end: bool,
}

impl Trie {
    fn new() -> Self {
        Trie {
            children: Default::default(), // 26 个 None
            is_end: false,
        }
    }

    /// 插入一个单词
    fn insert(&mut self, word: &str) {
        let mut node = self;
        for &b in word.as_bytes() {
            let idx = (b - b'a') as usize;
            node = node.children[idx].get_or_insert_with(|| Box::new(Trie::new()));
        }
        node.is_end = true;
    }

    /// 查找单词是否存在
    fn search(&self, word: &str) -> bool {
        match self.find_node(word) {
            Some(node) => node.is_end,
            None => false,
        }
    }

    /// 查找是否有以 prefix 开头的单词
    fn starts_with(&self, prefix: &str) -> bool {
        self.find_node(prefix).is_some()
    }

    /// 辅助：找到 prefix 对应的节点
    fn find_node(&self, prefix: &str) -> Option<&Trie> {
        let mut node = self;
        for &b in prefix.as_bytes() {
            let idx = (b - b'a') as usize;
            match &node.children[idx] {
                Some(child) => node = child,
                None => return None,
            }
        }
        Some(node)
    }
}
```

### 使用示例

```rust
let mut trie = Trie::new();
trie.insert("apple");
trie.insert("app");
trie.insert("application");

trie.search("apple");      // true
trie.search("app");        // true
trie.search("ap");         // false（不是完整单词）
trie.starts_with("ap");    // true（是某个单词的前缀）
trie.starts_with("b");     // false
```

## 四、Trie 的操作复杂度

| 操作 | 时间复杂度 | 说明 |
|------|----------|------|
| 插入 | O(m) | m 是单词长度 |
| 查找 | O(m) | m 是单词长度 |
| 前缀查询 | O(m) | m 是前缀长度 |
| 空间 | O(Σ × m × n) | Σ=字符集大小，n=单词数 |

## 五、变体：01-Trie（处理数字的异或问题）

**用二进制位建 Trie，常用于求最大异或值。**

```rust
struct BitTrie {
    children: [Option<Box<BitTrie>>; 2], // 只有 0 和 1
}

impl BitTrie {
    fn new() -> Self {
        BitTrie { children: [None, None] }
    }

    fn insert(&mut self, num: i32) {
        let mut node = self;
        for i in (0..31).rev() { // 从高位到低位 (31 bits: 值范围 0 到 2^31-1)
            let bit = ((num >> i) & 1) as usize;
            node = node.children[bit].get_or_insert_with(|| Box::new(BitTrie::new()));
        }
    }

    /// 查找与 num 异或结果最大的值
    fn max_xor(&self, num: i32) -> i32 {
        let mut node = self;
        let mut result = 0;
        for i in (0..31).rev() { // 必须覆盖全部 31 位
            let bit = ((num >> i) & 1) as usize;
            let want = 1 - bit; // 想要相反的位（异或为1更大）
            if node.children[want].is_some() {
                result |= 1 << i;
                node = node.children[want].as_ref().unwrap();
            } else {
                node = node.children[bit].as_ref().unwrap();
            }
        }
        result
    }
}
```

## 六、你做过的题目回顾

### LC 3093 最长公共后缀查询（5/28）

你用了**反向字典树**（把字符串倒过来插入 Trie），这样后缀查询变成了前缀查询。这是一个很聪明的技巧！

## 七、经典例题

### 例题 1：实现 Trie（LeetCode 208）

就是上面的标准实现。

### 例题 2：单词搜索 II（LeetCode 212）

> 在二维字母网格中找出所有字典中的单词。

思路：把所有字典单词插入 Trie，然后在网格上 DFS，沿着 Trie 的路径搜索。

### 例题 3：数组中两个数的最大异或值（LeetCode 421）

```rust
fn find_maximum_xor(nums: Vec<i32>) -> i32 {
    let mut trie = BitTrie::new();
    for &num in &nums {
        trie.insert(num);
    }
    let mut ans = 0;
    for &num in &nums {
        ans = ans.max(trie.max_xor(num));
    }
    ans
}
```

## 八、测试题

1. **问：** Trie 和 HashMap 有什么区别？什么时候用 Trie 更好？

   **答：** HashMap 只能精确匹配，Trie 天然支持前缀查询。当需要"找所有以 XX 开头的单词"时，Trie 远优于 HashMap。

2. **问：** 反向 Trie 是什么？什么时候用？

   **答：** 把字符串倒过来插入 Trie。当需要处理"后缀"问题时，反转后变成前缀问题，就可以用 Trie 解决。

## 九、训练题

| 题目 | 难度 | 知识点 |
|------|------|--------|
| [LeetCode 208. 实现 Trie](https://leetcode.cn/problems/implement-trie-prefix-tree/) | 中等 | Trie 基础 |
| [LeetCode 211. 添加搜索单词](https://leetcode.cn/problems/design-add-and-search-words-data-structure/) | 中等 | Trie + DFS |
| [LeetCode 212. 单词搜索 II](https://leetcode.cn/problems/word-search-ii/) | 困难 | Trie + 回溯 |
| [LeetCode 421. 数组最大异或值](https://leetcode.cn/problems/maximum-xor-of-two-numbers-in-an-array/) | 中等 | 01-Trie |
| [LeetCode 14. 最长公共前缀](https://leetcode.cn/problems/longest-common-prefix/) | 简单 | Trie/直接比较 |
| [LeetCode 720. 词典中最长的词](https://leetcode.cn/problems/longest-word-in-dictionary/) | 中等 | Trie + BFS |
