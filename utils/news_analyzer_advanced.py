#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
News Analyzer Advanced - Phân tích dữ liệu tin tức nâng cao
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import pyLDAvis
import pyLDAvis.sklearn
import networkx as nx
from textblob import TextBlob


class NewsAnalyzerAdvanced:
    """Lớp phân tích dữ liệu tin tức nâng cao"""

    def __init__(self):
        """Khởi tạo"""
        # Đảm bảo thư mục exports tồn tại
        if not os.path.exists('exports'):
            os.makedirs('exports')

        # Đảm bảo thư mục images tồn tại
        if not os.path.exists('images'):
            os.makedirs('images')

        # Tải stopwords tiếng Việt và tiếng Anh
        try:
            self.stop_words = set(stopwords.words('english'))
            # Thêm stopwords tiếng Việt
            vietnamese_stopwords = [
                'và', 'của', 'cho', 'là', 'để', 'trong', 'đã', 'với', 'những', 'được',
                'tại', 'có', 'này', 'từ', 'khi', 'đến', 'không', 'người', 'về', 'năm',
                'phải', 'sẽ', 'vào', 'một', 'các', 'như', 'theo', 'sau', 'nhiều', 'nhưng',
                'trên', 'cũng', 'đó', 'lại', 'nên', 'đang', 'còn', 'bị', 'thì', 'đây',
                'nếu', 'làm', 'chỉ', 'vì', 'mà', 'nói', 'ra', 'hay', 'ngày', 'thể',
                'quá', 'mới', 'cần', 'gì', 'vẫn', 'lên', 'tới', 'tôi', 'ông', 'bà'
            ]
            self.stop_words.update(vietnamese_stopwords)

            # Khởi tạo lemmatizer
            self.lemmatizer = WordNetLemmatizer()
        except:
            print("Không thể tải stopwords. Vui lòng cài đặt nltk và tải dữ liệu cần thiết.")
            self.stop_words = set()
            self.lemmatizer = None

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

    def preprocess_text(self, text):
        """Tiền xử lý văn bản"""
        if not isinstance(text, str):
            return ""

        # Chuyển về chữ thường
        text = text.lower()

        # Loại bỏ dấu câu và số
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)

        # Tokenize
        tokens = word_tokenize(text)

        # Loại bỏ stopwords
        tokens = [token for token in tokens if token not in self.stop_words]

        # Lemmatize
        if self.lemmatizer:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]

        # Loại bỏ từ ngắn
        tokens = [token for token in tokens if len(token) > 2]

        return ' '.join(tokens)

    def analyze_news_data_advanced(self, df):
        """Phân tích dữ liệu tin tức nâng cao"""
        try:
            # Kiểm tra các cột cần thiết
            required_columns = ['title', 'content']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                print(f"Thiếu các cột cần thiết: {', '.join(missing_columns)}")
                return None

            # Tiền xử lý dữ liệu
            df['processed_title'] = df['title'].apply(self.preprocess_text)
            df['processed_content'] = df['content'].apply(self.preprocess_text)

            # Kết hợp tiêu đề và nội dung
            df['processed_text'] = df['processed_title'] + ' ' + df['processed_content']

            # Tạo timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Tạo kết quả
            results = {}

            # 1. Tạo word cloud
            wordcloud_file = self.create_wordcloud(df['processed_text'], timestamp)
            results['wordcloud_file'] = wordcloud_file

            # 2. Phân tích chủ đề với LDA
            lda_vis_file = self.analyze_topics_lda(df['processed_text'], timestamp)
            results['lda_vis_file'] = lda_vis_file

            # 3. Tạo mạng lưới tag
            if 'tags' in df.columns:
                network_file = self.create_tag_network(df['tags'], timestamp)
                results['network_file'] = network_file

            # 4. Phân tích xu hướng theo thời gian
            if 'publish_time' in df.columns:
                time_trends_file = self.analyze_time_trends(df, timestamp)
                results['time_trends_file'] = time_trends_file

            # 5. Phân tích độ dài bài viết
            if 'word_count' in df.columns:
                length_dist_file = self.analyze_article_length(df, timestamp)
                results['length_dist_file'] = length_dist_file

            return results

        except Exception as e:
            print(f"Lỗi khi phân tích dữ liệu tin tức nâng cao: {e}")
            return None

    def create_wordcloud(self, text_series, timestamp):
        """Tạo word cloud từ dữ liệu văn bản"""
        try:
            # Kết hợp tất cả văn bản
            text = ' '.join(text_series.dropna())

            # Tạo word cloud
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                max_words=200,
                contour_width=3,
                contour_color='steelblue'
            ).generate(text)

            # Vẽ word cloud
            plt.figure(figsize=(10, 6))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title('Word Cloud - Các từ xuất hiện nhiều nhất')
            plt.tight_layout()

            # Lưu hình ảnh
            output_file = f"exports/wordcloud_{timestamp}.png"
            plt.savefig(output_file, dpi=300)
            plt.close()

            return output_file

        except Exception as e:
            print(f"Lỗi khi tạo word cloud: {e}")
            return None

    def analyze_topics_lda(self, text_series, timestamp, num_topics=5):
        """Phân tích chủ đề với LDA (Latent Dirichlet Allocation)"""
        try:
            # Tạo ma trận tần suất từ
            vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=1000)
            X = vectorizer.fit_transform(text_series.dropna())

            # Tạo mô hình LDA
            lda = LatentDirichletAllocation(
                n_components=num_topics,
                max_iter=10,
                learning_method='online',
                random_state=42
            )

            # Huấn luyện mô hình
            lda.fit(X)

            # Trực quan hóa LDA
            vis_data = pyLDAvis.sklearn.prepare(lda, X, vectorizer)

            # Lưu trực quan hóa
            output_file = f"exports/lda_vis_{timestamp}.html"
            pyLDAvis.save_html(vis_data, output_file)

            # Hiển thị các từ hàng đầu trong mỗi chủ đề
            feature_names = vectorizer.get_feature_names_out()

            plt.figure(figsize=(12, 8))

            for topic_idx, topic in enumerate(lda.components_):
                top_words_idx = topic.argsort()[:-11:-1]
                top_words = [feature_names[i] for i in top_words_idx]
                top_weights = [topic[i] for i in top_words_idx]

                plt.subplot(2, 3, topic_idx + 1)
                plt.bar(top_words, top_weights)
                plt.xticks(rotation=45, ha='right')
                plt.title(f'Chủ đề {topic_idx + 1}')
                plt.tight_layout()

            # Lưu hình ảnh
            topics_file = f"exports/topics_{timestamp}.png"
            plt.savefig(topics_file, dpi=300)
            plt.close()

            return output_file

        except Exception as e:
            print(f"Lỗi khi phân tích chủ đề với LDA: {e}")
            return None

    def create_tag_network(self, tags_series, timestamp):
        """Tạo mạng lưới tag"""
        try:
            # Tạo danh sách tất cả các tag
            all_tags = []

            for tags_list in tags_series:
                if isinstance(tags_list, list):
                    all_tags.extend(tags_list)

            if not all_tags:
                return None

            # Đếm tần suất của mỗi tag
            tag_counts = {}
            for tag in all_tags:
                if tag in tag_counts:
                    tag_counts[tag] += 1
                else:
                    tag_counts[tag] = 1

            # Tạo đồ thị
            G = nx.Graph()

            # Thêm các node (tag)
            for tag, count in tag_counts.items():
                G.add_node(tag, size=count)

            # Thêm các cạnh (mối quan hệ giữa các tag)
            for tags_list in tags_series:
                if isinstance(tags_list, list) and len(tags_list) > 1:
                    for i in range(len(tags_list)):
                        for j in range(i + 1, len(tags_list)):
                            tag1 = tags_list[i]
                            tag2 = tags_list[j]

                            if G.has_edge(tag1, tag2):
                                G[tag1][tag2]['weight'] += 1
                            else:
                                G.add_edge(tag1, tag2, weight=1)

            # Vẽ đồ thị
            plt.figure(figsize=(12, 10))

            # Tính toán layout
            pos = nx.spring_layout(G, k=0.3)

            # Vẽ các node
            node_sizes = [G.nodes[node]['size'] * 100 for node in G.nodes]
            nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='skyblue', alpha=0.8)

            # Vẽ các cạnh
            edge_weights = [G[u][v]['weight'] for u, v in G.edges]
            nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5, edge_color='gray')

            # Vẽ nhãn
            nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

            plt.title('Mạng lưới các tag')
            plt.axis('off')
            plt.tight_layout()

            # Lưu hình ảnh
            output_file = f"exports/tag_network_{timestamp}.png"
            plt.savefig(output_file, dpi=300)
            plt.close()

            return output_file

        except Exception as e:
            print(f"Lỗi khi tạo mạng lưới tag: {e}")
            return None

    def analyze_time_trends(self, df, timestamp):
        """Phân tích xu hướng theo thời gian"""
        try:
            # Kiểm tra cột thời gian
            if 'publish_time' not in df.columns:
                return None

            # Chuyển đổi cột thời gian sang datetime nếu cần
            if not pd.api.types.is_datetime64_any_dtype(df['publish_time']):
                df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

            # Nhóm dữ liệu theo ngày
            df_grouped = df.groupby(pd.Grouper(key='publish_time', freq='D')).size().reset_index(name='count')

            # Vẽ biểu đồ
            plt.figure(figsize=(12, 6))
            plt.plot(df_grouped['publish_time'], df_grouped['count'], marker='o', linestyle='-')
            plt.title('Số lượng bài viết theo thời gian')
            plt.xlabel('Ngày')
            plt.ylabel('Số lượng bài viết')
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Lưu hình ảnh
            output_file = f"exports/time_trends_{timestamp}.png"
            plt.savefig(output_file, dpi=300)
            plt.close()

            return output_file

        except Exception as e:
            print(f"Lỗi khi phân tích xu hướng theo thời gian: {e}")
            return None

    def analyze_article_length(self, df, timestamp):
        """Phân tích độ dài bài viết"""
        try:
            # Kiểm tra cột word_count
            if 'word_count' not in df.columns:
                return None

            # Vẽ biểu đồ phân phối độ dài
            plt.figure(figsize=(10, 6))

            # Histogram
            plt.hist(df['word_count'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            plt.title('Phân phối độ dài bài viết')
            plt.xlabel('Số từ')
            plt.ylabel('Số lượng bài viết')
            plt.grid(True, alpha=0.3)

            # Thêm thông tin thống kê
            avg_length = df['word_count'].mean()
            median_length = df['word_count'].median()
            max_length = df['word_count'].max()
            min_length = df['word_count'].min()

            plt.axvline(avg_length, color='red', linestyle='--', label=f'Trung bình: {avg_length:.0f} từ')
            plt.axvline(median_length, color='green', linestyle='--', label=f'Trung vị: {median_length:.0f} từ')

            plt.legend()
            plt.tight_layout()

            # Lưu hình ảnh
            output_file = f"exports/length_distribution_{timestamp}.png"
            plt.savefig(output_file, dpi=300)
            plt.close()

            return output_file

        except Exception as e:
            print(f"Lỗi khi phân tích độ dài bài viết: {e}")
            return None

    def analyze_sentiment(self, text_series):
        """Phân tích cảm xúc của văn bản"""
        try:
            sentiments = []

            for text in text_series:
                if isinstance(text, str) and text.strip():
                    blob = TextBlob(text)
                    polarity = blob.sentiment.polarity

                    if polarity > 0.1:
                        sentiment = 'positive'
                    elif polarity < -0.1:
                        sentiment = 'negative'
                    else:
                        sentiment = 'neutral'

                    sentiments.append({
                        'text': text[:100] + '...' if len(text) > 100 else text,
                        'polarity': polarity,
                        'sentiment': sentiment
                    })

            # Tạo DataFrame
            df_sentiment = pd.DataFrame(sentiments)

            # Tính tỷ lệ các loại cảm xúc
            if not df_sentiment.empty:
                sentiment_counts = df_sentiment['sentiment'].value_counts()
                total = len(df_sentiment)

                sentiment_percentages = {
                    'positive': (sentiment_counts.get('positive', 0) / total) * 100,
                    'neutral': (sentiment_counts.get('neutral', 0) / total) * 100,
                    'negative': (sentiment_counts.get('negative', 0) / total) * 100
                }

                return {
                    'sentiment_data': df_sentiment,
                    'sentiment_percentages': sentiment_percentages
                }

            return None

        except Exception as e:
            print(f"Lỗi khi phân tích cảm xúc: {e}")
            return None

    def cluster_articles(self, df, num_clusters=5):
        """Phân cụm các bài viết"""
        try:
            # Kiểm tra cột processed_text
            if 'processed_text' not in df.columns:
                df['processed_text'] = df['title'].apply(self.preprocess_text) + ' ' + df['content'].apply(
                    self.preprocess_text)

            # Tạo ma trận TF-IDF
            vectorizer = TfidfVectorizer(max_features=1000)
            X = vectorizer.fit_transform(df['processed_text'].dropna())

            # Phân cụm với K-means
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            df['cluster'] = kmeans.fit_predict(X)

            # Tìm các từ đặc trưng cho mỗi cụm
            feature_names = vectorizer.get_feature_names_out()
            cluster_centers = kmeans.cluster_centers_

            cluster_keywords = {}

            for i in range(num_clusters):
                # Lấy các từ đặc trưng nhất của cụm
                top_indices = cluster_centers[i].argsort()[-10:][::-1]
                top_features = [feature_names[j] for j in top_indices]

                cluster_keywords[i] = top_features

            return {
                'clustered_data': df,
                'cluster_keywords': cluster_keywords
            }

        except Exception as e:
            print(f"Lỗi khi phân cụm bài viết: {e}")
            return None