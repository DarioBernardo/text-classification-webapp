from json import JSONDecodeError
from openai import OpenAI
import json

from logger_config import setup_logger

logger = setup_logger(__name__)


class OpenAILanguageModel:

    def __init__(self, model_name: str, prompts_dir: str = "."):
        self.model_name = model_name
        self.client = OpenAI(
            # Defaults to os.environ.get("OPENAI_API_KEY")
            )

        with open(f"{prompts_dir}/prompt_single_class.txt", "r") as file:
            self.prompt_single_class = file.read()

        with open(f"{prompts_dir}/prompt_multiclass.txt", "r") as file:
            self.prompt_multi_class = file.read()


    def classify_text(self, text: str, options: dict, classes: list, temperature: float = 0.0):
        """
        Classify the text using the OpenAI API
        :param text: The text to classify
        :param options: The options for the classification
        :param classes: The classes to classify the text into
        :param temperature: The temperature parameter for the model
        :return: The classification result
        """

        logger.debug(f"Options: {options}")

        reasoning = options.get("reasoning", True)

        # Organise the classes for the prompt
        classes_string = []
        for c in classes:
            classes_string.append(f"'{c['class_name']}': '{c['class_description']}'. Class ID: '{c['class_id']}'")

        classes_string = "\n".join(classes_string)

        # Create the system prompt
        if options.get("multilabel", False):
            system_prompt = self.prompt_multi_class.format(classes=classes_string)
        else:
            system_prompt = self.prompt_single_class.format(classes=classes_string)

        logger.debug("=" * 10)
        logger.debug(system_prompt)
        logger.debug("-" * 10)
        logger.debug(text)
        logger.debug("=" * 10)

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": text
            }
        ]

        max_number_of_attempts = 3
        while max_number_of_attempts > 0:
            try:
                response = self.client.chat.completions.create(
                    model = self.model_name,
                    temperature = temperature,
                    response_format = {"type": "json_object"},
                    messages = messages
                )

                return extract_response(response)

                # return {'reasoning': 'The text mentions a request for a scoop of vanilla and a scoop of chocolate, indicating a desire for ice cream flavors made with real ingredients. Vanilla ice cream is made with real Madagascan vanilla, and chocolate ice cream is made with real chocolate.', 'result': ['V1']}
            except JSONDecodeError as e:
                print(f"Error decoding the response: {e}, number of attempts left: {max_number_of_attempts}")
                max_number_of_attempts -= 1
                if max_number_of_attempts == 0:
                    raise e

def extract_response(response):
    return json.loads(response.choices[0].message.content)