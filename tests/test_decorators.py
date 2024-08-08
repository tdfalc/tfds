import cloudpickle
import hashlib

from tfds.decorators import cache


def sample_function(tmp_path):
    @cache(save_dir=tmp_path, use_cache=True)
    def func(a, b):
        return a + b

    return func


def test_cache_decorator_new_computation(tmp_path):

    # Run the function and cache result
    result = sample_function(tmp_path)(2, 3)

    # Assert the result
    assert result == 5

    # Verify that cache file is created
    pickle_str = cloudpickle.dumps(((2, 3), {}))
    input_hash = hashlib.sha256(pickle_str).hexdigest()[:8]
    cache_path = tmp_path / f"func_{input_hash}.pkl"

    assert cache_path.exists()

    # Check cache content
    with open(cache_path, "rb") as f:
        cached_result = cloudpickle.load(f)

    assert cached_result == result
