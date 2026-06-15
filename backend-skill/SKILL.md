---
name: backend-skill
description: 按 GoBackendFram 框架约定开发、配置、集成或审查 Go 后端功能.
---

# GoBackendFram

## 使用时机

用于 GoBackendFram 项目的功能开发、配置接入、部署集成、代码审查和排障。

## 强制前置

- **强制前置步骤1**：用户必须去 https://backend-deploy-ten-indol.vercel.app 选择 Go 语言并且选择 `gobackendframe` 模板，创建项目资源以及所需的数据库、Redis、OSS 资源。
- **强制前置步骤2**：用户创建完项目资源后，需自行 `git clone` 项目到本地，或者提供 git 地址让agent clone
- 本地仓库可用后，至少查看 `docs/readme.md`、`common/config/config.go`、`resource/resource.go`、`web/api/execute.go`、`web/router/router.go`、`injector/set.go`、`injector/wire.go` 和最接近的业务域。


## 主流程

1. 先定位最接近的已有业务域，沿用它的命名、分层、请求/响应形态、错误风格、事务和路由习惯。
2. 如果涉及配置，按 `common/config -> resource/config/<env>_config.toml -> APP_ENV/AES_KEY -> resource.ReadFile` 的链路处理。
3. 如果涉及持久化，先改 `docs/database/*.sql`，再补 ORM、DAO、service、API、router 和 Wire。
4. API 层只做适配，必须选择 `web/api/execute.go` 中匹配的 helper，让绑定、校验、事务、响应包装和日志走框架标准路径。
5. 新业务域要在 `web/router/<domain>.go` 增加 loader，并把 loader 接入 `web/router/router.go`。
6. 依赖注入改 `injector/set.go` 和 `injector/wire.go`；改完进入 `injector/` 执行 `wire`，不要手改生成文件。

## 配置要点

- 三份环境配置固定是 `resource/config/dev_config.toml`、`resource/config/stg_config.toml`、`resource/config/prd_config.toml`，分别由 `APP_ENV=dev|stg|prd` 选择。
- 本地默认读取 embed 资源；k8s 中如果存在 `/<SERVICE_NAME>/resource/...` 挂载文件，会优先读取挂载文件，失败才回退 embed。
- `AES_KEY` 是运行环境变量，用来递归解密 TOML 中的 `ENC(...)`；它不是 `[encrypt.aes].key`。后者是业务请求解密中间件使用的应用配置。
- `AES_KEY` 必须是 32 字符，并且必须与生成 `ENC(...)` 的 key 完全一致。不要把真实 `AES_KEY` 写进 TOML、代码、日志、提交记录或交付说明。
- 新增配置时必须同时补齐 `common/config` 结构、`Config` 中心结构、全局变量赋值、dev/stg/prd 三份 TOML，以及必要的 k8s ConfigMap/Secret 或挂载资源。
- 密码、token、支付密钥、OAuth/JWT key、OSS key、AI key、私钥等敏感值写入 TOML 前先用 `go run tools/aesencrypt/main.go` 加密为 `"ENC(...)"`。
- 如果生产配置为空、缺 key，或当前 `AES_KEY` 无法解密已有 `ENC(...)`，不要猜配置；说明需要向陈培侨获取对应环境的真实配置和 AES_KEY。

## 约束

- 不要自行 clone 仓库；仓库准备由用户完成，或用户提供本地仓库路径。
- 不要手动编辑 `injector/wire_gen.go`。
- 不要在没有本地完整 GoBackendFram 仓库的情况下继续实现、补全路径或编造框架结构。
- 不要绕过 `web/api/execute.go`，在 API 层临时拼 JSON 响应。
- 不要在 service 方法里使用 `*gin.Context`，除非这个方法确实强绑定 HTTP。
- 不要在 DDL 里创建外键、触发器、存储过程，除非用户明确要求并接受偏离框架惯例。
- 不要打印 TOML、环境变量、`AES_KEY`、支付密钥、OAuth 密钥或 `ENC(...)` 解密后的敏感信息。
- 不要提交真实账户密码；如果缺配置，说明需要向陈培侨获取，而不是填占位值冒充可用配置。
- 不要把无关重构混进功能开发或框架适配里。
