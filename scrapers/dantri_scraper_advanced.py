#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dantri Scraper Advanced - Lấy dữ liệu từ Dân Trí nâng cao
"""

import os
import time
import re
import json
import pandas as pd
import concurrent.futures
from datetime import datetime, timedelta
import urllib.parse
import threading
import shutil
from textblob import TextBlob
from .base_scraper import BaseScraper


class DantriScraperAdvanced(BaseScraper):
    """Lớp lấy dữ liệu từ Dân Trí nâng cao"""

    def __init__(self, download_images=False, cache_enabled=True):
        """Khởi tạo"""
        super().__init__(url="https://dantri.com.vn")
        self.base_url = "https://dantri.com.vn"
        self.download_images = download_images
        self.cache_enabled = cache_enabled
        self.cache = {}

        # Tạo thư mục images nếu chưa tồn tại và download_images=True
        if self.download_images and not os.path.exists('images'):
            os.makedirs('images')

    def get_article_list_with_pagination(self, url, max_pages=3):
        """Lấy danh sách bài viết với phân trang"""
        all_articles = []

        for page in range(1, max_pages + 1):
            page_url = f"{url}/trang-{page}.htm" if page > 1 else url

            try:
                # Gửi request
                soup = super().scrape(page_url)

                # Kiểm tra nếu trang không tồn tại
                if not soup:
                    break

                # Tìm các bài viết
                article_elements = soup.select('article.article-item')

                if not article_elements:
                    break

                for article in article_elements:
                    # Lấy tiêu đề và link
                    title_element = article.select_one('h3.article-title a')

                    if title_element:
                        title = title_element.text.strip()
                        link = title_element['href']

                        if not link.startswith('http'):
                            link = self.base_url + link

                        # Lấy mô tả
                        description_element = article.select_one('div.article-excerpt')
                        description = description_element.text.strip() if description_element else ""

                        # Lấy thời gian
                        time_element = article.select_one('time.article-time')
                        publish_time = time_element.text.strip() if time_element else ""

                        # Lấy ảnh
                        image_element = article.select_one('img.article-thumb')
                        image_url = image_element['src'] if image_element and 'src' in image_element.attrs else ""

                        all_articles.append({
                            'title': title,
                            'link': link,
                            'description': description,
                            'publish_time': publish_time,
                            'image_url': image_url
                        })

                # Delay để tránh quá tải server
                time.sleep(1)

            except Exception as e:
                self.logger.error(f"Lỗi khi lấy trang {page}: {e}")
                break

        return all_articles

    def get_all_categories(self):
        """Lấy tất cả chuyên mục (bao gồm cả chuyên mục con)"""
        try:
            # Gửi request
            soup = super().scrape()

            if not soup:
                return None

            # Tìm các chuyên mục
            categories = []

            # Lấy chuyên mục chính
            main_categories = soup.select('nav.menu-wrap ul.menu > li.has-child')

            for i, main_category in enumerate(main_categories):
                main_link = main_category.select_one('a')

                if main_link:
                    main_name = main_link.text.strip()
                    main_url = main_link['href']

                    if not main_url.startswith('http'):
                        main_url = self.base_url + main_url

                    categories.append({
                        'name': main_name,
                        'url': main_url,
                        'level': 1
                    })

                    # Lấy chuyên mục con
                    sub_categories = main_category.select('ul.submenu li a')

                    for sub_link in sub_categories:
                        sub_name = sub_link.text.strip()
                        sub_url = sub_link['href']

                        if not sub_url.startswith('http'):
                            sub_url = self.base_url + sub_url

                        categories.append({
                            'name': sub_name,
                            'url': sub_url,
                            'level': 2,
                            'parent': main_name
                        })

            return categories

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy danh sách chuyên mục: {e}")
            return None

    def search_advanced(self, keyword, search_type='all', time_range=None, max_results=30):
        """Tìm kiếm nâng cao"""
        try:
            # Xây dựng URL tìm kiếm
            encoded_keyword = urllib.parse.quote(keyword)
            url = f"{self.base_url}/tim-kiem.htm?q={encoded_keyword}"

            # Thêm tham số tìm kiếm
            if search_type == 'title':
                url += "&t=1"
            elif search_type == 'content':
                url += "&t=2"

            # Thêm tham số thời gian
            if time_range == 'day':
                url += "&d=1"
            elif time_range == 'week':
                url += "&d=7"
            elif time_range == 'month':
                url += "&d=30"
            elif time_range == 'year':
                url += "&d=365"

            # Tính số trang cần lấy
            pages_to_fetch = (max_results + 19) // 20  # Mỗi trang có khoảng 20 kết quả

            # Lấy kết quả tìm kiếm
            all_results = []

            for page in range(1, pages_to_fetch + 1):
                page_url = f"{url}/trang-{page}.htm" if page > 1 else url

                # Gửi request
                soup = super().scrape(page_url)

                # Kiểm tra nếu trang không tồn tại
                if not soup:
                    break

                # Tìm các bài viết
                article_elements = soup.select('article.article-item')

                if not article_elements:
                    break

                for article in article_elements:
                    # Lấy tiêu đề và link
                    title_element = article.select_one('h3.article-title a')

                    if title_element:
                        title = title_element.text.strip()
                        link = title_element['href']

                        if not link.startswith('http'):
                            link = self.base_url + link

                        # Lấy mô tả
                        description_element = article.select_one('div.article-excerpt')
                        description = description_element.text.strip() if description_element else ""

                        # Lấy thời gian
                        time_element = article.select_one('time.article-time')
                        publish_time = time_element.text.strip() if time_element else ""

                        # Lấy ảnh
                        image_element = article.select_one('img.article-thumb')
                        image_url = image_element['src'] if image_element and 'src' in image_element.attrs else ""

                        all_results.append({
                            'title': title,
                            'link': link,
                            'summary': description,
                            'publish_time': publish_time,
                            'image_url': image_url
                        })

                # Kiểm tra nếu đã đủ số lượng kết quả
                if len(all_results) >= max_results:
                    break

                # Delay để tránh quá tải server
                time.sleep(1)

            # Giới hạn số lượng kết quả
            all_results = all_results[:max_results]

            # Chuyển đổi thành DataFrame
            df_results = pd.DataFrame(all_results)

            return df_results

        except Exception as e:
            self.logger.error(f"Lỗi khi tìm kiếm nâng cao: {e}")
            return pd.DataFrame()

    def scrape_by_date_range(self, category_url, start_date, end_date=None, max_articles=50):
        """Lấy tin theo khoảng thời gian"""
        try:
            # Chuyển đổi ngày bắt đầu và kết thúc
            start_date = datetime.strptime(start_date, '%Y-%m-%d')

            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            else:
                end_date = datetime.now()

            # Lấy danh sách bài viết
            all_articles = []
            page = 1

            while len(all_articles) < max_articles:
                page_url = f"{category_url}/trang-{page}.htm" if page > 1 else category_url

                # Gửi request
                soup = super().scrape(page_url)

                # Kiểm tra nếu trang không tồn tại
                if not soup:
                    break

                # Tìm các bài viết
                article_elements = soup.select('article.article-item')

                if not article_elements:
                    break

                found_articles_in_range = False

                for article in article_elements:
                    # Lấy thời gian
                    time_element = article.select_one('time.article-time')

                    if time_element:
                        publish_time_str = time_element.text.strip()

                        # Chuyển đổi chuỗi thời gian sang datetime
                        try:
                            # Xử lý các định dạng thời gian khác nhau
                            if re.search(r'\d{2}/\d{2}/\d{4}', publish_time_str):
                                publish_time = datetime.strptime(publish_time_str, '%d/%m/%Y %H:%M')
                            elif re.search(r'\d{2}:\d{2} \d{2}/\d{2}/\d{4}', publish_time_str):
                                publish_time = datetime.strptime(publish_time_str, '%H:%M %d/%m/%Y')
                            else:
                                # Nếu không khớp với các định dạng trên, thử định dạng khác
                                publish_time = datetime.strptime(publish_time_str, '%d/%m/%Y')
                        except:
                            # Nếu không thể chuyển đổi, bỏ qua bài viết này
                            continue

                        # Kiểm tra xem bài viết có nằm trong khoảng thời gian không
                        if start_date <= publish_time <= end_date:
                            found_articles_in_range = True

                            # Lấy tiêu đề và link
                            title_element = article.select_one('h3.article-title a')

                            if title_element:
                                title = title_element.text.strip()
                                link = title_element['href']

                                if not link.startswith('http'):
                                    link = self.base_url + link

                                # Lấy mô tả
                                description_element = article.select_one('div.article-excerpt')
                                description = description_element.text.strip() if description_element else ""

                                # Lấy ảnh
                                image_element = article.select_one('img.article-thumb')
                                image_url = image_element[
                                    'src'] if image_element and 'src' in image_element.attrs else ""

                                all_articles.append({
                                    'title': title,
                                    'link': link,
                                    'description': description,
                                    'publish_time': publish_time,
                                    'image_url': image_url
                                })

                                # Kiểm tra nếu đã đủ số lượng bài viết
                                if len(all_articles) >= max_articles:
                                    break
                        elif publish_time < start_date:
                            # Nếu bài viết cũ hơn ngày bắt đầu, dừng lại
                            break

                # Nếu không tìm thấy bài viết nào trong khoảng thời gian hoặc đã đủ số lượng, dừng lại
                if not found_articles_in_range or len(all_articles) >= max_articles:
                    break

                # Tăng số trang
                page += 1

                # Delay để tránh quá tải server
                time.sleep(1)

            # Chuyển đổi thành DataFrame
            df_articles = pd.DataFrame(all_articles)

            return df_articles

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy tin theo khoảng thời gian: {e}")
            return pd.DataFrame()

    def get_article_content_advanced(self, article_url, extract_comments=False):
        """Lấy nội dung bài viết nâng cao"""
        # Kiểm tra cache
        if self.cache_enabled and article_url in self.cache:
            return self.cache[article_url]

        try:
            # Gửi request
            soup = super().scrape(article_url)

            if not soup:
                return None

            # Lấy tiêu đề
            title_element = soup.select_one('h1.title-page')
            title = title_element.text.strip() if title_element else ""

            # Lấy mô tả
            description_element = soup.select_one('h2.singular-sapo')
            description = description_element.text.strip() if description_element else ""

            # Lấy thời gian
            time_element = soup.select_one('time.author-time')
            publish_time_str = time_element.text.strip() if time_element else ""

            # Chuyển đổi chuỗi thời gian sang datetime
            publish_time = None
            if publish_time_str:
                try:
                    # Xử lý các định dạng thời gian khác nhau
                    if re.search(r'\d{2}/\d{2}/\d{4}', publish_time_str):
                        publish_time = datetime.strptime(publish_time_str, '%d/%m/%Y %H:%M')
                    elif re.search(r'\d{2}:\d{2} \d{2}/\d{2}/\d{4}', publish_time_str):
                        publish_time = datetime.strptime(publish_time_str, '%H:%M %d/%m/%Y')
                    else:
                        # Nếu không khớp với các định dạng trên, thử định dạng khác
                        publish_time = datetime.strptime(publish_time_str, '%d/%m/%Y')
                except:
                    publish_time = None

            # Lấy tác giả
            author_element = soup.select_one('div.author-name')
            author = author_element.text.strip() if author_element else ""

            # Lấy chuyên mục
            category_element = soup.select_one('ul.breadcrumbs li:nth-child(2) a')
            category = category_element.text.strip() if category_element else ""

            # Lấy nội dung
            content_element = soup.select_one('div.singular-content')
            content = ""

            if content_element:
                # Loại bỏ các phần tử không cần thiết
                for element in content_element.select('div.e-magazine-detail, div.singular-sticky, div.related-news'):
                    element.decompose()

                # Lấy nội dung văn bản
                paragraphs = content_element.select('p')
                content = '\n'.join([p.text.strip() for p in paragraphs])

            # Đếm số từ
            word_count = len(content.split()) if content else 0

            # Lấy tags
            tags = []
            tag_elements = soup.select('ul.tags li a')

            for tag in tag_elements:
                tags.append(tag.text.strip())

            # Lấy ảnh
            images = []
            image_elements = soup.select('div.singular-content img')

            for img in image_elements:
                if 'src' in img.attrs:
                    image_url = img['src']
                    image_caption = ""

                    # Tìm caption của ảnh
                    caption_element = img.find_next('figcaption')
                    if caption_element:
                        image_caption = caption_element.text.strip()

                    # Tải ảnh về nếu được yêu cầu
                    local_path = None
                    if self.download_images:
                        try:
                            # Tạo tên file từ URL
                            image_filename = os.path.basename(image_url)
                            if '?' in image_filename:
                                image_filename = image_filename.split('?')[0]

                            # Thêm timestamp để tránh trùng tên
                            timestamp = int(time.time())
                            image_filename = f"{timestamp}_{image_filename}"

                            # Đường dẫn lưu file
                            local_path = os.path.join('images', image_filename)

                            # Tải ảnh
                            img_response = requests.get(image_url, headers=self.headers, stream=True)
                            img_response.raise_for_status()

                            with open(local_path, 'wb') as f:
                                shutil.copyfileobj(img_response.raw, f)
                        except Exception as e:
                            self.logger.error(f"Lỗi khi tải ảnh: {e}")
                            local_path = None

                    images.append({
                        'url': image_url,
                        'caption': image_caption,
                        'local_path': local_path
                    })

            # Lấy bình luận nếu được yêu cầu
            comments = []
            if extract_comments:
                # Lấy ID bài viết
                article_id = None
                script_elements = soup.select('script')

                for script in script_elements:
                    script_text = script.string
                    if script_text and 'article_id' in script_text:
                        match = re.search(r'article_id\s*=\s*(\d+)', script_text)
                        if match:
                            article_id = match.group(1)
                            break

                if article_id:
                    # Lấy bình luận
                    comments_url = f"https://comment.dantri.com.vn/api/comments?article_id={article_id}&order_by=newest&page=1&limit=100"

                    try:
                        comments_response = requests.get(comments_url, headers=self.headers)
                        comments_response.raise_for_status()

                        comments_data = comments_response.json()

                        if 'data' in comments_data and 'items' in comments_data['data']:
                            for comment in comments_data['data']['items']:
                                comments.append({
                                    'id': comment.get('id'),
                                    'content': comment.get('content'),
                                    'created_at': comment.get('created_at'),
                                    'user_name': comment.get('user', {}).get('name'),
                                    'likes': comment.get('likes_count', 0),
                                    'replies_count': comment.get('replies_count', 0)
                                })
                    except Exception as e:
                        self.logger.error(f"Lỗi khi lấy bình luận: {e}")

            # Phân tích cảm xúc
            sentiment = None
            try:
                if content:
                    blob = TextBlob(content)
                    polarity = blob.sentiment.polarity

                    if polarity > 0.1:
                        sentiment_label = 'positive'
                    elif polarity < -0.1:
                        sentiment_label = 'negative'
                    else:
                        sentiment_label = 'neutral'

                    sentiment = {
                        'score': polarity,
                        'label': sentiment_label
                    }
            except Exception as e:
                self.logger.error(f"Lỗi khi phân tích cảm xúc: {e}")

            # Tạo kết quả
            result = {
                'title': title,
                'description': description,
                'publish_time': publish_time,
                'publish_time_str': publish_time_str,
                'author': author,
                'category': category,
                'content': content,
                'word_count': word_count,
                'tags': tags,
                'images': images,
                'comments': comments,
                'sentiment': sentiment,
                'url': article_url
            }

            # Lưu vào cache
            if self.cache_enabled:
                self.cache[article_url] = result

            return result

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy nội dung bài viết: {e}")
            return None

    def scrape_articles_parallel(self, article_urls, max_workers=5, extract_comments=False):
        """Lấy nội dung nhiều bài viết song song"""
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Tạo các future
            future_to_url = {executor.submit(self.get_article_content_advanced, url, extract_comments): url for url in
                             article_urls}

            # Lấy kết quả khi hoàn thành
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    if data:
                        results.append(data)
                except Exception as e:
                    self.logger.error(f"Lỗi khi lấy nội dung bài viết {url}: {e}")

        return results

    def extract_trending_topics(self, num_days=7, min_articles=3):
        """Trích xuất chủ đề xu hướng"""
        try:
            # Tính ngày bắt đầu
            start_date = (datetime.now() - timedelta(days=num_days)).strftime('%Y-%m-%d')

            # Lấy tin mới nhất
            articles = self.get_article_list_with_pagination(f"{self.base_url}/tin-moi-nhat.htm", max_pages=10)

            if not articles:
                return None

            # Lấy nội dung chi tiết của các bài viết
            article_urls = [article['link'] for article in articles]
            article_details = self.scrape_articles_parallel(article_urls, max_workers=5)

            if not article_details:
                return None

            # Đếm số lần xuất hiện của mỗi tag
            tag_counts = {}
            total_articles = len(article_details)

            for article in article_details:
                if 'tags' in article and article['tags']:
                    for tag in article['tags']:
                        if tag in tag_counts:
                            tag_counts[tag] += 1
                        else:
                            tag_counts[tag] = 1

            # Lọc các tag xuất hiện nhiều nhất
            trending_topics = []

            for tag, count in tag_counts.items():
                if count >= min_articles:
                    percentage = count / total_articles * 100
                    trending_topics.append({
                        'tag': tag,
                        'count': count,
                        'percentage': percentage
                    })

            # Sắp xếp theo số lượng bài viết giảm dần
            trending_topics.sort(key=lambda x: x['count'], reverse=True)

            return trending_topics

        except Exception as e:
            self.logger.error(f"Lỗi khi trích xuất chủ đề xu hướng: {e}")
            return None

    def schedule_scraping(self, category_url, interval_hours=24, max_runs=7, output_dir="scheduled_data"):
        """Lên lịch scraping tự động"""
        # Tạo thư mục output nếu chưa tồn tại
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Hàm scraping
        def scrape_job(run_count):
            try:
                self.logger.info(
                    f"Bắt đầu scraping lần {run_count + 1}/{max_runs} vào {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                # Lấy danh sách bài viết
                articles = self.get_article_list_with_pagination(category_url, max_pages=3)

                if articles:
                    # Lấy nội dung chi tiết của các bài viết
                    article_urls = [article['link'] for article in articles[:20]]  # Giới hạn 20 bài viết
                    article_details = self.scrape_articles_parallel(article_urls, max_workers=5)

                    if article_details:
                        # Lưu dữ liệu
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{output_dir}/dantri_scheduled_{timestamp}.xlsx"

                        # Chuyển đổi thành DataFrame
                        df = pd.DataFrame(article_details)

                        # Lưu dữ liệu
                        df.to_excel(filename, index=False)

                        self.logger.info(f"Đã lưu dữ liệu vào file {filename}")
                        self.logger.info(f"Đã lấy được {len(article_details)} bài viết")

                self.logger.info(f"Hoàn thành scraping lần {run_count + 1}/{max_runs}")

                # Lên lịch cho lần tiếp theo nếu chưa đạt max_runs
                if run_count + 1 < max_runs:
                    # Tính thời gian chờ
                    interval_seconds = interval_hours * 3600

                    self.logger.info(f"Lần scraping tiếp theo sẽ diễn ra sau {interval_hours} giờ")

                    # Tạo timer
                    timer = threading.Timer(interval_seconds, scrape_job, args=[run_count + 1])
                    timer.daemon = True
                    timer.start()

            except Exception as e:
                self.logger.error(f"Lỗi khi thực hiện scraping tự động: {e}")

        # Bắt đầu scraping
        scrape_job(0)

    def export_to_multiple_formats(self, df, base_filename, formats=['excel']):
        """Xuất dữ liệu ra nhiều định dạng"""
        exported_files = []

        try:
            for format_type in formats:
                if format_type == 'excel':
                    filename = f"{base_filename}.xlsx"
                    df.to_excel(filename, index=False)
                    exported_files.append(filename)

                elif format_type == 'csv':
                    filename = f"{base_filename}.csv"
                    df.to_csv(filename, index=False, encoding='utf-8-sig')
                    exported_files.append(filename)

                elif format_type == 'json':
                    filename = f"{base_filename}.json"
                    df.to_json(filename, orient='records', force_ascii=False, indent=4)
                    exported_files.append(filename)

                elif format_type == 'html':
                    filename = f"{base_filename}.html"

                    # Tạo HTML với styling
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>Dữ liệu từ Dân Trí</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; margin: 20px; }}
                            table {{ border-collapse: collapse; width: 100%; }}
                            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                            th {{ background-color: #f2f2f2; }}
                            tr:nth-child(even) {{ background-color: #f9f9f9; }}
                            h1 {{ color: #2c3e50; }}
                            .timestamp {{ color: #7f8c8d; font-size: 0.8em; }}
                        </style>
                    </head>
                    <body>
                        <h1>Dữ liệu từ Dân Trí</h1>
                        <p class="timestamp">Xuất vào: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        {df.to_html(index=False)}
                    </body>
                    </html>
                    """

                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(html_content)

                    exported_files.append(filename)

        except Exception as e:
            self.logger.error(f"Lỗi khi xuất dữ liệu: {e}")

        return exported_files