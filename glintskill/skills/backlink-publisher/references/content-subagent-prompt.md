# 内容 subagent prompt

只要平台要求生成 tagline、summary、description、launch pitch、分类理由、founder note 或评论文本，就启动 fresh subagent。

发送给 subagent 的 prompt 使用这个结构：

```text
你正在为一个外链平台提交生成 listing 文案。

先阅读这些项目资料文件：
- <profile.md 的绝对路径>
- <metadata.json 的绝对路径>
- <public-submission-info.md 的绝对路径>

返回最终文案前，必须使用 $humanizer，路径是 /Users/test/.codex/skills/humanizer/SKILL.md。先生成草稿，再去 AI 味，最后只返回平台需要的最终字段值。

平台：
- 名称：<platform_name>
- URL：<platform_url>
- 需要字段：<页面可见的字段名和长度限制>
- 页面显示的受众或分类线索：<如果有就填写>

规则：
- 除非主 agent 提供额外事实，否则只使用项目资料中的事实。
- 公开邮箱、联系人姓名、公司所在地、成立时间、Founder、社交账号等字段只能来自 `public-submission-info.md` 或主 agent 明确提供的信息。
- 文案要自然、具体。
- 避免 emoji、em dash、en dash、聊天机器人式开场、夸大宣传和无依据指标。
- 不要操作浏览器。
- 不要提交任何内容。
- 默认用英文生成对外提交文案，除非平台或用户明确要求其他语言。

只返回 JSON：
{
  "fields": {
    "tagline": "...",
    "description": "...",
    "category": "..."
  },
  "notes": "任何不确定或缺失的事实。"
}
```

主 agent 负责把返回字段映射到浏览器表单。如果 subagent 对必填字段报告不确定，停止并向用户索取该事实。
