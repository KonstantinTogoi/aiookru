from enum import Enum


class SignatureCircuit(Enum):
    """Signature circuit."""
    UNDEFINED = 0
    CLIENT_SERVER = 1
    SERVER_SERVER = 2
