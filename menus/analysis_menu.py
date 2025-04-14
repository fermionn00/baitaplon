#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Analysis Menu - Menu phân tích dữ liệu
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from utils.common import clear_screen, print_header
from utils.data_cleaner import DataCleaner
from utils.news_analyzer_advanced import NewsAnalyzerAdvanced


def show_analysis_menu():
    """Hiển thị menu phân tích dữ liệu"""
    while True:
        clear_screen()
        print_header("PHÂN TÍCH DỮ LIỆU")
        print("\n1. Làm sạch dữ liệu")
        print("2. Tính toán thống kê")
        print("3. Vẽ biểu đồ")
        print("4. Phân tích dữ liệu theo thời gian")
        print("5. Phân tích dữ liệu tin tức")
        print("6. Phân tích dữ liệu tin tức nâng cao")
        print("0. Quay lại")

        choice = input("\nNhập lựa chọn của bạn: ")

        if choice == '0':
            break

        elif choice == '1':
            # Làm sạch dữ liệu
            file_path = input("\nNhập đường dẫn đến file dữ liệu: ")

            if not os.path.exists(file_path):
                print(f"\nFile {file_path} không tồn tại.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            # Khởi tạo data cleaner
            cleaner = DataCleaner()

            # Đọc dữ liệu
            df = cleaner.load_data(file_path)

            if df is not None:
                # Hiển thị thông tin ban đầu
                print(f"\nĐã đọc dữ liệu từ file {file_path}")
                print(f"Số dòng: {len(df)}")
                print(f"Số cột: {len(df.columns)}")

                # Chọn các thao tác làm sạch
                print("\nChọn các thao tác làm sạch:")
                print("1. Loại bỏ dòng trùng lặp")
                print("2. Loại bỏ dòng có nhiều giá trị thiếu")
                print("3. Điền giá trị thiếu")
                print("4. Loại bỏ giá trị ngoại lai")
                print("5. Chuẩn hóa văn bản")
                print("6. Tất cả các thao tác trên")

                clean_choice = input("\nNhập lựa chọn của bạn (nhiều lựa chọn, phân cách bằng dấu phẩy): ")
                clean_options = [int(x.strip()) for x in clean_choice.split(',') if x.strip().isdigit()]

                # Tạo danh sách các thao tác
                operations = []

                if 1 in clean_options or 6 in clean_options:
                    operations.append({'name': 'remove_duplicates'})

                if 2 in clean_options or 6 in clean_options:
                    threshold = float(input("\nNhập ngưỡng tỷ lệ giá trị thiếu để loại bỏ dòng (0-1): ") or "0.5")
                    operations.append({'name': 'remove_missing_values', 'params': {'threshold': threshold}})

                if 3 in clean_options or 6 in clean_options:
                    print("\nChọn phương pháp điền giá trị thiếu:")
                    print("1. Giá trị trung bình (mean)")
                    print("2. Giá trị trung vị (median)")
                    print("3. Giá trị phổ biến nhất (mode)")
                    print("4. Giá trị trước đó (ffill)")
                    print("5. Giá trị sau đó (bfill)")
                    print("6. Giá trị 0 (zero)")

                    fill_choice = input("\nNhập lựa chọn của bạn: ")

                    fill_method = 'mean'
                    if fill_choice == '2':
                        fill_method = 'median'
                    elif fill_choice == '3':
                        fill_method = 'mode'
                    elif fill_choice == '4':
                        fill_method = 'ffill'
                    elif fill_choice == '5':
                        fill_method = 'bfill'
                    elif fill_choice == '6':
                        fill_method = 'zero'

                    operations.append({'name': 'fill_missing_values', 'params': {'method': fill_method}})

                if 4 in clean_options or 6 in clean_options:
                    print("\nChọn phương pháp phát hiện ngoại lai:")
                    print("1. Z-score")
                    print("2. IQR (Interquartile Range)")

                    outlier_choice = input("\nNhập lựa chọn của bạn: ")

                    outlier_method = 'zscore'
                    if outlier_choice == '2':
                        outlier_method = 'iqr'

                    threshold = float(input("\nNhập ngưỡng để xác định giá trị ngoại lai: ") or "3")

                    operations.append(
                        {'name': 'remove_outliers', 'params': {'method': outlier_method, 'threshold': threshold}})

                if 5 in clean_options or 6 in clean_options:
                    # Hiển thị các cột văn bản
                    text_columns = df.select_dtypes(include=['object']).columns.tolist()

                    if text_columns:
                        print("\nCác cột văn bản:")
                        for i, col in enumerate(text_columns):
                            print(f"{i + 1}. {col}")

                        col_indices = input(
                            "\nNhập số thứ tự các cột cần chuẩn hóa (nhiều lựa chọn, phân cách bằng dấu phẩy): ")
                        selected_indices = [int(x.strip()) - 1 for x in col_indices.split(',') if x.strip().isdigit()]

                        if selected_indices:
                            selected_columns = [text_columns[i] for i in selected_indices if 0 <= i < len(text_columns)]
                            operations.append({'name': 'normalize_text', 'params': {'columns': selected_columns}})
                    else:
                        print("\nKhông có cột văn bản nào trong dữ liệu.")

                # Làm sạch dữ liệu
                if operations:
                    df_clean = cleaner.clean_data(df, operations)

                    # Hiển thị kết quả
                    print(f"\nĐã làm sạch dữ liệu: {len(df)} dòng -> {len(df_clean)} dòng")

                    # Lưu kết quả
                    output_file = os.path.splitext(file_path)[0] + "_cleaned.xlsx"
                    cleaner.save_data(df_clean, output_file)

                    print(f"\nĐã lưu dữ liệu đã làm sạch vào file {output_file}")
                else:
                    print("\nKhông có thao tác làm sạch nào được chọn.")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '2':
            # Tính toán thống kê
            file_path = input("\nNhập đường dẫn đến file dữ liệu: ")

            if not os.path.exists(file_path):
                print(f"\nFile {file_path} không tồn tại.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            try:
                # Đọc dữ liệu
                if file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    print("\nĐịnh dạng file không được hỗ trợ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                # Hiển thị thông tin
                print(f"\n Đã đọc dữ liệu từ file {file_path}")
                print(f"Số dòng: {len(df)}")
                print(f"Số cột: {len(df.columns)}")

                # Hiển thị các cột số
                numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

                if not numeric_columns:
                    print("\nKhông có cột số nào trong dữ liệu.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                print("\nCác cột số:")
                for i, col in enumerate(numeric_columns):
                    print(f"{i + 1}. {col}")

                # Chọn cột để tính toán thống kê
                col_indices = input(
                    "\nNhập số thứ tự các cột cần tính toán thống kê (nhiều lựa chọn, phân cách bằng dấu phẩy): ")
                selected_indices = [int(x.strip()) - 1 for x in col_indices.split(',') if x.strip().isdigit()]

                if not selected_indices:
                    print("\nKhông có cột nào được chọn.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                selected_columns = [numeric_columns[i] for i in selected_indices if 0 <= i < len(numeric_columns)]

                # Tính toán thống kê
                stats = df[selected_columns].describe()

                # Hiển thị kết quả
                print("\nKết quả thống kê:")
                print(stats)

                # Tính thêm các thống kê khác
                for col in selected_columns:
                    print(f"\nThống kê chi tiết cho cột {col}:")
                    print(f"Trung bình: {df[col].mean()}")
                    print(f"Trung vị: {df[col].median()}")
                    print(f"Độ lệch chuẩn: {df[col].std()}")
                    print(f"Giá trị nhỏ nhất: {df[col].min()}")
                    print(f"Giá trị lớn nhất: {df[col].max()}")
                    print(f"Tổng: {df[col].sum()}")
                    print(f"Số giá trị thiếu: {df[col].isna().sum()}")

                # Lưu kết quả
                output_file = os.path.splitext(file_path)[0] + "_stats.xlsx"
                stats.to_excel(output_file)

                print(f"\nĐã lưu kết quả thống kê vào file {output_file}")

            except Exception as e:
                print(f"\nLỗi khi tính toán thống kê: {e}")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '3':
            # Vẽ biểu đồ
            file_path = input("\nNhập đường dẫn đến file dữ liệu: ")

            if not os.path.exists(file_path):
                print(f"\nFile {file_path} không tồn tại.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            try:
                # Đọc dữ liệu
                if file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    print("\nĐịnh dạng file không được hỗ trợ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                # Hiển thị thông tin
                print(f"\nĐã đọc dữ liệu từ file {file_path}")
                print(f"Số dòng: {len(df)}")
                print(f"Số cột: {len(df.columns)}")

                # Hiển thị các cột
                print("\nCác cột trong dữ liệu:")
                for i, col in enumerate(df.columns):
                    print(f"{i + 1}. {col}")

                # Chọn loại biểu đồ
                print("\nChọn loại biểu đồ:")
                print("1. Biểu đồ cột (Bar chart)")
                print("2. Biểu đồ đường (Line chart)")
                print("3. Biểu đồ tròn (Pie chart)")
                print("4. Biểu đồ phân tán (Scatter plot)")
                print("5. Biểu đồ hộp (Box plot)")
                print("6. Biểu đồ histogram")

                chart_type = input("\nNhập lựa chọn của bạn: ")

                if chart_type == '1':
                    # Biểu đồ cột
                    x_col_index = int(input("\nNhập số thứ tự cột cho trục X: ")) - 1
                    y_col_index = int(input("Nhập số thứ tự cột cho trục Y: ")) - 1

                    if x_col_index < 0 or x_col_index >= len(df.columns) or y_col_index < 0 or y_col_index >= len(
                            df.columns):
                        print("\nSố thứ tự cột không hợp lệ.")
                        input("\nNhấn Enter để tiếp tục...")
                        continue

                    x_col = df.columns[x_col_index]
                    y_col = df.columns[y_col_index]

                    # Vẽ biểu đồ
                    plt.figure(figsize=(10, 6))
                    plt.bar(df[x_col], df[y_col])
                    plt.xlabel(x_col)
                    plt.ylabel(y_col)
                    plt.title(f"Biểu đồ cột {y_col} theo {x_col}")
                    plt.xticks(rotation=45)
                    plt.tight_layout()

                    # Lưu biểu đồ
                    output_file = os.path.splitext(file_path)[0] + "_bar_chart.png"
                    plt.savefig(output_file)
                    plt.close()

                    print(f"\nĐã lưu biểu đồ cột vào file {output_file}")

                elif chart_type == '2':
                    # Biểu đồ đường
                    x_col_index = int(input("\nNhập số thứ tự cột cho trục X: ")) - 1
                    y_col_index = int(input("Nhập số thứ tự cột cho trục Y: ")) - 1

                    if x_col_index < 0 or x_col_index >= len(df.columns) or y_col_index < 0 or y_col_index >= len(
                            df.columns):
                        print("\nSố thứ tự cột không hợp lệ.")
                        input("\nNhấn Enter để tiếp tục...")
                        continue

                    x_col = df.columns[x_col_index]
                    y_col = df.columns[y_col_index]

                    # Vẽ biểu đồ
                    plt.figure(figsize=(10, 6))
                    plt.plot(df[x_col], df[y_col], marker='o')
                    plt.xlabel(x_col)
                    plt.ylabel(y_col)
                    plt.title(f"Biểu đồ đường {y_col} theo {x_col}")
                    plt.xticks(rotation=45)
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()

                    # Lưu biểu đồ
                    output_file = os.path.splitext(file_path)[0] + "_line_chart.png"
                    plt.savefig(output_file)
                    plt.close()

                    print(f"\nĐã lưu biểu đồ đường vào file {output_file}")

                elif chart_type == '3':
                    # Biểu đồ tròn
                    col_index = int(input("\nNhập số thứ tự cột cho biểu đồ tròn: ")) - 1

                    if col_index < 0 or col_index >= len(df.columns):
                        print("\nSố thứ tự cột không hợp lệ.")
                        input("\nNhấn Enter để tiếp tục...")
                        continue

                    col = df.columns[col_index]

                    # Đếm tần suất
                    value_counts = df[col].value_counts()

                    # Giới hạn số lượng giá trị hiển thị
                    max_items = int(input("\nNhập số lượng giá trị tối đa hiển thị: ") or "10")

                    if len(value_counts) > max_items:
                        other_count = value_counts[max_items:].sum()
                        value_counts = value_counts[:max_items]
                        value_counts['Khác'] = other_count

                    # Vẽ biểu đồ
                    plt.figure(figsize=(10, 8))
                    plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
                    plt.axis('equal')
                    plt.title(f"Biểu đồ tròn cho {col}")
                    plt.tight_layout()

                    # Lưu biểu đồ
                    output_file = os.path.splitext(file_path)[0] + "_pie_chart.png"
                    plt.savefig(output_file)
                    plt.close()

                    print(f"\nĐã lưu biểu đồ tròn vào file {output_file}")

                elif chart_type == '4':
                    # Biểu đồ phân tán
                    x_col_index = int(input("\nNhập số thứ tự cột cho trục X: ")) - 1
                    y_col_index = int(input("Nhập số thứ tự cột cho trục Y: ")) - 1

                    if x_col_index < 0 or x_col_index >= len(df.columns) or y_col_index < 0 or y_col_index >= len(
                            df.columns):
                        print("\nSố thứ tự cột không hợp lệ.")
                        input("\nNhấn Enter để tiếp tục...")
                        continue

                    x_col = df.columns[x_col_index]
                    y_col = df.columns[y_col_index]

                    # Vẽ biểu đồ
                    plt.figure(figsize=(10, 6))
                    plt.scatter(df[x_col], df[y_col], alpha=0.5)
                    plt.xlabel(x_col)
                    plt.ylabel(y_col)
                    plt.title(f"Biểu đồ phân tán {y_col} theo {x_col}")
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()

                    # Lưu biểu đồ
                    output_file = os.path.splitext(file_path)[0] + "_scatter_plot.png"
                    plt.savefig(output_file)
                    plt.close()

                    print(f"\nĐã lưu biểu đồ phân tán vào file {output_file}")

                elif chart_type == '5':
                    # Biểu đồ hộp
                    col_indices = input("\nNhập số thứ tự các cột cần vẽ (nhiều lựa chọn, phân cách bằng dấu phẩy): ")
                    selected_indices = [int(x.strip()) - 1 for x in col_indices.split(',') if x.strip().isdigit()]

                    if not selected_indices:
                        print("\nKhông có cột nào được chọn.")
                        input("\nNhấn Enter để tiếp tục...")
                        continue

                    selected_columns = [df.columns[i] for i in selected_indices if 0 <= i < len(df.columns)]

                    # Vẽ biểu đồ
                    plt.figure(figsize=(12, 6))
                    plt.boxplot([df[col] for col in selected_columns], labels=selected_columns)
                    plt.title("Biểu đồ hộp")
                    plt.ylabel("Giá trị")
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()

                    # Lưu biểu đồ
                    output_file = os.path.splitext(file_path)[0] + "_box_plot.png"
                    plt.savefig(output_file)
                    plt.close()

                    print(f"\nĐã lưu biểu đồ hộp vào file {output_file}")

                elif chart_type == '6':
                    # Biểu đồ histogram
                    col_index = int(input("\nNhập số thứ tự cột cho histogram: ")) - 1

                    if col_index < 0 or col_index >= len(df.columns):
                        print("\nSố thứ tự cột không hợp lệ.")
                        input("\nNhấn Enter để tiếp tục...")
                        continue

                    col = df.columns[col_index]

                    # Số lượng bins
                    bins = int(input("\nNhập số lượng bins: ") or "10")

                    # Vẽ biểu đồ
                    plt.figure(figsize=(10, 6))
                    plt.hist(df[col], bins=bins, alpha=0.7, edgecolor='black')
                    plt.xlabel(col)
                    plt.ylabel("Tần suất")
                    plt.title(f"Histogram cho {col}")
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()

                    # Lưu biểu đồ
                    output_file = os.path.splitext(file_path)[0] + "_histogram.png"
                    plt.savefig(output_file)
                    plt.close()

                    print(f"\nĐã lưu histogram vào file {output_file}")

                else:
                    print("\nLựa chọn không hợp lệ.")

            except Exception as e:
                print(f"\nLỗi khi vẽ biểu đồ: {e}")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '4':
            # Phân tích dữ liệu theo thời gian
            file_path = input("\nNhập đường dẫn đến file dữ liệu: ")

            if not os.path.exists(file_path):
                print(f"\nFile {file_path} không tồn tại.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            try:
                # Đọc dữ liệu
                if file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    print("\nĐịnh dạng file không được hỗ trợ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                # Hiển thị thông tin
                print(f"\nĐã đọc dữ liệu từ file {file_path}")
                print(f"Số dòng: {len(df)}")
                print(f"Số cột: {len(df.columns)}")

                # Hiển thị các cột
                print("\nCác cột trong dữ liệu:")
                for i, col in enumerate(df.columns):
                    print(f"{i + 1}. {col}")

                # Chọn cột thời gian
                date_col_index = int(input("\nNhập số thứ tự cột thời gian: ")) - 1

                if date_col_index < 0 or date_col_index >= len(df.columns):
                    print("\nSố thứ tự cột không hợp lệ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                date_col = df.columns[date_col_index]

                # Chuyển đổi cột thời gian sang datetime
                try:
                    df[date_col] = pd.to_datetime(df[date_col])
                except:
                    print(f"\nKhông thể chuyển đổi cột {date_col} sang định dạng datetime.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                # Chọn cột giá trị
                value_col_index = int(input("\nNhập số thứ tự cột giá trị: ")) - 1

                if value_col_index < 0 or value_col_index >= len(df.columns):
                    print("\nSố thứ tự cột không hợp lệ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                value_col = df.columns[value_col_index]

                # Chọn tần suất phân tích
                print("\nChọn tần suất phân tích:")
                print("1. Ngày (D)")
                print("2. Tuần (W)")
                print("3. Tháng (M)")
                print("4. Quý (Q)")
                print("5. Năm (Y)")

                freq_choice = input("\nNhập lựa chọn của bạn: ")

                freq = 'D'
                if freq_choice == '2':
                    freq = 'W'
                elif freq_choice == '3':
                    freq = 'M'
                elif freq_choice == '4':
                    freq = 'Q'
                elif freq_choice == '5':
                    freq = 'Y'

                # Nhóm dữ liệu theo thời gian
                df_grouped = df.groupby(pd.Grouper(key=date_col, freq=freq))[value_col].agg(
                    ['count', 'sum', 'mean', 'min', 'max'])
                df_grouped = df_grouped.reset_index()

                # Hiển thị kết quả
                print("\nKết quả phân tích theo thời gian:")
                print(df_grouped.head())

                # Vẽ biểu đồ
                plt.figure(figsize=(12, 8))

                # Biểu đồ số lượng
                plt.subplot(2, 1, 1)
                plt.plot(df_grouped[date_col], df_grouped['count'], marker='o')
                plt.title(f"Số lượng {value_col} theo thời gian")
                plt.xlabel("Thời gian")
                plt.ylabel("Số lượng")
                plt.grid(True, alpha=0.3)

                # Biểu đồ giá trị trung bình
                plt.subplot(2, 1, 2)
                plt.plot(df_grouped[date_col], df_grouped['mean'], marker='o', color='orange')
                plt.title(f"Giá trị trung bình {value_col} theo thời gian")
                plt.xlabel("Thời gian")
                plt.ylabel("Giá trị trung bình")
                plt.grid(True, alpha=0.3)

                plt.tight_layout()

                # Lưu biểu đồ
                output_chart = os.path.splitext(file_path)[0] + "_time_series.png"
                plt.savefig(output_chart)
                plt.close()

                # Lưu dữ liệu
                output_file = os.path.splitext(file_path)[0] + "_time_series.xlsx"
                df_grouped.to_excel(output_file, index=False)

                print(f"\nĐã lưu kết quả phân tích vào file {output_file}")
                print(f"Đã lưu biểu đồ vào file {output_chart}")

            except Exception as e:
                print(f"\nLỗi khi phân tích dữ liệu theo thời gian: {e}")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '5':
            # Phân tích dữ liệu tin tức
            file_path = input("\nNhập đường dẫn đến file chứa dữ liệu tin tức: ")

            if not os.path.exists(file_path):
                print(f"\nFile {file_path} không tồn tại.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            try:
                # Đọc dữ liệu
                if file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    print("\nĐịnh dạng file không được hỗ trợ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                # Hiển thị thông tin
                print(f"\nĐã đọc dữ liệu từ file {file_path}")
                print(f"Số dòng: {len(df)}")
                print(f"Số cột: {len(df.columns)}")

                # Kiểm tra các cột cần thiết
                required_columns = ['title', 'content']
                missing_columns = [col for col in required_columns if col not in df.columns]

                if missing_columns:
                    print(f"\nFile thiếu các cột cần thiết: {', '.join(missing_columns)}")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                # Phân tích dữ liệu tin tức
                from utils.news_analyzer import NewsAnalyzer

                analyzer = NewsAnalyzer()
                results = analyzer.analyze_news_data(df)

                if results:
                    # Hiển thị kết quả
                    print("\nKết quả phân tích:")

                    if 'word_freq' in results:
                        print("\nCác từ xuất hiện nhiều nhất:")
                        for word, count in results['word_freq'].items():
                            print(f"- {word}: {count}")

                    if 'sentiment' in results:
                        print("\nPhân tích cảm xúc:")
                        print(f"- Tích cực: {results['sentiment']['positive']}%")
                        print(f"- Tiêu cực: {results['sentiment']['negative']}%")
                        print(f"- Trung tính: {results['sentiment']['neutral']}%")

                    if 'topics' in results:
                        print("\nCác chủ đề chính:")
                        for topic in results['topics']:
                            print(f"- {topic}")

                    if 'wordcloud_file' in results:
                        print(f"\nĐã tạo word cloud: {results['wordcloud_file']}")

                    # Lưu kết quả
                    output_file = os.path.splitext(file_path)[0] + "_analysis.xlsx"

                    # Chuyển kết quả thành DataFrame
                    result_data = {
                        'metric': [],
                        'value': []
                    }

                    if 'word_freq' in results:
                        for word, count in results['word_freq'].items():
                            result_data['metric'].append(f"word_freq_{word}")
                            result_data['value'].append(count)

                    if 'sentiment' in results:
                        for sentiment, value in results['sentiment'].items():
                            result_data['metric'].append(f"sentiment_{sentiment}")
                            result_data['value'].append(value)

                    if 'topics' in results:
                        for i, topic in enumerate(results['topics']):
                            result_data['metric'].append(f"topic_{i + 1}")
                            result_data['value'].append(topic)

                    # Lưu kết quả
                    result_df = pd.DataFrame(result_data)
                    result_df.to_excel(output_file, index=False)

                    print(f"\nĐã lưu kết quả phân tích vào file {output_file}")

                else:
                    print("\nKhông thể phân tích dữ liệu tin tức.")

            except Exception as e:
                print(f"\nLỗi khi phân tích dữ liệu tin tức: {e}")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '6':
            # Phân tích dữ liệu tin tức nâng cao
            file_path = input("\nNhập đường dẫn đến file chứa dữ liệu tin tức: ")

            if not os.path.exists(file_path):
                print(f"\nFile {file_path} không tồn tại.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            # Khởi tạo news analyzer nâng cao
            news_analyzer = NewsAnalyzerAdvanced()

            # Đọc dữ liệu
            df = news_analyzer.load_data(file_path)

            if df is not None:
                # Phân tích dữ liệu
                print("\nĐang phân tích dữ liệu tin tức nâng cao...")
                results = news_analyzer.analyze_news_data_advanced(df)

                # Hiển thị kết quả phân tích
                if results:
                    print("\nKết quả phân tích:")

                    if 'wordcloud_file' in results and results['wordcloud_file']:
                        print(f"- Word cloud: {results['wordcloud_file']}")

                    if 'lda_vis_file' in results and results['lda_vis_file']:
                        print(f"- Trực quan hóa LDA: {results['lda_vis_file']}")

                    if 'network_file' in results and results['network_file']:
                        print(f"- Mạng lưới tag: {results['network_file']}")

                    if 'time_trends_file' in results and results['time_trends_file']:
                        print(f"- Xu hướng theo thời gian: {results['time_trends_file']}")

                    if 'length_dist_file' in results and results['length_dist_file']:
                        print(f"- Phân phối độ dài: {results['length_dist_file']}")

            input("\nNhấn Enter để tiếp tục...")

        else:
            print("\nLựa chọn không hợp lệ. Vui lòng thử lại.")
            input("\nNhấn Enter để tiếp tục...")