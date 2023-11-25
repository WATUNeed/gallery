import asyncio
import math

import numpy as np
import pandas as pd
from datetime import datetime

from numpy.polynomial import Polynomial
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


# def predict_requests_in_hour(df: pd.DataFrame, target_hour: int):
#     # Data Preparation
#     # Count the frequency of records created in each hour
#     hour_counts = df['hour'].value_counts()
#
#     # Create a new DataFrame with row index and the frequency for the target hour
#     x = np.array(df.index).reshape(-1, 1)
#     y = np.array([hour_counts.get(hour, 0) if hour == target_hour else 0 for hour in df['hour']])
#
#     # Polynomial Features for Linear Regression
#     poly = PolynomialFeatures(degree=2)
#     x_poly = poly.fit_transform(x)
#
#     # Model Construction
#     model = LinearRegression()
#     model.fit(x_poly, y)
#
#     # Prediction
#     # Predict the frequency for each row index
#     y_pred = model.predict(x_poly)
#
#     # Find the row index with the highest predicted frequency for the target hour
#     max_index = np.argmax(y_pred)
#     print(df.iloc[max_index])
#     return df.iloc[max_index]

# def predict_requests_in_hour(df, target_hour):
#     # Extracting hour data and counting occurrences
#     hour_counts = df['hour'].value_counts().sort_index()
#     x = np.array(hour_counts.index).reshape(-1, 1)
#     y = np.array(hour_counts.values)
#
#     # Polynomial regression
#     poly = PolynomialFeatures(degree=2)
#     x_poly = poly.fit_transform(x)
#     poly_model = LinearRegression()
#     poly_model.fit(x_poly, y)
#
#     # Predicting for all hours and calculating distance from target hour
#     all_hours = np.arange(24).reshape(-1, 1)
#     all_hours_poly = poly.fit_transform(all_hours)
#     predictions = poly_model.predict(all_hours_poly)
#     distance_from_target = np.abs(all_hours - target_hour)
#
#     print(distance_from_target)
#     # Combining predictions and distances into a DataFrame
#     results_df = pd.DataFrame({
#         'hour': all_hours.flatten(),
#         'prediction': predictions,
#         'distance': distance_from_target.flatten()
#     })
#
#     # Sorting by prediction and distance
#     results_df.sort_values(by=['prediction', 'distance'], ascending=[False, True], inplace=True)
#
#     # Selecting top 5 records
#     top_records = results_df.head(10000000)
#
#     # Constructing the final DataFrame to return
#     final_df = pd.DataFrame()
#     for hour in top_records['hour']:
#         matched_rows = df[df['hour'] == hour]
#         final_df = pd.concat([final_df, matched_rows.head(1)])
#     print(final_df)
#     return final_df.reset_index(drop=True), results_df

def predict_requests_in_hour(df, target_hour):
    # Extracting hours and the count of each hour
    hour_counts = df['hour'].value_counts().sort_index()
    x = hour_counts.index.values.reshape(-1, 1)
    y = hour_counts.values

    # Polynomial features
    poly = PolynomialFeatures(degree=2)
    x_poly = poly.fit_transform(x)

    # Polynomial regression
    model = LinearRegression()
    model.fit(x_poly, y)

    # Predict for each hour
    hours = np.array(range(24)).reshape(-1, 1)
    hours_poly = poly.transform(hours)
    predictions = model.predict(hours_poly)

    # Creating a DataFrame with hours and predictions
    prediction_df = pd.DataFrame({'hour': hours.flatten(), 'predictions': predictions})

    # Calculating the distance from the target hour and sorting
    prediction_df['distance'] = abs(prediction_df['hour'] - target_hour)
    sorted_df = prediction_df.sort_values(by=['distance', 'predictions'], ascending=[True, False])

    # Getting the top 5 records
    top_hours = sorted_df.head(5)['hour'].values

    # Filtering the original DataFrame to get the top 5 records with collection_id
    result_df = df[df['hour'].isin(top_hours)].drop_duplicates(subset=['hour'])
    return result_df.sort_values(by='hour'), sorted_df
