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
        is_game_over, notation_hist, winner = self.logic.apply_action()
        reward_player1, reward_player2 = self.logic.calculate_reward(is_game_over, winner)
        
        observation = self.logic.get_current_game_state()

        # 這裡的 'done' 是一個布爾值，指示遊戲是否結束
        done = is_game_over
        
        # 返回當前的觀察、兩個玩家的獎勵、遊戲是否結束、以及其他可能的資訊
        return observation, (reward_player1, reward_player2), done, notation_hist


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
    player1_total_reward = 0
    player2_total_reward = 0

    for g in range(10):
        env = AnimalShogiEnv()
        initina_state = env.reset()
        
        is_game_over = False
        notation_hist = None
        winner = None

        while not is_game_over:
            observation, (reward_player1, reward_player2), is_game_over, notation_hist = env.step()
            # print(observation)
            player1_total_reward += reward_player1
            player2_total_reward += reward_player2

        # for hist in notation_hist:
        #     print(hist)
        print(f"game: {g} using {len(notation_hist)} steps")

        if reward_player1 == 5:
            print("Player 1 wins!")
        elif reward_player2 == 5:
            print("Player 2 wins!")
        else:
            print("Draw!")
    print(f"Player 1 total reward: {player1_total_reward}, Player 2 total reward: {player2_total_reward}")
