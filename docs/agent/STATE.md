# 下载站交接记忆

- 日期：2026-10-31（Asia/Shanghai）。用户明确授权发布独立新版官网及在线更新入口，并要求每次推送/发布更新记忆。
- 仓库：`pkokwho/duoge-download`，分支 `main`。阶段 1 包文件提交 `48334a7` 已推送；源码交接规则/授权提交：`pkokwho/duoduo-parkour@029b432`；游戏功能提交 `25a2851`。
- 发布内容提交 `88d1fec` 已推送并成功部署：首页、备用下载和 `release.json` 已提升到独立新版；独立清单 `update-standalone.json` 已发布。Pages 运行 `41156020066` 对 `88d1fec` 显示 Success（https://github.com/pkokwho/duoge-download/actions/runs/41156020066）。本次仅回写实际发布证据，不改安装包/页面/清单。
- 目标版本：`0.1.5-dev` / 6，独立包名 `org.duoge.parkour.standalone`，应用名“舵哥快跑（新版）”。Android 10+ / ARM64，55,017,643 字节。
- 文件：`downloads/duoge-parkour-0.1.5-dev-arm64-standalone.apk`。
- APK SHA-256：`dcbd7d776368a0770a224170b3f4ed7e75ebb725a746b7ff06594642189d6f51`。
- 签名证书 SHA-256：`05bfb8a25e259e4d7a63bae05dc347e28523e8197e79afa84d82414b65c4e88d`。本站仅发布安装包和公开元数据，绝不发布签名私钥/备份。
- 已有验证：签名、ZIP CRC/重复条目、16KiB 对齐、原生插件/Provider、图标、游戏冒烟及双通道回归通过。发布 JSON 用实际客户端验证当前公告/升级/SDK/旧包拒绝通过；Chromium 360×800 与 1280×900 页面下载、安装提示、资源响应、无 JS 错误/横向溢出检查通过。真机试装未执行，不得标为通过。
- 保留 `update.json` 的 0.1.4 原包名渠道和全部旧包；将新增 `update-standalone.json` 供独立新版检查更新。新版不自动继承旧纪录；旧游戏/旧纪录保留，不要求卸载。
- 远端证据：公开 Raw APK 完整下载后大小、SHA 和签名一致；远端实际 `update-standalone.json` 与发布文件一致；`88d1fec` 的远端首页与本地发布页面逐字节一致。阶段 1 Pages 运行 `41155569168` 也成功。直接官网 CDN HTTP 仍被开发环境策略拦截，不能说已直接核验 CDN。
- 公开入口：https://pkokwho.github.io/duoge-download/ ；https://pkokwho.github.io/duoge-download/update-standalone.json 。官网默认包为独立版；未来升级沿用独立签名。旧 `update.json` 及全部旧 APK 保留不变，元数据归档为 `release-0.1.4.json`、`download-routes-0.1.4.json`。
- 下一步：同步源码仓库 STATE/发布记录；如用户反馈安装问题再做真机诊断。以后每次推送/发布继续更新记忆。不要擅自重签现有包、混用更新通道或修改已发布的不可变 APK。
- 云环境当前不允许直接 HTTP 访问官网域名，已保存必要域名的开发环境网络草稿但未应用。不得绕过策略；可以核对 GitHub 仓库实际对象，直接官网 HTTP 仍需单独确认。

## 错误与注意

- Git 推送不是 Pages 部署成功的证据；Raw 校验也不是官网 CDN 已刷新证据。
- GitHub 托管的不同入口不能承诺中国大陆高速；没有实际手机测速就标为未验证。
- 必须区分独立安装和覆盖升级，避免旧版客户端下载错误包。
