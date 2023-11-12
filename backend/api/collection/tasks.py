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


def predict_requests_in_hour(df, target_hour):
    # Assuming 'df' is a DataFrame with 'created_at' and 'file_size' columns

    # Convert 'created_at' to hour of the day
    df['hour_of_day'] = df['created_at'].dt.hour

    # Aggregate data by hour and calculate total requests per hour
    hourly_data = df.groupby('hour_of_day').size().reset_index(name='requests')

    # Fit a polynomial regression model
    X = hourly_data['hour_of_day'].values.reshape(-1, 1)
    y = hourly_data['requests'].values

    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    # Predict for the target hour
    target_hour_poly = poly.transform([[target_hour]])
    predicted_requests = model.predict(target_hour_poly)

    return predicted_requests[0]
