# MacPush

> 轻量级 macOS 通知转发器 — 将 Mac 上的通知实时推送到邮箱或 Telegram
>
> Lightweight macOS notification forwarder — push Mac notifications to Email or Telegram in real time

[简体中文](#简体中文) | [English](#english)

---

## 简体中文

MacPush 是一个驻留在 macOS 菜单栏的小工具，它会实时监测系统通知中心数据库，将新通知通过 **电子邮件 (SMTP)** 或 **Telegram Bot** 转发到你的手机或其他设备。

**零第三方依赖**，纯 Python 标准库 + 原生 Objective-C 菜单栏 App，轻量、安全、开箱即用。

### 功能特性

- 🔔 **实时监测** — 轮询 macOS 通知中心 SQLite 数据库，新通知秒级到达
- ✉️ **邮件推送** — 通过 SMTP 协议发送通知邮件
- ✈️ **Telegram 推送** — 通过 Telegram Bot API 推送通知
- 🖥️ **菜单栏控制** — 原生 macOS 菜单栏 App，一键启停、查看状态
- ⚙️ **Web 配置面板** — 内置 WebKit 设置界面，可视化配置推送渠道
- 🔇 **智能免打扰** — 检测到用户正在使用 Mac 时自动暂停转发
- 🚀 **开机自启动** — 支持 LaunchAgent 开机自动运行
- 🚫 **应用过滤** — 可排除指定 App 的通知
- 📋 **运行日志** — Web 面板实时查看转发日志

### 快速开始

#### 环境要求

- macOS 11.0+（Big Sur 及以上，需要 SF Symbols 支持）
- Python 3（系统自带即可，无需额外安装）
- Xcode Command Line Tools（用于编译 Objective-C 菜单栏 App）

#### 1. 下载安装

**方式一：下载 DMG 安装包（推荐）**

1. 前往 [Releases 页面](https://github.com/xmcter/MacPush/releases) 下载最新的 `MacPush.dmg`
2. 双击打开 DMG，将 MacPush.app 拖入 Applications 文件夹快捷方式
3. 打开「应用程序」文件夹，启动 MacPush

> ⚠️ **首次打开提示「已损坏」或「无法验证开发者」怎么办？**
>
> MacPush 是开源项目，没有购买 Apple 开发者证书，所以 macOS Gatekeeper 会拦截。请执行以下任一方法解除：
>
> **方法一（推荐）**：在终端中运行：
> ```bash
> sudo xattr -cr /Applications/MacPush.app
> ```
>
> **方法二**：右键点击 MacPush.app → 选择「打开」→ 在弹窗中再次点击「打开」

**方式二：从源码构建**

```bash
git clone https://github.com/xmcter/MacPush.git
cd MacPush
chmod +x build_dist.sh
./build_dist.sh
cp -R MacPush.app /Applications/
```

#### 2. 授予完全磁盘访问权限

由于 macOS 的安全策略 (TCC)，系统通知数据库是受保护的。你需要授权 App 访问它：

1. 打开 **系统设置 > 隐私与安全 > 完全磁盘访问权限**
2. 将 `MacPush.app` 添加进去并开启权限

#### 3. 配置推送渠道

1. 从菜单栏点击 🔔 图标 → 选择「设置」
2. 在弹出的 Web 配置面板中，启用并填写邮箱 SMTP 信息，或 Telegram Bot Token / Chat ID
3. 点击「测试连接」验证配置
4. 点击「保存全部配置」

#### 4. 启动服务

在菜单栏下拉菜单中，打开「启用转发服务」开关即可。

### 推送渠道配置指南

#### 邮件 (SMTP)

以 QQ 邮箱为例：

1. **SMTP 服务器**：`smtp.qq.com`，**端口**：`465`
2. **发件人邮箱**：你的完整 QQ 邮箱地址
3. **SMTP 授权码**：在 QQ 邮箱设置 → 账户 → POP3/SMTP 服务中获取 16 位授权码（非邮箱登录密码）
4. **收件人邮箱**：接收通知的邮箱地址

#### Telegram Bot

1. 在 Telegram 中搜索 `@BotFather`，发送 `/newbot` 创建机器人，获得 **Bot Token**
2. 搜索 `@userinfobot`，发送任意消息获取你的 **Chat ID**
3. 确保你已与新创建的机器人发起过对话（点击 Start）

### 项目结构

```
MacPush/
├── MenuBarApp.m              # Objective-C 菜单栏 App 源码
├── forwarder.py              # 通知转发守护进程（核心逻辑）
├── config_helper.py          # 配置管理助手
├── web_config.py             # Web 配置面板 HTTP 服务器
├── build_dist.sh             # 构建脚本（编译并打包 .app）
├── build_dmg.sh              # DMG 安装包构建脚本
├── create_icns.sh            # 图标生成脚本
├── make_dmg_bg.py            # DMG 背景图生成脚本
├── create_ds_store.py        # DMG .DS_Store 生成脚本
├── com.a123.macpush.forwarder.plist  # LaunchAgent 模板
├── config.example.json       # 配置文件示例
├── app_icon.icns             # 应用图标
├── app_icon_transparent.png  # 图标源文件
├── dmg_background.png        # DMG 背景图
└── web/
    ├── index.html            # 配置面板页面
    ├── style.css             # 配置面板样式
    └── app.js                # 配置面板逻辑
```

### 技术原理

1. **通知监测**：macOS 所有通知缓存在 SQLite 数据库中，路径为 `$(getconf DARWIN_USER_DIR)/com.apple.notificationcenter/db2/db`
2. **数据解析**：数据库 `record` 表的 `data` 列是二进制属性列表 (bplist)，通过 Python `plistlib` 解析出标题、副标题、正文
3. **防重机制**：处理完通知后，将最新 `rec_id` 写入 `~/Library/Application Support/MacPush/.last_id`，重启时从该 ID 继续
4. **智能免打扰**：通过 `ioreg` 读取 HIDIdleTime，判断用户是否活跃
5. **推送发送**：邮件使用 `smtplib` SSL 连接；Telegram 使用 `urllib.request` 调用 Bot API

### 开机自启动

**方式一：通过 App 设置面板（推荐）**

在 MacPush 菜单栏 → 设置 → 全局高级设置中开启「开机自启动」开关，App 会自动创建 LaunchAgent。

**方式二：手动配置 LaunchAgent（仅转发守护进程）**

如果你只需要后台转发服务（不需要菜单栏 App），可以使用提供的 plist 模板：

```bash
# 编辑 com.a123.macpush.forwarder.plist，将 /path/to/MacPush 替换为实际路径
cp com.a123.macpush.forwarder.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.a123.macpush.forwarder.plist
```

停止服务：
```bash
launchctl unload ~/Library/LaunchAgents/com.a123.macpush.forwarder.plist
```

### 从源码构建图标

如果你修改了 `app_icon_transparent.png`，可以重新生成 `.icns` 文件：

```bash
chmod +x create_icns.sh
./create_icns.sh
```

### 配置文件

运行时配置存储在 `~/Library/Application Support/MacPush/config.json`，由 App 自动创建和管理。参考 `config.example.json` 了解配置结构。

### 许可证

[MIT License](LICENSE)

### 贡献

欢迎提交 Issue 和 Pull Request！

---

## English

MacPush is a lightweight macOS menu bar utility that monitors the system notification center database in real time and forwards new notifications to your phone or other devices via **Email (SMTP)** or **Telegram Bot**.

**Zero third-party dependencies** — pure Python standard library + native Objective-C menu bar app. Lightweight, secure, ready to use out of the box.

### Features

- 🔔 **Real-time Monitoring** — Polls the macOS notification center SQLite database, new notifications arrive in seconds
- ✉️ **Email Push** — Sends notification emails via SMTP
- ✈️ **Telegram Push** — Pushes notifications via Telegram Bot API
- 🖥️ **Menu Bar Control** — Native macOS menu bar app, one-click start/stop, status at a glance
- ⚙️ **Web Config Panel** — Built-in WebKit settings UI for visual channel configuration
- 🔇 **Smart Do-Not-Disturb** — Auto-pauses forwarding when the user is actively using the Mac
- 🚀 **Launch at Login** — Supports LaunchAgent auto-start
- 🚫 **App Filtering** — Exclude notifications from specific apps
- 📋 **Run Logs** — View forwarding logs in real time on the web panel

### Quick Start

#### Requirements

- macOS 11.0+ (Big Sur and above, requires SF Symbols support)
- Python 3 (pre-installed on macOS, no extra installation needed)
- Xcode Command Line Tools (to compile the Objective-C menu bar app)

#### 1. Download & Install

**Option A: Download DMG (Recommended)**

1. Go to the [Releases page](https://github.com/xmcter/MacPush/releases) and download the latest `MacPush.dmg`
2. Double-click to open the DMG, drag MacPush.app to the Applications folder shortcut
3. Open the Applications folder and launch MacPush

> ⚠️ **"Damaged" or "Unidentified Developer" warning on first launch?**
>
> MacPush is an open-source project without a paid Apple Developer certificate, so macOS Gatekeeper will block it. Use either method below to bypass:
>
> **Method 1 (Recommended)**: Run in Terminal:
> ```bash
> sudo xattr -cr /Applications/MacPush.app
> ```
>
> **Method 2**: Right-click MacPush.app → select "Open" → click "Open" again in the dialog

**Option B: Build from Source**

```bash
git clone https://github.com/xmcter/MacPush.git
cd MacPush
chmod +x build_dist.sh
./build_dist.sh
cp -R MacPush.app /Applications/
```

#### 2. Grant Full Disk Access

Due to macOS security policy (TCC), the system notification database is protected. You need to authorize the app to access it:

1. Open **System Settings > Privacy & Security > Full Disk Access**
2. Add `MacPush.app` and enable the permission

#### 3. Configure Push Channels

1. Click the 🔔 icon in the menu bar → select "Settings"
2. In the web config panel, enable and fill in your Email SMTP info or Telegram Bot Token / Chat ID
3. Click "Test Connection" to verify
4. Click "Save All Settings"

#### 4. Start the Service

Toggle on "Enable Forwarding" in the menu bar dropdown menu.

### Push Channel Setup Guide

#### Email (SMTP)

Using QQ Mail as an example:

1. **SMTP Server**: `smtp.qq.com`, **Port**: `465`
2. **Sender Email**: Your full QQ email address
3. **SMTP Auth Code**: Obtain the 16-digit authorization code from QQ Mail Settings → Account → POP3/SMTP Service (not your email login password)
4. **Recipient Email**: The email address to receive notifications

#### Telegram Bot

1. Search for `@BotFather` in Telegram, send `/newbot` to create a bot and get the **Bot Token**
2. Search for `@userinfobot`, send any message to get your **Chat ID**
3. Make sure you have started a conversation with your new bot (click Start)

### Project Structure

```
MacPush/
├── MenuBarApp.m              # Objective-C menu bar app source
├── forwarder.py              # Notification forwarder daemon (core logic)
├── config_helper.py          # Config management helper
├── web_config.py             # Web config panel HTTP server
├── build_dist.sh             # Build script (compiles and packages .app)
├── build_dmg.sh              # DMG installer build script
├── create_icns.sh            # Icon generation script
├── make_dmg_bg.py            # DMG background image generator
├── create_ds_store.py        # DMG .DS_Store generator
├── com.a123.macpush.forwarder.plist  # LaunchAgent template
├── config.example.json       # Config file example
├── app_icon.icns             # App icon
├── app_icon_transparent.png  # Icon source file
├── dmg_background.png        # DMG background image
└── web/
    ├── index.html            # Config panel page
    ├── style.css             # Config panel styles
    └── app.js                # Config panel logic
```

### How It Works

1. **Notification Monitoring**: All macOS notifications are cached in a SQLite database at `$(getconf DARWIN_USER_DIR)/com.apple.notificationcenter/db2/db`
2. **Data Parsing**: The `data` column in the database `record` table is a binary property list (bplist), parsed via Python `plistlib` to extract title, subtitle, and body
3. **Deduplication**: After processing, the latest `rec_id` is written to `~/Library/Application Support/MacPush/.last_id`; on restart, it resumes from that ID
4. **Smart Do-Not-Disturb**: Reads HIDIdleTime via `ioreg` to determine if the user is active
5. **Push Delivery**: Email uses `smtplib` SSL connection; Telegram uses `urllib.request` to call the Bot API

### Launch at Login

**Option A: Via App Settings Panel (Recommended)**

In MacPush menu bar → Settings → Advanced Settings, toggle on "Launch at Login". The app will automatically create a LaunchAgent.

**Option B: Manual LaunchAgent (forwarder daemon only)**

If you only need the background forwarding service (without the menu bar app), use the provided plist template:

```bash
# Edit com.a123.macpush.forwarder.plist, replace /path/to/MacPush with the actual path
cp com.a123.macpush.forwarder.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.a123.macpush.forwarder.plist
```

Stop the service:
```bash
launchctl unload ~/Library/LaunchAgents/com.a123.macpush.forwarder.plist
```

### Building Icon from Source

If you modified `app_icon_transparent.png`, you can regenerate the `.icns` file:

```bash
chmod +x create_icns.sh
./create_icns.sh
```

### Configuration File

Runtime config is stored at `~/Library/Application Support/MacPush/config.json`, automatically created and managed by the app. See `config.example.json` for the config structure.

### License

[MIT License](LICENSE)

### Contributing

Issues and Pull Requests are welcome!
