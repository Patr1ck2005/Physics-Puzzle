import json

from pymunk import Vec2d

from gui.phy_obj_ui.bg_wall_ui import CircleBGWallUI, RectBGWallUI
from gui.phy_obj_ui.entity_ui import BoxEntityUI, CircleEntityUI, BlankEntityUI, PolyEntityUI
from gui.phy_obj_ui.force_ui import ForceUI  # 假设 ForceUI 类在这个模块中
from gui.phy_obj_ui.constrain_ui import PinJointUI, SlideJointUI, SpringUI  # 假设这些 Joint 类在这个模块中
from gui.phy_obj_ui.check_label_ui import CheckLabelUI
from gui.phy_obj_ui.tool_ui import FrictionToolUI, ElasticityToolUI


class ObjsLoader:
    def __init__(self, objs_json_file):
        self.objs_json_file = objs_json_file
        self.objs = {
            'entities': {},
            'bg_walls': {},
            'forces': {},
            'constraints': {},
            'tools': {},
            'labels': {}
        }

    def load_objs(self):
        with open(self.objs_json_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 加载 entities
        for obj_config in config.get('entities', []):
            obj = self.create_obj(obj_config)
            if obj:
                self.objs['entities'][obj_config['name']] = obj

        # 加载 bg_walls
        for obj_config in config.get('bg_walls', []):
            obj = self.create_obj(obj_config)
            if obj:
                self.objs['bg_walls'][obj_config['name']] = obj

        # 加载 forces
        for obj_config in config.get('forces', []):
            obj = self.create_obj(obj_config)
            if obj:
                self.objs['forces'][obj_config['name']] = obj

        # 加载 constraints
        for obj_config in config.get('constraints', []):
            obj = self.create_obj(obj_config)
            if obj:
                self.objs['constraints'][obj_config['name']] = obj

        # 加载 tools
        for obj_config in config.get('tools', []):
            obj = self.create_obj(obj_config)
            if obj:
                self.objs['tools'][obj_config['name']] = obj

        # 加载 labels
        for obj_config in config.get('labels', []):
            obj = self.create_obj(obj_config)
            if obj:
                self.objs['labels'][obj_config['name']] = obj

        return self.objs

    def create_obj(self, obj_config):
        obj_type = obj_config.get("type")

        # 创建 Entity 类型的对象
        if obj_type == "BoxEntityUI":
            return BoxEntityUI(
                name=obj_config["name"],
                phy_type=obj_config["phy_type"],
                center=Vec2d(*obj_config["center"]),
                angle=obj_config.get("angle", 0),
                size=tuple(obj_config.get("size", (30, 30))),
                ico_path=obj_config.get("ico_path"),
                color=tuple(obj_config.get("color", (150, 150, 150))),
                mass=obj_config.get("mass", 1),
                elasticity=obj_config.get("elasticity", 0),
                friction=obj_config.get("friction", 0),
                charge=obj_config.get("charge", 0)
            )
        elif obj_type == "CircleEntityUI":
            return CircleEntityUI(
                name=obj_config["name"],
                phy_type=obj_config["phy_type"],
                center=Vec2d(*obj_config["center"]),
                angle=obj_config.get("angle", 0),
                r=obj_config.get("r", 20),
                ico_path=obj_config.get("ico_path"),
                color=tuple(obj_config.get("color", (150, 150, 150))),
                mass=obj_config.get("mass", 1),
                elasticity=obj_config.get("elasticity", 0),
                friction=obj_config.get("friction", 0),
                charge=obj_config.get("charge", 0)
            )
        elif obj_type == "PolyEntityUI":
            return PolyEntityUI(
                name=obj_config["name"],
                phy_type=obj_config["phy_type"],
                world_points=tuple(obj_config["world_points"]),
                angle=obj_config.get("angle", 0),
                ico_path=obj_config.get("ico_path"),
                color=tuple(obj_config.get("color", (150, 150, 150))),
                mass=obj_config.get("mass", 1),
                elasticity=obj_config.get("elasticity", 0),
                friction=obj_config.get("friction", 0),
                charge=obj_config.get("charge", 0)
            )
        # 创建 BackGroundWall 类型的对象
        elif obj_type == "CircleBGWallUI":
            return CircleBGWallUI(**obj_config)
        elif obj_type == "RectBGWallUI":
            return RectBGWallUI(**obj_config)
        # 创建 Force 类型的对象
        elif obj_type == "ForceUI":
            target = obj_config.get("target")
            target = self.objs['entities'][target] if target else None
            return ForceUI(
                name=obj_config["name"],
                force=Vec2d(*obj_config["force"]),
                target=target,
            )

        # 创建 tool 类型的对象
        elif obj_type == "FrictionToolUI":
            return FrictionToolUI(
                **obj_config
            )
        elif obj_type == "GravityToolUI":
            pass
        elif obj_type == "ElasticityToolUI":
            return ElasticityToolUI(
                **obj_config
            )

        # 创建 CheckLabel 类型的对象
        elif obj_type == "CheckLabelUI":
            return CheckLabelUI(
                **obj_config
            )

        # 创建 Constraint 类型的对象
        else:
            target_a = obj_config.get("target_a")
            target_b = obj_config.get("target_b")
            target_a = self.objs['entities'][target_a] if target_a else None
            target_b = self.objs['entities'][target_b] if target_a else None
            if obj_type == "PinJointUI":
                return PinJointUI(
                    name=obj_config["name"],
                    position=tuple(obj_config["position"]),
                    target_a=target_a,
                    target_b=target_b,
                    anchor_a=Vec2d(*obj_config.get("anchor_a", (0, 0))),
                    anchor_b=Vec2d(*obj_config.get("anchor_b", (0, 0))),
                )
            elif obj_type == "SlideJointUI":
                return SlideJointUI(
                    name=obj_config["name"],
                    position=tuple(obj_config["position"]),
                    target_a=target_a,
                    target_b=target_b,
                    anchor_a=Vec2d(*obj_config.get("anchor_a", (0, 0))),
                    anchor_b=Vec2d(*obj_config.get("anchor_b", (0, 0))),
                )
            elif obj_type == "SpringUI":
                return SpringUI(
                    name=obj_config["name"],
                    position=tuple(obj_config["position"]),
                    target_a=target_a,
                    target_b=target_b,
                    anchor_a=Vec2d(*obj_config.get("anchor_a", (0, 0))),
                    anchor_b=Vec2d(*obj_config.get("anchor_b", (0, 0))),
                )

        return None
