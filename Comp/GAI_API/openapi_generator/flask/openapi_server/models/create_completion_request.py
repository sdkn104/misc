from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server.models.chat_completion_stream_options import ChatCompletionStreamOptions
from openapi_server.models.create_completion_request_model import CreateCompletionRequestModel
from openapi_server.models.create_completion_request_prompt import CreateCompletionRequestPrompt
from openapi_server.models.stop_configuration import StopConfiguration
from openapi_server import util

from openapi_server.models.chat_completion_stream_options import ChatCompletionStreamOptions  # noqa: E501
from openapi_server.models.create_completion_request_model import CreateCompletionRequestModel  # noqa: E501
from openapi_server.models.create_completion_request_prompt import CreateCompletionRequestPrompt  # noqa: E501
from openapi_server.models.stop_configuration import StopConfiguration  # noqa: E501

class CreateCompletionRequest(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, model=None, prompt=None, best_of=1, echo=False, frequency_penalty=0, logit_bias=None, logprobs=None, max_tokens=16, n=1, presence_penalty=0, seed=None, stop=None, stream=False, stream_options=None, suffix=None, temperature=1, top_p=1, user=None):  # noqa: E501
        """CreateCompletionRequest - a model defined in OpenAPI

        :param model: The model of this CreateCompletionRequest.  # noqa: E501
        :type model: CreateCompletionRequestModel
        :param prompt: The prompt of this CreateCompletionRequest.  # noqa: E501
        :type prompt: CreateCompletionRequestPrompt
        :param best_of: The best_of of this CreateCompletionRequest.  # noqa: E501
        :type best_of: int
        :param echo: The echo of this CreateCompletionRequest.  # noqa: E501
        :type echo: bool
        :param frequency_penalty: The frequency_penalty of this CreateCompletionRequest.  # noqa: E501
        :type frequency_penalty: float
        :param logit_bias: The logit_bias of this CreateCompletionRequest.  # noqa: E501
        :type logit_bias: Dict[str, int]
        :param logprobs: The logprobs of this CreateCompletionRequest.  # noqa: E501
        :type logprobs: int
        :param max_tokens: The max_tokens of this CreateCompletionRequest.  # noqa: E501
        :type max_tokens: int
        :param n: The n of this CreateCompletionRequest.  # noqa: E501
        :type n: int
        :param presence_penalty: The presence_penalty of this CreateCompletionRequest.  # noqa: E501
        :type presence_penalty: float
        :param seed: The seed of this CreateCompletionRequest.  # noqa: E501
        :type seed: int
        :param stop: The stop of this CreateCompletionRequest.  # noqa: E501
        :type stop: StopConfiguration
        :param stream: The stream of this CreateCompletionRequest.  # noqa: E501
        :type stream: bool
        :param stream_options: The stream_options of this CreateCompletionRequest.  # noqa: E501
        :type stream_options: ChatCompletionStreamOptions
        :param suffix: The suffix of this CreateCompletionRequest.  # noqa: E501
        :type suffix: str
        :param temperature: The temperature of this CreateCompletionRequest.  # noqa: E501
        :type temperature: float
        :param top_p: The top_p of this CreateCompletionRequest.  # noqa: E501
        :type top_p: float
        :param user: The user of this CreateCompletionRequest.  # noqa: E501
        :type user: str
        """
        self.openapi_types = {
            'model': CreateCompletionRequestModel,
            'prompt': CreateCompletionRequestPrompt,
            'best_of': int,
            'echo': bool,
            'frequency_penalty': float,
            'logit_bias': Dict[str, int],
            'logprobs': int,
            'max_tokens': int,
            'n': int,
            'presence_penalty': float,
            'seed': int,
            'stop': StopConfiguration,
            'stream': bool,
            'stream_options': ChatCompletionStreamOptions,
            'suffix': str,
            'temperature': float,
            'top_p': float,
            'user': str
        }

        self.attribute_map = {
            'model': 'model',
            'prompt': 'prompt',
            'best_of': 'best_of',
            'echo': 'echo',
            'frequency_penalty': 'frequency_penalty',
            'logit_bias': 'logit_bias',
            'logprobs': 'logprobs',
            'max_tokens': 'max_tokens',
            'n': 'n',
            'presence_penalty': 'presence_penalty',
            'seed': 'seed',
            'stop': 'stop',
            'stream': 'stream',
            'stream_options': 'stream_options',
            'suffix': 'suffix',
            'temperature': 'temperature',
            'top_p': 'top_p',
            'user': 'user'
        }

        self._model = model
        self._prompt = prompt
        self._best_of = best_of
        self._echo = echo
        self._frequency_penalty = frequency_penalty
        self._logit_bias = logit_bias
        self._logprobs = logprobs
        self._max_tokens = max_tokens
        self._n = n
        self._presence_penalty = presence_penalty
        self._seed = seed
        self._stop = stop
        self._stream = stream
        self._stream_options = stream_options
        self._suffix = suffix
        self._temperature = temperature
        self._top_p = top_p
        self._user = user

    @classmethod
    def from_dict(cls, dikt) -> 'CreateCompletionRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CreateCompletionRequest of this CreateCompletionRequest.  # noqa: E501
        :rtype: CreateCompletionRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def model(self) -> CreateCompletionRequestModel:
        """Gets the model of this CreateCompletionRequest.


        :return: The model of this CreateCompletionRequest.
        :rtype: CreateCompletionRequestModel
        """
        return self._model

    @model.setter
    def model(self, model: CreateCompletionRequestModel):
        """Sets the model of this CreateCompletionRequest.


        :param model: The model of this CreateCompletionRequest.
        :type model: CreateCompletionRequestModel
        """
        if model is None:
            raise ValueError("Invalid value for `model`, must not be `None`")  # noqa: E501

        self._model = model

    @property
    def prompt(self) -> CreateCompletionRequestPrompt:
        """Gets the prompt of this CreateCompletionRequest.


        :return: The prompt of this CreateCompletionRequest.
        :rtype: CreateCompletionRequestPrompt
        """
        return self._prompt

    @prompt.setter
    def prompt(self, prompt: CreateCompletionRequestPrompt):
        """Sets the prompt of this CreateCompletionRequest.


        :param prompt: The prompt of this CreateCompletionRequest.
        :type prompt: CreateCompletionRequestPrompt
        """
        if prompt is None:
            raise ValueError("Invalid value for `prompt`, must not be `None`")  # noqa: E501

        self._prompt = prompt

    @property
    def best_of(self) -> int:
        """Gets the best_of of this CreateCompletionRequest.

        Generates `best_of` completions server-side and returns the \"best\" (the one with the highest log probability per token). Results cannot be streamed.  When used with `n`, `best_of` controls the number of candidate completions and `n` specifies how many to return – `best_of` must be greater than `n`.  **Note:** Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for `max_tokens` and `stop`.   # noqa: E501

        :return: The best_of of this CreateCompletionRequest.
        :rtype: int
        """
        return self._best_of

    @best_of.setter
    def best_of(self, best_of: int):
        """Sets the best_of of this CreateCompletionRequest.

        Generates `best_of` completions server-side and returns the \"best\" (the one with the highest log probability per token). Results cannot be streamed.  When used with `n`, `best_of` controls the number of candidate completions and `n` specifies how many to return – `best_of` must be greater than `n`.  **Note:** Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for `max_tokens` and `stop`.   # noqa: E501

        :param best_of: The best_of of this CreateCompletionRequest.
        :type best_of: int
        """
        if best_of is not None and best_of > 20:  # noqa: E501
            raise ValueError("Invalid value for `best_of`, must be a value less than or equal to `20`")  # noqa: E501
        if best_of is not None and best_of < 0:  # noqa: E501
            raise ValueError("Invalid value for `best_of`, must be a value greater than or equal to `0`")  # noqa: E501

        self._best_of = best_of

    @property
    def echo(self) -> bool:
        """Gets the echo of this CreateCompletionRequest.

        Echo back the prompt in addition to the completion   # noqa: E501

        :return: The echo of this CreateCompletionRequest.
        :rtype: bool
        """
        return self._echo

    @echo.setter
    def echo(self, echo: bool):
        """Sets the echo of this CreateCompletionRequest.

        Echo back the prompt in addition to the completion   # noqa: E501

        :param echo: The echo of this CreateCompletionRequest.
        :type echo: bool
        """

        self._echo = echo

    @property
    def frequency_penalty(self) -> float:
        """Gets the frequency_penalty of this CreateCompletionRequest.

        Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.  [See more information about frequency and presence penalties.](/docs/guides/text-generation)   # noqa: E501

        :return: The frequency_penalty of this CreateCompletionRequest.
        :rtype: float
        """
        return self._frequency_penalty

    @frequency_penalty.setter
    def frequency_penalty(self, frequency_penalty: float):
        """Sets the frequency_penalty of this CreateCompletionRequest.

        Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.  [See more information about frequency and presence penalties.](/docs/guides/text-generation)   # noqa: E501

        :param frequency_penalty: The frequency_penalty of this CreateCompletionRequest.
        :type frequency_penalty: float
        """
        if frequency_penalty is not None and frequency_penalty > 2:  # noqa: E501
            raise ValueError("Invalid value for `frequency_penalty`, must be a value less than or equal to `2`")  # noqa: E501
        if frequency_penalty is not None and frequency_penalty < -2:  # noqa: E501
            raise ValueError("Invalid value for `frequency_penalty`, must be a value greater than or equal to `-2`")  # noqa: E501

        self._frequency_penalty = frequency_penalty

    @property
    def logit_bias(self) -> Dict[str, int]:
        """Gets the logit_bias of this CreateCompletionRequest.

        Modify the likelihood of specified tokens appearing in the completion.  Accepts a JSON object that maps tokens (specified by their token ID in the GPT tokenizer) to an associated bias value from -100 to 100. You can use this [tokenizer tool](/tokenizer?view=bpe) to convert text to token IDs. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.  As an example, you can pass `{\"50256\": -100}` to prevent the <|endoftext|> token from being generated.   # noqa: E501

        :return: The logit_bias of this CreateCompletionRequest.
        :rtype: Dict[str, int]
        """
        return self._logit_bias

    @logit_bias.setter
    def logit_bias(self, logit_bias: Dict[str, int]):
        """Sets the logit_bias of this CreateCompletionRequest.

        Modify the likelihood of specified tokens appearing in the completion.  Accepts a JSON object that maps tokens (specified by their token ID in the GPT tokenizer) to an associated bias value from -100 to 100. You can use this [tokenizer tool](/tokenizer?view=bpe) to convert text to token IDs. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.  As an example, you can pass `{\"50256\": -100}` to prevent the <|endoftext|> token from being generated.   # noqa: E501

        :param logit_bias: The logit_bias of this CreateCompletionRequest.
        :type logit_bias: Dict[str, int]
        """

        self._logit_bias = logit_bias

    @property
    def logprobs(self) -> int:
        """Gets the logprobs of this CreateCompletionRequest.

        Include the log probabilities on the `logprobs` most likely output tokens, as well the chosen tokens. For example, if `logprobs` is 5, the API will return a list of the 5 most likely tokens. The API will always return the `logprob` of the sampled token, so there may be up to `logprobs+1` elements in the response.  The maximum value for `logprobs` is 5.   # noqa: E501

        :return: The logprobs of this CreateCompletionRequest.
        :rtype: int
        """
        return self._logprobs

    @logprobs.setter
    def logprobs(self, logprobs: int):
        """Sets the logprobs of this CreateCompletionRequest.

        Include the log probabilities on the `logprobs` most likely output tokens, as well the chosen tokens. For example, if `logprobs` is 5, the API will return a list of the 5 most likely tokens. The API will always return the `logprob` of the sampled token, so there may be up to `logprobs+1` elements in the response.  The maximum value for `logprobs` is 5.   # noqa: E501

        :param logprobs: The logprobs of this CreateCompletionRequest.
        :type logprobs: int
        """
        if logprobs is not None and logprobs > 5:  # noqa: E501
            raise ValueError("Invalid value for `logprobs`, must be a value less than or equal to `5`")  # noqa: E501
        if logprobs is not None and logprobs < 0:  # noqa: E501
            raise ValueError("Invalid value for `logprobs`, must be a value greater than or equal to `0`")  # noqa: E501

        self._logprobs = logprobs

    @property
    def max_tokens(self) -> int:
        """Gets the max_tokens of this CreateCompletionRequest.

        The maximum number of [tokens](/tokenizer) that can be generated in the completion.  The token count of your prompt plus `max_tokens` cannot exceed the model's context length. [Example Python code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken) for counting tokens.   # noqa: E501

        :return: The max_tokens of this CreateCompletionRequest.
        :rtype: int
        """
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, max_tokens: int):
        """Sets the max_tokens of this CreateCompletionRequest.

        The maximum number of [tokens](/tokenizer) that can be generated in the completion.  The token count of your prompt plus `max_tokens` cannot exceed the model's context length. [Example Python code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken) for counting tokens.   # noqa: E501

        :param max_tokens: The max_tokens of this CreateCompletionRequest.
        :type max_tokens: int
        """
        if max_tokens is not None and max_tokens < 0:  # noqa: E501
            raise ValueError("Invalid value for `max_tokens`, must be a value greater than or equal to `0`")  # noqa: E501

        self._max_tokens = max_tokens

    @property
    def n(self) -> int:
        """Gets the n of this CreateCompletionRequest.

        How many completions to generate for each prompt.  **Note:** Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for `max_tokens` and `stop`.   # noqa: E501

        :return: The n of this CreateCompletionRequest.
        :rtype: int
        """
        return self._n

    @n.setter
    def n(self, n: int):
        """Sets the n of this CreateCompletionRequest.

        How many completions to generate for each prompt.  **Note:** Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for `max_tokens` and `stop`.   # noqa: E501

        :param n: The n of this CreateCompletionRequest.
        :type n: int
        """
        if n is not None and n > 128:  # noqa: E501
            raise ValueError("Invalid value for `n`, must be a value less than or equal to `128`")  # noqa: E501
        if n is not None and n < 1:  # noqa: E501
            raise ValueError("Invalid value for `n`, must be a value greater than or equal to `1`")  # noqa: E501

        self._n = n

    @property
    def presence_penalty(self) -> float:
        """Gets the presence_penalty of this CreateCompletionRequest.

        Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.  [See more information about frequency and presence penalties.](/docs/guides/text-generation)   # noqa: E501

        :return: The presence_penalty of this CreateCompletionRequest.
        :rtype: float
        """
        return self._presence_penalty

    @presence_penalty.setter
    def presence_penalty(self, presence_penalty: float):
        """Sets the presence_penalty of this CreateCompletionRequest.

        Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.  [See more information about frequency and presence penalties.](/docs/guides/text-generation)   # noqa: E501

        :param presence_penalty: The presence_penalty of this CreateCompletionRequest.
        :type presence_penalty: float
        """
        if presence_penalty is not None and presence_penalty > 2:  # noqa: E501
            raise ValueError("Invalid value for `presence_penalty`, must be a value less than or equal to `2`")  # noqa: E501
        if presence_penalty is not None and presence_penalty < -2:  # noqa: E501
            raise ValueError("Invalid value for `presence_penalty`, must be a value greater than or equal to `-2`")  # noqa: E501

        self._presence_penalty = presence_penalty

    @property
    def seed(self) -> int:
        """Gets the seed of this CreateCompletionRequest.

        If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.  Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend.   # noqa: E501

        :return: The seed of this CreateCompletionRequest.
        :rtype: int
        """
        return self._seed

    @seed.setter
    def seed(self, seed: int):
        """Sets the seed of this CreateCompletionRequest.

        If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.  Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend.   # noqa: E501

        :param seed: The seed of this CreateCompletionRequest.
        :type seed: int
        """

        self._seed = seed

    @property
    def stop(self) -> StopConfiguration:
        """Gets the stop of this CreateCompletionRequest.


        :return: The stop of this CreateCompletionRequest.
        :rtype: StopConfiguration
        """
        return self._stop

    @stop.setter
    def stop(self, stop: StopConfiguration):
        """Sets the stop of this CreateCompletionRequest.


        :param stop: The stop of this CreateCompletionRequest.
        :type stop: StopConfiguration
        """

        self._stop = stop

    @property
    def stream(self) -> bool:
        """Gets the stream of this CreateCompletionRequest.

        Whether to stream back partial progress. If set, tokens will be sent as data-only [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format) as they become available, with the stream terminated by a `data: [DONE]` message. [Example Python code](https://cookbook.openai.com/examples/how_to_stream_completions).   # noqa: E501

        :return: The stream of this CreateCompletionRequest.
        :rtype: bool
        """
        return self._stream

    @stream.setter
    def stream(self, stream: bool):
        """Sets the stream of this CreateCompletionRequest.

        Whether to stream back partial progress. If set, tokens will be sent as data-only [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format) as they become available, with the stream terminated by a `data: [DONE]` message. [Example Python code](https://cookbook.openai.com/examples/how_to_stream_completions).   # noqa: E501

        :param stream: The stream of this CreateCompletionRequest.
        :type stream: bool
        """

        self._stream = stream

    @property
    def stream_options(self) -> ChatCompletionStreamOptions:
        """Gets the stream_options of this CreateCompletionRequest.


        :return: The stream_options of this CreateCompletionRequest.
        :rtype: ChatCompletionStreamOptions
        """
        return self._stream_options

    @stream_options.setter
    def stream_options(self, stream_options: ChatCompletionStreamOptions):
        """Sets the stream_options of this CreateCompletionRequest.


        :param stream_options: The stream_options of this CreateCompletionRequest.
        :type stream_options: ChatCompletionStreamOptions
        """

        self._stream_options = stream_options

    @property
    def suffix(self) -> str:
        """Gets the suffix of this CreateCompletionRequest.

        The suffix that comes after a completion of inserted text.  This parameter is only supported for `gpt-3.5-turbo-instruct`.   # noqa: E501

        :return: The suffix of this CreateCompletionRequest.
        :rtype: str
        """
        return self._suffix

    @suffix.setter
    def suffix(self, suffix: str):
        """Sets the suffix of this CreateCompletionRequest.

        The suffix that comes after a completion of inserted text.  This parameter is only supported for `gpt-3.5-turbo-instruct`.   # noqa: E501

        :param suffix: The suffix of this CreateCompletionRequest.
        :type suffix: str
        """

        self._suffix = suffix

    @property
    def temperature(self) -> float:
        """Gets the temperature of this CreateCompletionRequest.

        What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.  We generally recommend altering this or `top_p` but not both.   # noqa: E501

        :return: The temperature of this CreateCompletionRequest.
        :rtype: float
        """
        return self._temperature

    @temperature.setter
    def temperature(self, temperature: float):
        """Sets the temperature of this CreateCompletionRequest.

        What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.  We generally recommend altering this or `top_p` but not both.   # noqa: E501

        :param temperature: The temperature of this CreateCompletionRequest.
        :type temperature: float
        """
        if temperature is not None and temperature > 2:  # noqa: E501
            raise ValueError("Invalid value for `temperature`, must be a value less than or equal to `2`")  # noqa: E501
        if temperature is not None and temperature < 0:  # noqa: E501
            raise ValueError("Invalid value for `temperature`, must be a value greater than or equal to `0`")  # noqa: E501

        self._temperature = temperature

    @property
    def top_p(self) -> float:
        """Gets the top_p of this CreateCompletionRequest.

        An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.  We generally recommend altering this or `temperature` but not both.   # noqa: E501

        :return: The top_p of this CreateCompletionRequest.
        :rtype: float
        """
        return self._top_p

    @top_p.setter
    def top_p(self, top_p: float):
        """Sets the top_p of this CreateCompletionRequest.

        An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.  We generally recommend altering this or `temperature` but not both.   # noqa: E501

        :param top_p: The top_p of this CreateCompletionRequest.
        :type top_p: float
        """
        if top_p is not None and top_p > 1:  # noqa: E501
            raise ValueError("Invalid value for `top_p`, must be a value less than or equal to `1`")  # noqa: E501
        if top_p is not None and top_p < 0:  # noqa: E501
            raise ValueError("Invalid value for `top_p`, must be a value greater than or equal to `0`")  # noqa: E501

        self._top_p = top_p

    @property
    def user(self) -> str:
        """Gets the user of this CreateCompletionRequest.

        A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. [Learn more](/docs/guides/safety-best-practices#end-user-ids).   # noqa: E501

        :return: The user of this CreateCompletionRequest.
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, user: str):
        """Sets the user of this CreateCompletionRequest.

        A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. [Learn more](/docs/guides/safety-best-practices#end-user-ids).   # noqa: E501

        :param user: The user of this CreateCompletionRequest.
        :type user: str
        """

        self._user = user
