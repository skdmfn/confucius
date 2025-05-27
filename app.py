import streamlit as st
import random

st.set_page_config(page_title="Dino Run", layout="centered")
st.title("🦖 Dino Run - Text Edition")

# 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.jump = False
    st.session_state.game_over = False
    st.session_state.obstacle = False
    st.session_state.tick = 0

# 게임 오버 처리
if st.session_state.game_over:
    st.error("💥 Game Over!")
    st.write(f"Your final score: {st.session_state.score}")
    if st.button("🔄 Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    st.stop()

# UI: 점프 버튼
if st.button("⬆️ Jump"):
    st.session_state.jump = True

# 새로운 장애물 생성 (일정 간격)
if st.session_state.tick % 3 == 0:
    st.session_state.obstacle = random.choice([True, False])

# 충돌 검사
if st.session_state.obstacle and not st.session_state.jump:
    st.session_state.game_over = True

# 화면 그리기
dino = "🦖⬆️" if st.session_state.jump else "🦖"
cactus = "🌵" if st.session_state.obstacle else "⠀"
st.write(f"{dino} {' ' * 10} {cactus}")

# 점수 및 상태 업데이트
st.session_state.score += 1
st.session_state.jump = False
st.session_state.tick += 1

# 다음 프레임 진행 버튼
if st.button("▶️ Next Step"):
    pass  # 아무것도 안 해도 버튼 클릭 시 UI 갱신
else:
    st.info("⬆️ Jump를 누르고 ▶️ Next Step을 눌러보세요!")
