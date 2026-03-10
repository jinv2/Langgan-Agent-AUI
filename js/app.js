// AUI Core Logic
const chatStream = document.getElementById('chat-stream');
const inputField = document.getElementById('aui-input');

// Focus input on load
window.onload = () => {
    if(inputField) inputField.focus();
};

// Handle Enter Key
if(inputField) {
    inputField.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            handleInput();
        }
    });
}

function scrollToBottom() {
    chatStream.scrollTop = chatStream.scrollHeight;
}

window.sendPrompt = function(text) {
    if(inputField) {
        inputField.value = text;
        handleInput();
    }
}

window.handleInput = function() {
    const text = inputField.value.trim();
    if (!text) return;

    // 1. Append User Message
    appendMessage('user', text);
    inputField.value = '';
    
    // 2. Determine Intent based on keywords
    let intent = "general";
    if (text.includes("简报") || text.includes("今日") || text.includes("最新")) {
        intent = "brief";
    } else if (text.includes("雷达") || text.includes("扫描") || text.includes("前沿") || text.includes("开源")) {
        intent = "radar";
    } else if (text.includes("报价") || text.includes("私有化") || text.includes("需求") || text.includes("标案")) {
        intent = "proposal";
    } else if (text.includes("调阅") || text.includes("典藏库") || text.includes("GPT-5")) {
        intent = "archive";
    }
    
    // 3. Simulate Agent Processing
    simulateAgentProcess(intent, text);
};

function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    
    const avatarPath = role === 'agent' ? 'logo_ts.png' : 'https://ui-avatars.com/api/?name=User&background=330000&color=ff003c&bold=true';
    
    msgDiv.innerHTML = `
        <div class="avatar"><img src="${avatarPath}" alt="${role}"></div>
        <div class="msg-content glass-panel">
            <p>${text}</p>
        </div>
    `;
    
    chatStream.appendChild(msgDiv);
    scrollToBottom();
}

function simulateAgentProcess(intent, originalText) {
    // Show typing
    const typingId = 'typing-' + Date.now();
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message agent';
    typingDiv.id = typingId;
    typingDiv.innerHTML = `
        <div class="avatar"><img src="logo_ts.png" alt="agent"></div>
        <div class="msg-content glass-panel typing">
            <span></span><span></span><span></span>
        </div>
    `;
    chatStream.appendChild(typingDiv);
    scrollToBottom();

    // After 800ms, replace typing with Terminal Logs
    setTimeout(() => {
        document.getElementById(typingId).remove();
        
        const logId = 'log-' + Date.now();
        const logDiv = document.createElement('div');
        logDiv.className = 'message agent';
        logDiv.id = logId;
        
        let initialLog = "> 正在解析意图...\n> 识别完成。<br>> 调用决策大模型，分配行动子节点...";
        
        logDiv.innerHTML = `
            <div class="avatar"><img src="logo_ts.png" alt="agent"></div>
            <div class="msg-content glass-panel" style="width:100%; max-width:600px;">
                <div class="log-box" id="log-box-${logId}">${initialLog}</div>
            </div>
        `;
        chatStream.appendChild(logDiv);
        scrollToBottom();
        
        // Stream logs based on intent
        streamLogsAndExecute(intent, logId, originalText);
        
    }, 800);
}

function streamLogsAndExecute(intent, logId, originalText) {
    const logBox = document.getElementById(`log-box-${logId}`);
    if(!logBox) return;
    
    let logs = [];
    let executeFunc = null;
    
    switch(intent) {
        case "brief":
            logs = [
                "> 启动数据聚合器 (Thread 12)...",
                "> 正在穿透抓取今日 AI 头条数据源，深度缓存提取中...",
                "> 剔除 87% 噪音信息，请求 /api/daily-brief 接口...",
                "> 提取成功，正为您渲染【琅玕今日简报】卡片。"
            ];
            executeFunc = renderDailyBriefCard;
            break;
        case "radar":
            logs = [
                "> 唤醒全网雷达系统...",
                "> 突破 arXiv 与 GitHub 官方访问限制...",
                "> 抓取到 500+ 异构元数据，正在通过本地 vLLM 引擎进行语义归一化...",
                "> 分析完成，存在异常高优跳动，已过滤展示。"
            ];
            executeFunc = renderRadarCard;
            break;
        case "proposal":
            logs = [
                "> 解析您的需求：生成 270 万大模型本地私有化标案...",
                "> 正在调用「琅玕方案生成专精节点」...",
                "> 计算硬件损耗比：推荐 2台 H20...",
                "> 排版引擎挂载成功，等待生成并渲染下载链接。"
            ];
            executeFunc = () => renderProposalCard(originalText);
            break;
        case "archive":
            logs = [
                "> 正在检索【琅玕典藏库】历史核心研报...",
                "> 匹配度 99%：定位到《GPT-5 核心架构解密与实测表现》...",
                "> 正在解密私有向量库...",
                "> 文章抽取完毕，即将通过全屏面板展示。"
            ];
            executeFunc = () => openArticle('archive-gpt-5');
            break;
        default:
            logs = [
                "> 接收到未分类指令...",
                "> 推理中，已记录该需求。",
                "> 暂无可匹配的高阶可视化组件，为您生成文本回复。"
            ];
            executeFunc = () => {
                const msg = document.createElement('p');
                msg.style.marginTop = '15px';
                msg.innerText = "智能体已执行：针对您的泛领域需求进行了全网扫描并已存档至向量神经网，等待后续调度。";
                logBox.parentElement.appendChild(msg);
                scrollToBottom();
            };
    }
    
    // Simulate streaming
    let i = 0;
    const interval = setInterval(() => {
        if (i < logs.length) {
            logBox.innerHTML += `<br>${logs[i]}`;
            scrollToBottom();
            i++;
        } else {
            clearInterval(interval);
            setTimeout(() => {
                if(executeFunc) executeFunc(logBox.parentElement);
            }, 600);
        }
    }, 500);
}

// ----------------------------------------------------
// Component Renderers (Injected into Chat Stream)
// ----------------------------------------------------

async function renderDailyBriefCard(parentElement) {
    try {
        const response = await fetch('/api/daily-brief');
        const data = await response.json();
        
        let listHtml = data.list.slice(0, 5).map(item => `
            <div class="news-item" onclick="openArticle('gpt-5-4')">
                <i class="fa-solid fa-caret-right" style="color:var(--accent-jade); margin-right:5px;"></i> ${item}
            </div>
        `).join('');

        const card = document.createElement('div');
        card.className = "aiga-card";
        card.innerHTML = `
            <h3 class="card-title"><i class="fa-solid fa-scroll"></i> 琅玕深度简报 (${data.date})</h3>
            <div style="background: rgba(255,0,60,0.1); padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 3px solid var(--accent-jade);">
                <h4 style="color:#fff; margin-bottom: 5px; cursor:pointer;" onclick="openArticle('gpt-5-4')">${data.hero.title}</h4>
                <p style="color:var(--text-secondary); font-size: 0.9em;">${data.hero.summary}</p>
            </div>
            <div style="font-size: 0.95em;">
                ${listHtml}
                <div style="text-align:center; padding-top:10px;">
                    <span style="color:var(--text-muted); font-size: 0.8em;">(已折叠剩余 25 条资讯，按需随时调取)</span>
                </div>
            </div>
        `;
        parentElement.appendChild(card);
        scrollToBottom();
    } catch (error) {
        parentElement.innerHTML += `<p style="color:red; margin-top:10px;">[接口调用失败，后端服务未响应]</p>`;
    }
}

function renderRadarCard(parentElement) {
    const card = document.createElement('div');
    card.className = "aiga-card";
    card.innerHTML = `
        <h3 class="card-title"><i class="fa-solid fa-satellite-dish"></i> 全网雷达扫描结论</h3>
        <p style="color:var(--text-secondary); margin-bottom: 10px;">捕捉到 3 项异常跳动趋势：</p>
        <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 8px; display:flex; justify-content:space-between;">
            <span><i class="fa-brands fa-github" style="color:#fff"></i> GitHub 开源区</span>
            <span style="color:var(--accent-jade);">3个 Agent 框架 Star 飙升</span>
        </div>
        <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 8px; display:flex; justify-content:space-between;">
            <span><i class="fa-solid fa-graduation-cap" style="color:#fff"></i> arXiv 预印本</span>
            <span style="color:var(--accent-gold);">MoE 架构论文数量激增 40%</span>
        </div>
        <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 8px; display:flex; justify-content:space-between;">
            <span><i class="fa-solid fa-file-contract" style="color:#fff"></i> 财政采购网</span>
            <span style="color:var(--accent-blue);">发现 2 项千万级私有化大模型盲签招标</span>
        </div>
    `;
    parentElement.appendChild(card);
    scrollToBottom();
}

function renderProposalCard(promptText) {
    const card = document.createElement('div');
    card.className = "aiga-card";
    card.innerHTML = `
        <div style="background: rgba(0,0,0,0.4); border: 1px dashed var(--accent-jade); padding: 20px; border-radius: 8px; text-align:center;">
            <i class="fa-solid fa-file-signature" style="font-size: 2rem; color: var(--accent-jade); margin-bottom: 15px;"></i>
            <h3 style="color:#fff; margin-bottom: 10px;">智能标案生成完毕</h3>
            <p style="color:var(--text-secondary); margin-bottom: 20px;">基于您的指令，系统已利用内部行业知识库自动撰写了完整的项目建议书及硬件架构报价单（270万级别）。</p>
            <a href="/api/download-proposal?desc=${encodeURIComponent("政企大模型本地私有化专有部署方案")}" download class="btn-primary" style="text-decoration: none; display: inline-block;">
                <i class="fa-solid fa-download"></i> 立即下载源文件 (.doc)
            </a>
        </div>
    `;
    return card;
}

// ----------------------------------------------------
// Modal and Global Logic
// ----------------------------------------------------

window.openModal = function(contentHtml) {
    const modal = document.getElementById('global-modal');
    const body = document.getElementById('modal-body');
    body.innerHTML = contentHtml;
    modal.style.display = 'flex';
    // Small delay to allow display block to take effect before changing opacity
    setTimeout(() => {
        modal.style.opacity = '1';
    }, 10);
};

window.closeModal = function() {
    const modal = document.getElementById('global-modal');
    modal.style.opacity = '0';
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
};

async function openArticle(articleId) {
    openModal(`<div style="text-align:center; padding: 50px; color: var(--accent-jade);"><i class="fa-solid fa-spinner fa-spin fa-2x"></i><p style="margin-top:15px">正在从知识图谱深海提取...</p></div>`);
    try {
        const response = await fetch(`/api/article?id=${articleId}`);
        const data = await response.json();
        const content = `
            <div style="color: #fff; line-height: 1.8;">
                <h1 style="color: var(--accent-jade); margin-bottom: 10px;">${data.title}</h1>
                <div style="display: flex; justify-content: space-between; color: var(--text-muted); border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; margin-bottom: 20px;">
                    <span><i class="fa-solid fa-satellite-dish"></i> 源头：${data.source}</span>
                    <span><i class="fa-regular fa-clock"></i> 收录：${data.date}</span>
                </div>
                <div style="font-size: 1.05rem; white-space: pre-wrap; font-family: var(--font-heading)">
                    ${data.content}
                </div>
            </div>
        `;
        document.getElementById('modal-body').innerHTML = content;
    } catch (error) {
        document.getElementById('modal-body').innerHTML = `<p style="color:red">提取失败，连接中断。</p>`;
    }
}

window.openNotificationModal = function() {
    const content = `
        <div style="color: #fff; line-height: 1.8;">
            <h1 style="color: var(--accent-jade); margin-bottom: 5px;"><i class="fa-solid fa-bell"></i> 隐秘指挥舱 - 局域通讯</h1>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">全网异动监控与底层引擎状态通告</p>
            <div style="background: rgba(0,0,0,0.3); padding: 15px; border-left: 4px solid var(--accent-jade); margin-bottom: 10px;">
                <p style="margin: 0;"><strong>[系统]</strong> 全网数据清洗完成，新增高价值研报 12 份。 <span style="color:gray; font-size:0.8em;">(3分钟前)</span></p>
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 15px; border-left: 4px solid var(--accent-gold); margin-bottom: 10px;">
                <p style="margin: 0;"><strong>[捕手]</strong> 拦截到匹配度 98% 的高优盲签标讯，已放入待命区。 <span style="color:gray; font-size:0.8em;">(30分钟前)</span></p>
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 15px; border-left: 4px solid var(--accent-blue);">
                <p style="margin: 0;"><strong>[引擎]</strong> 本地推理引擎 vLLM 调度器已完成冷启动预热，GPU群绝对就绪。 <span style="color:gray; font-size:0.8em;">(2小时前)</span></p>
            </div>
        </div>
    `;
    openModal(content);
};

window.openAPISettings = function() {
    const currentModel = localStorage.getItem('langgan_model') || 'gpt-5-4';
    const currentKey = localStorage.getItem('langgan_apikey') || '';
    
    const content = `
        <div style="color: #fff; line-height: 1.8;">
            <h1 style="color: var(--accent-jade); margin-bottom: 5px;"><i class="fa-solid fa-microchip"></i> 算力引擎池接入配置</h1>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">琅玕智能体高度解耦，支持您随时拔插世界顶级推理架构接入 API Keys。</p>
            
            <div style="background: rgba(0,0,0,0.3); padding: 20px; border: 1px dashed var(--accent-jade); border-radius: 8px;">
                <div style="margin-bottom: 15px;">
                    <label style="display: block; color: var(--accent-gold); margin-bottom: 5px; font-weight: bold;"><i class="fa-solid fa-brain"></i> 挂载推理中枢 (Top 10 Models)</label>
                    <select id="model-select" style="width: 100%; padding: 12px; background: rgba(0,0,0,0.6); color: #fff; border: 1px solid var(--accent-jade); border-radius: 6px; font-family: var(--font-body); outline: none;">
                        <option value="gpt-5-4" ${currentModel === 'gpt-5-4' ? 'selected' : ''}>OpenAI GPT-5.4 (默认：综合推理最强)</option>
                        <option value="gpt-4o" ${currentModel === 'gpt-4o' ? 'selected' : ''}>OpenAI GPT-4o (多模态高速)</option>
                        <option value="claude-3-5" ${currentModel === 'claude-3-5' ? 'selected' : ''}>Anthropic Claude 3.5 Sonnet (代码/长文王座)</option>
                        <option value="gemini-1-5" ${currentModel === 'gemini-1-5' ? 'selected' : ''}>Google Gemini 1.5 Pro (百万上下文吃透)</option>
                        <option value="llama-3" ${currentModel === 'llama-3' ? 'selected' : ''}>Meta Llama 3 70B (开源最强理智线)</option>
                        <option value="deepseek" ${currentModel === 'deepseek' ? 'selected' : ''}>DeepSeek-V3 (国产代码与数学之光)</option>
                        <option value="glm-4" ${currentModel === 'glm-4' ? 'selected' : ''}>智谱 GLM-4 (国产复杂Agent首选)</option>
                        <option value="kimi" ${currentModel === 'kimi' ? 'selected' : ''}>月之暗面 Kimi (国产长文本王者)</option>
                        <option value="qwen-max" ${currentModel === 'qwen-max' ? 'selected' : ''}>通义千问 Qwen-Max</option>
                        <option value="ernie-4" ${currentModel === 'ernie-4' ? 'selected' : ''}>百度文心一言 Ernie 4.0</option>
                    </select>
                </div>
                
                <div style="margin-bottom: 25px;">
                    <label style="display: block; color: var(--accent-gold); margin-bottom: 5px; font-weight: bold;"><i class="fa-solid fa-key"></i> 授权密钥 (API Key)</label>
                    <input type="password" id="api-key-input" value="${currentKey}" placeholder="sk-..." style="width: 100%; padding: 12px; background: rgba(0,0,0,0.6); color: #00ff9d; border: 1px solid var(--accent-jade); border-radius: 6px; font-family: monospace; outline: none; letter-spacing: 2px;">
                    <p style="color: gray; font-size: 0.8em; margin-top: 5px;"><i class="fa-solid fa-shield-halved"></i> 密钥仅存储在您的本地浏览器中 (localStorage)，绝不会发送至我们的总控服务器。</p>
                </div>
                
                <div style="text-align: right;">
                    <button onclick="saveAPISettings()" class="btn-primary" style="display: inline-flex; align-items: center; gap: 8px;">
                        <i class="fa-solid fa-satellite-dish"></i> 保存并热更新接管
                    </button>
                </div>
            </div>
        </div>
    `;
    openModal(content);
};

window.saveAPISettings = function() {
    const model = document.getElementById('model-select').value;
    const key = document.getElementById('api-key-input').value;
    
    localStorage.setItem('langgan_model', model);
    localStorage.setItem('langgan_apikey', key);
    
    // Convert modal back to a success message
    const body = document.getElementById('modal-body');
    body.innerHTML = `
        <div style="text-align: center; color: #fff; padding: 40px 20px;">
            <i class="fa-solid fa-circle-check" style="font-size: 4rem; color: #00ff9d; margin-bottom: 20px;"></i>
            <h2 style="color: #00ff9d; margin-bottom: 15px;">算力引擎热切换成功</h2>
            <p style="color: var(--text-secondary);">已将架构挂载点切换至 <strong>${document.getElementById('model-select').options[document.getElementById('model-select').selectedIndex].text}</strong></p>
            <button onclick="closeModal()" class="btn-primary" style="margin-top: 25px;">返回隐秘指挥舱</button>
        </div>
    `;
};

window.toggleSidebar = function() {
    const sidebar = document.querySelector('.aui-sidebar');
    if(sidebar) {
        sidebar.classList.toggle('active');
    }
};
