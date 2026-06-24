---
name: project-profile-capture
description: 使用 Firecrawl 根据用户提供的项目落地页或产品 URL 抓取并保存本地项目资料文件夹。用于需要 Codex 获取网站摘要、页面 metadata、品牌 Logo、首屏截图和结构化 product 字段，并在当前项目下保存 profile.md、metadata.json、raw-firecrawl.json 和下载后的图片资产。
---

# 项目资料抓取

## 概览

为一个项目 URL 创建可复用的本地资料文件夹。可执行入口会调用已打包的抓取程序，访问 Firecrawl，立即下载 Logo 和首屏截图，并写入面向人阅读的 `profile.md` 与面向程序读取的 `metadata.json`。

## 工作流

1. 要求用户提供项目落地页 URL 或产品 URL。
2. 在希望保存项目资料的工作区运行可执行命令：

```bash
/Users/test/Documents/GlintSkill/skills/project-profile-capture/bin/project-profile-capture \
  <url> \
  --project-root "$PWD"
```

3. 只有当用户明确指定输出位置时，才使用 `--output-dir <path>`。
4. 只有当用户明确要覆盖已有资料文件夹时，才使用 `--overwrite`。
5. 如果用户希望把 Firecrawl key 写在源码里，编辑 `scripts/capture_project_profile.py` 顶部的 `HARDCODED_FIRECRAWL_API_KEY = "fc-..."`，然后由维护者重新打包。`--api-key` 参数仍然会优先覆盖源码内的 key。
6. 普通用户运行 `bin/project-profile-capture`，不需要输入 `python3`，也不需要安装 Python 包。
7. 如果没有配置 key，也可以继续运行；Firecrawl 可能会允许低额度未认证请求，也可能拒绝。
8. 结束时向用户返回 `profile.md`、`metadata.json`、Logo、截图路径，以及所有 warnings。

## 脚本约定

脚本接口：

```bash
bin/project-profile-capture <url> \
  --project-root <path> \
  --output-dir <path> \
  --api-key <key> \
  --overwrite
```

默认输出目录是 `<project-root>/<project-slug>/`。`project-slug` 的来源优先级为：`product.title`、`metadata.title`、`metadata.ogSiteName`、URL 域名。

`bin/project-profile-capture` 会自动查找 `dist/project-profile-capture-<系统>-<架构>`，例如 macOS Apple Silicon 使用 `dist/project-profile-capture-Darwin-arm64`，Intel Mac 使用 `dist/project-profile-capture-Darwin-x86_64`，Linux x86_64 使用 `dist/project-profile-capture-Linux-x86_64`。如果当前平台没有对应二进制文件，入口会自动退回执行 `scripts/capture_project_profile.py`。

如果目标机器没有对应二进制文件，维护者需要在同类机器上运行：

```bash
./skills/project-profile-capture/scripts/build_standalone.sh
```

Linux 版本可以用 Docker 在 macOS 上构建：

```bash
./skills/project-profile-capture/scripts/build_linux_with_docker.sh
```

Windows 暂不内置可执行文件；在 Windows 上可以通过 Python fallback 运行源码脚本。

## 输出

资料文件夹包含：

```text
<project-slug>/
|-- profile.md
|-- metadata.json
|-- raw-firecrawl.json
|-- logo.<ext>
`-- screenshot.<ext>
```

修改输出结构前，先阅读 `references/output-contract.md`。修改 Firecrawl 请求格式或失败处理前，先阅读 `references/firecrawl-scrape.md`。

## 失败处理

- Firecrawl 请求失败是阻塞错误，需要报告具体 HTTP/API 错误。
- `product` 数据缺失只是 warning，不算抓取失败。
- Logo 或截图下载失败时，如果其他资料已经可保存，则记录 warning 并继续。
- 截图只抓第一屏，不抓完整长页面。
- 不要同时启用 Zero Data Retention 和截图；Firecrawl 不支持这个组合。
