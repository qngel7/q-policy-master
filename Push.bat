@echo off
git add .
git commit -m "정책서 수정: %date%"
git push -u origin main
pause