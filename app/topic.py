from enum import Enum


class Topic(str, Enum):
    LOCK_STATUS = "NCSYS003_LOCK_STATUS",
    DOOR_STATUS = "NCSYS003_DOOR_STATUS",
    SET_LOCK_CODE = "NCSYS003_SET_LOCK_CODE",
    NODE_STATE = "NCSYS003_NODE_STATE",


    def __str__(self) -> str:
        return self.value
