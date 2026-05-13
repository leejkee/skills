#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import subprocess

def output(error: str, context: str):
    """
    输出序列化 JSON 格式文本
    """
    print(json.dumps({
        "error": error,
        "context": context
    }, ensure_ascii=False))


def is_installed(package_name: str) -> bool:
    """
    检查指定 pip 包是否已安装
    """
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "show",
                package_name,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.returncode == 0
    except Exception:
        return False


def install_package(package_name: str) -> bool:
    """
    使用 pip 安装指定包
    """
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                package_name,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.returncode == 0
    except Exception:
        return False

def write_env_file(env_ready: bool):
    """
    写入环境变量文件
    """
    write_content = "True" if env_ready else "False"
    with open(ENVREADY_FILENAME, "w") as f:
        f.write(write_content)

def create_env_file(file_name: str, file_path: str='.'):
    """
    创建环境变量文件
    """

def check_file_exists(file_name: str) -> bool:
    """
    检查环境变量文件是否存在
    """
    return os.path.isfile(file_name)

def check_env_from_file(file_path: str) -> bool:
    """
    读取env_ready文件 & 判断环境是否准备好
    """
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
            return content == "True"
    except Exception:
        return False

def main():
    if len(sys.argv) < 2:
        output(
            "missing argument",
            "please provide an accurate python package name."
        )
        return

    package_name = sys.argv[1].strip()

    if not package_name:
        output(
            "invalid argument",
            "package name is empty."
        )
        return

    if is_installed(package_name):
        output(
            "none",
            f"{package_name} is ready."
        )
        write_env_file(True)
        return

    success = install_package(package_name)

    if success and is_installed(package_name):
        output(
            "none",
            f"{package_name} is ready."
        )
        write_env_file(True)
    else:
        output(
            "install failed",
            f"{package_name} install failed, please ask user install it manually."
        )
        write_env_file(False)

if __name__ == "__main__":
    main()