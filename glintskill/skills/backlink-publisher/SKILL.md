---
name: backlink-publisher
description: 根据本地外链 JSON 队列或批次队列，把当前项目发布到免费外链、目录、startup listing、AI tools 和 gallery 平台。用于需要 Codex 使用 @chrome 操作用户已登录的 Chrome、读取项目资料夹、按单个 JSON 或 30 条左右的 batch JSON 逐组处理、通过 subagent 调用 $humanizer 生成自然文案、填写平台提交表单、直接提交免费 listing 并更新队列状态的任务。
---

# 外链发布器

## 概览

从单个 JSON 队列读取外链平台任务，把当前项目提交到免费外链平台。执行时使用 Chrome 插件操作浏览器，用本地项目资料夹作为事实来源，任何需要生成的 listing 文案都必须交给 fresh subagent 处理。

当候选外链很多时，优先使用批次 JSON 逐组运行。推荐每个 batch 控制在 30 条左右，并把可执行 batch 放在 `data/backlinks/batches/`，例如 `data/backlinks/batches/batch-001.json`。默认通过 `data/backlinks/foreign-backlinks-batches-manifest.json` 选择要运行的 batch；manifest 只用于记录批次顺序和数量，不是队列文件，不能直接传给发布流程。

## 必需输入

- 批次 manifest。默认路径：`data/backlinks/foreign-backlinks-batches-manifest.json`，用于选择要运行的 batch；实际运行时必须读取其中某一个 batch JSON。
- 外链队列 JSON。默认使用 manifest 指向的批次 JSON，例如 `data/backlinks/batches/batch-001.json`。旧单文件队列 `data/backlinks/free-backlinks.json` 只作为兼容入口：只有用户明确指定，或没有可用 manifest 时才使用。
- 项目资料夹，里面必须有 `profile.md` 和 `metadata.json`，格式兼容 `project-profile-capture` 的输出。
- 公开提交信息文件。默认路径：`public-submission-info.md`，用于保存允许公开使用的邮箱、联系人姓名、公司所在地、成立时间等信息。
- Chrome 中已经登录用户的 Google 账号。
- 团队人数默认为 1，除非用户明确指定

如果当前项目里有多个项目资料夹，并且用户没有指定目标项目，先询问用户使用哪一个。如果没有可用项目资料夹，停止并让用户先用 `project-profile-capture` 创建。

如果 `public-submission-info.md` 不存在，先创建模板并询问用户补充公开提交信息。如果文件存在但必填字段为空，第一时间询问用户补齐后再开始处理外链队列。不要从 Chrome、Google 账号或项目文案里推断私人联系信息。

## 参考文件

- 修改或更新队列前，先读 `references/backlinks-json-schema.md`。
- 使用 Chrome 或提交 listing 前，先读 `references/chrome-workflow.md`。
- 请求生成文案前，先读 `references/content-subagent-prompt.md`。
- 判断错误后是否继续前，先读 `references/failure-policy.md`。

## 工作流程

1. 确定本轮队列 JSON：
   - 如果用户指定了具体 JSON 文件，使用该文件。
   - 不要把 `batch-*-submitted.json` 当作执行队列；这类文件只是已提交结果导出。
   - 如果用户只指定 manifest，或没有指定 JSON 但默认 manifest 存在，先读取 manifest。用户指定了 batch 编号时使用对应 batch；没有指定时，按 manifest 顺序打开 `batches[].file`，选择第一个实际包含 `status: "pending"` 队列项的 batch，并在开始前报告 batch 编号和待处理条目数。不要只依赖 manifest 里的 `status` 字段。
   - 如果没有可用 manifest，再回退到 `data/backlinks/free-backlinks.json`。
   - 不要把 manifest 当作外链队列传给发布流程。
2. 校验本轮外链 JSON：

```bash
python3 skills/backlink-publisher/scripts/validate_backlinks_json.py <queue-json-path>
```

3. 读取并检查 `public-submission-info.md`。缺少必填公开信息时，先询问用户补齐：
   - 联系邮箱
   - 联系人姓名
   - 公司所在地
   - 成立时间
4. 读取所选项目资料夹中的 `profile.md` 和 `metadata.json`。
5. 默认只处理当前队列 JSON 内 `status: "pending"` 的队列项，除非用户明确要求重试其他状态。
6. 每处理一个队列项，先把该项状态设为 `in_progress`。
7. 所有浏览器操作都使用 `@chrome`。不要改用其他浏览器后端。
8. 打开平台 URL，寻找 submit、add、list、post、suggest 或类似入口。
9. 如果平台出现 Google 账号选择器，默认选择第一个可见的个人 Google 账号继续。只有无法判断是否为个人账号、要求额外敏感权限或没有 Google 登录选项时才停止。
10. 如果表单需要生成文案，按 `references/content-subagent-prompt.md` 启动 fresh subagent。
11. 使用项目资料、公开提交信息、生成文案、项目 URL、logo 和截图填写表单。
12. 免费 listing 表单的必填字段填完后直接提交。
13. 页面出现成功状态、成功提示或可用 listing URL 后，把该项标记为 `submitted`，并把 `result_url` 设为 listing URL 或当前页面 URL。
14. 如果触发停止条件，把该项标记为 `needs_user` 或 `failed`，把原因写入 `error`，并停止本轮任务。
15. 当前 batch 处理完后，报告本批提交、跳过、失败和需要用户处理的数量；除非用户明确要求继续，不要自动进入下一个 batch。

## 状态更新规则

更新 JSON 队列时：

- 保持队列项顺序不变。
- 保留未来可能新增的未知字段。
- 除非用户要求批量更新，只修改当前正在处理的队列项。
- 如果本轮输入是 batch JSON，状态写回该 batch 文件；不要把状态写回完整候选池或正式队列，除非用户明确指定。
- manifest 只作为批次索引；如果本轮是通过 manifest 选中的 batch，处理结束后同步对应 batch 的 `item_count`、`first_id`、`last_id` 和 `status`。没有 `pending` / `in_progress` 项时，把 manifest 中该 batch 标记为 `processed`；仍有待处理项时保持或设为 `pending`。
- `last_attempt_at` 使用 ISO 8601 时间戳。
- 提交成功时保持 `error: null`。

## 停止规则

如果页面要求 CAPTCHA、付费、浏览器权限、私密个人信息、用户未授权的非 Google 登录，或任何超出免费公开项目 listing 提交范围的动作，立即停止并报告给用户。通过 Google 登录或继续创建免费 listing 账号是允许的，但只能使用第一个可见的个人 Google 账号，且不能授权敏感权限。
