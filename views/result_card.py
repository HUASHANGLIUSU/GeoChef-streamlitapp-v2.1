import hashlib
import re
import streamlit as st
from model import ECNUModel
from github_parser import get_paper_link_by_name


def _md_line_to_html(line: str) -> str:
    """把 '- **key**: value' 格式的 Markdown 行转成 HTML span。"""
    line = line.strip()
    if not line:
        return ""
    # 替换 **text** 为 <b>text</b>
    line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
    # 去掉开头的 '- '
    if line.startswith("- "):
        line = line[2:]
    return f"<div class='field-kv'>- {line}</div>"

# 主要字段：大字显示
_PRIMARY_FIELDS = {"Name", "name", "Year", "year", "#Samples", "Modality", "modality", "Type", "type"}
# 跳过的内部字段
_SKIP_FIELDS = {"_sheet", "_text", "_years", "数据集备注"}


def _render_fields(raw_fields: list, lang: str, card_key: str):
    """把字段分主次两层渲染，英文模式走翻译缓存。"""
    primary = [(k, v) for k, v in raw_fields if k in _PRIMARY_FIELDS]
    secondary = [(k, v) for k, v in raw_fields if k not in _PRIMARY_FIELDS]

    if lang == "en":
        _fields_hash = hashlib.md5(str(raw_fields).encode()).hexdigest()[:8]
        cache_key = f"_trans_{card_key}_{_fields_hash}"
        if cache_key not in st.session_state:
            st.session_state[cache_key] = ECNUModel.translate_item_fields(raw_fields)
        all_lines = st.session_state[cache_key]
        # 按原始顺序拆回主次
        all_keys = [k for k, _ in raw_fields]
        primary_lines   = [_md_line_to_html(all_lines[i]) for i, (k, _) in enumerate(raw_fields) if k in _PRIMARY_FIELDS]
        secondary_lines = [_md_line_to_html(all_lines[i]) for i, (k, _) in enumerate(raw_fields) if k not in _PRIMARY_FIELDS]
    else:
        primary_lines   = [f"<div class='field-kv'>- <b>{k}</b>: {v}</div>" for k, v in primary]
        secondary_lines = [f"<div class='field-kv'>- <b>{k}</b>: {v}</div>" for k, v in secondary]

    if primary_lines:
        st.markdown(
            "<div class='field-primary'>" + " ".join(primary_lines) + "</div>",
            unsafe_allow_html=True,
        )
    if secondary_lines:
        st.markdown(
            "<div class='field-secondary'>" + " ".join(secondary_lines) + "</div>",
            unsafe_allow_html=True,
        )


def render_result_card(item: dict, card_key: str, i18n: dict, lang: str):
    """渲染单个数据集结果卡片，供精准筛选和泄露检测共用。"""
    with st.container(border=True):
        remark = str(item.get("数据集备注", "")).strip()
        if remark.lower() == "nan":
            remark = ""

        cols = st.columns([6, 3, 3], gap="large") if remark else st.columns([9, 3], gap="large")
        info_col  = cols[0]
        remark_col = cols[1] if remark else None
        btn_col   = cols[2] if remark else cols[1]

        with info_col:
            # 数据集名称 + 来源 sheet 标签
            name_val  = str(item.get("Name", item.get("name", ""))).strip()
            sheet_val = str(item.get("_sheet", "")).strip()
            dark = st.session_state.get("theme_mode", "dark") == "dark"
            tag_bg   = "rgba(59,130,246,0.12)" if dark else "rgba(37,99,235,0.08)"
            tag_text = "#93c5fd" if dark else "#1d4ed8"
            name_display = name_val or sheet_val or "Unknown"
            st.markdown(
                f"<div class='dataset-name'>"
                f"📁 {name_display}"
                f"<span class='field-tag'>{sheet_val}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

            raw_fields = [
                (k, v) for k, v in item.items()
                if k not in _SKIP_FIELDS and k not in {"Name", "name"} and v
            ]
            if raw_fields:
                _render_fields(raw_fields, lang, card_key)
            else:
                st.caption("暂无详细信息" if lang == "cn" else "No details")

        if remark and remark_col:
            with remark_col:
                st.markdown(
                    f"<p style='font-size:0.78rem;font-weight:700;text-transform:uppercase;"
                    f"letter-spacing:0.05em;opacity:0.6;margin-bottom:4px'>"
                    f"{i18n['remarks_label']}</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"<div class='explain-area'>{remark}</div>", unsafe_allow_html=True)

        with btn_col:
            paper_link = get_paper_link_by_name(name_val) if name_val else None
            if paper_link:
                st.markdown(
                    f'<a href="{paper_link}" target="_blank" class="link-button">'
                    f'{i18n["view_btn"]}</a>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    i18n["ai_explain_btn"],
                    key=f"explain_{card_key}",
                    use_container_width=True,
                    type="secondary",
                ):
                    st.session_state.pending_explain_link = paper_link
                    st.session_state.pending_explain_name = name_val
                    st.session_state.page = "paper"
                    st.rerun()
            else:
                st.info(i18n["no_paper_link"], icon="ℹ️")

            # 加入 / 移出对比
            if name_val:
                compare_data = st.session_state.get("_compare_data", [])
                in_compare   = name_val in compare_data

                if in_compare:
                    st.markdown("<div class='remove-btn'>", unsafe_allow_html=True)
                    if st.button(
                        i18n.get("compare_remove", "🗑️ 移出对比"),
                        key=f"remove_compare_{card_key}",
                        use_container_width=True,
                        type="secondary",
                    ):
                        st.session_state["_compare_data"] = [n for n in compare_data if n != name_val]
                        st.toast(i18n.get("compare_remove_ok", "已从对比列表移除"), icon="🗑️")
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    if st.button(
                        i18n.get("compare_add", "➕ 加入对比"),
                        key=f"add_compare_{card_key}",
                        use_container_width=True,
                        type="secondary",
                    ):
                        if len(compare_data) >= 4:
                            st.toast(i18n.get("compare_add_limit", "已达到对比上限（最多4个）"), icon="⚠️")
                        else:
                            st.session_state["_compare_data"] = compare_data + [name_val]
                            st.toast(i18n.get("compare_add_ok", "已加入对比列表"), icon="✅")
                            st.rerun()
