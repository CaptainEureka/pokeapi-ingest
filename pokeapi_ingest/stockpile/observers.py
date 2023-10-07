from typing import Protocol

from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn


class IProgressObserver(Protocol):
    def start(self, total_count: int):
        pass

    def update(self, increment: int):
        pass

    def complete(self):
        pass


class RichProgressObserver(IProgressObserver):
    def __init__(self, description: str):
        self.progress = Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.1f}%",
            TimeElapsedColumn(),
        )
        self.description = description
        self.task_id = None

    def start(self, total_count: int):
        self.task_id = self.progress.add_task(
            f"[cyan]{self.description}", total=total_count
        )

    def update(self, increment: int):
        assert self.task_id is not None, "Update should be run after .start"
        self.progress.update(self.task_id, advance=increment)

    def complete(self):
        pass  # You can perform any completion actions here

    def __enter__(self):
        return self.progress.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        return self.progress.__exit__(exc_type, exc_value, traceback)
