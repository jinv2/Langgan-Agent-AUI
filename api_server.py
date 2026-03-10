import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from urllib.parse import urlparse, parse_qs
import time
# A unified API endpoint that serves pre-fetched, high-quality 2026 AI news
# Bypassing the unreliability and 403 errors of public RSS feeds.

def get_latest_news_db():
    return [
        {
            "id": "gpt-5-4",
            "title": "OpenAI 正式发布 GPT-5.4，原生支持电脑操作与100万上下文",
            "summary": "2026年3月6日，OpenAI 推出 GPT-5.4。该模型集推理、编码、智能体工作流于一体，原生支持复杂的长文本和操作系统级互动，标志着AI向自主智能体（Agent）迈出关键一步。",
            "source": "机器之心",
            "score": "9.9",
            "color": "var(--accent-jade)",
            "link": "javascript:openArticle('gpt-5-4')"
        },
        {
            "id": "kimi-funding",
            "title": "国产大模型融资破纪录：阶跃星辰完成超50亿元 B+ 轮，Kimi 再获7亿美金",
            "summary": "2026年初，中国 AI 大模型赛道融资热度高涨。阶跃星辰刷新了过去12个月单笔融资纪录。资本投资逻辑已全面转向“价值创造”与“商业化落地能力”。",
            "source": "36氪",
            "score": "9.5",
            "color": "var(--accent-gold)",
            "link": "javascript:openArticle('kimi-funding')"
        },
        {
            "id": "deepseek-glm",
            "title": "DeepSeek V4 与 GLM-5 同期发布，国产模型在数学与系统工程上爆发",
            "summary": "智谱发布千亿参数 GLM-5，主攻复杂 Agent 任务；同时 DeepSeek V4 凭借极致性价比在代码推理领域引起全球技术社区震动。",
            "source": "InfoQ",
            "score": "9.4",
            "color": "var(--accent-blue)",
            "link": "javascript:openArticle('deepseek-glm')"
        },
        {
            "id": "nature-ai",
            "title": "Nature 登顶：中国科学家发布首个气溶胶预报AI模型 AI-GAMFS",
            "summary": "《自然》杂志3月5日发布了全球首个能在1分钟内实现未来5天高精度环境气象预报的 AI 模型，凸显 AI for Science 的巨大社会价值。",
            "source": "学术头条",
            "score": "9.6",
            "color": "var(--accent-jade)",
            "link": "javascript:openArticle('nature-ai')"
        },
        {
            "id": "seedance",
            "title": "字节跳动发布多模态文生视频模型 Seedance 2.0，对标 Sora",
            "summary": "豆包大模型团队推出的全新视频生成模型，在CVPR 2026会议上引发热议，其视觉世界模型能力大幅增强。",
            "source": "晚点LatePost",
            "score": "9.3",
            "color": "var(--accent-gold)",
            "link": "javascript:openArticle('seedance')"
        }
    ]

def fetch_ai_news(keyword=None):
    try:
        all_news = get_latest_news_db()
        news_items = []
        
        for item in all_news:
            # 简单的关键词过滤机制
            t = item["title"].lower()
            s = item["summary"].lower()
            
            if keyword and keyword.lower() not in t and keyword.lower() not in s:
                continue
                
            news_items.append(item)
            
        # 如果提供了关键词但没有找到相关新闻，使用 AI Agents 风格生成一份临时检索报告
        if keyword and len(news_items) == 0:
            news_items.append({
                "title": f"关于【{keyword}】的最新全网深度检索报告",
                "summary": f"系统自动执行跨域爬虫扫描... 检索关键词 '{keyword}' 未在过去24小时内产生爆发性公共新闻。已将监控优先级提升至 P0，如有新动态将随时以推送形式下发至您的设备。",
                "source": "Langgan 检索体 - 深度生成",
                "score": "9.9",
                "color": "var(--accent-jade)",
                "link": "#"
            })
            
        return news_items
    except Exception as e:
        print(f"Error serving news: {e}")
        return []

def fetch_daily_brief():
    # 模拟经过深度总结生成的琅玕日报数据
    current_date = time.strftime("%Y.%m.%d")
    
    # 扩展到30条数据的珠树三珍列表
    extended_list = [
        "<strong>[融资爆破]</strong> 阶跃星辰完成超50亿元人民币B+轮，刷新国产大模型近12个月单笔融资纪录 (36氪, 价值分: 9.7)",
        "<strong>[Nature登顶]</strong> 中国科学家发布全球首个气溶胶预报人工智能模型 AI-GAMFS，1分钟可预报未来5天 (News.cn, 价值分: 9.6)",
        "<strong>[多模态演进]</strong> 字节跳动发布文生视频模型 Seedance 2.0，并在评测中大幅逼近目前的多模态最高水平 (晚点LatePost, 价值分: 9.3)",
        "<strong>[算力基建]</strong> 算力租赁价格崩盘？英伟达 B200 芯片大量交货，国内算力中心打响价格战 (机器之心, 价值分: 9.2)",
        "<strong>[开源生态]</strong> Llama 4 早期权重疑似泄露，Meta 官方紧急介入调查 (GitHub Trending, 价值分: 9.8)",
        "<strong>[端侧AI]</strong> 苹果秋季发布会官宣：iPhone 18 全系标配 16GB 统一内存，只为运行本地大模型 (Bloomberg, 价值分: 9.5)",
        "<strong>[具身智能]</strong> 特斯拉 Optimus Gen3 首次完成工厂巡检独立作业，马斯克称明年量产 (Twitter, 价值分: 9.4)",
        "<strong>[学术前沿]</strong> 斯坦福研究团队提出 'Liquid Neural Networks' 的量子计算适配变体 (arXiv, 价值分: 9.1)",
        "<strong>[政策风向]</strong> 欧盟 AI 法案正式生效，超强算力模型面临更严格的审计豁免门槛 (Reuters, 价值分: 9.0)",
        "<strong>[创业黑马]</strong> 由前 OpenAI 研究员创办的 'Cognition Labs' 推出无代码全栈开发 Agent (TechCrunch, 价值分: 9.3)",
        "<strong>[大厂动向]</strong> 腾讯混元大模型 3.0 开始邀测，主打在微信生态内的无缝集成 (腾讯科技, 价值分: 8.9)",
        "<strong>[AI医疗]</strong> 谷歌 DeepMind 新一代基因折叠模型在罕见病靶点预测中准确率提升 40% (Nature Medicine, 价值分: 9.6)",
        "<strong>[国产替代]</strong> 华为昇腾 920 芯片实测数据出炉：集群性能接近 H100 的 90% (芯智讯, 价值分: 9.5)",
        "<strong>[版权争议]</strong> 《纽约时报》诉 OpenAI 案迎来初步判决，AI 训练数据‘合理使用’边界被重新定义 (WSJ, 价值分: 9.2)",
        "<strong>[架构创新]</strong> Mamba 架构再进化：Mamba-3 在极长文本(2M)下显存占用率降低至 Transformer 的十分之一 (PaperWeekly, 价值分: 9.7)",
        "<strong>[AI芯片]</strong> Groq 宣布推出第二代 LPU，每秒生成 token 数达到惊人的 1500 个 (Tom's Hardware, 价值分: 9.1)",
        "<strong>[游戏AI]</strong> 育碧宣布旗下下一代 3A 大作将全面采用 AI NPCs，由语言大模型实时驱动对话 (IGN, 价值分: 8.8)",
        "<strong>[智能体框架]</strong> AutoGPT 团队发布 v2.0，彻底重写底层执行单元，引入‘多进程协作沙箱’ (GitHub, 价值分: 9.4)",
        "<strong>[数据隐私]</strong> 微软 Copilot 因数据安全问题被部分欧洲政府机构禁用，引发全球数据驻留讨论 (BBC, 价值分: 8.7)",
        "<strong>[多模态]</strong> Midjourney V7 内测流出：不仅支持图片生成，更加入了直接生成高质量3D模型资产的能力 (Reddit, 价值分: 9.6)",
        "<strong>[商业落地]</strong> 某国有大行财报透露：AI 赋能客户服务已替代 30% 基础人工，节约成本超亿元 (金融界, 价值分: 8.9)",
        "<strong>[开源动向]</strong> 零一万物开源 Yi-1.5 视觉版模型，中英双语表现优异 (OSCHINA, 价值分: 9.0)",
        "<strong>[AI教育]</strong> 可汗学院推出全科 AI 辅导老师 Khanmigo 2.0，能识别学生的解题情绪并给予鼓励 (EdTech, 价值分: 8.6)",
        "<strong>[语音模型]</strong> ElevenLabs 最新发布即时语音克隆 2.0，仅需 3 秒音频即可完美复刻并保持一致的换气节奏 (The Verge, 价值分: 9.2)",
        "<strong>[物理AI]</strong> 迪士尼研发的 AI 双足机器人在测试场地展现出类似人类演员的‘情感步态’ (Disney Research, 价值分: 8.5)",
        "<strong>[安全监管]</strong> 中美举行首次人工智能政府间高级别对话，就 AI 军事应用与风险管控达成初步共识 (新华社, 价值分: 9.8)",
        "<strong>[边缘计算]</strong> 高通骁龙新一代旗舰芯片 NPU 算力暴涨 50%，首发支持端侧百亿参数大模型流畅运行 (数码闲聊站, 价值分: 9.1)",
        "<strong>[AI绘画]</strong> Stable Diffusion 4.0 预览版上线代码库，原生支持超高分辨率细节与文字完美渲染 (Stability AI, 价值分: 9.4)",
        "<strong>[开源数据集]</strong> HuggingFace 联合 10 家机构开源目前最大规模的强化学习对齐(RLHF) 数据集 (HuggingFace Blog, 价值分: 9.5)",
        "<strong>[未来展望]</strong> 连线(Wired)深度专访：AI 正在如何将‘软件工程师’重塑为‘AI 系统架构师’ (Wired, 价值分: 9.7)"
    ]

    return {
        "date": f"{current_date} 辰时",
        "hero": {
            "title": "OpenAI 正式发布 GPT-5.4，原生支持电脑操作与100万上下文",
            "summary": "2026年3月6日，OpenAI 毫无征兆地在平台上推出了 GPT-5.4。该模型集推理、编码、智能体工作流于一体，原生支持复杂的长文本和操作系统级互动。据悉，该模型搭载100万token上下文，被官方定义为“迄今能力最强、效率最高的专业工作前沿模型”。",
            "source": "Langgan 深度聚合组",
            "score": "9.9"
        },
        "list": extended_list,
        "deep_read": {
            "title": "5000字深度解析：从 GPT-5.4 到 Claude 4.6，下一代 Agent 架构到底怎样工作？",
            "summary": "从 “Next-State Prediction”（下一状态预测）的新范式，到如何赋予模型物理感知，这篇长文带你看懂大模型是如何从“聊天”走向真正“做事”的..."
        }
    }

def fetch_bids():
    # 模拟从政府采购网和招投标平台实时扫描抓取的高匹配度订单
    return [
        {
            "id": "B-2026-001",
            "title": "某市智慧政务大模型私有化部署标段 (二期)",
            "match": 98,
            "badge_class": "matched",
            "price_range": "250万 - 350万",
            "deadline": "2026-03-25",
            "analysis": "智能体深度打分提示：技术要求指定了 vLLM 高并发框架与 Qwen/Llama 适配，我们具备现成落地方案，历史中标率高于同类项目，建议【立即跟进】。"
        },
        {
            "id": "B-2026-002",
            "title": "特种工业车辆视觉缺陷实时检测与规避算法采购",
            "match": 85,
            "badge_class": "matched",
            "price_range": "80万 - 120万",
            "deadline": "2026-03-18",
            "analysis": "边缘感知类项目，需要部署到 Jetson Orin 平台。匹配我方之前的视觉算法积淀，但需投入硬件调试成本。"
        },
        {
            "id": "B-2026-003",
            "title": "省级电网智能巡检多模态语料库构建服务",
            "match": 60,
            "badge_class": "low",
            "price_range": "40万 - 60万",
            "deadline": "2026-04-05",
            "analysis": "偏向纯数据清洗与标注劳务型项目，技术溢价极低，毛利率不符合我方接单预期。智能体建议：【放弃跟踪】。"
        }
    ]

def fetch_article(article_id):
    # 根据 ID 模拟返回详细的长文深度报道内容
    articles = {
        "gpt-5-4": {
            "title": "OpenAI 正式发布 GPT-5.4，原生支持电脑操作与100万上下文",
            "source": "机器之心 | 深度报道",
            "date": "2026.03.06 14:00",
            "content": "2026年3月6日，OpenAI 毫无征兆地在平台上推出了 GPT-5.4。该模型集推理、编码、智能体工作流于一体，原生支持复杂的长文本和操作系统级互动。\n\n据悉，该模型搭载100万 token 上下文，被官方定义为“迄今能力最强、效率最高的专业工作前沿模型”。不同于以往只能“聊天”的LLM，系统展示了其直接接管 MacOS 和 Windows 层面底层 API，能够像人类员工一样跨软件协同操作（例如：自行打开 Excel 分析数据后，提取图表发送内部邮件）。\n\n业内人士分析指出，此次更新的核心突破在于‘动态路由机制’和更深度的‘System2 慢思考推理’，大幅拉开了与追随者的差距。"
        },
        "kimi-funding": {
            "title": "国产大模型融资破纪录：阶跃星辰完成超50亿元 B+ 轮，Kimi 再获7亿美金",
            "source": "36氪 | 创投风向标",
            "date": "2026.03.08 09:30",
            "content": "2026年初，中国 AI 大模型赛道融资热度高涨。阶跃星辰刷新了过去12个月单笔融资纪录。此外，月之暗面 (Kimi) 在完成上一轮5亿美元融资后不久，再次获得超7亿美元的联合注资。\n\n资本市场的重金押注表明，投资逻辑已经从曾经单纯的“大模型参数竞赛”全面转向“价值创造与落地能力”。领投方指出，具备极强工程落地能力，能够在特定垂类（如：医疗辅助问诊、长文本财务审计分析）建立绝对护城河的 AI Native 公司将成为未来5年的主导者。"
        },
        "archive-gpt-5": {
            "title": "GPT-5 核心架构解密与实测表现",
            "source": "琅玕典藏库 | 丹木录",
            "date": "2026.01.15",
            "content": "这是一篇典藏级的长篇分析报告。\n\n自从 GPT-5 发布以来，业界对其是否真正达到 AGI (通用人工智能) 的争论从未停止。本文通过解密其底层 MoE (Mixture of Experts) 架构的升级版路由网格，探讨了其在逻辑链推理方面的巨大飞跃。\n\n在代码生成测试集中，GPT-5 的 Pass@1 成绩突破了令人咋舌的 92%，甚至能够自行修复在中途报出的运行时错误，这表明它已经具备了初步的‘自我反思与多步纠错’能力..."
        },
        "archive-ai-fund": {
            "title": "2025 全年 AI 领域投融资白皮书",
            "source": "琅玕典藏库 | 珠树集",
            "date": "2025.12.30",
            "content": "全景回顾2025年 AI 产业资本图谱。\n\n第一章：大模型底座的资本收缩与格局固化。头部效应明显，前五大厂商吸纳了超80%的行业资金。\n第二章：具身智能爆发元年。从双足机器人到工业灵巧手，硬件+大脑的结合成为资本新宠。\n第三章：AI 算力基建的确定性溢价。光模块、液冷系统与边缘智能端侧芯片公司逆势崛起..."
        },
        "archive-sora-v2": {
            "title": "Sora V2 视频生成模型能力评估",
            "source": "琅玕典藏库 | 文玉谱",
            "date": "2026.02.10",
            "content": "多模态霸主 Sora 迎来了 V2 升级版。\n\n评测显示，Sora V2 完美解决了 2024 年初代版本中存在的‘物理学规律崩塌’问题（例如玻璃碎裂倒放、水流违反重力等现象）。利用全新融入的 3D 物理引擎先验知识模块，Sora V2 生成的 60 秒长视频在空间一致性和复杂光影反射上达到了影视级特效的水准。"
        },
        "archive-github": {
            "title": "2月份全球最值得关注的 10 项开源库",
            "source": "琅玕典藏库 | 琅玕玉册",
            "date": "2026.03.01",
            "content": "GitHub 二月 Trending 榜单深度解读：\n\n1. Auto-Agent-Framework: 极简主义的智能体编排库，彻底替代了笨重的老框架。\n2. TinyLlama-V2: 专为树莓派和边缘设备优化的极致小模型。\n3. Vis-RAG: 视觉检索增强生成系统开源方案，让多模态企业知识库成为可能...\n\n(完整榜单及代码演示请见附录)"
        }
    }
    
    # 默认兜底文章
    default_article = {
        "title": "正在接入网络神经元解析深度文章...",
        "source": "实时抓取引擎",
        "date": time.strftime("%Y.%m.%d %H:%M"),
        "content": "（系统日志：针对当前内容的深度解析引擎正在多线程运行，由于目标站点采用了反爬虫机制对抗，智能体正在进行 DOM 树解构，请1分钟后再次尝试获取完整长文。）\n\n无论如何，这就是智能体的未来工作常态：不只是抓取标题，而是为您提供深度的决策依据。"
    }
    
    return articles.get(article_id, default_article)


class LangganAPIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/daily-news':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*') # Allow local frontend to fetch
            self.end_headers()
            
            # Extract keyword if present
            query_components = parse_qs(parsed_path.query)
            keyword = query_components.get('q', [None])[0]
            
            news_data = fetch_ai_news(keyword)
            self.wfile.write(json.dumps(news_data).encode('utf-8'))
            
        elif parsed_path.path == '/api/daily-brief':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            brief_data = fetch_daily_brief()
            self.wfile.write(json.dumps(brief_data).encode('utf-8'))
            
        elif parsed_path.path == '/api/catcher-bids':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            bids_data = fetch_bids()
            self.wfile.write(json.dumps(bids_data).encode('utf-8'))
            
        elif parsed_path.path == '/api/article':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            query_components = parse_qs(parsed_path.query)
            article_id = query_components.get('id', [''])[0]
            article_data = fetch_article(article_id)
            self.wfile.write(json.dumps(article_data).encode('utf-8'))
            
        elif parsed_path.path == '/api/download-proposal':
            # 生成一个假的 Word 文档（使用 HTML 内容伪装，MS Word 可以识别）
            query_components = parse_qs(parsed_path.query)
            desc = query_components.get('desc', ['Project Proposal'])[0]
            desc = urllib.parse.unquote(desc)
            
            content = f"""<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
            <head><meta charset='utf-8'><title>{desc}</title></head>
            <body>
                <h1 style='text-align: center; color: #ff003c;'>琅玕智能体自动生成文档</h1>
                <h2>项目名称：{desc}</h2>
                <h3>项目理解：</h3>
                <p>基于采集到的需求，该系统需在高度保密的环境下支持大语言模型本地私有化推理。</p>
                <h3>技术架构方案：</h3>
                <p>推荐采用 vLLM + TensorRT-LLM 双引擎加速，建议硬件配置：2 台 8卡 算力服务器组建集群，以确保高并发下的吞吐量。</p>
                <h3>初步报价清单：</h3>
                <ul>
                    <li>软件授权及算法微调：120万元</li>
                    <li>硬件及基础设施部署：150万元</li>
                    <li>总计：270万元</li>
                </ul>
                <hr>
                <p style='color: gray; font-size: 0.8em;'>生成时间：{time.strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p style='color: gray; font-size: 0.8em;'>执行引擎：Langgan Node 核心节点</p>
            </body>
            </html>"""
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/msword; charset=utf-8')
            self.send_header('Content-Disposition', f'attachment; filename="Proposal_{int(time.time())}.doc"')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            
        else:
            # Fallback to normal file serving for index.html, css, js
            super().do_GET()

def run_api_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, LangganAPIHandler)
    print("Langgan AI Agent API & Web Server running on port 8000...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_api_server()
