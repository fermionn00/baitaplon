#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Excel Menu - Menu xử lý file Excel
"""

import os
import pandas as pd
from utils.common import clear_screen, print_header


def show_excel_menu():
    """Hiển thị menu xử lý file Excel"""
    while True:
        clear_screen()
        print_header("XỬ LÝ FILE EXCEL")
        print("\n1. Đọc file Excel")
        print("2. Gộp nhiều file Excel")
        print("3. Chuyển đổi định dạng")
        print("4. Lọc dữ liệu")
        print("5. Sắp xếp dữ liệu")
        print("0. Quay lại")

        choice = input("\nNhập lựa chọn của bạn: ")

        if choice == '0':
            break

        elif choice == '1':
            # Đọc file Excel
            file_path = input("\nNhập đường dẫn đến file Excel: ")

            if not os.path.exists(file_path):
                print(f"\nFile {file_path} không tồn tại.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            try:
                # Đọc file Excel
                df = pd.read_excel(file_path)

                # Hiển thị thông tin
                print(f"\nĐã đọc file {file_path}")
                print(f"Số dòng: {len(df)}")
                print(f"Số cột: {len(df.columns)}")
                print("\nCác cột trong file:")
                for col in df.columns:
                    print(f"- {col}")

                # Hiển thị dữ liệu
                print("\nDữ liệu (5 dòng đầu tiên):")
                print(df.head())

                # Lưu dữ liệu
                save_choice = input("\nBạn có muốn lưu dữ liệu ra file khác không? (y/n): ")
                if save_choice.lower() == 'y':
                    output_format = input("\nChọn định dạng xuất (excel/csv/json): ").lower()
                    output_file = input("Nhập tên file xuất: ")

                    if output_format == 'excel':
                        df.to_excel(output_file, index=False)
                    elif output_format == 'csv':
                        df.to_csv(output_file, index=False)
                    elif output_format == 'json':
                        df.to_json(output_file, orient='records')
                    else:
                        print("\nĐịnh dạng không hợp lệ.")
                        input("\nNhấn Enter để tiếp tục...")
                        continue

                    print(f"\nĐã lưu dữ liệu vào file {output_file}")

            except Exception as e:
                print(f"\nLỗi khi đọc file Excel: {e}")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '2':
            # Gộp nhiều file Excel
            folder_path = input("\nNhập đường dẫn đến thư mục chứa các file Excel: ")

            if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
                print(f"\nThư mục {folder_path} không tồn tại.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            # Lấy danh sách file Excel trong thư mục
            excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') or f.endswith('.xls')]

            if not excel_files:
                print(f"\nKhông tìm thấy file Excel nào trong thư mục {folder_path}.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            print("\nDanh sách file Excel:")
            for i, file in enumerate(excel_files):
                print(f"{i + 1}. {file}")

            # Chọn các file cần gộp
            file_indices = input("\nNhập số thứ tự các file cần gộp (nhiều lựa chọn, phân cách bằng dấu phẩy): ")
            selected_indices = [int(x.strip()) - 1 for x in file_indices.split(',') if x.strip().isdigit()]

            if not selected_indices:
                print("\nKhông có file nào được chọn.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            selected_files = [excel_files[i] for i in selected_indices if 0 <= i < len(excel_files)]

            if not selected_files:
                print("\nKhông có file nào hợp lệ được chọn.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            try:
                # Gộp các file Excel
                dfs = []
                for file in selected_files:
                    file_path = os.path.join(folder_path, file)
                    df = pd.read_excel(file_path)
                    dfs.append(df)

                # Gộp các DataFrame
                merged_df = pd.concat(dfs, ignore_index=True)

                # Hiển thị thông tin
                print(f"\nĐã gộp {len(selected_files)} file Excel")
                print(f"Số dòng: {len(merged_df)}")
                print(f"Số cột: {len(merged_df.columns)}")

                # Lưu dữ liệu
                output_file = input("\nNhập tên file xuất: ")
                merged_df.to_excel(output_file, index=False)

                print(f"\nĐã lưu dữ liệu vào file {output_file}")

            except Exception as e:
                print(f"\nLỗi khi gộp file Excel: {e}")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '3':
            # Chuyển đổi định dạng
            file_path = input("\nNhập đường dẫn đến file dữ liệu: ")

            if not os.path.exists(file_path):
                print(f"\nFile {file_path} không tồn tại.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            try:
                # Đọc dữ liệu
                if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                    df = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_path.endswith('.json'):
                    df = pd.read_json(file_path)
                else:
                    print("\nĐịnh dạng file không được hỗ trợ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                # Hiển thị thông tin
                print(f"\nĐã đọc file {file_path}")
                print(f"Số dòng: {len(df)}")
                print(f"Số cột: {len(df.columns)}")

                # Chọn định dạng xuất
                print("\nChọn định dạng xuất:")
                print("1. Excel (.xlsx)")
                print("2. CSV (.csv)")
                print("3. JSON (.json)")
                print("4. HTML (.html)")

                format_choice = input("\nNhập lựa chọn của bạn: ")

                # Nhập tên file xuất
                output_file = input("\nNhập tên file xuất: ")

                # Xuất dữ liệu
                if format_choice == '1':
                    df.to_excel(output_file, index=False)
                elif format_choice == '2':
                    df.to_csv(output_file, index=False)
                elif format_choice == '3':
                    df.to_json(output_file, orient='records')
                elif format_choice == '4':
                    df.to_html(output_file, index=False)
                else:
                    print("\nLựa chọn không hợp lệ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                print(f"\nĐã chuyển đổi và lưu dữ liệu vào file {output_file}")

            except Exception as e:
                print(f"\nLỗi khi chuyển đổi định dạng: {e}")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '4':
            # Lọc dữ liệu
            file_path = input("\nNhập đường dẫn đến file dữ liệu: ")

            if not os.path.exists(file_path):
                print(f"\nFile {file_path} không tồn tại.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            try:
                # Đọc dữ liệu
                if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                    df = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    print("\nĐịnh dạng file không được hỗ trợ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                # Hiển thị thông tin
                print(f"\nĐã đọc file {file_path}")
                print(f"Số dòng: {len(df)}")
                print(f"Số cột: {len(df.columns)}")

                # Hiển thị các cột
                print("\nCác cột trong dữ liệu:")
                for i, col in enumerate(df.columns):
                    print(f"{i + 1}. {col}")

                # Chọn cột để lọc
                col_index = int(input("\nNhập số thứ tự cột cần lọc: ")) - 1

                if col_index < 0 or col_index >= len(df.columns):
                    print("\nSố thứ tự cột không hợp lệ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                col_name = df.columns[col_index]

                # Chọn loại lọc
                print("\nChọn loại lọc:")
                print("1. Bằng (=)")
                print("2. Lớn hơn (>)")
                print("3. Nhỏ hơn (<)")
                print("4. Lớn hơn hoặc bằng (>=)")
                print("5. Nhỏ hơn hoặc bằng (<=)")
                print("6. Khác (!=)")
                print("7. Chứa (contains)")
                print("8. Bắt đầu bằng (startswith)")
                print("9. Kết thúc bằng (endswith)")

                filter_type = input("\nNhập lựa chọn của bạn: ")

                # Nhập giá trị lọc
                filter_value = input("\nNhập giá trị lọc: ")

                # Lọc dữ liệu
                if filter_type == '1':
                    filtered_df = df[df[col_name] == filter_value]
                elif filter_type == '2':
                    filtered_df = df[df[col_name] > float(filter_value)]
                elif filter_type == '3':
                    filtered_df = df[df[col_name] < float(filter_value)]
                elif filter_type == '4':
                    filtered_df = df[df[col_name] >= float(filter_value)]
                elif filter_type == '5':
                    filtered_df = df[df[col_name] <= float(filter_value)]
                elif filter_type == '6':
                    filtered_df = df[df[col_name] != filter_value]
                elif filter_type == '7':
                    filtered_df = df[df[col_name].astype(str).str.contains(filter_value)]
                elif filter_type == '8':
                    filtered_df = df[df[col_name].astype(str).str.startswith(filter_value)]
                elif filter_type == '9':
                    filtered_df = df[df[col_name].astype(str).str.endswith(filter_value)]
                else:
                    print("\nLựa chọn không hợp lệ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                # Hiển thị kết quả
                print(f"\nĐã lọc dữ liệu: {len(df)} dòng -> {len(filtered_df)} dòng")

                if not filtered_df.empty:
                    print("\nDữ liệu sau khi lọc (5 dòng đầu tiên):")
                    print(filtered_df.head())

                    # Lưu kết quả
                    save_choice = input("\nBạn có muốn lưu kết quả không? (y/n): ")
                    if save_choice.lower() == 'y':
                        output_file = input("\nNhập tên file xuất: ")
                        filtered_df.to_excel(output_file, index=False)
                        print(f"\nĐã lưu kết quả vào file {output_file}")
                else:
                    print("\nKhông có dữ liệu nào thỏa mãn điều kiện lọc.")

            except Exception as e:
                print(f"\nLỗi khi lọc dữ liệu: {e}")

            input("\nNhấn Enter để tiếp tục...")

        elif choice == '5':
            # Sắp xếp dữ liệu
            file_path = input("\nNhập đường dẫn đến file dữ liệu: ")

            if not os.path.exists(file_path):
                print(f"\nFile {file_path} không tồn tại.")
                input("\nNhấn Enter để tiếp tục...")
                continue

            try:
                # Đọc dữ liệu
                if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                    df = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    print("\nĐịnh dạng file không được hỗ trợ.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                # Hiển thị thông tin
                print(f"\nĐã đọc file {file_path}")
                print(f"Số dòng: {len(df)}")
                print(f"Số cột: {len(df.columns)}")

                # Hiển thị các cột
                print("\nCác cột trong dữ liệu:")
                for i, col in enumerate(df.columns):
                    print(f"{i + 1}. {col}")

                # Chọn cột để sắp xếp
                col_indices = input("\nNhập số thứ tự các cột cần sắp xếp (nhiều lựa chọn, phân cách bằng dấu phẩy): ")
                selected_indices = [int(x.strip()) - 1 for x in col_indices.split(',') if x.strip().isdigit()]

                if not selected_indices:
                    print("\nKhông có cột nào được chọn.")
                    input("\nNhấn Enter để tiếp tục...")
                    continue

                selected_columns = [df.columns[i] for i in selected_indices if 0 <= i < len(df.columns)]

                # Chọn thứ tự sắp xếp
                print("\nChọn thứ tự sắp xếp:")
                print("1. Tăng dần")
                print("2. Giảm dần")

                order_choice = input("\nNhập lựa chọn của bạn: ")

                ascending = True
                if order_choice == '2':
                    ascending = False

                # Sắp xếp dữ liệu
                sorted_df = df.sort_values(by=selected_columns, ascending=ascending)

                # Hiển thị kết quả
                print("\nDữ liệu sau khi sắp xếp (5 dòng đầu tiên):")
                print(sorted_df.head())

                # Lưu kết quả
                save_choice = input("\nBạn có muốn lưu kết quả không? (y/n): ")
                if save_choice.lower() == 'y':
                    output_file = input("\nNhập tên file xuất: ")
                    sorted_df.to_excel(output_file, index=False)
                    print(f"\nĐã lưu kết quả vào file {output_file}")

            except Exception as e:
                print(f"\nLỗi khi sắp xếp dữ liệu: {e}")

            input("\nNhấn Enter để tiếp tục...")

        else:
            print("\nLựa chọn không hợp lệ. Vui lòng thử lại.")
            input("\nNhấn Enter để tiếp tục...")