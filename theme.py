import streamlit as st

# ── NASA 色彩体系参考 ──────────────────────────────────────────────────────────
# 深色模式：以 NASA 深空蓝为基调，青色 #02bfe7 作为强调色
# 浅色模式：以 NASA 官网白底 + 深蓝文字为基调，干净、专业、高对比度


def get_theme_css():
    dark = st.session_state.theme_mode == "dark"

    if dark:
        # ── 深色：深空蓝调 ─────────────────────────────────────────────────────
        primary        = "#02bfe7"          # NASA cyan / 主强调色
        primary_dark   = "#046b99"          # NASA primary-alt-darkest
        primary_glow   = "rgba(2,191,231,0.15)"
        bg             = "#060d1a"          # 近黑深空蓝
        bg2            = "#0b1829"          # 次级背景
        card_bg        = "#0f2035"          # 卡片背景
        card_bg2       = "#132640"
        input_bg       = "#0b1829"
        text           = "#e8edf5"          # 近白，略带蓝调
        text_muted     = "#7a9bbf"          # 中灰蓝
        border         = "#1a3050"
        border_light   = "#1e3a5f"
        hover_bg       = "rgba(2,191,231,0.08)"
        sidebar_bg     = "#040c17"          # 比主背景更深
        topbar_from    = "#0b3d91"          # NASA primary-darker
        topbar_to      = "#061f4a"          # NASA primary-darkest
        badge_bg       = "rgba(2,191,231,0.12)"
        tag_bg         = "rgba(2,191,231,0.10)"
        tag_text       = "#02bfe7"
        shadow         = "rgba(0,0,0,0.5)"
        shadow_card    = "rgba(0,0,0,0.35)"
        user_msg_bg    = "#0b3d91"
        asst_msg_bg    = "#0f2035"
        no_result_bg   = "#0b1829"
        explain_bg     = "rgba(2,191,231,0.06)"
        hint_border    = "rgba(2,191,231,0.35)"
        hint_bg        = "rgba(2,191,231,0.06)"
        accent_bar     = "#02bfe7"
        divider        = "#1a3050"
        # 地图配色
        map_land       = "#0b1829"
        map_ocean      = "#040c17"
        map_choropleth = [
            [0.0,  "#061f4a"],
            [0.2,  "#0b3d91"],
            [0.5,  "#046b99"],
            [0.75, "#00a6d2"],
            [1.0,  "#02bfe7"],
        ]
    else:
        # ── 浅色：NASA 官网白底深蓝调 ─────────────────────────────────────────
        primary        = "#0b3d91"          # NASA primary-darker
        primary_dark   = "#061f4a"          # NASA primary-darkest
        primary_glow   = "rgba(11,61,145,0.10)"
        bg             = "#f8fafd"          # 极浅蓝白
        bg2            = "#eef2f9"          # 次级背景，带蓝调
        card_bg        = "#ffffff"
        card_bg2       = "#f4f7fc"
        input_bg       = "#ffffff"
        text           = "#061f4a"          # NASA primary-darkest，深蓝黑
        text_muted     = "#5a7a9e"          # 中蓝灰
        border         = "#d0daea"          # 冷蓝灰边框
        border_light   = "#dce4ef"          # NASA cool-blue-lightest
        hover_bg       = "#dce4ef"          # NASA cool-blue-lightest
        sidebar_bg     = "#eef2f9"
        topbar_from    = "#dce4ef"          # NASA cool-blue-lightest
        topbar_to      = "#f8fafd"
        badge_bg       = "rgba(11,61,145,0.07)"
        tag_bg         = "rgba(11,61,145,0.07)"
        tag_text       = "#0b3d91"
        shadow         = "rgba(6,31,74,0.08)"
        shadow_card    = "rgba(6,31,74,0.07)"
        user_msg_bg    = "#0b3d91"
        asst_msg_bg    = "#eef2f9"
        no_result_bg   = "#f4f7fc"
        explain_bg     = "#dce4ef"
        hint_border    = "rgba(11,61,145,0.25)"
        hint_bg        = "rgba(11,61,145,0.05)"
        accent_bar     = "#0b3d91"
        divider        = "#d0daea"
        # 地图配色
        map_land       = "#eef2f9"
        map_ocean      = "#dce4ef"
        map_choropleth = [
            [0.0,  "#dce4ef"],
            [0.2,  "#8ba6ca"],
            [0.5,  "#4773aa"],
            [0.75, "#046b99"],
            [1.0,  "#0b3d91"],
        ]

    # 把地图配色存入 session_state 供 stats_view 使用
    st.session_state["_map_choropleth"] = map_choropleth
    st.session_state["_map_land"]       = map_land
    st.session_state["_map_ocean"]      = map_ocean

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
strong {{ color: {text} !important; }}

/* ── 顶栏 ─────────────────────────────────────────────── */
.topbar-wrap {{
    background: linear-gradient(135deg, {topbar_from} 0%, {topbar_to} 100%);
    border-radius: 12px;
    padding: 0.9rem 1.4rem;
    margin-bottom: 1.4rem;
    border: 1px solid {border};
    box-shadow: 0 4px 16px {shadow};
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}
.topbar-icon {{ font-size: 1.5rem; line-height: 1; }}
.topbar-title {{
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin: 0 !important;
    letter-spacing: -0.01em;
    text-shadow: 0 1px 4px rgba(0,0,0,0.3);
}}
.topbar-accent {{
    display: inline-block;
    width: 4px;
    height: 1.3rem;
    background: {primary};
    border-radius: 2px;
    flex-shrink: 0;
    box-shadow: 0 0 8px {primary};
}}

/* ── 侧边栏 ───────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background-color: {sidebar_bg} !important;
    border-right: 1px solid {border} !important;
}}
section[data-testid="stSidebar"] * {{ color: {text} !important; }}

.sidebar-title {{
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    color: {text} !important;
    letter-spacing: -0.02em;
}}
.sidebar-subtitle {{
    font-size: 0.7rem;
    color: {text_muted} !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 1px;
}}

/* 侧边栏普通导航按钮 */
section[data-testid="stSidebar"] .stButton > button {{
    background-color: transparent !important;
    color: {text} !important;
    border: none !important;
    border-radius: 6px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 0.42rem 0.75rem !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    height: 36px !important;
    transition: background 0.15s ease !important;
    box-shadow: none !important;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
    background-color: {hover_bg} !important;
    transform: none !important;
    box-shadow: none !important;
}}
/* 激活页面：左侧强调色竖条 + 高亮背景 */
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
    background-color: {badge_bg} !important;
    color: {primary} !important;
    border-left: 3px solid {primary} !important;
    border-radius: 0 6px 6px 0 !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}}
section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {{
    background-color: {badge_bg} !important;
    transform: none !important;
}}

/* ── 主区域按钮 ───────────────────────────────────────── */
.stButton > button {{
    border-radius: 6px !important;
    border: none !important;
    box-shadow: 0 1px 4px {shadow} !important;
    transition: all 0.18s ease !important;
    height: 40px !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    color: white !important;
    background-color: {primary} !important;
    letter-spacing: 0.01em !important;
}}
.stButton > button[kind="secondary"] {{
    background-color: {card_bg} !important;
    color: {text} !important;
    border: 1px solid {border} !important;
    box-shadow: none !important;
    font-weight: 500 !important;
}}
.stButton > button:hover {{
    box-shadow: 0 4px 14px {shadow} !important;
    transform: translateY(-1px) !important;
    filter: brightness(1.08) !important;
}}
.stButton > button[kind="secondary"]:hover {{
    background-color: {hover_bg} !important;
    border-color: {primary} !important;
    color: {primary} !important;
    filter: none !important;
    transform: translateY(-1px) !important;
}}

/* ── 输入框 ───────────────────────────────────────────── */
.stTextInput > div > div > input {{
    border-radius: 6px !important;
    border: 1px solid {border} !important;
    background-color: {input_bg} !important;
    padding: 0.55rem 1rem !important;
    color: {text} !important;
    font-size: 0.9rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: {primary} !important;
    box-shadow: 0 0 0 3px {primary_glow} !important;
    outline: none !important;
}}
.stTextInput > div > div > input::placeholder {{ color: {text_muted} !important; }}

.stMultiSelect > div,
div[data-baseweb="select"] > div {{
    border-radius: 6px !important;
    border: 1px solid {border} !important;
    background-color: {input_bg} !important;
    color: {text} !important;
}}

/* ── Streamlit container border ──────────────────────── */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-color: {border} !important;
    background-color: {card_bg} !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 10px {shadow_card} !important;
    transition: box-shadow 0.2s ease !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    box-shadow: 0 4px 18px {shadow_card} !important;
}}

/* ── 数据集卡片字段层级 ───────────────────────────────── */
.dataset-name {{
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: {text} !important;
    margin-bottom: 0.45rem !important;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    flex-wrap: wrap;
}}
.field-tag {{
    display: inline-block;
    background: {tag_bg};
    color: {tag_text};
    border-radius: 4px;
    padding: 1px 7px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    margin: 1px 2px;
}}
.field-primary {{
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    color: {text} !important;
    line-height: 1.6 !important;
}}
.field-secondary {{
    font-size: 0.81rem !important;
    color: {text_muted} !important;
    line-height: 1.55 !important;
    margin-top: 0.2rem !important;
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
    border-radius: 6px !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    margin-bottom: 8px !important;
    transition: opacity 0.15s, transform 0.15s !important;
    box-shadow: 0 2px 8px {shadow} !important;
}}
.link-button:hover {{
    opacity: 0.92 !important;
    transform: translateY(-1px) !important;
}}

/* ── 提示条 ───────────────────────────────────────────── */
.chat-hint {{
    padding: 0.6rem 1rem !important;
    border-radius: 6px !important;
    border: 1px solid {hint_border} !important;
    background: {hint_bg} !important;
    font-size: 0.875rem !important;
    line-height: 1.5 !important;
    color: {text} !important;
}}

/* ── 无结果提示 ───────────────────────────────────────── */
.no-result {{
    padding: 2.5rem 2rem !important;
    text-align: center !important;
    background-color: {no_result_bg} !important;
    border-radius: 10px !important;
    border: 1px dashed {border} !important;
    color: {text_muted} !important;
    margin: 1rem 0 !important;
}}
.no-result h4 {{ color: {text} !important; margin-bottom: 0.4rem !important; }}

/* ── 备注区 ───────────────────────────────────────────── */
.explain-area {{
    background-color: {explain_bg} !important;
    border-radius: 6px !important;
    border-left: 3px solid {primary} !important;
    padding: 0.75rem 1rem !important;
    margin-top: 0.5rem !important;
    line-height: 1.6 !important;
    color: {text} !important;
    font-size: 0.875rem !important;
}}

/* ── 对话消息 ─────────────────────────────────────────── */
div[data-testid="stChatMessage"] {{
    background-color: {card_bg} !important;
    border-color: {border} !important;
    border-radius: 10px !important;
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
    font-weight: 700 !important;
}}

/* ── DataFrame ────────────────────────────────────────── */
div[data-testid="stDataFrame"] {{
    background-color: {card_bg} !important;
    border-color: {border} !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}}

/* ── Caption ──────────────────────────────────────────── */
div[data-testid="stCaptionContainer"] p {{
    color: {text_muted} !important;
    font-size: 0.82rem !important;
}}

/* ── Divider ──────────────────────────────────────────── */
hr {{ border-color: {divider} !important; opacity: 0.7 !important; }}

/* ── GitHub 链接 ──────────────────────────────────────── */
.github-link {{
    color: {primary} !important;
    text-decoration: none !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 4px !important;
    opacity: 0.9 !important;
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
    color: #e63946 !important;
    border-color: #e63946 !important;
}}

/* ── 滚动条 ───────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: {border};
    border-radius: 3px;
}}
::-webkit-scrollbar-thumb:hover {{ background: {text_muted}; }}

/* ── 浅色模式专项适配 ─────────────────────────────────── */
{"" if dark else f"""
/* 浅色下 Streamlit 默认白底组件补色 */
.stApp > div {{ background-color: {bg} !important; }}
div[data-testid="stAppViewContainer"] {{ background-color: {bg} !important; }}
div[data-testid="stHeader"] {{ background-color: {bg} !important; }}
div[data-testid="stToolbar"] {{ background-color: {bg} !important; }}
/* 浅色下 multiselect tag */
span[data-baseweb="tag"] {{
    background-color: {tag_bg} !important;
    color: {tag_text} !important;
    border-radius: 4px !important;
}}
/* 浅色下 selectbox 下拉 */
ul[data-testid="stSelectboxVirtualDropdown"],
ul[role="listbox"] {{
    background-color: {card_bg} !important;
    border: 1px solid {border} !important;
    border-radius: 6px !important;
    box-shadow: 0 4px 16px {shadow_card} !important;
}}
li[role="option"]:hover {{
    background-color: {hover_bg} !important;
}}
/* 浅色下 info box */
div[data-testid="stInfo"] {{
    background-color: {explain_bg} !important;
    border-color: {border} !important;
    color: {text} !important;
    border-radius: 6px !important;
}}
"""}
</style>
"""
