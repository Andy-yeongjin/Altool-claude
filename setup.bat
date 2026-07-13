@echo off
setlocal

set "ALTOOL_DIR=%~dp0"
if "%ALTOOL_DIR:~-1%"=="\" set "ALTOOL_DIR=%ALTOOL_DIR:~0,-1%"
set "NONINTERACTIVE="

if not "%~1"=="" (
    set "PROJECT_DIR=%~1"
    set "NONINTERACTIVE=1"
    goto :proceed
)

echo.
echo =============================================
echo   Altool Project Setup
echo =============================================
echo.

:: Windows folder picker dialog (VBScript)
set "TMPVBS=%TEMP%\altool_picker.vbs"
echo Set oShell = CreateObject("Shell.Application") > "%TMPVBS%"
echo Set oFolder = oShell.BrowseForFolder(0, "Select your project folder", 0) >> "%TMPVBS%"
echo If Not oFolder Is Nothing Then >> "%TMPVBS%"
echo     WScript.Echo oFolder.Self.Path >> "%TMPVBS%"
echo End If >> "%TMPVBS%"
for /f "delims=" %%i in ('cscript //nologo "%TMPVBS%"') do set "PROJECT_DIR=%%i"
del "%TMPVBS%" 2>nul

if not defined PROJECT_DIR goto :manual
if "%PROJECT_DIR%"=="" goto :manual
goto :proceed

:manual
echo.
echo   [!] Folder picker failed. Please type the project folder path.
echo   [!] Example: C:\Users\YourName\Desktop\my-project
echo.
set /p PROJECT_DIR="  Folder path: "

if not defined PROJECT_DIR (
    echo Cancelled.
    pause
    exit /b 0
)
if "%PROJECT_DIR%"=="" (
    echo Cancelled.
    pause
    exit /b 0
)

:proceed

echo   Target: %PROJECT_DIR%
echo.
echo   Copying files...

:: Altool engine (steps + templates + rules)
xcopy /e /i /y "%ALTOOL_DIR%\altool" "%PROJECT_DIR%\altool" > nul
for /d /r "%PROJECT_DIR%\altool" %%d in (__pycache__) do if exist "%%d" rmdir /s /q "%%d"
del /s /q "%PROJECT_DIR%\altool\*.pyc" "%PROJECT_DIR%\altool\*.pyo" 2>nul
echo   [OK] altool\ (engine)

:: CLAUDE.md (Claude Code project instructions)
if exist "%ALTOOL_DIR%\CLAUDE.md" (
    copy /y "%ALTOOL_DIR%\CLAUDE.md" "%PROJECT_DIR%\CLAUDE.md" > nul
    echo   [OK] CLAUDE.md
)

:: Claude Code local command(s): /altool
if not exist "%PROJECT_DIR%\.claude\commands\" mkdir "%PROJECT_DIR%\.claude\commands"
if exist "%ALTOOL_DIR%\templates\claude\commands\" (
    xcopy /e /i /y "%ALTOOL_DIR%\templates\claude\commands" "%PROJECT_DIR%\.claude\commands" > nul
    echo   [OK] Claude Code local command: /altool
) else (
    echo   [WARN] Command templates missing: templates\claude\commands
)

:: Claude Code project skills (e.g. vercel-react-best-practices)
if not exist "%PROJECT_DIR%\.claude\skills\" mkdir "%PROJECT_DIR%\.claude\skills"
if exist "%ALTOOL_DIR%\templates\claude\skills\" (
    for /d %%s in ("%ALTOOL_DIR%\templates\claude\skills\*") do (
        if exist "%%s\SKILL.md" (
            xcopy /e /i /y "%%s" "%PROJECT_DIR%\.claude\skills\%%~nxs" > nul
            echo   [OK] Claude Code skill: %%~nxs
        )
    )
) else (
    echo   [WARN] Skill templates missing: templates\claude\skills
)

:: constitution.md
if exist "%ALTOOL_DIR%\constitution.md" (
    copy /y "%ALTOOL_DIR%\constitution.md" "%PROJECT_DIR%\constitution.md" > nul
    echo   [OK] constitution.md
)

:: designs/
if not exist "%PROJECT_DIR%\designs\" mkdir "%PROJECT_DIR%\designs"
if not exist "%PROJECT_DIR%\designs\claude-design\" mkdir "%PROJECT_DIR%\designs\claude-design"
echo   [OK] designs\claude-design\ (Claude design HTML folder)
for %%f in (design.md) do (
    if exist "%ALTOOL_DIR%\designs\%%f" (
        copy /y "%ALTOOL_DIR%\designs\%%f" "%PROJECT_DIR%\designs\%%f" > nul
        echo   [OK] designs\%%f
    )
)

:: prd/
if not exist "%PROJECT_DIR%\prd\" mkdir "%PROJECT_DIR%\prd"
echo   [OK] prd\ (folder)

:: start.bat / end.bat
for %%f in (start.bat end.bat) do (
    if exist "%ALTOOL_DIR%\%%f" (
        copy /y "%ALTOOL_DIR%\%%f" "%PROJECT_DIR%\%%f" > nul
        echo   [OK] %%f
    )
)

:: .gitignore (only create when missing - never overwrite)
if not exist "%PROJECT_DIR%\.gitignore" (
    (
        echo # Altool state
        echo .altool/
        echo.
        echo # Node
        echo node_modules/
        echo .next/
        echo.
        echo # Python
        echo __pycache__/
        echo *.py[cod]
        echo.
        echo # Env / secrets
        echo .env
        echo .env*.local
        echo.
        echo # Local DB
        echo *.db
        echo *.db-journal
        echo.
        echo # Claude Code project config
        echo !.claude/
        echo.
        echo # Local browser/test artifacts
        echo .playwright-mcp/
    ) > "%PROJECT_DIR%\.gitignore"
    echo   [OK] .gitignore created
) else (
    echo   [SKIP] .gitignore exists - add ".altool/" manually if needed
)

echo.
echo =============================================
echo   Done!
echo =============================================
echo.
echo   1. Open Claude Code
echo   2. Open folder: %PROJECT_DIR%
echo   3. Restart Claude Code or open a new session if the command does not appear
echo   4. Type:  /altool setup
echo.
if not defined NONINTERACTIVE pause
