#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Custom Scraper - Lấy dữ liệu từ URL tùy chỉnh
"""

import pandas as pd
from .base_scraper import BaseScraper


class CustomScraper(BaseScraper):
    """Lớp lấy dữ liệu từ URL tùy chỉnh"""

    def __init__(self, url):
        """Khởi tạo"""
        super().__init__(url=url)

    def scrape_tables(self):
        """Lấy tất cả bảng từ URL"""
        try:
            # Gửi request và parse HTML
            soup = super().scrape()

            if not soup:
                return None

            # Tìm tất cả bảng
            tables = soup.find_all('table')

            if not tables:
                return None

            # Chuyển đổi các bảng thành DataFrame
            dfs = []

            for table in tables:
                # Lấy tiêu đề
                headers = []
                header_row = table.find('tr')

                if header_row:
                    headers = [th.text.strip() for th in header_row.find_all(['th', 'td'])]

                # Lấy dữ liệu
                rows = []
                data_rows = table.find_all('tr')[1:] if header_row else table.find_all('tr')

                for row in data_rows:
                    cells = [td.text.strip() for td in row.find_all('td')]
                    if cells:
                        rows.append(cells)

                # Tạo DataFrame
                if headers and rows and len(headers) == len(rows[0]):
                    df = pd.DataFrame(rows, columns=headers)
                elif rows:
                    df = pd.DataFrame(rows)
                else:
                    continue

                dfs.append(df)

            return dfs

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy dữ liệu bảng: {e}")
            return None

    def scrape_by_css(self, css_selector):
        """Lấy dữ liệu theo CSS selector"""
        try:
            # Gửi request và parse HTML
            soup = super().scrape()

            if not soup:
                return None

            # Tìm các phần tử theo CSS selector
            elements = soup.select(css_selector)

            if not elements:
                return None

            # Lấy nội dung của các phần tử
            data = [element.text.strip() for element in elements]

            return data

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy dữ liệu theo CSS selector: {e}")
            return None