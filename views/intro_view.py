import streamlit as st


CN_INTRO = """
**GeoChef** 是一个面向遥感视觉语言（RS-VLM）领域的数据集智能检索与分析平台，基于 Streamlit 构建，集成了 ECNU 大模型与 OpenAI 兼容接口。

平台收录了 VQA、Caption、VG、Comprehensive Data 等多个类别的遥感视觉语言数据集，提供以下核心功能：

- 🔍 **精准筛选**：支持按数据模态、任务类型、发布年份、发布单位、方法类型多维度组合筛选，并支持关键词全文搜索
- 🔀 **数据集对比**：最多同时对比 4 个数据集，自动高亮差异字段，并生成数值指标雷达图
- ⚠️ **数据泄露检测**：基于"包含数据集"字段构建原始数据集索引，支持单源查询和批量检测，可视化展示数据集间的关联关系图，帮助研究者识别训练集与测试集之间的潜在数据泄露风险
- 📚 **论文讲解助手**：输入数据集名称或论文链接，调用大模型生成结构化的专业讲解，支持追问和中英文切换
- 📊 **统计概览**：以图表形式展示数据集在年份、任务类型、数据模态、类别维度上的分布情况
- 💬 **ChatECNU 助手**：基于 ECNU 大模型的领域问答助手，内置遥感数据集构建与数据泄露专业知识

平台支持深色/浅色主题切换与中英文双语界面，所有功能页面独立渲染，状态跨页面持久保留。
"""

EN_INTRO = """
**GeoChef** is an intelligent retrieval and analysis platform for Remote Sensing Vision-Language (RS-VLM) datasets, built with Streamlit and powered by the ECNU large language model and OpenAI-compatible APIs.

The platform covers multiple categories of RS-VLM datasets including VQA, Caption, VG, and Comprehensive Data, offering the following core features:

- 🔍 **Precise Search**: Multi-dimensional filtering by modality, task type, year, publisher, and method, with full-text keyword search
- 🔀 **Dataset Comparison**: Compare up to 4 datasets side by side, with automatic difference highlighting and a numeric radar chart
- ⚠️ **Data Leakage Detection**: Builds a source dataset index from the "包含数据集" field, supports single-source and batch detection, and visualizes dataset relationships to help researchers identify potential data leakage between train and test sets
- 📚 **Paper Assistant**: Enter a dataset name or paper URL to get a structured expert explanation, with follow-up Q&A and bilingual support
- 📊 **Statistics Overview**: Charts showing dataset distributions across year, task type, modality, and category
- 💬 **ChatECNU Assistant**: A domain-specific Q&A assistant powered by ECNU LLM, with built-in knowledge on RS dataset construction and data leakage

The platform supports dark/light theme switching and Chinese/English bilingual UI. All feature pages render independently with persistent state across navigation.
"""


def render_intro(lang: str):
    st.markdown(CN_INTRO if lang == "cn" else EN_INTRO)
    st.divider()
    st.caption(
        "数据持续更新中，欢迎访问 [Github 主页](https://github.com/VisionXLab/Awesome-RS-VL-Data) 了解更多。"
        if lang == "cn" else
        "Data is continuously updated. Visit the [GitHub page](https://github.com/VisionXLab/Awesome-RS-VL-Data) for more."
    )
