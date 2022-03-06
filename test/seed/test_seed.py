def test_set_numpy_seed() -> None:
    from util.seed.seed import set_numpy_seed

    seed = 42
    import numpy as np

    set_numpy_seed(seed)
    state = np.random.get_state()
    assert seed == state[1][0]
