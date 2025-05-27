import streamlit as st
import time
import random
from streamlit_autorefresh import st_autorefresh

# 페이지 설정
st.set_page_config(page_title="Dino Run 🦖", layout="wide")
st.title("🦖 Dino Run - Streamlit Edition")

# 프레임 자동 갱신 (0.5초 간격)
st_autorefresh(interval=500, key="refresh")

# 초기화
if "dino_y" not in st.session_state:
    st.session_state.dino_y = 0  # 0: 지상, 1: 점프
    st.session_state.score = 0
    st.session_state.obstacles = [15]  # 장애물 위치 (화면 오른쪽에서 시작)
    st.session_state.velocity = 0
    st.session_state.game_over = False
    st.session_state.tick = 0

# 점프 처리
jump = st.button("⬆️ Jump")
if jump and st.session_state.dino_y == 0:
    st.session_state.velocity = 1.5

# 중력 및 점프 상태 계산
if st.session_state.dino_y > 0 or st.session_state.velocity > 0:
    st.session_state.dino_y += st.session_state.velocity
    st.session_state.velocity -= 0.5  # 중력
    if st.session_state.dino_y <= 0:
        st.session_state.dino_y = 0
        st.session_state.velocity = 0

# 장애물 이동
new_obstacles = []
for obs in st.session_state.obstacles:
    if obs > 0:
        new_obstacles.append(obs - 1)
# 새 장애물 생성
if random.random() < 0.1:
    new_obstacles.append(30)
st.session_state.obstacles = new_obstacles

# 충돌 검사
for obs in st.session_state.obstacles:
    if obs == 3 and st.session_state.dino_y < 1:
        st.session_state.game_over = True

# 화면 렌더링
cols = st.columns(30)
for i in range(30):
    if i == 3:
        if st.session_state.dino_y > 0:
            cols[i].markdown("🦖")  # 점프 중
        else:
            cols[i].markdown("🦖")  # 지상
    elif i in st.session_state.obstacles:
        cols[i].markdown("🌵")
    else:
        cols[i].markdown("⠀")

# 점수 증가
if not st.session_state.game_over:
    st.session_state.score += 1
    st.caption(f"Score: {st.session_state.score}")
else:
    st.error("💥 Game Over!")
    st.caption(f"Final Score: {st.session_state.score}")
    if st.button("🔄 Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
