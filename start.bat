@echo off
REM SoNoBot Startup Script for Windows CMD
REM Sets environment variables and starts the bot

echo 🚀 Starting SoNoBot...
echo.

REM Set environment variables
set BOT_TOKEN=11313522:339jDtbdAdQxc4RnLlp9TvBS4gV
set DB_PATH=sonobot.db
set LOG_LEVEL=INFO

REM Optional: Set admin ID if needed
REM set ADMIN_ID=123456789

REM Optional: Set BigModel AI API key if needed
REM set BIGMODEL_API_KEY=your_api_key_here

echo ✅ Environment variables set
echo    BOT_TOKEN: 11313522...
echo    DB_PATH: %DB_PATH%
echo    LOG_LEVEL: %LOG_LEVEL%
echo.

REM Start the bot
echo 🤖 Launching SoNoBot...
echo    Press Ctrl+C to stop the bot
echo.

python main.py

