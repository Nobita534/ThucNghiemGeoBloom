# Thực Nghiệm Thuật Toán Định Vị Địa Lý GeoBloom (VLDB 2025)

## 1. Giới thiệu bài báo gốc

### 📌 Bài toán đặt ra (Case Study)
Hệ thống Tìm kiếm Thông tin Địa lý (Geographic Information Retrieval - GIR) đóng vai trò cốt lõi trong các dịch vụ bản đồ trực tuyến và ứng dụng định vị dựa trên vị trí. Bài toán đặt ra là khi người dùng nhập một câu truy vấn dạng văn bản thô đi kèm với tọa độ vị trí không gian hiện tại (GPS), hệ thống phải tìm kiếm, tính toán điểm tương đồng và trả về danh sách các đối tượng địa lý (Points of Interest - POIs) phù hợp nhất với nhu cầu của người dùng.

### 🔄 Các phương pháp xử lý trước đó
* **Phương pháp truyền thống (Ví dụ: BM25-D):** Kết hợp các chỉ số so khớp từ khóa văn bản thô truyền thống (BM25) với khoảng cách hình học địa lý. Phương pháp này đạt tốc độ xử lý nhanh và gọn nhẹ nhưng chỉ thực hiện so khớp từ khóa thuần túy, hoàn toàn bỏ qua ngữ nghĩa sâu của câu truy vấn (ví dụ: coi hai từ đồng nghĩa là hai từ khác nhau).
* **Phương pháp học sâu dựa trên Mô hình ngôn ngữ lớn (PLMs - Ví dụ: BERT, DPR, LIST):** Sử dụng các kiến trúc mạng lớn có sẵn để mã hóa ngữ nghĩa văn bản thô thành các mảng vector nhúng dày đặc (Dense Embeddings). Các mô hình này đạt độ chính xác cao về ngữ nghĩa nhưng tiêu tốn tài nguyên phần cứng cực kỳ lớn, dung lượng lưu trữ nặng, tốc độ xử lý truy vấn chậm và đòi hỏi một lượng lớn dữ liệu gán nhãn (Labeled Queries) để huấn luyện.

### 🚀 Phương pháp đề xuất mới: Mô hình GeoBloom
Mô hình GeoBloom (xuất bản tại hội nghị khoa học PVLDB 2025) được đề xuất như một kiến trúc gọn nhẹ (Lightweight Framework) nhằm giải quyết triệt để các hạn chế của PLMs. Kiến trúc này gồm 3 thành phần cốt lõi:
1. **Mã hóa bằng Bloom Filter:** Chuyển đổi toàn bộ từ khóa văn bản thô của câu truy vấn và các POI nền thành các mảng vector nhị phân thưa (Sparse Vectors) có chiều dài cố định. Cơ chế này giúp xử lý rất tốt các từ khóa có tần suất xuất hiện thấp như địa chỉ nhà, tên thương hiệu riêng biệt, số hiệu tòa nhà mà không cần qua huấn luyện.
2. **Bộ đánh giá Bloom Filter Evaluator (Kiến trúc NNUE):** Áp dụng kiến trúc mạng nơ-ron cập nhật hiệu quả (NNUE) kế thừa từ các thuật toán cờ vua để tính toán và đánh giá trọng số của từng bit nhị phân giao nhau giữa câu truy vấn và POI. Bộ mạng này chạy tối ưu trên CPU và chỉ xử lý các bit có giá trị bằng 1, giúp giảm thiểu tối đa độ khuếch đại tính toán.
3. **Cấu trúc cây chỉ mục Bloom Filter Tree:** Phân hoạch không gian tìm kiếm POI theo phân cấp hình học, giúp giảm số lượng phép so sánh thực tế khi truy vấn trực tuyến mà vẫn giữ nguyên độ chính xác tương đương với tìm kiếm vét cạn (Brute-force).

### 📊 Kết quả thực nghiệm trong bài báo
* Vượt trội hơn các mô hình baseline học sâu trong cả hai môi trường: Không giám sát (Unsupervised - cải thiện tới 15.66% điểm NDCG@5) và Có giám sát (Supervised - cải thiện tới 10.94% điểm NDCG@5) trên tập dữ liệu thực tế.
* Tốc độ xử lý truy vấn nhanh hơn tối đa **80 lần** so với mô hình đối chứng dựa trên mạng học sâu.
* Tiết kiệm tới **74.72% bộ nhớ RAM** lúc runtime và giảm **87.64% dung lượng lưu trữ ổ cứng (Disk Space)** so với các giải pháp PLM.

### ⚖️ Ưu điểm và Nhược điểm của GeoBloom
* **Ưu điểm:** Siêu gọn nhẹ; hiệu năng thời gian và không gian cực cao; xử lý các từ khóa địa lý thô đặc thù (địa chỉ, số nhà) rất chính xác; đạt hiệu quả cao mà không phụ thuộc vào nguồn dữ liệu gán nhãn khổng lồ.
* **Nhược điểm:** Chịu ảnh hưởng bởi tỷ lệ xung đột băm (Hash Collision) tự nhiên của cấu trúc Bloom Filter và bị mất thông tin thứ tự của từ ngữ khi chuỗi văn bản thô quá dài (Mô hình phải giảm thiểu bằng cách kết hợp thêm bộ mã hóa n-gram và thành phần tích chập 1-D Convolution phụ trợ).


## 2. Giới thiệu repo của tác giả

Kho lưu trữ gốc của tác giả bao gồm **9 thư mục chính**. Toàn bộ mã nguồn này được cung cấp nhằm mục đích chứng minh thực nghiệm cho lý thuyết bài báo (VLDB 2025) trong việc giải quyết bài toán tìm kiếm thông tin địa lý (GIR) gọn nhẹ, đạt tốc độ cao và tiết kiệm ổ cứng mà không phụ thuộc vào dữ liệu gán nhãn khổng lồ.

### 🔍 Mục đích của từng thư mục
* **`baselines`**: Chứa mã nguồn chạy đối chứng của các phương pháp so khớp từ khóa truyền thống (BM25) và các mô hình học sâu (BERT, DPR, OpenAI).
* **`cuda`**: Chứa mã nguồn mã hóa phần cứng bằng ngôn ngữ CUDA C++ để tối ưu hóa hiệu năng tính toán Bloom Filter trên GPU.
* **`data`**: Lưu trữ các tệp nén chứa dữ liệu thô và dữ liệu văn bản thô chưa xử lý (`.7z`, `.txt`).
* **`data_bin`**: Chứa dữ liệu đã được số hóa sang định dạng cấu trúc nhị phân (`.bin`) giúp tăng tốc độ đọc ghi khi huấn luyện và kiểm thử.
* **`data_util`**: Chứa các script Python bổ trợ để làm sạch dữ liệu, tiền xử lý tập dữ liệu GeoGLUE và chia nhỏ tỷ lệ phân đoạn huấn luyện.
* **`model`**: Định nghĩa kiến trúc cốt lõi của GeoBloom bao gồm cấu trúc Bloom Filter, thuật toán phân cấp cây chỉ mục và xếp hạng LambdaRank.
* **`nnue`**: Chứa mã nguồn C++ của bộ mạng nơ-ron NNUE chạy tối ưu trên CPU phục vụ tính toán nhanh các bit nhị phân giao nhau.
* **`repeat`**: Chứa các file bash script (`.sh`) giúp lập kịch bản tự động kích hoạt tiến trình huấn luyện và đánh giá tuần tự trên các tập dữ liệu.
* **`result`**: Chứa các file Python thực hiện tính toán điểm số chất lượng (Recall, NDCG) và tóm tắt kết quả đầu ra sau khi mô hình chạy xong.


## 3. Tiến trình thực nghiệm chính

### 📊 Tập dữ liệu trọng tâm: `GeoGLUE_clean`
Thực nghiệm trong kho lưu trữ này tập trung hoàn toàn vào tập dữ liệu **`GeoGLUE_clean`** vì những lý do kỹ thuật cốt lõi sau:
* **Khắc phục dữ liệu nhiễu:** Tập dữ liệu GeoGLUE gốc của tác giả chứa hơn $50\%$ đối tượng địa lý giả (fake POIs) và bị xáo trộn vị trí tọa độ. 
* **Chuẩn hóa thực tế:** Tập dữ liệu `GeoGLUE_clean` đã được tiền xử lý bằng cách lọc và ánh xạ toàn bộ các câu truy vấn tương ứng với $17,290$ POIs nhiễu ban đầu sang các đối tượng địa lý thực tế tại thành phố Hàng Châu (Trung Quốc) thu thập từ OpenStreetMap. Quá trình khớp mã định danh (ID) chính xác này được thực hiện thông qua thuật toán BM25 và mô hình ngôn ngữ lớn GPT-4-turbo, giữ lại $10,278$ POIs sạch. Điều này đảm bảo kết quả đo đạc phản ánh chính xác năng lực vận hành của mô hình trong môi trường thực tế.

---

### 🔄 Thứ tự các bước thực hiện thực nghiệm
Tiến trình thực nghiệm hệ thống được triển khai tuần tự theo 6 giai đoạn sau:

1. **Chạy mô hình không giám sát (Unsupervised):** Kích hoạt thuật toán GeoBloom chạy trực tiếp dựa trên cơ chế so khớp bit nhị phân giao nhau giữa Bloom Filter của câu truy vấn và đối tượng địa lý mà không sử dụng dữ liệu huấn luyện gán nhãn.
2. **Huấn luyện có giám sát (Supervised Training) trên Kaggle:** Chạy file Notebook huấn luyện bộ mạng nơ-ron đánh giá trọng số bit NNUE tĩnh (`geobloom-supervised-training (1).ipynb`) sử dụng tài nguyên phần cứng trực tuyến của Kaggle.
3. **Thực nghiệm thiếu hụt dữ liệu (Varying Data):** Huấn luyện mô hình với các phân đoạn dữ liệu gán nhãn bị cắt giảm sâu (từ $2\%$ đến $70\%$) để kiểm thử độ ổn định thuật toán.
4. **Chạy các mô hình đối chứng (Baselines):** Chạy độc lập 2 mô hình đối chứng `BM25_D` (phương pháp so khớp từ khóa truyền thống kèm khoảng cách) và `BERT_D` (mô hình ngôn ngữ học sâu kèm khoảng cách) để lấy số liệu đối chiếu chất lượng và hiệu năng.
5. **Dựng Dashboard tổng quan:** Tập hợp toàn bộ các file log kết quả tĩnh, chuẩn hóa thành các bảng tính phẳng `.csv` dưới máy local và xây dựng Dashboard phân tích hiệu năng tương tác trực quan thông qua công cụ Power BI.
6. **Ứng dụng Website ví dụ:** Tích hợp mô hình đã huấn luyện hoàn chỉnh vào một giao diện web minh họa thực tế (Sắp thực hiện).


## 4. Mô tả chi tiết các bước thực nghiệm

### 1. Cài đặt môi trường
* **Mục đích:** Khởi tạo môi trường ảo Conda cô lập, cài đặt các thư viện Python phụ thuộc và biên dịch bộ tăng tốc C++ NNUE Engine để chuẩn bị nền tảng chạy thực nghiệm.
* **Cách thực hiện:** Chạy các lệnh sau tại thư mục gốc của kho lưu trữ:
  ```bash
  # 1. Khởi tạo và kích hoạt môi trường ảo Conda với Python 3.12
  conda create -n geobloom python=3.12 -y
  conda activate geobloom

  # 2. Cài đặt các thư viện Python bắt buộc
  pip install jieba_fast rank_bm25 transformers==4.38.0 accelerate scikit-learn==1.4.2 xxhash==3.4.1

  # 3. Biên dịch công cụ tăng tốc C++ NNUE Engine (Hỗ trợ tập lệnh tối ưu AVX2)
  g++ GeoBloom_Source/nnue/v19/nnue.cpp -o GeoBloom_Source/nnue/v19/nnue -pthread -mavx2 -O3 -fno-tree-vectorize

  # 4. Cài đặt công cụ p7zip và giải nén tập dữ liệu sạch GeoGLUE_clean
  sudo apt-get update && sudo apt-get install -y p7zip-full
  cd GeoBloom_Source/data && 7z x GeoGLUE_clean.7z -y && cd ../..
  ```

### 2. Chạy mô hình không giám sát (Unsupervised)
* **Mục đích:** Đánh giá năng lực định vị địa lý cơ bản của thuật toán GeoBloom bằng cơ chế so khớp bit nhị phân giao nhau thô giữa các Bloom Filter mà không cần huấn luyện mạng nơ-ron.
* **Cách chạy:**
  ```bash
  cd GeoBloom_Source
  nnue/v19/nnue GeoGLUE_clean test 8 800-800-800-800
  ```

### 3. Huấn luyện có giám sát (Supervised Training) trên Kaggle
* **Mục đích:** Huấn luyện bộ mạng nơ-ron đánh giá trọng số bit NNUE tĩnh nhằm tối ưu hóa tầm quan trọng của từng bit nhị phân liên kết với đáp án chính xác (Ground Truth).
* **Cách cài đặt và chạy file:**
  1. Nạp file Notebook `notebooks/geobloom-supervised-training (1).ipynb` lên môi trường Kaggle.
  2. Thiết lập cấu hình phần cứng Accelerator là **GPU T4**.
  3. Click chọn **Save Version** ở góc trên bên phải giao diện ➔ Chọn **Save & Run All (Commit)** để kích hoạt chế độ tự động thực thi ngầm hoàn toàn.
  4. Tiến trình chạy tự động sẽ huấn luyện mô hình qua 5 epochs, sinh file checkpoint `GeoGLUE_clean_geobloom_v19.pt` và bóc tách log hiệu năng thời gian thực vào file `results/GeoBloom_Supervised/result.txt`.

### 4. Thực nghiệm thiếu hụt dữ liệu (Varying Data)
* **Mục đích:** Kiểm thử độ ổn định và tính bền bỉ của thuật toán GeoBloom khi số lượng câu truy vấn gán nhãn dùng để huấn luyện bị cắt giảm thiếu hụt sâu sắc.
* **Cách cài đặt và chạy file:**
  1. Nạp file Notebook `notebooks/varyingdata-bigdataproj.ipynb` lên môi trường Kaggle.
  2. Thiết lập cấu hình phần cứng Accelerator là song song **GPU T4 x2** (Dual GPU).
  3. Click chọn **Save Version** ➔ Chọn **Save & Run All (Commit)** để kích hoạt tiến trình chạy tự động ngầm.
  4. Notebook sẽ tự động lặp qua tuần lặp huấn luyện và đánh giá mô hình tương ứng với 7 tỷ lệ dữ liệu huấn luyện đầu vào: 2%, 5%, 10%, 20%, 30%, 50%, và 70%. Kết quả điểm số bóc tách sau mỗi phân đoạn được ghi thẳng vào file log tĩnh `results/Varying Data/varying_data_results.txt`.

### 5. Chạy các mô hình đối chứng (Baselines)
* **Mục đích:** Đo đạc các chỉ số chất lượng định vị và hiệu năng tiêu thụ tài nguyên của mô hình so khớp từ khóa truyền thống (`BM25_D`) và mô hình học sâu (`BERT_D`) kết hợp khoảng cách hình học để làm cơ sở đối chứng thực nghiệm.
* **Cách cài đặt và chạy file:**
  1. Nạp hai file Notebook đối chứng `notebooks/baseline-bm25d.ipynb` và `notebooks/baseline-bertd.ipynb` lên môi trường Kaggle.
  2. Thiết lập cấu hình môi trường phần cứng cho **cả hai mô hình baseline hoàn toàn đồng bộ như nhau**: Đều cấu hình Accelerator là **GPU T4**.
  3. Trên giao diện của từng file Notebook, click chọn **Save Version** ➔ Chọn **Save & Run All (Commit)** để kích hoạt chế độ tự động chạy ngầm hoàn toàn.
  4. Sau khi kết thúc tiến trình chạy tự động, các thông số về thời gian chạy, tốc độ QPS và dung lượng file kết quả của hai baseline sẽ được ghi lại đồng bộ vào file log tĩnh `baseline_perf.txt` nằm trong thư mục kết quả tương ứng (`results/BM25_D/` và `results/BERT_D/`).

### 6. Dựng Dashboard tổng quan
* **Mục đích:** Chuẩn hóa các tệp log thô thu được từ môi trường Kaggle sang định dạng bảng tính phẳng, phục vụ việc xây dựng giao diện báo cáo hiệu năng trực quan và tương tác thời gian thực trên Power BI.
* **Cách chạy file:**
  1. Tại môi trường máy local (đã tải đầy đủ các folder kết quả ngầm từ Kaggle về đúng cấu trúc thư mục của dự án), mở terminal tại thư mục gốc và chạy file Python:
     ```bash
     python auto_benchmarking_dashboard.py
     ```
     Lệnh này sẽ tự động lọc bỏ thuộc tính RAM cũ, ép thuộc tính ổ cứng của hai baseline về trạng thái trống `null` và cập nhật trực tiếp số liệu vào file `Visualizaion/Bảng Tổng Hợp Số Liệu Thực Nghiệm (Benchmarking).csv`.
  2. Mở file thiết kế `Visualizaion/PowerBI/Dashboard thống kê hiệu năng của mô hình GeoBloom.pbix` bằng phần mềm **Power BI Desktop**, nhấn nút **Refresh** trên thanh công cụ để toàn bộ biểu đồ tự động đồng bộ số liệu mới.


## 5. Cấu trúc kho lưu trữ thực nghiệm (Repository Structure)

Cấu trúc cây thư mục tổng thể của kho lưu trữ `ThucNghiemGeoBloom` được tổ chức theo các phân khu chức năng như sau:

```text
ThucNghiemGeoBloom/
│
├─── auto_benchmarking_dashboard.py # Script Python tự động quét log, xử lý số liệu phẳng cho Dashboard local
├─── README.md                      # Tài liệu hướng dẫn thực nghiệm hệ thống tổng thể
│
├─── data/                          # Thư mục lưu trữ các tệp dữ liệu thô cục bộ
│
├─── evaluation/                    # Thư mục chứa các script đánh giá độc lập
│
├─── GeoBloom_Source/               # Kho lưu trữ mã nguồn nền tảng từ tác giả gốc (gồm model, nnue C++, baselines...)
│
├─── models/                        # Quản lý và lưu trữ các file trọng số mô hình sau khi huấn luyện
│    └─── GeoBloom_Supervised/
│         └─── GeoGLUE_clean_geobloom_v19.pt # File checkpoint trọng số của GeoBloom huấn luyện trên Kaggle
│
├─── notebooks/                     # Hệ thống các tệp Jupyter Notebook thực thi tiến trình thực nghiệm chính
│    ├─── baseline-bertd.ipynb      # Tiến trình chạy mô hình đối chứng BERT-D trên Kaggle
│    ├─── baseline-bm25d.ipynb      # Tiến trình chạy mô hình đối chứng BM25-D trên Kaggle
│    ├─── geobloom-supervised-training (1).ipynb # Tiến trình huấn luyện có giám sát mô hình GeoBloom v19
│    ├─── varyingdata-bigdataproj.ipynb # Vòng lặp thực nghiệm thiếu hụt dữ liệu (Robustness với 7 phân đoạn)
│    └─── Fail_analyze.ipynb        # Phân tích sâu các chuỗi câu truy vấn định vị bị lỗi của GeoBloom
│
├─── reports/                       # Thư mục lưu trữ các báo cáo thực nghiệm liên quan
│
├─── results/                       # Hệ thống quản lý log đầu ra tĩnh bóc tách từ Kaggle
│    ├─── BERT_D/                   # Kết quả đo đạc thời gian, ma trận nhúng và điểm số của BERT-D
│    ├─── BM25_D/                   # Kết quả đo đạc thời gian, tốc độ QPS và điểm số của BM25-D
│    ├─── GeoBloom_Supervised/      # Kết quả kiểm thử và log hiệu năng thời gian thực của GeoBloom có giám sát
│    ├─── Unsupervised_result/      # Nhật ký kết quả định vị không giám sát của GeoBloom
│    ├─── Varying Data/             # Tệp kết quả tĩnh 'varying_data_results.txt' lưu điểm số qua 7 tỷ lệ dữ liệu
│    └─── logs/                     # Folder lưu trữ phân loại chuỗi câu truy vấn định vị chi tiết
│         ├─── BERT_D_Analysis/     # Danh sách câu truy vấn Success/Top20/Fail của BERT-D
│         ├─── BM25_D_Analysis/     # Danh sách câu truy vấn Success/Top20/Fail của BM25-D
│         └─── geoglue_clean_unsupervised/ # Danh sách câu truy vấn Success/Top20/Fail của GeoBloom Unsupervised
│
└─── Visualizaion/                  # Phân khu cơ sở dữ liệu và tệp trực quan hóa Dashboard tập trung
     ├─── Bảng tổng hợp kết quả Varying Data.csv               # Dữ liệu phẳng đo độ ổn định mô hình
     ├─── Bảng Tổng Hợp Số Liệu Thực Nghiệm (Benchmarking).csv # Dữ liệu phẳng so sánh hiệu năng 3 mô hình
     │
     ├─── Dashboard/                # Lưu trữ các file ảnh tĩnh kết quả Dashboard trực quan (.png)
     └─── PowerBI/                  # Nơi lưu trữ file thiết kế Dashboard tương tác Power BI gốc
          └─── Dashboard thống kê hiệu năng của mô hình GeoBloom.pbix
```
