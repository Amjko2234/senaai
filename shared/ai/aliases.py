"""Type aliases for AI-related services.

Type Aliases:
    SysPrompt: Instruction for AI of role 'system'
    AsstPrompt: Instruction for AI of role 'assistant'
    UserPrompt: User's message to AI

    Temperature: Float value to adjust AI response from temperature
    Tokens: Int representation for AI API tokens

"""

from typing import NewType, TypeAlias

# Generation:
# Prompts
SysPrompt: TypeAlias = str
AsstPrompt: TypeAlias = str
UserPrompt: TypeAlias = str

# Behavior
Temperature: TypeAlias = float
Tokens: TypeAlias = int
