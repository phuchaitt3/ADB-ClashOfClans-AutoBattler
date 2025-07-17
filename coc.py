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
    print("-----START-----")
    
    # Attack
    run_adb_command("input tap 125 950")
    time.sleep(2) 

    # Find now
    run_adb_command("input tap 1420 700")
    time.sleep(40) 

    # Select hero
    run_adb_command("input tap 200 970")
    time.sleep(1) 
    run_adb_command("input tap 1285 820")
    time.sleep(1) 

    # Select witches
    run_adb_command("input tap 365 975")
    time.sleep(1)
    for _ in range(6):
        run_adb_command("input tap 1285 820")
        time.sleep(1) 
    
    # Activate skills
    # 365 975 1, 520 975 2, 670 975 3, 825 975 4, 980 975 5, 1125 975 6
    # 155, 150, 155, 155, 155
    for i in range(6):
        run_adb_command(f"input tap {365 + i * 155} 975")
        time.sleep(1)

    # Wait for the battle to finish
    time.sleep(60)

    # End battle
    run_adb_command("input tap 155 760")
    time.sleep(1)

    # Confirm end
    run_adb_command("input tap 1170 700")
    time.sleep(5)

    # Return home 
    run_adb_command("input tap 970 915")

    print("-----END-----")