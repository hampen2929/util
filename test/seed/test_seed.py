def test_set_numpy_seed() -> None:
    from util.seed.seed import set_numpy_seed

    seed = 42
    import numpy as np

    set_numpy_seed(seed)
    arr: np.ndarray
    _, arr, _, _, _ = np.random.get_state()  # type: ignore
    assert seed == arr[0]
