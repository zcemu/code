const fs = require('fs');

// 1. 开启Tauri便携模式
const tauriConfPath = 'apps/app/tauri.conf.json';
const cfg = JSON.parse(fs.readFileSync(tauriConfPath, 'utf8'));
cfg.tauri.portable = true;
fs.writeFileSync(tauriConfPath, JSON.stringify(cfg, null, 2), 'utf8');
console.log('✅ 已开启便携模式');
