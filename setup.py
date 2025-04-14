#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup - Cài đặt các thư viện cần thiết
"""

import subprocess
import sys


def install_requirements():
    """Cài đặt các thư viện cần thiết"""
    print("Đang cài đặt các thư viện cần thiết...")

    # Danh sách các thư viện cần thiết
    requirements = [
        "beautifulsoup4",  # Thư viện scraping HTML
        "requests",  # Thư viện HTTP requests
        "pandas",  # Xử lý dữ liệu và Excel
        "openpyxl",  # Hỗ trợ xử lý Excel
        "matplotlib",  # Vẽ biểu đồ
        "lxml",  # Parser HTML/XML
        "nltk",  # Xử lý ngôn ngữ tự nhiên
        "wordcloud",  # Tạo word cloud
        "scikit-learn",  # Học máy
        "seaborn",  # Vẽ biểu đồ nâng cao
        "gensim",  # Topic modeling
        "pyLDAvis",  # Trực quan hóa LDA
        "networkx",  # Phân tích mạng lưới
        "pillow",  # Xử lý hình ảnh
    ]

    # Cài đặt từng thư viện
    for package in requirements:
        print(f"Đang cài đặt {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    print("Đã cài đặt xong tất cả thư viện!")


if __name__ == "__main__":
    install_requirements()
    print("\nHướng dẫn sử dụng:")
    print("1. Chạy file main.py để khởi động ứng dụng")
    print("2. Làm theo hướng dẫn trên màn hình để scrape dữ liệu và xử lý file Excel")