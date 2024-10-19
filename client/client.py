import os, dotenv, numpy as np # Standard Python Imports
from openai import OpenAI

from client.config import * # # Configurations

class OpenAPI:
    """
    The universal OpenAI client, allowing users to interface with the OpenAI API.
    """

    def __init__(self: any, model: str = EMBEDDING_MODEL) -> 'OpenAPI':
        """
        Initializes an OpenAPI instance for interfacing with the OpenAI API.

        @return: An OpenAPI instance with fields set as specified.
        """
        dotenv.load_dotenv()
        self.key: str      = os.getenv('OPENAI_KEY')
        self.api: 'OpenAI' = OpenAI(api_key=self.key)
        self.model: str    = model

    def embedding(self: any, text: str) -> np.ndarray:
        """
        Returns the vector embedding of the given text.

        @param text: A string representing the text to embed.
        @return: A vector of floats representing the embedding of the text.
        """
        result: dict[any] = self.api.embeddings.create(model=self.model, input=text)
        # if (DEBUG): print(f'API Usage: {result.usage}')
        return np.array(result.data[0].embedding)

    def similarity(self: any, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Returns the cosine similarity between the two given vector embeddings.

        @param vec1: A vector of floats representing the first embedding.
        @param vec2: A vector of floats representing the second embedding.
        @return: A float representing the similarity between the two embeddings.
        """
        num: float = np.dot(vec1, vec2)
        den: float = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        return num / den

    def categorize(self: any, text: str, labels: list[str]) -> str:
        """
        Returns the label of the given text based on the provided labels.

        @param text: A string representing the text to categorize.
        @param labels: A list of strings representing the possible labels.
        @return: A string representing the best label of the text.
        """
        temb: np.ndarray   = self.embedding(text)
        lemb: np.ndarray   = [self.embedding(label) for label in labels]
        scores: np.ndarray = np.array([self.similarity(temb, label) for label in lemb])
        return labels[np.argmax(scores)], np.max(scores)
