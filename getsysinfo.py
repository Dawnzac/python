import os
import platform
import subprocess
import json

def get_hardware_info():
    system = platform.system()
    hardware_info = {}
    
    if system == "Linux":
        hardware_info["CPU"] = subprocess.getoutput("lscpu")
        hardware_info["Memory"] = subprocess.getoutput("free -h")
        hardware_info["Disk"] = subprocess.getoutput("lsblk")
        hardware_info["Network"] = subprocess.getoutput("ip a")
    elif system == "Darwin":  # macOS
        hardware_info["CPU"] = subprocess.getoutput("sysctl -n machdep.cpu.brand_string")
        hardware_info["Memory"] = subprocess.getoutput("sysctl -n hw.memsize")
        hardware_info["Disk"] = subprocess.getoutput("df -h")
        hardware_info["Network"] = subprocess.getoutput("ifconfig")
    
    return hardware_info

def get_installed_software():
    system = platform.system()
    installed_software = []
    
    if system == "Linux":
        try:
            installed_software = subprocess.getoutput("dpkg-query -W -f='${Package}\n'").split("\n")
        except:
            installed_software = subprocess.getoutput("rpm -qa").split("\n")
    elif system == "Darwin":  # macOS
        installed_software = subprocess.getoutput("brew list").split("\n")
    
    return installed_software

def main():
    inventory = {
        "Hardware": get_hardware_info(),
        "Software": get_installed_software(),
    }
    
    with open("inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)
    
if __name__ == "__main__":
    main()
