@echo off && setlocal enabledelayedexpansion

set pyexe=E:\project\pytoolsip\client\include\python\python.exe
set toolpath=E:\project\pytoolsip-tools\iwannafall\assets\tool\
set pjpath=E:\project\pytoolsip-tools\iwannafall\
set mainfile=main.py

cd %toolpath%

%pyexe% %mainfile% %pjpath%

pause