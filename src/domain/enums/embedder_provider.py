from enum import Enum

class EmbedderProvider(str, Enum):
    
    COHERE      = "cohere"
    