from django.core.cache import cache
import time
from contextlib import contextmanager

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes

def cache_output(func):
    def decorator(*args, **kwargs):
        cache_key = kwargs.pop('cache_key')
        cached_output = cache.get(cache_key)
        if not cached_output:
            with cache_lock(cache_key + 'in_progress') as lock:
                if not lock:
                    timeout = 0
                    while timeout < LOCK_EXPIRE:
                        cached_output = cache.get(cache_key)
                        if cached_output:
                            break
                        timeout += 1
                        time.sleep(1)
                cached_output = func(*args, **kwargs)
                cache.set(cache_key, cached_output)
        return cached_output
    return decorator



# https://docs.celeryproject.org/en/latest/tutorials/task-cookbook.html
@contextmanager
def cache_lock(lock_id):
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = cache.add(lock_id, True, LOCK_EXPIRE)
    try:
        yield status
    finally:
        # memcache delete is very slow, but we have to use it to take
        # advantage of using add() for atomic locking
        if time.monotonic() < timeout_at and status:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else
            # also don't release the lock if we didn't acquire it
            cache.delete(lock_id)