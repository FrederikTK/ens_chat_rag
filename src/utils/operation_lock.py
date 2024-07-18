import os
import time

class OperationLock:
    def __init__(self, lock_file_path="/app/data/operation.lock"):
        self.lock_file = lock_file_path

    def acquire(self, operation_name, timeout=60):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not os.path.exists(self.lock_file):
                with open(self.lock_file, 'w') as f:
                    f.write(operation_name)
                return True
            time.sleep(1)
        return False

    def release(self):
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)

    def get_current_operation(self):
        if os.path.exists(self.lock_file):
            with open(self.lock_file, 'r') as f:
                return f.read().strip()
        return None