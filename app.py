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
        if len(parts) == 3 and parts[1].lstrip("-").isdigit() and parts[2].lstrip("-").isdigit():
            dx = int(parts[1])
            dy = int(parts[2])
            move_player(dx, dy)
        else:
            log("❌ Invalid NAV command format. Use: NAV dx dy")
    elif parts[0] == "TOR":
        if len(parts) == 3 and parts[1].isdigit() and parts[2].isdigit():
            tx = int(parts[1])
            ty = int(parts[2])
            fire_torpedo(tx, ty)
        else:
            log("❌ Invalid TOR command format. Use: TOR x y")
    elif parts[0] == "SRS":
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

# --- Streamlit 상태 초기화 ---
if "game" not in st.session_state:
    st.session_state.game = init_game()
game = st.session_state.game

# --- UI 구성 ---
st.title("🚀 Star Trek Command Console")

st.text_area("Game Log", value="\n".join(game["log"]), height=300, disabled=True)

cmd = st.text_input("Enter command:", value="", key="cmd_input")

if st.button("Execute"):
    process_command(cmd)
    # 💡 Reset은 텍스트 입력창이 아닌 다른 변수로 우회
    st.experimental_rerun()  # rerun을 사용해 입력 초기화

st.text("Current Sector:")
st.text(render_grid())
