@echo off

SET SCRIPT_DIR=%~dp0
SET TOOLS_DIR=%SCRIPT_DIR%tools
SET RESOURCES_DIR=%SCRIPT_DIR%resources


copy %RESOURCES_DIR%\chromium_strings_old.grd %TOOLS_DIR%\old\chromium_strings.grd
copy %RESOURCES_DIR%\chromium_strings_zh-CN_old.xtb %TOOLS_DIR%\old\chromium_strings_zh-CN.xtb
copy %RESOURCES_DIR%\chromium_strings.grd %TOOLS_DIR%\new\chromium_strings.grd

copy %RESOURCES_DIR%\generated_resources_old.grd %TOOLS_DIR%\old\generated_resources.grd
copy %RESOURCES_DIR%\generated_resources_zh-CN_old.xtb %TOOLS_DIR%\old\generated_resources_zh-CN.xtb
copy %RESOURCES_DIR%\generated_resources.grd %TOOLS_DIR%\new\generated_resources.grd

ECHO Copy temp files success!


pushd %TOOLS_DIR%

echo.
echo handling chromium_strings.grd...
python3 "generate_translation_bundle.py" "--old_grd" "old/chromium_strings.grd" "--old_xtb" "old/chromium_strings_zh-CN.xtb" "--new_grd" "new/chromium_strings.grd" "-o" "new/chromium_strings_zh-CN.xtb"
IF ERRORLEVEL 0 echo grit resources success!
copy %TOOLS_DIR%\new\chromium_strings_zh-CN.xtb %RESOURCES_DIR%\chromium_strings_zh-CN.xtb

echo.
echo handling generated_resources.grd...
python3 "generate_translation_bundle.py" "--old_grd" "old/generated_resources.grd" "--old_xtb" "old/generated_resources_zh-CN.xtb" "--new_grd" "new/generated_resources.grd" "-o" "new/generated_resources_zh-CN.xtb"
IF ERRORLEVEL 0 echo grit resources success!
copy %TOOLS_DIR%\new\generated_resources_zh-CN.xtb %RESOURCES_DIR%\generated_resources_zh-CN.xtb 

popd


del /q %TOOLS_DIR%\old\chromium_strings.grd
del /q %TOOLS_DIR%\old\chromium_strings_zh-CN.xtb
del /q %TOOLS_DIR%\new\chromium_strings.grd
del /q %TOOLS_DIR%\new\chromium_strings_zh-CN.xtb

del /q %TOOLS_DIR%\old\generated_resources.grd
del /q %TOOLS_DIR%\old\generated_resources_zh-CN.xtb
del /q %TOOLS_DIR%\new\generated_resources.grd
del /q %TOOLS_DIR%\new\generated_resources_zh-CN.xtb
echo.
echo Clear temp files success!

pause