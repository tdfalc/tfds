from pathlib import Path
import os
import hashlib
from functools import wraps
from typing import Union, Callable, Any, Callable, Union

import cloudpickle


def cache(save_location: Union[str, Path], use_cache: bool = True) -> Callable:
    """
    A decorator that caches function results based on input arguments.

    Args:
        save_location (Union[str, Path]): Directory to save cache files.
        use_cache (bool): Whether to use disk caching. Defaults to True.

    Returns:
        Callable: The decorated function.
    """
    save_location = Path(save_location)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not use_cache:
                return func(*args, **kwargs)

            func_name = func.__name__
            input_hash = hashlib.sha256(cloudpickle.dumps((args, kwargs))).hexdigest()[
                :16
            ]
            cache_path = save_location / f"{func_name}_{input_hash}.pkl"

            if use_cache and cache_path.exists():
                with cache_path.open("rb") as f:
                    result = cloudpickle.load(f)
                    return result

            result = func(*args, **kwargs)

            if use_cache:
                save_location.mkdir(parents=True, exist_ok=True)
                with cache_path.open("wb") as f:
                    cloudpickle.dump(result, f)

            return result

        return wrapper

    return decorator


def blind_file_cache(
    save_location: Union[str, Path], use_cache: bool = True
) -> Callable:
    """
    A decorator that blindly caches the output of the wrapped function to disk using cloudpickle.

    This cache is "blind" in that it doesn't consider input arguments when retrieving cached results.
    It's suitable for functions without inputs or those where inputs are not expected to change.

    Args:
        save_location (Union[str, Path]): The file path to save the cache to.
        use_cache (bool): Whether to use the cache. Defaults to True.

    Returns:
        Callable: The decorated function.

    Example:
        @blind_file_cache(save_location='path/to/cache.pkl')
        def expensive_computation():
            # ... perform expensive computation ...
            return result
    """
    save_path = Path(save_location)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if use_cache and save_path.exists():
                with save_path.open("rb") as f:
                    return cloudpickle.load(f)

            result = func(*args, **kwargs)
            if not save_location.exists():
                os.makedirs(save_location.parent, exist_ok=True)
            with open(save_location, "wb") as f:
                cloudpickle.dump(result, f)
            return result

        return wrapper

    return decorator
