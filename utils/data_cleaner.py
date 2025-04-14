#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data Cleaner - Làm sạch dữ liệu
"""

import pandas as pd
import numpy as np
import re
import unicodedata


class DataCleaner:
    """Lớp làm sạch dữ liệu"""

    def load_data(self, file_path):
        """Đọc dữ liệu từ file"""
        try:
            if file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                print(f"Định dạng file {file_path} không được hỗ trợ.")
                return None

            return df
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")
            return None

    def save_data(self, df, file_path):
        """Lưu dữ liệu vào file"""
        try:
            if file_path.endswith('.xlsx'):
                df.to_excel(file_path, index=False)
            elif file_path.endswith('.csv'):
                df.to_csv(file_path, index=False)
            else:
                df.to_excel(file_path, index=False)

            return True
        except Exception as e:
            print(f"Lỗi khi lưu file: {e}")
            return False

    def clean_data(self, df, operations):
        """Làm sạch dữ liệu theo các thao tác được chỉ định"""
        df_clean = df.copy()

        for operation in operations:
            name = operation['name']
            params = operation.get('params', {})

            if name == 'remove_duplicates':
                df_clean = self.remove_duplicates(df_clean)

            elif name == 'remove_missing_values':
                threshold = params.get('threshold', 0.5)
                df_clean = self.remove_missing_values(df_clean, threshold)

            elif name == 'fill_missing_values':
                method = params.get('method', 'mean')
                df_clean = self.fill_missing_values(df_clean, method)

            elif name == 'remove_outliers':
                method = params.get('method', 'zscore')
                threshold = params.get('threshold', 3)
                df_clean = self.remove_outliers(df_clean, method, threshold)

            elif name == 'normalize_text':
                columns = params.get('columns', [])
                df_clean = self.normalize_text(df_clean, columns)

        return df_clean

    def remove_duplicates(self, df):
        """Loại bỏ các dòng trùng lặp"""
        return df.drop_duplicates()

    def remove_missing_values(self, df, threshold=0.5):
        """Loại bỏ các dòng có nhiều giá trị thiếu"""
        return df.dropna(thresh=int(threshold * len(df.columns)))

    def fill_missing_values(self, df, method='mean'):
        """Điền giá trị thiếu"""
        df_filled = df.copy()

        # Xử lý các cột số
        numeric_columns = df.select_dtypes(include=['number']).columns

        for col in numeric_columns:
            if method == 'mean':
                df_filled[col] = df_filled[col].fillna(df_filled[col].mean())
            elif method == 'median':
                df_filled[col] = df_filled[col].fillna(df_filled[col].median())
            elif method == 'mode':
                df_filled[col] = df_filled[col].fillna(df_filled[col].mode()[0])
            elif method == 'ffill':
                df_filled[col] = df_filled[col].fillna(method='ffill')
            elif method == 'bfill':
                df_filled[col] = df_filled[col].fillna(method='bfill')
            elif method == 'zero':
                df_filled[col] = df_filled[col].fillna(0)

        # Xử lý các cột không phải số
        non_numeric_columns = df.select_dtypes(exclude=['number']).columns

        for col in non_numeric_columns:
            if method == 'mode':
                df_filled[col] = df_filled[col].fillna(
                    df_filled[col].mode()[0] if not df_filled[col].mode().empty else '')
            elif method == 'ffill':
                df_filled[col] = df_filled[col].fillna(method='ffill')
            elif method == 'bfill':
                df_filled[col] = df_filled[col].fillna(method='bfill')
            else:
                df_filled[col] = df_filled[col].fillna('')

        return df_filled

    def remove_outliers(self, df, method='zscore', threshold=3):
        """Loại bỏ các giá trị ngoại lai"""
        df_clean = df.copy()
        numeric_columns = df.select_dtypes(include=['number']).columns

        for col in numeric_columns:
            if method == 'zscore':
                # Phương pháp Z-score
                z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())
                df_clean = df_clean[z_scores < threshold]

            elif method == 'iqr':
                # Phương pháp IQR (Interquartile Range)
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]

        return df_clean

    def normalize_text(self, df, columns):
        """Chuẩn hóa văn bản"""
        df_clean = df.copy()

        for col in columns:
            if col in df_clean.columns:
                # Chuyển về chữ thường
                df_clean[col] = df_clean[col].astype(str).str.lower()

                # Loại bỏ dấu câu
                df_clean[col] = df_clean[col].apply(lambda x: re.sub(r'[^\w\s]', '', x))

                # Chuẩn hóa Unicode
                df_clean[col] = df_clean[col].apply(
                    lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore').decode('ASCII'))

                # Loại bỏ khoảng trắng thừa
                df_clean[col] = df_clean[col].apply(lambda x: re.sub(r'\s+', ' ', x).strip())

        return df_clean