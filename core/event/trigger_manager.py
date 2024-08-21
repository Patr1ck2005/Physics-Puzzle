class State:
    def __init__(self, name):
        self.name = name
        self.triggers = []

    def add_trigger(self, trigger):
        self.triggers.append(trigger)

    def check_triggers(self):
        for trigger in self.triggers:
            trigger.check_and_trigger()


class TriggerManager:
    def __init__(self, event_state_machine):
        """
        Initializes the Trigger Manager.
        :param event_state_machine: Instance of event state machine for state management.
        """
        self.states = {}
        self.current_state = None
        self.event_state_machine = event_state_machine

    def add_state(self, state):
        """Adds a state to the manager."""
        self.states[state.name] = state

    def set_initial_state(self, state_name):
        """Sets the initial state of the manager."""
        self.current_state = self.states.get(state_name)

    def add_trigger_to_state(self, state_name, trigger):
        """Adds a trigger to a specific state."""
        if state_name in self.states:
            self.states[state_name].add_trigger(trigger)

    def check_triggers(self):
        """Checks triggers in the current state and triggers events."""
        if self.current_state:
            self.current_state.check_triggers()

    def transition_to_state(self, new_state_name):
        """Handles the transition to a new state."""
        if new_state_name in self.states:
            print(f"Transitioning from {self.current_state.name} to {new_state_name}")
            self.current_state = self.states[new_state_name]
        else:
            print(f"State {new_state_name} does not exist.")
