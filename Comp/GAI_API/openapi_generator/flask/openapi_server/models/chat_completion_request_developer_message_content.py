from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server.models.chat_completion_request_message_content_part_text import ChatCompletionRequestMessageContentPartText
from openapi_server import util

from openapi_server.models.chat_completion_request_message_content_part_text import ChatCompletionRequestMessageContentPartText  # noqa: E501

class ChatCompletionRequestDeveloperMessageContent(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self):  # noqa: E501
        """ChatCompletionRequestDeveloperMessageContent - a model defined in OpenAPI

        """
        self.openapi_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'ChatCompletionRequestDeveloperMessageContent':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ChatCompletionRequestDeveloperMessage_content of this ChatCompletionRequestDeveloperMessageContent.  # noqa: E501
        :rtype: ChatCompletionRequestDeveloperMessageContent
        """
        return util.deserialize_model(dikt, cls)
