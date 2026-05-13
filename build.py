"""
JSON Tool 打包脚本
用法: python build.py
"""

import subprocess
import sys
import os

def main():
    print("=" * 50)
    print("  JSON Tool 打包程序")
    print("=" * 50)

    # 安装依赖
    print("\n[1/3] 安装依赖...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])

    # 获取customtkinter资源路径
    import customtkinter
    ctk_path = os.path.dirname(customtkinter.__file__)
    assets_path = os.path.join(ctk_path, "assets")
    print(f"\n[2/3] 资源路径: {assets_path}")

    # 打包
    print("\n[3/3] 打包为EXE...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "JSONTool",
        "--add-data", f"{assets_path};customtkinter/assets/",
        "json_tool.py",
    ]
    subprocess.check_call(cmd)

    exe_path = os.path.join("dist", "JSONTool.exe")
    print("\n" + "=" * 50)
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"  打包成功！")
        print(f"  输出: {os.path.abspath(exe_path)}")
        print(f"  大小: {size_mb:.1f} MB")
    else:
        print("  打包失败，请检查错误信息。")
    print("=" * 50)

if __name__ == "__main__":
    main()
