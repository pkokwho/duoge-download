(() => {
  const note = document.getElementById('device-note');
  if (/iPhone|iPad|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) {
    note.textContent = '你正在使用 iPhone / iPad：此 APK 仅支持安卓，请使用安卓手机下载。';
  }
})();
