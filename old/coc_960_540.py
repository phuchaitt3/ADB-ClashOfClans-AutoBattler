import subprocess
import time

init_adb = False
init_adb = True
decup_flag = False # quick decup mode

# Original resolution: 1920x1080
# New resolution: 960x540

no_fights = 8
standard_delay = 0.09
button_delay = 0.2
find_now_wait = 6.2
return_home_wait = 2.4
time_wait_skills = 3
hero_skill_wait = 11.8 - time_wait_skills
time_wait_battle = 27

# Original coordinates for 1920x1080
# each_screen_move = (20, 10)
# first_point = (1520, 825) + each_screen_move*4
# second_point = (1600, 730) + each_screen_move*4
# third_point = (1790, 680) + each_screen_move*4
# forth_point = (1880, 610) + each_screen_move*4

# Halved coordinates for 960x540
# each_screen_move = (7*5, 6*5)
each_screen_move = (0,0)
first_x = 760
first_y = 420
last_x = 940
last_y = 300
x_diff = last_x - first_x # 180
y_diff = last_y - first_y # 120
first_point = (first_x + each_screen_move[0], first_y + each_screen_move[1])
second_point = (first_x + 1/3*x_diff + each_screen_move[0], first_y + 1/3*y_diff + each_screen_move[1])
third_point = (first_x + 2/3*x_diff + each_screen_move[0], first_y + 2/3*y_diff + each_screen_move[1])
forth_point = (last_x + each_screen_move[0], last_y + each_screen_move[1])

def play_hero():
    run_adb_command("input tap 100 485")
    time.sleep(standard_delay)
    run_adb_command(f"input tap {second_point[0]} {second_point[1]}") # 2nd position
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

def run_normal_fight():
    # Attack
    run_adb_command("input tap 62 475")
    time.sleep(button_delay)

    # Find now
    run_adb_command("input tap 710 350")
    time.sleep(find_now_wait)

    no_troops = 6
    tap_positions = [
        third_point,  # 1
        first_point,  # 2
        forth_point,  # 3
        third_point,  # 4
        second_point, # 5
        first_point,  # 6
    ]

    for i in range(no_troops):
        if i == 2:
            play_hero()

        run_adb_command(f"input tap {int(182.5 + i * 77.5)} 487")
        time.sleep(standard_delay)
        run_adb_command(f"input tap {tap_positions[i][0]} {tap_positions[i][1]}")
        time.sleep(standard_delay)

    # Activate skills
    time.sleep(time_wait_skills)
    for i in range(2, no_troops + 1):
        run_adb_command(f"input tap {int(182.5 + i * 77.5)} 487")
        time.sleep(2.5)

    # Activate hero skill
    time.sleep(hero_skill_wait)
    run_adb_command("input tap 100 485")

    # Wait for the battle to finish
    time.sleep(time_wait_battle-hero_skill_wait)

    end_battle()

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

    for loop in range(no_fights):
        if (loop % 2 == 0) or decup_flag:
            decup()
        else:
            run_normal_fight()