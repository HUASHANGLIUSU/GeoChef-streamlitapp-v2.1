# 🌍 GeoChef — 遥感视觉语言数据集智能检索平台

GeoChef 是一个面向遥感视觉语言（RS-VLM）领域的数据集智能检索与分析平台，基于 Streamlit 构建，集成了 ECNU 大模型与 OpenAI 兼容接口。

## ✨ 功能

| 页面 | 功能 |
|------|------|
| 🔍 **精准筛选** | 多维度组合筛选 + 关键词全文搜索，结果支持 Excel / CSV / Word / BibTeX / Markdown 导出 |
| 🔀 **数据集对比** | 最多 4 个数据集并排对比，差异高亮 + 雷达图 |
| ⚠️ **数据泄露检测** | 基于原始数据集索引，单源查询 / 批量检测，可视化关联图，支持导出 |
| 📚 **论文讲解助手** | 输入数据集名称或论文链接，AI 生成结构化讲解，支持追问和导出 |
| 📊 **数据集统计** | 概览图表 / 地理分布世界地图 / 增长趋势分析 |
| 💬 **ChatECNU 助手** | 遥感领域问答，内置搜索指导 + 数据泄露知识，支持导出对话 |
| 🛰️ **NASA 每日一图** | 自动拉取 NASA Earth Observatory 每日卫星图像 |

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

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

编辑 `.streamlit/secrets.toml`，填入你的 API Key：

```toml
CHATECNU_API_KEY = "your-chatecnu-api-key"
OPENAI_API_KEY   = "your-openai-compatible-api-key"
```

> 也可以通过环境变量传入，程序会自动回退到 `os.getenv()`。

### 4. 准备数据

将数据文件 `rs_vlm_datasets.xlsx` 放到项目根目录（已在 `.gitignore` 中排除，需自行提供）。

### 5. 启动应用

```bash
streamlit run main.py
```

## 📁 项目结构

```
GeoChef/
├── main.py                  # 应用入口，路由 & 侧边栏
├── core.py                  # GeoChef 数据类，加载 & 筛选 & 统计
├── model.py                 # ECNUModel，ECNU API 封装
├── paper_explainer.py       # 论文讲解，流式调用 OpenAI 兼容接口
├── github_parser.py         # 解析 dataset_links.md，建立名称→链接映射
├── i18n.py                  # 中英文字符串字典
├── theme.py                 # 深色/浅色主题 CSS
├── dataset_links.md         # 数据集论文链接（Markdown 格式）
├── rs_vlm_datasets.xlsx     # 数据集主文件（不纳入版本控制）
├── requirements.txt
├── .streamlit/
│   └── secrets.toml.example # 密钥配置模板
└── views/
    ├── intro_view.py        # 简介页
    ├── chat_view.py         # ChatECNU 对话
    ├── paper_view.py        # 论文讲解助手
    ├── filter_view.py       # 精准筛选
    ├── compare_view.py      # 数据集对比
    ├── leakage_view.py      # 数据泄露检测
    ├── leakage_graph.py     # 泄露关系可视化
    ├── stats_view.py        # 统计图表
    ├── nasa_view.py         # NASA 每日一图
    ├── result_card.py       # 数据集卡片组件
    ├── export_panel.py      # 筛选结果导出面板
    └── export_utils.py      # 导出工具（Excel/CSV/Word/BibTeX/Markdown/对话）
```

## 🔑 环境变量 / Secrets

| 变量名 | 用途 |
|--------|------|
| `CHATECNU_API_KEY` | ECNU 大模型，用于 ChatECNU 助手、字段翻译、对比翻译 |
| `OPENAI_API_KEY` | OpenAI 兼容接口（AutoDL Qwen），用于论文讲解助手 |

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

## 📄 License

[LICENSE](LICENSE.txt)

## 🔗 相关链接

- 数据集主页：[VisionXLab/Awesome-RS-VL-Data](https://github.com/VisionXLab/Awesome-RS-VL-Data)
