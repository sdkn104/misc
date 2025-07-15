import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.chat_completion_deleted import ChatCompletionDeleted  # noqa: E501
from openapi_server.models.chat_completion_list import ChatCompletionList  # noqa: E501
from openapi_server.models.chat_completion_message_list import ChatCompletionMessageList  # noqa: E501
from openapi_server.models.create_chat_completion_request import CreateChatCompletionRequest  # noqa: E501
from openapi_server.models.create_chat_completion_response import CreateChatCompletionResponse  # noqa: E501
from openapi_server.models.create_chat_completion_stream_response import CreateChatCompletionStreamResponse  # noqa: E501
from openapi_server.models.update_chat_completion_request import UpdateChatCompletionRequest  # noqa: E501
from openapi_server import util


def create_chat_completion(body):  # noqa: E501
    """**Starting a new project?** We recommend trying [Responses](/docs/api-reference/responses)  to take advantage of the latest OpenAI platform features. Compare [Chat Completions with Responses](/docs/guides/responses-vs-chat-completions?api-mode&#x3D;responses).  ---  Creates a model response for the given chat conversation. Learn more in the [text generation](/docs/guides/text-generation), [vision](/docs/guides/vision), and [audio](/docs/guides/audio) guides.  Parameter support can differ depending on the model used to generate the response, particularly for newer reasoning models. Parameters that are only supported for reasoning models are noted below. For the current state of  unsupported parameters in reasoning models,  [refer to the reasoning guide](/docs/guides/reasoning). 

     # noqa: E501

    :param create_chat_completion_request: 
    :type create_chat_completion_request: dict | bytes

    :rtype: Union[CreateChatCompletionResponse, Tuple[CreateChatCompletionResponse, int], Tuple[CreateChatCompletionResponse, int, Dict[str, str]]
    """
    create_chat_completion_request = body
    if connexion.request.is_json:
        create_chat_completion_request = CreateChatCompletionRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_chat_completion(completion_id):  # noqa: E501
    """Delete a stored chat completion. Only Chat Completions that have been created with the &#x60;store&#x60; parameter set to &#x60;true&#x60; can be deleted. 

     # noqa: E501

    :param completion_id: The ID of the chat completion to delete.
    :type completion_id: str

    :rtype: Union[ChatCompletionDeleted, Tuple[ChatCompletionDeleted, int], Tuple[ChatCompletionDeleted, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_chat_completion(completion_id):  # noqa: E501
    """Get a stored chat completion. Only Chat Completions that have been created with the &#x60;store&#x60; parameter set to &#x60;true&#x60; will be returned. 

     # noqa: E501

    :param completion_id: The ID of the chat completion to retrieve.
    :type completion_id: str

    :rtype: Union[CreateChatCompletionResponse, Tuple[CreateChatCompletionResponse, int], Tuple[CreateChatCompletionResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_chat_completion_messages(completion_id, after=None, limit=None, order=None):  # noqa: E501
    """Get the messages in a stored chat completion. Only Chat Completions that have been created with the &#x60;store&#x60; parameter set to &#x60;true&#x60; will be returned. 

     # noqa: E501

    :param completion_id: The ID of the chat completion to retrieve messages from.
    :type completion_id: str
    :param after: Identifier for the last message from the previous pagination request.
    :type after: str
    :param limit: Number of messages to retrieve.
    :type limit: int
    :param order: Sort order for messages by timestamp. Use &#x60;asc&#x60; for ascending order or &#x60;desc&#x60; for descending order. Defaults to &#x60;asc&#x60;.
    :type order: str

    :rtype: Union[ChatCompletionMessageList, Tuple[ChatCompletionMessageList, int], Tuple[ChatCompletionMessageList, int, Dict[str, str]]
    """
    return 'do some magic!'


def list_chat_completions(model=None, metadata=None, after=None, limit=None, order=None):  # noqa: E501
    """List stored Chat Completions. Only Chat Completions that have been stored with the &#x60;store&#x60; parameter set to &#x60;true&#x60; will be returned. 

     # noqa: E501

    :param model: The model used to generate the Chat Completions.
    :type model: str
    :param metadata: A list of metadata keys to filter the Chat Completions by. Example:  &#x60;metadata[key1]&#x3D;value1&amp;metadata[key2]&#x3D;value2&#x60; 
    :type metadata: Dict[str, str]
    :param after: Identifier for the last chat completion from the previous pagination request.
    :type after: str
    :param limit: Number of Chat Completions to retrieve.
    :type limit: int
    :param order: Sort order for Chat Completions by timestamp. Use &#x60;asc&#x60; for ascending order or &#x60;desc&#x60; for descending order. Defaults to &#x60;asc&#x60;.
    :type order: str

    :rtype: Union[ChatCompletionList, Tuple[ChatCompletionList, int], Tuple[ChatCompletionList, int, Dict[str, str]]
    """
    return 'do some magic!'


def update_chat_completion(completion_id, body):  # noqa: E501
    """Modify a stored chat completion. Only Chat Completions that have been created with the &#x60;store&#x60; parameter set to &#x60;true&#x60; can be modified. Currently, the only supported modification is to update the &#x60;metadata&#x60; field. 

     # noqa: E501

    :param completion_id: The ID of the chat completion to update.
    :type completion_id: str
    :param update_chat_completion_request: 
    :type update_chat_completion_request: dict | bytes

    :rtype: Union[CreateChatCompletionResponse, Tuple[CreateChatCompletionResponse, int], Tuple[CreateChatCompletionResponse, int, Dict[str, str]]
    """
    update_chat_completion_request = body
    if connexion.request.is_json:
        update_chat_completion_request = UpdateChatCompletionRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
