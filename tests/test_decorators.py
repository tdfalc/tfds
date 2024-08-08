import os

import cloudpickle

from tfds.decorators import cache


def cached_function(tmp_path, use_cache):
    @cache(tmp_path, use_cache=use_cache)
    def f(x):
        return x

    return f


def test_cache(tmp_path):

    input = "input"
    cached_function(tmp_path, use_cache=True)(input)

    fname = os.listdir(tmp_path).pop()
    with open(tmp_path / fname, "rb") as f:
        output = cloudpickle.load(f)
        assert output == input
