"""路径工具类，提供获取项目根目录和文件绝对路径的功能"""

import os


def get_root_path():
    """获取项目根目录的绝对路径"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_absolute_path(relative_path: str) -> str:
    """获取文件的绝对路径"""
    root_path = get_root_path()
    return os.path.join(root_path, relative_path)


if __name__ == "__main__":
    # 测试获取项目根目录
    print("项目根目录:", get_root_path())

    # 测试获取文件绝对路径
    test_relative_path = "data/sample.txt"
    print("文件绝对路径:", get_absolute_path(test_relative_path))
