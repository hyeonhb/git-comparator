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
        self.object_list = [] #엔진에서 처리될 obj list

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
        if self.paused:
            self.play()
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
            for obj in self.object_list:
                obj.open()

    def update_objects(self):
        with self.lock:
            for obj in self.object_list:
                obj.update()

    def final_objects(self):
        with self.lock:
            for obj in self.object_list:
                obj.final()

    def register_object(self, obj):
        with self.lock:
            self.object_list.append(obj)
            print(f"Registered obj: {obj, obj.name}")

    def unregister_object(self, obj):
        with self.lock:
            if obj in self.object_list:
                self.object_list.remove(obj)
                print(f"Unregistered obj: {obj, obj.name}")

    def get_object_list(self):
        with self.lock:
            return self.object_list.copy()