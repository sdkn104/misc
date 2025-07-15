# ChatCompletionStreamOptions
## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
| **include\_usage** | **Boolean** | If set, an additional chunk will be streamed before the &#x60;data: [DONE]&#x60; message. The &#x60;usage&#x60; field on this chunk shows the token usage statistics for the entire request, and the &#x60;choices&#x60; field will always be an empty array.   All other chunks will also include a &#x60;usage&#x60; field, but with a null value. **NOTE:** If the stream is interrupted, you may not receive the final usage chunk which contains the total token usage for the request.  | [optional] [default to null] |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

