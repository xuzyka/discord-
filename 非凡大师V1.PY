// ==UserScript==
// @name         非凡大师V1
// @namespace    http://tampermonkey.net/
// @version      4.0
// @description  Discord AI自动回复机器人
// @author       Your Name
// @match        https://discord.com/*
// @match        https://ptb.discord.com/*
// @match        https://canary.discord.com/*
// @grant        GM_setValue
// @grant        GM_getValue
// ==/UserScript==

(function() {
    'use strict';

    // 注入样式
    const style = document.createElement('style');
    style.textContent = `
        .discord-bot {
            position: fixed;
            top: 20px;
            right: 20px;
            width: 400px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            z-index: 9999;
            font-family: Arial, sans-serif;
            transition: all 0.3s ease;
        }

        .discord-bot.dark-mode {
            background: #2f3136;
            color: #fff;
        }

        .discord-bot.minimized {
            width: 200px;
            height: 40px;
            overflow: hidden;
        }

        .title-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px;
            background: #5865f2;
            color: white;
            border-radius: 8px 8px 0 0;
            cursor: move;
        }

        .title-bar h2 {
            margin: 0;
            font-size: 16px;
        }

        .control-buttons {
            display: flex;
            gap: 5px;
        }

        .control-buttons button {
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            padding: 2px 5px;
            border-radius: 3px;
            transition: background-color 0.2s;
        }

        .control-buttons button:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        .main-content {
            padding: 15px;
        }

        .section {
            margin-bottom: 20px;
        }

        .section-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #5865f2;
        }

        .dark-mode .section-title {
            color: #fff;
        }

        .token-list, .channel-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-height: 200px;
            overflow-y: auto;
        }

        .token-item, .channel-card {
            background: #f5f5f5;
            border-radius: 5px;
            padding: 10px;
            transition: all 0.2s;
        }

        .dark-mode .token-item, .dark-mode .channel-card {
            background: #40444b;
        }

        .token-header, .channel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
        }

        .token-body, .channel-body {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        input[type="text"], input[type="time"], input[type="number"], textarea {
            padding: 5px;
            border: 1px solid #ddd;
            border-radius: 3px;
            background: white;
            color: black;
        }

        .dark-mode input[type="text"], .dark-mode input[type="time"],
        .dark-mode input[type="number"], .dark-mode textarea {
            background: #2f3136;
            border-color: #202225;
            color: white;
        }

        button {
            padding: 5px 10px;
            background: #5865f2;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        button:hover {
            background: #4752c4;
        }

        .add-token, .add-channel {
            width: 100%;
            margin-top: 5px;
        }

        .status-bar {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 10px;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 5px;
        }

        .dark-mode .status-bar {
            background: #40444b;
        }

        .status-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #ff5555;
        }

        .status-indicator.running {
            background: #55ff55;
        }

        .log-container {
            margin-top: 10px;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 5px;
            max-height: 150px;
            overflow-y: auto;
        }

        .dark-mode .log-container {
            background: #40444b;
        }

        .log-item {
            margin-bottom: 5px;
            font-size: 12px;
        }

        .log-item.error {
            color: #ff5555;
        }

        .log-item.warning {
            color: #ffaa55;
        }

        .channel-progress {
            height: 4px;
            background: #ddd;
            border-radius: 2px;
            margin-top: 5px;
            overflow: hidden;
        }

        .dark-mode .channel-progress {
            background: #202225;
        }

        .progress-bar {
            height: 100%;
            background: #5865f2;
            transition: width 0.3s ease;
        }

        .hidden {
            display: none;
        }

        /* 动画效果 */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .discord-bot {
            animation: fadeIn 0.3s ease;
        }

        .minimized {
            transform-origin: top right;
            animation: minimize 0.3s ease;
        }

        @keyframes minimize {
            from {
                transform: scale(1);
            }
            to {
                transform: scale(0.8);
            }
        }

        .message-count-settings {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 5px;
        }

        .target-message-count {
            width: 120px;
        }

        .message-count-display {
            font-size: 12px;
            color: #666;
        }

        .dark-mode .message-count-display {
            color: #aaa;
        }

        .channel-progress {
            margin-top: 10px;
            height: 6px;
            background: #eee;
            border-radius: 3px;
            overflow: hidden;
        }

        .dark-mode .channel-progress {
            background: #2f3136;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #5865f2, #7289da);
            transition: width 0.3s ease;
        }

        .template-help-toggle {
            margin: 5px 0;
        }

        .template-help {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            font-size: 12px;
        }

        .dark-mode .template-help {
            background: #2f3136;
            color: #fff;
        }

        .template-help pre {
            margin: 0;
            white-space: pre-wrap;
            font-family: monospace;
        }

        .show-template-help {
            font-size: 12px;
            padding: 3px 8px;
        }

        .message-settings {
            background: #f8f9fa;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
        }

        .dark-mode .message-settings {
            background: #2f3136;
        }

        .variable-toggles {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            margin-bottom: 10px;
        }

        .variable-toggles label {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 12px;
        }

        .preset-values {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
        }

        .preset-values input {
            padding: 4px 8px;
            font-size: 12px;
        }

        .preset-values input:disabled {
            background: #eee;
            cursor: not-allowed;
        }

        .dark-mode .preset-values input:disabled {
            background: #202225;
        }

        .push-settings {
            padding: 10px;
            background: #f5f5f5;
            border-radius: 5px;
            margin-top: 10px;
        }

        .dark-mode .push-settings {
            background: #2f3136;
        }

        .push-options {
            margin: 10px 0;
            display: flex;
            gap: 10px;
        }

        .periodic-push-settings {
            margin-top: 10px;
            padding: 10px;
            background: rgba(0, 0, 0, 0.05);
            border-radius: 5px;
            display: none;
        }

        .dark-mode .periodic-push-settings {
            background: rgba(255, 255, 255, 0.05);
        }

        .setting-item {
            margin: 5px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .push-content-options {
            margin-top: 10px;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 5px;
        }

        .push-interval {
            width: 80px;
        }
    `;
    document.head.appendChild(style);

    class DiscordBot {
        constructor() {
            this.container = document.createElement('div');
            this.container.className = 'discord-bot';
            this.container.innerHTML = `
                <div class="title-bar">
                    <h2>Discord AI Bot</h2>
                    <div class="control-buttons">
                        <button class="minimize-btn">_</button>
                        <button class="dark-mode-btn">🌙</button>
                    </div>
                </div>
                <div class="main-content">
                    <div class="section">
                        <div class="section-title">Token管理</div>
                        <div class="token-list"></div>
                        <button class="add-token">添加Token</button>
                    </div>
                    <div class="section">
                        <div class="section-title">频道管理</div>
                        <div class="channel-list"></div>
                        <button class="add-channel">添加频道</button>
                    </div>
                    <div class="section">
                        <div class="section-title">发送设置</div>
                        <div class="send-settings">
                            <div>
                                <label>最小间隔(秒)</label>
                                <input type="number" class="min-interval" min="1" value="60">
                            </div>
                            <div>
                                <label>最大间隔(秒)</label>
                                <input type="number" class="max-interval" min="1" value="180">
                            </div>
                            <div>
                                <label>
                                    <input type="checkbox" class="enable-time-control">
                                    启用时间控制
                                </label>
                            </div>
                            <div class="time-control hidden">
                                <div>
                                    <label>开始时间</label>
                                    <input type="time" class="start-time" value="09:00">
                                </div>
                                <div>
                                    <label>结束时间</label>
                                    <input type="time" class="end-time" value="22:00">
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="section">
                        <button class="start-btn">开始发送</button>
                        <button class="stop-btn hidden">停止发送</button>
                    </div>
                    <div class="status-bar">
                        <div class="status-indicator"></div>
                        <div class="status-text">已停止</div>
                    </div>
                    <div class="log-container"></div>
                    <div class="section">
                        <div class="section-title">推送设置</div>
                        <div class="push-settings">
                            <input type="text" class="push-channel-id" placeholder="推送频道ID">
                            <div class="push-options">
                                <label>
                                    <input type="checkbox" class="enable-push">
                                    启用运行状态推送
                                </label>
                                <label>
                                    <input type="checkbox" class="enable-periodic-push">
                                    启用定期推送
                                </label>
                            </div>
                            <div class="periodic-push-settings">
                                <div class="setting-item">
                                    <label>推送间隔(分钟)</label>
                                    <input type="number" class="push-interval" min="1" value="30">
                                </div>
                                <div class="push-content-options">
                                    <label>
                                        <input type="checkbox" class="push-total-messages" checked>
                                        总消息数
                                    </label>
                                    <label>
                                        <input type="checkbox" class="push-channel-status" checked>
                                        频道状态
                                    </label>
                                    <label>
                                        <input type="checkbox" class="push-error-messages" checked>
                                        错误信息
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(this.container);

            // 初始化属性
            this.tokens = [];
            this.channels = [];
            this.minInterval = 60;
            this.maxInterval = 180;
            this.isRunning = false;
            this.timers = [];
            this.messageCount = 0;
            this.enableTimeControl = false;
            this.startTime = '09:00';
            this.endTime = '22:00';
            this.lastSaveTime = Date.now();
            this.autoSaveInterval = 30000; // 5秒自动保存一次

            // 初始化表情变量
            this.templateVariables = {
                '打招呼': ['早安', '午安', '晚安', 'Hi', 'Hello', '嗨'],
                '称赞': ['真棒', '太厉害了', '好厉害', '太强了', '好棒啊'],
                '结尾': ['期待你的回复~', '和你聊天真开心~', '下次再聊哦~', '爱你哦~', '拜拜~']
            };

            // 移除表情选项
            this.defaultEmoji = {};

            // 更新模板说明
            this.templateHelp = `
简单的变量使用说明：

1. 基础变量：
[打招呼] - 随机一个打招呼方式
[称赞] - 随机一个称赞语
[结尾] - 随机一个结尾语

2. 时间变量：
[时间] - 当前时间
[日期] - 当前日期

3. 数字变量：
[数字1-100] - 生成1到100之间的随机数

示例消息：
[打招呼]
现在是[时间]，这是第[数字1-100]条消息~
[称赞]！[结尾]

你也可以自定义变量组，格式：
<变量名=选项1|选项2|选项3>
例如：<心情=开心|快乐|激动|兴奋>

完整示例：
[打招呼]，我今天感觉<心情>，聊天真好 [结尾]
            `.trim();

            // 加载设置
            this.loadSettings();

            // 绑定事件
            this.bindEvents();

            // 更新UI
            this.updateUI();

            // 设置自动保存
            setInterval(() => this.autoSave(), this.autoSaveInterval);

            // 加载主题
            if (GM_getValue('darkMode', false)) {
                this.container.classList.add('dark-mode');
            }

            // 加载最小化状态
            if (GM_getValue('minimized', false)) {
                this.container.classList.add('minimized');
            }

            const additionalStyle = document.createElement('style');
            additionalStyle.textContent += `
                .message-settings {
                    background: #f8f9fa;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 10px 0;
                }

                .dark-mode .message-settings {
                    background: #2f3136;
                }

                .variable-toggles {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 8px;
                    margin-bottom: 10px;
                }

                .variable-toggles label {
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    font-size: 12px;
                }

                .preset-values {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 8px;
                }

                .preset-values input {
                    padding: 4px 8px;
                    font-size: 12px;
                }

                .preset-values input:disabled {
                    background: #eee;
                    cursor: not-allowed;
                }

                .dark-mode .preset-values input:disabled {
                    background: #202225;
                }
            `;
            document.head.appendChild(additionalStyle);

            // 添加推送相关属性
            this.pushChannelId = GM_getValue('pushChannelId', '');
            this.enablePush = GM_getValue('enablePush', false);
            this.enablePeriodicPush = GM_getValue('enablePeriodicPush', false);
            this.pushInterval = GM_getValue('pushInterval', 30);
            this.pushTotalMessages = GM_getValue('pushTotalMessages', true);
            this.pushChannelStatus = GM_getValue('pushChannelStatus', true);
            this.pushErrorMessages = GM_getValue('pushErrorMessages', true);
            this.pushTimer = null;
            this.errorMessages = [];
        }

        loadSettings() {
            try {
                const savedTokens = GM_getValue('tokens');
                if (Array.isArray(savedTokens)) {
                    this.tokens = savedTokens;
                }

                const savedChannels = GM_getValue('channels');
                if (Array.isArray(savedChannels)) {
                    this.channels = savedChannels;
                }

                this.minInterval = GM_getValue('minInterval', 60);
                this.maxInterval = GM_getValue('maxInterval', 300);
                this.startTime = GM_getValue('startTime', '00:00');
                this.endTime = GM_getValue('endTime', '23:59');
                this.enableTimeControl = GM_getValue('enableTimeControl', false);

                this.pushChannelId = GM_getValue('pushChannelId', '');
                this.enablePush = GM_getValue('enablePush', false);
                this.enablePeriodicPush = GM_getValue('enablePeriodicPush', false);
                this.pushInterval = GM_getValue('pushInterval', 30);
                this.pushTotalMessages = GM_getValue('pushTotalMessages', true);
                this.pushChannelStatus = GM_getValue('pushChannelStatus', true);
                this.pushErrorMessages = GM_getValue('pushErrorMessages', true);

                this.addLog('设置加载成功');
            } catch (error) {
                this.addLog('加载设置失败: ' + error.message, 'error');
                // 使用默认设置
                this.tokens = [];
                this.channels = [];
                this.minInterval = 60;
                this.maxInterval = 300;
                this.startTime = '00:00';
                this.endTime = '23:59';
                this.enableTimeControl = false;
                this.pushChannelId = '';
                this.enablePush = false;
                this.enablePeriodicPush = false;
                this.pushInterval = 30;
                this.pushTotalMessages = true;
                this.pushChannelStatus = true;
                this.pushErrorMessages = true;
            }
        }

        saveSettings() {
            try {
                GM_setValue('tokens', this.tokens);
                GM_setValue('channels', this.channels);
                GM_setValue('minInterval', this.minInterval);
                GM_setValue('maxInterval', this.maxInterval);
                GM_setValue('startTime', this.startTime);
                GM_setValue('endTime', this.endTime);
                GM_setValue('enableTimeControl', this.enableTimeControl);
                GM_setValue('pushChannelId', this.pushChannelId);
                GM_setValue('enablePush', this.enablePush);
                GM_setValue('enablePeriodicPush', this.enablePeriodicPush);
                GM_setValue('pushInterval', this.pushInterval);
                GM_setValue('pushTotalMessages', this.pushTotalMessages);
                GM_setValue('pushChannelStatus', this.pushChannelStatus);
                GM_setValue('pushErrorMessages', this.pushErrorMessages);

                this.lastSaveTime = Date.now();
                this.addLog('设置保存成功');
            } catch (error) {
                this.addLog('保存设置失败: ' + error.message, 'error');
            }
        }

        autoSave() {
            const now = Date.now();
            if (now - this.lastSaveTime >= this.autoSaveInterval) {
                this.saveSettings();
            }
        }

        validateSettings() {
            let isValid = true;
            const errors = [];

            // 验证Token
            if (this.tokens.length === 0) {
                errors.push('请添加至少一个Token');
                isValid = false;
            }

            // 验证频道
            if (this.channels.length === 0) {
                errors.push('请添加至少一个频道');
                isValid = false;
            }

            // 验证时间间隔
            if (this.minInterval <= 0 || this.maxInterval <= 0) {
                errors.push('时间间隔必须大于0');
                isValid = false;
            }

            if (this.minInterval > this.maxInterval) {
                errors.push('最小间隔不能大于最大间隔');
                isValid = false;
            }

            // 验证时间控制
            if (this.enableTimeControl) {
                if (!this.startTime || !this.endTime) {
                    errors.push('请设置开始和结束时间');
                    isValid = false;
                }
            }

            if (!isValid) {
                errors.forEach(error => this.addLog(error, 'error'));
            }

            return isValid;
        }

        async sendMessage(token, channel) {
            if (!channel.messages || channel.messages.length === 0) {
                this.addLog(`频道 ${channel.name || channel.id} 没有预设消息`, 'error');
                return;
            }

            // 检查是否达到目标消息数
            if (channel.sentMessageCount >= channel.targetMessageCount) {
                this.addLog(`频道 ${channel.name || channel.id} 已达到目标消息数量`, 'info');
                channel.enabled = false;
                this.updateUI();
                this.saveSettings();
                return;
            }

            this.currentChannelId = channel.id; // 添加这行来设置当前处理的频道ID
            const messageTemplate = channel.messages[Math.floor(Math.random() * channel.messages.length)];
            const processedMessage = this.processTemplate(messageTemplate);

            try {
                const response = await fetch(`https://discord.com/api/v9/channels/${channel.id}/messages`, {
                    method: 'POST',
                    headers: {
                        'Authorization': token.token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ content: processedMessage })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                channel.sentMessageCount = (channel.sentMessageCount || 0) + 1;
                this.messageCount++;
                this.updateUI();
                this.saveSettings();

                this.addLog(`成功发送消息到频道 ${channel.name || channel.id} (${channel.sentMessageCount}/${channel.targetMessageCount}): ${processedMessage}`);
            } catch (error) {
                this.addLog(`发送消息到频道 ${channel.name || channel.id} 失败: ${error.message}`, 'error');
            }
        }

        start() {
            if (this.isRunning) {
                this.addLog('已经在运行中', 'warning');
                return;
            }

            if (!this.validateSettings()) {
                return;
            }

            const enabledTokens = this.tokens.filter(t => t.token && t.enabled);
            const enabledChannels = this.channels.filter(c => c.id && c.enabled);

            this.isRunning = true;
            this.messageCount = 0;
            this.errorMessages = [];
            this.startTime = Date.now(); // 添加启动时间记录
            this.updateStatus();
            this.addLog('开始发送消息');

            const startMessage = `🚀 机器人已启动
━━━━━━━━━━━━━━━━━━━━━━
📊 初始配置
• 活跃频道: ${enabledChannels.length} 个
• 可用Token: ${enabledTokens.length} 个
• 发送间隔: ${this.minInterval}-${this.maxInterval} 秒
${this.enableTimeControl ? `• 运行时段: ${this.startTime}-${this.endTime}` : '• 全天运行'}
━━━━━━━━━━━━━━━━━━━━━━
⚙️ 推送设置
• ${this.enablePeriodicPush ? `每 ${this.pushInterval} 分钟推送一次状态` : '仅推送启动/停止状态'}`;

            this.sendPushMessage(startMessage);
            this.startPeriodicPush();

            for (const token of enabledTokens) {
                for (const channel of enabledChannels) {
                    const interval = Math.floor(Math.random() * (this.maxInterval - this.minInterval + 1)) + this.minInterval;
                    const timer = setInterval(() => {
                        if (!this.isRunning) return;
                        if (this.enableTimeControl && !this.isWithinTimeRange()) return;
                        this.sendMessage(token, channel);
                    }, interval * 1000);
                    this.timers.push(timer);
                }
            }

            this.container.querySelector('.start-btn').classList.add('hidden');
            this.container.querySelector('.stop-btn').classList.remove('hidden');
        }

        stop() {
            if (!this.isRunning) {
                this.addLog('没有在运行', 'warning');
                return;
            }

            const runTime = Math.floor((Date.now() - this.startTime) / 1000 / 60);
            const stopMessage = `🛑 机器人已停止
━━━━━━━━━━━━━━━━━━━━━━
📊 运行统计
• 运行时长: ${runTime} 分钟
• 总发送数: ${this.messageCount} 条
• 平均速度: ${(this.messageCount / runTime).toFixed(2)} 条/分钟
━━━━━━━━━━━━━━━━━━━━━━`;

            this.isRunning = false;
            this.timers.forEach(timer => clearInterval(timer));
            this.timers = [];
            this.updateStatus();
            this.addLog('停止发送消息');
            this.sendPushMessage(stopMessage);

            if (this.pushTimer) {
                clearInterval(this.pushTimer);
                this.pushTimer = null;
            }

            this.container.querySelector('.start-btn').classList.remove('hidden');
            this.container.querySelector('.stop-btn').classList.add('hidden');
        }

        isWithinTimeRange() {
            if (!this.enableTimeControl) return true;

            const now = new Date();
            const currentTime = now.getHours() * 60 + now.getMinutes();

            const [startHour, startMinute] = this.startTime.split(':').map(Number);
            const [endHour, endMinute] = this.endTime.split(':').map(Number);

            const startMinutes = startHour * 60 + startMinute;
            const endMinutes = endHour * 60 + endMinute;

            if (endMinutes >= startMinutes) {
                return currentTime >= startMinutes && currentTime <= endMinutes;
            } else {
                return currentTime >= startMinutes || currentTime <= endMinutes;
            }
        }

        updateUI() {
            // 更新Token列表
            const tokenList = this.container.querySelector('.token-list');
            tokenList.innerHTML = this.tokens.map((token, index) => this.createTokenItemHTML(token, index)).join('');

            // 更新频道列表
            const channelList = this.container.querySelector('.channel-list');
            channelList.innerHTML = this.channels.map((channel, index) => this.createChannelCardHTML(channel, index)).join('');

            // 更新发送设置
            this.container.querySelector('.min-interval').value = this.minInterval;
            this.container.querySelector('.max-interval').value = this.maxInterval;
            this.container.querySelector('.enable-time-control').checked = this.enableTimeControl;
            this.container.querySelector('.time-control').classList.toggle('hidden', !this.enableTimeControl);
            this.container.querySelector('.start-time').value = this.startTime;
            this.container.querySelector('.end-time').value = this.endTime;

            // 更新状态
            this.updateStatus();

            // 更新推送设置
            this.container.querySelector('.push-channel-id').value = this.pushChannelId;
            this.container.querySelector('.enable-push').checked = this.enablePush;
            this.container.querySelector('.enable-periodic-push').checked = this.enablePeriodicPush;
            this.container.querySelector('.push-interval').value = this.pushInterval;
            this.container.querySelector('.push-total-messages').checked = this.pushTotalMessages;
            this.container.querySelector('.push-channel-status').checked = this.pushChannelStatus;
            this.container.querySelector('.push-error-messages').checked = this.pushErrorMessages;

            // 显示/隐藏定期推送设置
            this.container.querySelector('.periodic-push-settings').style.display =
                this.enablePeriodicPush ? 'block' : 'none';
        }

        createTokenItemHTML(token, index) {
            return `
                <div class="token-item" data-index="${index}">
                    <div class="token-header">
                        <input type="checkbox" ${token.enabled ? 'checked' : ''}>
                        <button class="remove-token">删除</button>
                    </div>
                    <div class="token-body">
                        <input type="text" class="token-input" placeholder="Token" value="${token.token}">
                        <input type="text" class="token-note" placeholder="备注" value="${token.note}">
                    </div>
                </div>
            `;
        }

        createChannelCardHTML(channel, index) {
            return `
                <div class="channel-card" data-index="${index}">
                    <div class="channel-header">
                        <input type="checkbox" ${channel.enabled ? 'checked' : ''}>
                        <button class="remove-channel">删除</button>
                    </div>
                    <div class="channel-body">
                        <input type="text" class="channel-id" placeholder="频道ID" value="${channel.id}">
                        <input type="text" class="channel-name" placeholder="频道名称" value="${channel.name}">
                        <textarea class="channel-messages" placeholder="预设消息（每行一条）">${channel.messages.join('\n')}</textarea>
                        <div class="message-count-settings">
                            <input type="number" class="target-message-count" placeholder="目标消息数量" min="1000" max="10000" value="${channel.targetMessageCount || 1000}">
                            <span class="message-count-display">已发送: ${channel.sentMessageCount || 0}/${channel.targetMessageCount || 1000}</span>
                        </div>
                    </div>
                    <div class="channel-progress">
                        <div class="progress-bar" style="width: ${this.calculateProgress(channel)}%"></div>
                    </div>
                </div>
            `;
        }

        calculateProgress(channel) {
            if (!channel.targetMessageCount) return 0;
            const progress = ((channel.sentMessageCount || 0) / channel.targetMessageCount) * 100;
            return Math.min(progress, 100);
        }

        updateStatus() {
            const statusText = this.container.querySelector('.status-text');
            const statusIndicator = this.container.querySelector('.status-indicator');

            if (this.isRunning) {
                statusText.textContent = `运行中 - 已发送 ${this.messageCount} 条消息`;
                statusIndicator.classList.add('running');
            } else {
                statusText.textContent = '已停止';
                statusIndicator.classList.remove('running');
            }
        }

        addLog(message, type = 'info') {
            const logContainer = this.container.querySelector('.log-container');
            const logItem = document.createElement('div');
            logItem.className = `log-item ${type}`;
            logItem.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
            logContainer.appendChild(logItem);
            logContainer.scrollTop = logContainer.scrollHeight;

            // 限制日志数量
            while (logContainer.children.length > 100) {
                logContainer.removeChild(logContainer.firstChild);
            }

            if (type === 'error' && this.pushErrorMessages) {
                this.errorMessages.push(message);
            }
        }

        toggleDarkMode() {
            this.container.classList.toggle('dark-mode');
            const isDarkMode = this.container.classList.contains('dark-mode');
            GM_setValue('darkMode', isDarkMode);
        }

        toggleMinimize() {
            this.container.classList.toggle('minimized');
            const isMinimized = this.container.classList.contains('minimized');
            GM_setValue('minimized', isMinimized);
        }

        bindEvents() {
            // Token管理
            this.container.querySelector('.add-token').addEventListener('click', () => {
                this.tokens.push({ token: '', note: '', enabled: true });
                this.updateUI();
                this.saveSettings();
            });

            this.container.querySelector('.token-list').addEventListener('click', (e) => {
                const tokenItem = e.target.closest('.token-item');
                if (!tokenItem) return;

                const index = parseInt(tokenItem.dataset.index);
                if (e.target.matches('.remove-token')) {
                    this.tokens.splice(index, 1);
                    this.updateUI();
                    this.saveSettings();
                }
            });

            this.container.querySelector('.token-list').addEventListener('change', (e) => {
                const tokenItem = e.target.closest('.token-item');
                if (!tokenItem) return;

                const index = parseInt(tokenItem.dataset.index);
                if (e.target.matches('input[type="checkbox"]')) {
                    this.tokens[index].enabled = e.target.checked;
                } else if (e.target.matches('.token-input')) {
                    this.tokens[index].token = e.target.value;
                } else if (e.target.matches('.token-note')) {
                    this.tokens[index].note = e.target.value;
                }
                this.saveSettings();
            });

            // 频道管理
            this.container.querySelector('.add-channel').addEventListener('click', () => {
                this.channels.push({ id: '', name: '', messages: [], enabled: true });
                this.updateUI();
                this.saveSettings();
            });

            this.container.querySelector('.channel-list').addEventListener('click', (e) => {
                const channelCard = e.target.closest('.channel-card');
                if (!channelCard) return;

                const index = parseInt(channelCard.dataset.index);
                if (e.target.matches('.remove-channel')) {
                    this.channels.splice(index, 1);
                    this.updateUI();
                    this.saveSettings();
                }
            });

            this.container.querySelector('.channel-list').addEventListener('change', (e) => {
                const channelCard = e.target.closest('.channel-card');
                if (!channelCard) return;

                const index = parseInt(channelCard.dataset.index);
                if (e.target.matches('input[type="checkbox"]')) {
                    this.channels[index].enabled = e.target.checked;
                } else if (e.target.matches('.channel-id')) {
                    this.channels[index].id = e.target.value;
                } else if (e.target.matches('.channel-name')) {
                    this.channels[index].name = e.target.value;
                } else if (e.target.matches('.channel-messages')) {
                    this.channels[index].messages = e.target.value.split('\n').filter(msg => msg.trim());
                } else if (e.target.matches('.target-message-count')) {
                    const count = parseInt(e.target.value);
                    if (count >= 1000 && count <= 10000) {
                        this.channels[index].targetMessageCount = count;
                        this.channels[index].sentMessageCount = this.channels[index].sentMessageCount || 0;
                    } else {
                        e.target.value = this.channels[index].targetMessageCount || 1000;
                    }
                }
                this.saveSettings();
                this.updateUI();
            });

            // 发送控制
            this.container.querySelector('.start-btn').addEventListener('click', () => this.start());
            this.container.querySelector('.stop-btn').addEventListener('click', () => this.stop());

            // 时间控制
            this.container.querySelector('.enable-time-control').addEventListener('change', (e) => {
                this.enableTimeControl = e.target.checked;
                this.container.querySelector('.time-control').classList.toggle('hidden', !this.enableTimeControl);
                this.saveSettings();
            });

            this.container.querySelector('.start-time').addEventListener('change', (e) => {
                this.startTime = e.target.value;
                this.saveSettings();
            });

            this.container.querySelector('.end-time').addEventListener('change', (e) => {
                this.endTime = e.target.value;
                this.saveSettings();
            });

            // 间隔设置
            this.container.querySelector('.min-interval').addEventListener('change', (e) => {
                this.minInterval = parseInt(e.target.value);
                this.saveSettings();
            });

            this.container.querySelector('.max-interval').addEventListener('change', (e) => {
                this.maxInterval = parseInt(e.target.value);
                this.saveSettings();
            });

            // 界面控制
            this.container.querySelector('.minimize-btn').addEventListener('click', () => this.toggleMinimize());
            this.container.querySelector('.dark-mode-btn').addEventListener('click', () => this.toggleDarkMode());

            // 双击展开/收起
            this.container.querySelector('.title-bar').addEventListener('dblclick', () => this.toggleMinimize());

            // 拖动功能
            let isDragging = false;
            let currentX;
            let currentY;
            let initialX;
            let initialY;
            let xOffset = 0;
            let yOffset = 0;

            this.container.querySelector('.title-bar').addEventListener('mousedown', (e) => {
                initialX = e.clientX - xOffset;
                initialY = e.clientY - yOffset;

                if (e.target === this.container.querySelector('.title-bar')) {
                    isDragging = true;
                }
            });

            document.addEventListener('mousemove', (e) => {
                if (isDragging) {
                    e.preventDefault();

                    currentX = e.clientX - initialX;
                    currentY = e.clientY - initialY;

                    xOffset = currentX;
                    yOffset = currentY;

                    this.container.style.transform = `translate(${currentX}px, ${currentY}px)`;
                }
            });

            document.addEventListener('mouseup', () => {
                isDragging = false;
            });

            // 添加模板帮助切换事件
            this.container.querySelector('.channel-list').addEventListener('click', (e) => {
                if (e.target.matches('.show-template-help')) {
                    const helpDiv = e.target.nextElementSibling;
                    helpDiv.classList.toggle('hidden');
                    e.target.textContent = helpDiv.classList.contains('hidden') ? '查看变量说明' : '隐藏帮助';
                }
            });

            // 更新表情选择事件
            this.container.querySelector('.channel-list').addEventListener('change', (e) => {
                const channelCard = e.target.closest('.channel-card');
                if (!channelCard) return;

                const index = parseInt(channelCard.dataset.index);
                const channel = this.channels[index];

                if (e.target.matches('.preset-emoji')) {
                    channel.presetEmoji = e.target.value;
                }

                this.saveSettings();
            });

            // 推送设置
            this.container.querySelector('.push-channel-id').addEventListener('change', (e) => {
                this.pushChannelId = e.target.value;
                this.saveSettings();
            });

            this.container.querySelector('.enable-push').addEventListener('change', (e) => {
                this.enablePush = e.target.checked;
                this.saveSettings();
            });

            this.container.querySelector('.enable-periodic-push').addEventListener('change', (e) => {
                this.enablePeriodicPush = e.target.checked;
                this.container.querySelector('.periodic-push-settings').style.display =
                    this.enablePeriodicPush ? 'block' : 'none';
                this.saveSettings();
                if (this.isRunning) {
                    this.startPeriodicPush();
                }
            });

            this.container.querySelector('.push-interval').addEventListener('change', (e) => {
                this.pushInterval = parseInt(e.target.value) || 30;
                this.saveSettings();
                if (this.isRunning && this.enablePeriodicPush) {
                    this.startPeriodicPush();
                }
            });

            this.container.querySelector('.push-total-messages').addEventListener('change', (e) => {
                this.pushTotalMessages = e.target.checked;
                this.saveSettings();
            });

            this.container.querySelector('.push-channel-status').addEventListener('change', (e) => {
                this.pushChannelStatus = e.target.checked;
                this.saveSettings();
            });

            this.container.querySelector('.push-error-messages').addEventListener('change', (e) => {
                this.pushErrorMessages = e.target.checked;
                this.saveSettings();
            });
        }

        processTemplate(template) {
            let result = template;
            const channel = this.channels.find(c => c.id === this.currentChannelId);

            if (!channel) return result;

            // 处理时间变量
            result = result.replace(/\[时间\]/g, new Date().toLocaleTimeString());
            result = result.replace(/\[日期\]/g, new Date().toLocaleDateString());

            return result;
        }

        async sendPushMessage(message) {
            if (!this.enablePush || !this.pushChannelId) return;

            const enabledTokens = this.tokens.filter(t => t.token && t.enabled);
            if (enabledTokens.length === 0) return;

            const token = enabledTokens[0];

            try {
                const response = await fetch(`https://discord.com/api/v9/channels/${this.pushChannelId}/messages`, {
                    method: 'POST',
                    headers: {
                        'Authorization': token.token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ content: message })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                this.addLog('推送消息成功');
                // 清除已推送的错误消息
                this.errorMessages = [];
            } catch (error) {
                this.addLog(`推送消息失败: ${error.message}`, 'error');
            }
        }

        async sendPeriodicPushMessage() {
            if (!this.enablePeriodicPush || !this.isRunning) return;

            const now = new Date();
            const timeStr = now.toLocaleTimeString();
            const dateStr = now.toLocaleDateString();

            let message = `🤖 Discord AI Bot 状态报告
⏰ 报告时间: ${dateStr} ${timeStr}
━━━━━━━━━━━━━━━━━━━━━━\n`;

            if (this.pushTotalMessages) {
                const avgSpeed = this.messageCount > 0 ?
                    (this.messageCount / ((Date.now() - this.startTime) / 1000 / 60)).toFixed(2) : 0;
                message += `📊 消息统计
• 总发送数: ${this.messageCount} 条
• 平均速度: ${avgSpeed} 条/分钟
━━━━━━━━━━━━━━━━━━━━━━\n`;
            }

            if (this.pushChannelStatus) {
                message += `📈 频道状态\n`;
                const channelStatus = this.channels
                    .filter(c => c.enabled)
                    .map(c => {
                        const progress = ((c.sentMessageCount || 0) / (c.targetMessageCount || 1000) * 100).toFixed(1);
                        const progressBar = this.createProgressBar(progress);
                        return `• ${c.name || c.id}
  ${progressBar} ${progress}%
  ${c.sentMessageCount || 0}/${c.targetMessageCount || 1000} 条`;
                    })
                    .join('\n\n');
                message += channelStatus + '\n━━━━━━━━━━━━━━━━━━━━━━\n';
            }

            if (this.pushErrorMessages && this.errorMessages.length > 0) {
                message += `❌ 错误信息 (最近${Math.min(this.errorMessages.length, 5)}条)
${this.errorMessages.slice(-5).map(err => '• ' + err).join('\n')}
━━━━━━━━━━━━━━━━━━━━━━\n`;
            }

            message += `💡 运行状态: ${this.isRunning ? '🟢 正常运行中' : '🔴 已停止'}`;

            await this.sendPushMessage(message);
        }

        createProgressBar(percent) {
            const filled = Math.round(percent / 10);
            const empty = 10 - filled;
            return '▰'.repeat(filled) + '▱'.repeat(empty);
        }

        startPeriodicPush() {
            if (this.pushTimer) {
                clearInterval(this.pushTimer);
            }

            if (this.enablePeriodicPush) {
                this.pushTimer = setInterval(() => {
                    this.sendPeriodicPushMessage();
                }, this.pushInterval * 60 * 1000);
            }
        }
    }

    // 初始化实例
    (() => {
        new DiscordBot();
    })();
})();