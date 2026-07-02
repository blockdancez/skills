# Chrome 工作流程

操作浏览器时必须使用 Chrome 插件。这个 skill 不使用其他浏览器自动化能力。

## 初始化

- 按 `@chrome` skill 的说明连接浏览器。
- 打开或接管标签页前，先命名浏览器会话。
- 使用用户现有 Chrome profile 和已经登录的 Google 账号。
- 如果出现 Google 账号选择器，默认选择第一个可见的个人 Google 账号。不要选择明显属于公司、学校或管理型组织的账号；如果无法判断是否为个人账号，按失败处理策略把当前项标记为 `needs_user` 并写入原因，然后停止让用户接手。
- 不要检查 cookies、local storage、已保存密码或浏览器 profile 文件。

## 单个平台流程

1. 打开队列项的 `url`。
2. 从可见页面中识别公开提交路径，例如 submit、add、suggest、list、post、launch 或 contact form。
3. 优先依据可见页面状态和表单标签操作，不要依赖 DOM 源码顺序。
4. 用项目资料填写事实字段：
   - 项目名称
   - 项目 URL
   - tagline 或一句话描述
   - 详细描述
   - 分类
   - logo 路径
   - screenshot 路径
5. 用 `public-submission-info.md` 填写公开联系字段：
   - 联系邮箱
   - 联系人姓名
   - 公司所在地
   - 成立时间
   - Founder 姓名、X/Twitter、LinkedIn、GitHub 等可选字段
6. 缺少营销文案时，通过内容 subagent 生成。主 agent 不直接编写长文案。
7. 只上传所选项目资料夹中的项目资产。
8. 必填字段完成后，直接提交免费 listing 表单。
9. 记录成功信号：成功提示、提交后的 listing URL、确认页面或当前 URL。

## 直接提交授权

用户已授权本队列中的免费公开项目 listing 直接提交。该授权只覆盖项目资料和项目资产。

用户也授权在免费 listing 流程中使用现有 Google 登录状态。如果站点要求 `Continue with Google`，可以选择第一个可见的个人 Google 账号继续。

遇到付费、敏感个人数据、非项目文件、浏览器权限、非 Google 账号创建，或 listing 之外的权限授权时，提交前必须中止当前项，按失败处理策略记录原因，然后停止让用户接手。

## 标签页清理

按照 Chrome 插件说明清理标签页。触发停止规则时必须保留当前标签页，让用户能接手阻塞流程或查看页面状态。
