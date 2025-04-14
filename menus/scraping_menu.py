#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Scraping Menu - Menu scraping dữ liệu
"""

import os
import pandas as pd
from datetime import datetime
from utils.common import clear_screen, print_header
from scrapers.exchange_rate_scraper import ExchangeRateScraper
from scrapers.gold_price_scraper import GoldPriceScraper
from scrapers.custom_scraper import CustomScraper
from scrapers.dantri_scraper import DantriScraper
from menus.dantri_menu import show_dantri_advanced_menu


def show_scraping_menu():
    """Hiển thị menu scraping dữ liệu"""
    while True:
        clear_screen()
        print_header("SCRAPING DỮ LIỆU WEB")
        print("\n1. Lấy dữ liệu tỷ giá")
        print("2. Lấy dữ liệu giá vàng")
        print("3. Lấy dữ liệu từ URL tùy chỉnh")
        print("4. Lấy dữ liệu từ Dân Trí")
        print("5. Lấy dữ liệu từ Dân Trí (Nâng cao)")
        print("0. Quay lại")

        choice = input("\nNhập lựa chọn của bạn: ")

        if choice == '0':
            break

        elif choice == '1':
            # Lấy dữ liệu tỷ giá
            scraper = ExchangeRateScraper()

            print("\nĐang lấy dữ liệu tỷ giá...")
            data = scraper.scrape()

            if data:
                # Chuyển đổi thành DataFrame
                df = pd.DataFrame(data)

                # Lưu dữ liệu
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"data/exchange_rate_{timestamp}.xlsx"
                df.to_excel(filename, index=False)

                print(f"\nĐã lưu dữ liệu vào file {filename}")
                print("\nDữ liệu tỷ giá:")
                print(df)
            else:
                print("\nKhông lấy được dữ liệu tỷ giá.")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '2':
            # Lấy dữ liệu giá vàng
            scraper = GoldPriceScraper()

            print("\nĐang lấy dữ liệu giá vàng...")
            data = scraper.scrape()

            if data:
                # Chuyển đổi thành DataFrame
                df = pd.DataFrame(data)

                # Lưu dữ liệu
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"data/gold_price_{timestamp}.xlsx"
                df.to_excel(filename, index=False)

                print(f"\nĐã lưu dữ liệu vào file {filename}")
                print("\nDữ liệu giá vàng:")
                print(df)
            else:
                print("\nKhông lấy được dữ liệu giá vàng.")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '3':
            # Lấy dữ liệu từ URL tùy chỉnh
            url = input("\nNhập URL: ")

            if not url:
                print("\nURL không hợp lệ.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            # Chọn phương thức scraping
            print("\nChọn phương thức scraping:")
            print("1. Lấy tất cả bảng (table)")
            print("2. Lấy theo CSS selector")

            method_choice = input("\nNhập lựa chọn của bạn: ")

            if method_choice == '1':
                # Lấy tất cả bảng
                scraper = CustomScraper(url)

                print(f"\nĐang lấy dữ liệu từ {url}...")
                tables = scraper.scrape_tables()

                if tables:
                    print(f"\nĐã tìm thấy {len(tables)} bảng.")

                    # Lưu dữ liệu
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    for i, df in enumerate(tables):
                        filename = f"data/table_{i + 1}_{timestamp}.xlsx"
                        df.to_excel(filename, index=False)
                        print(f"\nĐã lưu bảng {i + 1} vào file {filename}")
                        print(f"\nDữ liệu bảng {i + 1}:")
                        print(df.head())
                else:
                    print("\nKhông tìm thấy bảng nào.")

            elif method_choice == '2':
                # Lấy theo CSS selector
                css_selector = input("\nNhập CSS selector: ")

                if not css_selector:
                    print("\nCSS selector không hợp lệ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                scraper = CustomScraper(url)

                print(f"\nĐang lấy dữ liệu từ {url} với selector {css_selector}...")
                data = scraper.scrape_by_css(css_selector)

                if data:
                    print(f"\nĐã tìm thấy {len(data)} phần tử.")

                    # Lưu dữ liệu
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"data/custom_{timestamp}.txt"

                    with open(filename, 'w', encoding='utf-8') as f:
                        for i, item in enumerate(data):
                            f.write(f"Item {i + 1}:\n{item}\n\n")

                    print(f"\nĐã lưu dữ liệu vào file {filename}")

                    # Hiển thị một số phần tử đầu tiên
                    print("\nDữ liệu:")
                    for i, item in enumerate(data[:5]):
                        print(f"Item {i + 1}: {item[:100]}...")

                    if len(data) > 5:
                        print(f"... và {len(data) - 5} phần tử khác.")
                else:
                    print("\nKhông tìm thấy phần tử nào.")

            else:
                print("\nLựa chọn không hợp lệ.")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '4':
            # Lấy dữ liệu từ Dân Trí
            scraper = DantriScraper()

            print("\nChọn chức năng:")
            print("1. Lấy tin mới nhất")
            print("2. Lấy tin từ chuyên mục")
            print("3. Tìm kiếm bài viết")

            function_choice = input("\nNhập lựa chọn của bạn: ")

            if function_choice == '1':
                # Lấy tin mới nhất
                limit = int(input("\nNhập số lượng bài viết cần lấy: ") or "10")

                print(f"\nĐang lấy {limit} tin mới nhất từ Dân Trí...")
                articles = scraper.get_latest_news(limit)

                if articles:
                    # Chuyển đổi thành DataFrame
                    df = pd.DataFrame(articles)

                    # Lưu dữ liệu
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"data/dantri_latest_{timestamp}.xlsx"
                    df.to_excel(filename, index=False)

                    print(f"\nĐã lưu dữ liệu vào file {filename}")
                    print(f"\nĐã lấy được {len(articles)} bài viết")

                    # Hiển thị thông tin
                    for i, article in enumerate(articles):
                        print(f"{i + 1}. {article['title']}")
                else:
                    print("\nKhông lấy được bài viết nào.")

            elif function_choice == '2':
                # Lấy tin từ chuyên mục
                print("\nĐang lấy danh sách chuyên mục...")
                categories = scraper.get_categories()

                if categories:
                    print("\nDanh sách chuyên mục:")
                    for i, category in enumerate(categories):
                        print(f"{i + 1}. {category['name']}")

                    cat_choice = int(input("\nChọn chuyên mục (nhập số): ")) - 1
                    if 0 <= cat_choice < len(categories):
                        limit = int(input("\nNhập số lượng bài viết cần lấy: ") or "10")

                        category = categories[cat_choice]
                        print(f"\nĐang lấy {limit} bài viết từ chuyên mục {category['name']}...")

                        articles = scraper.get_category_news(category['url'], limit)

                        if articles:
                            # Chuyển đổi thành DataFrame
                            df = pd.DataFrame(articles)

                            # Lưu dữ liệu
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"data/dantri_{category['name'].lower().replace(' ', '_')}_{timestamp}.xlsx"
                            df.to_excel(filename, index=False)

                            print(f"\nĐã lưu dữ liệu vào file {filename}")
                            print(f"\nĐã lấy được {len(articles)} bài viết")

                            # Hiển thị thông tin
                            for i, article in enumerate(articles):
                                print(f"{i + 1}. {article['title']}")
                        else:
                            print("\nKhông lấy được bài viết nào.")
                    else:
                        print("\nLựa chọn không hợp lệ.")
                else:
                    print("\nKhông lấy được danh sách chuyên mục.")

            elif function_choice == '3':
                # Tìm kiếm bài viết
                keyword = input("\nNhập từ khóa tìm kiếm: ")

                if keyword:
                    limit = int(input("\nNhập số lượng kết quả tối đa: ") or "10")

                    print(f"\nĐang tìm kiếm '{keyword}' trên Dân Trí...")
                    results = scraper.search(keyword, limit)

                    if results:
                        # Chuyển đổi thành DataFrame
                        df = pd.DataFrame(results)

                        # Lưu dữ liệu
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"data/dantri_search_{keyword.replace(' ', '_')}_{timestamp}.xlsx"
                        df.to_excel(filename, index=False)

                        print(f"\nĐã lưu dữ liệu vào file {filename}")
                        print(f"\nĐã tìm thấy {len(results)} kết quả")

                        # Hiển thị thông tin
                        for i, result in enumerate(results):
                            print(f"{i + 1}. {result['title']}")
                    else:
                        print(f"\nKhông tìm thấy kết quả nào cho từ khóa '{keyword}'.")
                else:
                    print("\nTừ khóa tìm kiếm không hợp lệ.")

            else:
                print("\nLựa chọn không hợp lệ.")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '5':
            # Lấy dữ liệu từ Dân Trí (Nâng cao)
            show_dantri_advanced_menu()

        else:
            print("\nLựa chọn không hợp lệ. Vui lòng thử lại.")
            input("\nNhấn Enter để tiếp tục...")