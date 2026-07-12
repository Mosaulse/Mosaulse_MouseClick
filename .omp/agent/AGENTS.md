# 1. 开发助手

## CodeGraph

In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

- **MCP tools** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them. `codegraph_node` returns one symbol's source + callers, or reads a whole file with line numbers. If the tools are listed but deferred, load them by name via tool search.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` and `codegraph node <symbol-or-file>` print the same output.

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.
## 语言规则
- 思考、回答、代码注释一律使用中文。
- 变量名/类名/方法名保持英文命名规范。
## 回答格式
无论我给你的是一段代码、一个报错、还是一个需求，你按以下结构回答：

**💡 修改了什么**
> 精简说明改了哪些地方，能用 diff 就用 diff。

**🧠 为什么这么做**
> 说明原理。结合 Python 底层机制（GIL 线程调度、PyQt5 事件循环、pyautogui 输入注入等）解释，不要只说"这样更快"。

**📦 修改后的结果**
> 给出修改后完整可用的代码。如果是架构或需求类问题，给出完整方案。

如果我给的不是代码而是问题或需求，直接跳过前两步，用第三步给出方案和注意事项。

# 2. Git提交信息规范

在执行 "Generate Commit Message" 时必须遵循以下规则：

- 使用中文
- 格式: `[类型]`: 描述 （描述限 50 字内，须用中文古文，且以动词开头）
- 上下文：仅根据 git 暂存区 (staged changes) 的内容生成，不要包含未暂存的修改。
- 类型
  - `[新增]`: 新功能
  - `[修复]`: 修复 bug
  - `[重构]`: 代码重构
  - `[测试]`: 测试变更
  - `[文档]`: 文档变更
  - `[样式]`: 格式调整
  - `[优化]`: 性能优化
  - `[发布]`: 版本发布
  - `[依赖]`: 更新依赖
