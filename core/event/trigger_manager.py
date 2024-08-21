import logging

# Configure the logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class State:
    def __init__(self, name):
        self.name = name
        self.triggers = []

    def add_trigger(self, trigger):
        logging.info(f"Trigger added to state '{self.name}': {trigger}")
        self.triggers.append(trigger)

    def check_triggers(self):
        # logging.info(f"Checking triggers for state '{self.name}'")
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
        logging.info("TriggerManager initialized")

    def add_state(self, state):
        """Adds a state to the manager."""
        self.states[state.name] = state
        logging.info(f"State added: {state.name}")

    def set_initial_state(self, state_name):
        """Sets the initial state of the manager."""
        if state_name in self.states:
            self.current_state = self.states.get(state_name)
            logging.info(f"Initial state set to: {state_name}")
        else:
            logging.error(f"State '{state_name}' does not exist. Cannot set initial state.")

    def add_trigger_to_state(self, state_name, trigger):
        """Adds a trigger to a specific state."""
        if state_name in self.states:
            self.states[state_name].add_trigger(trigger)
            logging.info(f"Trigger added to state '{state_name}': {trigger}")
        else:
            logging.error(f"State '{state_name}' does not exist. Cannot add trigger.")

    def check_triggers(self):
        """Checks triggers in the current state and triggers events."""
        if self.current_state:
            # logging.info(f"Checking triggers for current state: {self.current_state.name}")
            self.current_state.check_triggers()
        else:
            pass
            # logging.warning("No current state set. Cannot check triggers.")

    def transition_to_state(self, new_state_name):
        """Handles the transition to a new state."""
        if new_state_name in self.states:
            logging.info(f"Transitioning from {self.current_state.name if self.current_state else 'None'} to {new_state_name}")
            self.current_state = self.states[new_state_name]
        else:
            logging.error(f"State '{new_state_name}' does not exist. Cannot transition.")

    def draw_triggers(self, screen):
        """Draws triggers for the current state on the screen."""
        if self.current_state:
            # logging.info(f"Drawing triggers for state: {self.current_state.name}")
            for trigger in self.current_state.triggers:
                trigger.draw(screen)
        else:
            pass
            # logging.warning("No current state set. Cannot draw triggers.")
