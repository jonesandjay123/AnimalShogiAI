import random
from gym import spaces
from game import Game
from utils import get_cell_coords
from rl_utils import AnimalShogiEnvLogic

class AnimalShogiEnv:
    def __init__(self):
        self.starting_player = 1 # 在這裡，我們默認設置玩家1為先手，但可以通過seed()方法來改變
        self.logic = AnimalShogiEnvLogic(starting_player=self.starting_player)

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


    def step(self, action_idx):  # 注意：`step` 方法還需要一個 `action` 參數
        is_game_over, notation_hist, winner = self.logic.apply_action()  # 使用提供的動作
        reward_player1, reward_player2 = self.logic.calculate_reward(is_game_over, winner)

        _, action_list = self.logic.generate_possible_actions()
        
        observation = self.logic.get_current_game_state()

        # 這裡的 'done' 是一個布爾值，指示遊戲是否結束
        done = is_game_over
        
        return observation, (reward_player1, reward_player2), done, notation_hist


    def render(self, mode='human'):
        board = [['---' for _ in range(4)] for _ in range(4)]
        
        # Get current game state
        game_state = self.logic.get_current_game_state()

        # Fill in the board with pieces
        for cell_name, piece_data in game_state['board'].items():
            col, row = get_cell_coords(cell_name)  # Assuming you have this function or a similar one
            piece_type = piece_data[0]
            player = piece_data[1]
            board[row-1][col-1] = f"{piece_type}{'+' if player == 1 else '-'}{abs(player)}"

        # Print the board
        for row in board:
            print(" | ".join(row))
            print("-" * 17)

        # Print storage areas for both players
        print(f"Player 1 Storage: {game_state['storage']['1']}")
        print(f"Player 2 Storage: {game_state['storage']['-1']}")


    def seed(self, seed=None):
        # Set random seed if provided
        if seed is not None:
            random.seed(seed)

        # 隨機選擇一個玩家作為先手
        starting_player = random.choice([1, -1])
        self.logic.set_starting_player(starting_player)

        # 根據 starting_player 的值，決定顯示 "Player 1" 或 "Player 2"
        player_str = "Player 1" if starting_player == 1 else "Player 2"
        print(f"{player_str} starts first!")

    def close(self):
        pass  # 如果有任何清理工作需要在關閉環境時執行，可以在這裡添加

if __name__ == "__main__":
    player1_total_reward = 0
    player2_total_reward = 0

    for g in range(10):
        env = AnimalShogiEnv()
        env.seed() # 使用 seed 方法隨機選擇先手玩家

        initina_state = env.reset()
        
        is_game_over = False
        notation_hist = None
        winner = None

        while not is_game_over:
            env.logic.generate_possible_actions()
            observation, (reward_player1, reward_player2), is_game_over, notation_hist = env.step(0) #每回合的動作
            # env.render() # 棋盤每回合變化的視覺呈現

            player1_total_reward += reward_player1
            player2_total_reward += reward_player2

        print(f"game: {g} using {len(notation_hist)} steps")

        if reward_player1 == 5:
            print("Player 1 wins!")
        elif reward_player2 == 5:
            print("Player 2 wins!")
        else:
            print("Draw!")
    print(f"Player 1 total reward: {player1_total_reward}, Player 2 total reward: {player2_total_reward}")
