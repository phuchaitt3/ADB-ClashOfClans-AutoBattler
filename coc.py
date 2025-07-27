import subprocess
import time

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
    print(f"Executing: {' '.join(full_command)}")
    try:
        # Execute the command
        subprocess.run(full_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except FileNotFoundError:
        print("Error: 'adb' command not found. Is it in your system's PATH?")

# --- Main Automation Sequence ---
if __name__ == "__main__":
    for _ in range(5):
        print("-----START-----")
        
        standard_delay = 0.1

        # Attack
        run_adb_command("input tap 125 950")
        time.sleep(1) 

        # Find now
        run_adb_command("input tap 1420 700")
        time.sleep(9) 

        # # Play hero
        # run_adb_command("input tap 200 970")
        # time.sleep(standard_delay) 
        # run_adb_command("input tap 1620 740")
        # time.sleep(standard_delay) 

        # # Select witches
        # run_adb_command("input tap 365 975")
        # time.sleep(1)

        no_troops = 6
        tap_positions = [
            (1530, 820),  # 1
            (1620, 740),  # 2
            (1530, 820),  # 3
            (1620, 740),  # 4
            (1780, 670),  # 5
            (1860, 610),  # 6
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
        hero_skill_wait = 12 - time_wait_bombs
        time.sleep(hero_skill_wait)
        run_adb_command("input tap 200 970")

        # Wait for the battle to finish
        time.sleep(40-hero_skill_wait)

        # End battle
        run_adb_command("input tap 155 760")
        time.sleep(0.5)
        # Confirm end
        run_adb_command("input tap 1170 700")
        time.sleep(0.5)
        # Return home 
        run_adb_command("input tap 970 915")
        time.sleep(2.7)

        # Second end
        run_adb_command("input tap 155 760") # safe
        time.sleep(0.5)
        # Confirm end
        run_adb_command("input tap 1170 700") # mine
        time.sleep(0.5)
        # Return home 
        run_adb_command("input tap 970 915") 
        time.sleep(2.7)
        run_adb_command("input tap 105 635") 
        time.sleep(0.1)

        print("-----END-----")