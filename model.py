import requests
import time
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

API_URL = "https://chat.ecnu.edu.cn/open/api/v1/chat/completions"
API_KEY = st.secrets["CHATECNU_API_KEY"]
MODEL_NAME = "ecnu-plus"


class ECNUModel:
    @staticmethod
    def _chat_with_messages(messages, temperature=0.2, retries=2):
        for attempt in range(retries + 1):
            try:
                data = {
                    "model": MODEL_NAME,
                    "messages": messages,
                    "temperature": temperature,
                    "thinking": {"type": "enabled"}
                }
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                resp = requests.post(API_URL, json=data, headers=headers, timeout=60)
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"].strip()
            except Exception as e:
                if attempt < retries:
                    time.sleep(1.5 * (attempt + 1))
                else:
                    print(f"大模型请求失败（已重试 {retries} 次）: {e}")
                    return "抱歉，暂时无法响应请求，请稍后再试。"

    @staticmethod
    def chat(prompt):
        return ECNUModel._chat_with_messages([{"role": "user", "content": prompt}])

    @staticmethod
    def multi_chat(messages):
        return ECNUModel._chat_with_messages(messages)

    @staticmethod
    def generate_response(user_input, chat_history):
        system_prompt = """
        你是GeoChef遥感数据集检索系统的智能助手，需遵循以下规则：
        1. 若用户需求是构建/创建/制作数据集（如SAR数据集、光学数据集）：直接给出专业的构建建议，不涉及检索操作。
        2. 若用户需求是查询/查找/搜索数据集（如找SAR数据集、查2023年的遥感数据集）：告知用户使用本系统的筛选栏（数据模态/任务类型/年份等）+ 检索功能来查找，给出具体操作建议。
        3. 若用户要求翻译（如"翻译这段文字""把xxx翻译成英文"）：执行专业遥感领域翻译，保留格式。
        4. 若用户要求自我介绍（如"你是谁""介绍一下你自己"）：介绍GeoChef系统和功能。
        5. 其他通用问题：友好回应，并引导用户使用数据集构建/检索/翻译功能。
        6. 所有回复需简洁专业，贴合遥感领域，中文回复优先（用户说英文则用英文）。

        ====================== 数据泄露专业知识模块 ======================
        一、什么是数据泄露（Data Leakage）
        数据泄露是指训练集、验证集、测试集之间出现数据重叠、样本共享、来源交叉，
        导致模型在测试集上表现虚高，无法泛化到真实场景，是机器学习中最严重的错误之一。

        二、数据泄露的风险
        1. 模型评估结果不可信，测试精度虚高
        2. 模型上线后实际效果大幅下降
        3. 论文/实验结果无法复现，失去学术价值
        4. 误导研究方向，浪费算力与时间
        5. 视觉语言模型中，原始数据集共享会直接造成严重泄露

        三、数据泄露的检测方法（GeoChef 内置规则）
        1. 检查训练集与测试集是否共享原始数据集
        2. 只要两个数据集存在任意一个共同原始数据源，即判定为风险
        3. 检查样本ID、图像路径、标注文件是否重叠
        4. 检查时间、区域、采集设备是否交叉
        5. 本系统已自动实现：输入训练集 → 自动识别所有风险测试集

        四、数据泄露的重要性
        1. 保证实验真实性，是学术研究的基础
        2. 保证模型泛化能力，是工程落地的关键
        3. 避免错误结论，提高研究效率
        4. 遥感/视觉语言数据集来源复杂，必须严格检测

        五、视觉语言数据集专用规则
        1. 训练集A 包含 原始数据集X
        2. 测试集B 也包含 原始数据集X
        3. 则 A→B 测试存在数据泄露风险
        4. 本系统可一键检测所有风险数据集
        ============================================================
        """
        messages = [{"role": "system", "content": system_prompt}] + chat_history + [
            {"role": "user", "content": user_input}]
        return ECNUModel._chat_with_messages(messages)

    @staticmethod
    def translate_line(text):
        try:
            prompt = f"专业翻译为英文，保留所有markdown格式，不要解释，只输出翻译结果：{text}"
            return ECNUModel.chat(prompt)
        except:
            return text

    @staticmethod
    def translate_item_fields(fields: list[tuple]) -> list[str]:
        if not fields:
            return []
        lines = "\n".join(f"- **{k}**: {v}" for k, v in fields)
        try:
            prompt = f"专业翻译为英文，保留所有markdown格式（**加粗**、- 列表），不要解释，只输出翻译结果：\n{lines}"
            result = ECNUModel.chat(prompt)
            return result.split("\n")
        except:
            return [f"- **{k}**: {v}" for k, v in fields]
