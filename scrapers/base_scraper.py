#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base Scraper - Lớp cơ sở cho các scraper
"""

import requests
from bs4 import BeautifulSoup
import logging
import os
import time
from datetime import datetime

# Tạo thư mục logs nếu chưa tồn tại
if not os.path.exists('logs'):
    os.makedirs('logs')

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/scraper.log"),
        logging.StreamHandler()
    ]
)


class BaseScraper:
    """Lớp cơ sở cho các scraper"""

    def __init__(self, url=None, headers=None):
        """Khởi tạo"""
        self.url = url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_html(self, url=None, params=None):
        """Lấy HTML từ URL"""
        url = url or self.url

        if not url:
            self.logger.error("URL không được cung cấp")
            return None

        try:
            self.logger.info(f"Đang gửi request đến {url}")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Lỗi khi gửi request: {e}")
            return None

    def parse_html(self, html):
        """Parse HTML với BeautifulSoup"""
        if not html:
            return None

        return BeautifulSoup(html, 'html.parser')

    def scrape(self, url=None, params=None):
        """Phương thức scrape cơ bản"""
        html = self.get_html(url, params)

        if not html:
            return None

        return self.parse_html(html)

    def scrape_with_retry(self, url=None, params=None, max_retries=3, retry_delay=2):
        """Scrape với cơ chế retry"""
        retries = 0

        while retries < max_retries:
            result = self.scrape(url, params)

            if result:
                return result

            retries += 1
            self.logger.warning(f"Retry {retries}/{max_retries} sau {retry_delay} giây")
            time.sleep(retry_delay)

        self.logger.error(f"Đã thử {max_retries} lần nhưng không thành công")
        return None

    def save_to_file(self, data, filename):
        """Lưu dữ liệu vào file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(data)

            self.logger.info(f"Đã lưu dữ liệu vào file {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Lỗi khi lưu file: {e}")
            return False