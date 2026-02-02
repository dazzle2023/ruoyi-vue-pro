#!/usr/bin/env python3
"""
PDF to Markdown Converter
将 OneNET 城市物联网平台接口文档从 PDF 转换为 Markdown
"""

import sys
import re

try:
    import pdfplumber
except ImportError:
    print("正在安装 pdfplumber...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber"])
    import pdfplumber


def clean_text(text):
    """清理文本，移除多余空格和换行"""
    if not text:
        return ""
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def is_heading(text, font_size=None):
    """判断是否为标题"""
    if not text:
        return False

    # 基于文本模式判断
    heading_patterns = [
        r'^\d+\.\s+',  # 1. 标题
        r'^\d+\.\d+\s+',  # 1.1 标题
        r'^\d+\.\d+\.\d+\s+',  # 1.1.1 标题
        r'^第[一二三四五六七八九十]+章',  # 第一章
        r'^[一二三四五六七八九十]+、',  # 一、标题
    ]

    for pattern in heading_patterns:
        if re.match(pattern, text):
            return True

    return False


def get_heading_level(text):
    """获取标题级别"""
    if re.match(r'^\d+\.\s+', text):
        return 1
    elif re.match(r'^\d+\.\d+\s+', text):
        return 2
    elif re.match(r'^\d+\.\d+\.\d+\s+', text):
        return 3
    elif re.match(r'^第[一二三四五六七八九十]+章', text):
        return 1
    elif re.match(r'^[一二三四五六七八九十]+、', text):
        return 2
    return 2


def convert_pdf_to_markdown(pdf_path, output_path):
    """将 PDF 转换为 Markdown"""

    print(f"正在读取 PDF 文件: {pdf_path}")

    markdown_lines = []
    markdown_lines.append("# OneNET 城市物联网平台 V3.0 公开接口文档\n")
    markdown_lines.append("> 本文档由 PDF 自动转换生成\n")
    markdown_lines.append("---\n")

    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"总页数: {total_pages}")

            for page_num, page in enumerate(pdf.pages, 1):
                print(f"处理第 {page_num}/{total_pages} 页...")

                # 提取文本
                text = page.extract_text()

                if not text:
                    continue

                # 按行分割
                lines = text.split('\n')

                for line in lines:
                    line = clean_text(line)

                    if not line:
                        continue

                    # 跳过页码
                    if re.match(r'^\d+$', line) and len(line) <= 3:
                        continue

                    # 判断是否为标题
                    if is_heading(line):
                        level = get_heading_level(line)
                        markdown_lines.append(f"\n{'#' * (level + 1)} {line}\n")
                    else:
                        # 普通文本
                        markdown_lines.append(f"{line}\n")

                # 每页之间添加分隔
                if page_num < total_pages:
                    markdown_lines.append("\n")

        # 写入 Markdown 文件
        print(f"\n正在写入 Markdown 文件: {output_path}")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(markdown_lines)

        print(f"✓ 转换完成！")
        print(f"输出文件: {output_path}")

    except Exception as e:
        print(f"✗ 转换失败: {str(e)}")
        raise


if __name__ == "__main__":
    pdf_file = "./对接/副本11-OneNET城市物联网平台V3.0公开接口文档.pdf"
    output_file = "./requirements/OneNET城市物联网平台V3.0公开接口文档.md"

    convert_pdf_to_markdown(pdf_file, output_file)
