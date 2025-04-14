#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Common Utilities - Các hàm tiện ích chung
"""

import os
import sys
import subprocess
import platform


def clear_screen():
    """Xóa màn hình console"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def print_header(title):
    """In tiêu đề với định dạng đẹp"""
    width = 60
    print("=" * width)
    print(title.center(width))
    print("=" * width)


def check_dependencies():
    """Kiểm tra và cài đặt các thư viện phụ thuộc"""
    required_packages = [
        "requests",
        "beautifulsoup4",
        "pandas",
        "openpyxl",
        "matplotlib",
        "numpy",
        "scikit-learn",
        "nltk",
        "wordcloud",
        "pyLDAvis",
        "networkx",
        "textblob"
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("Đang cài đặt các thư viện cần thiết...")

        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"Đã cài đặt {package}")
            except subprocess.CalledProcessError:
                print(f"Không thể cài đặt {package}")
                return False

        # Tải dữ liệu NLTK
        try:
            import nltk
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')
            print("Đã tải dữ liệu NLTK")
        except:
            print("Không thể tải dữ liệu NLTK")
            return False

    return True