@echo off
chcp 65001 > nul
echo 개발 서버를 종료합니다...

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000') do (
    taskkill /f /pid %%a > nul 2>&1
)

echo 완료!
timeout /t 2 > nul
