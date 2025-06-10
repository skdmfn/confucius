import streamlit as st
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI와 공학 체험 웹앱", layout="centered")

st.title("🤖 AI & ⚙️ 공학 체험 웹앱")
st.write("진로: 인공지능, 공학 분야")

# ------------------------------
# 기능 1: 간단한 AI 숫자 인식기
# ------------------------------
st.header("1️⃣ 숫자 이미지 인식 AI 체험")

# 데이터셋 로드
digits = load_digits()
X_train, X_test, y_train, y_test = train_test_split(
    digits.data, digits.target, test_size=0.2, random_state=42
)

# 모델 훈련
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# 숫자 선택
index = st.slider("테스트할 이미지 번호를 선택하세요", 0, len(X_test)-1, 0)

# 이미지 예측
pred = knn.predict([X_test[index]])

# 이미지 출력
st.image(digits.images[index], caption=f"실제 숫자: {y_test[index]}", width=150)
st.success(f"🤖 AI 예측 결과: {pred[0]}")

# ------------------------------
# 기능 2: 공학용 계산기 (옴의 법칙)
# ------------------------------
st.header("2️⃣ 공학용 계산기 (옴의 법칙: V = I × R)")

calc_option = st.radio("계산할 값을 선택하세요", ["전압(V)", "전류(I)", "저항(R)"])

try:
    if calc_option == "전압(V)":
        current = st.number_input("전류 I (단위: A)", value=0.0)
        resistance = st.number_input("저항 R (단위: Ω)", value=1.0)
        voltage = current * resistance
        st.success(f"전압 V = {voltage:.2f} V")
    elif calc_option == "전류(I)":
        voltage = st.number_input("전압 V (단위: V)", value=0.0)
        resistance = st.number_input("저항 R (단위: Ω)", value=1.0)
        current = voltage / resistance if resistance != 0 else 0
        st.success(f"전류 I = {current:.2f} A")
    elif calc_option == "저항(R)":
        voltage = st.number_input("전압 V (단위: V)", value=0.0)
        current = st.number_input("전류 I (단위: A)", value=1.0)
        resistance = voltage / current if current != 0 else 0
        st.success(f"저항 R = {resistance:.2f} Ω")
except Exception as e:
    st.error(f"오류 발생: {e}")
