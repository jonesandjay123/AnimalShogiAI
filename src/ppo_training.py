import random
from gym import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.envs import DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback
from animal_shogi_gym import AnimalShogiEnv

class SimpleSaveCallback(BaseCallback):
    """
    每隔特定的timesteps保存模型。
    """
    def __init__(self, check_freq: int, save_path: str, verbose=1):
        super(SimpleSaveCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:
            if self.verbose > 0:
                print(f"Saving model at timesteps: {self.num_timesteps}")
            self.model.save(f"{self.save_path}_{self.num_timesteps}")
        return True

def train_and_save_model():
    """
    訓練模型並保存。
    """
    # 1. 創建和包裝你的環境
    env = DummyVecEnv([lambda: AnimalShogiEnv()])  # SB3的環境需要向量化，即使只有一個

    # 2. 初始化PPO代理
    model = PPO("MlpPolicy", env, verbose=1)

    # 定義回調函數
    callback = SimpleSaveCallback(check_freq=10000, save_path="animal_shogi_ppo")

    # 3. 訓練模型
    model.learn(total_timesteps=100000, callback=callback)
def load_and_continue_training():
    """
    加載已有的模型並繼續訓練。
    """
    loaded_model = PPO.load("animal_shogi_ppo")
    env = DummyVecEnv([lambda: AnimalShogiEnv()])  # 必須再次建立環境
    loaded_model.set_env(env)
    loaded_model.learn(total_timesteps=50000)

def test_model():
    """
    測試模型。
    """
    env = DummyVecEnv([lambda: AnimalShogiEnv()])
    model = PPO.load("animal_shogi_ppo")
    obs = env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render()  # 如果你想視覺化遊戲進行

if __name__ == "__main__":
    # 選擇以下操作之一來執行：
    train_and_save_model()  # 訓練模型並保存
    # load_and_continue_training()  # 加載模型並繼續訓練
    # test_model()  # 測試模型