# 外链 JSON schema

外链队列是 UTF-8 JSON 对象。默认路径：

```text
data/backlinks/free-backlinks.json
```

## 根字段

- `version`：整数。当前值：`1`。
- `default_login_method`：字符串。当前值：`"google"`。
- `requires_logged_in_chrome`：布尔值。当前值：`true`。
- `submit_policy`：字符串。当前值：`"auto_submit_free_listings"`。
- `items`：外链任务对象数组。

队列只保留仍值得自动尝试的免费外链平台。站点不可访问、证书异常、Cloudflare SSL 错误、域名停放/出售、跳转到无关内容、明确只提供付费/广告/赞助入口的条目，应该从队列移除，而不是保留为 `pending`。

## 队列项字段

每个队列项必须包含：

- `id`：稳定的小写 slug，在文件内唯一。
- `platform_name`：人类可读的平台名称。
- `url`：绝对 `http` 或 `https` URL。
- `free`：布尔值。本队列使用 `true`。
- `status`：只能是 `pending`、`in_progress`、`needs_user`、`submitted`、`skipped`、`failed`。
- `login_method`：字符串。除非用户明确要求其他方式，否则使用 `"google"`。
- `notes`：字符串。
- `last_attempt_at`：`null` 或 ISO 8601 时间戳字符串。
- `result_url`：`null` 或绝对 `http` / `https` URL。
- `error`：`null` 或简短错误字符串。

## 更新规则

- 保持队列项顺序稳定。
- 除非用户明确纠正，否则不要修改 `url`。
- 开始操作平台前，先设为 `status: "in_progress"`。
- 只有看到成功提示、listing URL 或明确的提交成功页面后，才设为 `status: "submitted"`。
- 如果用户可以在 Chrome 中继续或解锁当前流程，设为 `status: "needs_user"`。
- 如果当前信息和策略无法完成平台提交，设为 `status: "failed"`。
- `needs_user` 和 `failed` 都必须写入简短 `error`。
- 如果之前因为缺少公开联系信息或多 Google 账号选择器被跳过，修正规则后可以重置为 `pending`，并清空 `last_attempt_at`、`result_url` 和 `error`。
