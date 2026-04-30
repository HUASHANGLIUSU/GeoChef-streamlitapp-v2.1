# 🌍 GeoChef — 遥感视觉语言数据集智能检索平台

GeoChef 是一个面向遥感视觉语言（RS-VLM）领域的数据集智能检索与分析平台，基于 Streamlit 构建，集成 ECNU 大模型与 OpenAI 兼容接口，支持中英文双语与深色/浅色主题切换。

---

## ✨ 功能一览

| 页面 | 核心能力 |
|------|---------|
| 🔍 **精准筛选** | 数据模态 / 任务类型 / 年份 / 发布单位 / 方法类型多维筛选 + 关键词全文搜索；结果支持 **Excel / CSV / Word / BibTeX / Markdown** 五种格式导出 |
| 🔀 **数据集对比** | 最多 4 个数据集并排对比，差异字段自动高亮，生成数值指标雷达图 |
| ⚠️ **数据泄露检测** | 基于原始数据集倒排索引，支持单源查询与批量检测，可视化关联关系图，结果可导出 |
| 📚 **论文讲解助手** | 输入数据集名称或论文链接，AI 流式生成结构化专业讲解，支持多轮追问，对话可导出 |
| 📊 **数据集统计** | 概览图表（年份 / 任务 / 模态 / 类别）· 气泡地图（论文来源国家）· 增长趋势（折线图 / 堆叠面积图 / 同比增速） |
| 💬 **ChatECNU 助手** | 遥感领域问答，内置数据集搜索指导与数据泄露专业知识，对话可导出 |
| 🛰️ **NASA 每日一图** | 自动拉取 NASA Earth Observatory 每日卫星图像，优先展示当天图片，可浏览近期图集 |

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/VisionXLab/GeoChef-streamlitapp.git
cd GeoChef-streamlitapp
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置密钥

复制模板并填入 API Key：

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

```toml
# .streamlit/secrets.toml
CHATECNU_API_KEY = "your-chatecnu-api-key"
OPENAI_API_KEY   = "your-openai-compatible-api-key"
```

| 变量名 | 用途 |
|--------|------|
| `CHATECNU_API_KEY` | ECNU 大模型，用于 ChatECNU 助手、字段翻译、对比翻译 |
| `OPENAI_API_KEY` | OpenAI 兼容接口（AutoDL Qwen），用于论文讲解助手 |

### 4. 准备数据

将数据文件 `rs_vlm_datasets.xlsx` 放到项目根目录（已在 `.gitignore` 中排除，需自行提供）。

### 5. 启动

```bash
streamlit run main.py
```

---

## 📁 项目结构

```
GeoChef/
├── main.py                  # 应用入口：路由、侧边栏、顶栏
├── core.py                  # GeoChef 数据类：加载、筛选、统计、泄露检测索引
├── model.py                 # ECNUModel：ECNU API 封装（聊天、翻译）
├── paper_explainer.py       # 论文讲解：流式调用 OpenAI 兼容接口
├── github_parser.py         # 解析 dataset_links.md，建立数据集名称 → 论文链接映射
├── i18n.py                  # 中英文字符串字典
├── theme.py                 # NASA 风格深色/浅色主题 CSS
├── dataset_links.md         # 数据集论文链接（Markdown 格式）
├── rs_vlm_datasets.xlsx     # 数据集主文件（不纳入版本控制）
├── requirements.txt
├── .streamlit/
│   └── secrets.toml.example # 密钥配置模板
└── views/
    ├── intro_view.py        # 简介页（功能卡片网格）
    ├── chat_view.py         # ChatECNU 对话 + 导出
    ├── paper_view.py        # 论文讲解助手 + 导出
    ├── filter_view.py       # 精准筛选
    ├── compare_view.py      # 数据集对比
    ├── leakage_view.py      # 数据泄露检测
    ├── leakage_graph.py     # 泄露关系可视化（放射状节点图）
    ├── stats_view.py        # 统计图表（概览 / 地理 / 趋势）
    ├── nasa_view.py         # NASA 每日一图
    ├── result_card.py       # 数据集卡片组件（筛选 & 泄露检测共用）
    ├── export_panel.py      # 筛选结果导出面板
    └── export_utils.py      # 导出工具（数据集 + 对话记录）
```

---

## 📦 依赖

```
streamlit >= 1.32.0
pandas >= 2.0.0
openpyxl >= 3.1.0
openai >= 1.0.0
requests >= 2.31.0
python-dotenv >= 1.0.0
plotly >= 5.0.0
python-docx >= 1.1.0
```

---

## 📄 License

[LICENSE](LICENSE.txt)

## 🔗 相关链接

- 数据集主页：[VisionXLab/Awesome-RS-VL-Data](https://github.com/VisionXLab/Awesome-RS-VL-Data)
