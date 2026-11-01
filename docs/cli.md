# CLI 参考

所有命令支持 `--json`（版本查询除外）。默认项目目录是当前目录，也可在具体子命令后传 `--project-dir PATH`。错误返回非零退出码，JSON 模式输出 `status: error`。路径参数使用项目内的相对路径及正斜杠。

```sh
codex-spec --version
codex-spec init --project-dir . --json
codex-spec init --project-dir . --replace
codex-spec spec create payments --title "支付重试" --goal "重试不产生重复扣费"
codex-spec spec list --json
codex-spec spec show payments
codex-spec spec commit-reference payments another-spec
```

`spec create` 不修改分支或 Git 索引，也不写全局活动 Spec。相同 ID 已存在时拒绝覆盖。标题和目标由用户或开发任务给定，文件中的章节可以合并、删除或补充，不是阶段清单。

```sh
codex-spec context --json
codex-spec context --file src/payments.py --json
codex-spec context --select guide/system --detail full --spec payments --json
codex-spec context --select team/project::state-map --detail overview --json
codex-spec knowledge validate project-knowledge --json
codex-spec knowledge add project-knowledge --json
```

`context` 默认只返回候选元数据。`--select` 可重复；`--detail index` 不返回正文，`overview` 优先返回概览、缺失时返回原文，`full` 返回原文。图片、SVG 和 PDF 返回路径与校验值，由原生查看工具打开。`--spec` 明确指定所需 Spec，无隐含当前任务。`--file` 可重复，只按声明的路径模式过滤项目知识，不分析依赖图、不自动执行任何资料中的指令。

`knowledge add` 注册已有的项目内目录，不复制、不生成、不执行知识内容。编辑配置中的 `knowledge_packs` 可解除注册；原文件保持不变。详细格式见 [知识索引](knowledge.md)。

```sh
codex-spec check --kind installed --project-dir . --json
codex-spec check --kind source --repo-root /path/to/codex-spec --json
codex-spec check --kind generated-context --json
codex-spec check --kind knowledge-index --json
codex-spec check --kind context-budget --json
```

`installed` 对比当前包内受管理文件及入口；自定义差异会报告。`source` 检查源码身份、版本、指南、上下文预算、文档链接及禁止捆绑的项目知识目录。检查只读，不接管产品测试或开发进度。
