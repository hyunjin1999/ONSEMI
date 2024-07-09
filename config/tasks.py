from celery import shared_task

@shared_task(bind=True)
def add(self, x, y):
    print(f"Task {self.request.id} started with arguments: {x}, {y}")
    result = x + y
    print(f"Task {self.request.id} finished with result: {result}")
    return result