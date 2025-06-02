#!/usr/bin/env python3
import os
import platform
import subprocess
import socket
import uuid
import psutil
import requests
import GPUtil
from datetime import timedelta, datetime
from pathlib import Path
from getpass import getuser
from colorama import Fore, Style, init

print(" ")

init(autoreset=True)

RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = (
    Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE
)
BOLD = Style.BRIGHT

COLOR_LIST = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]


def colorize_ascii(logo):
    lines = logo.splitlines()
    colored = []
    for i, line in enumerate(lines):
        color = COLOR_LIST[i % len(COLOR_LIST)]
        colored.append(color + BOLD + line)
    return "\n".join(colored)


def get_ascii_logo():
    config_path = Path("bfetch_config.txt")
    if config_path.exists():
        selected = config_path.read_text().strip()
    else:
        selected = f"{platform.system().lower()}.txt"  # fallback

    ascii_path = Path("ascii") / selected
    if ascii_path.exists():
        with open(ascii_path) as f:
            return colorize_ascii(f.read())
    return colorize_ascii("No ASCII logo found.")



def get_gpu():
    try:
        gpus = [gpu.name for gpu in GPUtil.getGPUs()]
        if not gpus:
            output = subprocess.check_output(["system_profiler", "SPDisplaysDataType"]).decode()
            gpus = [line.split(":", 1)[1].strip() for line in output.splitlines() if "Chipset Model:" in line]
        return gpus
    except:
        return ["Unknown"]
    
def get_cpu():
    if platform.system() == "Darwin":
        try:
            cpu_model = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
            return cpu_model
        except:
            return "Unknown"
    return platform.processor() or "Unknown"



def get_uptime():
    uptime_seconds = (datetime.now() - datetime.fromtimestamp(psutil.boot_time())).total_seconds()
    return str(timedelta(seconds=int(uptime_seconds)))


def get_memory():
    mem = psutil.virtual_memory()
    return f"{mem.used / 1e9:.1f} GB / {mem.total / 1e9:.1f} GB"


def get_ips():
    try:
        public_ip = requests.get("https://api.ipify.org").text
    except:
        public_ip = "Unavailable"
    try:
        private_ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]
        private_ip = private_ip[0] if private_ip else "127.0.0.1"
    except:
        private_ip = "Unavailable"
    return public_ip, private_ip


def get_location():
    try:
        loc = requests.get("http://ip-api.com/json").json()
        return f"{loc['city']}, {loc['country']}"
    except:
        return "Unavailable"


def get_weather():
    try:
        data = requests.get("https://wttr.in/?format=%C+%t", timeout=5).text.strip()
        return data
    except:
        return "Unavailable"


def get_hwid():
    return hex(uuid.getnode())


def display():
    logo = get_ascii_logo()
    user_host = f"{getuser()}@{socket.gethostname()}"
    os_name = platform.system()
    kernel = platform.version()
    cpu = get_cpu()
    gpus = get_gpu()
    memory = get_memory()
    uptime = get_uptime()
    shell = os.environ.get("SHELL", "/bin/sh")
    wmde = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION") or "Unknown"
    public_ip, private_ip = get_ips()
    location = get_location()
    weather = get_weather()
    hwid = get_hwid()
    gpu_line = " | ".join(f"GPU{i+1}: {gpu}" for i, gpu in enumerate(gpus))
    if len(gpus) > 1:
        gput = 'GPUs'
    else:
        gput = 'GPU'
    info = [
        f"{BLUE}{BOLD}User:       {WHITE}{user_host}",
        f"{RED}{BOLD}System:     {WHITE}{platform.machine()}",
        f"{GREEN}{BOLD}OS:         {WHITE}{os_name} ({platform.release()})",
        f"{MAGENTA}{BOLD}Kernel:     {WHITE}{kernel}",
        f"{CYAN}{BOLD}Uptime:     {WHITE}{uptime}",
        f"{YELLOW}{BOLD}CPU:        {WHITE}{cpu}",
        f"{YELLOW}{BOLD}{gput}:        {WHITE}{gpu_line}",
        f"{MAGENTA}{BOLD}Memory:     {WHITE}{memory}",
        f"{GREEN}{BOLD}Shell:      {WHITE}{shell}",
        f"{BLUE}{BOLD}WM/DE:      {WHITE}{wmde}",
        f"{CYAN}{BOLD}Public IP:  {WHITE}{public_ip}",
        f"{CYAN}{BOLD}Private IP: {WHITE}{private_ip}",
        f"{BLUE}{BOLD}Location:   {WHITE}{location}",
        f"{BLUE}{BOLD}Weather:    {WHITE}{weather}",
        f"{YELLOW}{BOLD}HWID:       {WHITE}{hwid}",
    ]

    logo_lines = logo.splitlines()
    pad = max(len(line) for line in logo_lines) + 4
    for i in range(max(len(logo_lines), len(info))):
        l = logo_lines[i] if i < len(logo_lines) else ""
        r = info[i] if i < len(info) else ""
        print(f"{l.ljust(pad)}{r}")


if __name__ == "__main__":
    display()
    print(" ")
