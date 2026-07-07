# 失败处理策略

出现下列情况时，先判断应该 `skipped`、`needs_user` 还是 `failed`。只有 `needs_user` 和 `failed` 停止本轮任务；`skipped` 不停止，继续处理当前 batch 中的下一个 `pending` 队列项。

如果平台不符合当前项目要求，且用户不需要在 Chrome 中接手，使用 `skipped` 并继续下一个队列项：

- 平台只接受 boilerplate、template、open source、deal、discount、特定集成、特定行业或其他当前项目事实不满足的提交。
- 平台分类不适合当前项目，且没有通用分类。
- 表单问题本质是在确认一个当前项目没有的适配事实，例如要求说明如何使用某个特定第三方产品，而项目资料没有这种集成。

`skipped` 必须写入 `last_attempt_at` 和简短 `error`，但不要停止当前 batch。

如果用户可以在 Chrome 中解决或继续流程，使用 `needs_user`：

- CAPTCHA 或机器人验证。
- Google 登录缺失、过期或要求 2FA。
- Google 账号选择器中无法判断哪个是个人账号。
- 站点要求用户创建非 Google 账号。
- 站点要求浏览器权限。
- 表单要求 `public-submission-info.md` 中没有的公开联系信息。
- 表单要求私密个人信息。
- 用户必须在不清楚的付费或公开选项之间做选择。
- 有必填字段，但无法从可见标签判断含义。

如果当前计划无法提交该平台，使用 `failed`：

- 平台不是免费的。
- 平台不再接受提交。
- 直接打开 URL 后无法访问。
- 提交表单损坏，或拒绝有效项目数据。
- 平台要求用户未授权的非 Google 登录方式。

不要因为页面要求选择 Google 账号而失败。出现账号选择器时，默认选择第一个可见的个人 Google 账号继续；如果无法判断是否为个人账号或要求敏感授权，按 `needs_user` 记录原因后停止。

`needs_user` 和 `failed` 都必须：

- 把 `last_attempt_at` 设置为当前时间戳。
- 把 `error` 设置为一句简短原因。
- 停止处理后续队列项，直到用户给出新指令。
- 如果用户可以在 Chrome 中接手，保留当前 Chrome 标签页并告诉用户需要完成的动作。
