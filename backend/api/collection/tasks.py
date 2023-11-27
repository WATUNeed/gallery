import asyncio
import os
import shutil
from pathlib import Path
from uuid import UUID

import pandas as pd
from datetime import datetime, timedelta

import plotly.express as px
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from backend.api.base_classes.models import Session
from backend.api.collection.models import CollectionDownloadQueryHistory, Collection
from backend.cache.redis_ import RedisContextManager
from backend.config.backend import BACKEND_CONFIG
from backend.task_scheduler import celery_app


async def get_history():
    async with Session() as session:
        async with session.begin():
            return await CollectionDownloadQueryHistory.get_history(session)


async def cached_predicted_calls(collection_id: UUID):
    async with Session() as session:
        async with session.begin():
            collection = await session.get(Collection, collection_id)
            images = await Collection.get_image(session, collection_id)

            if not Path(BACKEND_CONFIG.collection_path).is_dir():
                os.mkdir(BACKEND_CONFIG.collection_path)

            main_dir = f'{BACKEND_CONFIG.collection_path}{collection_id}'

            if not Path(main_dir).is_dir():
                os.mkdir(main_dir)
                os.mkdir(f'{main_dir}/images/')
            else:
                shutil.rmtree(f'{main_dir}/images/')
                os.mkdir(f'{main_dir}/images/')

            for image in images:
                image_name = image.name.replace(' ', '_')
                with open(f'{main_dir}/images/{image_name}.png', mode='wb') as file:
                    file.write(image.file)

            collection_name = collection.name.replace(' ', '_')
            shutil.make_archive(f'{main_dir}/{collection_name}', 'zip', f'{main_dir}/images')
            async with RedisContextManager() as redis:
                await redis.set_item(str(collection_id), '', timedelta(hours=1))


@celery_app.task
def task_predict_collections():
    df = pd.DataFrame(
        [
            {
                'name': item.collection.name,
                'collection_id': item.collection_id,
                'file_size': item.file_size,
                'sender_id': item.sender_id,
                'hour': item.created_at.hour,
            }
            for item in asyncio.run(get_history())
        ]
    )
    target_hour = datetime.utcnow().hour
    df = prepare_calls_history_df(df, target_hour)
    df, normalized_weights = calculate_parameters_weights(df)

    result = []
    for index in range(10):
        result.append(df['collection_id'].iloc[index])
        asyncio.run(cached_predicted_calls(df['collection_id'].iloc[index]))
    return result


def normalize_distance(distance):
    return 1 - min(max(distance, 0), 1)


def prepare_calls_history_df(df: DataFrame, target_hour: int) -> DataFrame:
    df['hour_repeats'] = df.groupby('collection_id')['hour'].transform('count')
    df['proximity_to_target_hour'] = df['hour'].apply(lambda hour: normalize_distance(abs(target_hour - hour) / 23))
    df['file_size'] = abs(df['file_size'] / df['file_size'].max())
    df['senders_count'] = df.groupby('collection_id')['sender_id'].transform('nunique')
    df['priority'] = (df['hour_repeats'] + df['file_size'] + df['senders_count'] + df['proximity_to_target_hour'])
    return df


def calculate_parameters_weights(df: DataFrame):
    x = df[['proximity_to_target_hour', 'file_size', 'hour_repeats', 'senders_count']]
    y = df['priority']

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    model = LinearRegression()
    model.fit(x_scaled, y)

    weights = model.coef_

    normalized_weights = {name: weight for name, weight in zip(x.columns, weights / weights.sum())}

    df['priority'] = (sum(weight * df[param] for param, weight in normalized_weights.items()))

    df = df.sort_values(by='priority', ascending=False)

    return df, normalized_weights


def save_fig_to_html(df: DataFrame):
    for param in ['name', 'file_size', 'hour_repeats', 'senders_count', 'proximity_to_target_hour']:
        df = df.sort_values(by='priority', ascending=False)
        fig = px.scatter(df, x=param, y='priority')
        fig.write_html(f"/src/frontend/{param}.html")
