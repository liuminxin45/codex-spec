# Codex Spec

让 Codex 在复杂软件开发中保持四个工程习惯：做之前明确正确结果；修改时理解相关系统；做完后观察真实行为；失败时修正假设。

Codex Spec 是一层轻量工程指导。一个总 Skill、七份按需指南、独立 Spec 文档，以及可选的项目知识索引，帮助开发过程形成可以检查的判断依据。

它适用于 UI 重构、复杂状态、跨模块变更和持续返工，也适用于日常维护。小修改直接处理；复杂修改按可验证的功能切片推进。文档深度取决于风险，不以完成阶段或生成文件数量判断成功。

Codex Spec is an independent engineering-guidance layer for Codex, combining an on-demand Skill, specification documents, and optional project knowledge indexes.

## 选用与边界

适合希望在跨模块修改、UI 重构和反复修复中保留目标、判断与验证依据的开发者。小修改可以直接处理，复杂工作再使用独立 Spec；它不要求每次任务都生成整套文档。

它不提供模型服务，不是任务执行引擎，也不会隔离多个会话的改动。CLI 的安装与包测试不证明 AI 输出质量提升；最终行为仍需在目标项目中验证。

## 安装

需要 Python 3.11 或更高版本。建议在专用 Python 环境中安装：

```sh
python -m pip install "codex-spec @ git+https://github.com/liuminxin45/codex-spec.git@v0.1.0"
codex-spec init --project-dir /path/to/project
```

也可以从 [GitHub Releases](https://github.com/liuminxin45/codex-spec/releases/latest) 下载 wheel，通过 `python -m pip install /path/to/codex_spec-0.1.0-py3-none-any.whl` 安装。尚未发布到 PyPI，不要直接使用 `pip install codex-spec`。

在目标项目中新建 Codex 会话，使用 `$codex-spec`。安装器写入 `.agents/skills/codex-spec/`、一个简短的 `AGENTS.md` 入口和 `.codex-spec/config.json`。已有用户内容会保留；自定义的受管理文件需要显式 `init --replace` 才会覆盖。

## 使用

```text
$codex-spec 重构订单详情页，沿用现有视觉体系，保留筛选和返回行为。
$codex-spec 修复切换查询后旧响应覆盖新结果的问题，先查清状态归属。
$codex-spec 这个问题修了两次仍然存在，重新复现并检验根因假设。
```

重要变更可以建立独立 Spec：

```sh
codex-spec spec create order-details --title "订单详情改造" --goal "更快找到订单状态与下一步操作"
codex-spec context --select guide/ui --select guide/system --detail full --spec order-details
codex-spec spec commit-reference order-details
```

后一个命令输出提交正文中的引用：

```text
Spec: order-details
Spec-Docs: specs/order-details/spec.md
```

多个会话可以在当前分支、当前目录处理不同 Spec。没有全局活动任务、会话锁、文件认领、脏工作区门禁或自动分支管理。提交引用支持多个 Spec。工具不会隔离并发改动，合并和提交范围由开发者判断。

## 工程指导

| 指南 | 在什么情况下读取 |
| --- | --- |
| Product | 目标不清、设计选择影响体验、需要明确不可破坏行为 |
| UI | 页面、组件、交互与视觉一致性变更 |
| System | 状态、异步、接口和跨模块影响 |
| Slices | 大功能、迁移、需要分步验证的改造 |
| Diagnosis | 复现困难、修复失败、源码和运行现象不一致 |
| Verification | 选择证据、验证测试有效性、区分已证实与待验证 |
| Knowledge | 按需查阅项目事实、维护经验证的经验 |

默认只加载总 Skill 和索引；需要时读取指南、知识概览与原始资料。CLI 是文件辅助工具，Codex 可以直接用原生文件、终端和浏览器工具完成工作。没有任务执行引擎，也不强制新增测试、全量测试、独立验证 Agent 或人工审批。

## 文档与验证

- [文档入口](docs/README.md)：安装、CLI、知识管理与工程指导审查。
- [行为评估](docs/behavior-evaluation.md)：四种真实工程场景的固定任务与对照协议。
- [0.1.0 发布说明](docs/releases/0.1.0.md)：干净升级的变更范围。
- [English](README.en.md)

源码检查与安装包测试验证工具行为；它们不证明 AI 已经稳定改善产品质量。UI 与交互结果仍需在实际应用中观察，人的反馈只能来自真实反馈。

本项目由 Spec Kit 演进而来，0.1.0 是新的产品与接口起点，不兼容旧命令、配置或工作流。旧内容保留在 Git 历史中；升级到已有项目时，先检查并移除项目内原有入口，避免两套指导同时生效。工具不自动删除项目文件或全局 Skill。

MIT 许可证，保留 [原始版权声明](LICENSE)。
