// Paste into the DevTools Console on the LinkedIn post, after playing the
// video to the end. The segment URLs are copied to your clipboard; then run:
//   pbpaste | linkedin-dl --segments -
(() => {
  const urls = new Set();
  performance.getEntriesByType('resource')
    .map(e => e.name)
    .filter(u => u.includes('dms.licdn.com/playlist/vid'))
    .forEach(u => urls.add(u));
  const list = [...urls];
  copy(JSON.stringify(list));
  console.log(`Copied ${list.length} segment URLs to the clipboard.`);
})();
