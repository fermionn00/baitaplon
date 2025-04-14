#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main Menu - Menu chính của ứng dụng
"""

import sys
from utils.common import clear_screen, print_header
from menus.scraping_menu import show_scraping_menu
from menus.excel_menu import show_excel_menu
from menus.analysis_menu import show_analysis_menu


def show_main_menu():
    """Hiển thị menu chính"""
    while True:
        clear_screen()
        print_header("WEB SCRAPING APP")
        print("\n1. Scraping dữ liệu web")
        print("2. Xử lý file Excel")
        print("3. Phân tích dữ liệu")
        print("0. Thoát")

        choice = input("\nNhập lựa chọn của bạn: ")

        if choice == '0':
            print("\nCảm ơn bạn đã sử dụng ứng dụng!")
            sys.exit(0)

        elif choice == '1':
            show_scraping_menu()

        elif choice == '2':
            show_excel_menu()

        elif choice == '3':
            show_analysis_menu()

        else:
            print("\nLựa chọn không hợp lệ. Vui lòng thử lại.")
            input("\nNhấn Enter để tiếp tục...")