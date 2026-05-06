# 🌍 GeoChef — 遥感视觉语言数据集智能检索平台

*[立即使用GeoChef](https://geochef-v2-1.streamlit.app/)*

GeoChef 是一个面向遥感视觉语言（RS-VLM）领域的数据集智能检索与分析平台，**集成了七大核心功能模块**，提供从数据检索、对比分析到论文理解的全流程解决方案。平台基于 Streamlit 构建，集成 ECNU 大模型与 OpenAI 兼容接口，支持中英文双语与深色/浅色主题切换，**采用 NASA 风格配色方案，兼具专业性与美观性**。**无需本地部署，打开网页即可使用！**

**✨ 平台特色：**
- **功能全面**：七大模块覆盖遥感数据集全生命周期管理
- **设计独特**：全球首个集成数据泄露检测的遥感数据集平台
- **视觉美观**：NASA 风格配色 + 每日卫星图像，激发研究灵感
- **智能交互**：AI 论文讲解 + 专业问答，降低学习门槛
- **便捷使用**：零配置网页版，跨平台即时访问

---

## 🎯 核心功能与独创性

### 🔍 **精准筛选** · 多维检索引擎
- **独创的多维筛选体系**：数据模态 / 任务类型 / 年份 / 发布单位 / 方法类型五维交叉筛选
- **智能全文搜索**：基于关键词的语义检索，快速定位目标数据集
- **多格式导出**：支持 **Excel / CSV / Word / BibTeX / Markdown** 五种专业格式，满足不同场景需求

### 🔀 **数据集对比** · 可视化分析
- **智能并排对比**：最多 4 个数据集同时对比，差异字段自动高亮显示
- **雷达图分析**：生成数值指标雷达图，直观展示数据集特性差异与优势
- **结构化展示**：表格化呈现关键参数，便于学术引用与报告撰写

### ⚠️ **数据泄露检测** · **防患于未然**
- **倒排索引算法**：基于原始数据集构建高效检索索引，支持单源查询与批量检测
- **可视化关联图谱**：放射状节点图清晰展示数据泄露路径与关联关系
- **学术诚信保障**：为遥感领域研究者提供数据来源验证工具，填补行业空白

### 📚 **论文讲解助手** · **AI 学术伙伴**
- **智能论文解析**：输入数据集名称或论文链接，AI 流式生成结构化专业讲解
- **多轮深度对话**：支持追问与细节探讨，深入理解论文方法与创新点
- **学习笔记生成**：对话记录可导出，自动整理为学习笔记与参考文献

### 📊 **数据集统计** · 宏观洞察
- **多维概览图表**：年份分布 / 任务类型 / 数据模态 / 类别统计，把握领域发展脉络
- **地理可视化**：气泡地图展示论文来源国家分布，识别研究热点区域
- **趋势分析**：折线图 / 堆叠面积图 / 同比增速分析，预测领域发展方向

### 💬 **ChatECNU 助手** · 领域专家
- **遥感专业问答**：内置数据集搜索指导与数据泄露专业知识库
- **实时技术咨询**：解答遥感数据处理、模型训练、评估指标等技术疑问
- **对话存档**：专业讨论内容可导出，形成知识积累

### 🛰️ **NASA 每日一图** · **美学与灵感**
- **每日卫星影像**：自动拉取 NASA Earth Observatory 最新卫星图像，**优先展示当天图片**
- **NASA 风格设计**：平台整体采用 **NASA 官方配色方案**，深蓝/浅蓝/橙色主题，专业且美观
- **研究灵感激发**：浏览近期遥感图集，了解地球变化，激发遥感研究创意
- **视觉体验优化**：精心设计的界面布局与交互动画，提升使用愉悦度

---

## 🌐 立即使用

**无需安装，无需配置，打开网页即可体验全部功能：**

**[https://geochef-v2-1.streamlit.app/](https://geochef-v2-1.streamlit.app/)**

### 为什么选择 GeoChef？
- 🚀 **功能全面性**：七大模块覆盖遥感数据集全生命周期，从检索到分析一站式解决
- 🏆 **技术独创性**：全球首个集成数据泄露检测的遥感数据集平台，填补行业空白
- 🎨 **视觉美观性**：NASA 官方配色方案 + 每日卫星图像，专业界面激发研究灵感
- 🤖 **智能交互性**：AI 论文讲解 + 专业问答，降低遥感领域学习门槛
- 🌍 **便捷访问性**：零配置网页版，跨平台即时访问，无需环境部署

### 网页版核心优势：
- ✅ **零配置启动**：无需安装 Python、依赖包或配置环境，点击即用
- ✅ **数据预加载**：内置完整遥感视觉语言数据集，包含 100+ 个高质量数据集
- ✅ **API 已配置**：ECNU 大模型和 OpenAI 兼容接口已就绪，AI 功能开箱即用
- ✅ **跨平台访问**：支持 Windows、macOS、Linux、iOS、Android 全平台
- ✅ **实时更新**：功能更新自动同步，NASA 每日图像自动刷新
- ✅ **专业设计**：NASA 风格深色/浅色主题，精心优化的交互体验
---
### 本地部署（可选）
如果您需要自定义数据或进行二次开发，也可以选择本地部署：

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

- **立即使用网页版**：[https://geochef-v2-1.streamlit.app/](https://geochef-v2-1.streamlit.app/)
- 数据集主页：[VisionXLab/Awesome-RS-VL-Data](https://github.com/VisionXLab/Awesome-RS-VL-Data)
