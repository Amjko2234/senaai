from dataclasses import dataclass

from ....shared.types.ai import *


@dataclass
class Prompt:
    """Represents a user prompt for AI response generation"""

    user_id: UserID = Field()
