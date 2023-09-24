from gym import spaces
from game import Game
from rl_utils import AnimalShogiEnvLogic

class AnimalShogiEnv:
    def __init__(self):
        # Initialize game logic
        self.logic = AnimalShogiEnvLogic()

        # Define action space and observation space
        self.action_space = spaces.Discrete(60)  # Maximum possible actions
        self.observation_space = spaces.Dict({
            "turn_count": spaces.Discrete(100),  # Assuming a max of 100 turns
            "current_player": spaces.Discrete(2),  # Player 1 or -1
            "board": spaces.Dict({key: spaces.Tuple([spaces.Discrete(10), spaces.Discrete(2)]) for key in ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4"]}),
            "storage": spaces.Dict({"1": spaces.MultiDiscrete([5 for _ in range(7)]), "-1": spaces.MultiDiscrete([5 for _ in range(7)])})
        })

    def reset(self):
        # Reset the game to its initial state
        self.logic.create_initial_board_config()
        initial_state, _ = self.logic.generate_possible_actions()
        return initial_state


    def step(self):
        self.logic.apply_action()

        # Step 3: Calculate reward
        # reward = self.logic.calculate_reward(self.logic.game_over, self.logic.current_player)

        # # Step 4: Check if the game is over
        # done = self.logic.game_over

        # # Step 5: Return the results
        # new_state, _ = self.logic.generate_possible_actions()  # Or you can call generate_possible_actions again to get the new state after the action
        # info = {}  # Any additional info you'd like to return. For now, it's an empty dictionary.

        # return new_state, reward, done, info

    def render(self, mode='human'):
        # Visualization code (optional)
        pass

    def close(self):
        # Cleanup code (optional)
        pass

    def seed(self, seed=None):
        # Set random seed (optional)
        pass

if __name__ == "__main__":
    env = AnimalShogiEnv()
    initina_state = env.reset()
    print(initina_state)
    env.step()