import streamlit as st

# 功能卡片数据：(icon, cn_title, en_title, cn_desc, en_desc)
_FEATURES = [
    (
        "🔍", "精准筛选", "Precise Search",
        "多维度组合筛选 + 关键词全文搜索，结果支持 Excel / CSV / Word / BibTeX / Markdown 五种格式导出。",
        "Multi-dimensional filtering with full-text keyword search. Export results in Excel, CSV, Word, BibTeX, or Markdown.",
    ),
    (
        "🔀", "数据集对比", "Dataset Comparison",
        "最多同时对比 4 个数据集，差异字段自动高亮，并生成数值指标雷达图。",
        "Compare up to 4 datasets side by side with automatic difference highlighting and a numeric radar chart.",
    ),
    (
        "⚠️", "数据泄露检测", "Leakage Detection",
        "基于原始数据集索引，支持单源查询和批量检测，可视化关联关系图，结果可导出。",
        "Source-dataset index for single or batch leakage detection with relationship graph visualization and export.",
    ),
    (
        "📚", "论文讲解助手", "Paper Assistant",
        "输入数据集名称或论文链接，AI 生成结构化专业讲解，支持多轮追问和对话导出。",
        "Enter a dataset name or paper URL for structured AI explanations with follow-up Q&A and export.",
    ),
    (
        "📊", "数据集统计", "Statistics",
        "概览图表 · 地理分布世界地图 · 增长趋势分析（折线图 / 堆叠面积图 / 同比增速）。",
        "Overview charts · Geographic world map · Trend analysis with line, stacked area, and YoY growth charts.",
    ),
    (
        "💬", "ChatECNU 助手", "ChatECNU Assistant",
        "遥感领域问答助手，内置搜索指导与数据泄露知识，支持对话导出。",
        "Domain Q&A assistant with built-in search guidance and leakage knowledge, with conversation export.",
    ),
    (
        "🛰️", "NASA 每日一图", "NASA Image of Day",
        "自动拉取 NASA Earth Observatory 每日卫星图像，优先展示当天图片，可浏览近期图集。",
        "Auto-fetches NASA Earth Observatory's daily satellite image, with a browsable recent gallery.",
    ),
]


def _card(icon, title, desc, dark: bool) -> str:
    bg      = "#0f2035"          if dark else "#ffffff"
    border  = "#1a3050"          if dark else "#d0daea"
    text    = "#e8edf5"          if dark else "#061f4a"
    muted   = "#7a9bbf"          if dark else "#5a7a9e"
    primary = "#02bfe7"          if dark else "#0b3d91"
    icon_bg = "rgba(2,191,231,0.10)"  if dark else "rgba(11,61,145,0.07)"
    shadow  = "rgba(0,0,0,0.3)"  if dark else "rgba(6,31,74,0.07)"
    return (
        f"<div style='background:{bg};border:1px solid {border};border-radius:10px;"
        f"padding:1.1rem 1.1rem 1rem 1.1rem;box-shadow:0 2px 8px {shadow};"
        f"transition:box-shadow 0.2s;height:100%'>"
        f"<div style='display:flex;align-items:center;gap:0.6rem;margin-bottom:0.5rem'>"
        f"<span style='font-size:1.25rem;background:{icon_bg};border-radius:7px;"
        f"width:2.1rem;height:2.1rem;display:flex;align-items:center;justify-content:center'>"
        f"{icon}</span>"
        f"<span style='font-size:0.92rem;font-weight:700;color:{text}'>{title}</span>"
        f"</div>"
        f"<p style='font-size:0.81rem;color:{muted};line-height:1.6;margin:0'>{desc}</p>"
        f"</div>"
    )


def render_intro(lang: str):
    dark = st.session_state.get("theme_mode", "dark") == "dark"
    is_cn = lang == "cn"

    # 平台简介
    primary = "#02bfe7" if dark else "#0b3d91"
    text    = "#e8edf5" if dark else "#061f4a"
    muted   = "#7a9bbf" if dark else "#5a7a9e"
    bg_hero = "rgba(2,191,231,0.05)"   if dark else "rgba(11,61,145,0.04)"
    border  = "#1a3050"                if dark else "#d0daea"

    hero_cn = (
        f"<div style='background:{bg_hero};border:1px solid {border};border-radius:14px;"
        f"padding:1.4rem 1.6rem;margin-bottom:1.4rem'>"
        f"<div style='font-size:1.5rem;font-weight:800;color:{text};margin-bottom:0.4rem'>"
        f"🌍 GeoChef</div>"
        f"<p style='font-size:0.92rem;color:{muted};line-height:1.7;margin:0'>"
        f"面向<strong style='color:{primary}'>遥感视觉语言（RS-VLM）</strong>领域的数据集智能检索与分析平台，"
        f"基于 Streamlit 构建，集成 ECNU 大模型与 OpenAI 兼容接口。"
        f"收录 VQA、Caption、VG、Comprehensive Data 等多类别数据集。"
        f"</p></div>"
    )
    hero_en = (
        f"<div style='background:{bg_hero};border:1px solid {border};border-radius:14px;"
        f"padding:1.4rem 1.6rem;margin-bottom:1.4rem'>"
        f"<div style='font-size:1.5rem;font-weight:800;color:{text};margin-bottom:0.4rem'>"
        f"🌍 GeoChef</div>"
        f"<p style='font-size:0.92rem;color:{muted};line-height:1.7;margin:0'>"
        f"An intelligent retrieval &amp; analysis platform for "
        f"<strong style='color:{primary}'>Remote Sensing Vision-Language (RS-VLM)</strong> datasets, "
        f"built with Streamlit and powered by ECNU LLM &amp; OpenAI-compatible APIs. "
        f"Covers VQA, Caption, VG, Comprehensive Data and more."
        f"</p></div>"
    )
    st.markdown(hero_cn if is_cn else hero_en, unsafe_allow_html=True)

    # 功能卡片网格（3 列）
    feat_label = "核心功能" if is_cn else "Core Features"
    st.markdown(
        f"<p style='font-size:0.78rem;font-weight:700;color:{muted};"
        f"text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.7rem'>"
        f"{feat_label}</p>",
        unsafe_allow_html=True,
    )

    cols_per_row = 3
    rows = [_FEATURES[i:i+cols_per_row] for i in range(0, len(_FEATURES), cols_per_row)]
    for row in rows:
        cols = st.columns(len(row), gap="medium")
        for col, (icon, cn_t, en_t, cn_d, en_d) in zip(cols, row):
            with col:
                st.markdown(
                    _card(icon, cn_t if is_cn else en_t, cn_d if is_cn else en_d, dark),
                    unsafe_allow_html=True,
                )
        st.markdown("<div style='margin-bottom:0.6rem'></div>", unsafe_allow_html=True)

    st.divider()

    # 底部说明
    caption_cn = "数据持续更新中，欢迎访问 [Github 主页](https://github.com/VisionXLab/Awesome-RS-VL-Data) 了解更多。"
    caption_en = "Data is continuously updated. Visit the [GitHub page](https://github.com/VisionXLab/Awesome-RS-VL-Data) for more."
    st.caption(caption_cn if is_cn else caption_en)
