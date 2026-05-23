import os
import numpy as np
from tqdm import trange

def load_text(text_path):
    """
    Mục đích: Đọc file văn bản thô cấu trúc dữ liệu địa lý (poi.txt hoặc test.txt).
    Ứng dụng: Tách chuỗi văn bản, trích xuất tọa độ UTM (X, Y) và danh sách ID đáp án đúng (Ground Truth).
    """
    text = []
    locations = []
    truths = []
    with open(text_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split('\t')
            text.append(line[0])
            utm_lat = float(line[1])
            utm_lon = float(line[2])
            locations.append([utm_lat, utm_lon])
            if len(line) > 3:
                truths.append([int(x) for x in line[3].split(',')])
    return text, locations, truths

def process_baseline_analysis(model_name, dataset, query_text, query_locations, truths, poi_text, poi_locations):
    """
    Mục đích: Hàm cốt lõi chịu trách nhiệm tính toán khoảng cách không gian và phân loại lỗi.
    Ứng dụng: 
      - Đọc file dự đoán .npy của baseline.
      - Duyệt qua từng câu query, tính khoảng cách sai lệch (mét) giữa tọa độ dự đoán Top 1 và tọa độ thật.
      - Phân phối kết quả vào 3 danh sách (Success, Top20, Fail) và xuất ra 3 file .txt tương ứng.
    """
    # Đường dẫn đến file dự đoán .npy của bạn (lùi 2 cấp thư mục ra repo gốc)
    npy_path = f'../results/{model_name}/{dataset}_{model_name}_top100.npy'
    
    if not os.path.exists(npy_path):
        print(f"DEBUG: Không tìm thấy file dự đoán của mô hình tại {npy_path}")
        return

    # Load mảng dự đoán top-100 của baseline
    top100_list = np.load(npy_path)
    num_queries = len(query_text)
    
    case1_lines = [] # Lưu các ca đoán trúng ngay vị trí Top 1
    case2_lines = [] # Lưu các ca đoán trượt Top 1 nhưng trúng trong Top 20
    case3_lines = [] # Lưu các ca đoán sai hoàn toàn (văng khỏi Top 20)

    for i in trange(num_queries, desc=f"Đang bóc tách lỗi không gian cho {model_name}"):
        query_idx = i
        truth_idx = truths[query_idx][0] # ID đáp án đúng thực tế
        
        # Lấy danh sách Top 20 kết quả mà model baseline dự đoán (ép kiểu sang list)
        topk_idx = list(top100_list[query_idx][:20])
        
        # Tính khoảng cách Euclidean hình học (mét) từ người dùng đến vị trí đáp án đúng
        truth_dist = np.sqrt((query_locations[query_idx][0] - poi_locations[truth_idx][0]) ** 2 + 
                             (query_locations[query_idx][1] - poi_locations[truth_idx][1]) ** 2)
        
        # Trường hợp 1: Đoán trúng ngay Top 1
        if truth_idx == topk_idx[0]:
            case1_lines.append(f'Query: {query_text[query_idx]}, Truth: {poi_text[truth_idx]}, Distance: {truth_dist:.0f}')
        else:
            # Kiểm tra xem đáp án đúng có nằm trong Top 20 hay không
            try:
                truth_idx_in_topk = topk_idx.index(truth_idx)
            except ValueError:
                truth_idx_in_topk = -1
                
            if truth_idx_in_topk != -1:
                # Trường hợp 2: Đáp án đúng lọt vào khoảng vị trí từ 2 đến 20
                case2_lines.append(f'Query: {query_text[query_idx]}, Truth: {poi_text[truth_idx]}, Distance: {truth_dist:.0f}')
                for j in range(truth_idx_in_topk):
                    dist = np.sqrt((query_locations[query_idx][0] - poi_locations[topk_idx[j]][0]) ** 2 + 
                                   (query_locations[query_idx][1] - poi_locations[topk_idx[j]][1]) ** 2)
                    case2_lines.append(f'\t- POI: {poi_text[topk_idx[j]]}, Distance: {dist:.0f}')
            else:
                # Trường hợp 3: Đoán sai hoàn toàn, văng khỏi Top 20
                case3_lines.append(f'Query: {query_text[query_idx]}, Truth: {poi_text[truth_idx]}, Distance: {truth_dist:.0f}')
                for j in range(20):
                    dist = np.sqrt((query_locations[query_idx][0] - poi_locations[topk_idx[j]][0]) ** 2 + 
                                   (query_locations[query_idx][1] - poi_locations[topk_idx[j]][1]) ** 2)
                    case3_lines.append(f'\t- POI: {poi_text[topk_idx[j]]}, Distance: {dist:.0f}')

    # Thiết lập thư mục xuất file kết quả (lưu ngược về folder kết quả tương ứng trong repo gốc)
    output_dir = f'../../results/{model_name}_Analysis'
    os.makedirs(output_dir, exist_ok=True)
    
    # Ghi file kết quả tĩnh
    with open(f'{output_dir}/success.txt', 'w', encoding='utf-8') as f:
        for line in case1_lines: f.write(line + '\n')
    with open(f'{output_dir}/top20.txt', 'w', encoding='utf-8') as f:
        for line in case2_lines: f.write(line + '\n')
    with open(f'{output_dir}/fail.txt', 'w', encoding='utf-8') as f:
        for line in case3_lines: f.write(line + '\n')
        
    print(f" Đã xuất thành công bộ 3 file phân tích lỗi vào: {output_dir}\n")

if __name__ == '__main__':
    dataset = 'GeoGLUE_clean'
    
    # Khai báo đường dẫn dữ liệu gốc của dataset (lùi 1 cấp từ vị trí chạy file)
    poi_text_path = f'data/{dataset}/poi.txt'
    query_text_path = f'data/{dataset}/test.txt'
    
    print(f"--- Bắt đầu đọc dữ liệu tập nền {dataset} ---")
    poi_text, poi_locations, _ = load_text(poi_text_path)
    query_text, query_locations, truths = load_text(query_text_path)
    
    # Thực thi tuần lặp bóc tách lỗi cho 2 mô hình baseline
    baselines = ['BM25_D', 'BERT_D']
    for model in baselines:
        process_baseline_analysis(model, dataset, query_text, query_locations, truths, poi_text, poi_locations)
