# Firecrawl 抓取说明

对单个项目 URL 使用 `POST https://api.firecrawl.dev/v2/scrape`。

## 认证

- 如果调用命令提供了 `--api-key`，优先使用它。
- 如果用户明确要求把 key 写在脚本里，在 `scripts/capture_project_profile.py` 中设置 `HARDCODED_FIRECRAWL_API_KEY = "fc-..."`。
- 否则读取环境变量 `FIRECRAWL_API_KEY`，并用 `Authorization: Bearer $FIRECRAWL_API_KEY` 请求。
- 没有 key 时仍允许发起未认证请求；Firecrawl 可能降低额度或直接拒绝。
- 不要把 API key 写入生成的项目资料文件。

## 请求格式

默认一起请求这些 formats：

```json
["markdown", "summary", "branding", "product", {"type": "screenshot", "fullPage": false}]
```

- `markdown`：清洗后的页面正文，用于 `profile.md` 摘录。
- `summary`：网站摘要。
- `branding`：品牌信息，包括 `branding.logo` 和 `branding.images.logo`；脚本也会 fallback 到 favicon / ogImage。
- `product`：确定性 product 抽取，包含 title、brand、category、description、variants、price、sale、availability、images。
- `screenshot`：只抓第一屏截图。保持 `fullPage` 为 `false`，并立刻下载返回的签名截图 URL，因为截图 URL 会过期。

## Product 处理

Firecrawl 的 product 抽取是 fail-closed。页面没有明确 product 结构时，响应可能不包含 `product`，或只返回 warning。此时保存其他资料，并在本地 `warnings` 中记录，不要把整次抓取判定为失败。

## 截图处理

截图与 Firecrawl Zero Data Retention 不兼容，因为截图需要上传到持久存储。这个 skill 不要设置 `zeroDataRetention: true`。
