import time
import threading

class VirtualSimEngine:
    def __init__(self, tick = 60):
        self.tick = tick
        self.delta_time = 0
        self.running = False
        self.paused = False
        self.lock = threading.Lock()
        self.condition = threading.Condition()
        self.object_list = [] #엔진에서 처리될 object list

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        print("engine start")

    def pause(self):
        with self.condition:
            self.paused = True
            print("engine paused")

    def play(self):
        with self.condition:
            self.paused = False
            self.condition.notify_all()
            print("engine resumed")

    def stop(self):
        self.running = False
        self.thread.join() 
        print("engine stop")

    def run(self):
        sleep_time = 0.0
        real_sleep_time = 0.0
        sleep_diff = 0.0
        while self.running:
            with self.condition:
                while self.paused:
                    self.condition.wait()
            start_time = time.time()
            self.open_objects()
            self.update_objects()
            self.final_objects()
            elapsed_time = time.time() - start_time

            real_sleep_start = time.time()
            sleep_diff = real_sleep_time - sleep_time
            sleep_time = max(0, (1/self.tick) - elapsed_time - sleep_diff)
            time.sleep(sleep_time)
            real_sleep_time = time.time() - real_sleep_start

            self.delta_time = real_sleep_time + elapsed_time

    def open_objects(self):
        with self.lock:
            for object in self.object_list:
                object.open()

    def update_objects(self):
        with self.lock:
            for object in self.object_list:
                object.update()

    def final_objects(self):
        with self.lock:
            for object in self.object_list:
                object.final()

    def register_object(self, object):
        with self.lock:
            self.object_list.append(object)
            print(f"Registered object: {object, object.name}")

    def unregister_object(self, object):
        with self.lock:
            if object in self.object_list:
                self.object_list.remove(object)
                print(f"Unregistered object: {object, object.name}")

    def get_object_list(self):
        with self.lock:
            return self.object_list.copy()