#!/usr/bin/env python3
"""Rally Navigator 中文汉化工具

用法:
  python translate.py <en_json路径> [输出目录]

示例:
  python translate.py "e:\Rally Navigator\resources\locales\en\translation.json"
  python translate.py "en.json" "output"
"""

import sys
import os
import json
import argparse
from src.translator import translate_json


def main():
    parser = argparse.ArgumentParser(
        description="Rally Navigator 中文汉化工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python translate.py "e:\\Rally Navigator\\resources\\locales\\en\\translation.json"
  python translate.py input.json -o my_translation
        """
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=r"e:\Rally Navigator\resources\locales\en\translation.json",
        help="英文翻译文件路径 (default: Rally Navigator en/translation.json)"
    )
    parser.add_argument(
        "-o", "--output",
        default=r"resources\locales\zh-Hans-CN",
        help="输出目录 (default: resources/locales/zh-Hans-CN)"
    )
    parser.add_argument(
        "-s", "--stats",
        action="store_true",
        default=True,
        help="显示翻译统计信息"
    )

    args = parser.parse_args()

    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"[错误] 找不到输入文件: {args.input}")
        sys.exit(1)

    # 执行翻译
    result = translate_json(args.input, args.output)

    # 输出统计
    if args.stats:
        total = result["total"]
        translated = result["translated"]
        kept = result["kept"]
        print(f"\n{'='*40}")
        print(f"  汉化完成！")
        print(f"{'='*40}")
        print(f"  总条目数:     {total}")
        print(f"  已翻译:       {translated:>4} ({translated*100//total}%)")
        print(f"  保留原文:     {kept:>4} ({kept*100//total}%)")
        print(f"  输出文件:     {result['output']}")
        print(f"{'='*40}")

        if kept > 0 and result.get("untranslated"):
            print(f"\n  未翻译条目 (前20条):")
            for item in result["untranslated"][:20]:
                print(f"    - {item['id']}")
            if len(result["untranslated"]) > 20:
                print(f"    ... 还有 {len(result['untranslated'])-20} 条")

    print("\n✅ 完成！")


if __name__ == "__main__":
    main()
