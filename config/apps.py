# beat 작업을 하게 되면 간혹 장고보다 celery가 먼저 실행되는 경우가 발생함
# 이를 방지하기 위해 절차를 걸어두는 코드라고 함
from django.apps import AppConfig

class ConfigAppConfig(AppConfig):
    name = 'config'

    def ready(self):
        import config.beat_tasks  # noqa