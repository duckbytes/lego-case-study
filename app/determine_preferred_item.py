from app import models


def determine_preferred_item(bricks):
    """Determine the preferred item for a set of bricks.
    Filter for items by ItemStatus first.
    Then filter the result to find the item with the lowest price.

    Args:
        bricks (list): A list of Brick objects.

    Returns:
        Item: The preferred item for the set of bricks.
    """

    # Get all items for the bricks
    items = []
    for brick in bricks:
        items.extend(brick.items)

    items = [item for item in items if item.master_data and item.master_data.status]
    items_to_filter = []
    item_status = [item.master_data.status for item in items if item.master_data]
    if models.ItemStatus.Normal in item_status:
        items_to_filter = [
            item
            for item in items
            if item.master_data.status == models.ItemStatus.Normal
        ]
    elif models.ItemStatus.Novelty in item_status:
        items_to_filter = [
            item
            for item in items
            if item.master_data.status == models.ItemStatus.Novelty
        ]
    elif models.ItemStatus.Outgoing in item_status:
        items_to_filter = [
            item
            for item in items
            if item.master_data.status == models.ItemStatus.Outgoing
        ]
    elif models.ItemStatus.Discontinued in item_status:
        items_to_filter = [
            item
            for item in items
            if item.master_data.status == models.ItemStatus.Discontinued
        ]

    # no items
    if len(items_to_filter) == 0:
        return None
    # If there is only one item, it is the preferred item
    if len(items_to_filter) == 1:
        return items_to_filter[0]
    # If there are multiple items, determine the preferred item
    # based on the lowest price
    elif len(items_to_filter) > 1:
        return min(items_to_filter, key=lambda item: item.master_data.price)
