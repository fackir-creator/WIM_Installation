@echo off
setlocal enabledelayedexpansion
cls
pushd "%~dp0" >nul 2>&1
chcp 65001 >nul 2>&1
:: Script Idea, Renderings, Tests, Code Fixes, Gemini AI Training - fatkir 1/26/2026
:: ========================================================================
:: БЛОК 0: ВАЖНИ ПРАВИЛА ЗА РЕДАКТИРАНЕ (ЗАРАДИ EnableDelayedExpansion)
:: ========================================================================
:: 1. СИМВОЛЪТ "!" (Удивителна):
::    - ПРОБЛЕМ: Скриптът го мисли за променлива и гърми или го скрива.
::    - ГРЕШНО:  echo ВНИМАНИЕ!
::    - ВЯРНО:   echo ВНИМАНИЕ^^! (трябват две колибки преди него)
::    - НАЙ-ДОБРЕ: Избягвайте го напълно в текстовете.
::
:: 2. СКОБИ "( )" (Кръгли скоби):
::    - ПРОБЛЕМ: Ако са вътре в IF проверка, чупят логиката на блока.
::    - ГРЕШНО:  if ... ( echo Изберете (Y или N) )
::    - ВЯРНО:   if ... ( echo Изберете [Y или N] )
::    - РЕШЕНИЕ: Винаги ползвайте квадратни скоби [] в текстовете.
::
:: 3. СИМВОЛЪТ "|" (Права черта / Pipe):
::    - ПРОБЛЕМ: Опитва се да изпълни текста като команда.
::    - ЗАБРАНЕНО: Да се ползва в echo текст.
::
:: 4. СИМВОЛЪТ "%" (Процент):
::    - ПРОБЛЕМ: Трябва да се ескейпва, за да се види.
::    - ВЯРНО:   echo Зареждане на 100%%
::
:: 5. ПРАЗНИ РЕДОВЕ:
::    - ПРОБЛЕМ: "echo." понякога гърми с "ECHO is off".
::    - РЕШЕНИЕ: Ползвайте "echo(" за празен ред.
:: ========================================================================

:: ========================================================================
:: начало на блок 1 - Пътища и Конфигурация
:: ========================================================================
:: --- ПЪТИЩА ДО WIM ФАЙЛОВЕТЕ ---
set "wim[1]=Y:\WIM\11.wim;Windows 11 Pro x64"
set "wim[2]=Y:\WIM\11pro_oem.wim;Windows 11 Pro OEM x64"
set "wim[3]=Y:\WIM\11home_oem.wim;Windows 11 Home OEM x64"
set "wim[4]=Y:\WIM\10.wim;Windows 10 Pro x64"
set "wim[5]=Y:\WIM\81.wim;Windows 8.1 Pro x64"
set "wim[6]=Y:\WIM\7.wim;Windows 7 Pro x64"
set "wim[7]=Y:\WIM\7x32.wim;Windows 7 Pro x86 MBR ONLY"

:: --- ПЪТИЩА ДО ИНСТРУМЕНТИ ---
set "rstPath=Y:\WIM\IntelRST"
set "keyExe=Z:\SSTR\MInst\Portable\OemKey_All.exe"
set "txtRelPath=Users\User\Desktop"
set "txtFileName=WindowsKEY.txt"

:: --- АВТОМАТИЧНО БРОЕНЕ ---
set "total_wims=0"
:COUNT_LOOP
set /a "next_chk=total_wims+1"
if defined wim[%next_chk%] (
    set "total_wims=%next_chk%"
    goto COUNT_LOOP
)

:: --- ИНИЦИАЛИЗАЦИЯ НА БУКВИ ---
set "allLtrs=S W D I J K L M N O P Q R T U V X Y Z"
set "bootDrive=" & set "winDrive=" & set "dataDrive="
for %%L in (%allLtrs%) do (
    if not exist %%L:\ (
        if not defined bootDrive (set "bootDrive=%%L") else (
            if not defined winDrive (set "winDrive=%%L") else (
                if not defined dataDrive (set "dataDrive=%%L")
            )
        )
    )
)
:: ========================================================================
:: край на блок 1

:: ========================================================================
:: начало на блок 2 
:: ========================================================================
:BLOCK_CHECKS

fltmc >nul 2>&1 || (
    powershell -Command "Start-Process '%~dpnx0' -Verb RunAs"
    exit /b
)

:: 2. ПРОВЕРКА ЗА WinPE (БЛОКИРАЩА)
set "isWinPE=0"
reg query "HKLM\SYSTEM\CurrentControlSet\Control\MiniNT" >nul 2>&1
if %errorlevel% equ 0 set "isWinPE=1"

if "%isWinPE%"=="0" (
    cls & color 4F
    echo ========================================================================
    echo                  ^^! ПРЕДУПРЕЖДЕНИЕ ЗА СИГУРНОСТ ^^!
    echo ========================================================================
    echo(
    echo      ВНИМАНИЕ: Скриптът НЕ е стартиран в Windows PE среда ^^!
    echo(
    echo      Изпълнението му в работеща Windows среда ще доведе до:
    echo      НЕОБРАТИМИ ЩЕТИ, ИЗТРИВАНЕ НА ДИСКОВЕ И ЗАГУБА НА ДАННИ ^^!
    echo(
    echo            ТОЗИ СКРИПТ Е ПРЕДНАЗНАЧЕН САМО ЗА ИНСТАЛАЦИЯ ^^!
    echo       Стартирането му в работещ Windows е НАПЪЛНО ЗАБРАНЕНО ^^!
    echo(
    echo ========================================================================
    echo                   НАТИСНЕТЕ КЛАВИШ ЗА ИЗХОД
    echo ========================================================================
    pause >nul
    exit
)
:: ========================================================================
:: край на блок 2

:: ========================================================================
:: начало на блок 3 - engin (Менюта и Логика)
:: ========================================================================
:MENU_1
:: Преди да покажем менюто, се уверяваме, че всичко е чисто
call :RESET_TO_STEP1

cls & color 0A
echo ========================================================================
echo                   СТЪПКА 1.0: ИЗБОР НА ОПЕРАЦИОННА СИСТЕМА
echo ========================================================================

for /L %%i in (1,1,%total_wims%) do (
    for /f "tokens=2 delims=;" %%B in ("!wim[%%i]!") do echo   [%%i] %%B
)

echo(
echo   [P] ПРОВЕРКА НА ВЕРСИЯТА НА ИНСТАЛИРАН WINDOWS
echo   [R] RST Drivers (Зареждане в RAM на WinPE)
echo   [K] Windows OEM KEY
echo   [E] Express = [Win] space [Disk] Примери: [E1 0] или [E12 0]
echo(
call :DISPLAY_DISKS
echo(

set "choice="
set "installIndex=1"
set "expressMode=0"
set /p "choice=Въведете Номер (1-%total_wims%) ИЛИ Команда (R/K/P/Е) ИЛИ (Enter = 1): "

if "%choice%"=="" set "choice=1"
if /i "%choice%"=="p" goto MENU_VERSION_CHECK
if /i "%choice%"=="r" (call :LOAD_PREINSTALL_RST & goto MENU_1)
if /i "%choice%"=="k" (
    if exist "%keyExe%" (start "" "%keyExe%") else (color 0C & echo   Файлът не е намерен & timeout /t 2 >nul)
    goto MENU_1
)
set "firstChar=%choice:~0,1%"
if /i "%firstChar%"=="E" goto PARSE_EXPRESS

:: ИЗВИКВАНЕ НА ПРОВЕРКИ ОТ БЛОК 5
call :VALIDATE_NUMERIC "%choice%"
if %errorlevel% neq 0 goto WRONG_CHOICE_HANDLER
call :VALIDATE_WIM_EXIST "%choice%"
if %errorlevel% neq 0 goto WRONG_CHOICE_HANDLER

for /f "tokens=1,2 delims=;" %%A in ("!wim[%choice%]!") do (
    set "fullWimPath=%%A"
    set "selectedName=%%B"
)
goto MENU_2

:PARSE_EXPRESS
set "wimID=" & set "diskChar=" & set "targetDisk="
set "cleanInput=%choice:~1%"
set "cleanInput=!cleanInput::= !"
set "cleanInput=!cleanInput:/= !"
set "cleanInput=!cleanInput:-= !"
set "cleanInput=!cleanInput:+= !"

for /f "tokens=1,2" %%A in ("!cleanInput!") do (
    set "wimID=%%A"
    set "diskChar=%%B"
)

:: ВАЛИДАЦИЯ ЗА ЕКСПРЕСЕН РЕЖИМ (ПОПРАВКА ЗА e50)
if "%wimID%"=="" (color 0C & echo( & echo   ГРЕШКА: Липсва ID на Windows & timeout /t 2 >nul & goto MENU_1)
if "%diskChar%"=="" (
    color 0C & echo( 
    echo   ГРЕШКА: Невалиден формат [Липсва номер на диск]
    echo   Правилен формат: E5 0 ^(с интервал^)
    timeout /t 3 >nul 
    goto MENU_1
)

call :VALIDATE_NUMERIC "%wimID%"
if %errorlevel% neq 0 (color 0C & echo( & echo   ГРЕШКА: Невалиден номер на Windows & timeout /t 2 >nul & goto MENU_1)

call :VALIDATE_WIM_EXIST "%wimID%"
if %errorlevel% neq 0 (color 0C & echo( & echo   Windows N%wimID% не съществува & timeout /t 3 >nul & goto MENU_1)

call :VALIDATE_DISK_EXIST "%diskChar%"
if %errorlevel% neq 0 (color 0C & echo( & echo   ГРЕШКА: Диск %diskChar% не съществува & timeout /t 3 >nul & goto MENU_1)

set "targetDisk=%diskChar%"
for /f "tokens=4,5" %%A in ('echo list disk ^| diskpart ^| findstr /R /C:"Disk %targetDisk% "') do set "dSize=%%A %%B"

set "expressMode=1" & set "method=2" & set "b_mode=UEFI" & set "b_msg=UEFI" & set "installIndex=1"
set "p_msg=Full Disk"

for /f "tokens=1,2 delims=;" %%A in ("!wim[%wimID%]!") do (
    set "fullWimPath=%%A"
    set "selectedName=%%B (EXPRESS: E%wimID% %diskChar%)"
)
goto PREPARE_EXPRESS

:WRONG_CHOICE_HANDLER
color 0C & echo( & echo   ГРЕШЕН ИЗБОР ИЛИ НЕВАЛИДНА КОМАНДА & timeout /t 2 >nul & goto MENU_1

:PREPARE_EXPRESS
cls & color 0A
echo ========================================================================
echo                   EXPRESS ИНСТАЛАЦИЯ СТАРТИРА 
echo ========================================================================
echo   СИСТЕМА:    !selectedName!
echo   ЦЕЛ:        DISK %targetDisk% (%dSize%)
echo   РЕЖИМ:      GPT / ЕДИН ДЯЛ
echo ========================================================================
echo            СТАРТИРАНЕ СЛЕД 6 СЕКУНДИ...
echo      [X] ОТКАЗ И ВРЪЩАНЕ В НАЧАЛОТО (Стъпка 1)
echo ========================================================================

choice /c sx /t 6 /d s /n >nul
if errorlevel 2 (call :RESET_TO_STEP1 & goto MENU_1)
goto PROCEED

:MENU_2
cls & color 0A
echo ========================================================================
echo                   СТЪПКА 2.0: ИЗБОР НА ЦЕЛЕВИ ДИСК
echo ========================================================================
echo(
echo  ИЗБРАН OS: %selectedName%
echo(
call :DISPLAY_DISKS
echo(
echo   [D] Device Manager   [R] RST Drivers (Инжектиране в RAM на WinPE)
echo   [K] Windows OEM KEY  [B] Назад (Към Стъпка 1)
echo(
echo ========================================================================

set "targetInput="
set /p "targetInput=Избор на Диск № или Буква (Enter = Диск 0): "

if "!targetInput!"=="" set "targetInput=0"
if /i "!targetInput!"=="b" (call :RESET_TO_STEP1 & goto MENU_1)
if /i "!targetInput!"=="d" (start devmgmt.msc & goto MENU_2)
if /i "!targetInput!"=="r" (call :LOAD_PREINSTALL_RST & goto MENU_2)
if /i "!targetInput!"=="k" (
    if exist "%keyExe%" (start "" "%keyExe%") else (color 0C & echo   Файлът не е намерен & timeout /t 2 >nul)
    goto MENU_2
)

call :VALIDATE_DISK_EXIST "!targetInput!"
if %errorlevel% neq 0 (goto WRONG_DISK_CHOICE)

set "targetDisk=!targetInput!"
set "dSize=Unknown"
for /f "tokens=4,5" %%A in ('echo list disk ^| diskpart ^| findstr /R /C:"Disk !targetDisk! "') do set "dSize=%%A %%B"
goto MENU_3

:WRONG_DISK_CHOICE
color 0C & echo( & echo   ГРЕШЕН ИЗБОР НА ДИСК & timeout /t 2 >nul & goto MENU_2

:MENU_VERSION_CHECK
cls & color 0A
echo ========================================================================
echo               ПРОВЕРКА НА ВЕРСИЯТА НА ИНСТАЛИРАН WINDOWS
echo ========================================================================
echo  Налични устройства:
echo(
wmic logicaldisk get caption,volumename 2>nul
echo ************************************************************************
echo  Въведете БУКВА на диска (напр. C или D)
echo(
echo  [1] Назад към ГЛАВНО МЕНЮ
echo  [2] Инжектиране на RST Drivers в Windows PE (Ако не се вижда диска)
echo ========================================================================
set "chkLtr="
set /p "chkLtr=Избор или Буква: "

if "%chkLtr%"=="1" goto MENU_1
if "%chkLtr%"=="2" (call :LOAD_PREINSTALL_RST & goto MENU_VERSION_CHECK)
if "%chkLtr%"=="" goto MENU_VERSION_CHECK

set "chkLtr=%chkLtr:~0,1%"
call :VALIDATE_LETTER "%chkLtr%"
if %errorlevel% neq 0 (color 0C & echo( & echo   Устройство %chkLtr%: не съществува & timeout /t 2 >nul & color 0A & goto MENU_VERSION_CHECK)

set "hiveToCheck=%chkLtr%:\Windows\System32\config\SOFTWARE"
if not exist "%hiveToCheck%" (color 0C & echo( & echo   ГРЕШКА: На %chkLtr%: не е открит Windows & timeout /t 2 >nul & color 0A & goto MENU_VERSION_CHECK)

echo( & echo   Зареждане на информация...
reg unload HKLM\OFFLINE >nul 2>&1
reg load HKLM\OFFLINE "%hiveToCheck%" >nul
if !errorlevel! neq 0 (color 0C & echo   ГРЕШКА: Регистърът е зает & pause & color 0A & goto MENU_VERSION_CHECK)

chcp 437 >nul
set "cName=Unknown" & set "cEd=Unknown" & set "cBuild=Unknown"
for /f "tokens=2*" %%A in ('reg query "HKLM\OFFLINE\Microsoft\Windows NT\CurrentVersion" /v ProductName 2^>nul') do set "cName=%%B"
for /f "tokens=2*" %%A in ('reg query "HKLM\OFFLINE\Microsoft\Windows NT\CurrentVersion" /v EditionID 2^>nul') do set "cEd=%%B"
for /f "tokens=2*" %%A in ('reg query "HKLM\OFFLINE\Microsoft\Windows NT\CurrentVersion" /v DisplayVersion 2^>nul') do set "cBuild=%%B"
if "%cBuild%"=="Unknown" for /f "tokens=2*" %%A in ('reg query "HKLM\OFFLINE\Microsoft\Windows NT\CurrentVersion" /v ReleaseId 2^>nul') do set "cBuild=%%B"
chcp 65001 >nul

reg unload HKLM\OFFLINE >nul 2>&1

:VERSION_RESULT_LOOP
cls & color 0A
echo ========================================================================
echo                 РЕЗУЛТАТ ОТ ПРОВЕРКАТА НА ДИСК %chkLtr%:
echo ========================================================================
echo(
echo  ОПЕРАЦИОННА СИСТЕМА:  %cName%
echo  ИЗДАНИЕ (EDITION):    %cEd%
echo  ВЕРСИЯ (BUILD):       %cBuild%
echo(
echo ========================================================================
echo  [1] Проверка на друг диск
echo  [2] Назад към ГЛАВНО МЕНЮ
echo ========================================================================
set "post="
set /p "post=Избор: "
if "%post%"=="1" goto MENU_VERSION_CHECK
if "%post%"=="2" goto MENU_1
goto VERSION_RESULT_LOOP

:MENU_3
cls & color 0A
echo ========================================================================
echo                   СТЪПКА 3.0: МЕТОД НА ИНСТАЛАЦИЯ
echo ========================================================================
echo  ИЗБРАН OS:   %selectedName%
echo  ИЗБРАН ДИСК: %targetDisk% (Общ размер: %dSize%)
echo ========================================================================
echo(
echo  [1] АВТО: ЕДИН ПАРТИШЪН (Целия диск)
echo ------------------------------------------------------------------------
echo  [2] АВТО: ДВА ПАРТИШЪНА (C: 150GB + Остатъкa за Data)
echo ------------------------------------------------------------------------
echo  [3] АВТО: ИЗБОР НА РАЗМЕР ЗА C: (Остатъка от диск за Data)
echo ------------------------------------------------------------------------
echo  [4] РЪЧНО: ИЗБОР НА СЪЩЕСТВУВАЩИ ПАРТИШЪНИ
echo ------------------------------------------------------------------------
echo  [B] Назад
echo ========================================================================
set "method=2"
set /p "method=Избор [1-4], по подразбиране е [%method%]: "
if /i "%method%"=="b" (call :RESET_TO_STEP2 & goto MENU_2)
if "%method%"=="" set "method=2"

if "%method%"=="1" (set "p_msg=Full Disk" & goto MENU_4)
if "%method%"=="2" (set "customSizeMB=153600" & set "p_msg=150GB + Data" & goto MENU_4)
if "%method%"=="3" goto CUSTOM_SIZE
if "%method%"=="4" goto MANUAL_PARTS
color 0C & echo НЕВАЛИДЕН МЕТОД! & timeout /t 2 >nul & goto MENU_3

:CUSTOM_SIZE
cls & color 0A
echo ========================================================================
echo                   СТЪПКА 3.3: ИЗБОР НА РАЗМЕР ЗА C:
echo ========================================================================
echo(
echo ИЗБРАНА OS: %selectedName%
echo(
call :DISPLAY_DISKS
echo(
echo  ИЗБРАН ДИСК ЗА РАБОТА: %targetDisk% (Размер: %dSize%)
echo(
echo ========================================================================
echo(
echo    [ВНИМАНИЕ]: МИНИМАЛЕН РАЗМЕР - 60 GB
echo(
echo    [B] Назад
echo(
echo ========================================================================
set "userGB="
set /p "userGB=Въведете размер за C: в GB: "
if "!userGB!"=="" goto CUSTOM_SIZE
if /i "!userGB!"=="b" (call :RESET_TO_STEP3 & goto MENU_3)
call :VALIDATE_NUMERIC "!userGB!"
if %errorlevel% neq 0 (color 0C & echo( & echo   ГРЕШКА: Трябва число над 60 GB & timeout /t 2 >nul & color 0A & goto CUSTOM_SIZE)

set /a "numGB=!userGB!"
if !numGB! LSS 60 (color 0C & echo( & echo   ГРЕШКА: Трябва число над 60 GB & timeout /t 2 >nul & color 0A & goto CUSTOM_SIZE)
set /a "customSizeMB=!numGB! * 1024"
set "p_msg=!numGB! GB + Data"
set "method=3"
goto MENU_4

:MANUAL_PARTS
cls & color 0A
echo ========================================================================
echo                   СТЪПКА 3.4: РЪЧЕН ИЗБОР [ДИСК %targetDisk%]
echo ========================================================================
echo  ИЗБРАН OS:   %selectedName%
echo  ИЗБРАН ДИСК: %targetDisk% (%dSize%)
echo ========================================================================
if "%targetDisk%"=="" (color 0C & echo   ГРЕШКА: Няма избран диск! Връщане назад... & timeout /t 3 >nul & goto MENU_2)

:: ------------------------------------------------------------------------
:: БРОНИРАНА ЛОГИКА ЗА GPT/MBR
:: Проверяваме дали дискът има звездичка (*) в колона GPT в Diskpart
:: ------------------------------------------------------------------------
set "diskStyle=MBR"
(echo list disk) | diskpart | findstr /C:"Disk %targetDisk% " | findstr "*" >nul
if %errorlevel% equ 0 set "diskStyle=GPT"

echo  [*] Засечена структура на диска: %diskStyle%
echo  [*] Четене на таблицата с дялове...

set "chk_script=%temp%\chk_p.txt"
set "parts_out=%temp%\parts_list.txt"
(echo select disk %targetDisk% & echo list partition) > "%chk_script%"
chcp 437 >nul
diskpart /s "%chk_script%" > "%parts_out%"
chcp 65001 >nul

if not exist "%parts_out%" (set "err_msg=Неуспешно извличане на списъка с дялове от Diskpart." & goto FATAL_ERROR)
type "%parts_out%" | findstr /i "Partition"
echo ========================================================================
echo  [B] Назад
echo ========================================================================

:GET_BOOT_PART
set "bootPart="
set /p "bootPart=Номер на BOOT (System/EFI) дял: "
if /i "%bootPart%"=="b" (call :RESET_TO_STEP3 & goto MENU_3)
if "%bootPart%"=="" goto GET_BOOT_PART
type "%parts_out%" | findstr /C:"Partition %bootPart% " >nul
if !errorlevel! neq 0 (color 0C & echo   Несъществуващ партишън & timeout /t 2 >nul & color 0A & goto GET_BOOT_PART)

:GET_WIN_PART
set "winPart="
set /p "winPart=Номер на WINDOWS (OS) дял: "
if /i "%winPart%"=="b" (call :RESET_TO_STEP3 & goto MENU_3)
if "%winPart%"=="" goto GET_WIN_PART
type "%parts_out%" | findstr /C:"Partition %winPart% " >nul
if !errorlevel! neq 0 (color 0C & echo   Несъществуващ партишън & timeout /t 2 >nul & color 0A & goto GET_WIN_PART)

if "%winPart%"=="%bootPart%" (color 0C & echo   ГРЕШКА: Избрали сте един и същ дял за всичко & timeout /t 2 >nul & color 0A & goto MANUAL_PARTS)

set "p_msg=P%bootPart% + P%winPart%"
set "method=4"

:: ------------------------------------------------------------------------
:: АВТОМАТИЧЕН ИЗБОР НА РЕЖИМ СПОРЕД ДИСКА (ПРЕСКАЧАМЕ MENU_4)
:: ------------------------------------------------------------------------
if "%diskStyle%"=="GPT" (
    set "b_mode=UEFI"
    set "b_msg=UEFI [Auto-Detect GPT]"
    goto CONFIRM
)
if "%diskStyle%"=="MBR" (
    set "b_mode=BIOS"
    set "b_msg=Legacy [Auto-Detect MBR]"
    goto CONFIRM
)

:MENU_4
cls & color 0A
echo ========================================================================
echo                   СТЪПКА 4.0: ИЗБОР НА BOOT РЕЖИМ
echo ========================================================================
echo  ИЗБРАН OS:   %selectedName%
echo  ИЗБРАН ДИСК: %targetDisk% (%dSize%)
echo  МЕТОД:       %p_msg%
echo ========================================================================
echo(
echo  [1] GPT (UEFI) [DEFAULT]
echo  [2] MBR (Legacy)
echo(
echo  [B] Назад
echo ========================================================================
set "boot_choice="
set /p "boot_choice=Избор [1]: "
if "%boot_choice%"=="" set "boot_choice=1"
if /i "%boot_choice%"=="b" (call :RESET_TO_STEP3 & goto MENU_3)
if "%boot_choice%"=="1" (set "b_mode=UEFI" & set "b_msg=UEFI" & goto CONFIRM)
if "%boot_choice%"=="2" (set "b_mode=BIOS" & set "b_msg=Legacy" & goto CONFIRM)
color 0C & echo   ГРЕШЕН ИЗБОР & timeout /t 2 >nul & goto MENU_4

:CONFIRM
cls & color 4F
echo ========================================================================
echo                    ВНИМАНИЕ: ПОТВЪРЖДЕНИЕ 
echo ========================================================================
echo  [*] ОБРАЗ: %selectedName%
echo  [*] ДИСК:  %targetDisk% (%dSize%)
echo  [*] РЕЖИМ: %b_msg%
echo  [*] МЕТОД: %p_msg%
echo ========================================================================
echo  ВСИЧКИ ДАННИ НА ДИСК %targetDisk% ЩЕ БЪДАТ ИЗТРИТИ!
echo ========================================================================
set "f_conf="
set /p "f_conf=Y/Enter за Старт | B за Назад: "
if /i "%f_conf%"=="b" (call :RESET_TO_STEP3 & goto MENU_3)
if "%f_conf%"=="" set "f_conf=y"
if /i "%f_conf%" neq "y" goto CONFIRM
:: ========================================================================
:: край на блок 3


:: ========================================================================
:: начало на блок 4 - Дискпарт (Екшън)
:: ========================================================================
:PROCEED
cls
color 0A
echo ========================================================================
echo                   СТАРТИРАНЕ НА ОПЕРАЦИЯТА
echo ========================================================================
echo  [*] ОБРАЗ: %selectedName%
echo  [*] ДИСК:  %targetDisk% (%dSize%)
echo  [*] РЕЖИМ: %b_msg%
echo  [*] МЕТОД: %p_msg%
echo ========================================================================

:: Нулиране на грешката преди старт
set "err_msg="

if "%targetDisk%"=="" (set "err_msg=Целевият диск не е дефиниран." & goto FATAL_ERROR)
if "%method%"=="4" (
    if "%bootPart%"=="" (set "err_msg=Boot дялът не е дефиниран." & goto FATAL_ERROR)
    if "%winPart%"=="" (set "err_msg=Windows дялът не е дефиниран." & goto FATAL_ERROR)
)

set "dp_clean=%temp%\dp_clean.txt"
set "dp=%temp%\diskpart.txt"
set "dp_log=%temp%\diskpart.log"

set "cmd_os_part=create partition primary"
set "do_create_data=0"
if "%method%"=="1" (set "cmd_os_part=create partition primary size=153600" & set "do_create_data=1")
if "%method%"=="3" (set "cmd_os_part=create partition primary size=%customSizeMB%" & set "do_create_data=1")

if "%method%"=="4" goto SKIP_FULL_CLEAN

:: ========================================================
:: ЕТАП 1: ПЪЛНО ПОЧИСТВАНЕ (КРИТИЧНО ЗА GPT/MBR)
:: ========================================================
echo  [*] Почистване на диска и старите дялове...
(echo select disk %targetDisk% & echo clean & echo rescan) > "%dp_clean%"

chcp 437 >nul
diskpart /s "%dp_clean%" >nul 2>&1
chcp 65001 >nul

echo  [*] Изчакване (5 сек) за опресняване на диска...
ping -n 6 127.0.0.1 >nul

:SKIP_FULL_CLEAN
:: ========================================================
:: ЕТАП 2: СЪЗДАВАНЕ НА НОВИТЕ ДЯЛОВЕ
:: ========================================================
> "%dp%" (
    echo select disk %targetDisk%
    
    if "%method%"=="4" (
        echo select partition %bootPart%
        echo delete partition override
        echo select partition %winPart%
        echo delete partition override
    ) else (
        if "%b_mode%"=="UEFI" (
            echo convert gpt
            echo create partition efi size=260
            echo format quick fs=fat32 label=System
        ) else (
            echo convert mbr
            echo create partition primary size=500
            echo format quick fs=ntfs label=System
            echo active
        )
    )

    if "%method%"=="4" (
        if "%b_mode%"=="UEFI" (
            echo create partition efi size=260
            echo format quick fs=fat32 label=System
        ) else (
            echo create partition primary size=500
            echo format quick fs=ntfs label=System
            echo active
        )
    )

    echo assign letter=%bootDrive% noerr

    echo %cmd_os_part%
    echo format quick fs=ntfs label=Windows
    echo assign letter=%winDrive% noerr

    if "%do_create_data%"=="1" (
        echo create partition primary
        echo format quick fs=ntfs label=Data
        echo assign letter=%dataDrive% noerr
    )
)

echo  [*] ИЗПЪЛНЯВАМ DISKPART (СЪЗДАВАНЕ)...
echo ========================================================================
chcp 437 >nul
diskpart /s "%dp%" > "%dp_log%" 2>&1
if errorlevel 1 (
    chcp 65001 >nul
    echo [!] ГРЕШКА ПРИ DISKPART!
    type "%dp_log%"
    set "err_msg=ГРЕШКА В DISKPART (Разделяне на диска)!"
    goto FATAL_ERROR
)
chcp 65001 >nul
echo  [*] DISKPART ЗАВЪРШИ УСПЕШНО
echo ========================================================================

echo  [*] Прилагане на образа...
dism /Apply-Image /ImageFile:"%fullWimPath%" /Index:%installIndex% /ApplyDir:%winDrive%:\
if errorlevel 1 (
    set "err_msg=ГРЕШКА В DISM (Разархивиране на образа)!"
    goto FATAL_ERROR
)

echo.
echo  [*] Инициализация на boot записите (Изчакайте)...
ping -n 4 127.0.0.1 >nul
set "bcd_log=%temp%\bcd_log.txt"

echo  [*] Стартиране на BCDBOOT...
bcdboot %winDrive%:\Windows /s %bootDrive%: /f %b_mode% > "%bcd_log%" 2>&1
if errorlevel 1 (
    set "err_msg=ГРЕШКА В BCDBOOT (Създаване на Boot файловете)!"
    goto FATAL_ERROR
)

if /i "%b_mode%"=="BIOS" (
    bootsect /nt60 %bootDrive%: /force /mbr >nul 2>&1
    if errorlevel 1 (
        set "err_msg=ГРЕШКА В BOOTSECT (Запис на MBR)!"
        goto FATAL_ERROR
    )
)

goto END_INSTALL
:: ========================================================================
:: край на блок 4


:: ========================================================================
:: начало на блок 5 - Проверки и Тулове (Functions)
:: ========================================================================
:VALIDATE_NUMERIC
:: ::проверка за валидни цифри
if "%~1"=="" exit /b 1
for /f "delims=0123456789" %%a in ("%~1") do exit /b 1
exit /b 0

:VALIDATE_WIM_EXIST
:: ::проверка дали избраният номер съществува
if not defined wim[%~1] exit /b 1
exit /b 0

:VALIDATE_DISK_EXIST
:: ::проверка дали дискът е валиден през Diskpart
(echo select disk %~1) | diskpart | findstr /C:"is now the selected disk" >nul
exit /b %errorlevel%

:VALIDATE_LETTER
:: ::проверка дали буквата съществува
if exist "%~1:\" (exit /b 0) else (exit /b 1)

:FATAL_ERROR
cls & color 0C
echo ========================================================================
echo                           ФАТАЛНА ГРЕШКА 
echo ========================================================================
echo  Възникна проблем, който прекъсна инсталацията.
echo ========================================================================
echo  [*] ОБРАЗ: %selectedName%
echo  [*] ДИСК:  %targetDisk% (%dSize%)
echo  [*] РЕЖИМ: %b_msg%
echo  [*] МЕТОД: %p_msg%
echo ========================================================================
echo.
echo   ПРИЧИНА: %err_msg%
echo.
if exist "%bcd_log%" (
    echo  --- ПОДРОБНОСТИ ОТ BCDBOOT ---
    type "%bcd_log%"
    echo  ------------------------------
)
echo.
echo ========================================================================
echo  [R]     Рестартирай ВЕДНАГА
echo  [B]     Назад към СТЪПКА 1
echo  [X]     Изход
echo ========================================================================
choice /c rbx /n /m "Избор: "
if errorlevel 3 (call :CLEAN_TEMP & exit /b)
if errorlevel 2 (call :CLEAN_TEMP & goto MENU_1)
if errorlevel 1 wpeutil reboot
goto FATAL_ERROR

:END_INSTALL
cls
color 0A
echo ========================================================================
echo                ИНСТАЛАЦИЯТА ПРИКЛЮЧИ УСПЕШНО!
echo ========================================================================
echo  [*] ОБРАЗ: %selectedName%
echo  [*] ДИСК:  %targetDisk% (%dSize%)
echo  [*] РЕЖИМ: %b_msg%
echo  [*] МЕТОД: %p_msg%
echo ========================================================================
echo(
echo [D] Инжектирай RST драйвери на новия Windows
echo [R] Рестартирай ВЕДНАГА
echo [K] Постави PRODUCT KEY
echo [B] Назад към СТЪПКА 1
echo [X] Изход от скрипта
echo(

:: --- ЛОГИКА ЗА ТАЙМЕРА (EXPRESS = 30 сек, NORMAL = 1 час) ---
set "r_time=3600"
set "r_text=1 час"

if "%expressMode%"=="1" (
    set "r_time=30"
    set "r_text=30 секунди"
)

echo Автоматичен рестарт след %r_text%...
echo ========================================================================
choice /c drkbx /t %r_time% /d r /n /m "Избор: "
if errorlevel 5 (call :CLEAN_TEMP & exit /b)
if errorlevel 4 (call :CLEAN_TEMP & goto MENU_1)
if errorlevel 3 goto MAKE_KEY_FILE
if errorlevel 2 wpeutil reboot
if errorlevel 1 goto DRIVERS_MENU
goto END_INSTALL

:DRIVERS_MENU
cls & color 0A
echo ========================================================================
echo        СТЪПКА 5.0: ИНЖЕКТИРАНЕ НА RST ДРАЙВЕРИ НА НОВИЯ WINDOWS
echo ========================================================================
echo            ВАЖНО: ТОВА СЛАГА ДРАЙВЕРА В НОВИЯ WINDOWS!
echo ========================================================================
set "count=0"
for /f "delims=" %%D in ('dir "%rstPath%" /ad /b 2^>nul') do (
    set /a count+=1
    set "folder[!count!]=%%D"
    echo   [!count!] %%D
)
echo.
echo  [ENTER] ПРОДЪЛЖИ БЕЗ ДРАЙВЕРИ или [X]
echo ========================================================================
set "drv_choice="
set /p "drv_choice=Избор на цифра за RST + Enter или Enter за пропускане : "
if "%drv_choice%"=="" goto END_INSTALL
if /i "%drv_choice%"=="x" goto END_INSTALL
if not defined folder[%drv_choice%] (color 0C & echo   ГРЕШЕН ИЗБОР & timeout /t 2 >nul & goto DRIVERS_MENU)
set "selectedFolder=!folder[%drv_choice%]!"
echo.
echo [*] Инжектиране на драйвери в %winDrive%:\Windows...
dism /Image:%winDrive%:\ /Add-Driver /Driver:"%rstPath%\!selectedFolder!" /Recurse
if errorlevel 1 (color 0C & echo. & echo   ГРЕШКА! & pause) else (echo. & echo   OK - Успешно.)
pause
goto END_INSTALL

:RESET_TO_STEP1
set "fullWimPath=" & set "selectedName=" & set "targetDisk=" & set "dSize="
set "method=" & set "customSizeMB=" & set "bootPart=" & set "winPart=" & set "b_mode=" & set "p_msg="
exit /b

:RESET_TO_STEP2
set "targetDisk=" & set "dSize=" & set "method=" & set "customSizeMB=" & set "bootPart=" & set "winPart=" & set "b_mode=" & set "p_msg="
exit /b

:RESET_TO_STEP3
set "method=" & set "customSizeMB=" & set "bootPart=" & set "winPart=" & set "b_mode=" & set "p_msg="
exit /b

:CLEAN_TEMP
del /q "%temp%\cd.txt" "%temp%\chk_p.txt" "%temp%\parts_list.txt" "%temp%\diskpart.txt" "%temp%\diskpart.log" "%temp%\dp_clean.txt" "%temp%\bcd_log.txt" >nul 2>&1
exit /b

:DISPLAY_DISKS
echo ************************************************************************
echo                           НАЛИЧНИ ДИСКОВЕ:
echo ************************************************************************
(echo list disk) | diskpart | findstr /R /C:"Disk ###" /C:"\-\-\-" /C:"Disk [0-9]"
echo ************************************************************************
exit /b

:MAKE_KEY_FILE
set "targetDir=%winDrive%:\%txtRelPath%"
if not exist "%targetDir%" mkdir "%targetDir%" >nul 2>&1
set "kFile=%targetDir%\%txtFileName%"
echo. > "%kFile%"
echo [*] Отваряне на Notepad...
start "" notepad "%kFile%"
echo.
echo Файлът е създаден: %kFile%
echo Затворете Notepad след като поставите ключа.
pause
goto END_INSTALL

:LOAD_PREINSTALL_RST
:RST_LOOP
cls & color 0A
echo ========================================================================
echo        ЗАРЕЖДАНЕ НА RST ДРАЙВЕРИ ЗА WinPE (Pre-install)
echo ========================================================================
echo  ВАЖНО: ТОВА ЗАРЕЖДА ДРАЙВЕРА СЕГА, ЗА ДА ВИДИТЕ ДИСКА!
echo ========================================================================
set "c=0"
for /f "delims=" %%D in ('dir "%rstPath%" /ad /b 2^>nul') do (
    set /a c+=1
    set "f[!c!]=%%D"
    echo   [!c!] %%D
)
echo ========================================================================
echo  [B] Назад (Към меню Дискове)
echo ========================================================================
set "d_ch="
set /p "d_ch=Изберете драйвер: "
if "!d_ch!"=="" goto RST_LOOP
if /i "!d_ch!"=="b" exit /b
if not defined f[%d_ch%] goto RST_LOOP
set "p=%rstPath%\!f[%d_ch%]!"
echo.
echo ========================================================================
echo [*] Зареждане на драйвери в RAM-а на WinPE...
echo       %p%
echo ========================================================================
for /r "%p%" %%i in ("*.inf") do (
    echo [..] Зареждане: %%~nxi
    drvload "%%i" >nul 2>&1
    if !errorlevel! equ 0 (echo       [OK] УСПЕШНО) else (echo       [!] ГРЕШКА)
)
echo.
echo ========================================================================
echo  ГОТОВО. ПРОВЕРЕТЕ ДАЛИ ДИСКЪТ СЕ Е ПОЯВИЛ.
echo ========================================================================
echo  [1] Зареди друг драйвер
echo  [2] Готово (Връщане към предходното меню)
echo ========================================================================
:RST_EXIT_CHOICE
set "rst_act="
set /p "rst_act=Избор [1/2]: "
if "%rst_act%"=="1" goto RST_LOOP
if "%rst_act%"=="2" exit /b
goto RST_EXIT_CHOICE
:: ========================================================================
:: край на блок 5