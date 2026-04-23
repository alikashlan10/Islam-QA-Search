from enum import Enum

class RerankerProvider(str, Enum):
    
    COHERE = "cohere"
    NONE   = "none"      # passthrough — returns chunks as-is
