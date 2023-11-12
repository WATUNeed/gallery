from celery import Celery
from celery.schedules import crontab

from backend.config.rabbit import RABBITMQ_CONFIG
from backend.api.user.models import User
from backend.api.collection.models import Collection, CollectionDownloadQueryHistory
from backend.api.photo.models import Photo, PhotoRate
from backend.api.rate.models import Rate
from backend.events.database import update_photo_rate_after_insert_in_rate

celery_app = Celery(
    'celery_scheduler',
    broker=RABBITMQ_CONFIG.connection_url,
    # backend=REDIS_CONFIG.connection_url(),
    broker_connection_retry_on_startup=True
)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from backend.api.collection.tasks import task_make_magic

    sender.add_periodic_task(
        10.0,
        # crontab(minute='*'),
        task_make_magic.s(),
        name='Every minute'
    )


if __name__ == '__main__':
    celery_app.start()
