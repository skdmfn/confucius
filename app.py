import streamlit as st
import random

st.set_page_config(page_title="Star Trek (1971 Remake)", layout="wide")
st.title("🖖 Star Trek (1971) - Streamlit Edition")

st.markdown("""
### 📘 How to Play

Welcome, Captain! Your mission is to destroy all Klingon ships before stardate 2265.

**Command Reference:**
- `NAV dx dy` — Navigate by relative direction. Example: `NAV 1 -1` moves diagonally.
- `SRS` — Short Range Scan of current 8x8 sector.
- `PHA` — Fire phasers (hits Klingons adjacent to Enterprise).
- `TOR x y` — Launch photon torpedo at absolute sector position (e.g., `TOR 2 3`).

**Legend:**
- `E`: Your ship (the Enterprise)
- `K`: Klingon ship
- `B`: Starbase
- ` `: Empty space

Use your energy and torpedoes wisely!
""")

# 초기 상태 설정
if "game" not in st.session_state:
    st.session_state.game = {
        "quadrant": [[0]*8 for _ in range(8)],  # 8x8 은하계
        "sector": [[" "]*8 for _ in range(8)],  # 8x8 섹터
        "ship_pos": [4, 4],
        "energy": 3000,
        "torpedoes": 10,
        "klingons": [],
        "stardate": 2250,
        "deadline": 2265,
        "base_pos": [],
        "log": [],
    }

# 게임 상태 불러오기
game = st.session_state.game

# 초기 배치 (1회만)
if not game["klingons"]:
    for _ in range(3):
        x, y = random.randint(0,7), random.randint(0,7)
        game["klingons"].append([x, y])
        game["sector"][x][y] = "K"
    base_x, base_y = random.randint(0,7), random.randint(0,7)
    game["base_pos"] = [base_x, base_y]
    game["sector"][base_x][base_y] = "B"
    sx, sy = game["ship_pos"]
    game["sector"][sx][sy] = "E"

# 명령어 처리 함수
def process_command(cmd):
    cmd = cmd.strip().upper()
    game["log"].append(f"> {cmd}")
    if cmd.startswith("NAV"):
        try:
            _, dx, dy = cmd.split()
            dx, dy = int(dx), int(dy)
            sx, sy = game["ship_pos"]
            nsx, nsy = sx + dx, sy + dy
            if 0 <= nsx < 8 and 0 <= nsy < 8:
                if game["sector"][nsx][nsy] == "K":
                    game["log"].append("💥 You crashed into a Klingon ship! Game Over.")
                    st.session_state.game_over = True
                    return
                game["sector"][sx][sy] = " "
                game["sector"][nsx][nsy] = "E"
                game["ship_pos"] = [nsx, nsy]
                game["energy"] -= 100
            else:
                game["log"].append("❌ Navigation out of bounds.")
        except:
            game["log"].append("❌ Invalid NAV command format. Use: NAV dx dy")
    elif cmd.startswith("SRS"):
        srs = "\n".join([" ".join(row) for row in game["sector"]])
        game["log"].append(f"📡 Short Range Scan:\n{srs}")
    elif cmd.startswith("PHA"):
        sx, sy = game["ship_pos"]
        hit = False
        for k in game["klingons"][:]:
            kx, ky = k
            if abs(kx - sx) <= 1 and abs(ky - sy) <= 1:
                game["log"].append(f"🔫 Hit Klingon at ({kx},{ky})")
                game["sector"][kx][ky] = " "
                game["klingons"].remove(k)
                game["energy"] -= 200
                hit = True
        if not hit:
            game["log"].append("💨 No Klingon in range!")
    elif cmd.startswith("TOR"):
        if game["torpedoes"] <= 0:
            game["log"].append("❌ No torpedoes left!")
        else:
            try:
                _, tx, ty = cmd.split()
                tx, ty = int(tx), int(ty)
                if [tx, ty] in game["klingons"]:
                    game["klingons"].remove([tx, ty])
                    game["sector"][tx][ty] = " "
                    game["log"].append(f"💥 Klingon destroyed at ({tx},{ty})!")
                else:
                    game["log"].append("🎯 Torpedo missed!")
                game["torpedoes"] -= 1
            except:
                game["log"].append("❌ Invalid TOR format. Use: TOR x y")
    else:
        game["log"].append("❓ Unknown command")

# 명령어 입력창
cmd = st.text_input("Enter Command (NAV dx dy, PHA, TOR x y, SRS)")
if cmd:
    process_command(cmd)

# 정보 출력
st.markdown(f"**Stardate**: {game['stardate']}   |  **Energy**: {game['energy']}   |  **Torpedoes**: {game['torpedoes']}")

# 로그 출력
st.subheader("Command Log")
st.text("\n".join(game["log"][-10:]))

# 승리 / 패배 조건
if "game_over" in st.session_state and st.session_state.game_over:
    st.error("Game Over - You crashed into an enemy ship!")
elif len(game["klingons"]) == 0:
    st.success("All Klingons destroyed. You win!")
