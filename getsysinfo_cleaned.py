import os
import platform
import subprocess
import json

def get_hardware_info():
    system = platform.system()
    hardware_info = {}
    
    if system == "Linux":
        cpu_info = subprocess.getoutput("lscpu | grep 'Model name' | awk -F: '{print $2}'").strip()
        cpu_arch = subprocess.getoutput("lscpu | grep 'Architecture' | awk -F: '{print $2}'").strip()
        memory_info = subprocess.getoutput("free -h | awk '/^Mem:/ {print $2}'").strip()
        disk_info = subprocess.getoutput("lsblk -o SIZE -n -d | awk '{sum += $1} END {print sum}'").strip()
        ip_address = subprocess.getoutput("hostname -I | awk '{print $1}'").strip()
        
        hardware_info["CPU"] = {"Name": cpu_info, "Architecture": cpu_arch}
        hardware_info["Memory"] = memory_info
        hardware_info["Disk"] = disk_info
        hardware_info["IP Address"] = ip_address

    elif system == "Darwin":  # macOS
        cpu_info = subprocess.getoutput("sysctl -n machdep.cpu.brand_string").strip()
        memory_info = subprocess.getoutput("sysctl -n hw.memsize").strip()
        disk_info = subprocess.getoutput("df -h / | awk 'NR==2 {print $2}'").strip()
        ip_address = subprocess.getoutput("ipconfig getifaddr en0").strip()
        
        hardware_info["CPU"] = {"Name": cpu_info, "Summary": "N/A"}
        hardware_info["Memory"] = f"{int(memory_info) / (1024**3):.2f} GB"
        hardware_info["Disk"] = disk_info
        hardware_info["IP Address"] = ip_address
    
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
