# 安装与干净升级

可将下面这段指令交给目标项目中的 Codex：

> 安装 liuminxin45/codex-spec 的 v0.1.0。先确认可用的 Python 3.11+，在专用环境中通过 GitHub 固定版本或发布 wheel 安装，再对当前项目运行 codex-spec init。检查安装结果，告诉我如何在新会话中使用 $codex-spec。已有 Spec Kit 的项目先列出旧入口及需要移除的内容，按我的升级要求处理，保留业务文档和代码。

## 手动安装

```sh
python -m venv .venv-codex-spec
```

Windows PowerShell 激活环境：

```powershell
.\.venv-codex-spec\Scripts\Activate.ps1
```

macOS / Linux 激活环境：

```sh
. .venv-codex-spec/bin/activate
```

然后安装并初始化：

```sh
python -m pip install "codex-spec @ git+https://github.com/liuminxin45/codex-spec.git@v0.1.0"
codex-spec init --project-dir .
codex-spec check --kind installed --project-dir . --json
```

该虚拟环境是本地工具，加入项目的忽略列表即可。无 Git 时使用 [发布 wheel](https://github.com/liuminxin45/codex-spec/releases/tag/v0.1.0)。不依赖 PowerShell 运行时；PowerShell 脚本只用于本仓库源码检查。

初始化支持未建 Git 仓库的目录，也支持已有分支和未提交改动。生成的 Skill 使用项目内路径，不要求全局安装 Skill。新建会话后显式调用 `$codex-spec`；如果客户端没有发现项目 Skill，直接读取入口文件也能执行同一套指导。

## 更新受管理文件

重复 `init` 会保留配置、Spec 与用户 `AGENTS.md`。对已有自定义受管理文件会报冲突；检查差异后可使用 `init --replace` 更新 Skill 和受管理入口。用户放在入口区块之外的内容继续保留。

旧版本没有自动迁移器。旧 `.specify/`、旧项目 Skill、旧工作流配置及旧 `AGENTS.md` 引用应逐项审查后移除；具体安装位置以实际项目为准。不要删除整个 `specs/` 或整个 `AGENTS.md`，其中可能包含业务资料。新工具不会加载旧格式，也不会修改全局安装目录。
