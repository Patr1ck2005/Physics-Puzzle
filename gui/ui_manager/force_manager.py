from gui.phy_obj_ui.force_ui import ForceUI


class ForceManager:
    running_forces: dict[str, ForceUI]

    def __init__(self, space):
        self.space = space
        self.running_forces = {}
        self.selected_obj = None
        self.pressed_obj = None
        self.m_pos = None
        self.m_d_pos = None

    def update(self, m_pos):
        for force in self.running_forces.values():
            force.update(m_pos)

    def render_running_forces(self, screen):
        for force in self.running_forces.values():
            force.draw(screen)

    def add_force(self, force):
        self.running_forces[force.name] = force


