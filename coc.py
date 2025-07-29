import subprocess
import time

# --- Configuration ---
# The identifier for your BlueStacks instance from 'adb devices'
# This is crucial to avoid the "more than one device" error.
ADB_DEVICE = "localhost:5555" 
# adb connect localhost:5555

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

standard_delay = 0.1
button_delay = 0.2
find_now_wait = 6
return_home_wait = 2.5

def end_battle():
    # End battle
    run_adb_command("input tap 155 760")
    time.sleep(button_delay)
    # Confirm end
    run_adb_command("input tap 1170 700")
    time.sleep(button_delay)
    # Return home 
    run_adb_command("input tap 970 915")
    time.sleep(3.7)

    # Second end
    run_adb_command("input tap 155 760") # safe
    time.sleep(button_delay)
    # Confirm end
    run_adb_command("input tap 1170 700") # mine
    time.sleep(button_delay)
    # Return home 
    run_adb_command("input tap 970 915") 
    time.sleep(return_home_wait)
    run_adb_command("input tap 105 635") 
    time.sleep(0.1)

def run_normal_fight():
    # Attack
    run_adb_command("input tap 125 950")
    time.sleep(button_delay)

    # Find now
    run_adb_command("input tap 1420 700")
    time.sleep(find_now_wait) 

    # # Play hero
    # run_adb_command("input tap 200 970")
    # time.sleep(standard_delay) 
    # run_adb_command("input tap 1620 740")
    # time.sleep(standard_delay) 

    # # Select witches
    # run_adb_command("input tap 365 975")
    # time.sleep(1)

    no_troops = 6
    each_screen_move = (10, 5)
    first_point = (1530, 820) + each_screen_move*2
    second_point = (1620, 740) + each_screen_move*2
    third_point = (1790, 675)
    forth_point = (1870, 615)
    tap_positions = [
        first_point,  # 1
        third_point,  # 2
        first_point,  # 3
        second_point,  # 4
        third_point,  # 5
        forth_point,  # 6
    ]

    time_wait_bombs = 3

    for i in range(no_troops):
        if i == 2:
            # Play hero
            run_adb_command("input tap 200 970")
            time.sleep(standard_delay) 
            run_adb_command("input tap 1620 740")
            time.sleep(standard_delay) 
            # Wait to search bombs
            time.sleep(time_wait_bombs)
        
        run_adb_command(f"input tap {365 + i * 155} 975")
        time.sleep(standard_delay)
        # toggle = i % 2
        run_adb_command(f"input tap {tap_positions[i][0]} {tap_positions[i][1]}")
        # 1530 820
        time.sleep(standard_delay)
    
    # Activate skills
    # 365 975 1, 520 975 2, 670 975 3, 825 975 4, 980 975 5, 1125 975 6
    # 155, 150, 155, 155, 155
    for i in range(2, no_troops + 1):
        run_adb_command(f"input tap {365 + i * 155} 975")
        time.sleep(2.5)

    # Activate hero skill
    hero_skill_wait = 11.8 - time_wait_bombs
    time.sleep(hero_skill_wait)
    run_adb_command("input tap 200 970")

    # Wait for the battle to finish
    time.sleep(30-hero_skill_wait)

    end_battle()

def decup():
    # Attack
    run_adb_command("input tap 125 950")
    time.sleep(button_delay)

    # Find now
    run_adb_command("input tap 1420 700")
    time.sleep(find_now_wait) 

    # Play hero
    run_adb_command("input tap 200 970")
    time.sleep(standard_delay) 
    run_adb_command("input tap 1620 740")
    time.sleep(standard_delay) 

    # End battle
    run_adb_command("input tap 155 760")
    time.sleep(button_delay)
    # Confirm end
    run_adb_command("input tap 1170 700")
    time.sleep(button_delay)
    # Return home 
    run_adb_command("input tap 970 915")
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
    # connect_adb_device(ADB_DEVICE)

    for loop in range(8):
        if loop % 2 == 0:
            decup()
        else:
            run_normal_fight()