from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server.models.completion_usage_completion_tokens_details import CompletionUsageCompletionTokensDetails
from openapi_server.models.completion_usage_prompt_tokens_details import CompletionUsagePromptTokensDetails
from openapi_server import util

from openapi_server.models.completion_usage_completion_tokens_details import CompletionUsageCompletionTokensDetails  # noqa: E501
from openapi_server.models.completion_usage_prompt_tokens_details import CompletionUsagePromptTokensDetails  # noqa: E501

class CompletionUsage(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, completion_tokens=0, prompt_tokens=0, total_tokens=0, completion_tokens_details=None, prompt_tokens_details=None):  # noqa: E501
        """CompletionUsage - a model defined in OpenAPI

        :param completion_tokens: The completion_tokens of this CompletionUsage.  # noqa: E501
        :type completion_tokens: int
        :param prompt_tokens: The prompt_tokens of this CompletionUsage.  # noqa: E501
        :type prompt_tokens: int
        :param total_tokens: The total_tokens of this CompletionUsage.  # noqa: E501
        :type total_tokens: int
        :param completion_tokens_details: The completion_tokens_details of this CompletionUsage.  # noqa: E501
        :type completion_tokens_details: CompletionUsageCompletionTokensDetails
        :param prompt_tokens_details: The prompt_tokens_details of this CompletionUsage.  # noqa: E501
        :type prompt_tokens_details: CompletionUsagePromptTokensDetails
        """
        self.openapi_types = {
            'completion_tokens': int,
            'prompt_tokens': int,
            'total_tokens': int,
            'completion_tokens_details': CompletionUsageCompletionTokensDetails,
            'prompt_tokens_details': CompletionUsagePromptTokensDetails
        }

        self.attribute_map = {
            'completion_tokens': 'completion_tokens',
            'prompt_tokens': 'prompt_tokens',
            'total_tokens': 'total_tokens',
            'completion_tokens_details': 'completion_tokens_details',
            'prompt_tokens_details': 'prompt_tokens_details'
        }

        self._completion_tokens = completion_tokens
        self._prompt_tokens = prompt_tokens
        self._total_tokens = total_tokens
        self._completion_tokens_details = completion_tokens_details
        self._prompt_tokens_details = prompt_tokens_details

    @classmethod
    def from_dict(cls, dikt) -> 'CompletionUsage':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CompletionUsage of this CompletionUsage.  # noqa: E501
        :rtype: CompletionUsage
        """
        return util.deserialize_model(dikt, cls)

    @property
    def completion_tokens(self) -> int:
        """Gets the completion_tokens of this CompletionUsage.

        Number of tokens in the generated completion.  # noqa: E501

        :return: The completion_tokens of this CompletionUsage.
        :rtype: int
        """
        return self._completion_tokens

    @completion_tokens.setter
    def completion_tokens(self, completion_tokens: int):
        """Sets the completion_tokens of this CompletionUsage.

        Number of tokens in the generated completion.  # noqa: E501

        :param completion_tokens: The completion_tokens of this CompletionUsage.
        :type completion_tokens: int
        """
        if completion_tokens is None:
            raise ValueError("Invalid value for `completion_tokens`, must not be `None`")  # noqa: E501

        self._completion_tokens = completion_tokens

    @property
    def prompt_tokens(self) -> int:
        """Gets the prompt_tokens of this CompletionUsage.

        Number of tokens in the prompt.  # noqa: E501

        :return: The prompt_tokens of this CompletionUsage.
        :rtype: int
        """
        return self._prompt_tokens

    @prompt_tokens.setter
    def prompt_tokens(self, prompt_tokens: int):
        """Sets the prompt_tokens of this CompletionUsage.

        Number of tokens in the prompt.  # noqa: E501

        :param prompt_tokens: The prompt_tokens of this CompletionUsage.
        :type prompt_tokens: int
        """
        if prompt_tokens is None:
            raise ValueError("Invalid value for `prompt_tokens`, must not be `None`")  # noqa: E501

        self._prompt_tokens = prompt_tokens

    @property
    def total_tokens(self) -> int:
        """Gets the total_tokens of this CompletionUsage.

        Total number of tokens used in the request (prompt + completion).  # noqa: E501

        :return: The total_tokens of this CompletionUsage.
        :rtype: int
        """
        return self._total_tokens

    @total_tokens.setter
    def total_tokens(self, total_tokens: int):
        """Sets the total_tokens of this CompletionUsage.

        Total number of tokens used in the request (prompt + completion).  # noqa: E501

        :param total_tokens: The total_tokens of this CompletionUsage.
        :type total_tokens: int
        """
        if total_tokens is None:
            raise ValueError("Invalid value for `total_tokens`, must not be `None`")  # noqa: E501

        self._total_tokens = total_tokens

    @property
    def completion_tokens_details(self) -> CompletionUsageCompletionTokensDetails:
        """Gets the completion_tokens_details of this CompletionUsage.


        :return: The completion_tokens_details of this CompletionUsage.
        :rtype: CompletionUsageCompletionTokensDetails
        """
        return self._completion_tokens_details

    @completion_tokens_details.setter
    def completion_tokens_details(self, completion_tokens_details: CompletionUsageCompletionTokensDetails):
        """Sets the completion_tokens_details of this CompletionUsage.


        :param completion_tokens_details: The completion_tokens_details of this CompletionUsage.
        :type completion_tokens_details: CompletionUsageCompletionTokensDetails
        """

        self._completion_tokens_details = completion_tokens_details

    @property
    def prompt_tokens_details(self) -> CompletionUsagePromptTokensDetails:
        """Gets the prompt_tokens_details of this CompletionUsage.


        :return: The prompt_tokens_details of this CompletionUsage.
        :rtype: CompletionUsagePromptTokensDetails
        """
        return self._prompt_tokens_details

    @prompt_tokens_details.setter
    def prompt_tokens_details(self, prompt_tokens_details: CompletionUsagePromptTokensDetails):
        """Sets the prompt_tokens_details of this CompletionUsage.


        :param prompt_tokens_details: The prompt_tokens_details of this CompletionUsage.
        :type prompt_tokens_details: CompletionUsagePromptTokensDetails
        """

        self._prompt_tokens_details = prompt_tokens_details
