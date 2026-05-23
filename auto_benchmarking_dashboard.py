import os
import re
import pandas as pd
import numpy as np

def parse_accuracy_metrics(file_path):
    """
    Mục đích: Đọc và trích xuất các chỉ số Recall và NDCG từ file kết quả chấm điểm.
    Ứng dụng: Quét file metric_scores.txt của baseline, dùng Regex (Biểu thức chính quy) 
             để nhặt chính xác các con số sau dấu hai chấm (:).
    """
    metrics = {}
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Tìm các cặp mẫu dạng Metric_Name: Số_Thập_Phân
        pattern = r'([a-zA-Z0-9@]+):\s*([0-9.]+)'
        matches = re.findall(pattern, content)
        for name, value in matches:
            metrics[name] = float(value)
            
    return metrics

def calculate_spatial_logs(analysis_dir):
    """
    Mục đích: Đọc 3 file success.txt, top20.txt, fail.txt để bóc tách lỗi không gian.
    Ứng dụng: 
      - Đếm số lượng dòng của từng file để tính tỷ lệ phần trăm (%) phân bổ kết quả.
      - Trích xuất toàn bộ con số 'Distance: X' trong file top20 và fail để tính toán 
        chính xác Sai số trung bình (Mean) và Sai số trung vị (Median) bằng mét.
    """
    results = {
        'count_success': 0, 'count_top20': 0, 'count_fail': 0,
        'mean_dist': '-', 'median_dist': '-'
    }
    
    success_file = os.path.join(analysis_dir, 'success.txt')
    top20_file = os.path.join(analysis_dir, 'top20.txt')
    fail_file = os.path.join(analysis_dir, 'fail.txt')
    
    # 1. Đếm số câu query trúng phóc Top 1
    if os.path.exists(success_file):
        with open(success_file, 'r', encoding='utf-8') as f:
            results['count_success'] = len(f.readlines())
            
    # 2. Đếm số câu lọt Top 20 và gom các khoảng cách sai lệch
    distances = []
    if os.path.exists(top20_file):
        with open(top20_file, 'r', encoding='utf-8') as f:
            for line in f:
                if 'Query:' in line: # Chỉ lấy dòng chứa thông tin câu query chính
                    results['count_top20'] += 1
                    match = re.search(r'Distance:\s*([0-9.]+)', line)
                    if match:
                        distances.append(float(match.group(1)))
                        
    # 3. Đếm số câu thất bại hoàn toàn (Fail) và gom khoảng cách sai lệch
    if os.path.exists(fail_file):
        with open(fail_file, 'r', encoding='utf-8') as f:
            for line in f:
                if 'Query:' in line:
                    results['count_fail'] += 1
                    match = re.search(r'Distance:\s*([0-9.]+)', line)
                    if match:
                        distances.append(float(match.group(1)))
                        
    # 4. Tính toán thống kê sai số không gian (mét) nếu có dữ liệu lỗi
    if distances:
        results['mean_dist'] = f"{np.mean(distances):.0f}"
        results['median_dist'] = f"{np.median(distances):.0f}"
        
    return results

if __name__ == '__main__':
    csv_path = 'Bảng Tổng Hợp Số Liệu Thực Nghiệm (Benchmarking).csv'
    print("--- Bắt đầu quy trình tự động hóa bóc tách số liệu ---")
    
    # Đọc cấu trúc file CSV hiện tại của bạn vào bộ nhớ dưới dạng DataFrame
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        print(f"Không tìm thấy file {csv_path} tại đây!")
        exit()
        
    # Thiết lập danh sách các hàng mới cần bổ sung vào file CSV
    new_rows = [
        "Recall@10", "Recall@20", "NDCG@1", "NDCG@5",
        "Tỷ lệ Success (%)", "Tỷ lệ Tiệm cận (%)", "Tỷ lệ Fail (%)",
        "Sai số trung bình (m)", "Sai số trung vị (m)"
    ]
    
    # Nếu trong file CSV cũ chưa có các dòng này, tiến hành chèn thêm vào
    for row_name in new_rows:
        if row_name not in df.iloc[:, 0].values:
            empty_row = {df.columns[0]: row_name}
            for col in df.columns[1:]:
                empty_row[col] = '-'
            df = pd.concat([df, pd.DataFrame([empty_row])], ignore_index=True)
            
    # Đặt cột đầu tiên làm Index định danh để dễ dàng điền chuẩn xác dữ liệu theo tọa độ ô
    df.set_index(df.columns[0], inplace=True)
    
    # ==========================================
    # PHẦN 1: TỰ ĐỘNG ĐIỀN CHO BASELINE BERT_D
    # ==========================================
    # Đọc chỉ số từ file metric_scores.txt
    bert_metrics = parse_accuracy_metrics('results/BERT_D/metric_scores.txt')
    if bert_metrics:
        df.at['Recall@10', df.columns[1]] = bert_metrics.get('Recall@10', '-')
        df.at['Recall@20', df.columns[1]] = bert_metrics.get('Recall@20', '-')
        df.at['NDCG@1', df.columns[1]] = bert_metrics.get('NDCG@1', '-')
        df.at['NDCG@5', df.columns[1]] = bert_metrics.get('NDCG@5', '-')
        
    # Đọc log phân tích lỗi từ folder log bạn vừa gom
    bert_logs = calculate_spatial_logs('results/logs/BERT_D_Analysis')
    total_bert = bert_logs['count_success'] + bert_logs['count_top20'] + bert_logs['count_fail']
    if total_bert > 0:
        df.at['Tỷ lệ Success (%)', df.columns[1]] = f"{(bert_logs['count_success']/total_bert)*100:.2f}%"
        df.at['Tỷ lệ Tiệm cận (%)', df.columns[1]] = f"{(bert_logs['count_top20']/total_bert)*100:.2f}%"
        df.at['Tỷ lệ Fail (%)', df.columns[1]] = f"{(bert_logs['count_fail']/total_bert)*100:.2f}%"
        df.at['Sai số trung bình (m)', df.columns[1]] = bert_logs['mean_dist']
        df.at['Sai số trung vị (m)', df.columns[1]] = bert_logs['median_dist']

    # ==========================================
    # PHẦN 2: TỰ ĐỘNG ĐIỀN CHO BASELINE BM25_D
    # ==========================================
    bm25_metrics = parse_accuracy_metrics('results/BM25_D/metric_scores.txt')
    if bm25_metrics:
        df.at['Recall@10', df.columns[0]] = bm25_metrics.get('Recall@10', '-')
        df.at['Recall@20', df.columns[0]] = bm25_metrics.get('Recall@20', '-')
        df.at['NDCG@1', df.columns[0]] = bm25_metrics.get('NDCG@1', '-')
        df.at['NDCG@5', df.columns[0]] = bm25_metrics.get('NDCG@5', '-')
        
    bm25_logs = calculate_spatial_logs('results/logs/BM25_D_Analysis')
    total_bm25 = bm25_logs['count_success'] + bm25_logs['count_top20'] + bm25_logs['count_fail']
    if total_bm25 > 0:
        df.at['Tỷ lệ Success (%)', df.columns[0]] = f"{(bm25_logs['count_success']/total_bm25)*100:.2f}%"
        df.at['Tỷ lệ Tiệm cận (%)', df.columns[0]] = f"{(bm25_logs['count_top20']/total_bm25)*100:.2f}%"
        df.at['Tỷ lệ Fail (%)', df.columns[0]] = f"{(bm25_logs['count_fail']/total_bm25)*100:.2f}%"
        df.at['Sai số trung bình (m)', df.columns[0]] = bm25_logs['mean_dist']
        df.at['Sai số trung vị (m)', df.columns[0]] = bm25_logs['median_dist']

    # ==========================================
    # PHẦN 3: TỰ ĐỘNG ĐIỀN CHO MÔ HÌNH GEOBLOOM
    # ==========================================
    # Quét dữ liệu lỗi từ kết quả analyze.py gốc của GeoBloom (nếu bạn đã chạy và lưu)
    geobloom_logs = calculate_spatial_logs('results/logs/geoglue_clean_unsupervised')
    total_geo = geobloom_logs['count_success'] + geobloom_logs['count_top20'] + geobloom_logs['count_fail']
    if total_geo > 0:
        df.at['Tỷ lệ Success (%)', df.columns[2]] = f"{(geobloom_logs['count_success']/total_geo)*100:.2f}%"
        df.at['Tỷ lệ Tiệm cận (%)', df.columns[2]] = f"{(geobloom_logs['count_top20']/total_geo)*100:.2f}%"
        df.at['Tỷ lệ Fail (%)', df.columns[2]] = f"{(geobloom_logs['count_fail']/total_geo)*100:.2f}%"
        df.at['Sai số trung bình (m)', df.columns[2]] = geobloom_logs['mean_dist']
        df.at['Sai số trung vị (m)', df.columns[2]] = geobloom_logs['median_dist']
        
    # Đưa cột Index quay lại trạng thái bình thường ban đầu và xuất file
    df.reset_index(inplace=True)
    df.to_csv(csv_path, index=False)
    
    print(f"🎉 ĐÃ ĐIỀN HOÀN TẤT VÀ CẬP NHẬT THÀNH CÔNG VÀO FILE: {csv_path}")
