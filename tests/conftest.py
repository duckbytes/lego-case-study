import pytest
import random
from app import app, models, db


@pytest.fixture(scope="session")
def client():
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="function")
def preferred_item(status):
    bricks = []
    items = []
    master_datas = []
    for i in range(0, 10):
        brick = models.Brick(
            design_id=1, color_ids=[random.randint(0, 100) for n in range(0, 10)]
        )
        db.session.add(brick)
        if status == models.ItemStatus.Normal:
            stat = random.choice(list(models.ItemStatus))
        elif status == models.ItemStatus.Novelty:
            stat = random.choice(
                [
                    models.ItemStatus.Novelty,
                    models.ItemStatus.Discontinued,
                    models.ItemStatus.Outgoing,
                ]
            )
        elif status == models.ItemStatus.Outgoing:
            stat = random.choice(
                [models.ItemStatus.Outgoing, models.ItemStatus.Discontinued]
            )
        else:
            stat = models.ItemStatus.Discontinued
        master_data = models.MasterData(price=i + 2, status=stat)
        item = models.Item(bricks=[brick], master_data=master_data)
        bricks.append(brick)
        items.append(item)
        master_datas.append(master_data)

    master_data = models.MasterData(price=1, status=status)
    master_datas.append(master_data)
    item = models.Item(bricks=bricks[0:2], master_data=master_data)
    items.append(item)
    db.session.add(item)
    db.session.add(master_data)
    db.session.commit()
    yield {"bricks": bricks, "expected_item": item}
    for brick in bricks:
        db.session.delete(brick)
    for item in items:
        db.session.delete(item)
    for master_data in master_datas:
        db.session.delete(master_data)
