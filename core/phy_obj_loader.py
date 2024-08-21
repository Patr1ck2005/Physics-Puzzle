import json
from gui.phy_obj_ui.entity_ui import BoxEntityUI, CircleEntityUI, BlankEntityUI


class EntityLoader:
    def __init__(self, entities_json_file):
        self.entities_json_file = entities_json_file
        self.entities = {}

    def load_entities(self):
        with open(self.entities_json_file, 'r') as f:
            config = json.load(f)

        for entity_config in config['entities']:
            entity = self.create_entity(entity_config)
            if entity:
                self.entities[entity_config['name']] = entity

        return self.entities

    def create_entity(self, entity_config):
        entity_type = entity_config.get("type")

        if entity_type == "BoxEntityUI":
            return BoxEntityUI(
                name=entity_config["name"],
                phy_type=entity_config["phy_type"],
                position=tuple(entity_config["position"]),
                angle=entity_config.get("angle", 0),
                size=tuple(entity_config.get("size", (30, 30))),
                ico_path=entity_config.get("ico_path"),
                color=tuple(entity_config.get("color", (150, 150, 150)))
            )
        elif entity_type == "CircleEntityUI":
            return CircleEntityUI(
                name=entity_config["name"],
                phy_type=entity_config["phy_type"],
                center=tuple(entity_config["center"]),
                angle=entity_config.get("angle", 0),
                r=entity_config.get("r", 20),
                ico_path=entity_config.get("ico_path"),
                color=tuple(entity_config.get("color", (150, 150, 150)))
            )
        elif entity_type == "BlankEntityUI":
            return BlankEntityUI(
                name=entity_config.get("name", "Blank"),
                phy_type=entity_config.get("phy_type", "None"),
                center=tuple(entity_config.get("center", (0, 0))),
                angle=entity_config.get("angle", 0),
                size=tuple(entity_config.get("size", (0, 0))),
                ico_color=tuple(entity_config.get("ico_color", (150, 150, 150)))
            )
        return None
