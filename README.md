# MacPush

> 轻量级 macOS 通知转发器 — 将 Mac 上的通知实时推送到 Telegram 或邮箱

MacPush 是一个驻留在 macOS 菜单栏的小工具，它会实时监测系统通知中心数据库，将新通知通过 **Telegram Bot** 或 **电子邮件 (SMTP)** 转发到你的手机或其他设备。

**零第三方依赖**，纯 Python 标准库 + 原生 Objective-C 菜单栏 App，轻量、安全、开箱即用。

## 功能特性

- 🔔 **实时监测** — 轮询 macOS 通知中心 SQLite 数据库，新通知秒级到达
- ✈️ **Telegram 推送** — 通过 Telegram Bot API 推送通知
- ✉️ **邮件推送** — 通过 SMTP 协议发送通知邮件
- 🖥️ **菜单栏控制** — 原生 macOS 菜单栏 App，一键启停、查看状态
- ⚙️ **Web 配置面板** — 内置 WebKit 设置界面，可视化配置推送渠道
- 🔇 **智能免打扰** — 检测到用户正在使用 Mac 时自动暂停转发
- 🚀 **开机自启动** — 支持 LaunchAgent 开机自动运行
- 🚫 **应用过滤** — 可排除指定 App 的通知
- 📋 **运行日志** — Web 面板实时查看转发日志

## 截图

<!-- TODO: 添加截图 -->

## 快速开始

### 环境要求

- macOS 11.0+（Big Sur 及以上，需要 SF Symbols 支持）
- Python 3（系统自带即可，无需额外安装）
- Xcode Command Line Tools（用于编译 Objective-C 菜单栏 App）

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/MacPush.git
cd MacPush
```

### 2. 授予完全磁盘访问权限

由于 macOS 的安全策略 (TCC)，系统通知数据库是受保护的。你需要授权终端访问它：

1. 打开 **系统设置 > 隐私与安全 > 完全磁盘访问权限**
2. 将运行此程序的终端（Terminal / iTerm2）或编译后的 `MacPush.app` 添加进去并开启权限

### 3. 构建并安装 App

```bash
chmod +x build_dist.sh
./build_dist.sh
cp -R MacPush.app /Applications/
```

### 4. 配置推送渠道

1. 从菜单栏点击 🔔 图标 → 选择「设置」
2. 在弹出的 Web 配置面板中，启用并填写 Telegram Bot Token / Chat ID，或邮箱 SMTP 信息
3. 点击「测试连接」验证配置
4. 点击「保存全部配置」

### 5. 启动服务

在菜单栏下拉菜单中，打开「启用转发服务」开关即可。

## 推送渠道配置指南

### Telegram Bot

1. 在 Telegram 中搜索 `@BotFather`，发送 `/newbot` 创建机器人，获得 **Bot Token**
2. 搜索 `@userinfobot`，发送任意消息获取你的 **Chat ID**
3. 确保你已与新创建的机器人发起过对话（点击 Start）

### 邮件 (SMTP)

以 QQ 邮箱为例：

1. **SMTP 服务器**：`smtp.qq.com`，**端口**：`465`
2. **发件人邮箱**：你的完整 QQ 邮箱地址
3. **SMTP 授权码**：在 QQ 邮箱设置 → 账户 → POP3/SMTP 服务中获取 16 位授权码（非邮箱登录密码）
4. **收件人邮箱**：接收通知的邮箱地址

## 项目结构

```
MacPush/
├── MenuBarApp.m              # Objective-C 菜单栏 App 源码
├── forwarder.py              # 通知转发守护进程（核心逻辑）
├── config_helper.py          # 配置管理助手
├── web_config.py             # Web 配置面板 HTTP 服务器
├── build_dist.sh             # 构建脚本（编译并打包 .app）
├── create_icns.sh            # 图标生成脚本
├── com.a123.macpush.forwarder.plist  # LaunchAgent 模板
├── config.example.json       # 配置文件示例
├── app_icon.icns             # 应用图标
├── app_icon_transparent.png  # 图标源文件
└── web/
    ├── index.html            # 配置面板页面
    ├── style.css             # 配置面板样式
    └── app.js                # 配置面板逻辑
```

## 技术原理

1. **通知监测**：macOS 所有通知缓存在 SQLite 数据库中，路径为 `$(getconf DARWIN_USER_DIR)/com.apple.notificationcenter/db2/db`
2. **数据解析**：数据库 `record` 表的 `data` 列是二进制属性列表 (bplist)，通过 Python `plistlib` 解析出标题、副标题、正文
3. **防重机制**：处理完通知后，将最新 `rec_id` 写入 `~/.last_id`，重启时从该 ID 继续
4. **智能免打扰**：通过 `ioreg` 读取 HIDIdleTime，判断用户是否活跃
5. **推送发送**：Telegram 使用 `urllib.request` 调用 Bot API；邮件使用 `smtplib` SSL 连接

## 开机自启动

### 方式一：通过 App 设置面板（推荐）

在 MacPush 菜单栏 → 设置 → 全局高级设置中开启「开机自启动」开关，App 会自动创建 LaunchAgent。

### 方式二：手动配置 LaunchAgent（仅转发守护进程）

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

## 从源码构建图标

如果你修改了 `app_icon_transparent.png`，可以重新生成 `.icns` 文件：

```bash
chmod +x create_icns.sh
./create_icns.sh
```

## 配置文件

运行时配置存储在 `~/Library/Application Support/MacPush/config.json`，由 App 自动创建和管理。参考 `config.example.json` 了解配置结构。

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！
