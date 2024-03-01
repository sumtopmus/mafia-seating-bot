from dynaconf import settings


class ProgressBar():
    def __init__(self, total, callback=None):
        self.progress = 0
        self.total = total
        self.callback = callback
        self.last_called = 0

    async def update(self, increment=1):
        self.progress += increment
        if self.progress > self.total:
            self.progress = self.total
        if self.callback is not None:
            # Calculate current progress percentage.
            progress_percentage = self.progress / self.total * 100
            # If progress has increased by a threshold.
            if progress_percentage - self.last_called >= settings.MINIMAL_PROGRESS:
                await self.callback(self.progress, self.total)
                # Update the last called progress.
                self.last_called = progress_percentage
