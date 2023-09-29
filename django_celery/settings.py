import os
CELERY_BROKER_URL = f"redis://:{os.environ['REDIS_PASSWORD']}@{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}"
CELERY_RESULT_BACKEND = f"redis://:{os.environ['REDIS_PASSWORD']}@{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}"