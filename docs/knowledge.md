# 项目知识索引

知识由使用项目维护。Codex Spec 源码只提供通用指南，不附带项目知识包。小项目直接阅读现有文档即可；重复使用的资料较多时，再在项目内创建目录与 `pack.json`。

```json
{
  "schema_version": 1,
  "id": "team/project",
  "resources": [
    {
      "id": "state-map",
      "kind": "fact",
      "summary": "订单状态归属与接口边界",
      "path": "state-map.md",
      "overview": "overview.md",
      "scope": ["src/orders/**", "tests/orders/**"],
      "source_refs": ["src/orders/store.ts", "docs/order-api.md"],
      "reviewed_at": "2026-11-01",
      "status": "verified"
    }
  ]
}
```

`id`、`kind`、`summary`、`path` 为资源必需字段；`scope` 默认为 `**`。包 ID 支持小写字母、数字、连字符与斜杠；资源 ID 是小写连字符标识。资源种类为 `fact`、`procedure`、`design`、`constraint`、`experience`。`path` 和可选 `overview` 均相对于包目录，必须指向存在的文件。引用不能通过绝对路径或符号链接越出目录。

`source_refs`、`reviewed_at` 和 `status` 是给阅读者的溯源信息，不是自动核实的证明；未填状态按 `candidate` 展示。优先记录可复查的来源和适用版本。路径过滤使用大小写敏感的 glob 字符串匹配，`**` 可跨目录；它不是 Git ignore 语法，也不表示完整调用关系。

先索引，再概览，最后按需读原文。对关键约束仍要核对当前源码、运行结果和真实需求。资料冲突时记录差异与依据，不按知识文件数量投票。工具返回的 SHA-256 帮助识别本次读取内容，不保证内容正确或未来不变。

稳定事实、操作方法、视觉参照和失败经验分别标明类型。经验应包括症状、已检验根因、有效修复、适用边界与失效条件；一次猜测或临时补丁留在当前 Spec。更新和清理过期内容是维护工作，不自动把每次修复追加为长期规则。
