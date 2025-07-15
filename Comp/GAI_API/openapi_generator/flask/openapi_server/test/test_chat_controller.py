import unittest

from flask import json

from openapi_server.models.chat_completion_deleted import ChatCompletionDeleted  # noqa: E501
from openapi_server.models.chat_completion_list import ChatCompletionList  # noqa: E501
from openapi_server.models.chat_completion_message_list import ChatCompletionMessageList  # noqa: E501
from openapi_server.models.create_chat_completion_request import CreateChatCompletionRequest  # noqa: E501
from openapi_server.models.create_chat_completion_response import CreateChatCompletionResponse  # noqa: E501
from openapi_server.models.create_chat_completion_stream_response import CreateChatCompletionStreamResponse  # noqa: E501
from openapi_server.models.update_chat_completion_request import UpdateChatCompletionRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestChatController(BaseTestCase):
    """ChatController integration test stubs"""

    def test_create_chat_completion(self):
        """Test case for create_chat_completion

        **Starting a new project?** We recommend trying [Responses](/docs/api-reference/responses)  to take advantage of the latest OpenAI platform features. Compare [Chat Completions with Responses](/docs/guides/responses-vs-chat-completions?api-mode=responses).  ---  Creates a model response for the given chat conversation. Learn more in the [text generation](/docs/guides/text-generation), [vision](/docs/guides/vision), and [audio](/docs/guides/audio) guides.  Parameter support can differ depending on the model used to generate the response, particularly for newer reasoning models. Parameters that are only supported for reasoning models are noted below. For the current state of  unsupported parameters in reasoning models,  [refer to the reasoning guide](/docs/guides/reasoning). 
        """
        create_chat_completion_request = {"reasoning_effort":"medium","top_logprobs":11,"metadata":{"key":"metadata"},"logit_bias":{"key":5},"seed":2147483647,"functions":[{"name":"name","description":"description","parameters":{"key":""}},{"name":"name","description":"description","parameters":{"key":""}},{"name":"name","description":"description","parameters":{"key":""}},{"name":"name","description":"description","parameters":{"key":""}},{"name":"name","description":"description","parameters":{"key":""}}],"function_call":"none","presence_penalty":-1.413674807798822,"tools":[{"function":{"name":"name","description":"description","strict":False,"parameters":{"key":""}},"type":"function"},{"function":{"name":"name","description":"description","strict":False,"parameters":{"key":""}},"type":"function"}],"web_search_options":{"search_context_size":"medium","user_location":{"approximate":{"country":"country","city":"city","timezone":"timezone","region":"region"},"type":"approximate"}},"logprobs":False,"top_p":1,"max_completion_tokens":0,"modalities":["text","text"],"frequency_penalty":0.4109824732281613,"response_format":{"type":"text"},"stream":False,"temperature":1,"tool_choice":"none","service_tier":"auto","model":"gpt-4o","audio":{"voice":"ash","format":"wav"},"max_tokens":2,"store":False,"n":1,"stop":"\n","prediction":{"type":"content","content":"PredictionContent_content"},"messages":[{"role":"developer","name":"name","content":"ChatCompletionRequestDeveloperMessage_content"},{"role":"developer","name":"name","content":"ChatCompletionRequestDeveloperMessage_content"}],"stream_options":{"include_usage":True},"user":"user-1234"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/v1/chat/completions',
            method='POST',
            headers=headers,
            data=json.dumps(create_chat_completion_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_chat_completion(self):
        """Test case for delete_chat_completion

        Delete a stored chat completion. Only Chat Completions that have been created with the `store` parameter set to `true` can be deleted. 
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/v1/chat/completions/{completion_id}'.format(completion_id='completion_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_chat_completion(self):
        """Test case for get_chat_completion

        Get a stored chat completion. Only Chat Completions that have been created with the `store` parameter set to `true` will be returned. 
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/v1/chat/completions/{completion_id}'.format(completion_id='completion_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_chat_completion_messages(self):
        """Test case for get_chat_completion_messages

        Get the messages in a stored chat completion. Only Chat Completions that have been created with the `store` parameter set to `true` will be returned. 
        """
        query_string = [('after', 'after_example'),
                        ('limit', 20),
                        ('order', asc)]
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/v1/chat/completions/{completion_id}/messages'.format(completion_id='completion_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_chat_completions(self):
        """Test case for list_chat_completions

        List stored Chat Completions. Only Chat Completions that have been stored with the `store` parameter set to `true` will be returned. 
        """
        query_string = [('model', 'model_example'),
                        ('metadata', {'key': 'metadata_example'}),
                        ('after', 'after_example'),
                        ('limit', 20),
                        ('order', asc)]
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/v1/chat/completions',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_chat_completion(self):
        """Test case for update_chat_completion

        Modify a stored chat completion. Only Chat Completions that have been created with the `store` parameter set to `true` can be modified. Currently, the only supported modification is to update the `metadata` field. 
        """
        update_chat_completion_request = openapi_server.UpdateChatCompletionRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/v1/chat/completions/{completion_id}'.format(completion_id='completion_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(update_chat_completion_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
