import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Tải model sentiment analysis tiếng Việt
MODEL_NAME = "mr4/phobert-base-vi-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Giao diện Streamlit
st.set_page_config(page_title="Vietnamese Sentiment Analysis", page_icon="🇻🇳")
st.title("🇻🇳 Ứng dụng phân tích cảm xúc tiếng Việt")
st.write("Nhập vào một câu hoặc đoạn văn bản để phân tích cảm xúc (tích cực / tiêu cực / trung lập).")

# Nhập văn bản
user_input = st.text_area("Nhập văn bản:", "")

if st.button("Phân tích"):
    if user_input.strip() == "":
        st.warning("⚠️ Vui lòng nhập văn bản.")
    else:
        # Gọi mô hình Hugging Face
        result = sentiment_pipeline(user_input)[0]
        label = result['label']
        score = result['score']

        # Hiển thị kết quả
        st.subheader("Kết quả phân tích")
        st.write(f"**Văn bản nhập vào:** {user_input}")
        st.write(f"**Nhận định cảm xúc:** {label}")
        st.write(f"**Độ tin cậy:** {score:.2%}")
