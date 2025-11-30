#!/usr/bin/env pwsh
# SoNoBot Startup Script for Windows PowerShell
# Sets environment variables and starts the bot

Write-Host "🚀 Starting SoNoBot..." -ForegroundColor Green
Write-Host ""

# Set environment variables
$env:BOT_TOKEN = "11313522:339jDtbdAdQxc4RnLlp9TvBS4gV"
$env:DB_PATH = "sonobot.db"
$env:LOG_LEVEL = "INFO"

# Optional: Set admin ID if needed
# $env:ADMIN_ID = "123456789"

# Optional: Set BigModel AI API key if needed
# $env:BIGMODEL_API_KEY = "your_api_key_here"

Write-Host "✅ Environment variables set:" -ForegroundColor Cyan
Write-Host "   BOT_TOKEN: $($env:BOT_TOKEN.Substring(0, 10))..." -ForegroundColor Gray
Write-Host "   DB_PATH: $env:DB_PATH" -ForegroundColor Gray
Write-Host "   LOG_LEVEL: $env:LOG_LEVEL" -ForegroundColor Gray
Write-Host ""

# Start the bot
Write-Host "🤖 Launching SoNoBot..." -ForegroundColor Yellow
Write-Host "   Press Ctrl+C to stop the bot" -ForegroundColor Gray
Write-Host ""

python main.py

