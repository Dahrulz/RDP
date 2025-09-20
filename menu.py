#!/usr/bin/env python3
import os, sys, subprocess, shutil, json, time
import readchar

URL   = "https://github.com/Dahrulz/RDP/actions"
REPO  = "Dahrulz/RDP"
WF    = "main.yml"
TS_PKG = "com.tailscale.ipn"
PLAY   = "https://play.google.com/store/apps/details?id=com.tailscale.ipn"

# ---------- AUTO-INSTALL ----------
def install(pkg):
    if shutil.which(pkg) is None:
        print(f"\n📦 Installing {pkg} …")
        subprocess.run(["pkg", "install", pkg, "-y"], check=True)

def pip_install(mod):
    try: __import__(mod)
    except ImportError:
        print(f"\n📦 Installing python-{mod} …")
        subprocess.run([sys.executable, "-m", "pip", "install", mod], check=True)

install("gh"); install("python"); pip_install("readchar")
# ----------------------------------

def clear(): os.system("clear")

def banner(title="TERMUX MENU BROWSER v1.4"):
    bar = "┌" + "─"*30 + "┐"; print(bar)
    print(f"│{title:^30}│")
    print("└" + "─"*30 + "┘")

# ---------- KEY FILTER ----------
ALLOWED = {readchar.key.UP, readchar.key.DOWN, readchar.key.ENTER,
           "\r", "\n", "q", readchar.key.CTRL_C}
def read_key_safe():
    while True:
        k = readchar.readkey()
        if k in ALLOWED: return k
# --------------------------------

# WARNA: biru terang = pilihan, putih = lainnya
def show_menu(items, selected):
    clear(); banner()
    for idx, text in enumerate(items, 1):
        if idx == selected:
            print(f"\033[1;36m▶ {idx}. {text}\033[0m")   # CYAN BRIGHT
        else:
            print(f"  {idx}. {text}")                   # WHITE NORMAL
    print("\n[↑↓] Navigate   [Enter] Choose   [q] Quit")

def success_screen():
    clear(); banner("SUCCESS")
    print("\n✅ Success! Link telah dibuka di browser.\n")
    print("\033[1;36mTekan Enter untuk kembali …\033[0m", end="", flush=True)
    while read_key_safe() not in (readchar.key.ENTER, "\r", "\n"): pass

def total_workflows():
    try:
        out = subprocess.check_output(["gh", "workflow", "list", "--repo", REPO, "--json", "id"],
                                      stderr=subprocess.DEVNULL)
        return len(json.loads(out))
    except Exception:
        return 0

# ---------- SUB-MENUS (ALL COLOURED) ----------
def run_workflow():
    clear(); banner("RUN WORKFLOWS")
    if subprocess.run(["gh", "auth", "status"], capture_output=True).returncode != 0:
        print("\n🔑 Belum login GitHub. Ikuti prompt di bawah:")
        subprocess.run(["gh", "auth", "login", "--web", "--git-protocol", "https"])
    total = total_workflows()
    print(f"\n📊 Total workflows: {total}\n")
    sub = ["Run workflows", "View workflows", "Back"]
    sub_pos = 1
    while True:
        clear(); banner("RUN WORKFLOWS")
        print(f"📊 Total workflows: {total}\n")
        for idx, text in enumerate(sub, 1):
            if idx == sub_pos:
                print(f"\033[1;36m▶ {idx}. {text}\033[0m")
            else:
                print(f"  {idx}. {text}")
        print("\n[↑↓] Navigate   [Enter] Choose")
        key = read_key_safe()
        if key == readchar.key.UP: sub_pos = (sub_pos - 2) % len(sub) + 1
        elif key == readchar.key.DOWN: sub_pos = sub_pos % len(sub) + 1
        elif key in (readchar.key.ENTER, "\r", "\n"):
            if sub_pos == 1:
                clear(); banner("RUN WORKFLOWS")
                print("\n⏳ Memicu workflow …\n")
                rc = subprocess.run(["gh", "workflow", "run", WF, "--repo", REPO, "--ref", "main"],
                                    stderr=subprocess.STDOUT).returncode
                print("\n✅ Workflow berhasil dipicu!" if rc == 0 else "\n❌ Gagal memicu workflow.")
                print("\033[1;36mTekan Enter untuk kembali …\033[0m", end="", flush=True)
                while read_key_safe() not in (readchar.key.ENTER, "\r", "\n"): pass
            elif sub_pos == 2:
                clear(); banner("VIEW WORKFLOWS")
                print(f"\n📋 Daftar workflow (total {total}):\n")
                subprocess.run(["gh", "workflow", "list", "--repo", REPO, "--limit", "20"])
                print("\033[1;36mTekan Enter untuk kembali …\033[0m", end="", flush=True)
                while read_key_safe() not in (readchar.key.ENTER, "\r", "\n"): pass
            else:
                return

def tailscale_menu():
    clear(); banner("TAILSCALE")
    installed = False
    try:
        test = subprocess.run(["am", "start", "-n", f"{TS_PKG}/.ipn.MainActivity"],
                              capture_output=True, text=True, timeout=3)
        installed = (test.returncode == 0)
    except Exception:
        installed = False

    sub = ["Buka Tailscale" if installed else "Install Tailscale", "Back"]
    sub_pos = 1
    while True:
        clear(); banner("TAILSCALE")
        for idx, text in enumerate(sub, 1):
            if idx == sub_pos:
                print(f"\033[1;36m▶ {idx}. {text}\033[0m")
            else:
                print(f"  {idx}. {text}")
        print("\n[↑↓] Navigate   [Enter] Choose")
        key = read_key_safe()
        if key == readchar.key.UP: sub_pos = (sub_pos - 2) % len(sub) + 1
        elif key == readchar.key.DOWN: sub_pos = sub_pos % len(sub) + 1
        elif key in (readchar.key.ENTER, "\r", "\n"):
            if sub_pos == 1:
                if installed:
                    os.system(f"am start -n {TS_PKG}/.ipn.MainActivity")
                else:
                    os.system(f"am start -a android.intent.action.VIEW -d {PLAY}")
                return
            else:
                return

def edit_script():
    clear(); banner("EDIT SCRIPT")
    sub = ["Edit script", "Reset script", "Back"]; sub_pos = 1
    while True:
        clear(); banner("EDIT SCRIPT")
        for idx, text in enumerate(sub, 1):
            if idx == sub_pos:
                print(f"\033[1;36m▶ {idx}. {text}\033[0m")
            else:
                print(f"  {idx}. {text}")
        print("\n[↑↓] Navigate   [Enter] Choose")
        key = read_key_safe()
        if key == readchar.key.UP: sub_pos = (sub_pos - 2) % len(sub) + 1
        elif key == readchar.key.DOWN: sub_pos = sub_pos % len(sub) + 1
        elif key in (readchar.key.ENTER, "\r", "\n"):
            if sub_pos == 1:
                clear(); banner("EDIT SCRIPT")
                print("\n📂 Membuka nano …\n"); os.system("nano menu.py")
                while read_key_safe() not in (readchar.key.ENTER, "\r", "\n"): pass
                print("\033[1;36mTekan Enter untuk kembali …\033[0m", end="", flush=True)
                while read_key_safe() not in (readchar.key.ENTER, "\r", "\n"): pass
            elif sub_pos == 2:
                reset_script()
            else:
                return

def reset_script():
    clear(); banner("RESET SCRIPT")
    print("\n⚠️  Kosongkan isi menu.py?\n")
    reset_menu = ["Ya", "Back"]; yakin = 1
    while True:
        for idx, txt in enumerate(reset_menu, 1):
            if idx == yakin:
                print(f"\033[1;36m▶ {idx}. {txt}\033[0m")
            else:
                print(f"  {idx}. {txt}")
        key = read_key_safe()
        if key in (readchar.key.UP, readchar.key.DOWN):
            yakin = 3 - yakin
            clear(); banner("RESET SCRIPT")
            print("\n⚠️  Kosongkan isi menu.py?\n")
        elif key in (readchar.key.ENTER, "\r", "\n"):
            break
    if yakin == 1:
        open("menu.py", "w").close()  # kosongkan (0 byte)
        clear(); banner("RESET SCRIPT")
        print("\n✅ File dikosongkan.")
        sys.exit(0)                   # langsung keluar total
    else:
        print("\033[1;36mTekan Enter untuk kembali …\033[0m", end="", flush=True)
        while read_key_safe() not in (readchar.key.ENTER, "\r", "\n"): pass

def main():
    menu = ["Open browser GitHub", "Run workflows", "Edit script", "Tailscale", "Exit"]
    pos = 1
    while True:
        show_menu(menu, pos)
        key = read_key_safe()
        if key == readchar.key.UP: pos = (pos - 2) % len(menu) + 1
        elif key == readchar.key.DOWN: pos = pos % len(menu) + 1
        elif key in (readchar.key.ENTER, "\r", "\n"):
            if pos == 1:
                os.system(f"am start -a android.intent.action.VIEW -d {URL}")
                success_screen()
            elif pos == 2: run_workflow()
            elif pos == 3: edit_script()
            elif pos == 4: tailscale_menu()
            else: clear(); banner("EXIT LIST"); break
        elif key in ("q", readchar.key.CTRL_C): clear(); banner("EXIT LIST"); break

if __name__ == "__main__":
    main()
    
