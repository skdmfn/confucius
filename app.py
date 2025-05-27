import streamlit as st

# --- 게임 초기화 함수 ---
def init_game():
    return {
        "grid_size": 8,
        "player_pos": [3, 3],
        "klingons": [[0, 0], [1, 1], [1, 0]],
        "bases": [[4, 7]],
        "enemies": [[5, 5]],
        "game_over": False,
        "log": [],
    }

# --- 로그 기록 함수 ---
def log(msg):
    game["log"].append(msg)

# --- 현재 지도 출력 함수 ---
def render_grid():
    size = game["grid_size"]
    px, py = game["player_pos"]
    lines = []
    horiz_line = "+---" * size + "+"
    lines.append(horiz_line)
    for y in range(size):
        row = "|"
        for x in range(size):
            cell = " . "
            if [x, y] == [px, py]:
                cell = " E "
            elif [x, y] in game["klingons"]:
                cell = " K "
            elif [x, y] in game["bases"]:
                cell = " B "
            elif [x, y] in game["enemies"]:
                cell = " X "
            row += cell + "|"
        lines.append(row)
        lines.append(horiz_line)
    return "\n".join(lines)

# --- 명령 처리 함수 ---
def process_command(cmd):
    cmd = cmd.strip().upper()
    if not cmd:
        log("❌ No command entered.")
        return

    parts = cmd.split()
    if parts[0] == "NAV":
        # NAV x y 명령어 예시: 좌표로 플레이어 이동
        if len(parts) == 3 and parts[1].lstrip("-").isdigit() and parts[2].lstrip("-").isdigit():
            dx = int(parts[1])
            dy = int(parts[2])
            move_player(dx, dy)
        else:
            log("❌ Invalid NAV command format. Use: NAV dx dy")
    elif parts[0] == "TOR":
        # TOR x y 토르피도 발사 명령 예시
        if len(parts) == 3 and parts[1].lstrip("-").isdigit() and parts[2].lstrip("-").isdigit():
            tx = int(parts[1])
            ty = int(parts[2])
            fire_torpedo(tx, ty)
        else:
            log("❌ Invalid TOR command format. Use: TOR x y")
    elif parts[0] == "SRS":
        # SRS 단거리 스캔 출력
        log("📡 Short Range Scan:")
        log(render_grid())
    else:
        log(f"❌ Unknown command: {cmd}")

# --- 플레이어 이동 ---
def move_player(dx, dy):
    new_x = game["player_pos"][0] + dx
    new_y = game["player_pos"][1] + dy
    size = game["grid_size"]
    if 0 <= new_x < size and 0 <= new_y < size:
        game["player_pos"] = [new_x, new_y]
        log(f"🚀 Moved to ({new_x}, {new_y})")
    else:
        log("❌ Move out of bounds!")

# --- 토르피도 발사 ---
def fire_torpedo(tx, ty):
    if [tx, ty] in game["klingons"]:
        game["klingons"].remove([tx, ty])
        log(f"💥 Klingon destroyed at ({tx}, {ty})")
    else:
        log("🎯 Torpedo missed!")

# --- Streamlit 앱 시작 ---
if "game" not in st.session_state:
    st.session_state.game = init_game()
if "cmd_input" not in st.session_state:
    st.session_state.cmd_input = ""

game = st.session_state.game

st.title("🚀 Star Trek Command Console")

# 로그 출력 (읽기전용)
st.text_area("Game Log", value="\n".join(game["log"]), height=300, disabled=True)

# 명령어 입력창
cmd = st.text_input("Enter command:", key="cmd_input")

# 명령 실행 버튼 누르면 처리하고 입력창 초기화
if st.button("Execute"):
    process_command(cmd)
    st.session_state.cmd_input = ""  # **여기서만 상태 변경!**

# 현재 위치 출력
st.text("Current Sector:")
st.text(render_grid())
