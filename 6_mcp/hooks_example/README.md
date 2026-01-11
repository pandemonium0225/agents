# Claude Code Hooks 範例

Hooks 是在特定事件發生時自動執行的 shell 指令。

## 檔案結構

```
hooks_example/
├── .claude/
│   └── settings.json    ← Hook 設定
├── lint_hook.sh         ← Lint 檢查腳本
├── safety_hook.sh       ← 安全檢查腳本
└── README.md
```

## Hook 類型

| Hook 類型 | 觸發時機 | 用途 |
|-----------|----------|------|
| `PreToolUse` | 工具執行**前** | 驗證、阻止危險操作 |
| `PostToolUse` | 工具執行**後** | 記錄日誌、後處理 |
| `Notification` | 需要通知時 | 桌面通知 |
| `Stop` | Claude 停止時 | 清理、報告 |

## 可用環境變數

Hook 腳本可以使用這些環境變數：

| 變數 | 說明 |
|------|------|
| `CLAUDE_TOOL_NAME` | 工具名稱（如 Bash, Edit） |
| `CLAUDE_TOOL_INPUT` | 工具的輸入參數 |
| `CLAUDE_NOTIFICATION_MESSAGE` | 通知訊息內容 |

## 範例 1：記錄日誌

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[$(date)] Bash: $CLAUDE_TOOL_INPUT\" >> /tmp/claude.log"
          }
        ]
      }
    ]
  }
}
```

## 範例 2：阻止危險操作

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./safety_hook.sh \"$CLAUDE_TOOL_INPUT\""
          }
        ]
      }
    ]
  }
}
```

如果 `safety_hook.sh` 回傳非零 exit code，操作會被阻止。

## 範例 3：Commit 前執行 Lint

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'git commit'; then ./lint_hook.sh; fi"
          }
        ]
      }
    ]
  }
}
```

## 使用方式

1. 將 `.claude/settings.json` 複製到你的專案根目錄
2. 將需要的 hook 腳本複製過去
3. 確保腳本有執行權限：`chmod +x *.sh`
4. Claude Code 會自動讀取設定

## 流程圖

```
使用者請求 → Claude 決定用工具
                   │
                   ▼
            PreToolUse Hook
            （可以阻止操作）
                   │
                   ▼ (exit 0 才繼續)
              執行工具
                   │
                   ▼
            PostToolUse Hook
            （記錄、後處理）
                   │
                   ▼
              回傳結果
```
