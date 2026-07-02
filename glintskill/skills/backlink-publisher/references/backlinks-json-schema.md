# 外链 JSON schema

外链队列是 UTF-8 JSON 对象。批次发布的默认入口是 manifest：

```text
data/backlinks/foreign-backlinks-batches-manifest.json
```

manifest 不是队列 JSON，不能传给发布流程。实际执行时必须读取其中某一个兼容同一 schema 的批次队列 JSON。可执行 batch 默认放在 `data/backlinks/batches/`，例如：

```text
data/backlinks/batches/batch-001.json
```

旧单文件队列 `data/backlinks/free-backlinks.json` 只作为兼容入口：只有用户明确指定，或没有可用 manifest 时才使用。

大型候选池应拆成多个 batch JSON 逐组运行，推荐每组约 30 条。manifest 只用于记录批次顺序、数量和人工进度，不是队列 JSON，不能传给 `validate_backlinks_json.py` 或发布流程。`batch-*-submitted.json` 是已提交结果导出，不是执行队列。

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
- 如果运行的是批次 JSON，只更新当前批次文件；不要把状态同步回完整候选池或正式队列，除非用户明确要求。
- 处理完一个 batch 后先报告本批结果，不自动进入下一个 batch，除非用户明确要求继续。
- 开始操作平台前，先设为 `status: "in_progress"`。
- 只有看到成功提示、listing URL 或明确的提交成功页面后，才设为 `status: "submitted"`。
- 如果用户可以在 Chrome 中继续或解锁当前流程，设为 `status: "needs_user"`。
- 如果当前信息和策略无法完成平台提交，设为 `status: "failed"`。
- `needs_user` 和 `failed` 都必须写入简短 `error`。
- 运行中把当前项设为 `needs_user` 或 `failed` 后，立即停止本轮任务；不要继续处理下一个 `pending` 项，除非用户明确要求跳过并继续。
- 如果之前因为缺少公开联系信息或多 Google 账号选择器被跳过，修正规则后可以重置为 `pending`，并清空 `last_attempt_at`、`result_url` 和 `error`。

## manifest 规则

- `total_items` 必须等于 manifest 中所有可执行 batch 的实际 `items.length` 之和。
- 每个 batch 的 `item_count`、`first_id`、`last_id` 必须和对应 batch JSON 的实际内容一致。
- 选择下一个 batch 时，以实际 batch JSON 中是否存在 `status: "pending"` 为准，不要只看 manifest 的 `status`。
- 已经没有 `pending` / `in_progress` 项的 batch，在 manifest 中标记为 `processed`。
