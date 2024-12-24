import os
import subprocess
import sys
import importlib.util
import time

def is_package_installed(package_name):
    """检查包是否已安装"""
    return importlib.util.find_spec(package_name) is not None

def install_requirements():
    """安装依赖"""
    requirements_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print("No requirements.txt found")
        return False
    
    try:
        # 检查是否需要安装 gradio
        if not is_package_installed("gradio"):
            print("Installing gradio...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio>=4.0.0"])
            time.sleep(2)  # 等待安装完成
            print("Successfully installed gradio")
            return True
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False

def setup():
    """在 ComfyUI 启动时执行安装"""
    if install_requirements():
        print("\n" + "="*50)
        print("Gradio has been installed successfully!")
        print("Please restart ComfyUI to complete the installation.")
        if os.name == 'nt':
            print("\nOn Windows:")
            print("1. Close the current window")
            print("2. Run run_cpu.bat or run_gpu.bat again")
        else:
            print("\nOn Linux/Mac:")
            print("1. Press Ctrl+C to stop the current process")
            print("2. Run python main.py again")
        print("="*50 + "\n")

if __name__ == "__main__":
    setup() 