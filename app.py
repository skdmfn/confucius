import streamlit as st

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

def in_bounds(x, y, size):
    return 0 <= x < size and 0 <= y < size

def log(msg):
    game["log"].append(msg)

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

def long_range_scan():
    return render_grid()

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

def klingon_move():
    px, py = game["player_pos"]
    new_positions = []
    for kx, ky in game["klingons"]:
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
        if in_bounds(nkx, nky, game["grid_size"]) and [nkx, nky] != game["player_pos"]:
            new_positions.append([nkx, nky])
        else:
            new_positions.append([kx, ky])
    game["klingons"] = new_positions

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

def dock():
    px, py = game["player_pos"]
    if [px, py] in game["bases"]:
        log("⚓ Docked successfully at base.")
    else:
        log("❌ Not at a base. Move to a base to dock.")

def process_command(cmd):
    parts = cmd.strip().upper().split()
    if len(parts) == 0 or parts[0] == "":
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

# 세션 상태 초기화: game, cmd_input 없으면 초기화
if "game" not in st.session_state:
    st.session_state.game = init_game()

if "cmd_input" not in st.session_state:
    st.session_state.cmd_input = ""

game = st.session_state.game

st.title("🚀 Star Trek Command Console")

st.text_area("Game Log", value="\n".join(game["log"]), height=300, key="game_log", disabled=True)

# cmd_input을 key만 지정해서 상태와 연결 (value는 지정하지 말 것)
cmd_input = st.text_input("Enter command:", key="cmd_input")

if st.button("Execute"):
    process_command(cmd_input)
    # 버튼 눌렀을 때만 cmd_input 비우기
    st.session_state.cmd_input = ""

st.text("Current Sector:")
st.text(render_grid())
