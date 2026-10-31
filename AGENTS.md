# 下载官网维护规则

1. 开始工作先读本文件和 `docs/agent/STATE.md`，检查 Git 状态、diff 和远端分支。游戏源码仓库为 `pkokwho/duoduo-parkour`，其 `docs/agent/STATE.md` 是工程交接入口。
2. 用户要求每次推送或发布都更新项目记忆：推送前更新本站 STATE，发布后记录实际远端提交、版本、包名、验证证据和剩余事项；不要把 Git 推送成功当作 Pages 部署/HTTP 核验成功。
3. 先上传已签名 APK 并核验远端完整 SHA，再提升下载页与更新清单。不得发布无签名包，不得将私钥、签名备份、口令或构建缓存上传本站。
4. 原包名 `org.duoge.parkour` 使用 `update.json`；独立新版 `org.duoge.parkour.standalone` 使用 `update-standalone.json`。二者不可混用，不要把独立新版写进旧更新清单诱导覆盖安装。
5. 新版可与旧版并存，无需卸载旧版，但不自动继承旧纪录。下载页必须说明。实际构建最低 API 29（Android 10），不要沿用旧页面 Android 7+ 的错误说明。
6. 保留旧 APK、旧清单及已发布试玩；不覆盖不可变安装包或擅自删除文件。发布新版本需要用户授权；当前会话已明确授权发布 0.1.5-dev 独立版官网及在线更新入口。
