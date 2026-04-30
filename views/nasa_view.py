import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import re


NASA_RSS_URL = "https://earthobservatory.nasa.gov/feeds/image-of-the-day.rss"

# RSS 命名空间
NS = {
    "media": "http://search.yahoo.com/mrss/",
    "dc":    "http://purl.org/dc/elements/1.1/",
}


def _extract_image_from_html(html: str) -> str | None:
    """
    从 content:encoded 的 HTML 中提取第一张主图 URL。
    优先取带 fetchpriority="high" 的图（通常是主图），否则取第一个 img src。
    URL 中的 &amp; 会被反转义，并裁剪为合适尺寸（w=1200）。
    """
    # 优先：fetchpriority="high" 的图
    m = re.search(r'fetchpriority=["\']high["\'][^>]*src=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if not m:
        m = re.search(r'src=["\']([^"\']+)["\'][^>]*fetchpriority=["\']high["\']', html, re.IGNORECASE)
    # 备用：第一个 assets.science.nasa.gov 图片
    if not m:
        m = re.search(r'src=["\'](https://assets\.science\.nasa\.gov[^"\']+)["\']', html, re.IGNORECASE)
    # 再备用：任意 https img src
    if not m:
        m = re.search(r'src=["\'](https://[^"\']+\.(?:jpg|jpeg|png|webp)[^"\']*)["\']', html, re.IGNORECASE)

    if not m:
        return None

    url = m.group(1)
    # 反转义 HTML 实体
    url = url.replace("&amp;", "&").replace("&#038;", "&")
    # 把超大尺寸替换为 1200px 宽，减少加载时间
    url = re.sub(r"[?&]w=\d+", lambda mo: mo.group(0).replace(mo.group(0).split("=")[1], "1200"), url, count=1)
    # 去掉 h= 参数，让服务端按比例缩放
    url = re.sub(r"&h=\d+", "", url)
    return url


def _parse_rss(xml_text: str) -> list[dict]:
    """解析 RSS XML，返回条目列表，每条包含 title/date/link/image/description。"""
    root = ET.fromstring(xml_text)
    channel = root.find("channel")
    if channel is None:
        return []

    # content 命名空间
    CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"

    items = []
    for item in channel.findall("item"):
        title = (item.findtext("title") or "").strip()
        link  = (item.findtext("link")  or "").strip()
        desc  = (item.findtext("description") or "").strip()
        pub_date_str = (item.findtext("pubDate") or "").strip()

        # 解析日期
        pub_date = None
        if pub_date_str:
            try:
                pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                try:
                    pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S GMT")
                except ValueError:
                    pass

        # 优先从 content:encoded 提取图片（包含完整 HTML）
        image_url = None
        content_encoded = item.find(f"{{{CONTENT_NS}}}encoded")
        if content_encoded is not None and content_encoded.text:
            image_url = _extract_image_from_html(content_encoded.text)

        # 备用：media:content / media:thumbnail
        if not image_url:
            media_content = item.find("media:content", NS)
            if media_content is not None:
                image_url = media_content.get("url")
        if not image_url:
            media_thumb = item.find("media:thumbnail", NS)
            if media_thumb is not None:
                image_url = media_thumb.get("url")

        # 再备用：description 里的 img
        if not image_url and desc:
            m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', desc, re.IGNORECASE)
            if m:
                image_url = m.group(1).replace("&amp;", "&")

        # 清理 description 中的 HTML 标签，保留纯文本摘要
        clean_desc = re.sub(r"<[^>]+>", "", desc).strip()
        # 去掉末尾的 "The post ... appeared first on NASA Science." 样板文字
        clean_desc = re.sub(r"\s*The post .+appeared first on .+\.$", "", clean_desc).strip()

        items.append({
            "title":       title,
            "link":        link,
            "description": clean_desc,
            "date":        pub_date,
            "image_url":   image_url,
        })

    return items


@st.cache_data(ttl=3600)  # 缓存 1 小时，避免频繁请求
def _fetch_nasa_items() -> tuple[list[dict], str | None]:
    """
    拉取 NASA Earth Observatory RSS，返回 (items, error_msg)。
    items 按日期降序排列。
    """
    try:
        resp = requests.get(NASA_RSS_URL, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (compatible; GeoChef/1.0)"
        })
        resp.raise_for_status()
        items = _parse_rss(resp.text)
        # 按日期降序
        items.sort(key=lambda x: x["date"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
        return items, None
    except requests.exceptions.Timeout:
        return [], "请求超时，请稍后刷新重试。"
    except requests.exceptions.RequestException as e:
        return [], f"网络请求失败：{e}"
    except ET.ParseError as e:
        return [], f"RSS 解析失败：{e}"


def _pick_best_item(items: list[dict]) -> dict | None:
    """
    优先返回当天的条目；若当天没有，则返回最新一条（通常是昨天）。
    NASA 的 RSS 时区为 UTC，这里用 UTC 日期比较。
    """
    if not items:
        return None
    today_utc = datetime.now(timezone.utc).date()
    for item in items:
        if item["date"] and item["date"].date() == today_utc:
            return item
    # 没有今天的，返回最新一条
    return items[0]


def render_nasa(i18n: dict, lang: str):
    is_cn = lang == "cn"

    # 刷新按钮
    col_title, col_refresh = st.columns([5, 1])
    with col_refresh:
        if st.button(
            "🔄 " + ("刷新" if is_cn else "Refresh"),
            key="nasa_refresh_btn",
            use_container_width=True,
            type="secondary",
        ):
            _fetch_nasa_items.clear()
            st.rerun()

    with st.spinner("正在加载 NASA 每日一图..." if is_cn else "Loading NASA Image of the Day..."):
        items, error = _fetch_nasa_items()

    if error:
        st.error(("加载失败：" if is_cn else "Failed to load: ") + error)
        return

    if not items:
        st.warning("暂无数据" if is_cn else "No data available")
        return

    best = _pick_best_item(items)
    if not best:
        st.warning("暂无数据" if is_cn else "No data available")
        return

    # ── 主图展示 ──────────────────────────────────────────
    today_utc = datetime.now(timezone.utc).date()
    item_date = best["date"].date() if best["date"] else None
    is_today = item_date == today_utc

    date_str = best["date"].strftime("%Y-%m-%d") if best["date"] else "—"
    freshness_badge = (
        ("📅 今日更新" if is_cn else "📅 Today's Image")
        if is_today else
        ("📅 最新（" + date_str + "）" if is_cn else "📅 Latest (" + date_str + ")")
    )

    st.markdown(f"### {best['title']}")
    st.caption(freshness_badge)

    if best["image_url"]:
        st.image(best["image_url"], use_container_width=True)
    else:
        st.info(
            "图片暂时无法加载，请点击下方链接查看原文。"
            if is_cn else
            "Image unavailable. Please visit the original link below."
        )

    if best["description"]:
        st.markdown(best["description"])

    # 来源标注
    source_label = "来源" if is_cn else "Source"
    st.markdown(
        f'<p style="font-size:0.8rem;opacity:0.65;margin-top:0.5rem">'
        f'📡 {source_label}: '
        f'<a href="{best["link"]}" target="_blank">NASA Earth Observatory — Image of the Day</a>'
        f'</p>',
        unsafe_allow_html=True,
    )

    st.divider()

    # ── 近期图片列表 ──────────────────────────────────────
    recent_label = "近期图片" if is_cn else "Recent Images"
    with st.expander(f"🗂️ {recent_label}", expanded=False):
        recent = [it for it in items if it is not best][:9]  # 最多展示 9 条
        if not recent:
            st.caption("暂无更多" if is_cn else "No more items")
        else:
            cols = st.columns(3, gap="medium")
            for i, item in enumerate(recent):
                with cols[i % 3]:
                    if item["image_url"]:
                        st.image(item["image_url"], use_container_width=True)
                    d = item["date"].strftime("%m-%d") if item["date"] else ""
                    st.markdown(
                        f'<p style="font-size:0.8rem;margin:4px 0 2px 0"><strong>{item["title"]}</strong></p>'
                        f'<p style="font-size:0.75rem;opacity:0.6">{d}</p>'
                        f'<a href="{item["link"]}" target="_blank" style="font-size:0.75rem">'
                        f'{"查看原文" if is_cn else "View"} →</a>',
                        unsafe_allow_html=True,
                    )
                    st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)

    # ── 侧边栏内嵌小卡片（供侧边栏底部展示缩略图） ──────────
    # 通过 session_state 传递给 sidebar 渲染
    st.session_state["_nasa_thumb"] = {
        "title":     best["title"],
        "image_url": best["image_url"],
        "link":      best["link"],
        "date_str":  date_str,
        "is_today":  is_today,
    }
