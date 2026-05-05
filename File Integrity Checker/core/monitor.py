from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

modified_count = 0
deleted_count = 0
new_count = 0


class MonitorHandler(FileSystemEventHandler):

    def __init__(self, socketio):
        self.socketio = socketio

    def send_update(self, msg):
        global modified_count, deleted_count, new_count

        self.socketio.emit("update", {
            "modified": modified_count,
            "deleted": deleted_count,
            "new": new_count,
            "log": msg
        })

    def on_created(self, event):
        global new_count

        if not event.is_directory:
            msg = f"🟢 New File: {event.src_path}"
            print(msg)

            new_count += 1
            self.send_update(msg)

    def on_modified(self, event):
        global modified_count

        if not event.is_directory:
            msg = f"🟠 Modified: {event.src_path}"
            print(msg)

            modified_count += 1
            self.send_update(msg)

    def on_deleted(self, event):
        global deleted_count

        if not event.is_directory:
            msg = f"🔴 Deleted: {event.src_path}"
            print(msg)

            deleted_count += 1
            self.send_update(msg)


def start_monitor(path, socketio, app):
    print("📂 Monitoring folder:", path)

    handler = MonitorHandler(socketio)
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()

    print("🚀 Real-time monitoring started...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()