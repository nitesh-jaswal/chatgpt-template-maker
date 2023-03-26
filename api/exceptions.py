import enum
class OpenAIErrorKind(str, enum.Enum):
    THROTTLE = "throttle"
    INTERNAL_ERROR = "internal_error"
    BAD_REQUEST = "bad_request"
    INCOMPLETE = "incomplete"
    EMPTY = "empty"
    OTHER = "other"

class OpenAIAPIException(Exception):
    
    def __init__(self, kind: OpenAIErrorKind, message: str = ""):
        self.kind = kind
        match kind:
            case OpenAIErrorKind.THROTTLE:
                message = ""
            case OpenAIErrorKind.INTERNAL_ERROR:
                message = ""
            case OpenAIErrorKind.BAD_REQUEST:
                message = ""
            case OpenAIErrorKind.INCOMPLETE:
                message = ""
            case OpenAIErrorKind.OTHER:
                message = ""
            case _:
                raise NotImplementedError(f"The {kind} error kind has not been implemented")
        super().__init__(message)

class OpenAIClientAuthException(Exception):
    ...

class BufferExceeded(Exception):
    pass
