#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dantri Menu - Menu scraping Dân Trí nâng cao
"""

import os
import pandas as pd
from datetime import datetime
from utils.common import clear_screen, print_header
from scrapers.dantri_scraper_advanced import DantriScraperAdvanced


def show_dantri_advanced_menu():
    """Hiển thị menu scraping Dân Trí nâng cao"""
    while True:
        clear_screen()
        print_header("SCRAPING DỮ LIỆU TỪ DÂN TRÍ (NÂNG CAO)")
        print("\n1. Lấy tin mới nhất (đa luồng)")
        print("2. Lấy tin từ chuyên mục (với phân trang)")
        print("3. Tìm kiếm nâng cao")
        print("4. Lấy tin theo khoảng thời gian")
        print("5. Phân tích chủ đề xu hướng")
        print("6. Lên lịch scraping tự động")
        print("7. Xuất dữ liệu ra nhiều định dạng")
        print("0. Quay lại")

        choice = input("\nNhập lựa chọn của bạn: ")

        if choice == '0':
            break

        # Khởi tạo scraper nâng cao
        download_images = input("\nBạn có muốn tải hình ảnh về máy không? (y/n): ").lower() == 'y'
        scraper = DantriScraperAdvanced(download_images=download_images)

        if choice == '1':
            # Lấy tin mới nhất (đa luồng)
            limit = int(input("\nNhập số lượng bài viết cần lấy: ") or "10")

            print(f"\nĐang lấy {limit} tin mới nhất từ Dân Trí...")

            # Lấy danh sách bài viết
            articles = scraper.get_article_list_with_pagination(f"{scraper.base_url}/tin-moi-nhat.htm", max_pages=3)

            if articles:
                # Lấy URL của các bài viết
                article_urls = [article['link'] for article in articles[:limit]]

                print(f"\nĐang lấy nội dung chi tiết của {len(article_urls)} bài viết...")

                # Lấy nội dung chi tiết (đa luồng)
                extract_comments = input("Bạn có muốn lấy bình luận không? (y/n): ").lower() == 'y'
                article_details = scraper.scrape_articles_parallel(article_urls, extract_comments=extract_comments)

                if article_details:
                    # Chuyển đổi thành DataFrame
                    df = pd.DataFrame(article_details)

                    # Lưu dữ liệu
                    filename = f"data/dantri_advanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    formats = []

                    if input("Xuất ra Excel? (y/n): ").lower() == 'y':
                        formats.append('excel')
                    if input("Xuất ra CSV? (y/n): ").lower() == 'y':
                        formats.append('csv')
                    if input("Xuất ra JSON? (y/n): ").lower() == 'y':
                        formats.append('json')
                    if input("Xuất ra HTML? (y/n): ").lower() == 'y':
                        formats.append('html')

                    if not formats:
                        formats = ['excel']

                    exported_files = scraper.export_to_multiple_formats(df, filename, formats)

                    print("\nĐã xuất dữ liệu ra các file:")
                    for file in exported_files:
                        print(f"- {file}")

                    # Hiển thị thông tin
                    print(f"\nĐã lấy được {len(article_details)} bài viết")
                    for i, article in enumerate(article_details):
                        print(f"{i + 1}. {article['title']}")
                        if 'sentiment' in article:
                            print(
                                f"   Sentiment: {article['sentiment']['label']} (Score: {article['sentiment']['score']:.2f})")
                        print(f"   Word count: {article.get('word_count', 0)}")
                        print()

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '2':
            # Lấy tin từ chuyên mục (với phân trang)
            print("\nĐang lấy danh sách chuyên mục...")
            categories = scraper.get_all_categories()

            if categories:
                print("\nDanh sách chuyên mục:")
                for i, category in enumerate(categories):
                    indent = "  " * (category['level'] - 1)
                    print(f"{i + 1}. {indent}{category['name']}")

                cat_choice = int(input("\nChọn chuyên mục (nhập số): ")) - 1
                if 0 <= cat_choice < len(categories):
                    max_pages = int(input("\nNhập số trang tối đa cần lấy: ") or "3")

                    category = categories[cat_choice]
                    print(f"\nĐang lấy bài viết từ chuyên mục {category['name']} (tối đa {max_pages} trang)...")

                    articles = scraper.get_article_list_with_pagination(category['url'], max_pages=max_pages)

                    if articles:
                        # Chuyển đổi thành DataFrame
                        df = pd.DataFrame(articles)

                        # Lưu dữ liệu
                        filename = f"data/dantri_{category['name'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                        df.to_excel(filename, index=False)

                        print(f"\nĐã lưu dữ liệu vào file {filename}")
                        print(f"\nĐã lấy được {len(articles)} bài viết")

                        # Hiển thị thông tin
                        for i, article in enumerate(articles[:10]):  # Chỉ hiển thị 10 bài đầu tiên
                            print(f"{i + 1}. {article['title']}")

                        if len(articles) > 10:
                            print(f"... và {len(articles) - 10} bài viết khác")
                    else:
                        print("\nKhông lấy được bài viết nào")
                else:
                    print("\nLựa chọn không hợp lệ")
            else:
                print("\nKhông lấy được danh sách chuyên mục")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '3':
            # Tìm kiếm nâng cao
            keyword = input("\nNhập từ khóa tìm kiếm: ")
            if keyword:
                print("\nChọn loại tìm kiếm:")
                print("1. Tất cả")
                print("2. Chỉ tiêu đề")
                print("3. Chỉ nội dung")
                search_type_choice = input("Nhập lựa chọn: ")

                search_type = 'all'
                if search_type_choice == '2':
                    search_type = 'title'
                elif search_type_choice == '3':
                    search_type = 'content'

                print("\nChọn khoảng thời gian:")
                print("1. Tất cả thời gian")
                print("2. 1 ngày qua")
                print("3. 1 tuần qua")
                print("4. 1 tháng qua")
                print("5. 1 năm qua")
                time_range_choice = input("Nhập lựa chọn: ")

                time_range = None
                if time_range_choice == '2':
                    time_range = 'day'
                elif time_range_choice == '3':
                    time_range = 'week'
                elif time_range_choice == '4':
                    time_range = 'month'
                elif time_range_choice == '5':
                    time_range = 'year'

                max_results = int(input("\nNhập số kết quả tối đa: ") or "30")

                print(f"\nĐang tìm kiếm '{keyword}' với các tùy chọn đã chọn...")
                results = scraper.search_advanced(keyword, search_type, time_range, max_results)

                if not results.empty:
                    # Lưu dữ liệu
                    filename = f"data/dantri_search_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    results.to_excel(filename, index=False)

                    print(f"\nĐã lưu kết quả tìm kiếm vào file {filename}")
                    print(f"\nĐã tìm thấy {len(results)} kết quả")

                    # Hiển thị thông tin
                    for i, row in results.iterrows():
                        print(f"{i + 1}. {row['title']}")
                        print(f"   {row['summary'][:100]}...")
                        print()
                else:
                    print(f"\nKhông tìm thấy kết quả nào cho từ khóa '{keyword}'")
            else:
                print("\nTừ khóa tìm kiếm không hợp lệ")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '4':
            # Lấy tin theo khoảng thời gian
            print("\nNhập khoảng thời gian (định dạng YYYY-MM-DD):")
            start_date = input("Từ ngày: ")
            end_date = input("Đến ngày (để trống nếu là ngày hiện tại): ") or None

            category_url = input(
                "\nNhập URL chuyên mục (để trống nếu lấy tin mới nhất): ") or f"{scraper.base_url}/tin-moi-nhat.htm"
            max_articles = int(input("\nNhập số bài viết tối đa: ") or "50")

            print(f"\nĐang lấy tin từ {start_date} đến {end_date or 'hiện tại'}...")
            results = scraper.scrape_by_date_range(category_url, start_date, end_date, max_articles)

            if not results.empty:
                # Lưu dữ liệu
                filename = f"data/dantri_date_range_{start_date}_to_{end_date or 'now'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                results.to_excel(filename, index=False)

                print(f"\nĐã lưu kết quả vào file {filename}")
                print(f"\nĐã lấy được {len(results)} bài viết")

                # Hiển thị thông tin
                for i, row in results.iterrows():
                    print(f"{i + 1}. {row['title']} ({row['publish_time']})")
                    if i >= 9:  # Chỉ hiển thị 10 bài đầu tiên
                        print(f"... và {len(results) - 10} bài viết khác")
                        break
            else:
                print(f"\nKhông tìm thấy bài viết nào trong khoảng thời gian đã chọn")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '5':
            # Phân tích chủ đề xu hướng
            num_days = int(input("\nNhập số ngày gần đây để phân tích: ") or "7")
            min_articles = int(input("Nhập số bài viết tối thiểu để coi là xu hướng: ") or "3")

            print(f"\nĐang phân tích chủ đề xu hướng trong {num_days} ngày qua...")
            trending_topics = scraper.extract_trending_topics(num_days, min_articles)

            if trending_topics:
                # Lưu dữ liệu
                df_trending = pd.DataFrame(trending_topics)
                filename = f"data/dantri_trending_topics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                df_trending.to_excel(filename, index=False)

                print(f"\nĐã lưu kết quả vào file {filename}")
                print(f"\nĐã tìm thấy {len(trending_topics)} chủ đề xu hướng:")

                # Hiển thị thông tin
                for i, topic in enumerate(trending_topics):
                    print(f"{i + 1}. {topic['tag']} - {topic['count']} bài viết ({topic['percentage']:.1f}%)")
            else:
                print(f"\nKhông tìm thấy chủ đề xu hướng nào")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '6':
            # Lên lịch scraping tự động
            category_url = input("\nNhập URL chuyên mục: ") or f"{scraper.base_url}/tin-moi-nhat.htm"
            interval_hours = float(input("Nhập khoảng thời gian giữa các lần scrape (giờ): ") or "24")
            max_runs = int(input("Nhập số lần scrape tối đa: ") or "7")
            output_dir = input("Nhập thư mục lưu dữ liệu: ") or "scheduled_data"

            print(f"\nBắt đầu lên lịch scraping cho {category_url}, mỗi {interval_hours} giờ, tối đa {max_runs} lần")
            print("Lưu ý: Quá trình này sẽ chạy trong thời gian dài. Bạn có thể nhấn Ctrl+C để dừng lại.")

            try:
                scraper.schedule_scraping(category_url, interval_hours, max_runs, output_dir)
            except KeyboardInterrupt:
                print("\nĐã dừng lịch scraping")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '7':
            # Xuất dữ liệu ra nhiều định dạng
            file_path = input("\nNhập đường dẫn đến file Excel chứa dữ liệu: ")

            if os.path.exists(file_path) and file_path.endswith('.xlsx'):
                # Đọc dữ liệu
                df = pd.read_excel(file_path)

                if not df.empty:
                    # Chọn định dạng xuất
                    formats = []
                    if input("Xuất ra Excel? (y/n): ").lower() == 'y':
                        formats.append('excel')
                    if input("Xuất ra CSV? (y/n): ").lower() == 'y':
                        formats.append('csv')
                    if input("Xuất ra JSON? (y/n): ").lower() == 'y':
                        formats.append('json')
                    if input("Xuất ra HTML? (y/n): ").lower() == 'y':
                        formats.append('html')

                    if formats:
                        # Tạo tên file cơ sở
                        base_filename = os.path.splitext(file_path)[0] + "_exported"

                        # Xuất dữ liệu
                        exported_files = scraper.export_to_multiple_formats(df, base_filename, formats)

                        print("\nĐã xuất dữ liệu ra các file:")
                        for file in exported_files:
                            print(f"- {file}")
                    else:
                        print("\nKhông có định dạng nào được chọn")
                else:
                    print("\nFile không chứa dữ liệu")
            else:
                print("\nFile không tồn tại hoặc không phải là file Excel")

            input("\nNhấn Enter để tiếp tục...")

        else:
            print("\nLựa chọn không hợp lệ. Vui lòng thử lại.")
            input("\nNhấn Enter để tiếp tục...")