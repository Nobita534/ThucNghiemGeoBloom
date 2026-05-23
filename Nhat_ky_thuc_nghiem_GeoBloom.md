# NHẬT KÝ THỰC NGHIỆM VÀ PHÂN TÍCH HỆ THỐNG GEOBLOOM

---

## 1. Tổng quan bài báo

- **Bài báo giải quyết vấn đề gì?** Bài báo giải quyết bài toán định vị địa điểm (POI Retrieval - Toponym Resolution) từ các câu truy vấn văn bản thô dựa trên sự kết hợp giữa thông tin Không gian (Spatial) và Văn bản (Text).
- **Case study / Bối cảnh sử dụng:** Tìm kiếm và định vị chính xác vị trí của một địa điểm dựa trên các chuỗi tìm kiếm bản địa chứa thông tin mơ hồ, nhiễu từ khóa phụ hoặc mốc giao thông.
- **Vì sao vấn đề này quan trọng?** Định vị POI Unsupervised truyền thống thường bị nhiễu bởi các từ khóa định hướng hoặc thực thể giao thông xung quanh, làm lệch kết quả ở cự ly gần hoặc đoán sai vùng địa lý hoàn toàn.
- **Điểm nổi bật của phương pháp:** Mô hình đề xuất cấu trúc kết hợp cây chỉ mục K-Means, bộ lọc Bloom Filters và mạng nơ-ron NNUE để tối ưu hóa đồng thời độ chính xác không gian và tốc độ xử lý câu hỏi.

---

## 2. Tổng quan repository ThucNghiemGeoBloom

- **Mục đích:** Repository `ThucNghiemGeoBloom` do người dùng thiết lập nhằm mục đích lưu trữ cấu trúc kịch bản thực nghiệm cá nhân, quản lý tập trung các kết quả đầu ra (outputs), tổ chức các notebook chạy thực nghiệm trên Cloud (Kaggle) và máy cục bộ (Local), phục vụ công tác trực quan hóa và phân tích sâu dữ liệu bài báo.
- **Cấu trúc và các thành phần chính:**
  - Thư mục `results/`: Trung tâm lưu trữ toàn bộ dữ liệu log thực thi (Unsupervised/Supervised), tệp chỉ mục cấu trúc cây (`tree.bin`), và các file phân tích dữ liệu thành công/thất bại sau kịch bản chạy.
  - Thư mục `notebooks/`: Chứa các tệp Jupyter Notebook (`.ipynb`) dùng để cấu hình và thực thi mã nguồn baseline đối chứng trên môi trường Kaggle, cùng các kịch bản chạy thử nghiệm và trực quan hóa phân tích lỗi.
  - Thư mục `GeoBloom_Source/`: Mã nguồn thực thi cốt lõi được clone trực tiếp từ gốc của tác giả để triển khai gọi module thực nghiệm cục bộ.

---

## 3. Dataset Analysis

- **Các bộ dữ liệu đã dùng:** `GeoGLUE`, `GeoGLUE_clean`, `Beijing`, `Shanghai`, `Synthetic`.
- **Ý nghĩa từng dataset:** Các bộ dữ liệu địa lý đô thị thực tế dùng để huấn luyện và kiểm thử khả năng tìm kiếm POI lân cận.
- **Dataset quan trọng nhất & Đã thực nghiệm:** `GeoGLUE_clean`.
- **Format dữ liệu:** Dạng văn bản phân tách bằng ký tự Tab (`\t`), trong đó cột thứ 4 chứa chuỗi ID đáp án đúng (`Ground Truth`) cách nhau bởi dấu phẩy.
- **Kích thước dữ liệu:** Tập kiểm thử chứa **12,000 queries**.

---

## 4. Quá trình setup & thực nghiệm

### Giai đoạn 1: Thiết lập môi trường local

- **Đã setup:** Khởi tạo môi trường ảo độc lập thông qua Anaconda phục vụ dự án với câu lệnh: `conda create -n geobloom python=3.10`.
- **Đã cài đặt thư viện:** Triển khai cài đặt các gói thư viện tính toán khoa học và học sâu nền tảng: `numpy`, `pandas`, `tqdm`, `scipy`, `torch`, `transformers`, `scikit-learn`.
- **Hành động mã nguồn:**
  - Tiến hành sao chép mã nguồn của tác giả từ liên kết gốc (`https://github.com/pkuliyi2015/GeoBloom`).
  - Khởi tạo cấu trúc quản lý mã nguồn thực nghiệm riêng biệt tại (`https://github.com/Nobita534/ThucNghiemGeoBloom`).

### Giai đoạn 2: Chạy Unsupervised và supervised training

- **Đã setup kịch bản:** Thiết lập quy trình tiền xử lý dữ liệu và khởi chạy mô hình Unsupervised hoàn toàn trên môi trường máy cục bộ (Local). Song song đó, cấu hình kịch bản huấn luyện có giám sát Supervised sử dụng tài nguyên phần cứng mạnh (GPU Tesla T4x2) thông qua môi trường Kaggle Notebooks trên bộ dữ liệu sạch `GeoGLUE_clean`.
- **Lưu trữ dữ liệu:** Lưu vết toàn bộ kết quả chạy, tham số huấn luyện và output training trực tiếp vào thư mục `results` của repo `ThucNghiemGeoBloom`.

### Giai đoạn 3: Chạy 2 baseline model để so sánh

- **Đã thực hiện:** Thiết lập hai tệp notebook riêng biệt mang tên `baseline-bm25d.ipynb` và `baseline-bertd.ipynb` trên nền tảng Kaggle để chạy độc lập hai mô hình đối chứng tương ứng là BM25_D (Thuần văn bản truyền thống) và BERT_D (Học sâu ngữ nghĩa).
- **Lưu trữ dữ liệu:** Trích xuất các tệp cấu trúc và lưu ngược kết quả đầu ra về phân vùng thư mục `results` của `ThucNghiemGeoBloom`.

### Giai đoạn 4: Phân tích lỗi

- **Đã thực hiện:** Thực thi tệp lệnh script kịch bản `analyze.py` của hệ thống để tiến hành bóc tách, phân loại dữ liệu đầu ra và xuất bản thành 4 tệp tin báo cáo tĩnh: `success.txt`, `fail.txt`, `top20.txt`, và `result.txt`.
- **Trực quan hóa:** Xây dựng riêng một file notebook chuyên biệt cho mục đích Phân tích lỗi nhằm mục đích chạy thử nghiệm trực quan (visualization) các phân phối sai lệch dữ liệu địa lý.

---

## 5. Các vấn đề đã gặp

- **Vấn đề 1 (Lỗi thực thi Evaluation):** Khi thực hiện chạy file lệnh `evaluation.py` trong folder `GeoBloom_Source` để đánh giá hai mô hình baseline, hệ thống gặp lỗi hoặc không thể xuất kết quả do bị thiếu file đầu vào, tuy nhiên tại thời điểm đó giao diện terminal không chỉ điểm rõ ràng là đang thiếu cụ thể tệp tin nào khiến quá trình kiểm thử bị gián đoạn.
- **Vấn đề 2 (Định hướng Dashboard tối ưu insight):** Người dùng có dự định xây dựng một hệ thống Dashboard tổng quan nhằm trực quan hóa các phiên chạy mô hình, đối sánh hiệu năng tài nguyên và hiển thị biểu đồ phân tích lỗi. Tuy nhiên, hiện tại hệ thống dashboard chưa tối ưu được các insight chuyên sâu do các thông số thống kê chưa được chọn lọc và cấu trúc một cách phù hợp.
- **Vấn đề 3 (Độ phủ dữ liệu của Dataset phụ):** Trong kịch bản chạy Unsupervised, hệ thống có thực hiện xử lý dữ liệu đầu ra cho hai bộ dữ liệu đã progressing là `Beijing` và `Shanghai`. Tuy nhiên, cả hai bộ này đều chưa được khởi chạy huấn luyện (training) cũng như chưa được chạy qua hai mô hình baseline. Đặt ra bài toán nghi vấn: _If chỉ chạy duy nhất bộ dữ liệu GeoGLUE_clean thì đã đủ điều kiện khoa học chưa?_ Nhận định thực tế cho thấy chỉ cần tập trung bộ `GeoGLUE_clean` là chuẩn xác nhất vì đây là tập dữ liệu có thông tin đặc tả đầy đủ nhất trong tài liệu `README.md` của tác giả.
- **Vấn đề 4 (Khả năng bóc tách cây của Baseline):** Qua nghiên cứu mã nguồn tệp `analyze.py` trong folder `result` của tác giả, phát hiện hệ thống sử dụng hàm chức năng `deserialize_tree` để tách cấu trúc cây phân vùng trong file chỉ mục `tree.bin`. Cần làm rõ luận điểm liệu có thể áp dụng trực tiếp hàm chức năng này để phân tích chuyên sâu cấu trúc cây cho hai mô hình baseline là `BM25_D` và `BERT_D` hay không.

---

## 6. Kết quả đã đạt được

Hệ thống đã thực hiện chạy thành công hoàn toàn các tiến trình lõi và thu thập đầy đủ các thành phần dữ liệu sau đây bên trong thư mục `results/` của repo `ThucNghiemGeoBloom`:

- Trích xuất toàn bộ dữ liệu log hệ thống bằng lệnh cấu hình mạng `nnue` của cả hai chế độ chạy Unsupervised và huấn luyện Supervised.
- Sinh thành công tệp cấu trúc cây chỉ mục không gian `tree.bin` cho các mô hình baseline thông qua quá trình tính toán phân tán trên tài nguyên Kaggle.
- Kết xuất thành công bộ 4 file dữ liệu phục vụ phân tích chất lượng từ file kịch bản `analyze.py`, bao gồm các tệp: `success`, `fail`, `result`, và `top20`.

---

## 7. Những phần chưa hoàn thành (Blocker hiện tại)

- **Blocker 1 (Chưa đối chiếu đầy đủ số liệu):** Công tác so sánh trực quan, trực diện giữa hiệu năng của hai mô hình baseline và kết quả sau khi huấn luyện có giám sát (supervised training). Hiện tại, người dùng mới chỉ dừng lại ở bước trích xuất thủ công các thông số vận hành tĩnh (thời gian chạy, tốc độ QPS, dung lượng ổ cứng chiếm dụng, dung lượng RAM tiêu thụ) trong quá trình khởi tạo cấu trúc `tree.bin` để lưu vào file tổng hợp `Bảng Tổng Hợp Số Liệu Thực Nghiệm (Benchmarking) - CSV`.
- **Blocker 2 (Thiếu hụt Metrics độ chính xác):** Chưa thể khởi chạy thành công file script `evaluation.py` cục bộ để trích xuất ra các chỉ số metric định lượng khoa học cốt lõi (bao gồm `Recall@20`, `Recall@10`, `NDCG@5`, `NDCG@1`) của hai mô hình baseline. Do đó, hiện tại chưa có đủ dữ liệu nền để tiến hành đánh giá biến động thuật toán khi cắt giảm tỷ lệ dữ liệu (Varying Data).

---

## 8. Lộ trình hành động tiếp theo (Roadmap)

1. **Khắc phục lỗi thực thi `evaluation.py`:** Sửa đổi cấu trúc code bằng cách chèn dòng lệnh gọi thực thi hàm `test()` một cách tường minh cho các mô hình `BM25_D` và `BERT_D` bên dưới khối mã kiểm tra `if __name__ == '__main__':` để bắt buộc hệ thống in kết quả ra màn hình terminal.
2. **Đồng bộ định dạng tệp dự đoán cục bộ:** Di chuyển hoặc biên dịch lại các file kết quả dự đoán thu được từ các notebook trên Kaggle thành định dạng mảng cấu trúc `.npy`, đổi tên chính xác theo logic nhận diện của script (ví dụ: `GeoGLUE_clean_BM25_D_top100.npy`) và đặt vào thư mục `GeoBloom_Source/result/`.
3. **Hoàn thiện bảng Benchmarking thực nghiệm:** Chạy lại lệnh đánh giá kiểm thử tổng thể để thu về các con số cụ thể của `Recall` và `NDCG`, từ đó điền bổ sung vào các ô dữ liệu đang bị khuyết của hai mô hình baseline trong bảng số liệu.
4. **Thực hiện đánh giá dữ liệu cắt giảm (Varying Data):** Gọi hàm đánh giá tuần tự trên các tệp dữ liệu đã phân tách theo tỷ lệ phần trăm (`portions = [0.02, 0.05, 0.1, 0.3, 0.5, 0.7]`) để thu thập số liệu và tiến hành vẽ biểu đồ đường, chứng minh trực quan độ ổn định của kiến trúc thuật toán trước hội đồng báo cáo.
