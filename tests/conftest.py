import datetime as dt
import json
import os

import pytest

from data_subscriptions.models import (
    DatasetActivityList,
    NonsubscribableDataset,
    Subscription,
)
from data_subscriptions.app import create_app
from data_subscriptions.extensions import db as _db

os.environ["FLASK_ENV"] = "test"
os.environ["TIME_IN_SECONDS_BETWEEN_NOTIFICATION_DELIVERIES"] = "1800"


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def nonsubscribable_dataset():
    return NonsubscribableDataset(dataset_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")


@pytest.fixture
def dataset_activity_list():
    return DatasetActivityList(
        blob=[
            {
                "object_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "timestamp": "2020-02-01T00:00:00.000000",
            }
        ],
        collected_at=dt.datetime(2020, 2, 1),
        last_activity_created_at=dt.datetime(2020, 2, 1),
    )


@pytest.fixture
def subscription():
    return Subscription(
        dataset_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        user_id="00000000-0000-0000-0000-000000000000",
    )


@pytest.fixture
def subscription_list():
    return [
        {"dataset_id": "b72159fe-67d8-4ea7-8313-af2bf9210799", "user_id": "user1"},
        {"dataset_id": "b72159fe-67d8-4ea7-8313-af2bf92107100", "user_id": "user1"},
        {"dataset_id": "b72159fe-67d8-4ea7-8313-af2bf92107101", "user_id": "user2"},
        {"dataset_id": "b72159fe-67d8-4ea7-8313-af2bf92107102", "user_id": "user2"},
    ]

@pytest.fixture
def all_subscription(db, subscription_list):
    for x in [Subscription(**x) for x in subscription_list]: 
        db.session.add(x)
    db.session.commit()
    
    return subscription_list
    