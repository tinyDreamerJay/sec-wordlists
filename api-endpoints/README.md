# api-endpoints 字典

## 来源

整理自 SecLists `Discovery/Web-Content/api/api-endpoints.txt` 与 `api/api-seen-in-wild.txt`，
补充常见版本前缀（`api/v1/`、`api/v2/`、`api/internal/`、`api/admin/`）与文档、健康检查、
Spring Actuator 路径，去重后共 7930 行，截断 20000 行以内。

## 适用方位

用于接口面直打：找未授权接口、旧版本接口、内部接口与调试端点、Swagger/OpenAPI 文档。
判据看 200 与 `application/json` 响应、401/403 说明接口存在但需鉴权、405 说明方法不符但路径有效，
以及错误体结构（统一 JSON error 与框架默认页）识别后端技术栈；实际项目里从目标 JS 里 grep 路径命中率最高。