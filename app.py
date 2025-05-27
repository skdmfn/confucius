import streamlit as st
import random

st.set_page_config(page_title="Star Trek Advanced (Streamlit Edition)", layout="wide")
st.title("🖖 Star Trek Advanced - Streamlit Edition")

st.markdown("""
### 📘 How to Play

Welcome, Captain! Your mission is to destroy all Klingon ships before stardate 2265.

**Command Reference:**
- `NAV dx dy` — Navigate by relative direction (e.g., `NAV 1 -1`)
- `SRS` — Short Range Scan (shows current sector)
- `LRS` — Long Range Scan (shows quadrant overview)
- `PHA` — Fire phasers (hits Klingons adjacent to Enterprise)
- `TOR x y` — Fire photon torpedo at absolute sector coordinates
- `DOCK` — Dock at starbase to refuel/rearm
- `COMP` — Access ship computer for info

**Legend:**
- `E`: Enterprise (your ship)
- `K`: Klingon ship
- `B`: Starbase
- `.`: Empty space

Use energy and torpedoes wisely! Move carefully, Klingons also move!
""")

if "game" not in st.session_state:
    st.session_state.game = {
        "sector": [["." for _ in range(8)] for _ in range(8)],
        "ship_pos": [4, 4],
        "energy": 3000,
        "torpedoes": 10,
        "klingons": [],
        "stardate": 2250,
        "deadline": 2265,
        "base_pos": [],
        "log": [],
        "game_over": False,
    }

game = st.session_state.game

# 초기 배치
if not game["klingons"]:
    for _ in range(3):
        while True:
            x, y = random.randint(0,7), random.randint(0,7)
            if (x,y) != tuple(game["ship_pos"]):
                break
        game["klingons"].append([x,y])
        game["sector"][x][y] = "K"
    while True:
        bx, by = random.randint(0,7), random.randint(0,7)
        if game["sector"][bx][by] == ".":
            game["base_pos"] = [bx, by]
            game["sector"][bx][by] = "B"
            break
    sx, sy = game["ship_pos"]
    game["sector"][sx][sy] = "E"


def log(msg):
    game["log"].append(msg)
    if len(game["log"]) > 20:
        game["log"].pop(0)


def move_klingons():
    new_positions = []
    for kx, ky in game["klingons"]:
        possible_moves = []
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = kx + dx, ky + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if game["sector"][nx][ny] == ".":
                        possible_moves.append((nx, ny))
        if possible_moves:
            nx, ny = random.choice(possible_moves)
        else:
            nx, ny = kx, ky
        new_positions.append([nx, ny])
    # 맵 갱신
    for kx, ky in game["klingons"]:
        game["sector"][kx][ky] = "."
    for nx, ny in new_positions:
        if [nx, ny] == game["ship_pos"]:
            log("💥 Klingon ship crashed into you! Game Over.")
            game["game_over"] = True
        game["sector"][nx][ny] = "K"
    game["klingons"] = new_positions


def short_range_scan():
    lines = []
    border = "+---"*8 + "+"
    lines.append(border)
    for row in game["sector"]:
        line = "|"
        for c in row:
            line += f" {c} |"
        lines.append(line)
        lines.append(border)
    return "\n".join(lines)


def long_range_scan():
    klingon_count = len(game["klingons"])
    base_x, base_y = game["base_pos"]
    sx, sy = game["ship_pos"]
    quadrant_map = [["." for _ in range(8)] for _ in range(8)]
    quadrant_map[base_x][base_y] = "B"
    quadrant_map[sx][sy] = "E"
    for kx, ky in game["klingons"]:
        quadrant_map[kx][ky] = "K"
    lines = []
    border = "+---"*8 + "+"
    lines.append(border)
    for row in quadrant_map:
        line = "|"
        for c in row:
            line += f" {c} |"
        lines.append(line)
        lines.append(border)
    summary = f"Klingons: {klingon_count}, Starbase at {game['base_pos']}, Enterprise at {game['ship_pos']}"
    return "\n".join(lines) + "\n" + summary


def dock():
    if game["ship_pos"] == game["base_pos"]:
        game["energy"] = 3000
        game["torpedoes"] = 10
        log("⚡ Docked at starbase. Energy and torpedoes replenished.")
    else:
        log("❌ You must be at the starbase to dock.")


def process_command(cmd):
    if game["game_over"]:
        log("Game over. Restart to play again.")
        return

    cmd = cmd.strip().upper()
    log(f"> {cmd}")
    parts = cmd.split()
    if not parts:
        log("❓ Enter a command.")
        return

    c = parts[0]

    if c == "NAV":
        if len(parts) != 3:
            log("❌ Invalid NAV command format. Use: NAV dx dy")
            return
        try:
            dx, dy = int(parts[1]), int(parts[2])
        except:
            log("❌ NAV dx dy must be integers.")
            return
        sx, sy = game["ship_pos"]
        nsx, nsy = sx + dx, sy + dy
        if 0 <= nsx < 8 and 0 <= nsy < 8:
            if game["sector"][nsx][nsy] == "K":
                log("💥 You crashed into a Klingon ship! Game Over.")
                game["game_over"] = True
                return
            game["sector"][sx][sy] = "."
            game["sector"][nsx][nsy] = "E"
            game["ship_pos"] = [nsx, nsy]
            game["energy"] -= 100
            move_klingons()
        else:
            log("❌ Navigation out of bounds.")

    elif c == "SRS":
        scan = short_range_scan()
        log("📡 Short Range Scan:\n" + scan)

    elif c == "LRS":
        scan = long_range_scan()
        log("🔭 Long Range Scan:\n" + scan)

    elif c == "PHA":
        sx, sy = game["ship_pos"]
        hit = False
        to_remove = []
        for kx, ky in game["klingons"]:
            if abs(kx - sx) <= 1 and abs(ky - sy) <= 1:
                log(f"🔫 Hit Klingon at ({kx},{ky})")
                game["sector"][kx][ky] = "."
                to_remove.append([kx, ky])
                game["energy"] -= 200
                hit = True
        for k in to_remove:
            game["klingons"].remove(k)
        if not hit:
            log("💨 No Klingon in range!")
        else:
            move_klingons()

    elif c == "TOR":
        if game["torpedoes"] <= 0:
            log("❌ No torpedoes left!")
            return
        if len(parts) != 3:
            log("❌ Invalid TOR format. Use: TOR x y")
            return
        try:
            tx, ty = int(parts[1]), int(parts[2])
        except:
            log("❌ TOR coordinates must be integers.")
            return
        if 0 <= tx < 8 and 0 <= ty < 8:
            if [tx, ty] in game["klingons"]:
                game["klingons"].remove([tx, ty])
                game["sector"][tx][ty] = "."
                log(f"💥 Klingon destroyed at ({tx},{ty})!")
            else:
                log("🎯 Torpedo missed!")
            game["torpedoes"] -= 1
            move_klingons()
        else:
            log("❌ TOR target out of bounds.")

    elif c == "DOCK":
        dock()

    elif c == "COMP":
        log(f"🖥️ Ship status - Energy: {game['energy']}, Torpedoes: {game['torpedoes']}, Stardate: {game['stardate']}")

    else:
        log("❌ Unknown command.")

    # 게임 종료 조건 체크
    if game["energy"] <= 0:
        log("⚠️ Energy depleted. You lost!")
        game["game_over"] = True
    if len(game["klingons"]) == 0:
        log("🎉 All Klingons destroyed. You won!")
        game["game_over"] = True
    if game["stardate"] > game["deadline"]:
        log("⌛ Stardate expired. You lost!")
        game["game_over"] = True

    game["stardate"] += 1


# UI 입력
cmd_input = st.text_input("Enter command:", key="cmd_input")

if st.button("Execute") or cmd_input:
    process_command(cmd_input)
    # 입력창 초기화
    st.session_state.cmd_input = ""

# 게임 로그 출력
st.text_area("Log", value="\n".join(game["log"]), height=400)

# 상태 요약
st.markdown(f"""
**Energy:** {game['energy']}  
**Torpedoes:** {game['torpedoes']}  
**Stardate:** {game['stardate']} / {game['deadline']}  
**Klingons Remaining:** {len(game['klingons'])}
""")

if game["game_over"]:
    st.markdown("## 🚀 Game Over! Refresh the page to start a new game.")
