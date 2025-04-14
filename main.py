#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Web Scraping App - Ứng dụng thu thập dữ liệu từ web
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Import các module menu
from menus.main_menu import show_main_menu
from utils.common import clear_screen, print_header, check_dependencies


def main():
    """Hàm chính của ứng dụng"""
    # Kiểm tra và cài đặt các thư viện phụ thuộc
    if not check_dependencies():
        print("Không thể cài đặt các thư viện cần thiết. Vui lòng cài đặt thủ công.")
        sys.exit(1)

    # Tạo thư mục data nếu chưa tồn tại
    if not os.path.exists('data'):
        os.makedirs('data')

    # Tạo thư mục exports nếu chưa tồn tại
    if not os.path.exists('exports'):
        os.makedirs('exports')

    # Tạo thư mục images nếu chưa tồn tại
    if not os.path.exists('images'):
        os.makedirs('images')

    # Hiển thị menu chính
    show_main_menu()


if __name__ == "__main__":
    main()