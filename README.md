# Thử nghiệm GeoBloom

Dự án này chứa mã nguồn, dữ liệu đánh giá và kết quả thực nghiệm phục vụ đồ án/nghiên cứu về mô hình không gian GeoBloom.

## 📂 Cấu trúc thư mục hiện tại

- `GeoBloom_Source/`: Chứa toàn bộ mã nguồn gốc từ tác giả.
- `models/`: Lưu trữ trọng số (checkpoints) của mô hình sau khi huấn luyện.
- `results/`: Nơi chứa kết quả dạng vector, embeddings và dữ liệu so sánh (BM25, BERT, GeoBloom_Supervised).
- `Unsupervised_result/`: Chứa báo cáo kết quả chạy không giám sát (bao gồm Điểm số, QPS và RAM).
- `notebooks/`, `evaluation/`, `reports/`: Các không gian làm việc chuẩn bị cho phân tích thực nghiệm và viết báo cáo.

*Lưu ý: Các file dữ liệu thô (.txt) và file nén nhị phân (.bin) có dung lượng >100MB đã được loại trừ thông qua `.gitignore` để đảm bảo giới hạn băng thông của GitHub.*
