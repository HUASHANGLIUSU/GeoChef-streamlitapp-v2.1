import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def _chart_colors():
    dark = st.session_state.get("theme_mode", "dark") == "dark"
    return {
        "font_color": "#f9fafb" if dark else "#1e293b",
        "grid_color": "rgba(255,255,255,0.1)" if dark else "rgba(0,0,0,0.08)",
    }


def render_stats(i18n: dict, lang: str, chef):
    with st.expander(i18n.get("stats_expand", "📊 展开 / 收起图表"), expanded=False):
        stats = chef.get_stats()
        c = _chart_colors()

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown(f"**{i18n['stats_by_year']}**")
            year_data = stats["year"]
            if year_data:
                fig = go.Figure(go.Bar(
                    x=list(year_data.keys()),
                    y=list(year_data.values()),
                    marker_color="#2563eb",
                    hovertemplate="%{x}: %{y} datasets<extra></extra>"
                ))
                fig.update_layout(
                    margin=dict(l=0, r=0, t=10, b=0), height=260,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(size=12, color=c["font_color"]),
                    xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(color=c["font_color"])),
                    yaxis=dict(showgrid=True, gridcolor=c["grid_color"], tickfont=dict(color=c["font_color"])),
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with col2:
            st.markdown(f"**{i18n['stats_by_task']}**")
            task_data = stats["task"]
            if task_data:
                fig = px.pie(
                    names=list(task_data.keys()), values=list(task_data.values()),
                    color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4,
                )
                fig.update_traces(textposition="inside", textinfo="percent+label",
                                  textfont=dict(color=c["font_color"]))
                fig.update_layout(
                    margin=dict(l=0, r=0, t=10, b=0), height=260,
                    paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                    font=dict(size=12, color=c["font_color"]),
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        col3, col4 = st.columns(2, gap="large")

        with col3:
            st.markdown(f"**{i18n['stats_by_modal']}**")
            modal_data = stats["modal"]
            if modal_data:
                sorted_modal = dict(sorted(modal_data.items(), key=lambda x: x[1], reverse=True))
                fig = go.Figure(go.Bar(
                    x=list(sorted_modal.values()), y=list(sorted_modal.keys()),
                    orientation="h", marker_color="#10b981",
                    hovertemplate="%{y}: %{x} datasets<extra></extra>"
                ))
                fig.update_layout(
                    margin=dict(l=0, r=0, t=10, b=0), height=220,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(size=12, color=c["font_color"]),
                    xaxis=dict(showgrid=True, gridcolor=c["grid_color"], tickfont=dict(color=c["font_color"])),
                    yaxis=dict(showgrid=False, tickfont=dict(color=c["font_color"])),
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with col4:
            st.markdown(f"**{i18n['stats_by_sheet']}**")
            sheet_data = {k: v for k, v in stats["sheet"].items()
                          if k not in ["统计期刊数量、国家数量、年份"]}
            if sheet_data:
                fig = px.pie(
                    names=list(sheet_data.keys()), values=list(sheet_data.values()),
                    color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.4,
                )
                fig.update_traces(textposition="inside", textinfo="percent+label",
                                  textfont=dict(color=c["font_color"]))
                fig.update_layout(
                    margin=dict(l=0, r=0, t=10, b=0), height=220,
                    paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                    font=dict(size=12, color=c["font_color"]),
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
