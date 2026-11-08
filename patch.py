import os

print("正在执行定制化修改...")

# 1. 修改 Rust 后端入口实现便携版
main_rs = 'apps/app/src-tauri/src/main.rs'
if os.path.exists(main_rs):
    with open(main_rs, 'r', encoding='utf-8') as f:
        content = f.read()

    portable_snippet = '''
    if let Ok(exe_path) = std::env::current_exe() {
        if let Some(exe_dir) = exe_path.parent() {
            let data_dir = exe_dir.join("data");
            if !data_dir.exists() { let _ = std::fs::create_dir_all(&data_dir); }
            unsafe { std::env::set_var("THESEUS_CONFIG_DIR", data_dir.to_str().unwrap()); }
        }
    }
    '''

    if 'THESEUS_CONFIG_DIR' not in content:
        new_content = content.replace('fn main() {', 'fn main() {' + portable_snippet)
        with open(main_rs, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("-> 成功为 main.rs 注入便携版逻辑")

# 2. 修改前端样式隐藏右侧 Plus 横幅与广告
css_files = []
for root, dirs, files in os.walk('apps/app'):
    for file in files:
        if file.endswith('.css'):
            css_files.append(os.path.join(root, file))

for css_file in css_files:
    with open(css_file, 'r', encoding='utf-8') as f:
        c_content = f.read()
    # 找找看是不是全局样式文件，往里面追加隐藏横幅的 CSS
    if 'display: none !important;' not in c_content:
        with open(css_file, 'a', encoding='utf-8') as f:
            f.write("\n/* 自定义：隐藏 Plus 横幅与广告 */\ndiv[class*='plus'], div[class*='banner'], aside[class*='plus'], section[class*='promo'] { display: none !important; }\n")
        print(f"-> 成功向 {css_file} 注入去广告样式")
        break

print("定制化修改完成！")
