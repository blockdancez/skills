# 输出契约

默认输出目录是 `<project-root>/<project-slug>/`。`project-slug` 的生成优先级为：

1. `product.title`
2. `metadata.title`
3. `metadata.ogSiteName`
4. URL 域名

资料文件夹应包含：

```text
<project-slug>/
|-- profile.md
|-- metadata.json
|-- raw-firecrawl.json
|-- logo.<ext>
`-- screenshot.<ext>
```

当 Firecrawl 没有返回 Logo URL，或图片主机拒绝下载时，`logo.<ext>` 可以缺失。当 Firecrawl 没有返回截图 URL，或截图 URL 无法下载时，`screenshot.<ext>` 可以缺失。缺失资产必须写入 `metadata.json` 的 `warnings`。

## metadata.json

写入 UTF-8 JSON，并包含：

- `source_url`
- `resolved_url`
- `project_name`
- `project_slug`
- `captured_at`
- `summary`
- `metadata`
- `branding`
- `product`
- `assets.logo_url`
- `assets.logo_path`
- `assets.screenshot_url`
- `assets.screenshot_path`
- `warnings`

## profile.md

写入面向人阅读的 Markdown，并包含：

- 项目名、原始 URL、解析后 URL、抓取时间
- 网站 summary
- 页面 metadata description 和 Open Graph 字段
- Logo URL 与本地 Logo 路径
- 截图 URL 与本地截图路径
- product title、brand、category、description
- variant price、original price、availability、image URLs
- 页面 markdown 摘录
- warnings
