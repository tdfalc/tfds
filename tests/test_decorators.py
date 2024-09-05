import pytest
import time

from tfds.decorators import cache, blind_file_cache


@pytest.fixture
def temp_cache_dir(tmp_path):
    return tmp_path / "test_cache"


@pytest.fixture
def temp_cache_file(tmp_path):
    return tmp_path / "test_cache.pkl"


def test_cache(temp_cache_dir):
    call_count = 0

    @cache(save_location=temp_cache_dir)
    def test_func(x, y):
        nonlocal call_count
        call_count += 1
        return x + y

    # First call
    assert test_func(1, 2) == 3
    assert call_count == 1

    # Cached call
    assert test_func(1, 2) == 3
    assert call_count == 1  # Should use cache

    # Different arguments
    assert test_func(3, 4) == 7
    assert call_count == 2  # New args, should call function

    # Verify disk cache
    assert len(list(temp_cache_dir.glob("*"))) == 2  # Two cache files should exist


def test_cache_disabled(temp_cache_dir):
    call_count = 0

    @cache(save_location=temp_cache_dir, use_cache=False)
    def test_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    assert test_func(5) == 10
    assert test_func(5) == 10
    assert call_count == 2  # Should call function twice


def test_blind_file_cache(temp_cache_file):

    call_count = 0

    @cache(save_location=temp_cache_file)
    def test_func(x, y):
        nonlocal call_count
        call_count += 1
        return x + y

    # First call
    assert test_func(1, 2) == 3
    assert call_count == 1

    # Cached call
    assert test_func(1, 2) == 3
    assert call_count == 1  # Should use cache

    # Different arguments
    assert test_func(3, 4) == 7
    assert call_count == 2  # New args, should call function

    # Verify disk cache
    assert temp_cache_file.exists()


def test_cache_bypass(temp_cache_file):

    call_count = 0

    @cache(save_location=temp_cache_file, use_cache=False)
    def test_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    assert test_func(5) == 10
    assert test_func(5) == 10
    assert call_count == 2  # Should call function twice

    # No file should exist
    assert not temp_cache_file.exists()
