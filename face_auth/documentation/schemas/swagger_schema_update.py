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


class SubClassesRunner(ABC):
    """
    このクラスを継承したクラスのrunメソッドを実行する
    """

    @abstractmethod
    def run(self):
        """
        このクラスを継承したクラスは
        runメソッドをオーバーライドする
        """
        pass

    @classmethod
    def run_for_subclasses(cls, subclasses_import_paths: list[str]=None):
        """
        このクラスを継承したクラスのrunメソッドを実行する
        args:
            subclasses_import_paths: サブクラスが定義されているインポートパスのリスト
        """
        if subclasses_import_paths is None:
            subclasses_import_paths = []

        for subclass_import_path in subclasses_import_paths:
            subclasses = find_subclasses_in_path(cls, subclass_import_path)
            for subclass in subclasses:
                subclass.run()


class SwaggerSchemaUpdater(SubClassesRunner):

    @abstractmethod
    def run():
        """
        Swaggerの拡張情報をこのメソッドに記載する
        usage:
            def run():
                YourViewSet.your_method = swagger_auto_schema(
                    operation_summary="this summary",
                    operation_description="this description",
                    responses={200: openapi.Response('success'), 404: openapi.Response('Not Found')},
                )(YourViewSet.your_method)
                
                YourViewSet.your_method2 = swagger_auto_schema(
                    operation_summary="this summary",
                ...
                    
        """
        super().run()
