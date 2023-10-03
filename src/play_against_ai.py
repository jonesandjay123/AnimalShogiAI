import torch
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from animal_shogi_gym import AnimalShogiEnv

# 載入模型
model = PPO.load("animal_shogi_ppo_1000000.zip")

# # 確保你的觀察空間(observation space)和動作空間(action space)與訓練時使用的相同
# # 你可能需要創建一個dummy環境(dummy environment)來設置這些
# dummy_env = YourCustomEnvironment()  # 你的環境類
# dummy_env = DummyVecEnv([lambda: dummy_env])

# # 用你的觀察值(observation)生成動作(action)
# # 注意：你可能需要將觀察值轉換為模型可以接受的格式
# observation = dummy_env.reset()
# action, _ = model.predict(observation, deterministic=True)

# 現在你可以使用這個動作在你的環境中進行一步操作
# observation, reward, done, info = env.step(action)
if __name__ == "__main__":
    player1_total_reward = 0
    player2_total_reward = 0

    for g in range(1):
        env = AnimalShogiEnv()
        env.seed() # 使用 seed 方法隨機選擇先手玩家

        observation = env.reset()
        
        is_game_over = False
        notation_hist = None
        round_player = None

        while not is_game_over:
            action, _ = model.predict(observation, deterministic=True)
            observation, reward, is_game_over, info = env.step(action) #每回合的動作
            notation_hist = info['notation_hist']
            round_player = info['round_player']
            # env.render() # 棋盤每回合變化的視覺呈現

            if round_player == 1:
                player1_total_reward += reward
            else:
                player2_total_reward += reward

        print(f"game: {g} using {len(notation_hist)} steps => notations: {notation_hist}")

        if len(notation_hist) >= 100:
            print("Draw!\n")
        elif round_player == 1:
            print("Player 1 wins!\n")
        else:
            print("Player 2 wins!\n")

    print(f"Player 1 total reward: {player1_total_reward}, Player 2 total reward: {player2_total_reward}, reward points: {reward}")
