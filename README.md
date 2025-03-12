# Auto-VocabMaster 百词斩单词对战自动化工具  
An Automated Tool for Baicizhan Vocabulary Battle  

## 项目概述 / Project Overview  
本项目是一个专为百词斩单词对战设计的自动化脚本工具，基于OCR文字识别、语义向量匹配和模拟操作技术。通过多级词库查询与深度学习模型，实现高准确率的答案选择，帮助用户快速提升对战等级（实测可达“英语王者”级别）。  
This project is an automated script tool designed for Baicizhan vocabulary battles. It utilizes OCR text recognition, semantic vector matching, and simulated operations. Through multi-level vocabulary database queries and deep learning models, it achieves high-accuracy answer selection, helping users rapidly advance their battle ranks (tested to reach "English King" level).  

## 功能特性 / Key Features  
### 自动化对战流程 / Automated Battle Process  
自动识别题目与选项，模拟点击操作，无需人工干预。  
Auto-recognize questions and options, simulate clicks without manual intervention.  
### 多重匹配机制 / Multi-Level Matching  
优先使用本地词库（SQLite）查询释义，未命中时通过百词斩APP实时搜索并更新词库。  
Prioritize local database (SQLite) for word meanings; fallback to real-time Baicizhan APP search if missing.  
### 高性能OCR集成 / High-Performance OCR  
采用PaddleOCR进行文字识别，支持中英文混合文本精准定位。  
Leverage PaddleOCR for accurate text recognition in mixed Chinese-English contexts.  
### 语义相似度计算 / Semantic Similarity Calculation  
使用Sentence-BERT模型（distiluse-base-multilingual）计算问题与选项的语义相似度。  
Utilize Sentence-BERT model to measure semantic relevance between questions and options.  
### 异常处理与日志 / Error Handling & Logging  
内置能量检测、错误重试机制，并记录详细运行日志（app.log）。  
Built-in energy detection, retry mechanisms, and detailed runtime logging.  

## 技术细节 / Technical Details  
### 核心组件 / Core Components  
- OCR引擎: PaddleOCR（中英文识别）  
- 语义模型: SentenceTransformers (distiluse-base-multilingual-cased-v2)  
- 自动化控制: PyAutoGUI + PyWinAuto  
- 词库管理: SQLite3 数据库  

## 安装与配置 / Installation & Setup  
### 环境要求 / Environment Requirements  
- Python 3.8+  
- 雷电模拟器9（多开窗口，分辨率设置为“手机版-1600x720”）  
- 百词斩APP（需登录并进入对战页面）  

### 步骤指南 / Setup Guide  
#### 克隆仓库  
git clone https://github.com/your-repo/Auto-VocabMaster.git  
cd Auto-VocabMaster  
pip install -r requirements.txt  
配置模拟器
打开雷电多开器，创建两个实例，分别命名为：

雷电模拟器（主对战窗口）
百词斩单词查询（备用查询窗口）
设置窗口置顶（右键菜单 → 窗口置顶）。
初始化词库
将预训练词库 words.db 放入 baicizhanciku/ 目录。

启动程序
bash
深色版本
python main.py  
使用方法 / Usage
确保两个模拟器窗口分别处于以下状态：

雷电模拟器: 百词斩对战准备界面（显示“开始对战吧！”按钮）。
百词斩单词查询: 百词斩单词查询页面。
运行程序后，脚本将自动执行以下操作：
截屏 → OCR识别 → 词库查询 → 语义匹配 → 点击正确答案。
注意事项 / Notes
分辨率必须严格匹配，否则坐标定位失效。
若遇“能量不足”，程序会自动等待60秒后重试。
首次启动需预加载模型，耗时约1-2分钟。
贡献与许可 / Contribution & License
词库来源
100-vocabulary-lib (CC BY-NC 4.0)
开源许可
本项目基于MIT协议开源，欢迎提交Issue或PR。

Let the AI conquer your vocabulary battles! 🚀  
