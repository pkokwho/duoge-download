# 下载站交接记忆

- 日期：2026-10-31（Asia/Shanghai）。仓库 `pkokwho/duoge-download` / `main`；源码 `pkokwho/duoduo-parkour` / `master`。每次推送/发布均须更新两仓库相应记忆，区分推送、部署与实际 HTTP 核验。
- 用户已授权测试正常后部署，现回复“都正常”，确认 0.1.6 手机安装/配色正常。发布条件已满足，无需重复索取许可。该反馈不等于全部设备、性能、旧版存档迁移或大陆测速通过。

## 当前发布：0.1.19-dev / 22（2026-11-06，最新）

- 内容：修复部分手机排行榜传不上去（弱网下超时 8→20 秒、失败退避重试 2 次、上传改后台、
  失败时显示具体原因）。源码记录见 `docs/releases/0.1.19.md`。
- APK `downloads/duoge-parkour-0.1.19-dev-arm64-standalone.apk` 与 `downloads/duoge-parkour-latest.apk`：
  61,370,829 B，SHA-256 `41315de1762ead5b191fe72d390a14a32fe89189b2e8a7a9057fd55658ad5c0a`；
  证书 `d6105f4e…` 未变，versionCode=22，可直接覆盖安装。
- 提交 `42d9bc2` 已 push main：新增命名包与 `.sha256`、替换 latest、提升 `update-standalone.json` 到 code 22、
  更新 `index.html` / `download-lines.html` / `release.json` / `download-routes.json`。旧包名 `update.json` 仍 code 16。
- 按上次约定删除 0.1.17 命名包；站点体积 **360.4 MB**（低于 Pages 1 GB）。**下次发版应删 0.1.18。**
- 核验：Pages **built**；加速节点完整下载线上 APK **逐字节一致**；
  两条清单用发布版 `validate_manifest` 跑 **26 项断言全通过**（code 19/20/21 可更新、22 为 current）。
- 手机真机安装与游戏内更新流程仍未验证。

## 历史：0.1.18-dev / 21（2026-11-06）

- 用户 2026-11-06 明确要求「再发布新版、更新下载官网、旧版本自动检查更新」。源码记录见
  `pkokwho/duoduo-parkour` `docs/releases/0.1.18.md`。
- APK `downloads/duoge-parkour-0.1.18-dev-arm64-standalone.apk` 与 `downloads/duoge-parkour-latest.apk`：
  61,370,829 B（58.5 MiB），SHA-256 `69fa00d92ad1284a870993ad88b8244493087460ef24e9c73cbc4535b260d92d`；
  证书 `d6105f4e…` 未变，versionCode=21，可直接覆盖安装。
- 提交 `439acba` 已 push main：新增命名包与 `.sha256`、替换 latest、提升 `update-standalone.json` 到 code 21、
  更新 `index.html` / `download-lines.html` / `release.json` / `download-routes.json`。旧包名 `update.json` 仍 code 16。
- 核验：Pages **built**；Raw 命名包完整下载 61,370,829 B 与签名包逐字节一致；
  两条线上清单用发布版 `validate_manifest` 跑 **26 项断言全通过**（code 18/19/20 可更新、21 为 current）。
- 站点体积 **360.4 MB**（低于 Pages 1 GB）。本次保留 0.1.17 命名包一个周期，**下次发版应删除 0.1.17**。
- 手机真机安装与游戏内更新流程仍未验证。

## 历史：0.1.17-dev / 20（2026-11-05）

- 用户 2026-11-04 23:33 明确授权发布新版、更新下载官网、让旧版本自动检查更新可用；并确认「加速节点 + GitHub 官网」「FALLBACK_APK_URL 一并改到新版」「源码本地 commit + push 下载仓库」。
- 源码发布记录见 `pkokwho/duoduo-parkour` `docs/releases/0.1.17.md`。APK `downloads/duoge-parkour-0.1.17-dev-arm64-standalone.apk` 与 `downloads/duoge-parkour-latest.apk`：61,350,021 B（58.5 MiB），SHA-256 `4b829ab844cefc81bd855d8507c96b4d87529bb8c05ab5c9afc200ec9d5937f9`；证书 `d6105f4e…` 未变。
- 阶段 1 提交 `a118e77` 已 push main，仅含签名 APK / SHA / latest；Raw 完整下载大小与 SHA 已核验，先于页面提升。
- 阶段 2 提交提升 `index.html`、`download-lines.html`、`update-standalone.json`、`download-routes.json`、`release.json` 到 code 20；旧包名 `update.json` 仍为 0.1.13-dev / code 16，未混入独立新版。
- 加速节点（WorkBuddy 托管 `publish-download/`）已部署，主清单 code 20、页面 0.1.17-dev、完整下载线上 APK 与签名包逐字节一致。两条更新线路一致后，code 17/18/19 客户端可判定可更新，code 20 判 current。
- 注意：会话恢复曾把本地工作区回滚到发布前，线上部署与 Git push 仍持久；已按线上核验过的 APK 重建本地副本后再提交。接手须重新 `git status` / 线上核验，不要只信本地快照。
- Pages 推送后曾为 building（CDN 仍返回 0.1.13-dev）；随后 `gh api .../pages/builds/latest` 显示 `6a23f10` **built**，线上 Pages 备用清单与首页实测 code 20 / 0.1.17-dev / 新 SHA，用该清单复跑旧版更新判定 22 项全通过。以下各节为历史记录，不代表当前版本。

## 历史发布：0.1.13-dev / 16（2026-11-03）

- 本次更新源码发布记录见 `pkokwho/duoduo-parkour` `docs/releases/0.1.13.md`；发布提交 `7688ed3`。
- APK：`downloads/duoge-parkour-0.1.13-dev-arm64-standalone.apk` 与 `downloads/duoge-parkour-latest.apk`，61,230,439 B（58.4 MiB）。
- SHA-256：`947461d55898b6d9c38f1b6270d673d0c89f1aab8fffd1ca1de8104a79ff8516`；证书 `d6105f4e…` 不变。
- 首页、备用页、`update.json`、`update-standalone.json` 已升至 0.1.13-dev / code 16；旧 APK 与历史页面保留。本段之前的内容为历史记录，不代表当前版本。

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

## 2026-10-31 状态核对与镜像方案中止（必须先看）

- 下载慢仍未解决；此前百度/蓝奏/SourceForge建议均没有完成新的高速分发验证，不能称作成功方案。用户明确不想再注册、提供邮箱或授权，已感到疲惫和愤怒；不要重复这些操作请求，也不要继续引入未经验证的平台。
- 0.1.7双角色APK已公开测试发布：bf52468 / Pages41178787480 Success，测试页 https://pkokwho.github.io/duoge-download/test-0.1.7.html 。本次再次完整下载Raw APK为HTTP200，62,080,826 bytes及SHA cd9c982ca39e3ef1935d70adbcb9f084827bab9d60745668602006c1be1012f5一致。
- 正式默认下载/独立游戏内更新仍为0.1.6(code7)，原update.json仍0.1.4；未将0.1.7提升为正式默认更新，不把公开测试发布与正式提升混为一谈。没有0.1.8或其他新APK发布。
- 新分发工具、MIT范围声明、代码ZIP和隐藏镜像入口只在非默认分支feat/automatic-download-mirrors@e7f494b保存，未合并main/未部署/未提供SourceForge链接；账号配置disabled，没有创建SourceForge账号或项目。
- 源码master交接022fe8c已撤下活动镜像workflow，保留template；这些镜像尝试未改动游戏脚本/模型/场景/现有APK。原签名和已完成双角色功能保留。
- 本提交只给main补上此前仅草稿分支记录的中止状态与版本事实，安装包/页面/清单不改。以前main=e167015；当前交接提交用git log -1读取。后续接手先梳理现状，不要求用户重复上述流程；速度未解决必须直说。

## Supabase 探活工作流（2026-11-06，提交 `72bda5a`）

- 文件 `.github/workflows/supabase-keepalive.yml`。目的：Supabase 免费项目连续 7 天无请求会被暂停。
- 每天 UTC 01:00（北京 09:00）请求 `https://iqhbawtwwvgwotxvqjwz.supabase.co/rest/v1/lb_top?select=rank&limit=1`，
  用公开 key（本就随 APK 分发，非机密）。失败会显式 fail 并提示需到后台恢复。
- 每月 1 号向 `keepalive` 分支强制推一个孤立空提交，规避 GitHub「仓库 60 天无提交停用定时任务」；
  只推非默认分支，**不触发 Pages 重建**，main 不受影响。
- 实测（run `42062594916`，手动触发带 `heartbeat=true`）：探活 `HTTP 200`、body `[]`；心跳生成
  `refs/heads/keepalive` = `c8bd1c6`，main 仍为 `72bda5a`。
- 若 60 天后仍被停用，用 `gh workflow enable supabase-keepalive.yml` 重新启用；**它只能防暂停，不能救暂停**，
  真被暂停必须登录 Supabase 后台手动恢复。

## 站点瘦身（2026-11-06，提交 `a2f4d40`）

- 起因：站点内容 1.16 GB，超 GitHub Pages 1 GB 限制，继续加版本可能构建失败。
- 保留 4 个文件（约 166 MB）：`duoge-parkour-latest.apk`、`duoge-parkour-0.1.17-dev-arm64-standalone.apk`（+ `.sha256`）、
  `duoge-parkour-0.1.4-dev-arm64.apk`（首页「旧版继续保留」入口）。
- 删除 26 个无任何页面/清单引用的旧包（0.1 ~ 0.1.13）与两个孤儿测试页 `test-0.1.6.html` / `test-0.1.7.html`。
- 结果：**站点 301.8 MB**（85 个跟踪文件），Pages 构建 `built` 无错误；线上核验 index 200、
  latest 61,350,021 B、命名包 61,350,021 B、0.1.4 51,248,394 B、已删文件 404。
- 找回方式：`git show <commit>:downloads/<文件名> > 输出`（历史仍在，仓库 clone 体积不变）。
- 遗留：`download-routes-0.1.5.json`、`release-0.1.5.json` 等历史元数据仍提到已删文件，不被页面或客户端消费。
