@echo off && setlocal enabledelayedexpansion

set pyexe=E:\project\pytoolsip\client\include\python\python.exe
set pjfile=E:\project\pytoolsip-tools\iwannafall\assets\tool\
set mainfile=main.py

cd %pjfile%

%pyexe% %mainfile%

pause