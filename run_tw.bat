@echo off

echo handling chromium_strings.grd...
python3 "generate_translation_bundle.py" "--old_grd" "old/chromium_strings.grd" "--old_xtb" "old/chromium_strings_zh-TW.xtb" "--new_grd" "new/chromium_strings.grd" "-o" "new/chromium_strings_zh-TW.xtb"
IF ERRORLEVEL 0 ECHO Success!

echo handling generated_resources.grd...
python3 "generate_translation_bundle.py" "--old_grd" "old/generated_resources.grd" "--old_xtb" "old/generated_resources_zh-TW.xtb" "--new_grd" "new/generated_resources.grd" "-o" "new/generated_resources_zh-TW.xtb"
IF ERRORLEVEL 0 ECHO Success!

cmd /k