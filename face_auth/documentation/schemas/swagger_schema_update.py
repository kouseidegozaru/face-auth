import importlib
import inspect
import pkgutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Type


def find_subclasses_in_path(base_class: Type, path: str) -> List[Type]:
    """
    指定されたパス内で、base_classを継承した全てのサブクラスを取得

    :param base_class: 親クラス
    :param path: インポートパス (例: 'my_package.submodule')
    :return: サブクラスのリスト
    """
    subclasses = []

    # 指定されたパスをモジュールとしてインポート可能な形式に変換
    base_dir = Path(path.replace('.', '/'))
    package_name = path.split('.')[-1]

    if not base_dir.exists():
        print(f"Directory {base_dir} does not exist.")
        return subclasses

    # 指定ディレクトリのすべてのモジュールを動的に読み込む
    for _, module_name, is_pkg in pkgutil.iter_modules([str(base_dir)]):
        full_module_name = f"{path}.{module_name}"
        try:
            module = importlib.import_module(full_module_name)
        except Exception as e:
            print(f"Could not import module {full_module_name}: {e}")
            continue

        # モジュール内のクラスを調べる
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj is not base_class and issubclass(obj, base_class):
                subclasses.append(obj)

    return subclasses
