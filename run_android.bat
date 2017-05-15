@echo off

echo handling android_chrome_strings.grd...
python3 "generate_translation_bundle.py" "--old_grd" "old/android_chrome_strings.grd" "--old_xtb" "old/android_chrome_strings_zh-CN.xtb" "--new_grd" "new/android_chrome_strings.grd" "-o" "new/android_chrome_strings_zh-CN.xtb"

cmd /k