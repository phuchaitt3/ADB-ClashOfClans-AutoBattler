import subprocess
import time
import sys

init_adb = False
# init_adb = True

decup_flag = False # quick decup mode
fight_mode = False
fight_mode_loops = 5
no_auto_end = False
no_hero = True
full_fight = False

# X 7 1 or 6 1
no_decup = 0
no_fights = 6

standard_delay = 0.001
button_delay = 0.1
no_troops = 6
no_noskill = 0
no_skill_troops = no_troops - no_noskill

find_now_wait = 4.7
return_home_wait = 2.2
if not full_fight:
    time_wait_skills = 0
else:
    time_wait_skills = 2
if not full_fight:
    witch_wait = 2.2
else:
    witch_wait = 3.5
if not full_fight:
    if not no_hero:
        time_wait_battle = 3.2
    else:
        time_wait_battle = 3.7
else:
    time_wait_battle = 12

first_x = 780 # 730
last_x = 950
first_y = 430
last_y = 320 # 270

x_diff = last_x - first_x
y_diff = last_y - first_y
first_point = (first_x, first_y)
second_point = (first_x + 1/5*x_diff, first_y + 1/5*y_diff)
third_point = (first_x + 2/5*x_diff, first_y + 2/5*y_diff)
forth_point = (first_x + 3/5*x_diff, first_y + 3/5*y_diff)
fifth_point = (first_x + 4/5*x_diff, first_y + 4/5*y_diff)
sixth_point = (last_x, last_y)

tap_positions = [
    sixth_point,  # 1
    fifth_point,  # 2
    forth_point,  # 3
    third_point,  # 4
    second_point, # 5
    first_point,  # 6
]

if no_hero:
    first_troop_x = 182.5 - 77.5
else:
    first_troop_x = 182.5

def play_hero():
    run_adb_command("input tap 100 485")
    time.sleep(standard_delay)
    run_adb_command(f"input tap {first_point[0]} {first_point[1]}")
    time.sleep(standard_delay)

# --- Configuration ---
# The identifier for your BlueStacks instance from 'adb devices'
# This is crucial to avoid the "more than one device" error.
ADB_DEVICE = "localhost:5555"

# --- Helper Function ---
# It's good practice to create a function to run your commands.
def run_adb_command(command):
    """Executes a given ADB command on the specified device."""
    # We split the command into a list of arguments for subprocess.run
    full_command = ["adb", "-s", ADB_DEVICE, "shell"] + command.split()
    # print(f"Executing: {' '.join(full_command)}")
    try:
        # Execute the command
        subprocess.run(full_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except FileNotFoundError:
        print("Error: 'adb' command not found. Is it in your system's PATH?")

def end_battle():
    if no_auto_end:
        return
    
    # End battle
    run_adb_command("input tap 77 380")
    time.sleep(button_delay)
    # Confirm end
    run_adb_command("input tap 585 350")
    time.sleep(button_delay)
    # Return home
    run_adb_command("input tap 485 457")
    time.sleep(3.8)

    # Second end
    run_adb_command("input tap 77 380") # safe
    time.sleep(button_delay)
    # Confirm end
    run_adb_command("input tap 585 350") # mine
    time.sleep(button_delay)
    # Return home
    run_adb_command("input tap 485 457")
    time.sleep(return_home_wait)
    run_adb_command("input tap 52 317")
    time.sleep(0.1)
    
def end_battle_once():
    if no_auto_end:
        return

    run_adb_command("input tap 77 380")
    time.sleep(button_delay)
    # Confirm end
    run_adb_command("input tap 585 350")
    time.sleep(button_delay)
    # Return home
    run_adb_command("input tap 485 457")
    time.sleep(return_home_wait)

def run_normal_fight():
    # Attack
    run_adb_command("input tap 62 475")
    time.sleep(button_delay)

    # Find now
    run_adb_command("input tap 710 350")
    time.sleep(find_now_wait)

    for i in range(no_troops):
        if (i == no_noskill) and (not no_hero):
            play_hero()

        run_adb_command(f"input tap {int(first_troop_x + i * 77.5)} 487")
        time.sleep(standard_delay)
        tap_map = f"input tap {tap_positions[i][0]} {tap_positions[i][1]}"
        run_adb_command(tap_map)
        # print(tap_map)
        time.sleep(standard_delay)

    # Activate skills
    time.sleep(time_wait_skills)
    # for i in range(no_noskill, no_troops + 1):
    for i in [5, 0, 4, 1, 3, 2]:
        run_adb_command(f"input tap {int(first_troop_x + i * 77.5)} 487")
        time.sleep(witch_wait)
        if (i == 3) and (not no_hero): # hero
            run_adb_command("input tap 100 485")

    # Wait for the battle to finish
    time.sleep(time_wait_battle)

    if full_fight:
        end_battle()
    else:
        end_battle_once()

def decup():
    # Attack
    run_adb_command("input tap 62 475")
    time.sleep(button_delay)

    # Find now
    run_adb_command("input tap 710 350")
    time.sleep(find_now_wait)

    play_hero()

    # End battle
    run_adb_command("input tap 77 380")
    time.sleep(button_delay)
    # Confirm end
    run_adb_command("input tap 585 350")
    time.sleep(button_delay)
    # Return home
    run_adb_command("input tap 485 457")
    time.sleep(return_home_wait)

def connect_adb_device(device_address):
    """Connects to an ADB device or emulator."""
    try:
        # adb connect is not a shell command, so we run it directly
        result = subprocess.run(["adb", "connect", device_address], check=True, capture_output=True, text=True)
        print(result.stdout.strip())
        print(result.stderr.strip())
        # Give it a moment to establish connection
        time.sleep(2)
        print("ADB connection attempt complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to device: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
    except FileNotFoundError:
        print("Error: 'adb' command not found. Is it in your system's PATH?")

# --- Main Automation Sequence ---
if __name__ == "__main__":
    if init_adb:
        connect_adb_device(ADB_DEVICE)

    if fight_mode:
        for loop in range(fight_mode_loops):
            run_normal_fight()
        sys.exit()
    for loop in range(no_decup):
        decup()
    for loop in range(no_fights):
        run_normal_fight() 