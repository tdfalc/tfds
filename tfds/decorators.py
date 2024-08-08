from pathlib import Path
import os
import hashlib
from functools import wraps

import cloudpickle


def cache(
    save_dir: Path,
    use_cache=True,
    extra_mem_cache=True,
):
    mem_cache = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__

            # Serialize arguments and keyword arguments using cloudpickle
            pickle_str = cloudpickle.dumps((args, kwargs))
            input_hash = hashlib.sha256(pickle_str).hexdigest()[:8]

            # Construct the cache path
            cache_path = save_dir / f"{func_name}_{input_hash}.pkl"

            if use_cache:
                if extra_mem_cache and cache_path in mem_cache:
                    return mem_cache[cache_path]

                if cache_path.exists():
                    with open(cache_path, "rb") as f:
                        result = cloudpickle.load(f)
                        mem_cache[cache_path] = result
                        return result

            result = func(*args, **kwargs)
            mem_cache[cache_path] = result

            # Create the directory if it doesn't exist
            if not save_dir.exists():
                os.makedirs(save_dir, exist_ok=True)

            # Save the result to the cache
            with open(cache_path, "wb") as f:
                cloudpickle.dump(result, f)

            return result

        return wrapper

    return decorator
