import re

README_LOCAL_PATH = "README.md"
name_to_paper = {}


def load_github_paper_links():
    global name_to_paper
    name_to_paper.clear()

    try:
        with open(README_LOCAL_PATH, "r", encoding="utf-8") as f:
            md_text = f.read()

        pattern = r'\[(.*?)\]\((https?://.*?)\)'
        matches = re.findall(pattern, md_text, re.DOTALL | re.IGNORECASE)

        valid_count = 0
        for name, link in matches:
            clean_name = name.strip().lower()
            clean_link = link.strip()
            if len(clean_name) >= 2 and any(
                    key in clean_link for key in ["arxiv", "sciencedirect", "ieee", "mdpi", "github", "cvf"]):
                name_to_paper[clean_name] = clean_link
                valid_count += 1

        print(f"解析完成 | 匹配 {len(matches)} 条 | 有效学术链接 {valid_count} 个")

    except FileNotFoundError:
        print(f"未找到文件：{README_LOCAL_PATH}")
        name_to_paper = {}
    except Exception as e:
        print(f"解析失败：{str(e)}")
        name_to_paper = {}


def get_paper_link_by_name(name):
    if not name:
        return None
    target_name = name.strip().lower()
    for key in name_to_paper:
        if target_name in key or key in target_name:
            return name_to_paper[key]
    return None


if __name__ == "__main__":
    load_github_paper_links()
    test_list = ["osvqa", "geochat", "geoplan-bench", "SkyEyeGPT"]
    for test_name in test_list:
        link = get_paper_link_by_name(test_name)
        print(f"   {test_name} → {link if link else '未匹配到'}")
