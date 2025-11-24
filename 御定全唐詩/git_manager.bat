@echo off
chcp 65001 >nul
echo ========================================================
echo 《御定全唐詩》文件管理工具
echo ========================================================
echo.

if "%1"=="" (
    echo 使用方法:
    echo   git_manager.bat scan          - 扫描项目文件
    echo   git_manager.bat lists         - 生成推送文件列表
    echo   git_manager.bat gitignore     - 创建.gitignore文件
    echo   git_manager.bat backup        - 备份大文件
    echo   git_manager.bat clean         - 清理生成文件
    echo   git_manager.bat all           - 执行所有操作
    echo.
    echo 示例:
    echo   git_manager.bat all
    pause
    exit /b 1
)

cd /d "%~dp0"

if "%1"=="scan" (
    python git_file_manager.py --scan
    goto :end
)

if "%1"=="lists" (
    python git_file_manager.py --generate-lists --quiet
    goto :end
)

if "%1"=="gitignore" (
    python git_file_manager.py --create-gitignore --quiet
    goto :end
)

if "%1"=="backup" (
    python git_file_manager.py --backup-large --quiet
    goto :end
)

if "%1"=="clean" (
    python git_file_manager.py --clean-generated --dry-run --quiet
    set /p confirm="确认删除? (y/N): "
    if /i "%confirm%"=="y" (
        python git_file_manager.py --clean-generated --quiet
    )
    goto :end
)

if "%1"=="all" (
    python git_file_manager.py --scan
    python git_file_manager.py --generate-lists --quiet
    python git_file_manager.py --create-gitignore --quiet
    python git_file_manager.py --backup-large --quiet
    goto :end
)

echo ❌ 未知的命令: %1
echo.
echo 使用 'git_manager.bat' 查看帮助信息

:end
pause