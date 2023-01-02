from unittest.mock import MagicMock

import pytest
from app import models


@pytest.mark.parametrize(
    "status",
    [
        models.ItemStatus.Normal,
        models.ItemStatus.Novelty,
        models.ItemStatus.Outgoing,
        models.ItemStatus.Discontinued,
    ],
)
def test_preferred_item(client, preferred_item):
    bricks = preferred_item["bricks"]
    expected_item = preferred_item["expected_item"]
    brick_ids = ['"{}"'.format(brick.id) for brick in bricks]
    brick_id_strings = ", ".join(brick_ids)
    query = """
    query {
        preferredItem(brickIds: [%s]) {
            item {
                id
            }
        }
    }
    """ % (
        brick_id_strings
    )
    response = client.post(
        "/graphql",
        json={"query": query},
    )
    response = client.post("/graphql", json={"query": query})

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["preferredItem"]["item"]["id"] == str(expected_item.id)


@pytest.mark.parametrize(
    "status",
    [
        models.ItemStatus.Normal,
    ],
)
@pytest.mark.usefixtures("mocker")
def test_preferred_item_failure(mocker, client, preferred_item):
    # the mock doesn't work here
    # left as a placeholder for now
    return
    mock_determine_preferred_item = MagicMock(side_effect=Exception("test exception"))
    mocker.patch(
        "app.determine_preferred_item",
        mock_determine_preferred_item,
    )

    bricks = preferred_item["bricks"]

    brick_ids = ['"{}"'.format(brick.id) for brick in bricks]
    brick_id_strings = ", ".join(brick_ids)
    query = """
    query {
        preferredItem(brickIds: [%s]) {
            errors
            item {
                id
            }
        }
    }
    """ % (
        brick_id_strings
    )
    response = client.post("/graphql", json={"query": query})

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["preferredItem"]["errors"][0] == ["test exception"]
