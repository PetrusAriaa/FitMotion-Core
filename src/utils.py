from http.client import HTTPException
from uuid import UUID


def validate_uuid(string_uuid: str):
    try:
        _uuid = UUID(string_uuid)
        return _uuid, None
    except:
        return None, HTTPException("Invalid id")