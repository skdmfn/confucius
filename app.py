import streamlit as st
import time
import random

st.set_page_config(page_title="Dino Run!", layout="centered")
st.title("🦖 Dino Run")

# 게임 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.jump = False
    st.session_state.obstacle = False

# 점프 버튼
jump_pressed = st.button("⬆️ Jump")

# 점프 처리
if jump_pressed and not st.session_state.jump:
    st.session_state.jump = True
    jump_time = time.time()

# 장애물 생성
if random.randint(1, 10) > 7:
    st.session_state.obstacle = True
else:
    st.session_state.obstacle = False

# 충돌 검사
if st.session_state.obstacle and not st.session_state.jump:
    st.session_state.game_over = True

# 게임 화면 출력
if st.session_state.game_over:
    st.error("💥 Game Over!")
    st.write(f"Your score: {st.session_state.score}")
    if st.button("🔄 Restart"):
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.jump = False
else:
    dino = "🦖" if not st.session_state.jump else "🦖⬆️"
    obs = "🌵" if st.session_state.obstacle else "⠀"
    st.write(f"{dino} {' ' * 10} {obs}")
    st.session_state.score += 1
    time.sleep(0.5)
    st.experimental_rerun()
