---
name: mapc
description: "mapc — 代码仓库思维导图。为代码仓库生成结构化 markmap 思维导图。默认对当前目录或用户指定目录生成骨架 + LLM 补描述；--evolution 模式额外生成早/中期骨架图对照演化。"
---

# mapc — 代码仓库思维导图

> 为代码仓库生成结构化思维导图（markmap 格式）。
> 触发方式：`/mapc`（当前目录）或 `/mapc 目标描述`（如 `/mapc parkour那个项目`）
> 特别模式：`/mapc --evolution`（额外生成早/中期骨架图，详见第 10 节）

---

## 工作流

1. **确定目标目录**：
   - 无参数 → 使用当前工作目录
   - 有参数 → 在用户文件系统中搜索匹配的目录，找到后确认
2. **生成骨架**：在目标目录下运行本 skill 自带的 `scripts/repo2mindmap.py`（纯 Python 标准库，无需 pip install）
   - 脚本位于本 SKILL.md 同级的 `scripts/` 目录下，请根据当前系统自动定位完整路径
3. 读取生成的 MINDMAP.md
4. 按下方规范，分 Session 补全所有节点的"作用 / 输入 / 输出"以及类描述、文件描述
5. 用户输入数字（如 `1`）推进到下一个 Session

---

## 规范

你是代码仓库文档整理助手。请为当前仓库改造 **MINDMAP.md**（markmap 格式）并严格遵循以下规范，不要遗漏。

> **前置条件**：仓库根目录已存在由 `repo2mindmap.py` 自动生成的骨架 MINDMAP.md，其中包含目录 / 文件 / 类 / 函数节点。你需要在此骨架上逐步补全"作用 / 输入 / 输出"以及类描述、文件描述。

---

### 1 ｜整体层级结构

```
仓库名（#）
├─ 图例行（文件 / 函数分类 / Token 配色）
├─ 顶层目录（##）
│   ├─ 子目录（📁）
│   │   ├─ 文件（📦 / 🚀 / 🧩 / 🧪 / 🛠️）
│   │   │   ├─ ★ 文件说明（作用：…）          ← 文件级
│   │   │   ├─ 🧱 类
│   │   │   │   ├─ ★ 类说明（作用：…）         ← 类级
│   │   │   │   ├─ 🔧 函数
│   │   │   │   │   ├─ ★ 作用：…              ← 函数级
│   │   │   │   │   │   ├─ 输入（徽章）
│   │   │   │   │   │   │   └─ in. 参数: 类型
│   │   │   │   │   │   └─ 输出（徽章）
│   │   │   │   │   │       └─ out. 返回值: 类型
│   │   │   │   ├─ 🔧 函数 …
│   │   │   ├─ 🧱 类 …
│   │   │   ├─ 🔧 模块级函数（不属于任何类）
│   │   │   │   └─ 作用 / 输入 / 输出 …
```

**关键规则**：
- "输入 / 输出"必须挂在"作用"下面（比"作用"深一层）。
- 多输入 / 多输出时，每个参数 / 返回值 **单独一行**，不可合并。
- 类描述放置规则：
  - 有方法的类 → 描述与 🔧 节点**并列**（同缩进层级）。
  - 无方法的类（纯配置）→ 描述作为**子节点**。
- 文件描述 = "文件自身功能 + 在整体代码库中的角色"。
- 对于"作用"，尽量抽象出来通俗易懂的解释

---

### 2 ｜markmap 前置配置

```yaml
---
markmap:
  initialExpandLevel: 99      # 全展开
  maxWidth: 260
  colorFreezeLevel: 2
---
```

紧跟 YAML 头之后，添加 `<style>` 块统一控制底层节点字号（避免每个 span 重复内联 font-size）：

```html
<style>
span[style*="background:#1d4ed8"],
span[style*="background:#c2410c"] { font-size:12px; }
span[style*="color:#1c7ed6"] { font-size:11px; font-weight:700; }
span[style*="color:#e8590c"] { font-size:11px; font-weight:700; }
span[style*="color:#9CDCFE"],
span[style*="color:#4EC9B0"],
span[style*="color:#C586C0"] { font-size:11px; }
</style>
```

---

### 3 ｜节点字体大小（从上到下递减）

| 层级 | font-size | font-weight | 说明 |
|---|---|---|---|
| 顶层目录标题（`##` + folder span） | 35 px | 700 | 仓库名同级 |
| 子目录节点（📁） | 32 px | 700 | |
| 文件节点（📦 / 🚀 / 🧩 / 🧪 / 🛠️） | 29 px | 600 | 带 `[link](path)` |
| 类节点（🧱） | 27 px | 700 | |
| 函数节点（🔧） | 25 px | 600 | |
| "作用："描述 | 13 px | 600 | 前缀色 `#495057`，正文色 `#ffffff` |
| 输入 / 输出徽章 | 12 px | 700 | 圆角 + 背景色 + 粗体 |
| `in.` / `out.` 及参数行 | 11 px | — | 见 Token 配色 |

---

### 4 ｜颜色体系

#### A. 文件图例颜色

| 角色 | 颜色 | Emoji |
|---|---|---|
| folder | `#2b8a3e` | 📁 |
| entry | `#e67700` | 🚀 |
| library | `#0b7285` | 📦 |
| tests | `#1864ab` | 🧪 |
| config | `#0ca678` | 🧩 |
| tools | `#6a4c93` | 🛠️ |
| class | `#d9480f` | 🧱 |

#### B. 函数分类颜色（函数名 span 上色）

| 分类 | 颜色 | 色值 | 判断方式 | 示例 |
|---|---|---|---|---|
| 入口 | 红色 | `#e74c3c` | `main`、`train`、脚本启动函数 | 🔧 train |
| 公开接口 | 蓝色 | `#3498db` | 类的公开方法（非 `_` 开头） | 🔧 step |
| 工厂/构造 | 绿色 | `#2ecc71` | `from_*`、`@classmethod` 构造器 | 🔧 from_config |
| 特殊方法 | 橙色 | `#e67e22` | `__init__`、`__repr__`、`__len__` 等 | 🔧 \_\_init\_\_ |
| 内部实现 | 灰色 | `#95a5a6` | `_xxx` 私有方法、模块级工具函数 | 🔧 \_helper |
| GPU 内核 | 紫色 | `#9b59b6` | `@wp.kernel` 等装饰器、名含 kernel | 🔧 compute_kernel |

**颜色直觉**：红=起点 · 蓝=正门 · 绿=创造 · 橙=特殊 · 灰=背景 · 紫=异世界

#### C. 调用层级徽章（G / L 系统）

每个函数名前放置 1-2 个圆角徽章，标识其在调用链中的位置。

**G 徽章（跨文件深度）**：

| 标记 | 背景色 | 含义 |
|---|---|---|
| `G0` | `#e74c3c`（红） | Surface——用户直接调用 |
| `G1` | `#e67e22`（橙） | Service——被入口调用的公开方法 |
| `G2` | `#f1c40f`（黄） | Core——被 API 层调用的底层实现 |

**L 徽章（文件内深度）**：仅在同一文件内存在调用分层时显示。

| 标记 | 背景色 | 含义 |
|---|---|---|
| `L0` | `#444`（深灰） | 顶层——文件内的主入口函数 |
| `L1` | `#888`（灰） | 被调用——被同文件其他函数调用 |

**徽章样式**：`background:色值; color:#fff; border-radius:10px; padding:2px 8px; font-size:25px; font-weight:900`

**书写规则**：
- G 徽章必须有，L 徽章仅在文件内存在调用分层时才加（如文件内所有函数都是并列的、互不调用，则省略 L 徽章）
- 徽章放在函数名 span 之前，与函数名同行

#### D. 输入 / 输出 Token 配色

| 元素 | 文字色 | 背景色 |
|---|---|---|
| 输入徽章 | `#dbeafe` | `#1d4ed8` |
| 输出徽章 | `#fff7ed` | `#c2410c` |
| `in.` | `#1c7ed6` | — |
| `out.` | `#e8590c` | — |
| 变量名 | `#9CDCFE` | — |
| 类型 | `#4EC9B0` | — |
| 关键字（如 `None`） | `#C586C0` | — |

---

### 5 ｜输入 / 输出书写格式（严格）

每个参数 / 返回值写成 **变量名: 类型**，各占一行：

```
- in. mesh_pos_w: Tensor[N,m,3]
- in. sensor_cfg: SensorCfg
- out. hit_distances: Tensor[N,r]
```

无返回值时写 `out. None`（关键字色 `#C586C0`）。

---

### 6 ｜视觉规范补充

- 输入 / 输出做**徽章样式**：`border-radius:4px; padding:1px 6px`。
- 保留四行图例（文件图例 / 函数分类 / Token 配色 / 调用层级）于仓库名下方。
- 不修改语义内容，只做结构化与样式化。

---

### 7 ｜工作流（分步对话）

整个改造过程分为 **多个 Session**，每个 Session 覆盖一个独立范围。

1. **我**说出总任务后，你给出 Session 列表（含范围 / 预估文件数 / 触发快捷键）。
2. 每个 Session 开始前，**我只需输入对应数字**（如 `1`），你自动执行该 Session。
3. 单个 Session 内部流程：
   - 定位待处理节点 → 阅读源码 → 编写并运行 Python 脚本批量插入 → 输出统计。
4. Session 完成后给出变化统计表（行数 / 作用数 / 徽章数），等待我输入下一个数字。
5. **全部 Session 完成后**输出最终汇总表。

---

### 8 ｜输出要求

- 直接修改工作区中的 MINDMAP.md（覆盖式）。
- 不解释过程，不省略节点。
- 每次修改后用脚本统计并报告计数。
- 默认中文输出。用户可指定语言（如"用英文"）。

---

### 9 ｜中英术语对照（英文输出时固定用词）

| 中文 | English |
|------|---------|
| 作用 | Purpose |
| 输入 | Input |
| 输出 | Output |
| 图例 | Legend |
| 文件说明 | Role |
| 类说明 | Role |
| 入口 | Entry |
| 公开接口 | Public API |
| 工厂/构造 | Factory |
| 特殊方法 | Dunder |
| 内部实现 | Internal |
| GPU 内核 | GPU Kernel |
| 入口层 (G0) | Surface |
| API 层 (G1) | Service |
| 内部层 (G2) | Core |

---

### 10 ｜Evolution 模式（`--evolution`）

**触发**：用户输入 `/mapc --evolution` 或 `/mapc --evolution 目标描述`。

**目的**：在正常 `/mapc` 产物之外，**额外**生成早/中期的骨架思维导图，让用户看清项目是**怎么长起来的**。早/中期骨架没有被后期 feature 淹没，核心抽象一目了然。

**核心思想**：
- 早/中期图**只出骨架**（纯 AST，零 LLM 成本），用来干净地看那个时间点的结构
- 当前版本仍走完整流程（骨架 + LLM Session 补描述），是主产物
- 三张图并排对照，不需要颜色标注演化 —— 用户自己扫结构差异即可

#### 前置检查

1. **必须是 git 仓库**：若不是，提示用户并退回普通 `/mapc`
2. **提交数 ≥ 10**：`git rev-list --count HEAD` 太少时不值得，建议直接普通模式
3. **工作区干净**：有未提交变更时提示用户（worktree 机制不会影响主工作区，但提醒为好）

#### 工作流

1. **选 3 个代表性 commit**（早 / 中 / 当前）：
   - 读取 `git log --oneline --stat`、`git tag`、顶层目录出现时间
   - 按「核心架构确立 / 功能显著扩张 / 当前 HEAD」三个阶段挑 commit
   - 告诉用户选择结果和理由，让用户可以修正或确认

2. **结构差异预检**（决定是否跳过早/中期骨架）：

   对每个候选 commit 计算「结构签名」：
   - 顶层目录集合：`git ls-tree --name-only <hash> | grep -v '^\.' | sort`（只取目录+非隐藏）
   - 有效文件数：`git ls-tree -r <hash> | awk '{print $4}' | grep -E '\.(py|cpp|cc|hpp|h|md|toml|yaml|yml|json|ini)$' | wc -l`

   判断规则（每个阶段独立判断，独立跳过）：

   | 阶段 | 跳过条件 |
   |---|---|
   | 早期 | 顶层目录集合 == 当前 **AND** 文件数 / 当前文件数 ≥ **0.8** |
   | 中期 | 顶层目录集合 == 当前 **AND** 文件数 / 当前文件数 ≥ **0.9** |

   - 跳过时明确告知用户原因，例如：「早期版本已有 N 文件，与当前 M 文件结构高度重叠（顶层目录一致、占比 85%），跳过 `MINDMAP_early.md` 生成」
   - 如果**两个阶段都被跳过**：告知用户「此仓库结构演化幅度小，evolution 模式价值有限」，询问是否继续（继续 = 只生成当前版本主图，等同默认 `/mapc`）

3. **在主仓库里记录当前分支**（用于后续参考，无需 checkout）：
   ```bash
   MAIN_REPO=$(pwd)
   REPO_NAME=$(basename "$MAIN_REPO")
   ```

4. **为未被跳过的阶段创建独立 worktree**（不影响主目录）：
   ```bash
   git worktree add "/tmp/${REPO_NAME}-early" <early_hash>
   git worktree add "/tmp/${REPO_NAME}-mid"   <mid_hash>
   ```

5. **在各 worktree 运行 `repo2mindmap.py`**（纯 AST，秒出）：
   ```bash
   python <skill_dir>/scripts/repo2mindmap.py "/tmp/${REPO_NAME}-early"
   python <skill_dir>/scripts/repo2mindmap.py "/tmp/${REPO_NAME}-mid"
   ```
   脚本会把 `MINDMAP.md` 写到传入目录下。

6. **把骨架图拷回主仓库并重命名**：
   ```bash
   cp "/tmp/${REPO_NAME}-early/MINDMAP.md" "$MAIN_REPO/MINDMAP_early.md"
   cp "/tmp/${REPO_NAME}-mid/MINDMAP.md"   "$MAIN_REPO/MINDMAP_mid.md"
   ```

7. **当前版本走完整 `/mapc` 流程**（见第 7 节的 Session 工作流），产出 `MINDMAP.md`

8. **清理 worktree**（只清理实际创建的）：
   ```bash
   git worktree remove "/tmp/${REPO_NAME}-early"
   git worktree remove "/tmp/${REPO_NAME}-mid"
   ```

#### 产物

| 文件 | 内容 | 生成方式 |
|---|---|---|
| `MINDMAP_early.md` | 早期骨架图 | 纯 AST，无描述 |
| `MINDMAP_mid.md`   | 中期骨架图 | 纯 AST，无描述 |
| `MINDMAP.md`       | 当前版本深度图 | AST + LLM Session 补描述（主产物） |

用户打开 `MINDMAP.md` 深读当前版本；需要看演化时切到 `MINDMAP_early.md` / `MINDMAP_mid.md` 作参照。

#### 成本

- 比普通 `/mapc` 多 1 次 LLM 调用（选 commit 时的 git log 分析，可合并到第一步对话里）
- 多 2 次 `repo2mindmap.py` 运行（纯 Python AST，秒级）
- 多 2 次 `git worktree add` + `remove`（本地磁盘操作，秒级）
