from sqlalchemy import event, Connection, func, create_engine
from sqlalchemy.orm import Session

from backend.api.photo.models import Photo
from backend.api.rate.models import Rate
from backend.config.database import DB_CONFIG


@event.listens_for(Rate, 'after_insert')
def update_photo_rate_after_insert_in_rate(mapper, connection: Connection, target: Rate):
    session = Session(bind=create_engine(DB_CONFIG.connection_url))
    photo_id = target.photos[0].id

    average_rating = session.query(
        func.avg(Rate.rate)
    ).filter(
        Rate.photos.any(Photo.id == photo_id)
    ).scalar()

    if average_rating is None:
        average_rating = float(target.rate)

    session.query(
        Photo
    ).filter(
        Photo.id == photo_id
    ).update(
        {Photo.rate: round(average_rating, 2)}
    )
    session.commit()

