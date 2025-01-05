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
        print("未找到 requirements.txt 文件")
        return False
    
    required_packages = {
        "numpy": "1.21.0",
        "Pillow": "9.0.0",
        "torch": "1.7.0",
        "gradio": "4.0.0"
    }
    
    need_install = False
    
    try:
        for package, min_version in required_packages.items():
            if not is_package_installed(package):
                print(f"正在安装 {package}>={min_version}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}>={min_version}"])
                need_install = True
                time.sleep(1)  # 等待安装完成
                print(f"成功安装 {package}")
        
        return need_install
    except subprocess.CalledProcessError as e:
        print(f"安装依赖时出错: {e}")
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