import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập font và style cấu hình hiển thị trực quan
sns.set_theme(style="darkgrid")
plt.rcParams['font.family'] = 'DejaVu Sans' # Tránh lỗi hiển thị ký tự đặc biệt
plt.rcParams['axes.unicode_minus'] = False

# ==============================================================================
# HÀM 1: BIỂU ĐỒ CỘT GHÉP ĐO ĐỘ CHÍNH XÁC (ACCURACY METRICS)
# ==============================================================================
def draw_accuracy_chart(ax):
    """
    Vẽ biểu đồ cột ghép so sánh Recall và NDCG giữa 3 mô hình
    """
    # Số liệu thực tế trích xuất từ các phiên chạy của bạn
    metrics = ['Recall@10', 'Recall@20', 'NDCG@1', 'NDCG@5']
    bm25 = [0.4253, 0.4958, 0.2107, 0.2904]
    bert = [0.1472, 0.1793, 0.0518, 0.0846]
    geobloom = [0.7354, 0.7909, 0.4278, 0.5563] # Lấy số liệu test mới nhất của bạn
    
    x = np.arange(len(metrics))
    width = 0.25
    
    ax.bar(x - width, bm25, width, label='BM25-D (Truyền thống)', color='#7f8c8d')
    ax.bar(x, bert, width, label='BERT-D (Học sâu)', color='#bdc3c7')
    ax.bar(x + width, geobloom, width, label='GeoBloom (Đề xuất - v19)', color='#2e7d32')
    
    ax.set_title('1. Chỉ Số Chất Lượng Truy Vấn (Accuracy Metrics)', fontsize=12, fontweight='bold', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=10)
    ax.set_ylabel('Giá trị phân bách phân', fontsize=10)
    ax.set_ylim(0, 1.0)
    ax.legend(fontsize=9, loc='upper left')

# ==============================================================================
# HÀM 2: BIỂU ĐỒ TRÒN PHÂN PHỐI LỖI KHÔNG GIAN (SPATIAL ERROR PIE CHART)
# ==============================================================================
def draw_spatial_pie_chart(ax):
    """
    Vẽ biểu đồ tròn thể hiện tỷ lệ phân phối chất lượng định vị của GeoBloom
    """
    labels = ['Success (Top 1)', 'Tiệm cận (Top 2-20)', 'Fail (> Top 20)']
    sizes = [23.68, 29.32, 47.00] # Số liệu thực tế trong file Benchmarking của bạn
    colors = ['#4caf50', '#ffeb3b', '#f44336']
    explode = (0.05, 0, 0)  # Nổi bật miếng bánh Success
    
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.2f%%',
           shadow=False, startangle=140, textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax.set_title('2. Tỷ Lệ Phân Phối Lỗi Không Gian (GeoBloom)', fontsize=12, fontweight='bold', pad=15)

# ==============================================================================
# HÀM 3: BIỂU ĐỒ CỘT ĐƠN ĐO BIÊN ĐỘ LỆCH KHOẢNG CÁCH (DISTANCE ERROR BAR CHART)
# ==============================================================================
def draw_distance_error_chart(ax):
    """
    Vẽ biểu đồ cột so sánh sai số trung bình và sai số trung vị bằng mét
    """
    categories = ['Sai số trung bình (Mean)', 'Sai số trung vị (Median)']
    values = [11610, 912] # Số liệu hình học thực tế của GeoBloom
    
    bars = ax.bar(categories, values, color=['#e65100', '#ffb74d'], width=0.5)
    
    # Hiển thị số liệu mét trên đầu cột
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:,} m',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
                    
    ax.set_title('3. Biên Độ Lệch Khoảng Cách Định Vị Lỗi', fontsize=12, fontweight='bold', pad=10)
    ax.set_ylabel('Khoảng cách sai số (Mét)', fontsize=10)
    ax.set_ylim(0, max(values) * 1.15)

# ==============================================================================
# HÀM 4: BẢNG SO SÁNH HIỆU NĂNG TÀI NGUYÊN (SYSTEM EFFICIENCY TEXT TABLE)
# ==============================================================================
def draw_efficiency_table(ax):
    """
    Vẽ bảng dữ liệu so sánh Thời gian, Tốc độ QPS và Ổ cứng (Không có dòng RAM)
    """
    ax.axis('off') # Ẩn hệ trục tọa độ để dựng bảng text thuần túy
    
    data = [
        ["Tiêu chí Đánh giá", "BM25-D", "BERT-D", "GeoBloom (v19)"],
        ["Thời gian Test", "18072.20s (~5h)", "1033.29s (~17m)", "105.63s (~1m45s)"],
        ["Tốc độ (QPS)", "0.673 QPS", "11.765 QPS", "115.086 QPS"],
        ["Dung lượng đĩa (Disk)", "-", "-", "22.05 MB"]
    ]
    
    table = ax.table(cellText=data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_font_size(10)
    table.scale(1.0, 2.3) # Giãn dòng bảng cho đẹp, dễ đọc
    
    # Định dạng highlight tiêu đề và cột mô hình đề xuất
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#2c3e50')
        if col == 3 and row > 0:
            cell.set_text_props(weight='bold', color='#1b5e20')
            cell.set_facecolor('#e8f5e9')
            
    ax.set_title('4. Bảng So Sánh Hiệu Năng & Tài Nguyên Hệ Thống', fontsize=12, fontweight='bold', pad=5)

# ==============================================================================
# HÀM 5: BIỂU ĐỒ ĐƯỜNG ĐỘ ỔN ĐỊNH VỚI DỮ LIỆU THIẾU HỤT (ROBUSTNESS LINE CHART)
# ==============================================================================
def draw_robustness_line_chart(ax):
    """
    Vẽ biểu đồ đường tuyến tính thể hiện độ ổn định Recall@20 dựa trên dữ liệu Varying Data
    """
    portions = ['2%', '5%', '10%', '20%', '30%', '50%', '70%']
    recall_20 = [0.5616, 0.7002, 0.7276, 0.7520, 0.7598, 0.7763, 0.7828] # Lấy từ file varying_data_results của bạn
    
    ax.plot(portions, recall_20, marker='o', linestyle='-', color='#0d47a1', linewidth=2.5, markersize=8, label='GeoBloom (v19)')
    
    # Hiển thị số liệu điểm số tại mỗi nút tọa độ
    for i, txt in enumerate(recall_20):
        ax.annotate(f'{txt*100:.2f}%', (portions[i], recall_20[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, fontweight='bold', color='#0d47a1')
        
    ax.set_title('5. Độ Ổn Định Thuật Toán Khí Thiếu Hụt Dữ Liệu Huấn Luyện (Robustness)', fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel('Tỷ lệ phần trăm dữ liệu huấn luyện (Portion)', fontsize=10)
    ax.set_ylabel('Điểm chất lượng Recall@20', fontsize=10)
    ax.set_ylim(0.4, 0.9)

# ==============================================================================
# HÀM MAIN: KHỞI TẠO CANVAS, GHÉP CÁC BIỂU ĐỒ VÀ XUẤT FILE .PNG
# ==============================================================================
def main():
    # 1. Định nghĩa đường dẫn lưu file mục tiêu
    target_folder = os.path.expanduser('~/ThucNghiemGeoBloom')
    os.makedirs(target_folder, exist_ok=True)
    output_png_path = os.path.join(target_folder, 'dashboard_experimental_summary.png')
    
    # 2. Khởi tạo một lưới đồ họa Canvas lớn (Kích thước 16x12 inches, gồm 3 hàng, 2 cột)
    fig = plt.figure(figsize=(16, 12))
    
    # Thiết lập lưới vị trí (Grid Spec Layout)
    grid = plt.GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.25)
    
    ax1 = fig.add_subplot(grid[0, 0]) # Hàng 0, Cột 0 -> Vẽ Accuracy Bar Chart
    ax2 = fig.add_subplot(grid[0, 1]) # Hàng 0, Cột 1 -> Vẽ Pie Chart Phân phối lỗi
    ax3 = fig.add_subplot(grid[1, 0]) # Hàng 1, Cột 0 -> Vẽ Distance Error
    ax4 = fig.add_subplot(grid[1, 1]) # Hàng 1, Cột 1 -> Vẽ Bảng Tĩnh Tài Nguyên Efficiency
    ax5 = fig.add_subplot(grid[2, :]) # Hàng 2, Chiếm trọn cả 2 cột -> Vẽ Đồ thị đường Robustness trải dài
    
    # 3. Kích hoạt gọi lệnh vẽ tuần tự từ 5 hàm độc lập
    draw_accuracy_chart(ax1)
    draw_spatial_pie_chart(ax2)
    draw_distance_error_chart(ax3)
    draw_efficiency_table(ax4)
    draw_robustness_line_chart(ax5)
    
    # 4. Thêm Tiêu đề tổng của toàn bộ bức ảnh Dashboard
    fig.suptitle('BÁO CÁO TỔNG HỢP KẾT QUẢ THỰC NGHIỆM THUẬT TOÁN GEOBLOOM (VLDB 2025)', 
                 fontsize=16, fontweight='bold', y=0.96, color='#1a237e')
    
    # Thêm dòng chú thích khoa học nhỏ ở chân trang
    fig.text(0.1, 0.02, '* Chú thích: Chỉ số dung lượng đĩa cứng (Disk) của các mô hình baseline hiển thị trống (-) do không có công cụ đo lường đồng bộ nhất quán từ mã nguồn của tác giả.', 
             fontsize=9, style='italic', color='#555555')
    
    # 5. Lưu đồ họa thành file ảnh tĩnh định dạng PNG sắc nét
    plt.savefig(output_png_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"🎉 Xuất Dashboard thành công! File ảnh tổng hợp đã được lưu tại: {output_png_path}")

if __name__ == '__main__':
    main()