#!/bin/bash
set -e

# 1. 开启Tauri便携模式，配置存在exe同目录
TAURI_CONF="apps/app/tauri.conf.json"
jq '.tauri.portable = true' "$TAURI_CONF" > tmp.json && mv tmp.json "$TAURI_CONF"

# 2. 注释广告初始化入口，不启动广告窗口
sed -i 's/init_ads();/\/\/ init_ads();/' apps/app/src/main.rs

# 3. 清空广告iframe页面
echo "" > apps/frontend/src/public/promo-frame.html

# 4. 移除Modrinth+横幅相关渲染（前端匹配）
sed -i 's/<ModrinthPlusBanner //<!-- <ModrinthPlusBanner /g' apps/frontend/**/*.vue
sed -i 's/\/ModrinthPlusBanner>/\/ModrinthPlusBanner -->/g' apps/frontend/**/*.vue
