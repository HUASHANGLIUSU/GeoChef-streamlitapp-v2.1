import streamlit as st


def get_theme_css():
    if st.session_state.theme_mode == "dark":
        primary_color = "#2563eb"
        bg_color = "#111827"
        card_bg = "#1f2937"
        input_bg = "#374151"
        text_color = "#f9fafb"
        border_color = "#374151"
        hover_color = "#4b5563"
        user_msg_bg = "#3b82f6"
        user_msg_text = "#ffffff"
        assistant_msg_bg = "#374151"
        assistant_msg_text = "#f9fafb"
        no_result_bg = "#1f2937"
        explain_area_bg = "#374151"
        sidebar_bg = "#1a2332"        # 侧边栏比主背景深
    else:
        primary_color = "#3b5bdb"
        bg_color = "#f5f0eb"          # 暖米色背景
        card_bg = "#fffdf9"           # 卡片略白，和背景有区分
        input_bg = "#fffdf9"
        text_color = "#1a1a2e"        # 深蓝黑，比纯黑柔和
        border_color = "#d4c5b0"      # 暖棕色边框
        hover_color = "#e8e0f5"       # 淡紫悬停
        user_msg_bg = "#3b5bdb"
        user_msg_text = "#ffffff"
        assistant_msg_bg = "#ede8e0"  # 暖灰，和背景有区分
        assistant_msg_text = "#1a1a2e"
        no_result_bg = "#f0ebe3"
        explain_area_bg = "#eae4f7"   # 淡紫备注区
        sidebar_bg = "#ede8e0"        # 侧边栏暖灰，比主背景深一点

    return f"""
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
.stApp {{
    max-width: 1200px; margin: 0 auto; padding: 1rem 2rem;
    background-color: {bg_color} !important; color: {text_color} !important;
}}
h1, h2, h3, h4, h5, h6 {{ color: {text_color} !important; }}
.stButton > button {{
    border-radius: 8px !important; border: none !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    transition: all 0.2s ease !important; height: 40px !important;
    font-weight: 500 !important; color: white !important;
    background-color: {primary_color} !important;
}}
.stButton > button[type="secondary"] {{
    background-color: {hover_color} !important; color: {primary_color} !important;
    border: 1px solid {border_color} !important;
}}
.stButton > button:hover {{
    box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    transform: translateY(-1px) !important; opacity: 0.95;
}}
.stMultiSelect > div {{
    border-radius: 8px !important; border: 1px solid {border_color} !important;
    background-color: {input_bg} !important; color: {text_color} !important;
}}
.stTextInput > div > div > input {{
    border-radius: 8px !important; border: 1px solid {border_color} !important;
    background-color: {input_bg} !important; padding: 0.6rem 1rem !important;
    color: {text_color} !important;
}}
.result-card {{
    background-color: {card_bg} !important; border-radius: 12px !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06) !important;
    padding: 1.5rem !important; margin-bottom: 1.5rem !important;
    border: 1px solid {border_color} !important; color: {text_color} !important;
}}
.no-result {{
    padding: 2rem !important; text-align: center !important;
    background-color: {no_result_bg} !important; border-radius: 12px !important;
    border: 1px dashed {border_color} !important; color: {text_color} !important;
    margin: 1rem 0 !important;
}}
.explain-area {{
    background-color: {explain_area_bg} !important; border-radius: 8px !important;
    padding: 1rem !important; margin-top: 0.8rem !important;
    line-height: 1.6 !important; color: {text_color} !important;
}}
.github-link {{
    color: {primary_color} !important; text-decoration: none !important;
    font-weight: 500 !important; display: inline-block !important; margin-top: 8px !important;
}}
.github-link:hover {{ text-decoration: underline !important; }}
.chat-history {{
    max-height: 300px !important; overflow-y: auto !important;
    padding: 1rem !important; border-radius: 8px !important;
    background-color: {card_bg} !important; margin-bottom: 1rem !important;
    border: 1px solid {border_color} !important;
}}
.user-message {{
    background-color: {user_msg_bg} !important; padding: 0.8rem 1rem !important;
    border-radius: 8px !important; margin-bottom: 0.8rem !important;
    text-align: right !important; color: {user_msg_text} !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
}}
.assistant-message {{
    background-color: {assistant_msg_bg} !important; padding: 0.8rem 1rem !important;
    border-radius: 8px !important; margin-bottom: 0.8rem !important;
    text-align: left !important; color: {assistant_msg_text} !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
}}
ul {{ margin: 0.8rem 0 !important; padding-left: 1.8rem !important; }}
li {{ margin-bottom: 0.5rem; color: {text_color} !important; line-height: 1.5 !important; }}
.link-button {{
    display: block !important; width: 100% !important; height: 40px !important;
    line-height: 40px !important; text-align: center !important;
    background-color: {primary_color} !important; color: white !important;
    border-radius: 8px !important; text-decoration: none !important;
    font-weight: 500 !important; margin-bottom: 8px !important;
}}
.leak-button-wrapper {{
    display: flex !important; align-items: center !important;
    justify-content: center !important; height: 100% !important; margin-top: 24px !important;
}}
/* ── Streamlit 原生组件颜色适配 ── */
/* container border */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-color: {border_color} !important;
    background-color: {card_bg} !important;
    border-radius: 10px !important;
}}
/* expander */
details > summary {{
    color: {text_color} !important;
    background-color: {card_bg} !important;
}}
details[open] > summary, details {{
    background-color: {card_bg} !important;
    border-color: {border_color} !important;
}}
/* tabs */
div[data-testid="stTabs"] button {{
    color: {text_color} !important;
}}
div[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {primary_color} !important;
    border-bottom-color: {primary_color} !important;
}}
/* dataframe */
div[data-testid="stDataFrame"] {{
    background-color: {card_bg} !important;
    border-color: {border_color} !important;
}}
/* chat_message */
div[data-testid="stChatMessage"] {{
    background-color: {card_bg} !important;
    border-color: {border_color} !important;
    color: {text_color} !important;
}}
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] code {{
    color: {text_color} !important;
}}
/* selectbox / multiselect dropdown */
div[data-baseweb="select"] > div {{
    background-color: {input_bg} !important;
    border-color: {border_color} !important;
    color: {text_color} !important;
}}
/* caption / small text */
div[data-testid="stCaptionContainer"] p {{
    color: {text_color} !important; opacity: 0.7;
}}
/* 侧边栏背景和文字 */
section[data-testid="stSidebar"] {{
    background-color: {sidebar_bg} !important;
    border-right: 1px solid {border_color} !important;
}}
section[data-testid="stSidebar"] * {{
    color: {text_color} !important;
}}
section[data-testid="stSidebar"] .stButton > button {{
    background-color: {input_bg} !important;
    color: {text_color} !important;
    border: 1px solid {border_color} !important;
    text-align: left !important;
    justify-content: flex-start !important;
}}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
    background-color: {primary_color} !important;
    color: white !important;
    border: none !important;
}}/* 移出对比按钮红色样式 */
.remove-btn button {{
    color: #ef4444 !important;
    border-color: #ef4444 !important;
}}</style>
"""
