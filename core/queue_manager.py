import threading
from typing import List, Callable
from .downloader import DownloaderTask


class QueueManager:
    def __init__(self):
        self.tasks: List[DownloaderTask] = []
        self.on_task_added: Callable[[DownloaderTask], None] = None

    def add_task(self, task: DownloaderTask):
        self.tasks.append(task)
        if self.on_task_added:
            self.on_task_added(task)

        # Khởi chạy luồng download ngay khi add
        thread = threading.Thread(target=task.run, daemon=True)
        thread.start()

    def get_tasks(self) -> List[DownloaderTask]:
        return self.tasks