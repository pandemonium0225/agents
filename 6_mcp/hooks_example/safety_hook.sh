#!/bin/bash
# safety_hook.sh - 阻止危險的 git 操作
#
# 這個腳本檢查並阻止可能有危險的指令
#
# 設定方式：
# {
#   "hooks": {
#     "PreToolUse": [
#       {
#         "matcher": "Bash",
#         "hooks": [
#           {
#             "type": "command",
#             "command": "./safety_hook.sh \"$CLAUDE_TOOL_INPUT\""
#           }
#         ]
#       }
#     ]
#   }
# }

INPUT="$1"

# 危險指令清單
DANGEROUS_PATTERNS=(
    "git push.*--force"
    "git push.*-f"
    "git reset --hard"
    "rm -rf /"
    "rm -rf ~"
    "DROP TABLE"
    "DELETE FROM.*WHERE 1=1"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if echo "$INPUT" | grep -qE "$pattern"; then
        echo "BLOCKED: Dangerous command detected!"
        echo "Pattern matched: $pattern"
        echo "Command was: $INPUT"
        exit 1
    fi
done

echo "Safety check passed"
exit 0
