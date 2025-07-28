echo ================================================
echo 【启动电费监控网页】
echo ================================================
cd /d %~dp0
call .venv\Scripts\activate
python src\web_panel.py
