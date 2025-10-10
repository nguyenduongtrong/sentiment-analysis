# Sentiment Analysis (Phân tích cảm xúc)

Một ứng dụng mẫu dùng Python + Hugging Face + Streamlit để phân tích cảm xúc (positive / negative / neutral) — mục tiêu cho tiếng Việt.
Giao diện cho phép so sánh kết quả của 3 mô hình sentiment phổ biến.

---

## 📌 Mô tả

- Dự án này là một ứng dụng web đơn giản để **phân tích cảm xúc** (sentiment) của văn bản tiếng Việt.
- Phân tích cảm xúc (tích cực / tiêu cực / trung lập) cho văn bản tiếng Việt.
- Sử dụng 3 mô hình từ Hugging Face:
  - `mr4/phobert-base-vi-sentiment-analysis`
  - `5CD-AI/Vietnamese-Sentiment-visobert`
  - `wonrax/phobert-base-vietnamese-sentiment`
- Giao diện Streamlit: 3 ô nhập liệu nằm ngang, mỗi ô tương ứng một model, kết quả hiển thị dạng bảng phía dưới để dễ so sánh.

---

## 🧩 Cấu trúc thư mục

```
sentiment-analysis/
├── app.py               # file chính chạy Streamlit
├── requirements.txt     # file liệt kê dependencies
├── README.md            # hướng dẫn sử dụng (file này)
└── (các file khác nếu có)
```

- `app.py` — chứa mã nguồn Streamlit + logic gọi Hugging Face pipeline  
- `requirements.txt` — các thư viện cần cài: `streamlit`, `transformers`, `torch`, `sentencepiece`, v.v.  
- `README.md` — hướng dẫn sử dụng, mô tả dự án  

---

## 🚀 Cài đặt và chạy

### 1. Clone repository

```bash
git clone https://github.com/nguyenduongtrong/sentiment-analysis.git
cd sentiment-analysis
```

### 2. Tạo virtual environment (venv)

```bash
python -m venv .venv
```

Kích hoạt nó:

- Trên **Windows (PowerShell)**:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

  Nếu gặp lỗi `running scripts is disabled`, bạn có thể dùng lệnh:
  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- Trên **Windows (CMD)**:
  ```cmd
  .venv\Scriptsctivate.bat
  ```

- Trên **macOS / Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Cài dependencies

```bash
pip install -r requirements.txt
```

### 4. Chạy ứng dụng

```bash
streamlit run app.py
```

Mở trình duyệt và truy cập địa chỉ hiển thị (mặc định là `http://localhost:8501`).

---

## ✅ Cách sử dụng

- Nhập đoạn văn bản tiếng Việt vào ô nhập liệu  
- Nhấn nút **Phân tích**  
- Ứng dụng sẽ hiển thị:
  - Các nhãn cảm xúc cùng xác suất (positive / negative / neutral)  
  - Biểu đồ phân bố xác suất  

Ví dụ:
> “Mình rất thích bộ phim này” → positive (xác suất cao)  
> “Đồ ăn rất dở, tôi không hài lòng” → negative

---

## ⚠️ Lưu ý & cải thiện

- Lần chạy đầu sẽ tải model từ Hugging Face (cần internet, có thể mất thời gian).
- Ứng dụng đã cache pipeline để tăng tốc cho lần chạy sau.
- Nhãn trả về có thể khác nhau giữa các model (`LABEL_0`, `LABEL_1`, ... hoặc tên cụ thể). Có thể tự map sang tiếng Việt nếu muốn.
- Với dữ liệu thực tế (bình luận mạng xã hội, phản hồi khách hàng), bạn có thể cần fine-tune lại hoặc sử dụng mô hình khác  
- Có thể mở rộng app để:
  - Nhập **nhiều câu cùng lúc** và phân tích từng câu riêng biệt  
  - So sánh kết quả giữa nhiều mô hình  
  - Lưu trữ kết quả vào database  
  - Tích hợp API để sử dụng từ ứng dụng khác  

---

## 🔧 Các model sử dụng

- `mr4/phobert-base-vi-sentiment-analysis`
- `5CD-AI/Vietnamese-Sentiment-visobert`
- `wonrax/phobert-base-vietnamese-sentiment`

Bạn có thể thêm/thay đổi model trong file `main.py` (dictionary `MODEL_INFOS`).

---

## 📚 Tài liệu & tham khảo

- [Hugging Face — Transformers](https://huggingface.co/transformers/)  
- [Streamlit Documentation](https://docs.streamlit.io/)  
- Mô hình `mr4/phobert-base-vi-sentiment-analysis` trên Hugging Face  
- Các bài viết / tài liệu về sentiment analysis tiếng Việt  
