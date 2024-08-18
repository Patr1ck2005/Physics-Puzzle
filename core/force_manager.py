from gui.force_ui import ForceUI


class ForceManager:
    running_forces: dict[str, ForceUI]

    def __init__(self, screen, space):
        self.screen = screen
        self.space = space
        self.running_forces = {}
        self.selected_obj = None
        self.pressed_obj = None
        self.m_pos = None
        self.m_d_pos = None

    def update(self, m_pos):
        for force in self.running_forces.values():
            force.update(m_pos)

    def render_running_forces(self):
        for force in self.running_forces.values():
            force.draw(self.screen)

    def add_force(self, force):
        self.running_forces[force.name] = force


