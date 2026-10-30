# 舵哥快跑官方下载站

官网：https://pkokwho.github.io/duoge-download/
公开静态站仓库：pkokwho/duoge-download。游戏源码继续私有，本站不包含源码、构建缓存或签名文件。

当前版本：0.1.3-dev / versionCode4 / org.duoge.parkour，Android7.0+ ARM64，58.2MiB。
下载：downloads/duoge-parkour-0.1.3-dev-arm64.apk
SHA256：22e38f0aedd5a1e3c8c3ba719b85cfb8afdc88c5b49fce444332d6bef34acba7

首页、release.json、update.json、test/updater兼容入口均指向同一真实版本。旧APK保留为归档。旧0.1.1没有更新器，需手动覆盖安装一次；0.1.2可通过原检查更新入口升级。新版本在首页右上角设置中检查/下载，最终仍由安卓系统确认安装。

更新：近景A构图、明确设置入口、完整车辆与已驶过车体整车淡出，保留触控和性能修复、原动画、旧最高分。同包名与证书已校验。云端1296网格姿态/8比例、设置/下载/存档及控制场景连续渲染通过；不等于已逐一测试所有品牌真机。

发布顺序：先上传APK并验证公网完整SHA256，再提升网页和更新清单；不得先指向尚不存在的APK。发布更新时递增versionCode、保持签名，不要求卸载或清除数据。

构图预览：camera-preview.html。图片使用WebP；无第三方追踪、新增付费服务或自有域名。
