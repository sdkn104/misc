# Documentation for OpenAI API

<a name="documentation-for-api-endpoints"></a>
## Documentation for API Endpoints

All URIs are relative to *https://api.openai.com/v1*

| Class | Method | HTTP request | Description |
|------------ | ------------- | ------------- | -------------|
| *ChatApi* | [**createChatCompletion**](Apis/ChatApi.md#createchatcompletion) | **POST** /chat/completions | **Starting a new project?** We recommend trying [Responses](/docs/api-reference/responses)  to take advantage of the latest OpenAI platform features. Compare [Chat Completions with Responses](/docs/guides/responses-vs-chat-completions?api-mode=responses).  ---  Creates a model response for the given chat conversation. Learn more in the [text generation](/docs/guides/text-generation), [vision](/docs/guides/vision), and [audio](/docs/guides/audio) guides.  Parameter support can differ depending on the model used to generate the response, particularly for newer reasoning models. Parameters that are only supported for reasoning models are noted below. For the current state of  unsupported parameters in reasoning models,  [refer to the reasoning guide](/docs/guides/reasoning).  |
*ChatApi* | [**deleteChatCompletion**](Apis/ChatApi.md#deletechatcompletion) | **DELETE** /chat/completions/{completion_id} | Delete a stored chat completion. Only Chat Completions that have been created with the `store` parameter set to `true` can be deleted.  |
*ChatApi* | [**getChatCompletion**](Apis/ChatApi.md#getchatcompletion) | **GET** /chat/completions/{completion_id} | Get a stored chat completion. Only Chat Completions that have been created with the `store` parameter set to `true` will be returned.  |
*ChatApi* | [**getChatCompletionMessages**](Apis/ChatApi.md#getchatcompletionmessages) | **GET** /chat/completions/{completion_id}/messages | Get the messages in a stored chat completion. Only Chat Completions that have been created with the `store` parameter set to `true` will be returned.  |
*ChatApi* | [**listChatCompletions**](Apis/ChatApi.md#listchatcompletions) | **GET** /chat/completions | List stored Chat Completions. Only Chat Completions that have been stored with the `store` parameter set to `true` will be returned.  |
*ChatApi* | [**updateChatCompletion**](Apis/ChatApi.md#updatechatcompletion) | **POST** /chat/completions/{completion_id} | Modify a stored chat completion. Only Chat Completions that have been created with the `store` parameter set to `true` can be modified. Currently, the only supported modification is to update the `metadata` field.  |
| *CompletionsApi* | [**createCompletion**](Apis/CompletionsApi.md#createcompletion) | **POST** /completions | Creates a completion for the provided prompt and parameters. |
| *ModelsApi* | [**deleteModel**](Apis/ModelsApi.md#deletemodel) | **DELETE** /models/{model} | Delete a fine-tuned model. You must have the Owner role in your organization to delete a model. |
*ModelsApi* | [**listModels**](Apis/ModelsApi.md#listmodels) | **GET** /models | Lists the currently available models, and provides basic information about each one such as the owner and availability. |
*ModelsApi* | [**retrieveModel**](Apis/ModelsApi.md#retrievemodel) | **GET** /models/{model} | Retrieves a model instance, providing basic information about the model such as the owner and permissioning. |


<a name="documentation-for-models"></a>
## Documentation for Models

 - [ChatCompletionDeleted](./Models/ChatCompletionDeleted.md)
 - [ChatCompletionFunctionCallOption](./Models/ChatCompletionFunctionCallOption.md)
 - [ChatCompletionFunctions](./Models/ChatCompletionFunctions.md)
 - [ChatCompletionList](./Models/ChatCompletionList.md)
 - [ChatCompletionMessageList](./Models/ChatCompletionMessageList.md)
 - [ChatCompletionMessageList_data_inner](./Models/ChatCompletionMessageList_data_inner.md)
 - [ChatCompletionMessageToolCall](./Models/ChatCompletionMessageToolCall.md)
 - [ChatCompletionMessageToolCallChunk](./Models/ChatCompletionMessageToolCallChunk.md)
 - [ChatCompletionMessageToolCallChunk_function](./Models/ChatCompletionMessageToolCallChunk_function.md)
 - [ChatCompletionMessageToolCall_function](./Models/ChatCompletionMessageToolCall_function.md)
 - [ChatCompletionNamedToolChoice](./Models/ChatCompletionNamedToolChoice.md)
 - [ChatCompletionNamedToolChoice_function](./Models/ChatCompletionNamedToolChoice_function.md)
 - [ChatCompletionRequestAssistantMessage](./Models/ChatCompletionRequestAssistantMessage.md)
 - [ChatCompletionRequestAssistantMessageContentPart](./Models/ChatCompletionRequestAssistantMessageContentPart.md)
 - [ChatCompletionRequestAssistantMessage_audio](./Models/ChatCompletionRequestAssistantMessage_audio.md)
 - [ChatCompletionRequestAssistantMessage_content](./Models/ChatCompletionRequestAssistantMessage_content.md)
 - [ChatCompletionRequestAssistantMessage_function_call](./Models/ChatCompletionRequestAssistantMessage_function_call.md)
 - [ChatCompletionRequestDeveloperMessage](./Models/ChatCompletionRequestDeveloperMessage.md)
 - [ChatCompletionRequestDeveloperMessage_content](./Models/ChatCompletionRequestDeveloperMessage_content.md)
 - [ChatCompletionRequestFunctionMessage](./Models/ChatCompletionRequestFunctionMessage.md)
 - [ChatCompletionRequestMessage](./Models/ChatCompletionRequestMessage.md)
 - [ChatCompletionRequestMessageContentPartAudio](./Models/ChatCompletionRequestMessageContentPartAudio.md)
 - [ChatCompletionRequestMessageContentPartAudio_input_audio](./Models/ChatCompletionRequestMessageContentPartAudio_input_audio.md)
 - [ChatCompletionRequestMessageContentPartFile](./Models/ChatCompletionRequestMessageContentPartFile.md)
 - [ChatCompletionRequestMessageContentPartFile_file](./Models/ChatCompletionRequestMessageContentPartFile_file.md)
 - [ChatCompletionRequestMessageContentPartImage](./Models/ChatCompletionRequestMessageContentPartImage.md)
 - [ChatCompletionRequestMessageContentPartImage_image_url](./Models/ChatCompletionRequestMessageContentPartImage_image_url.md)
 - [ChatCompletionRequestMessageContentPartRefusal](./Models/ChatCompletionRequestMessageContentPartRefusal.md)
 - [ChatCompletionRequestMessageContentPartText](./Models/ChatCompletionRequestMessageContentPartText.md)
 - [ChatCompletionRequestSystemMessage](./Models/ChatCompletionRequestSystemMessage.md)
 - [ChatCompletionRequestSystemMessage_content](./Models/ChatCompletionRequestSystemMessage_content.md)
 - [ChatCompletionRequestToolMessage](./Models/ChatCompletionRequestToolMessage.md)
 - [ChatCompletionRequestToolMessage_content](./Models/ChatCompletionRequestToolMessage_content.md)
 - [ChatCompletionRequestUserMessage](./Models/ChatCompletionRequestUserMessage.md)
 - [ChatCompletionRequestUserMessageContentPart](./Models/ChatCompletionRequestUserMessageContentPart.md)
 - [ChatCompletionRequestUserMessage_content](./Models/ChatCompletionRequestUserMessage_content.md)
 - [ChatCompletionResponseMessage](./Models/ChatCompletionResponseMessage.md)
 - [ChatCompletionResponseMessage_annotations_inner](./Models/ChatCompletionResponseMessage_annotations_inner.md)
 - [ChatCompletionResponseMessage_annotations_inner_url_citation](./Models/ChatCompletionResponseMessage_annotations_inner_url_citation.md)
 - [ChatCompletionResponseMessage_audio](./Models/ChatCompletionResponseMessage_audio.md)
 - [ChatCompletionResponseMessage_function_call](./Models/ChatCompletionResponseMessage_function_call.md)
 - [ChatCompletionStreamOptions](./Models/ChatCompletionStreamOptions.md)
 - [ChatCompletionStreamResponseDelta](./Models/ChatCompletionStreamResponseDelta.md)
 - [ChatCompletionStreamResponseDelta_function_call](./Models/ChatCompletionStreamResponseDelta_function_call.md)
 - [ChatCompletionTokenLogprob](./Models/ChatCompletionTokenLogprob.md)
 - [ChatCompletionTokenLogprob_top_logprobs_inner](./Models/ChatCompletionTokenLogprob_top_logprobs_inner.md)
 - [ChatCompletionTool](./Models/ChatCompletionTool.md)
 - [ChatCompletionToolChoiceOption](./Models/ChatCompletionToolChoiceOption.md)
 - [CompletionUsage](./Models/CompletionUsage.md)
 - [CompletionUsage_completion_tokens_details](./Models/CompletionUsage_completion_tokens_details.md)
 - [CompletionUsage_prompt_tokens_details](./Models/CompletionUsage_prompt_tokens_details.md)
 - [CreateChatCompletionRequest](./Models/CreateChatCompletionRequest.md)
 - [CreateChatCompletionRequest_allOf_audio](./Models/CreateChatCompletionRequest_allOf_audio.md)
 - [CreateChatCompletionRequest_allOf_function_call](./Models/CreateChatCompletionRequest_allOf_function_call.md)
 - [CreateChatCompletionRequest_allOf_response_format](./Models/CreateChatCompletionRequest_allOf_response_format.md)
 - [CreateChatCompletionResponse](./Models/CreateChatCompletionResponse.md)
 - [CreateChatCompletionResponse_choices_inner](./Models/CreateChatCompletionResponse_choices_inner.md)
 - [CreateChatCompletionResponse_choices_inner_logprobs](./Models/CreateChatCompletionResponse_choices_inner_logprobs.md)
 - [CreateChatCompletionStreamResponse](./Models/CreateChatCompletionStreamResponse.md)
 - [CreateChatCompletionStreamResponse_choices_inner](./Models/CreateChatCompletionStreamResponse_choices_inner.md)
 - [CreateCompletionRequest](./Models/CreateCompletionRequest.md)
 - [CreateCompletionRequest_model](./Models/CreateCompletionRequest_model.md)
 - [CreateCompletionRequest_prompt](./Models/CreateCompletionRequest_prompt.md)
 - [CreateCompletionResponse](./Models/CreateCompletionResponse.md)
 - [CreateCompletionResponse_choices_inner](./Models/CreateCompletionResponse_choices_inner.md)
 - [CreateCompletionResponse_choices_inner_logprobs](./Models/CreateCompletionResponse_choices_inner_logprobs.md)
 - [CreateModelResponseProperties](./Models/CreateModelResponseProperties.md)
 - [DeleteModelResponse](./Models/DeleteModelResponse.md)
 - [FunctionObject](./Models/FunctionObject.md)
 - [JSON_schema](./Models/JSON_schema.md)
 - [ListModelsResponse](./Models/ListModelsResponse.md)
 - [Model](./Models/Model.md)
 - [ModelIdsShared](./Models/ModelIdsShared.md)
 - [ModelResponseProperties](./Models/ModelResponseProperties.md)
 - [PredictionContent](./Models/PredictionContent.md)
 - [PredictionContent_content](./Models/PredictionContent_content.md)
 - [ReasoningEffort](./Models/ReasoningEffort.md)
 - [ResponseFormatJsonObject](./Models/ResponseFormatJsonObject.md)
 - [ResponseFormatJsonSchema](./Models/ResponseFormatJsonSchema.md)
 - [ResponseFormatText](./Models/ResponseFormatText.md)
 - [ServiceTier](./Models/ServiceTier.md)
 - [StopConfiguration](./Models/StopConfiguration.md)
 - [VoiceIdsShared](./Models/VoiceIdsShared.md)
 - [WebSearchContextSize](./Models/WebSearchContextSize.md)
 - [WebSearchLocation](./Models/WebSearchLocation.md)
 - [Web_search](./Models/Web_search.md)
 - [Web_search_user_location](./Models/Web_search_user_location.md)
 - [updateChatCompletion_request](./Models/updateChatCompletion_request.md)


<a name="documentation-for-authorization"></a>
## Documentation for Authorization

<a name="ApiKeyAuth"></a>
### ApiKeyAuth

- **Type**: HTTP Bearer Token authentication

