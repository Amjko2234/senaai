from openai import AsyncOpenAI


class OpenAIClient:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4.1-mini"

    async def ask(self, prompt: str) -> str | None:
        response = await self.client.chat.completions.create(
            model=self.model,
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content


client: OpenAIClient | None = None


def init(api_key: str):
    global client
    if client is None:
        client = OpenAIClient(api_key)
