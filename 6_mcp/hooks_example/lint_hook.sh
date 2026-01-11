#!/bin/bash
# lint_hook.sh - 在 git commit 前執行 lint 檢查
#
# 這個腳本可以被 Hook 呼叫，用來驗證程式碼品質
#
# 用法：在 .claude/settings.json 中設定：
# {
#   "hooks": {
#     "PreToolUse": [
#       {
#         "matcher": "Bash",
#         "hooks": [
#           {
#             "type": "command",
#             "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'git commit'; then ./lint_hook.sh; fi"
#           }
#         ]
#       }
#     ]
#   }
# }

echo "Running lint check before commit..."

# 檢查是否有 package.json（Node.js 專案）
if [ -f "package.json" ]; then
    echo "Found package.json, running npm run lint..."
    npm run lint
    LINT_RESULT=$?

    if [ $LINT_RESULT -ne 0 ]; then
        echo "ERROR: Lint check failed! Please fix the issues before committing."
        exit 1
    fi
fi

# 檢查是否有 Python 檔案
PYTHON_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
if [ -n "$PYTHON_FILES" ]; then
    echo "Found Python files, running ruff check..."
    ruff check $PYTHON_FILES
    RUFF_RESULT=$?

    if [ $RUFF_RESULT -ne 0 ]; then
        echo "ERROR: Ruff check failed! Please fix the issues before committing."
        exit 1
    fi
fi

echo "All checks passed!"
exit 0
