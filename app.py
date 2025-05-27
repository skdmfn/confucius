import streamlit as st

# 게임 초기 상태 설정
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

# 좌표 유효성 검사
def in_bounds(x, y, size):
    return 0 <= x < size and 0 <= y < size

# 로그 기록 함수
def log(msg):
    game["log"].append(msg)

# 게임판 출력 함수
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
                cell = " E "  # E: Player (Enterprise)
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

# 단기 스캔 (player 주변 3x3)
def short_range_scan():
    px, py = game["player_pos"]
    size = game["grid_size"]
    scan_size = 3
    half = scan_size // 2

    lines = []
    horiz_line = "+---" * scan_size + "+"
    lines.append(horiz_line)

    for dy in range(-half, half + 1):
        row = "|"
        for dx in range(-half, half + 1):
            x, y = px + dx, py + dy
            if in_bounds(x, y, size):
                if [x, y] == [px, py]:
                    cell = " E "
                elif [x, y] in game["klingons"]:
                    cell = " K "
                elif [x, y] in game["bases"]:
                    cell = " B "
                elif [x, y] in game["enemies"]:
                    cell = " X "
                else:
                    cell = " . "
            else:
                cell = "   "
            row += cell + "|"
        lines.append(row)
        lines.append(horiz_line)
    return "\n".join(lines)

# 장거리 스캔 (전체 맵 표시)
def long_range_scan():
    return render_grid()

# 플레이어 이동
def nav(dx, dy):
    if game["game_over"]:
        log("❌ Game over. Restart to play again.")
        return
    px, py = game["player_pos"]
    nx, ny = px + dx, py + dy
    if not in_bounds(nx, ny, game["grid_size"]):
        log("❌ Navigation out of bounds.")
        return
    game["player_pos"] = [nx, ny]
    log(f"➡️ Moved to ({nx}, {ny}).")
    klingon_move()

# 클링온 한 칸 이동 (랜덤 혹은 플레이어 쪽으로)
def klingon_move():
    from random import choice

    px, py = game["player_pos"]
    new_positions = []

    for kx, ky in game["klingons"]:
        # 간단하게 플레이어 쪽으로 1칸 이동 시도
        dx = 0
        dy = 0
        if kx < px:
            dx = 1
        elif kx > px:
            dx = -1
        if ky < py:
            dy = 1
        elif ky > py:
            dy = -1

        nkx, nky = kx + dx, ky + dy
        # 범위 내 & 플레이어 위치 아님
        if in_bounds(nkx, nky, game["grid_size"]) and [nkx, nky] != game["player_pos"]:
            new_positions.append([nkx, nky])
        else:
            new_positions.append([kx, ky])
    game["klingons"] = new_positions

# 어뢰 발사 (Torpedo)
def torpedo(dx, dy):
    if game["game_over"]:
        log("❌ Game over. Restart to play again.")
        return

    px, py = game["player_pos"]
    tx, ty = px + dx, py + dy
    if not in_bounds(tx, ty, game["grid_size"]):
        log("❌ Torpedo out of bounds.")
        return

    if [tx, ty] in game["klingons"]:
        game["klingons"].remove([tx, ty])
        log(f"💥 Klingon destroyed at ({tx}, {ty})!")
        if len(game["klingons"]) == 0:
            log("🏆 All Klingons destroyed. You win!")
            game["game_over"] = True
    else:
        log("🎯 Torpedo missed!")

# 도킹 (Dock)
def dock():
    px, py = game["player_pos"]
    if [px, py] in game["bases"]:
        log("⚓ Docked successfully at base.")
    else:
        log("❌ Not at a base. Move to a base to dock.")

# 명령어 처리
def process_command(cmd):
    parts = cmd.strip().upper().split()
    if len(parts) == 0:
        log("❌ No command entered.")
        return

    command = parts[0]

    try:
        if command == "NAV":
            if len(parts) != 3:
                log("❌ Invalid NAV command format. Use: NAV dx dy")
                return
            dx, dy = int(parts[1]), int(parts[2])
            nav(dx, dy)
        elif command == "SRS":
            log("📡 Short Range Scan:")
            log(short_range_scan())
        elif command == "LRS":
            log("📡 Long Range Scan:")
            log(long_range_scan())
        elif command == "TOR":
            if len(parts) != 3:
                log("❌ Invalid TOR command format. Use: TOR dx dy")
                return
            dx, dy = int(parts[1]), int(parts[2])
            torpedo(dx, dy)
        elif command == "DOCK":
            dock()
        elif command == "HELP":
            log("Commands: NAV dx dy, SRS, LRS, TOR dx dy, DOCK, HELP")
        else:
            log(f"❌ Unknown command: {command}")
    except ValueError:
        log("❌ Invalid numeric value in command.")

# Streamlit 앱 시작

# 세션 상태 초기화
if "game" not in st.session_state:
    st.session_state["game"] = init_game()

game = st.session_state["game"]

if "cmd_input" not in st.session_state:
    st.session_state["cmd_input"] = ""

st.title("🚀 Star Trek Command Console")

st.text_area("Game Log", value="\n".join(game["log"]), height=300, key="game_log", disabled=True)

cmd_input = st.text_input("Enter command:", key="cmd_input")

if st.button("Execute") or (cmd_input and not game["game_over"]):
    process_command(cmd_input)
    # 입력 초기화
    st.session_state["cmd_input"] = ""

# 게임판 보여주기
st.text("Current Sector:")
st.text(render_grid())

