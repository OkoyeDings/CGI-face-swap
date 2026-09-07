@echo off
set appdata=%~dp0tmp
set userprofile=%~dp0tmp
set temp=%~dp0tmp
set PATH=%PATH%;ffmpeg;venv\Lib\site-packages\torch\lib;venv\Lib\site-packages\nvidia\cudnn\bin;venv\Lib\site-packages\nvidia\cublas\bin;models

set CUDA_MODULE_LOADING=LAZY

.\venv\Scripts\python.exe lipsync.py
pause
