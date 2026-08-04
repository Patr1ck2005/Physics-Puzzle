"""ObjsLoader / LevelLoader 关卡加载单元测试"""
import json
import os
import tempfile

import pytest
import pymunk
from pymunk import Vec2d

from core.phy_obj_loader import ObjsLoader
from core.level_loader import LevelLoader


class TestObjsLoader:
    """ObjsLoader JSON 加载"""

    def test_load_empty_config(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump({}, f)
            f.flush()
            loader = ObjsLoader(f.name)
            objs = loader.load_objs()

        assert objs['entities'] == {}
        assert objs['bg_walls'] == {}
        assert objs['forces'] == {}
        assert objs['constraints'] == {}
        assert objs['tools'] == {}
        assert objs['labels'] == {}

    def test_load_box_entity(self):
        config = {
            "entities": [
                {
                    "type": "BoxEntityUI",
                    "name": "box1",
                    "phy_type": "dynamic",
                    "center": [100, 200],
                    "angle": 45,
                    "size": [50, 50],
                    "color": [155, 0, 0]
                }
            ]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(config, f)
            f.flush()
            loader = ObjsLoader(f.name)
            objs = loader.load_objs()

        assert "box1" in objs['entities']
        entity = objs['entities']['box1']
        assert entity.name == "box1"
        assert entity.body.body_type == pymunk.Body.DYNAMIC

    def test_load_circle_entity(self):
        config = {
            "entities": [
                {
                    "type": "CircleEntityUI",
                    "name": "circle1",
                    "phy_type": "dynamic",
                    "center": [300, 600],
                    "r": 25
                }
            ]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(config, f)
            f.flush()
            loader = ObjsLoader(f.name)
            objs = loader.load_objs()

        assert "circle1" in objs['entities']

    def test_load_check_label(self):
        config = {
            "labels": [
                {
                    "type": "CheckLabelUI",
                    "name": "label1",
                    "property_name": "center",
                    "expected_value": [400, 400]
                }
            ]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(config, f)
            f.flush()
            loader = ObjsLoader(f.name)
            objs = loader.load_objs()

        assert "label1" in objs['labels']

    def test_load_constraint_resolves_targets(self):
        """验证约束的 target_b 正确解析（回归测试：原 bug 检查 target_a 而非 target_b）"""
        config = {
            "entities": [
                {
                    "type": "BoxEntityUI",
                    "name": "box_a",
                    "phy_type": "dynamic",
                    "center": [100, 100],
                    "size": [30, 30]
                },
                {
                    "type": "BoxEntityUI",
                    "name": "box_b",
                    "phy_type": "dynamic",
                    "center": [200, 200],
                    "size": [30, 30]
                }
            ],
            "constraints": [
                {
                    "type": "PinJointUI",
                    "name": "joint1",
                    "position": [150, 150],
                    "target_a": "box_a",
                    "target_b": "box_b",
                    "anchor_a": [0, 0],
                    "anchor_b": [0, 0]
                }
            ]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(config, f)
            f.flush()
            loader = ObjsLoader(f.name)
            objs = loader.load_objs()

        joint = objs['constraints']['joint1']
        assert joint.target_a is not None
        assert joint.target_b is not None
        assert joint.target_a.name == "box_a"
        assert joint.target_b.name == "box_b"  # 回归测试：原代码这里会是 None


class TestLevelLoader:
    """LevelLoader 集成测试"""

    def test_load_entities_from_real_level(self):
        """加载真实关卡 level_1 的 scene.json"""
        loader = LevelLoader('levels/level_1/scene.json')
        entities = loader.load_entities()
        assert 'box1' in entities['entities']
        assert 'circle1' in entities['entities']
        assert 'box2' in entities['entities']
        assert 'poly1' in entities['entities']

    def test_load_inventory_from_real_level(self):
        """加载真实关卡 level_1 的 inventory.json"""
        loader = LevelLoader('levels/level_1/inventory.json')
        objs = loader.load_entities()
        assert len(objs['labels']) == 4

    def test_setting_loader(self):
        """加载 setting.json"""
        from core.setting_loader import EngineLoader
        from core.engine import Engine
        engine = Engine()
        loader = EngineLoader(engine)
        loader.load_from_json('levels/level_1/setting.json')
        # level_1 的 setting.json 中 gravity=0，setter 直接设置 space.gravity
        assert engine.space.gravity == (0.0, 0.0)


class TestRealLevelIntegration:
    """真实关卡集成测试"""

    def test_load_level_1_scene_and_inventory(self):
        """完整加载 level_1 的场景和物品栏"""
        scene_objs = ObjsLoader('levels/level_1/scene.json').load_objs()
        inventory_objs = ObjsLoader('levels/level_1/inventory.json').load_objs()

        # 场景应包含 4 个实体
        assert len(scene_objs['entities']) == 4
        # 物品栏应包含 4 个标签
        assert len(inventory_objs['labels']) == 4

        # 合并后不应冲突
        all_entities = {**inventory_objs['entities'], **scene_objs['entities']}
        all_labels = {**inventory_objs['labels'], **scene_objs['labels']}
        assert len(all_entities) == 4
        assert len(all_labels) == 4

    def test_sand_box_level_loads(self):
        """沙盒模式可加载"""
        objs = ObjsLoader('levels/sand_box/scene.json').load_objs()
        assert 'entities' in objs
