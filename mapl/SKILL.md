# mapl — 知识学习思维导图

> 为某个编程主题生成包含 Know（知识讲解）+ Code（代码示例）的学习思维导图。
> 触发方式：`/mapl {主题}`（如 `/mapl NumPy`）

---

## 工作流

```
┌─────────────────────────────────┐
│  Step 0  生成框架（1 次）        │   ← L1-L3
└────────────┬────────────────────┘
             ▼
┌─────────────────────────────────┐
│  Step 1  填充 Know（第 N 章）    │   ← Know 分支
│  Step 2  填充 Code（第 N 章）    │   ← Code 分支
│         ↻ 对每一章循环           │
└─────────────────────────────────┘
```

### 快捷指令约定

- 当我发送 **`1`** 时，表示 **「执行下一步」**。
- 你需要自动判断当前处于流程中的哪一步，然后执行对应的下一步操作。
- 如果我在某次 `1` 之后进行了调试 / 修改等若干轮对话，
  再次发送 `1` 时，仍然表示 **「继续流程中的下一步」**，而非重新开始。
- 具体推进逻辑：
  1. 第一次 `1` → 执行 Step 0，生成框架
  2. 之后每次 `1` → 按章节顺序交替执行 Step 1（Know）→ Step 2（Code）→ 下一章 Step 1 → Step 2 → …
  3. 所有章节都完成后，提示「全部章节已生成完毕」

---

## Step 0 ｜生成框架（L1 → L3）

请生成一份 **{主题}** 常用语法思维导图的框架，格式为 markmap 兼容的 Markdown。
本步只生成 L1（标题）、L2（章节）、L3（固定两个分支）三层，不生成更深的内容。

### 文件头（原样输出）

```
---
markmap:
  initialExpandLevel: 99
  maxWidth: 320
  colorFreezeLevel: 2
---

<style>
code {
  color: #D4D4D4 !important;
  background-color: #1E1E1E !important;
  border: 1px solid #2D2D2D;
  border-radius: 4px;
  padding: 0 4px;
  font-family: Consolas, "Courier New", monospace;
}
</style>
```

### 总体层级树（仅供参考，本步只生成 L1–L3）

```
L1  # 标题
└─ L2  ## 章（如 "1. 数组创建"）
   ├─ L3-A  Know（文字性知识讲解）
   │   ├─ 概念 / 规则 / 要点
   │   ├─ 涉及的函数名罗列
   │   └─ 可继续延伸若干层
   └─ L3-B  Code（代码示例）
       └─ L4  大分支
           └─ L5  小分支
               └─ L6  代表性代码示例（每个小分支 1 个）
                   ├─ L7① 输出结果（按需）
                   ├─ L7② 代码变体
                   ├─ L7③ 代码变体 …
                   ├─ L7④ 🚫 易错点代码（至少 2 个）
                   └─ L7⑤ 🚫 易错点代码
                       └─ L8  输出结果 / 注释（可选）
```

### 生成规则

【L1】顶级标题：

```
# {主题} 常用语法思维导图
```

【L2】每个章节用 `##` + span：

```
## <span style="color:#1971c2">🧱 N. 章标题</span>
```

【L3】每章恰好 2 个子分支，名称固定，不可改动：

```
- <span style="color:#2b8a3e">📖 Know</span>
- <span style="color:#569CD6">💻 Code</span>
```

L3 下不写任何内容，留空等待后续步骤填充。

### 任务

1. 根据 {主题} 的知识体系，规划出完整的章节列表（L2），数量由内容决定
2. 章节顺序从基础到进阶，覆盖 {主题} 的核心使用场景
3. 每章只输出章标题 + Know / Code 两个空分支

---

## Step 1 ｜填充 Know 分支

展开当前章 `<span style="color:#2b8a3e">📖 Know</span>` 下的所有子层级。

### Know 分支结构

```
- <span style="color:#2b8a3e">📖 Know</span>
  - <span style="color:#2b8a3e">🛠️ 知识分组标题 A</span>
    - 概念描述（纯文本）
    - `函数名(参数)` / `方法名()`（行内 code 标记）
    - 可继续嵌套子层，按需延伸
  - <span style="color:#2b8a3e">🛠️ 知识分组标题 B</span>
    - ……
```

### 内容要求

- 先分析本章知识体系包含哪些独立的知识点或概念域，每个独立部分对应一个 🛠️ 分组，数量不做硬性限制
- 每个分组内列出：
  - 核心概念 / 规则（简洁文字，每条 1 行）
  - 涉及的函数、方法、属性名（用 `code` 行内标记）
  - 重要参数说明（如 `axis=None`、`keepdims=False`）
  - 如有易混淆概念，单独列出对比说明
- 层级不设上限，但每层内容精炼不冗余
- 覆盖核心用法即可，不列罕见用法
- 与前面章节重复的知识点不再展开，标注"详见第 1️⃣2️⃣3️⃣… 章"

### 格式规则

- 🛠️ 行格式固定：`<span style="color:#2b8a3e">🛠️ 标题</span>`
- 纯文字描述不加任何 HTML span
- 不要在 Know 中放代码示例（代码全部在 Code 分支）

### 代码相关文字高亮（VS Code Dark+ 配色）

Know 分支中出现的函数名、方法名、参数名、类/类型名、关键字、字符串值等
**代码相关文字**，不要只用 markdown 反引号，需用 `<span>` 内联上色，
配色遵循 VS Code Dark+ 主题：

| 类型        | 色值      | 示例写法 |
|------------|-----------|----------|
| 关键字      | `#569CD6` | `<span style="color:#569CD6">import</span>` |
| 函数/方法名  | `#DCDCAA` | `<span style="color:#DCDCAA">array()</span>` |
| 变量/参数名  | `#9CDCFE` | `<span style="color:#9CDCFE">axis</span>` |
| 类/类型     | `#4EC9B0` | `<span style="color:#4EC9B0">ndarray</span>` |
| 字符串      | `#CE9178` | `<span style="color:#CE9178">'float32'</span>` |
| 数字        | `#B5CEA8` | `<span style="color:#B5CEA8">0</span>` |
| 注释        | `#6A9955` | `<span style="color:#6A9955"># 说明</span>` |
| 运算符/标点  | `#D4D4D4` | `<span style="color:#D4D4D4">=</span>`（Know 内联需上色） |

**具体规则：**

1. 函数/方法名行：整行用上色 span 包裹各 token，不再使用反引号
   - 例：`<span style="color:#DCDCAA">np.zeros</span>(<span style="color:#9CDCFE">shape</span>, <span style="color:#9CDCFE">dtype</span><span style="color:#D4D4D4">=</span><span style="color:#CE9178">'float64'</span>)`
2. 参数说明行：参数名上色，等号与默认值也按类型着色
   - 例：`<span style="color:#9CDCFE">axis</span><span style="color:#D4D4D4">=</span><span style="color:#569CD6">None</span>` 表示沿所有轴操作
3. 纯概念描述行（不涉及任何代码 token）保持纯文本，不加 span
4. 同一行中可以混排纯文本和上色 span
   - 例：返回值类型为 `<span style="color:#4EC9B0">ndarray</span>`

---

## Step 2 ｜填充 Code 分支

展开当前章 `<span style="color:#569CD6">💻 Code</span>` 下 L4 → L8 全部层级。

### Code 分支层级结构

```
- <span style="color:#569CD6">💻 Code</span>
  - L4  大分支（按本章知识内容划分为几个方面，每个方面一个大分支）
    - L5  小分支（每个方面再按具体代码类型细分，每种一个小分支）
      - L6  代表性代码示例（每个小分支仅 1 个）
        - L7① 代表性代码的输出结果（按需，不是必须）
        - L7② 代码变体（覆盖该场景的其他常见写法）
        - L7③ 代码变体 …
        - L7④ 🚫 易错点代码
        - L7⑤ 🚫 易错点代码
          - L8  输出结果 / 注释（可选，用于解释 L7 的行为）
```

### 数量规则

- **L4**：先分析本章知识涵盖哪几个方面，每个方面对应一个大分支，数量由内容决定
- **L5**：每个大分支下，分析该方面有哪几种代码类型或使用场景，每种对应一个小分支，数量由内容决定
- **L6**：每个小分支下恰好 1 个代表性代码
- **L7**：变体尽量覆盖常见写法；🚫 易错至少 2 个
- **L8**：按需决定有无
- 覆盖核心用法即可，不列罕见用法
- 与前面章节重复的代码场景不再展开，标注"详见第 1️⃣2️⃣3️⃣… 章"

### 各层 Markdown 写法

**【L4 大分支】**

```
  - <span style="color:#0ca678">📦 大分支名</span>
```

图标可选：📦 📋 🔢 🔄 🧷 🧱 🔧，同一章内不重复

**【L5 小分支】**

```
    - <span style="color:#099268">🧩 小分支名</span>
```

**【L6 代表性代码 ▸】**

```
      - <span style="color:#569CD6">▸</span> <span style="font-family:Consolas, 'Courier New', monospace; background:#1E1E1E; border:1px solid #2D2D2D; border-radius:4px; padding:0 4px;">&nbsp;&nbsp;代码</span>
```

**【L7 输出 ↳】**

```
        - <span style="color:#364fc7">↳</span> <span style="font-family:Consolas, 'Courier New', monospace; background:#1E1E1E; border:1px solid #2D2D2D; border-radius:4px; padding:0 4px;">结果</span>
```

**【L7 变体 ▸】** 与 L7① 同层

```
        - <span style="color:#569CD6">▸</span> <span style="font-family:Consolas, 'Courier New', monospace; background:#1E1E1E; border:1px solid #2D2D2D; border-radius:4px; padding:0 4px;">&nbsp;&nbsp;变体代码</span>
```

**【L7 易错 🚫 ▸】** 与 L7① 同层

```
        - <span style="color:#d6336c">🚫</span> <span style="color:#569CD6">▸</span> <span style="font-family:Consolas, 'Courier New', monospace; background:#1E1E1E; border:1px solid #2D2D2D; border-radius:4px; padding:0 4px;">易错代码</span>
```

**【L8 输出/注释 ↳（可选）】** L7 的子层

```
          - <span style="color:#364fc7">↳</span> <span style="font-family:Consolas, 'Courier New', monospace; background:#1E1E1E; border:1px solid #2D2D2D; border-radius:4px; padding:0 4px;">结果或注释</span>
```

### 缩进规则

- `▸` 行代码框内首字符前有 `&nbsp;&nbsp;`（2 个不换行空格）
- `🚫 ▸` 行代码框内无额外 `&nbsp;&nbsp;`
- `↳` 行代码框内无额外前导空格

### 代码内语法高亮（VS Code Dark+）

代码框内每个 token 用 `<span style="color:XXX">` 包裹：

| 类型        | 色值      |
|------------|-----------|
| 关键字      | `#569CD6` |
| 函数/方法名  | `#DCDCAA` |
| 变量/参数名  | `#9CDCFE` |
| 类/类型     | `#4EC9B0` |
| 字符串      | `#CE9178` |
| 数字        | `#B5CEA8` |
| 注释        | `#6A9955` |
| 运算符/标点  | 不着色（Code 代码框内背景深色，无需上色） |

### 多行代码换行

一个 `▸` 行多条语句时，用 `<br>&nbsp;&nbsp;&nbsp;&nbsp;` 换行（不用分号拼接）。

### 注释三色

| 用途              | 色值      |
|------------------|-----------|
| 默认注释          | `#6A9955` |
| 要点 / 陷阱提醒   | `#ff922b` |
| 概念名 / 函数名   | `#74c0fc` |
