# 舵哥快跑 · 官方下载

马眼工作室出品。此公开仓库只含下载站、图片、安装包及公共更新清单，游戏源码保持私有。

- 官网：https://pkokwho.github.io/duoge-download/
- 当前默认修复版：0.1.1-dev / versionCode 2。
- 游戏内更新体验版：0.1.2-dev / versionCode 3，https://pkokwho.github.io/duoge-download/updater.html 。需要手动覆盖安装一次，以后的新版本可在游戏内检查、下载并交由安卓系统确认安装。
- 适用：ARM64 Android 7.0+。同包名和签名，更新时不要先卸载旧版，以保留本地数据。
- 当前版本信息：release.json；体验版信息：updater-release.json；客户端更新协议：update.json。

当前 update.json 指向已发布默认版 code2；已安装 code3 的体验版不会降级。没有更高版本时显示最新是正常的。系统授权及安装过程仍需真机确认，不能静默安装。

后续发布顺序：签名/包名/递增版本号和文件校验→上传 APK→验证公网完整下载→同步官网与 update.json。私有源码、签名文件和构建缓存不得上传。
