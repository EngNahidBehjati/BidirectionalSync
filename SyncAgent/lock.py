import fcntl
import sys


class SingleInstanceLock:
    def __init__(self, path="/var/lock/sync-agent.lock"):
        self.path = path
        self.fd = None

    def acquire(self):
        self.fd = open(self.path, "w")
        try:
            fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            sys.exit(0)

    def release(self):
        if self.fd:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
            self.fd.close()
