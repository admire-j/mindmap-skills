# repo2mindmap.py  —— 生成 Markmap 思维导图（带文件角色标签与着色）
# 用法（保持不变）：在仓库根目录由你现有的 mkmap/mkmaphtml 调用即可。
from __future__ import annotations
import os, ast
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Set, Optional

# ---------- 默认配置 ----------
DEFAULT_IGNORE: Set[str] = {
    ".git","__pycache__",".venv","env","build","dist",".idea",".vscode","logs","outputs","checkpoints"
}
DEFAULT_VALID_EXT: Set[str] = {".py",".cpp",".cc",".hpp",".h",".md",".toml",".yaml",".yml",".json",".ini"}

DEFAULT_COLORS = {
    "folder":"#2b8a3e",
    "file":"#1c7ed6",
    "class":"#d9480f",
    "func":"#5f3dc4",
    # 文件角色
    "entry":"#e67700",   # 入口：橙
    "lib":"#0b7285",     # 库：青
    "test":"#1864ab",    # 测试：深蓝
    "config":"#0ca678",  # 配置：绿
    "tool":"#6a4c93",    # 工具：紫
}
DEFAULT_EMOJI = {
    "folder":"📁",
    "file":"📄",
    "class":"🧱",
    "func":"🔧",
    # 文件角色
    "entry":"🚀",
    "lib":"📦",
    "test":"🧪",
    "config":"🧩",
    "tool":"🛠️",
}

@dataclass
class MindmapConfig:
    root_dir: str = "."
    targets: Optional[List[str]] = None
    ignore: Set[str] = field(default_factory=lambda: set(DEFAULT_IGNORE))
    valid_ext: Set[str] = field(default_factory=lambda: set(DEFAULT_VALID_EXT))

    # 展示
    expand_all: bool = True
    show_empty_py: bool = False           # 没有类/函数（/变量）的 .py 是否显示
    show_cfg_vars: bool = False           # 是否显示“配置变量”（全大写/含 Cfg/以 _cfg 结尾）
    max_classes: int = 12
    max_funcs: int = 16
    max_vars: int = 32

    # 样式
    colors: Dict[str,str] = field(default_factory=lambda: dict(DEFAULT_COLORS))
    emoji: Dict[str,str]  = field(default_factory=lambda: dict(DEFAULT_EMOJI))
    max_width: int = 260
    color_freeze_level: int = 2

    # 输出文件名（mkmap/mkmaphtml 会用）
    output_md: str = "MINDMAP.md"
    output_html: str = "mindmap.html"

# ---------- 样式常量 ----------
# 各层级节点的 font-size / font-weight
STYLE = {
    "h2_folder":  (35, 700),   # ## 顶层目录标题
    "folder":     (32, 700),   # 📁 子目录
    "file":       (29, 600),   # 📦/🚀/🧩/🧪/🛠️ 文件
    "class":      (27, 700),   # 🧱 类
    "func":       (25, 600),   # 🔧 函数
}

# ---------- 工具函数 ----------
def _colorize(colors: Dict[str,str], kind: str, text: str) -> str:
    return f'<span style="color:{colors[kind]}">{text}</span>'

def _styled(text: str, *, size: int, weight: int, color: str) -> str:
    """带 font-size / font-weight / color 的 span"""
    return f'<span style="font-size:{size}px;font-weight:{weight};color:{color}">{text}</span>'

def _escape_html(s: str) -> str:
    import html
    return html.escape(s)

def _autodetect_targets(root_dir: str, ignore: Set[str]) -> List[str]:
    # 目标目录自动探测：
    # - 保持原先“常见目录优先”的顺序
    # - 但不要因为命中候选目录就丢掉其它顶层目录（例如 legged_gym）
    candidates = ["src","lib","app","apps","packages","core","server","client","parkour_isaaclab","scripts","rsl_rl"]
    all_dirs = [d for d in os.listdir(root_dir)
                if os.path.isdir(os.path.join(root_dir, d))
                and not d.startswith(".")
                and d not in ignore]

    prioritized = [d for d in candidates if d in all_dirs]
    rest = [d for d in all_dirs if d not in prioritized]
    return prioritized + sorted(rest)

def _list_tree(root_dir: str, targets: List[str], ignore: Set[str], valid_ext: Set[str]
               ) -> List[Tuple[str, List[str], List[str]]]:
    items = []
    for base in targets:
        abs_base = os.path.join(root_dir, base)
        if not os.path.isdir(abs_base): continue
        for r, dirs, files in os.walk(abs_base):
            rel_root = os.path.relpath(r, root_dir)
            dirs[:] = [d for d in dirs if d not in ignore and not d.startswith(".")]
            sel = [f for f in files if os.path.splitext(f)[1] in valid_ext]
            items.append((rel_root, sorted(dirs), sorted(sel)))
    return items

# ---------- 代码解析与分类 ----------
class PyInfo:
    def __init__(self):
        self.classes: List[str] = []
        self.funcs: List[str] = []
        self.vars_cfg: List[str] = []
        self.has_main_guard: bool = False
        self.imports: Set[str] = set()
        self.has_shebang: bool = False

def _parse_python_file_abs(abs_path: str, cfg: MindmapConfig) -> PyInfo:
    info = PyInfo()
    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            src = f.read()
        if src.startswith("#!"):
            info.has_shebang = True
        tree = ast.parse(src, filename=abs_path)
    except Exception:
        return info

    # main 守卫
    for n in getattr(tree, "body", []):
        if isinstance(n, ast.If):
            # if __name__ == "__main__": ...
            try:
                cond = ast.unparse(n.test) if hasattr(ast, "unparse") else ""
            except Exception:
                cond = ""
            if "__name__" in cond and "__main__" in cond:
                info.has_main_guard = True
                break

    for n in ast.walk(tree):
        if isinstance(n, ast.ClassDef):
            info.classes.append(n.name)
        elif isinstance(n, ast.FunctionDef) and not n.name.startswith("_"):
            info.funcs.append(n.name)
        elif isinstance(n, ast.Import):
            for a in n.names: info.imports.add(a.name)
        elif isinstance(n, ast.ImportFrom):
            if n.module: info.imports.add(n.module)

    # 顶层配置变量（可选）
    cfg_like = []
    for n in getattr(tree, "body", []):
        if isinstance(n, (ast.Assign, ast.AnnAssign)):
            targets = []
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name):
                        targets.append(t.id)
            elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
                targets.append(n.target.id)
            for name in targets:
                if not name: continue
                if name.startswith("_"): continue
                if (name.isupper()) or name.lower().endswith("_cfg") or ("Cfg" in name or "CFG" in name):
                    cfg_like.append(name)
    info.classes = sorted(set(info.classes))[:cfg.max_classes]
    info.funcs   = sorted(set(info.funcs))[:cfg.max_funcs]
    info.vars_cfg= sorted(set(cfg_like))[:cfg.max_vars]
    return info

def _classify_file(rel_path: str, info: Optional[PyInfo]) -> str:
    """返回文件角色：entry/lib/test/config/tool（默认 lib）"""
    p = rel_path.replace("\\","/")
    name = os.path.basename(p)
    # 测试
    if p.startswith("tests/") or name.startswith("test_") or name.endswith("_test.py"):
        return "test"
    # 入口：main守卫 / shebang / scripts/bin 目录 / 常见命名
    if info and (info.has_main_guard or info.has_shebang):
        return "entry"
    if p.startswith(("scripts/","tools/","bin/")) or name in {"main.py","cli.py","train.py","demo.py"} or name.startswith("run_"):
        return "entry"
    # 配置：纯配置文件或 .py 中只有变量（或主要是变量）
    ext = os.path.splitext(name)[1].lower()
    if ext in {".yaml",".yml",".toml",".json",".ini"}:
        return "config"
    if info:
        if not info.classes and not info.funcs and info.vars_cfg:
            return "config"
    # 工具：utils/helpers/common
    if "/utils/" in p or "/helpers/" in p or "/common/" in p:
        return "tool"
    # 默认为库
    return "lib"

# ---------- 主生成 ----------
def generate_mindmap(config: MindmapConfig) -> str:
    root = os.path.abspath(config.root_dir)
    targets = config.targets or _autodetect_targets(root, config.ignore)

    initial = 20 if config.expand_all else 2
    repo_name = os.path.basename(root)
    lines = [
        "---",
        "markmap:",
        f"  initialExpandLevel: {initial}",
        f"  maxWidth: {config.max_width}",
        f"  colorFreezeLevel: {config.color_freeze_level}",
        "---",
        f'# <span style="font-size:35px;font-weight:700">{repo_name}</span>',
        "",
        "- 文件图例: "
        + " · ".join([
            _colorize(config.colors,"folder", f"{config.emoji['folder']} folder"),
            _colorize(config.colors,"entry",  f"{config.emoji['entry']} entry"),
            _colorize(config.colors,"lib",    f"{config.emoji['lib']} library"),
            _colorize(config.colors,"test",   f"{config.emoji['test']} tests"),
            _colorize(config.colors,"config", f"{config.emoji['config']} config"),
            _colorize(config.colors,"tool",   f"{config.emoji['tool']} tools"),
            _colorize(config.colors,"class",  f"{config.emoji['class']} class"),
        ]),
        "- 函数分类: "
        + " · ".join([
            '<span style="color:#d9480f">⬤ dunder</span>',
            '<span style="color:#1c7ed6">⬤ 实例方法</span>',
            '<span style="color:#0ca678">⬤ 工厂方法</span>',
            '<span style="color:#2f9e44">⬤ 工具函数</span>',
            '<span style="color:#ae3ec9">⬤ GPU 内核</span>',
            '<span style="color:#e67700">⬤ 入口/脚本</span>',
            '<span style="color:#868e96">⬤ 包导出</span>',
        ]),
        "- Token 配色: "
        + " · ".join([
            '<span style="color:#1c7ed6">in.</span>',
            '<span style="color:#e8590c">out.</span>',
            '<span style="color:#9CDCFE">变量名</span>',
            '<span style="color:#4EC9B0">类型</span>',
            '<span style="color:#C586C0">关键字</span>',
        ]),
        ""
    ]

    items = _list_tree(root, targets, config.ignore, config.valid_ext)
    top_map: Dict[str, List[Tuple[str,List[str],List[str]]]] = {}
    for rel_root, dirs, files in items:
        top = rel_root.split(os.sep)[0]
        top_map.setdefault(top, []).append((rel_root, dirs, files))

    for top, buckets in sorted(top_map.items()):
        sz, wt = STYLE['h2_folder']
        clr = config.colors['folder']
        lines.append(f'## {_styled(config.emoji["folder"]+" "+top, size=sz, weight=wt, color=clr)}')
        seen_dirs: Set[str] = set()

        for rel_root, dirs, files in sorted(buckets):
            parts = rel_root.split(os.sep)
            subparts = parts[1:]
            # 输出子目录树（去重）
            cur = ""
            for i,p in enumerate(subparts):
                cur = os.path.join(*parts[:i+2])
                if cur in seen_dirs: continue
                seen_dirs.add(cur)
                sz, wt = STYLE['folder']
                clr = config.colors['folder']
                lines.append(f"{'  '*i}- {_styled(config.emoji['folder']+' '+p, size=sz, weight=wt, color=clr)}")

            base_indent = "  "*max(0,len(subparts))
            for f in files:
                rel_path = os.path.join(rel_root, f)
                abs_path = os.path.join(root, rel_path)
                ext = os.path.splitext(f)[1].lower()

                pyinfo: Optional[PyInfo] = None
                if ext == ".py":
                    pyinfo = _parse_python_file_abs(abs_path, config)

                # 以前：如果 .py 里没有类/函数（以及可选的配置变量），会直接跳过文件本身
                # 现在：无论文件里有没有定义，都至少把“文件名”列出来；仅在为空时隐藏子项
                show_py_children = True
                if ext == ".py" and pyinfo and not config.show_empty_py:
                    has_children = bool(pyinfo.classes or pyinfo.funcs or (config.show_cfg_vars and pyinfo.vars_cfg))
                    if not has_children:
                        show_py_children = False

                role = _classify_file(rel_path, pyinfo)
                role_color = config.colors.get(role, config.colors["file"])
                role_emoji = config.emoji.get(role, config.emoji["file"])

                # 文件行（链接到源码，带 font-size）
                fsz, fwt = STYLE['file']
                file_label = f"{role_emoji} {f}"
                file_styled = f'<span style="font-size:{fsz}px;font-weight:{fwt};color:{role_color}">{file_label}</span>'
                file_link = f"[{file_styled}]({rel_path})"
                lines.append(f"{base_indent}- {file_link}")

                # 子项：每个类 / 函数独立为一个分支
                if ext == ".py" and pyinfo and show_py_children:
                    csz, cwt = STYLE['class']
                    cclr = config.colors['class']
                    for c in pyinfo.classes:
                        lines.append(f"{base_indent}  - {_styled(config.emoji['class']+' '+c, size=csz, weight=cwt, color=cclr)}")
                    ksz, kwt = STYLE['func']
                    kclr = config.colors['func']
                    for fn in pyinfo.funcs:
                        lines.append(f"{base_indent}  - {_styled(config.emoji['func']+' '+fn, size=ksz, weight=kwt, color=kclr)}")
                    if config.show_cfg_vars and pyinfo.vars_cfg:
                        for v in pyinfo.vars_cfg:
                            lines.append(f"{base_indent}  - {_colorize(config.colors,'config', config.emoji['config']+' '+v)}")

    return "\n".join(lines)

# ---------- 输出辅助 ----------
def write_markdown(config: MindmapConfig) -> str:
    md = generate_mindmap(config)
    out = os.path.join(config.root_dir, config.output_md)
    with open(out,"w",encoding="utf-8") as f:
        f.write(md)
    return out

def write_html(config: MindmapConfig, markdown_text: Optional[str]=None) -> str:
    md = markdown_text or generate_mindmap(config)
    html = f"""<!doctype html>
<html><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Markmap Export</title>
<script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.18.12"></script>
<style>html,body,#mindmap{{height:100%;margin:0}}</style>
</head>
<body>
<div id="mindmap"></div>
<script type="text/markdown">
{_escape_html(md)}
</script>
</body></html>"""
    out = os.path.join(config.root_dir, config.output_html)
    with open(out,"w",encoding="utf-8") as f:
        f.write(html)
    return out

# ---------- 直接运行（可选） ----------
if __name__ == "__main__":
    cfg = MindmapConfig(root_dir=".", expand_all=True)
    print("Writing:", write_markdown(cfg))
