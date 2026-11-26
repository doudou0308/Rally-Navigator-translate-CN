"""Rally Navigator 翻译核心模块

负责读取英文 JSON 翻译文件，应用中文字典进行翻译，输出结果。
"""

import os
import json
from src.trans_map import trans_map


def translate_json(input_path, output_dir):
    """将英文翻译 JSON 文件汉化并输出。

    Args:
        input_path: 英文 translation.json 路径
        output_dir: 输出目录路径

    Returns:
        dict: {
            "total": 总条目数,
            "translated": 已翻译数,
            "kept": 保留原文数,
            "untranslated": 未翻译条目列表,
            "output": 输出文件路径
        }
    """
    # 读取输入
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("翻译文件顶层必须是数组")

    # 执行翻译
    output = []
    untranslated = []

    translated_count = 0
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict) or "id" not in item or not isinstance(item.get("content"), str):
            raise ValueError(f"第 {index} 条记录必须包含 id 和字符串 content")
        content = item["content"]
        if content in trans_map:
            translated = trans_map[content]
        else:
            translated = content  # 保留原文
            untranslated.append(item)

        if translated != content:
            translated_count += 1

        output.append({
            "id": item["id"],
            "content": translated
        })

    # 写入输出
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "translation.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return {
        "total": len(data),
        "translated": translated_count,
        "kept": len(data) - translated_count,
        "untranslated": untranslated,
        "output": output_path,
    }

