import threading


def fire_and_forget(f):
    def wrapped():
        threading.Thread(target=f).start()

    return wrapped
