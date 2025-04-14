#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gold Price Scraper - Lấy dữ liệu giá vàng
"""

from datetime import datetime
from .base_scraper import BaseScraper


class GoldPriceScraper(BaseScraper):
    """Lớp lấy dữ liệu giá vàng"""

    def __init__(self):
        """Khởi tạo"""
        super().__init__(url="https://sjc.com.vn/giavang/textContent.php")

    def scrape(self):
        """Lấy dữ liệu giá vàng"""
        try:
            # Gửi request và parse HTML
            soup = super().scrape()

            if not soup:
                return None

            # Tìm bảng giá vàng
            tables = soup.find_all('table')

            if not tables:
                return None

            # Lấy dữ liệu từ bảng
            data = []

            for table in tables:
                rows = table.find_all('tr')

                for row in rows[1:]:  # Bỏ qua hàng tiêu đề
                    cols = row.find_all('td')

                    if len(cols) >= 4:
                        gold_type = cols[0].text.strip()
                        buy_price = cols[1].text.strip()
                        sell_price = cols[2].text.strip()
                        unit = cols[3].text.strip()

                        data.append({
                            'gold_type': gold_type,
                            'buy_price': buy_price,
                            'sell_price': sell_price,
                            'unit': unit,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })

            return data

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy dữ liệu giá vàng: {e}")
            return None