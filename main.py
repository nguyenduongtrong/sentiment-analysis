import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import pandas as pd

# --- Cấu hình các model ---
MODEL_INFOS = {
    "mr4/phobert-base-vi-sentiment-analysis": "Phobert (mr4)",
    "5CD-AI/Vietnamese-Sentiment-visobert": "VisoBERT (5CD-AI)",
    "wonrax/phobert-base-vietnamese-sentiment": "PhoBERT (wonrax)",
}

# Cache loader: dùng st.cache_resource nếu có, fallback sang st.cache
def _cache_resource_or_cache(fn):
    # Return decorated function using available cache decorator
    if hasattr(st, "cache_resource"):
        return st.cache_resource(fn)
    else:
        return st.cache(fn)

@_cache_resource_or_cache
def load_pipeline(model_name: str):
    """Tải tokenizer, model và tạo pipeline (cached)."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# --- Giao diện Streamlit ---
st.set_page_config(page_title="Vietnamese Sentiment Analysis", page_icon="🇻🇳")
st.title("Ứng dụng phân tích cảm xúc tiếng Việt")
st.write("Nhập vào một câu hoặc đoạn văn bản trong mỗi ô tương ứng để phân tích bằng model được ghi rõ.")

def analyze_with_model(model_name: str, text: str):
    """Gọi pipeline đã cached và trả về label, score hoặc lỗi."""
    if text.strip() == "":
        return None, "⚠️ Vui lòng nhập văn bản."
    try:
        with st.spinner(f"Đang phân tích bằng {MODEL_INFOS.get(model_name, model_name)} ..."):
            pipe = load_pipeline(model_name)
            res = pipe(text)
            if isinstance(res, list) and len(res) > 0:
                r = res[0]
                return r, None
            return None, "Không nhận được kết quả từ pipeline."
    except Exception as e:
        return None, f"Lỗi khi gọi model: {e}"

# Hiển thị 3 ô input nằm ngang (3 cột) — kết quả sẽ hiển thị dọc phía dưới để dễ so sánh
st.markdown("---")

# Tạo 3 cột có cùng kích thước (tạo bằng nhau bằng cách truyền list giống nhau)
cols = st.columns([1, 1, 1])
for i, (model_name, friendly) in enumerate(MODEL_INFOS.items()):
    with cols[i]:
        st.subheader(friendly)
        # key dùng chỉ số để tránh các ký tự khoảng trắng trong tên
        text_key = f"input_{i}"
        btn_key = f"btn_{i}"
        # Đặt chiều cao cố định để diện mạo đồng đều
        text = st.text_area(f"Nhập văn bản cho {friendly}", key=text_key, height=120)
        if st.button(f"Phân tích với {friendly}", key=btn_key):
            result, error = analyze_with_model(model_name, text)
            if error is not None:
                st.warning(error)
            else:
                # Lưu kết quả vào session_state để hiển thị phía dưới
                label = result.get("label") if result and hasattr(result, "get") else None
                score = result.get("score") if result and hasattr(result, "get") else None
                st.session_state[f"result_{i}"] = {
                    "model": friendly,
                    "text": text,
                    "label": label,
                    "score": score,
                }

# Phần hiển thị kết quả dọc theo từng model (để so sánh dễ dàng)
st.markdown("---")
st.header("Kết quả so sánh")
# Thu thập các kết quả hiện có
rows = []
for i, (model_name, friendly) in enumerate(MODEL_INFOS.items()):
    r_key = f"result_{i}"
    if r_key in st.session_state:
        r = st.session_state[r_key]
        rows.append({
            "Model": r.get("model", friendly),
            "Văn bản": r.get("text", ""),
            "Nhận định": r.get("label", "Không xác định"),
            "Độ tin cậy": r.get("score"),
        })

if len(rows) == 0:
    st.info("Chưa có kết quả. Nhập văn bản và nhấn 'Phân tích' ở ô tương ứng.")
else:
    # Hiển thị dưới dạng bảng để dễ so sánh; nếu có pandas, dùng DataFrame để định dạng cột %
    if pd is not None:
        df = pd.DataFrame(rows)
        # Format tỷ lệ phần trăm cho hiển thị: convert to percent strings
        if "Độ tin cậy" in df.columns:
            df["Độ tin cậy"] = df["Độ tin cậy"].apply(lambda x: f"{x:.2%}" if pd.notnull(x) else "—")
        st.table(df)
    else:
        # Fallback: dùng st.table trực tiếp với list of dicts
        # Convert score to formatted strings
        for r in rows:
            if r.get("Độ tin cậy") is not None:
                r["Độ tin cậy"] = f"{r['Độ tin cậy']:.2%}"
            else:
                r["Độ tin cậy"] = "—"
        st.table(rows)
