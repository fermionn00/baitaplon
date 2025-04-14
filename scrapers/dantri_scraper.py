#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dantri Scraper - Lấy dữ liệu từ Dân Trí
"""

import time
import re
from .base_scraper import BaseScraper


class DantriScraper(BaseScraper):
    """Lớp lấy dữ liệu từ Dân Trí"""

    def __init__(self):
        """Khởi tạo"""
        super().__init__(url="https://dantri.com.vn")
        self.base_url = "https://dantri.com.vn"

    def get_latest_news(self, limit=10):
        """Lấy tin mới nhất"""
        try:
            # Gửi request
            url = f"{self.base_url}/tin-moi-nhat.htm"
            soup = super().scrape(url)

            if not soup:
                return None

            # Tìm các bài viết
            articles = []
            article_elements = soup.select('article.article-item')

            for article in article_elements[:limit]:
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

                    articles.append({
                        'title': title,
                        'link': link,
                        'description': description,
                        'publish_time': publish_time,
                        'image_url': image_url
                    })

            return articles

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy tin mới nhất: {e}")
            return None

    def get_categories(self):
        """Lấy danh sách chuyên mục"""
        try:
            # Gửi request
            soup = super().scrape()

            if not soup:
                return None

            # Tìm các chuyên mục
            categories = []
            category_elements = soup.select('nav.menu-wrap ul.menu > li.has-child > a')

            for category in category_elements:
                name = category.text.strip()
                url = category['href']

                if not url.startswith('http'):
                    url = self.base_url + url

                categories.append({
                    'name': name,
                    'url': url
                })

            return categories

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy danh sách chuyên mục: {e}")
            return None

    def get_category_news(self, category_url, limit=10):
        """Lấy tin từ chuyên mục"""
        try:
            # Gửi request
            soup = super().scrape(category_url)

            if not soup:
                return None

            # Tìm các bài viết
            articles = []
            article_elements = soup.select('article.article-item')

            for article in article_elements[:limit]:
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

                    articles.append({
                        'title': title,
                        'link': link,
                        'description': description,
                        'publish_time': publish_time,
                        'image_url': image_url
                    })

            return articles

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy tin từ chuyên mục: {e}")
            return None

    def search(self, keyword, limit=10):
        """Tìm kiếm bài viết"""
        try:
            # Gửi request
            url = f"{self.base_url}/tim-kiem.htm?q={keyword}"
            soup = super().scrape(url)

            if not soup:
                return None

            # Tìm các bài viết
            articles = []
            article_elements = soup.select('article.article-item')

            for article in article_elements[:limit]:
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

                    articles.append({
                        'title': title,
                        'link': link,
                        'description': description,
                        'publish_time': publish_time,
                        'image_url': image_url
                    })

            return articles

        except Exception as e:
            self.logger.error(f"Lỗi khi tìm kiếm bài viết: {e}")
            return None

    def get_article_content(self, article_url):
        """Lấy nội dung bài viết"""
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
            publish_time = time_element.text.strip() if time_element else ""

            # Lấy tác giả
            author_element = soup.select_one('div.author-name')
            author = author_element.text.strip() if author_element else ""

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

                    images.append({
                        'url': image_url,
                        'caption': image_caption
                    })

            return {
                'title': title,
                'description': description,
                'publish_time': publish_time,
                'author': author,
                'content': content,
                'tags': tags,
                'images': images,
                'url': article_url
            }

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy nội dung bài viết: {e}")
            return None