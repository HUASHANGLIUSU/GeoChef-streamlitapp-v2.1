import streamlit as st


def get_theme_css():
    dark = st.session_state.theme_mode == "dark"

    if dark:
        primary        = "#3b82f6"
        primary_dark   = "#1d4ed8"
        primary_glow   = "rgba(59,130,246,0.18)"
        bg             = "#0f172a"
        bg2            = "#1e293b"
        card_bg        = "#1e293b"
        card_bg2       = "#263347"
        input_bg       = "#1e293b"
        text           = "#f1f5f9"
        text_muted     = "#94a3b8"
        border         = "#334155"
        border_light   = "#2d3f55"
        hover_bg       = "#2d3f55"
        sidebar_bg     = "#0d1526"
        topbar_from    = "#1e3a5f"
        topbar_to      = "#0f172a"
        badge_bg       = "rgba(59,130,246,0.15)"
        tag_bg         = "rgba(59,130,246,0.12)"
        tag_text       = "#93c5fd"
        shadow         = "rgba(0,0,0,0.4)"
        shadow_card    = "rgba(0,0,0,0.3)"
        user_msg_bg    = "#1d4ed8"
        asst_msg_bg    = "#1e293b"
        no_result_bg   = "#1e293b"
        explain_bg     = "#1a2d45"
        hint_border    = "rgba(59,130,246,0.4)"
        hint_bg        = "rgba(59,130,246,0.08)"
    else:
        primary        = "#2563eb"
        primary_dark   = "#1d4ed8"
        primary_glow   = "rgba(37,99,235,0.12)"
        bg             = "#f8fafc"
        bg2            = "#f1f5f9"
        card_bg        = "#ffffff"
        card_bg2       = "#f8fafc"
        input_bg       = "#ffffff"
        text           = "#0f172a"
        text_muted     = "#64748b"
        border         = "#e2e8f0"
        border_light   = "#cbd5e1"
        hover_bg       = "#eff6ff"
        sidebar_bg     = "#f1f5f9"
        topbar_from    = "#dbeafe"
        topbar_to      = "#f8fafc"
        badge_bg       = "rgba(37,99,235,0.08)"
        tag_bg         = "rgba(37,99,235,0.08)"
        tag_text       = "#1d4ed8"
        shadow         = "rgba(0,0,0,0.06)"
        shadow_card    = "rgba(0,0,0,0.08)"
        user_msg_bg    = "#2563eb"
        asst_msg_bg    = "#f1f5f9"
        no_result_bg   = "#f8fafc"
        explain_bg     = "#eff6ff"
        hint_border    = "rgba(37,99,235,0.35)"
        hint_bg        = "rgba(37,99,235,0.06)"

    return f"""
<style>
/* ── 全局重置 ─────────────────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; }}

/* ── 主背景 ───────────────────────────────────────────── */
.stApp {{
    background-color: {bg} !important;
    color: {text} !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                 "Hiragino Sans GB", "Microsoft YaHei", sans-serif !important;
}}

/* ── 字体层级 ─────────────────────────────────────────── */
h1 {{ font-size: 1.75rem !important; font-weight: 700 !important;
      color: {text} !important; letter-spacing: -0.02em !important; }}
h2 {{ font-size: 1.35rem !important; font-weight: 600 !important;
      color: {text} !important; letter-spacing: -0.01em !important; }}
h3 {{ font-size: 1.05rem !important; font-weight: 600 !important;
      color: {text} !important; }}
h4, h5 {{ font-size: 0.9rem !important; font-weight: 600 !important;
           color: {text} !important; }}
p, li {{ color: {text} !important; line-height: 1.65 !important; }}

/* ── 顶栏 ─────────────────────────────────────────────── */
.topbar-wrap {{
    background: linear-gradient(135deg, {topbar_from} 0%, {topbar_to} 100%);
    border-radius: 14px;
    padding: 1rem 1.4rem 0.9rem 1.4rem;
    margin-bottom: 1.4rem;
    border: 1px solid {border};
    box-shadow: 0 2px 12px {shadow};
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}
.topbar-icon {{
    font-size: 1.6rem;
    line-height: 1;
}}
.topbar-title {{
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: {text} !important;
    margin: 0 !important;
    letter-spacing: -0.01em;
}}
.topbar-accent {{
    display: inline-block;
    width: 4px;
    height: 1.4rem;
    background: linear-gradient(180deg, {primary} 0%, {primary_dark} 100%);
    border-radius: 2px;
    flex-shrink: 0;
}}

/* ── 侧边栏 ───────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background-color: {sidebar_bg} !important;
    border-right: 1px solid {border} !important;
}}
section[data-testid="stSidebar"] * {{
    color: {text} !important;
}}
/* 侧边栏标题 */
.sidebar-title {{
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    color: {text} !important;
    letter-spacing: -0.02em;
    padding: 0.2rem 0 0.1rem 0;
}}
.sidebar-subtitle {{
    font-size: 0.72rem;
    color: {text_muted} !important;
    margin-top: -2px;
    letter-spacing: 0.03em;
}}
/* 侧边栏普通导航按钮 */
section[data-testid="stSidebar"] .stButton > button {{
    background-color: transparent !important;
    color: {text} !important;
    border: none !important;
    border-radius: 8px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 0.45rem 0.75rem !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    height: 38px !important;
    transition: background 0.15s ease !important;
    box-shadow: none !important;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
    background-color: {hover_bg} !important;
    transform: none !important;
    box-shadow: none !important;
}}
/* 激活页面按钮：左侧蓝色竖条 + 高亮背景 */
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
    background-color: {primary_glow} !important;
    color: {primary} !important;
    border-left: 3px solid {primary} !important;
    border-radius: 0 8px 8px 0 !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}}
section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {{
    background-color: {primary_glow} !important;
    transform: none !important;
}}

/* ── 主区域按钮 ───────────────────────────────────────── */
.stButton > button {{
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 1px 3px {shadow} !important;
    transition: all 0.18s ease !important;
    height: 40px !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    color: white !important;
    background-color: {primary} !important;
    letter-spacing: 0.01em !important;
}}
.stButton > button[kind="secondary"] {{
    background-color: {card_bg} !important;
    color: {text} !important;
    border: 1px solid {border} !important;
    box-shadow: none !important;
}}
.stButton > button:hover {{
    box-shadow: 0 4px 12px {shadow} !important;
    transform: translateY(-1px) !important;
    filter: brightness(1.05) !important;
}}
.stButton > button[kind="secondary"]:hover {{
    background-color: {hover_bg} !important;
    border-color: {primary} !important;
    color: {primary} !important;
    filter: none !important;
}}

/* ── 输入框 ───────────────────────────────────────────── */
.stTextInput > div > div > input {{
    border-radius: 8px !important;
    border: 1px solid {border} !important;
    background-color: {input_bg} !important;
    padding: 0.55rem 1rem !important;
    color: {text} !important;
    font-size: 0.9rem !important;
    transition: border-color 0.15s ease !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: {primary} !important;
    box-shadow: 0 0 0 3px {primary_glow} !important;
}}
.stMultiSelect > div {{
    border-radius: 8px !important;
    border: 1px solid {border} !important;
    background-color: {input_bg} !important;
    color: {text} !important;
}}
div[data-baseweb="select"] > div {{
    background-color: {input_bg} !important;
    border-color: {border} !important;
    color: {text} !important;
    border-radius: 8px !important;
}}

/* ── 筛选区容器 ───────────────────────────────────────── */
.filter-section {{
    background: {card_bg} !important;
    border: 1px solid {border} !important;
    border-radius: 12px !important;
    padding: 1.1rem 1.2rem 0.8rem 1.2rem !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 1px 4px {shadow} !important;
}}
.filter-label {{
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    color: {text_muted} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    margin-bottom: 0.35rem !important;
}}

/* ── 数据集卡片 ───────────────────────────────────────── */
/* Streamlit container border */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-color: {border} !important;
    background-color: {card_bg} !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px {shadow_card} !important;
    transition: box-shadow 0.2s ease !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    box-shadow: 0 4px 16px {shadow_card} !important;
}}
/* 卡片内字段标签 */
.field-primary {{
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: {text} !important;
}}
.field-secondary {{
    font-size: 0.82rem !important;
    color: {text_muted} !important;
    line-height: 1.55 !important;
}}
/* 数据集名称标签 */
.dataset-name {{
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: {text} !important;
    margin-bottom: 0.5rem !important;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}}
/* 字段 tag 样式 */
.field-tag {{
    display: inline-block;
    background: {tag_bg};
    color: {tag_text};
    border-radius: 4px;
    padding: 1px 7px;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 2px 3px 2px 0;
}}

/* ── 链接按钮 ─────────────────────────────────────────── */
.link-button {{
    display: block !important;
    width: 100% !important;
    height: 38px !important;
    line-height: 38px !important;
    text-align: center !important;
    background: linear-gradient(135deg, {primary} 0%, {primary_dark} 100%) !important;
    color: white !important;
    border-radius: 8px !important;
    text-decoration: none !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    margin-bottom: 8px !important;
    transition: opacity 0.15s ease !important;
    box-shadow: 0 2px 6px {shadow} !important;
}}
.link-button:hover {{ opacity: 0.9 !important; }}

/* ── 提示条 ───────────────────────────────────────────── */
.chat-hint {{
    padding: 0.6rem 1rem !important;
    border-radius: 8px !important;
    border: 1px solid {hint_border} !important;
    background: {hint_bg} !important;
    font-size: 0.87rem !important;
    line-height: 1.5 !important;
    color: {text} !important;
}}

/* ── 无结果提示 ───────────────────────────────────────── */
.no-result {{
    padding: 2.5rem 2rem !important;
    text-align: center !important;
    background-color: {no_result_bg} !important;
    border-radius: 12px !important;
    border: 1px dashed {border} !important;
    color: {text_muted} !important;
    margin: 1rem 0 !important;
}}
.no-result h4 {{ color: {text} !important; margin-bottom: 0.4rem !important; }}

/* ── 备注区 ───────────────────────────────────────────── */
.explain-area {{
    background-color: {explain_bg} !important;
    border-radius: 8px !important;
    border-left: 3px solid {primary} !important;
    padding: 0.8rem 1rem !important;
    margin-top: 0.6rem !important;
    line-height: 1.6 !important;
    color: {text} !important;
    font-size: 0.88rem !important;
}}

/* ── 对话消息 ─────────────────────────────────────────── */
div[data-testid="stChatMessage"] {{
    background-color: {card_bg} !important;
    border-color: {border} !important;
    border-radius: 12px !important;
    color: {text} !important;
}}
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] code {{
    color: {text} !important;
}}

/* ── Expander ─────────────────────────────────────────── */
details > summary {{
    color: {text} !important;
    background-color: {card_bg} !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}}
details[open] > summary, details {{
    background-color: {card_bg} !important;
    border-color: {border} !important;
    border-radius: 8px !important;
}}

/* ── Tabs ─────────────────────────────────────────────── */
div[data-testid="stTabs"] button {{
    color: {text_muted} !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}}
div[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {primary} !important;
    border-bottom-color: {primary} !important;
    font-weight: 600 !important;
}}

/* ── DataFrame ────────────────────────────────────────── */
div[data-testid="stDataFrame"] {{
    background-color: {card_bg} !important;
    border-color: {border} !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}}

/* ── Caption ──────────────────────────────────────────── */
div[data-testid="stCaptionContainer"] p {{
    color: {text_muted} !important;
    font-size: 0.82rem !important;
}}

/* ── Divider ──────────────────────────────────────────── */
hr {{ border-color: {border} !important; opacity: 0.6 !important; }}

/* ── GitHub 链接 ──────────────────────────────────────── */
.github-link {{
    color: {primary} !important;
    text-decoration: none !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 4px !important;
    opacity: 0.85 !important;
    transition: opacity 0.15s !important;
}}
.github-link:hover {{ opacity: 1 !important; text-decoration: underline !important; }}

/* ── 泄露检测按钮对齐 ─────────────────────────────────── */
.leak-button-wrapper {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 100% !important;
    margin-top: 24px !important;
}}

/* ── 移出对比按钮 ─────────────────────────────────────── */
.remove-btn button {{
    color: #ef4444 !important;
    border-color: #ef4444 !important;
}}

/* ── 滚动条美化 ───────────────────────────────────────── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: {border};
    border-radius: 3px;
}}
::-webkit-scrollbar-thumb:hover {{ background: {text_muted}; }}
</style>
"""
