---
name: backlink-publisher
description: 根据本地外链 JSON 队列，把当前项目发布到免费外链、目录、startup listing、AI tools 和 gallery 平台。用于需要 Codex 使用 @chrome 操作用户已登录的 Chrome、读取项目资料夹、通过 subagent 调用 $humanizer 生成自然文案、填写平台提交表单、直接提交免费 listing 并更新队列状态的任务。
---

# 外链发布器

## 概览

从 JSON 队列读取外链平台任务，把当前项目提交到免费外链平台。执行时使用 Chrome 插件操作浏览器，用本地项目资料夹作为事实来源，任何需要生成的 listing 文案都必须交给 fresh subagent 处理。

## 必需输入

- 外链队列 JSON。默认路径：`data/backlinks/free-backlinks.json`。
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

1. 校验外链 JSON：

```bash
python3 skills/backlink-publisher/scripts/validate_backlinks_json.py data/backlinks/free-backlinks.json
```

2. 读取并检查 `public-submission-info.md`。缺少必填公开信息时，先询问用户补齐：
   - 联系邮箱
   - 联系人姓名
   - 公司所在地
   - 成立时间
3. 读取所选项目资料夹中的 `profile.md` 和 `metadata.json`。
4. 默认只处理 `status: "pending"` 的队列项，除非用户明确要求重试其他状态。
5. 每处理一个队列项，先把该项状态设为 `in_progress`。
6. 所有浏览器操作都使用 `@chrome`。不要改用其他浏览器后端。
7. 打开平台 URL，寻找 submit、add、list、post、suggest 或类似入口。
8. 如果平台出现 Google 账号选择器，默认选择第一个可见的个人 Google 账号继续。只有无法判断是否为个人账号、要求额外敏感权限或没有 Google 登录选项时才停止。
9. 如果表单需要生成文案，按 `references/content-subagent-prompt.md` 启动 fresh subagent。
10. 使用项目资料、公开提交信息、生成文案、项目 URL、logo 和截图填写表单。
11. 免费 listing 表单的必填字段填完后直接提交。
12. 页面出现成功状态、成功提示或可用 listing URL 后，把该项标记为 `submitted`，并把 `result_url` 设为 listing URL 或当前页面 URL。
13. 如果触发停止条件，把该项标记为 `needs_user` 或 `failed`，把原因写入 `error`，并停止本轮任务。

## 状态更新规则

更新 JSON 队列时：

- 保持队列项顺序不变。
- 保留未来可能新增的未知字段。
- 除非用户要求批量更新，只修改当前正在处理的队列项。
- `last_attempt_at` 使用 ISO 8601 时间戳。
- 提交成功时保持 `error: null`。

## 停止规则

如果页面要求 CAPTCHA、付费、浏览器权限、私密个人信息、用户未授权的非 Google 登录，或任何超出免费公开项目 listing 提交范围的动作，立即停止并报告给用户。通过 Google 登录或继续创建免费 listing 账号是允许的，但只能使用第一个可见的个人 Google 账号，且不能授权敏感权限。
