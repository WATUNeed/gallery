import asyncio
import math

import pandas as pd
from datetime import datetime

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from backend.api.base_classes.models import Session
from backend.api.collection.models import CollectionDownloadQueryHistory
from backend.task_scheduler import celery_app


async def get_history():
    async with Session() as session:
        async with session.begin():
            return await CollectionDownloadQueryHistory.get_history(session)


@celery_app.task
def task_make_magic():
    print('work')
    df = pd.DataFrame([item.to_dict() for item in asyncio.run(get_history())])
    print(df.iloc[[math.floor(predict_requests_in_hour(df, datetime.now().hour))]]["collection_id"])


def predict_requests_in_hour(df: pd.DataFrame, target_hour: int):
    return <predict df row for this hour>
