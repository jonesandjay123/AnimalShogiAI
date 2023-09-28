from tqdm import tqdm
from stable_baselines3.common.callbacks import BaseCallback


class TQDMProgressBar(BaseCallback):
    """
    TQDM ProgressBar callback for Stable Baselines3.
    """
    def __init__(self, total_timesteps=1000000):  # <-- total_timesteps is necessary now
        super(TQDMProgressBar, self).__init__()
        self.pbar = None
        self.total_timesteps = total_timesteps
        
    def _on_training_start(self):
        self.pbar = tqdm(total=self.total_timesteps, desc="Training progress")
        
    def _on_step(self):
        self.pbar.n = self.num_timesteps
        self.pbar.last_print_n = self.num_timesteps
        self.pbar.update()
        return True
    
    def _on_training_end(self):
        self.pbar.n = self.total_timesteps
        self.pbar.last_print_n = self.total_timesteps
        self.pbar.update()
        self.pbar.close()
