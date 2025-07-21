from openai import AsyncOpenAI


class OpenAIClient:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4.1-mini"

    async def ask(self, prompt: str) -> str | None:
        response = await self.client.chat.completions.create(
            model=self.model,
            max_tokens=50,
            messages=[
                {
                    "role": "system",
                    "content": "your name is AmjkoAI. You may be address as that--AI or also OpenAI",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    async def message(self, prompt: str) -> str | None:
        response = await self.client.chat.completions.create(
            model=self.model,
            max_tokens=100,
            messages=[
                {
                    "role": "system",
                    "content": "your name is AmjkoAI. You may be address as that--AI or also OpenAI",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content


_client: OpenAIClient | None = None


def init(api_key: str) -> None:
    global _client
    if _client is None:
        _client = OpenAIClient(api_key)

    return


def get_client() -> OpenAIClient:
    if _client is None:
        raise RuntimeError("OpenAI Client not initialized")
    return _client
