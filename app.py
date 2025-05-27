import streamlit as st
import random

st.set_page_config(page_title="Star Trek (Enhanced)", layout="wide")
st.title("🖖 Star Trek (Enhanced) - Streamlit Edition")

st.markdown("""
### 📘 How to Play

Welcome, Captain! Your mission is to destroy all Klingon ships before stardate 2265.

**Command Reference:**
- `NAV dx dy` — Navigate by relative direction. Moves your ship by dx, dy (range -1 to 1).
- `SRS` — Short Range Scan (shows current 8x8 sector).
- `LRS` — Long Range Scan (shows surrounding quadrants summary).
- `PHA` — Fire phasers (hits Klingons adjacent to Enterprise).
- `TOR x y` — Launch photon torpedo at absolute sector coordinates (0-7).
- `DOCK` — Dock at starbase to fully recharge energy and torpedoes.
- `COMP` — Access onboard computer help and status.

**Legend:**
- `E`: Your ship (the Enterprise)
- `K`: Klingon ship
- `B`: Starbase
- `.`: Empty space

Use your energy and torpedoes wisely!
""")

# === 초기 상태 설정 및 저장 ===
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
        "win": False,
        "quadrant": [[random.randint(0, 3) for _ in range(8)] for _ in range(8)],  # For LRS, random klingon counts
    }

game = st.session_state.game

# === 게임 초기 배치 ===
if not game["klingons"]:
    # Clear sector
    game["sector"] = [["." for _ in range(8)] for _ in range(8)]
    # Place Klingons randomly, 4 ships
    game["klingons"] = []
    for _ in range(4):
        while True:
            x, y = random.randint(0, 7), random.randint(0, 7)
            if game["sector"][x][y] == "." and (x, y) != tuple(game["ship_pos"]):
                game["sector"][x][y] = "K"
                game["klingons"].append([x, y])
                break
    # Place starbase
    while True:
        bx, by = random.randint(0, 7), random.randint(0, 7)
        if game["sector"][bx][by] == "." and (bx, by) != tuple(game["ship_pos"]):
            game["sector"][bx][by] = "B"
            game["base_pos"] = [bx, by]
            break
    # Place Enterprise
    sx, sy = game["ship_pos"]
    game["sector"][sx][sy] = "E"

# === 도킹 처리 함수 ===
def dock():
    sx, sy = game["ship_pos"]
    if game["sector"][sx][sy] == "B":
        game["energy"] = 3000
        game["torpedoes"] = 10
        game["log"].append("⚡ Docked at starbase. Energy and torpedoes fully recharged.")
    else:
        game["log"].append("❌ Not at a starbase. Cannot dock.")

# === 적 움직임 처리 함수 ===
def move_klingons():
    new_positions = []
    for kx, ky in game["klingons"]:
        # Random move -1,0,1 in x and y, stay in bounds, no collision with Enterprise
        game["sector"][kx][ky] = "."
        dx, dy = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
        nx, ny = kx + dx, ky + dy
        if 0 <= nx < 8 and 0 <= ny < 8:
            if game["sector"][nx][ny] in [".", "B"]:  # Can move on empty or starbase
                new_positions.append([nx, ny])
            else:
                new_positions.append([kx, ky])  # stay if blocked
        else:
            new_positions.append([kx, ky])  # stay if out of bounds
    game["klingons"] = new_positions
    # Place klingons in sector map
    for (kx, ky) in game["klingons"]:
        # If collides with Enterprise, game over
        if [kx, ky] == game["ship_pos"]:
            game["log"].append("💥 A Klingon ship rammed the Enterprise! Game Over.")
            game["game_over"] = True
            return
        game["sector"][kx][ky] = "K"

# === 명령어 처리 함수 ===
def process_command(cmd):
    if game["game_over"] or game["win"]:
        return
    cmd = cmd.strip().upper()
    game["log"].append(f"> {cmd}")

    sx, sy = game["ship_pos"]

    if cmd.startswith("NAV"):
        parts = cmd.split()
        if len(parts) != 3:
            game["log"].append("❌ Invalid NAV command format. Use: NAV dx dy")
            return
        try:
            dx, dy = int(parts[1]), int(parts[2])
            if dx not in [-1, 0, 1] or dy not in [-1, 0, 1]:
                game["log"].append("❌ NAV dx dy must be between -1 and 1")
                return
            nx, ny = sx + dx, sy + dy
            if not (0 <= nx < 8 and 0 <= ny < 8):
                game["log"].append("❌ Navigation out of bounds.")
                return
            if game["sector"][nx][ny] == "K":
                game["log"].append("💥 You crashed into a Klingon ship! Game Over.")
                game["game_over"] = True
                return
            # Move Enterprise
            game["sector"][sx][sy] = "."
            game["sector"][nx][ny] = "E"
            game["ship_pos"] = [nx, ny]
            game["energy"] -= 100
            # Klingons move after you
            move_klingons()
        except ValueError:
            game["log"].append("❌ NAV command dx and dy must be integers.")
    elif cmd == "SRS":
        # Show current sector
        scan_lines = []
        scan_lines.append("+---"*8 + "+")
        for row in game["sector"]:
            line = "| " + " | ".join(row) + " |"
            scan_lines.append(line)
            scan_lines.append("+---"*8 + "+")
        game["log"].append("📡 Short Range Scan:\n" + "\n".join(scan_lines))
    elif cmd == "LRS":
        # Long Range Scan: show klingon counts in nearby quadrants as a grid
        lrs_lines = []
        lrs_lines.append("🛰️ Long Range Scan (Klingons per quadrant)")
        lrs_lines.append("+----"*8 + "+")
        for row in game["quadrant"]:
            line = "| " + " | ".join(str(x) for x in row) + " |"
            lrs_lines.append(line)
            lrs_lines.append("+----"*8 + "+")
        game["log"].append("\n".join(lrs_lines))
    elif cmd == "PHA":
        # Phaser attack adjacent klingons
        sx, sy = game["ship_pos"]
        hit_any = False
        for k in game["klingons"][:]:
            kx, ky = k
            if abs(kx - sx) <= 1 and abs(ky - sy) <= 1:
                game["sector"][kx][ky] = "."
                game["klingons"].remove(k)
                game["energy"] -= 200
                game["log"].append(f"🔫 Hit Klingon at ({kx},{ky})")
                hit_any = True
        if not hit_any:
            game["log"].append("💨 No Klingon in range!")
        else:
            # Klingons move after phaser fire
            move_klingons()
    elif cmd.startswith("TOR"):
        if game["torpedoes"] <= 0:
            game["log"].append("❌ No torpedoes left!")
            return
        parts = cmd.split()
        if len(parts) != 3:
            game["log"].append("❌ Invalid TOR format. Use: TOR x y")
            return
        try:
            tx, ty = int(parts[1]), int(parts[2])
            if not (0 <= tx < 8 and 0 <= ty < 8):
                game["log"].append("❌ TOR coordinates out of bounds (0-7).")
                return
            if [tx, ty] in game["klingons"]:
                game["klingons"].remove([tx, ty])
                game["sector"][tx][ty] = "."
                game["log"].append(f"💥 Klingon destroyed at ({
