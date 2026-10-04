def favorite_document_to_response(document: dict):
    return {
        "id": str(document["_id"]),
        "user_id": document["user_id"],
        "name": document["name"],
        "created_at": document["created_at"],
    }


def favorite_item_document_to_response(document: dict):
    return {
        "id": str(document["_id"]),
        "favorite_id": str(document["favorite_id"]),
        "content_id": str(document["content_id"]),
        "status": document["status"],
        "created_at": document["created_at"],
    }