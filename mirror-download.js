/* Offer only a fully verified mirror for this exact page's APK digest. */
(() => {
  const slots = [...document.querySelectorAll('[data-mirror-apk]')];
  if (!slots.length) return;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);
  fetch('mirror-links.json', { cache: 'no-cache', signal: controller.signal })
    .then(response => response.ok ? response.json() : null)
    .then(data => {
      if (!data || data.schema_version !== 1 || !data.files) return;
      for (const slot of slots) {
        const name = slot.dataset.mirrorApk;
        const entry = data.files[name];
        if (!entry || entry.sha256 !== slot.dataset.mirrorSha256) continue;
        const url = new URL(entry.url);
        const parts = url.pathname.split('/');
        const validPath = parts.length === 7 && parts[1] === 'projects' &&
          /^[a-z0-9][a-z0-9-]{1,59}$/.test(parts[2]) && parts[3] === 'files' &&
          /^v[0-9.]+-standalone$/.test(parts[4]) && parts[5] === name && parts[6] === 'download';
        if (url.protocol !== 'https:' || url.hostname !== 'sourceforge.net' || url.port || url.username || url.password || url.search || url.hash || !validPath) continue;
        const link = document.createElement('a');
        link.href = url.href;
        link.textContent = 'SourceForge 镜像下载（备用线路） →';
        link.rel = 'noopener noreferrer';
        slot.replaceChildren(link);
        slot.hidden = false;
      }
    })
    .catch(() => {})
    .finally(() => clearTimeout(timer));
})();
