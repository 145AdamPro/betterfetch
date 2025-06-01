from setuptools import setup
import platform
from pathlib import Path
import subprocess

# Interactive setup for logo selection

def install_requirements():
    try:
        subprocess.check_call(["pip3", "install", "-r", "requirements.txt"])
        print("\n✅ Requirements installed successfully.")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies.")

def configure_logo():
    ascii_dir = Path("ascii")
    if not ascii_dir.exists():
        ascii_dir.mkdir()
    available = [f.name for f in ascii_dir.glob("*.txt")]

    print("\n📁 Available ASCII logos:")
    for name in available:
        print(f" - {name}")

    choice = input("\n🎨 Enter the logo filename you want to use (e.g., macos.txt): ").strip()
    config_path = Path("bfetch_config.txt")

    if (ascii_dir / choice).exists():
        config_path.write_text(choice)
        print(f"✅ Config saved to {config_path}")
    else:
        print("⚠️ That logo file does not exist in the ascii/ directory. Using default logo.")
        config_path.write_text(f"{platform.system().lower()}.txt")

def main():
    print("🚀 Setting up BetterFetch...\n")
    configure_logo()
    install_requirements()
    print("\n🎉 Setup complete! Run with: bfetch")

if __name__ == "__main__":
    main()

setup(
    name='betterfetch',
    version='1.0.0',
    py_modules=['bfetch'],
    install_requires=[
        'psutil',
        'requests',
        'GPUtil',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'bfetch = bfetch:display',
        ],
    },
    include_package_data=True,
    author='Adam',
    description='A blazing-fast, colorful, and fully customizable system fetch tool',
)
