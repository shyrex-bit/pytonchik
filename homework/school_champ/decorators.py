def log_action(func):
    def wrapper(self, name, points):
        print("[LOG] Выполняется действие:", func.__name__)
        return func(self, name, points)

    return wrapper