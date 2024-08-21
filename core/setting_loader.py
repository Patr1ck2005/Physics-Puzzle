import json


class EngineLoader:
    def __init__(self, engine):
        """
        初始化Loader对象，并传入物理引擎实例。

        :param engine: 物理引擎实例
        """
        self.engine = engine

    def load_from_json(self, json_file_path):
        """
        从JSON文件中读取参数并设置物理引擎的属性。

        :param json_file_path: JSON文件的路径
        """
        try:
            with open(json_file_path, 'r') as file:
                config = json.load(file)
                self._apply_config(config)
        except FileNotFoundError:
            print(f"文件 {json_file_path} 未找到。")
        except json.JSONDecodeError:
            print(f"文件 {json_file_path} 不是有效的JSON文件。")

    def _apply_config(self, config):
        """
        应用从JSON读取的配置到物理引擎实例。

        :param config: JSON文件中读取的配置字典
        """
        for key, value in config.items():
            if hasattr(self.engine, key):
                setattr(self.engine, key, value)
                print(f"设置 {key} = {value}")
            else:
                print(f"物理引擎没有属性 {key}")