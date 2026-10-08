import time

from google import genai
from google.genai import types

from app.core.config import settings


class GeminiClient:
    """
    Client wrapper for Google's Gemini API.

    This class keeps Gemini-specific API logic in one place
    so the rest of the application can simply call generate().
    """

    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Add it to the project .env file."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL

    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
        max_output_tokens: int = 2048,
        max_retries: int = 3,
    ) -> str:
        """
        Generate a response from Gemini.

        Retries temporary server errors such as HTTP 503.
        """

        last_error = None

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_output_tokens,
                    ),
                )

                result = response.text

                if not result:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return result.strip()

            except Exception as error:
                last_error = error

                # Retry temporary API/server failures.
                if "503" in str(error) or "UNAVAILABLE" in str(error):
                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    raise

        raise RuntimeError(
            "Gemini request failed after multiple retries."
        ) from last_error


gemini_client = GeminiClient()