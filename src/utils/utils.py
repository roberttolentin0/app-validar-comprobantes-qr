import time


def measure_time(func):
    ''' Decorator para medir tiempo de ejecución'''
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"La función {func.__name__} tardó {total_time:.2f} segundos en ejecutarse")
        return result
    return wrapper