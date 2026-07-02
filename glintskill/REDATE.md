# GlintSkill 使用说明

这个仓库里目前包含三个 Codex skill：

- `project-profile-capture`：根据项目 URL 抓取项目资料，生成项目资料文件夹。
- `backlink-publisher`：读取外链 JSON 队列，用 Chrome 把项目提交到外链平台。
- `humanizer`：给外链发布文案去 AI 味，供 `backlink-publisher` 的 subagent 调用。

推荐使用顺序：

```text
先用 project-profile-capture 生成项目资料
再用 backlink-publisher 去发布外链
```

## 一键安装

直接复制这一条命令运行：

```bash
cd /Users/test/Documents/GlintSkill && mkdir -p ~/.codex/skills && rm -rf ~/.codex/skills/project-profile-capture ~/.codex/skills/backlink-publisher ~/.codex/skills/humanizer && cp -R skills/project-profile-capture skills/backlink-publisher skills/humanizer ~/.codex/skills/
```

安装后，新开一个 Codex 对话，或重启 Codex，让它重新读取 skill。

`project-profile-capture` 已经带可执行入口。普通用户直接运行 `bin/project-profile-capture`，不需要写 `python3`，也不需要安装 `requests` 或其他 Python 包。

当前仓库内置这些可执行文件时，入口会按平台自动选择：

```text
macOS Apple Silicon: skills/project-profile-capture/dist/project-profile-capture-Darwin-arm64
Intel Mac:           skills/project-profile-capture/dist/project-profile-capture-Darwin-x86_64
Linux x86_64:        skills/project-profile-capture/dist/project-profile-capture-Linux-x86_64
Linux arm64:         skills/project-profile-capture/dist/project-profile-capture-Linux-arm64
```

如果当前平台没有对应的可执行文件，入口会自动退回执行 Python 源脚本。

macOS 和 Linux 用户运行：

```bash
~/.codex/skills/project-profile-capture/bin/project-profile-capture --help
```

如果要重新打包当前平台，维护者运行：

```bash
./skills/project-profile-capture/scripts/build_standalone.sh
```

如果要在 macOS 上重新打包 Linux x86_64 和 Linux arm64，维护者运行：

```bash
./skills/project-profile-capture/scripts/build_linux_with_docker.sh
```

Windows 暂不内置可执行文件；在 Windows 上可以通过 Python fallback 运行源码脚本。

## 1. 抓取项目资料

这个步骤会根据项目 URL 生成一个项目资料文件夹，里面有项目介绍、Logo、首屏截图和原始抓取数据。

直接对 Codex 说：

```text
使用 $project-profile-capture 抓取 https://glypho.app，并保存到当前项目根目录。
```

也可以自己运行脚本：

```bash
~/.codex/skills/project-profile-capture/bin/project-profile-capture \
  https://glypho.app \
  --project-root "$PWD" \
  --overwrite
```

运行成功后，会生成类似这样的目录：

```text
glypho-ai-svg-generator/
|-- profile.md
|-- metadata.json
|-- raw-firecrawl.json
|-- logo.png
`-- screenshot.png
```

说明：

- `profile.md`：给人看的项目资料。
- `metadata.json`：给后续自动化流程读取的数据。
- `logo.png`：项目 Logo。
- `screenshot.png`：项目首屏截图。
- `raw-firecrawl.json`：Firecrawl 返回的原始数据，方便排查问题。

如果页面不是标准商品页，`product` 可能为空，这是正常情况。SaaS 落地页经常不会返回标准 product 数据。

## 2. 发布外链

这个步骤会读取外链队列，然后用 Chrome 打开外链平台，填写项目资料并提交免费 listing。

开始前确认三件事：

```text
1. 当前项目根目录里已经有项目资料文件夹，例如 glypho-ai-svg-generator/
2. data/backlinks/free-backlinks.json 已经准备好
3. public-submission-info.md 已经填写公开提交信息
```

Chrome 也要提前准备好：

```text
1. 打开 Chrome
2. 登录你的 Google 账号
3. 保持 Codex 可以操作 Chrome
```

然后对 Codex 说：

```text
使用 $backlink-publisher 为 glypho-ai-svg-generator 处理 data/backlinks/free-backlinks.json 里 pending 的外链。
```

`backlink-publisher` 会做这些事：

```text
1. 检查外链 JSON 格式
2. 读取项目资料文件夹
3. 读取 public-submission-info.md
4. 打开 Chrome 进入外链平台
5. 用项目资料填写表单
6. 需要文案时派 subagent 生成，并调用 $humanizer 去 AI 味
7. 免费 listing 可以直接提交
8. 成功后更新 JSON 状态为 submitted
9. 遇到付费、验证码、敏感权限或无法判断的问题，记录原因后跳过当前项并继续下一个
```

外链 JSON 可以先手动校验：

```bash
python3 ~/.codex/skills/backlink-publisher/scripts/validate_backlinks_json.py \
  data/backlinks/free-backlinks.json
```

## 常见问题

### Codex 找不到 skill

确认已经复制到：

```text
~/.codex/skills/project-profile-capture
~/.codex/skills/backlink-publisher
~/.codex/skills/humanizer
```

然后新开一个 Codex 对话，或重启 Codex。

### 提示缺少 humanizer

`backlink-publisher` 需要 `$humanizer` 来处理外链平台文案。如果 Codex 提示找不到 `$humanizer`，重新运行一键安装命令，或单独复制：

```bash
cp -R skills/humanizer ~/.codex/skills/
```

### Firecrawl 抓取失败

优先检查 `project-profile-capture` 源码顶部是否已经配置 Firecrawl key：

```python
HARDCODED_FIRECRAWL_API_KEY = "fc-..."
```

也可以临时用命令行传：

```bash
~/.codex/skills/project-profile-capture/bin/project-profile-capture \
  https://glypho.app \
  --api-key "fc-..." \
  --project-root "$PWD" \
  --overwrite
```

### 外链发布卡住

如果遇到这些情况，skill 会停下来让你处理：

- 验证码
- 付费页面
- 要求敏感权限
- Google 账号无法判断
- 表单字段和项目资料明显不匹配

你处理完之后，可以把对应队列项重置为 `pending`，再让 Codex 继续跑。

### 应该从哪里开始

最简单的完整流程是：

```text
1. 使用 $project-profile-capture 抓取项目 URL
2. 检查生成的 profile.md 和 screenshot.png
3. 填好 public-submission-info.md
4. 登录 Chrome 的 Google 账号
5. 使用 $backlink-publisher 发布 pending 外链
```
