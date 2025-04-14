#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exchange Rate Scraper - Lấy dữ liệu tỷ giá
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base_scraper import BaseScraper


class ExchangeRateScraper(BaseScraper):
    """Lớp lấy dữ liệu tỷ giá"""

    def __init__(self):
        """Khởi tạo"""
        super().__init__(url="https://portal.vietcombank.com.vn/Personal/TG/Pages/ty-gia.aspx")

    def scrape(self):
        """Lấy dữ liệu tỷ giá"""
        try:
            # Gửi request
            soup = super().scrape()

            if not soup:
                return None

            # Tìm bảng tỷ giá
            table = soup.find('table', {'class': 'table-responsive'})

            if not table:
                return None

            # Lấy dữ liệu từ bảng
            data = []

            rows = table.find_all('tr')
            for row in rows[1:]:  # Bỏ qua hàng tiêu đề
                cols = row.find_all('td')

                if len(cols) >= 5:
                    currency_code = cols[0].text.strip()
                    currency_name = cols[1].text.strip()
                    buy_cash = cols[2].text.strip()
                    buy_transfer = cols[3].text.strip()
                    sell = cols[4].text.strip()

                    data.append({
                        'currency_code': currency_code,
                        'currency_name': currency_name,
                        'buy_cash': buy_cash,
                        'buy_transfer': buy_transfer,
                        'sell': sell,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })

            return data

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy dữ liệu tỷ giá: {e}")
            return None