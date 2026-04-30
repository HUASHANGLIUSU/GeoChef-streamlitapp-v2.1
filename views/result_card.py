import streamlit as st
from model import ECNUModel
from github_parser import get_paper_link_by_name


def render_result_card(item: dict, card_key: str, i18n: dict, lang: str):
    """渲染单个数据集结果卡片，供精准筛选和泄露检测共用。"""
    with st.container(border=True):
        remark = str(item.get("数据集备注", "")).strip()
        if remark.lower() == "nan":
            remark = ""

        cols = st.columns([6, 3, 3], gap="large") if remark else st.columns([9, 3], gap="large")
        info_col = cols[0]
        remark_col = cols[1] if remark else None
        btn_col = cols[2] if remark else cols[1]

        with info_col:
            st.markdown(f"### 📁 {item.get('_sheet', item.get('name', 'Unknown'))}")
            raw_fields = [
                (k, v) for k, v in item.items()
                if k not in ["_sheet", "_text", "_years", "数据集备注"] and v
            ]
            if lang == "en" and raw_fields:
                import hashlib
                _fields_hash = hashlib.md5(str(raw_fields).encode()).hexdigest()[:8]
                cache_key = f"_trans_{card_key}_{_fields_hash}"
                if cache_key not in st.session_state:
                    st.session_state[cache_key] = ECNUModel.translate_item_fields(raw_fields)
                lines = st.session_state[cache_key]
            else:
                lines = [f"- **{k}**: {v}" for k, v in raw_fields]
            st.markdown("\n".join(lines) if lines else ("- 暂无详细信息" if lang == "cn" else "- No details"))

        if remark and remark_col:
            with remark_col:
                st.markdown(f"**{i18n['remarks_label']}**")
                st.markdown(f"<div class='explain-area'>{remark}</div>", unsafe_allow_html=True)

        with btn_col:
            name = str(item.get("Name", item.get("name", ""))).strip()
            paper_link = get_paper_link_by_name(name)
            if paper_link:
                st.markdown(
                    f'<a href="{paper_link}" target="_blank" class="link-button">{i18n["view_btn"]}</a>',
                    unsafe_allow_html=True
                )
                if st.button(i18n["ai_explain_btn"], key=f"explain_{card_key}", use_container_width=True, type="secondary"):
                    st.session_state.pending_explain_link = paper_link
                    st.session_state.pending_explain_name = name
                    st.session_state.page = "paper"
                    st.rerun()
            else:
                st.info(i18n["no_paper_link"], icon="ℹ️")

            # 加入/移出对比按钮
            if name:
                compare_data = st.session_state.get("_compare_data", [])
                in_compare = name in compare_data

                if in_compare:
                    st.markdown("<div class='remove-btn'>", unsafe_allow_html=True)
                    if st.button(
                        i18n.get("compare_remove", "🗑️ 移出对比"),
                        key=f"remove_compare_{card_key}",
                        use_container_width=True,
                        type="secondary",
                    ):
                        new_list = [n for n in compare_data if n != name]
                        st.session_state["_compare_data"] = new_list
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
                            new_list = compare_data + [name]
                            st.session_state["_compare_data"] = new_list
                            st.toast(i18n.get("compare_add_ok", "已加入对比列表"), icon="✅")
                            st.rerun()
