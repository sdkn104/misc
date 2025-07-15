# ChatApi

All URIs are relative to *https://api.openai.com/v1*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createChatCompletion**](ChatApi.md#createChatCompletion) | **POST** /chat/completions | **Starting a new project?** We recommend trying [Responses](/docs/api-reference/responses)  to take advantage of the latest OpenAI platform features. Compare [Chat Completions with Responses](/docs/guides/responses-vs-chat-completions?api-mode&#x3D;responses).  ---  Creates a model response for the given chat conversation. Learn more in the [text generation](/docs/guides/text-generation), [vision](/docs/guides/vision), and [audio](/docs/guides/audio) guides.  Parameter support can differ depending on the model used to generate the response, particularly for newer reasoning models. Parameters that are only supported for reasoning models are noted below. For the current state of  unsupported parameters in reasoning models,  [refer to the reasoning guide](/docs/guides/reasoning).  |
| [**deleteChatCompletion**](ChatApi.md#deleteChatCompletion) | **DELETE** /chat/completions/{completion_id} | Delete a stored chat completion. Only Chat Completions that have been created with the &#x60;store&#x60; parameter set to &#x60;true&#x60; can be deleted.  |
| [**getChatCompletion**](ChatApi.md#getChatCompletion) | **GET** /chat/completions/{completion_id} | Get a stored chat completion. Only Chat Completions that have been created with the &#x60;store&#x60; parameter set to &#x60;true&#x60; will be returned.  |
| [**getChatCompletionMessages**](ChatApi.md#getChatCompletionMessages) | **GET** /chat/completions/{completion_id}/messages | Get the messages in a stored chat completion. Only Chat Completions that have been created with the &#x60;store&#x60; parameter set to &#x60;true&#x60; will be returned.  |
| [**listChatCompletions**](ChatApi.md#listChatCompletions) | **GET** /chat/completions | List stored Chat Completions. Only Chat Completions that have been stored with the &#x60;store&#x60; parameter set to &#x60;true&#x60; will be returned.  |
| [**updateChatCompletion**](ChatApi.md#updateChatCompletion) | **POST** /chat/completions/{completion_id} | Modify a stored chat completion. Only Chat Completions that have been created with the &#x60;store&#x60; parameter set to &#x60;true&#x60; can be modified. Currently, the only supported modification is to update the &#x60;metadata&#x60; field.  |


<a name="createChatCompletion"></a>
# **createChatCompletion**
> CreateChatCompletionResponse createChatCompletion(CreateChatCompletionRequest)

**Starting a new project?** We recommend trying [Responses](/docs/api-reference/responses)  to take advantage of the latest OpenAI platform features. Compare [Chat Completions with Responses](/docs/guides/responses-vs-chat-completions?api-mode&#x3D;responses).  ---  Creates a model response for the given chat conversation. Learn more in the [text generation](/docs/guides/text-generation), [vision](/docs/guides/vision), and [audio](/docs/guides/audio) guides.  Parameter support can differ depending on the model used to generate the response, particularly for newer reasoning models. Parameters that are only supported for reasoning models are noted below. For the current state of  unsupported parameters in reasoning models,  [refer to the reasoning guide](/docs/guides/reasoning). 

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **CreateChatCompletionRequest** | [**CreateChatCompletionRequest**](../Models/CreateChatCompletionRequest.md)|  | |

### Return type

[**CreateChatCompletionResponse**](../Models/CreateChatCompletionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json, text/event-stream

<a name="deleteChatCompletion"></a>
# **deleteChatCompletion**
> ChatCompletionDeleted deleteChatCompletion(completion\_id)

Delete a stored chat completion. Only Chat Completions that have been created with the &#x60;store&#x60; parameter set to &#x60;true&#x60; can be deleted. 

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **completion\_id** | **String**| The ID of the chat completion to delete. | [default to null] |

### Return type

[**ChatCompletionDeleted**](../Models/ChatCompletionDeleted.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="getChatCompletion"></a>
# **getChatCompletion**
> CreateChatCompletionResponse getChatCompletion(completion\_id)

Get a stored chat completion. Only Chat Completions that have been created with the &#x60;store&#x60; parameter set to &#x60;true&#x60; will be returned. 

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **completion\_id** | **String**| The ID of the chat completion to retrieve. | [default to null] |

### Return type

[**CreateChatCompletionResponse**](../Models/CreateChatCompletionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="getChatCompletionMessages"></a>
# **getChatCompletionMessages**
> ChatCompletionMessageList getChatCompletionMessages(completion\_id, after, limit, order)

Get the messages in a stored chat completion. Only Chat Completions that have been created with the &#x60;store&#x60; parameter set to &#x60;true&#x60; will be returned. 

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **completion\_id** | **String**| The ID of the chat completion to retrieve messages from. | [default to null] |
| **after** | **String**| Identifier for the last message from the previous pagination request. | [optional] [default to null] |
| **limit** | **Integer**| Number of messages to retrieve. | [optional] [default to 20] |
| **order** | **String**| Sort order for messages by timestamp. Use &#x60;asc&#x60; for ascending order or &#x60;desc&#x60; for descending order. Defaults to &#x60;asc&#x60;. | [optional] [default to asc] [enum: asc, desc] |

### Return type

[**ChatCompletionMessageList**](../Models/ChatCompletionMessageList.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="listChatCompletions"></a>
# **listChatCompletions**
> ChatCompletionList listChatCompletions(model, metadata, after, limit, order)

List stored Chat Completions. Only Chat Completions that have been stored with the &#x60;store&#x60; parameter set to &#x60;true&#x60; will be returned. 

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **model** | **String**| The model used to generate the Chat Completions. | [optional] [default to null] |
| **metadata** | [**Map**](../Models/String.md)| A list of metadata keys to filter the Chat Completions by. Example:  &#x60;metadata[key1]&#x3D;value1&amp;metadata[key2]&#x3D;value2&#x60;  | [optional] [default to null] |
| **after** | **String**| Identifier for the last chat completion from the previous pagination request. | [optional] [default to null] |
| **limit** | **Integer**| Number of Chat Completions to retrieve. | [optional] [default to 20] |
| **order** | **String**| Sort order for Chat Completions by timestamp. Use &#x60;asc&#x60; for ascending order or &#x60;desc&#x60; for descending order. Defaults to &#x60;asc&#x60;. | [optional] [default to asc] [enum: asc, desc] |

### Return type

[**ChatCompletionList**](../Models/ChatCompletionList.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="updateChatCompletion"></a>
# **updateChatCompletion**
> CreateChatCompletionResponse updateChatCompletion(completion\_id, updateChatCompletion\_request)

Modify a stored chat completion. Only Chat Completions that have been created with the &#x60;store&#x60; parameter set to &#x60;true&#x60; can be modified. Currently, the only supported modification is to update the &#x60;metadata&#x60; field. 

### Parameters

|Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **completion\_id** | **String**| The ID of the chat completion to update. | [default to null] |
| **updateChatCompletion\_request** | [**updateChatCompletion_request**](../Models/updateChatCompletion_request.md)|  | |

### Return type

[**CreateChatCompletionResponse**](../Models/CreateChatCompletionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

