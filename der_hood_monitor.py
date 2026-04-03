import requests
import time
import schedule
from datetime import datetime

# ============================================================
#  EDIT THESE TWO LINES WHEN THE GAME LINK CHANGES
# ============================================================
GAME_URL = "https://www.roblox.com/games/78871371189272/DER-HOOD"
WEBHOOK_URL = "https://discord.com/api/webhooks/1489524124840755271/v0TakNYNeWG0YjuBqJfU5Qi_LXJGKa3azgDVQgieQhR2-gykKUtJdJFEkFkFXThLxb6V"
# ============================================================

CHECK_INTERVAL_HOURS = 1


def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def send_discord(message):
    try:
        r = requests.post(WEBHOOK_URL, json={"content": message}, timeout=10)
        if r.status_code in (200, 204):
            log(f'Discord message sent: "{message}"')
        else:
            log(f"Discord returned status {r.status_code}")
    except Exception as e:
        log(f"Failed to send Discord message: {e}")


def check_game():
    log(f"Checking: {GAME_URL}")
    try:
        r = requests.get(GAME_URL, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        is_up = r.status_code == 200
    except Exception as e:
        log(f"Request error: {e}")
        is_up = False

    if is_up:
        log("Game is UP")
        send_discord("der is still up")
    else:
        log("Game is DOWN")
        send_discord("der is down")
        log("Game is down — stopping monitor.")
        raise SystemExit(0)


if __name__ == "__main__":
    log("Der Hood monitor started.")
    log(f"Checking every {CHECK_INTERVAL_HOURS} hour(s).")
    log(f"Game URL: {GAME_URL}")

    # Run immediately on start
    check_game()

    # Schedule hourly checks
    schedule.every(CHECK_INTERVAL_HOURS).hours.do(check_game)

    while True:
        schedule.run_pending()
        time.sleep(30)
