import random
from gym import spaces, Env
from game import Game
from utils import get_cell_coords
from rl_utils import AnimalShogiEnvLogic

class AnimalShogiEnv(Env):
    metadata = {'render.modes': ['human']}  # 添加metadata屬性
    def __init__(self):
        self.starting_player = 1 # 在這裡，我們默認設置玩家1為先手，但可以通過seed()方法來改變
        self.logic = AnimalShogiEnvLogic(starting_player=self.starting_player)

        # Define action space and observation space
        self.action_space = spaces.Discrete(60)  # Maximum possible actions
        n_discrete_values = [
            100,  # turn_count
            2,    # current_player
        ]
        # For the board
        n_discrete_values.extend([10, 2] * 12)  # 12 cells, each with piece type and player

        # For the storage
        n_discrete_values.extend([5] * 7 * 2)  # 7 slots for each of 2 players

        self.observation_space = spaces.MultiDiscrete(n_discrete_values)

    def convert_observation_to_array(self, observation_dict):
        PIECE_MAPPING = {
            'G': 1,
            'E': 2,
            'L': 3,
            'C': 4,
            'H': 5,  # 添加母雞的映射
            0: 0  # Assume 0 represents an empty cell
        }

        PLAYER_MAPPING = {
            1: 0,   # Map player 1 to 0
            -1: 1   # Map player -1 to 1
        }

        observation_array = [
            observation_dict["turn_count"],
            PLAYER_MAPPING[observation_dict["current_player"]],  # Use the player mapping
        ]
        for cell_name in ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4"]:
            piece = observation_dict["board"][cell_name][0]
            observation_array.append(PIECE_MAPPING.get(piece, 0))
            observation_array.append(PLAYER_MAPPING.get(observation_dict["board"][cell_name][1], 0))  # Use the player mapping

        # For the storage: ensure we always have 7 values for each player's storage
        storage_player1 = [PIECE_MAPPING.get(piece, 0) for piece in observation_dict["storage"]["1"]] + [0] * (7 - len(observation_dict["storage"]["1"]))
        storage_player2 = [PIECE_MAPPING.get(piece, 0) for piece in observation_dict["storage"]["-1"]] + [0] * (7 - len(observation_dict["storage"]["-1"]))

        observation_array.extend(storage_player1)
        observation_array.extend(storage_player2)
        
        assert all(isinstance(item, int) for item in observation_array), f"Non-int value found: {observation_array}"
        return observation_array


    def reset(self):
        # Reset the game to its initial state
        self.logic.create_initial_board_config()
        # return initial_state
        observation_dict = self.logic.generate_possible_actions()[0]
        observation_array = self.convert_observation_to_array(observation_dict)
        return observation_array


    def step(self, action_idx):  # 注意：`step` 方法還需要一個 `action` 參數
        observation, possible_actions = self.logic.generate_possible_actions()
        action_idx = action_idx % len(possible_actions)
        action = possible_actions[action_idx]

        is_game_over, notation_hist, current_player = self.logic.apply_action(action)  # 使用提供的動作
        reward_player1, reward_player2 = self.logic.calculate_reward(is_game_over, current_player)  # 計算獎勵

        # 這裡的 'done' 是一個布爾值，指示遊戲是否結束
        done = is_game_over

        # Return reward based on the current player
        reward = reward_player1 if current_player == 1 else reward_player2

        info = {'notation_hist': notation_hist, 'round_player': current_player}

        return observation, reward, done, info



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
        round_player = None

        while not is_game_over:
            action_idx = env.action_space.sample()
            observation, reward, is_game_over, info = env.step(action_idx) #每回合的動作
            notation_hist = info['notation_hist']
            round_player = info['round_player']
            # env.render() # 棋盤每回合變化的視覺呈現

            if round_player == 1:
                player1_total_reward += reward
            else:
                player2_total_reward += reward

        print(f"game: {g} using {len(notation_hist)} steps => notations: {notation_hist}")
        # for notation in notation_hist:
        #     print(notation)

        if len(notation_hist) >= 100:
            print("Draw!\n")
        elif round_player == 1:
            print("Player 1 wins!\n")
        else:
            print("Player 2 wins!\n")
    print(f"Player 1 total reward: {player1_total_reward}, Player 2 total reward: {player2_total_reward}, reward points: {reward}")
