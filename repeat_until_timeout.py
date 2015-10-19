# The basic idea is to use signal handlers to set an alarm for some time interval and raise an exception once that timer expires.
# Note that this will only work on UNIX.
# http://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish
from functools import wraps
import signal
from selenium.common.exceptions import NoSuchElementException

TIMEOUT_OCCURRED = 'Timeout occurred'

__version__ = '0.01'
class TimeoutError(AssertionError):
    pass


def repeat_until_timeout(seconds=15):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(str(repeat_until_timeout_last_error))

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                global repeat_until_timeout_last_error
                repeat_until_timeout_last_error = TimeoutError(TIMEOUT_OCCURRED)
                while True:
                    try:
                        return func(*args, **kwargs)
                    except TimeoutError as e:
                        raise e
                    except Exception as e:
                        repeat_until_timeout_last_error = e
            finally:
                signal.alarm(0)

        return wraps(func)(wrapper)

    return decorator
