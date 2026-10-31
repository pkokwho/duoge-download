# 下载站交接记忆

- 日期：2026-10-31（Asia/Shanghai）。仓库 `pkokwho/duoge-download` / `main`；源码 `pkokwho/duoduo-parkour` / `master`。每次推送/发布均须更新两仓库相应记忆，区分推送、部署与实际 HTTP 核验。
- 用户已授权测试正常后部署，现回复“都正常”，确认 0.1.6 手机安装/配色正常。发布条件已满足，无需重复索取许可。该反馈不等于全部设备、性能、旧版存档迁移或大陆测速通过。

## 当前发布：0.1.6-dev 正式入口提升

- 版本 0.1.6-dev / 7，包名 `org.duoge.parkour.standalone`，名称“舵哥快跑（新版）”；ARM64 / Android 10+，API 29/36。
- APK：`downloads/duoge-parkour-0.1.6-dev-arm64-standalone.apk`，55,115,947 bytes（52.6 MiB）。复用手机确认的原测试包，不重构/重签/覆盖已发布文件。
- SHA-256：`047d88d122231a8538223dc107b1e0d978bfb80da389aae797fec4c995c506e4`。
- 证书 SHA-256：`05bfb8a25e259e4d7a63bae05dc347e28523e8197e79afa84d82414b65c4e88d`，与 0.1.5 相同，可直接更新该独立版。私钥/备份绝不上传本站或源码。
- 修复：14 个模型恢复原始顶点颜色，保留几何、玩法、角色动作。源码功能修复 41ef962，公开测试交接 70cabed。证据见源码 docs/verification/0.1.6/README.md。
- 本次从 main=54a094f 提升首页、备用下载、release.json、download-routes.json、update-standalone.json；公告写明白模修复、配色恢复、保留玩法动作与独立安装边界。测试页同步“已转为默认版本”。历史 0.1.5 元数据新增归档 release-0.1.5.json / download-routes-0.1.5.json。
- 推送前通过：清单/所有当前下载链接与真实 APK 的版本、大小、SHA 一致；真实 0.1.5 客户端可识别升级，真实 0.1.6 可显示当前修复公告；SDK、错误包名、禁止降级检查通过。Chromium 360×800、1280×900 首页/备用页链接及公告正确，无横向溢出或 JS 错误。
- 实际正式发布提交 `3506214` 已成功推送（54a094f→3506214）；Pages https://github.com/pkokwho/duoge-download/actions/runs/41173088826 对 3506214 已观察到 Success。远端首页/备用页/release/routes/新旧更新清单与本地逐字节一致；对远端真实清单的 .5/.6 客户端验证通过。本记忆提交仅回写成功证据，不改变已部署产品内容。下一步同步源码记忆并向用户报告完成；当前交接提交可用 git log -1 查看。

## 入口与更新边界

- 官网：https://pkokwho.github.io/duoge-download/
- 独立游戏内更新：https://pkokwho.github.io/duoge-download/update-standalone.json
- 备用下载：https://pkokwho.github.io/duoge-download/download-lines.html
- 专用测试下载：https://pkokwho.github.io/duoge-download/test-0.1.6.html
- 原包名 `org.duoge.parkour` 的 `update.json` 保持 0.1.4；所有旧 APK 保留。原版与独立新版并存，旧纪录保留但不自动导入，不要求卸载。
- 原 0.1.4 私钥缺失，无法提供同签名覆盖升级；旧版游戏内更新目标仍未解决。不能伪造包名、版本或签名让旧客户端接受独立包。
- 云环境 HTTP 仍限制直接访问官网 CDN 和 GitHub API；运行时观察 enforced，官网不在允许域名。使用 GitHub/Raw/Actions 验证，不能冒充直接 CDN 实测；网络配置草稿未应用。

## 已完成的测试发布与历史证据

- 0.1.6 APK/测试页上传 `26558cad363fce6e2ae7f98b3586ada1452ee057`，记忆回写 `54a094f`。Raw 完整下载 HTTP 200，大小/SHA/签名核对通过。
- 测试 Pages https://github.com/pkokwho/duoge-download/actions/runs/41161142852 对 26558ca 显示 Success；随后用户在手机确认“都正常”。
- 历史 0.1.5：资产 48334a7，正式页面/独立清单 88d1fecc869a658babe796494aef9a3846452d3e，交接 518baee；Pages 41155569168、41156020066、41156243455 均 Success。该版遗漏颜色是已确认问题，.6 已修复，旧 APK 保留。

## 错误教训

- 工作区路径无法作为手机可用下载；先发布独立测试链接，再要求手机确认，可晚于它提升正式清单。
- 无窗口/签名/CRC 不证明画面正常；资源恢复要检查 COLOR_0 和实际导出包渲染。
- Git 推送不是 Pages 成功；Raw 校验不是 CDN 已刷新。没有手机测速就不承诺大陆高速。
- 遇到本地稀疏检出新 APK，使用 git add --sparse 显式暂存；不要为了消除警告引入私钥或改用占位 LFS 文件。

## 0.1.7 双角色公开测试（正式入口仍 .6）

- 用户授权只做双角色/选角预览/记住选择，并移除常驻金色脚下光环；整体UI重做延期。按既有流程先提供公开手机测试下载，确认后再提升正式入口。原.6安装/配色反馈不等于.7手机验证。
- 源码功能提交 affd36e（master + feat/dual-characters）；新模型由 f9f0881 提供，已独立绑骨/烘焙四动作，原舵哥和校园资源/玩法/计分不变。选角偏好单独存 characters.cfg，不改成绩。源/实际APK双轮回归及Mobile/OpenGL实际渲染通过，证据见源码 docs/verification/0.1.7 与 DUAL-CHARACTERS.md。
- 测试APK downloads/duoge-parkour-0.1.7-dev-arm64-standalone.apk：.7/code8，org.duoge.parkour.standalone，62,080,826 bytes（59.2MiB），SHA cd9c982ca39e3ef1935d70adbcb9f084827bab9d60745668602006c1be1012f5，证书继续05bfb8a...同一独立签名。可直接更新.5/.6独立版；原.4边界不变。
- 仅新增已签名APK/SHA、test-0.1.7.html 和选角截图；基线main=18c847f。正式首页/release/routes/update-standalone.json保持.6，旧update.json和所有旧APK不变。测试上传提交 bf5246840adb91c568ee6a503d5c8d7a6bfbaf2c 已推送（18c847f→bf52468）；远端公开APK完整下载HTTP200，大小/SHA/签名一致，远端测试HTML逐字节一致。Pages https://github.com/pkokwho/duoge-download/actions/runs/41178787480 标题对应bf52468，已观察到Success。本提交只回写真实证据；云环境仍未直接核验官网CDN内容。
- 手机链接目标 https://pkokwho.github.io/duoge-download/test-0.1.7.html ，备用为Raw main/downloads/下同名APK。只发布公开产物，不发布私钥/备份/authoring文件；每次推送/发布同步记忆。

- .7测试页本地Chromium360×800和1280×900检查下载链接、实际包截图加载、无横向溢出/JS错误通过。手机.7体验尚未反馈，正式入口保持.6；下一步让用户试选角、跑跳滑铲与重启记忆，正常后再按授权提升正式入口并同步记忆。

## 自动镜像草稿：账号路线暂停，不改生产

- 用户已授权程序开源/自动分发，但随后表示注册授权太复杂、已疲惫。当前无需用户回答任何注册、邮箱、授权问题；不再催促注册新平台。SourceForge账号路线暂停，速度问题仍未解决。
- 本分支feat/automatic-download-mirrors基于main=e167015，保存已测试发布器/模板：本公开库适合作公开Release目标；源码库匿名网页404，不当作公开附件下载源。
- .6/.7的程序源码ZIP已按白名单生成（69/76文件，约80/89KB），带MIT/NOTICE/来源commit，不含美术/肖像、私有历史、内部agent记录或私钥；用户明确接受代码开源，因此可在本公开草稿分支保存，非安装包重新构建。
- distribution/releases.json冻结现有APK/源代码包身份；内置GITHUB_TOKEN自动发布设计无需额外SSH密钥。SourceForge官方Github Integration仍须账号本人一次授权，当前未创建账号、未启用config、没有已验证SourceForge镜像链接。
- 分发器7项单测、实际.6/.7 APK与代码ZIP预检通过；UI语法及正确文件/哈希/域名护栏通过。这里只是非默认分支草稿，main-only工作流不运行、Pages不部署；不是成功发布证据。
- 现有main首页、release/routes、update-standalone.json/.4 update.json、所有旧APK均保持原样。SourceForge disabled，mirror-links为空，新网页挂点隐藏；主下载不切换，不宣称大陆速度改善。
- 后续仅在用户主动恢复此路线后再处理必要授权/验证，或寻找真正可测试且无需新账号的路线；不得把用户之前的开放授权当作可以擅自替其完成邮箱/OAuth/人机验证。
