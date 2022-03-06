from loguru import logger


def seed_everything(seed: int, cudnn_deterministic: bool = False) -> None:
    set_python_seed(seed)
    set_numpy_seed(seed)
    set_torch_seed(seed, cudnn_deterministic)
    logger.info(f"set every seed({seed}).")


def set_python_seed(seed: int) -> None:
    import os
    import random

    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    logger.info(f"set python seed({seed}).")


def set_numpy_seed(seed: int) -> None:
    import numpy as np

    np.random.seed(seed)
    logger.info(f"set numpy seed({seed}).")


def set_torch_seed(seed: int, cudnn_deterministic: bool) -> None:
    import torch

    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    if cudnn_deterministic:
        torch.backends.cudnn.deterministic = True
        logger.warning(
            "You have chosen to seed training. This will turn on the CUDNN deterministic setting, "
            "which can slow down your training considerably! You may see unexpected behavior "
            "when restarting from checkpoints."
        )
    torch.backends.cudnn.benchmark = True
    logger.info(f"set torch seed({seed}).")
