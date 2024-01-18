from enum import Enum


class Topic(str, Enum):
    LOCK_STATUS = "NCSYS003_LOCK_STATUS",
    DOOR_STATUS = "NCSYS003_DOOR_STATUS",
    SEND_OTP = "NCSYS003_SEND_OTP",
    NODE_STATE = "NCSYS003_NODE_STATE",


    def __str__(self) -> str:
        return self.value
