@echo off
set appdata=%~dp0tmp
set userprofile=%~dp0tmp
set temp=%~dp0tmp
set PATH=%PATH%;ffmpeg;venv\Lib\site-packages\torch\lib;venv\Lib\site-packages\nvidia\cudnn\bin;venv\Lib\site-packages\nvidia\cublas\bin;models

set CUDA_MODULE_LOADING=LAZY

:menu
echo.
echo  [1] Face Swap
echo  [2] Lip Sync (pick an audio file + a video/image)
echo.
set /p choice="Choose an option (1 or 2): "

if "%choice%"=="1" (
    .\venv\Scripts\python.exe run.py --execution-provider cuda
    goto end
)
if "%choice%"=="2" (
    .\venv\Scripts\python.exe lipsync.py
    goto end
)
echo Invalid choice.
goto menu

:end
pause

