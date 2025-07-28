@echo off
cd /d D:\Documents\Github\nju_electric_monitor
chcp 65001 >nul
echo ================================================
echo 【南京大学电费监控脚本（自动模式）】
echo ================================================
echo.

cd /d %~dp0

echo 【加载虚拟环境...】
call .venv\Scripts\activate

echo 【正在检查环境...】
python tests\test_environment.py

echo.
echo 【正在运行主脚本...】
python src\nju_electric_monitor_auto.py

echo.
echo 【按任意键退出...】
pause >nul