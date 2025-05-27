import streamlit as st
import random

st.set_page_config(page_title="Dino Run 🦖", layout="wide")
st.title("🦖 Dino Run - Manual Frame Edition")

# 상태 초기화
if "dino_y" not in st.session_state:
    st.session_state.dino_y = 0
    st.session_state.velocity = 0
    st.session_state.score = 0
    st.session_state.tick = 0
    st.session_state.obstacles = [20]
    st.session_state.game_over = False

# UI
col1, col2 = st.columns(2)
jump = col1.button("⬆️ Jump")
next_frame = col2.button("▶️ Next Frame")

# 점프
if jump and st.session_state.dino_y == 0:
    st.session_state.velocity = 1.5

# 물리 처리
if st.session_state.dino_y > 0 or st.session_state.velocity > 0:
    st.session_state.dino_y += st.session_state.velocity
    st.session_state.velocity -= 0.5
    if st.session_state.dino_y <= 0:
        st.session_state.dino_y = 0
        st.session_state.velocity = 0

# 다음 프레임 처리
if next_frame and not st.session_state.game_over:
    # 장애물 이동
    st.session_state.obstacles = [o - 1 for o in st.session_state.obstacles if o > 0]

    # 새 장애물 생성
    if random.random() < 0.1:
        st.session_state.obstacles.append(30)

    # 충돌 검사
    for obs in st.session_state.obstacles:
        if obs == 3 and st.session_state.dino_y < 1:
            st.session_state.game_over = True

    st.session_state.score += 1

# 화면 렌더링
cols = st.columns(30)
for i in range(30):
    if i == 3:
        if st.session_state.dino_y > 0:
            cols[i].markdown("🦖⬆️")
        else:
            cols[i].markdown("🦖")
    elif i in st.session_state.obstacles:
        cols[i].markdown("🌵")
    else:
        cols[i].markdown("⠀")

# 결과
if st.session_state.game_over:
    st.error("💥 Game Over!")
    st.write(f"Your score: {st.session_state.score}")
    if st.button("🔄 Restart"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.experimental_rerun()
else:
    st.caption(f"Score: {st.session_state.score}")
