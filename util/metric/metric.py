import functools
import os
import time
from collections import defaultdict, deque
from typing import Optional, Tuple

import numpy as np
import torch

__all__ = [
    "AverageMeter",
    "MeterBuffer",
    "get_total_and_free_memory_in_Mb",
    "occupy_mem",
    "gpu_mem_usage",
]


def get_total_and_free_memory_in_Mb(cuda_device: str) -> Tuple[int, int]:
    devices_info_str = os.popen("nvidia-smi --query-gpu=memory.total,memory.used --format=csv,nounits,noheader")
    devices_info = devices_info_str.read().strip().split("\n")
    total, used = devices_info[int(cuda_device)].split(",")
    return int(total), int(used)


def occupy_mem(cuda_device: str, mem_ratio: float = 0.9) -> None:
    """
    pre-allocate gpu memory for training to avoid memory Fragmentation.
    """
    total, used = get_total_and_free_memory_in_Mb(cuda_device)
    max_mem = int(total * mem_ratio)
    block_mem = max_mem - used
    x = torch.cuda.FloatTensor(256, 1024, block_mem)
    del x
    time.sleep(5)


def gpu_mem_usage() -> int:
    """
    Compute the GPU memory usage for the current device (MB).
    """
    mem_usage_bytes = torch.cuda.max_memory_allocated()
    return mem_usage_bytes / (1024 * 1024)


class AverageMeter:
    """Track a series of values and provide access to smoothed values over a
    window or the global series average.
    """

    def __init__(self, window_size: int = 50) -> None:
        self._deque = deque(maxlen=window_size)
        self._total = 0.0
        self._count = 0

    def update(self, value: float) -> None:
        self._deque.append(value)
        self._count += 1
        self._total += value

    @property
    def median(self):
        d = np.array(list(self._deque))
        return np.median(d)

    @property
    def avg(self) -> float:
        # if deque is empty, nan will be returned.
        d = np.array(list(self._deque))
        return d.mean()

    @property
    def global_avg(self) -> float:
        return self._total / max(self._count, 1e-5)

    @property
    def latest(self) -> deque:
        return self._deque[-1] if len(self._deque) > 0 else None

    @property
    def total(self) -> float:
        return self._total

    def reset(self) -> None:
        self._deque.clear()
        self._total = 0.0
        self._count = 0

    def clear(self) -> None:
        self._deque.clear()


class MeterBuffer(defaultdict):
    """Computes and stores the average and current value"""

    def __init__(self, window_size=20):
        factory = functools.partial(AverageMeter, window_size=window_size)
        super().__init__(factory)

    def reset(self) -> None:
        for v in self.values():
            v.reset()

    def get_filtered_meter(self, filter_key: str = "time"):
        return {k: v for k, v in self.items() if filter_key in k}

    def update(self, values: Optional[float] = None, **kwargs) -> None:
        if values is None:
            values = {}
        values.update(kwargs)
        for k, v in values.items():
            if isinstance(v, torch.Tensor):
                v = v.detach()
            self[k].update(v)

    def clear_meters(self) -> None:
        for v in self.values():
            v.clear()
