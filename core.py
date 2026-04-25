import pandas as pd
import random
import json
import re
import streamlit as st


@st.cache_resource
def load_chef(path="rs_vlm_datasets.xlsx") -> "GeoChef":
    chef = GeoChef()
    chef.load(path)
    return chef


MODAL_KEYWORDS = {
    "SAR": {"sar", "sentinel-1", "sentinel1", "雷达"},
    "Optical (RGB)": {"rgb", "optical", "光学", "可见光"},
    "Multispectral": {"msi", "sentinel-2", "sentinel2", "landsat", "多光谱"},
    "Hyperspectral": {"hsi", "高光谱"},
    "LiDAR": {"lidar", "激光雷达"},
}

TASK_LIST = ["VQA", "Caption", "VG", "Classification", "Detection", "Segmentation"]


class GeoChef:
    def __init__(self):
        self.data = []
        self.years = []
        self.publishers = []
        self.methods = []
        self.modalities = list(MODAL_KEYWORDS.keys())
        self.tasks = TASK_LIST

    def load(self, path="rs_vlm_datasets.xlsx"):
        sheets = ["VQA", "Cap", "Caption", "VG", "Comprehensive Data", "Comprehensive benchmark",
                  "统计期刊数量、国家数量、年份"]
        leakage_sheets = ["VQA", "Cap", "VG", "Comprehensive Data", "Comprehensive benchmark"]
        items = []
        publishers = set()
        methods = set()
        years = set()

        self._name_to_sources: dict[str, list[str]] = {}
        self._source_to_names: dict[str, list[str]] = {}
        self._all_sources: list[str] = []
        _source_display: dict[str, str] = {}

        for sheet in sheets:
            try:
                df = pd.read_excel(path, sheet_name=sheet)
                for _, row in df.iterrows():
                    item = row.dropna().to_dict()
                    item["_sheet"] = sheet
                    item["_text"] = json.dumps(item, ensure_ascii=False).lower()
                    item["_years"] = set(re.findall(r'\b(199\d|20[0-2]\d)\b', item["_text"]))
                    items.append(item)

                    p = str(item.get("Publisher", item.get("publisher", ""))).strip()
                    if p and len(p) > 1:
                        publishers.add(p)

                    m = str(item.get("Method", item.get("method", ""))).strip()
                    if m and len(m) > 1:
                        methods.add(m)

                    years.update(item["_years"])

                    if sheet in leakage_sheets:
                        name = str(item.get("Name", item.get("name", ""))).strip()
                        raw_sources = str(item.get("包含数据集", "")).strip()
                        if name and raw_sources and raw_sources.lower() != "nan":
                            parts = re.split(r'[,，、;；\n]+', raw_sources)
                            sources = [p.strip() for p in parts if p.strip() and len(p.strip()) >= 2]
                            if sources:
                                self._name_to_sources[name] = sources
                                for src in sources:
                                    src_lower = src.lower()
                                    _source_display.setdefault(src_lower, src)
                                    self._source_to_names.setdefault(src_lower, [])
                                    if name not in self._source_to_names[src_lower]:
                                        self._source_to_names[src_lower].append(name)
            except Exception as e:
                print(f"[GeoChef] 加载 sheet '{sheet}' 失败: {e}")
                continue

        self.data = items
        self.years = sorted(list(years))
        self.publishers = sorted(list(publishers))
        self.methods = sorted(list(methods))
        self._all_sources = sorted(_source_display.values(), key=lambda x: x.lower())
        self._name_to_item: dict[str, dict] = {}
        for item in self.data:
            name = str(item.get("Name", item.get("name", ""))).strip()
            if name and name not in self._name_to_item:
                self._name_to_item[name] = item
        self._stats_cache = self._compute_stats()
        self._all_dataset_names = self._compute_dataset_names()

    def get_all_sources(self) -> list[str]:
        return self._all_sources

    def query_by_multiple_sources(self, source_names: list[str]) -> dict[str, list[dict]]:
        per_source: dict[str, list[dict]] = {}
        for src in source_names:
            per_source[src] = self.query_by_source(src)

        if len(source_names) > 1:
            name_sets = [set(e["name"] for e in entries) for entries in per_source.values()]
            common_names = name_sets[0].intersection(*name_sets[1:])
        else:
            common_names = set()

        return {"per_source": per_source, "common_names": common_names}

    def query_by_source(self, source_name: str) -> list[dict]:
        src_lower = source_name.strip().lower()
        matched_key = None
        for key in self._source_to_names:
            if src_lower in key or key in src_lower:
                matched_key = key
                break
        if not matched_key:
            return []

        results = []
        for name in self._source_to_names[matched_key]:
            sources = self._name_to_sources.get(name, [])
            item = self._name_to_item.get(name)
            if item is None:
                continue
            remark = str(item.get("数据集备注", "")).strip()
            if remark.lower() == "nan":
                remark = ""
            results.append({"name": name, "sources": sources, "remark": remark, "item": item})
        return results

    def check_modal(self, item_words, modals):
        if not modals: return True
        for m in modals:
            if MODAL_KEYWORDS[m] & item_words: return True
        return False

    def check_task(self, text, tasks):
        if not tasks: return True
        return any(t.lower() in text for t in tasks)

    def check_year(self, item_years, years):
        if not years: return True
        return bool(set(years) & item_years)

    def check_publisher(self, item, selected):
        if not selected: return True
        return str(item.get("Publisher", item.get("publisher", ""))).strip() in selected

    def check_method(self, item, selected):
        if not selected: return True
        return str(item.get("Method", item.get("method", ""))).strip() in selected

    def check_keywords(self, text, kws):
        if not kws: return True
        return all(kw.lower() in text for kw in kws)

    def filter(self, modals, tasks, years, publishers, methods, kws):
        res = []
        for item in self.data:
            item_words = set(re.findall(r"\w+", item["_text"]))
            if (self.check_modal(item_words, modals) and
                    self.check_task(item["_text"], tasks) and
                    self.check_year(item["_years"], years) and
                    self.check_publisher(item, publishers) and
                    self.check_method(item, methods) and
                    self.check_keywords(item["_text"], kws)):
                res.append(item)
        return res

    def get_stats(self) -> dict:
        return self._stats_cache

    def _compute_stats(self) -> dict:
        from collections import Counter
        year_counter = Counter()
        modal_counter = Counter()
        task_counter = Counter()
        sheet_counter = Counter()

        for item in self.data:
            years = item.get("_years", set())
            if years:
                year_counter[min(years)] += 1
            sheet = item.get("_sheet", "")
            if sheet:
                sheet_counter[sheet] += 1
            text = item.get("_text", "")
            words = set(re.findall(r"\w+", text))
            for modal, kws in MODAL_KEYWORDS.items():
                if kws & words:
                    modal_counter[modal] += 1
            for task in TASK_LIST:
                if task.lower() in text:
                    task_counter[task] += 1

        return {
            "year": dict(sorted(year_counter.items())),
            "modal": dict(modal_counter),
            "task": dict(task_counter),
            "sheet": dict(sheet_counter),
        }

    def get_item_by_name(self, name: str) -> dict | None:
        item = self._name_to_item.get(name.strip())
        if item:
            return item
        target = name.strip().lower()
        for n, it in self._name_to_item.items():
            if target in n.lower() or n.lower() in target:
                return it
        return None

    def get_all_dataset_names(self) -> list[str]:
        return self._all_dataset_names

    def _compute_dataset_names(self) -> list[str]:
        names, seen = [], set()
        for item in self.data:
            name = str(item.get("Name", item.get("name", ""))).strip()
            if name and name not in seen:
                names.append(name)
                seen.add(name)
        return sorted(names)

    def random_one(self):
        return random.choice(self.data) if self.data else None
