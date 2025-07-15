

OpenAI API
==========

The OpenAI REST API. Please see https://platform.openai.com/docs/api-reference for more details.

More information: [https://help.openai.com/](https://help.openai.com/)

Contact Info: [team@openapitools.org](team@openapitools.org)

Version: 2.3.0

BasePath:/v1

MIT

https://github.com/openai/openai-openapi/blob/master/LICENSE

Access
------

1.  HTTP Bearer Token authentication

Methods
-------

\[ Jump to [Models](#__Models) \]

### Table of Contents

#### [Chat](#Chat)

*   [`post /chat/completions`](#createChatCompletion)
*   [`delete /chat/completions/{completion_id}`](#deleteChatCompletion)
*   [`get /chat/completions/{completion_id}`](#getChatCompletion)
*   [`get /chat/completions/{completion_id}/messages`](#getChatCompletionMessages)
*   [`get /chat/completions`](#listChatCompletions)
*   [`post /chat/completions/{completion_id}`](#updateChatCompletion)

#### [Completions](#Completions)

*   [`post /completions`](#createCompletion)

#### [Models](#Models)

*   [`delete /models/{model}`](#deleteModel)
*   [`get /models`](#listModels)
*   [`get /models/{model}`](#retrieveModel)

Chat
====

[Up](#__Methods)

    post /chat/completions

**Starting a new project?** We recommend trying [Responses](/docs/api-reference/responses) to take advantage of the latest OpenAI platform features. Compare [Chat Completions with Responses](/docs/guides/responses-vs-chat-completions?api-mode=responses).

* * *

Creates a model response for the given chat conversation. Learn more in the [text generation](/docs/guides/text-generation), [vision](/docs/guides/vision), and [audio](/docs/guides/audio) guides.

Parameter support can differ depending on the model used to generate the response, particularly for newer reasoning models. Parameters that are only supported for reasoning models are noted below. For the current state of unsupported parameters in reasoning models, [refer to the reasoning guide](/docs/guides/reasoning).

(createChatCompletion)

### Consumes

This API call consumes the following media types via the Content-Type request header:

*   `application/json`

### Request body

CreateChatCompletionRequest [CreateChatCompletionRequest](#CreateChatCompletionRequest) (required)

Body Parameter —

### Return type

[CreateChatCompletionResponse](#CreateChatCompletionResponse)

### Example data

Content-Type: application/json

    {
      "created" : 3,
      "usage" : {
        "completion_tokens" : 2,
        "prompt_tokens" : 4,
        "completion_tokens_details" : {
          "accepted_prediction_tokens" : 1,
          "audio_tokens" : 1,
          "reasoning_tokens" : 1,
          "rejected_prediction_tokens" : 6
        },
        "prompt_tokens_details" : {
          "audio_tokens" : 7,
          "cached_tokens" : 1
        },
        "total_tokens" : 7
      },
      "model" : "model",
      "service_tier" : "auto",
      "id" : "id",
      "choices" : [ {
        "finish_reason" : "stop",
        "index" : 0,
        "message" : {
          "role" : "assistant",
          "function_call" : {
            "name" : "name",
            "arguments" : "arguments"
          },
          "refusal" : "refusal",
          "annotations" : [ {
            "type" : "url_citation",
            "url_citation" : {
              "start_index" : 1,
              "end_index" : 6,
              "title" : "title",
              "url" : "url"
            }
          }, {
            "type" : "url_citation",
            "url_citation" : {
              "start_index" : 1,
              "end_index" : 6,
              "title" : "title",
              "url" : "url"
            }
          } ],
          "tool_calls" : [ {
            "function" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "id" : "id",
            "type" : "function"
          }, {
            "function" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "id" : "id",
            "type" : "function"
          } ],
          "audio" : {
            "expires_at" : 5,
            "transcript" : "transcript",
            "data" : "data",
            "id" : "id"
          },
          "content" : "content"
        },
        "logprobs" : {
          "refusal" : [ {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          }, {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          } ],
          "content" : [ {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          }, {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          } ]
        }
      }, {
        "finish_reason" : "stop",
        "index" : 0,
        "message" : {
          "role" : "assistant",
          "function_call" : {
            "name" : "name",
            "arguments" : "arguments"
          },
          "refusal" : "refusal",
          "annotations" : [ {
            "type" : "url_citation",
            "url_citation" : {
              "start_index" : 1,
              "end_index" : 6,
              "title" : "title",
              "url" : "url"
            }
          }, {
            "type" : "url_citation",
            "url_citation" : {
              "start_index" : 1,
              "end_index" : 6,
              "title" : "title",
              "url" : "url"
            }
          } ],
          "tool_calls" : [ {
            "function" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "id" : "id",
            "type" : "function"
          }, {
            "function" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "id" : "id",
            "type" : "function"
          } ],
          "audio" : {
            "expires_at" : 5,
            "transcript" : "transcript",
            "data" : "data",
            "id" : "id"
          },
          "content" : "content"
        },
        "logprobs" : {
          "refusal" : [ {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          }, {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          } ],
          "content" : [ {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          }, {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          } ]
        }
      } ],
      "system_fingerprint" : "system_fingerprint",
      "object" : "chat.completion"
    }

### Example data

Content-Type: text/event-stream

    Custom MIME type example not yet supported: text/event-stream

### Produces

This API call produces the following media types according to the Accept request header; the media type will be conveyed by the Content-Type response header.

*   `application/json`
*   `text/event-stream`

### Responses

#### 200

OK [CreateChatCompletionResponse](#CreateChatCompletionResponse)

* * *

[Up](#__Methods)

    delete /chat/completions/{completion_id}

Delete a stored chat completion. Only Chat Completions that have been created with the `store` parameter set to `true` can be deleted. (deleteChatCompletion)

### Path parameters

completion\_id (required)

Path Parameter — The ID of the chat completion to delete. default: null

### Return type

[ChatCompletionDeleted](#ChatCompletionDeleted)

### Example data

Content-Type: application/json

    {
      "deleted" : true,
      "id" : "id",
      "object" : "chat.completion.deleted"
    }

### Produces

This API call produces the following media types according to the Accept request header; the media type will be conveyed by the Content-Type response header.

*   `application/json`

### Responses

#### 200

The chat completion was deleted successfully. [ChatCompletionDeleted](#ChatCompletionDeleted)

* * *

[Up](#__Methods)

    get /chat/completions/{completion_id}

Get a stored chat completion. Only Chat Completions that have been created with the `store` parameter set to `true` will be returned. (getChatCompletion)

### Path parameters

completion\_id (required)

Path Parameter — The ID of the chat completion to retrieve. default: null

### Return type

[CreateChatCompletionResponse](#CreateChatCompletionResponse)

### Example data

Content-Type: application/json

    {
      "created" : 3,
      "usage" : {
        "completion_tokens" : 2,
        "prompt_tokens" : 4,
        "completion_tokens_details" : {
          "accepted_prediction_tokens" : 1,
          "audio_tokens" : 1,
          "reasoning_tokens" : 1,
          "rejected_prediction_tokens" : 6
        },
        "prompt_tokens_details" : {
          "audio_tokens" : 7,
          "cached_tokens" : 1
        },
        "total_tokens" : 7
      },
      "model" : "model",
      "service_tier" : "auto",
      "id" : "id",
      "choices" : [ {
        "finish_reason" : "stop",
        "index" : 0,
        "message" : {
          "role" : "assistant",
          "function_call" : {
            "name" : "name",
            "arguments" : "arguments"
          },
          "refusal" : "refusal",
          "annotations" : [ {
            "type" : "url_citation",
            "url_citation" : {
              "start_index" : 1,
              "end_index" : 6,
              "title" : "title",
              "url" : "url"
            }
          }, {
            "type" : "url_citation",
            "url_citation" : {
              "start_index" : 1,
              "end_index" : 6,
              "title" : "title",
              "url" : "url"
            }
          } ],
          "tool_calls" : [ {
            "function" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "id" : "id",
            "type" : "function"
          }, {
            "function" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "id" : "id",
            "type" : "function"
          } ],
          "audio" : {
            "expires_at" : 5,
            "transcript" : "transcript",
            "data" : "data",
            "id" : "id"
          },
          "content" : "content"
        },
        "logprobs" : {
          "refusal" : [ {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          }, {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          } ],
          "content" : [ {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          }, {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          } ]
        }
      }, {
        "finish_reason" : "stop",
        "index" : 0,
        "message" : {
          "role" : "assistant",
          "function_call" : {
            "name" : "name",
            "arguments" : "arguments"
          },
          "refusal" : "refusal",
          "annotations" : [ {
            "type" : "url_citation",
            "url_citation" : {
              "start_index" : 1,
              "end_index" : 6,
              "title" : "title",
              "url" : "url"
            }
          }, {
            "type" : "url_citation",
            "url_citation" : {
              "start_index" : 1,
              "end_index" : 6,
              "title" : "title",
              "url" : "url"
            }
          } ],
          "tool_calls" : [ {
            "function" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "id" : "id",
            "type" : "function"
          }, {
            "function" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "id" : "id",
            "type" : "function"
          } ],
          "audio" : {
            "expires_at" : 5,
            "transcript" : "transcript",
            "data" : "data",
            "id" : "id"
          },
          "content" : "content"
        },
        "logprobs" : {
          "refusal" : [ {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          }, {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          } ],
          "content" : [ {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          }, {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          } ]
        }
      } ],
      "system_fingerprint" : "system_fingerprint",
      "object" : "chat.completion"
    }

### Produces

This API call produces the following media types according to the Accept request header; the media type will be conveyed by the Content-Type response header.

*   `application/json`

### Responses

#### 200

A chat completion [CreateChatCompletionResponse](#CreateChatCompletionResponse)

* * *

[Up](#__Methods)

    get /chat/completions/{completion_id}/messages

Get the messages in a stored chat completion. Only Chat Completions that have been created with the `store` parameter set to `true` will be returned. (getChatCompletionMessages)

### Path parameters

completion\_id (required)

Path Parameter — The ID of the chat completion to retrieve messages from. default: null

### Query parameters

after (optional)

Query Parameter — Identifier for the last message from the previous pagination request. default: null

limit (optional)

Query Parameter — Number of messages to retrieve. default: 20

order (optional)

Query Parameter — Sort order for messages by timestamp. Use `asc` for ascending order or `desc` for descending order. Defaults to `asc`. default: asc

### Return type

[ChatCompletionMessageList](#ChatCompletionMessageList)

### Example data

Content-Type: application/json

    {
      "first_id" : "first_id",
      "data" : [ {
        "role" : "assistant",
        "function_call" : {
          "name" : "name",
          "arguments" : "arguments"
        },
        "refusal" : "refusal",
        "annotations" : [ {
          "type" : "url_citation",
          "url_citation" : {
            "start_index" : 1,
            "end_index" : 6,
            "title" : "title",
            "url" : "url"
          }
        }, {
          "type" : "url_citation",
          "url_citation" : {
            "start_index" : 1,
            "end_index" : 6,
            "title" : "title",
            "url" : "url"
          }
        } ],
        "tool_calls" : [ {
          "function" : {
            "name" : "name",
            "arguments" : "arguments"
          },
          "id" : "id",
          "type" : "function"
        }, {
          "function" : {
            "name" : "name",
            "arguments" : "arguments"
          },
          "id" : "id",
          "type" : "function"
        } ],
        "audio" : {
          "expires_at" : 5,
          "transcript" : "transcript",
          "data" : "data",
          "id" : "id"
        },
        "id" : "id",
        "content" : "content"
      }, {
        "role" : "assistant",
        "function_call" : {
          "name" : "name",
          "arguments" : "arguments"
        },
        "refusal" : "refusal",
        "annotations" : [ {
          "type" : "url_citation",
          "url_citation" : {
            "start_index" : 1,
            "end_index" : 6,
            "title" : "title",
            "url" : "url"
          }
        }, {
          "type" : "url_citation",
          "url_citation" : {
            "start_index" : 1,
            "end_index" : 6,
            "title" : "title",
            "url" : "url"
          }
        } ],
        "tool_calls" : [ {
          "function" : {
            "name" : "name",
            "arguments" : "arguments"
          },
          "id" : "id",
          "type" : "function"
        }, {
          "function" : {
            "name" : "name",
            "arguments" : "arguments"
          },
          "id" : "id",
          "type" : "function"
        } ],
        "audio" : {
          "expires_at" : 5,
          "transcript" : "transcript",
          "data" : "data",
          "id" : "id"
        },
        "id" : "id",
        "content" : "content"
      } ],
      "last_id" : "last_id",
      "has_more" : true,
      "object" : "list"
    }

### Produces

This API call produces the following media types according to the Accept request header; the media type will be conveyed by the Content-Type response header.

*   `application/json`

### Responses

#### 200

A list of messages [ChatCompletionMessageList](#ChatCompletionMessageList)

* * *

[Up](#__Methods)

    get /chat/completions

List stored Chat Completions. Only Chat Completions that have been stored with the `store` parameter set to `true` will be returned. (listChatCompletions)

### Query parameters

model (optional)

Query Parameter — The model used to generate the Chat Completions. default: null

metadata (optional)

Query Parameter —

A list of metadata keys to filter the Chat Completions by. Example:

`metadata[key1]=value1&metadata[key2]=value2`

default: null

after (optional)

Query Parameter — Identifier for the last chat completion from the previous pagination request. default: null

limit (optional)

Query Parameter — Number of Chat Completions to retrieve. default: 20

order (optional)

Query Parameter — Sort order for Chat Completions by timestamp. Use `asc` for ascending order or `desc` for descending order. Defaults to `asc`. default: asc

### Return type

[ChatCompletionList](#ChatCompletionList)

### Example data

Content-Type: application/json

    {
      "first_id" : "first_id",
      "data" : [ {
        "created" : 3,
        "usage" : {
          "completion_tokens" : 2,
          "prompt_tokens" : 4,
          "completion_tokens_details" : {
            "accepted_prediction_tokens" : 1,
            "audio_tokens" : 1,
            "reasoning_tokens" : 1,
            "rejected_prediction_tokens" : 6
          },
          "prompt_tokens_details" : {
            "audio_tokens" : 7,
            "cached_tokens" : 1
          },
          "total_tokens" : 7
        },
        "model" : "model",
        "service_tier" : "auto",
        "id" : "id",
        "choices" : [ {
          "finish_reason" : "stop",
          "index" : 0,
          "message" : {
            "role" : "assistant",
            "function_call" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "refusal" : "refusal",
            "annotations" : [ {
              "type" : "url_citation",
              "url_citation" : {
                "start_index" : 1,
                "end_index" : 6,
                "title" : "title",
                "url" : "url"
              }
            }, {
              "type" : "url_citation",
              "url_citation" : {
                "start_index" : 1,
                "end_index" : 6,
                "title" : "title",
                "url" : "url"
              }
            } ],
            "tool_calls" : [ {
              "function" : {
                "name" : "name",
                "arguments" : "arguments"
              },
              "id" : "id",
              "type" : "function"
            }, {
              "function" : {
                "name" : "name",
                "arguments" : "arguments"
              },
              "id" : "id",
              "type" : "function"
            } ],
            "audio" : {
              "expires_at" : 5,
              "transcript" : "transcript",
              "data" : "data",
              "id" : "id"
            },
            "content" : "content"
          },
          "logprobs" : {
            "refusal" : [ {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            }, {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            } ],
            "content" : [ {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            }, {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            } ]
          }
        }, {
          "finish_reason" : "stop",
          "index" : 0,
          "message" : {
            "role" : "assistant",
            "function_call" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "refusal" : "refusal",
            "annotations" : [ {
              "type" : "url_citation",
              "url_citation" : {
                "start_index" : 1,
                "end_index" : 6,
                "title" : "title",
                "url" : "url"
              }
            }, {
              "type" : "url_citation",
              "url_citation" : {
                "start_index" : 1,
                "end_index" : 6,
                "title" : "title",
                "url" : "url"
              }
            } ],
            "tool_calls" : [ {
              "function" : {
                "name" : "name",
                "arguments" : "arguments"
              },
              "id" : "id",
              "type" : "function"
            }, {
              "function" : {
                "name" : "name",
                "arguments" : "arguments"
              },
              "id" : "id",
              "type" : "function"
            } ],
            "audio" : {
              "expires_at" : 5,
              "transcript" : "transcript",
              "data" : "data",
              "id" : "id"
            },
            "content" : "content"
          },
          "logprobs" : {
            "refusal" : [ {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            }, {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            } ],
            "content" : [ {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            }, {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            } ]
          }
        } ],
        "system_fingerprint" : "system_fingerprint",
        "object" : "chat.completion"
      }, {
        "created" : 3,
        "usage" : {
          "completion_tokens" : 2,
          "prompt_tokens" : 4,
          "completion_tokens_details" : {
            "accepted_prediction_tokens" : 1,
            "audio_tokens" : 1,
            "reasoning_tokens" : 1,
            "rejected_prediction_tokens" : 6
          },
          "prompt_tokens_details" : {
            "audio_tokens" : 7,
            "cached_tokens" : 1
          },
          "total_tokens" : 7
        },
        "model" : "model",
        "service_tier" : "auto",
        "id" : "id",
        "choices" : [ {
          "finish_reason" : "stop",
          "index" : 0,
          "message" : {
            "role" : "assistant",
            "function_call" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "refusal" : "refusal",
            "annotations" : [ {
              "type" : "url_citation",
              "url_citation" : {
                "start_index" : 1,
                "end_index" : 6,
                "title" : "title",
                "url" : "url"
              }
            }, {
              "type" : "url_citation",
              "url_citation" : {
                "start_index" : 1,
                "end_index" : 6,
                "title" : "title",
                "url" : "url"
              }
            } ],
            "tool_calls" : [ {
              "function" : {
                "name" : "name",
                "arguments" : "arguments"
              },
              "id" : "id",
              "type" : "function"
            }, {
              "function" : {
                "name" : "name",
                "arguments" : "arguments"
              },
              "id" : "id",
              "type" : "function"
            } ],
            "audio" : {
              "expires_at" : 5,
              "transcript" : "transcript",
              "data" : "data",
              "id" : "id"
            },
            "content" : "content"
          },
          "logprobs" : {
            "refusal" : [ {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            }, {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            } ],
            "content" : [ {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            }, {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            } ]
          }
        }, {
          "finish_reason" : "stop",
          "index" : 0,
          "message" : {
            "role" : "assistant",
            "function_call" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "refusal" : "refusal",
            "annotations" : [ {
              "type" : "url_citation",
              "url_citation" : {
                "start_index" : 1,
                "end_index" : 6,
                "title" : "title",
                "url" : "url"
              }
            }, {
              "type" : "url_citation",
              "url_citation" : {
                "start_index" : 1,
                "end_index" : 6,
                "title" : "title",
                "url" : "url"
              }
            } ],
            "tool_calls" : [ {
              "function" : {
                "name" : "name",
                "arguments" : "arguments"
              },
              "id" : "id",
              "type" : "function"
            }, {
              "function" : {
                "name" : "name",
                "arguments" : "arguments"
              },
              "id" : "id",
              "type" : "function"
            } ],
            "audio" : {
              "expires_at" : 5,
              "transcript" : "transcript",
              "data" : "data",
              "id" : "id"
            },
            "content" : "content"
          },
          "logprobs" : {
            "refusal" : [ {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            }, {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            } ],
            "content" : [ {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            }, {
              "top_logprobs" : [ {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              }, {
                "logprob" : 7.061401241503109,
                "bytes" : [ 9, 9 ],
                "token" : "token"
              } ],
              "logprob" : 5.637376656633329,
              "bytes" : [ 2, 2 ],
              "token" : "token"
            } ]
          }
        } ],
        "system_fingerprint" : "system_fingerprint",
        "object" : "chat.completion"
      } ],
      "last_id" : "last_id",
      "has_more" : true,
      "object" : "list"
    }

### Produces

This API call produces the following media types according to the Accept request header; the media type will be conveyed by the Content-Type response header.

*   `application/json`

### Responses

#### 200

A list of Chat Completions [ChatCompletionList](#ChatCompletionList)

* * *

[Up](#__Methods)

    post /chat/completions/{completion_id}

Modify a stored chat completion. Only Chat Completions that have been created with the `store` parameter set to `true` can be modified. Currently, the only supported modification is to update the `metadata` field. (updateChatCompletion)

### Path parameters

completion\_id (required)

Path Parameter — The ID of the chat completion to update. default: null

### Consumes

This API call consumes the following media types via the Content-Type request header:

*   `application/json`

### Request body

updateChatCompletion\_request [updateChatCompletion\_request](#updateChatCompletion_request) (required)

Body Parameter —

### Return type

[CreateChatCompletionResponse](#CreateChatCompletionResponse)

### Example data

Content-Type: application/json

    {
      "created" : 3,
      "usage" : {
        "completion_tokens" : 2,
        "prompt_tokens" : 4,
        "completion_tokens_details" : {
          "accepted_prediction_tokens" : 1,
          "audio_tokens" : 1,
          "reasoning_tokens" : 1,
          "rejected_prediction_tokens" : 6
        },
        "prompt_tokens_details" : {
          "audio_tokens" : 7,
          "cached_tokens" : 1
        },
        "total_tokens" : 7
      },
      "model" : "model",
      "service_tier" : "auto",
      "id" : "id",
      "choices" : [ {
        "finish_reason" : "stop",
        "index" : 0,
        "message" : {
          "role" : "assistant",
          "function_call" : {
            "name" : "name",
            "arguments" : "arguments"
          },
          "refusal" : "refusal",
          "annotations" : [ {
            "type" : "url_citation",
            "url_citation" : {
              "start_index" : 1,
              "end_index" : 6,
              "title" : "title",
              "url" : "url"
            }
          }, {
            "type" : "url_citation",
            "url_citation" : {
              "start_index" : 1,
              "end_index" : 6,
              "title" : "title",
              "url" : "url"
            }
          } ],
          "tool_calls" : [ {
            "function" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "id" : "id",
            "type" : "function"
          }, {
            "function" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "id" : "id",
            "type" : "function"
          } ],
          "audio" : {
            "expires_at" : 5,
            "transcript" : "transcript",
            "data" : "data",
            "id" : "id"
          },
          "content" : "content"
        },
        "logprobs" : {
          "refusal" : [ {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          }, {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          } ],
          "content" : [ {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          }, {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          } ]
        }
      }, {
        "finish_reason" : "stop",
        "index" : 0,
        "message" : {
          "role" : "assistant",
          "function_call" : {
            "name" : "name",
            "arguments" : "arguments"
          },
          "refusal" : "refusal",
          "annotations" : [ {
            "type" : "url_citation",
            "url_citation" : {
              "start_index" : 1,
              "end_index" : 6,
              "title" : "title",
              "url" : "url"
            }
          }, {
            "type" : "url_citation",
            "url_citation" : {
              "start_index" : 1,
              "end_index" : 6,
              "title" : "title",
              "url" : "url"
            }
          } ],
          "tool_calls" : [ {
            "function" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "id" : "id",
            "type" : "function"
          }, {
            "function" : {
              "name" : "name",
              "arguments" : "arguments"
            },
            "id" : "id",
            "type" : "function"
          } ],
          "audio" : {
            "expires_at" : 5,
            "transcript" : "transcript",
            "data" : "data",
            "id" : "id"
          },
          "content" : "content"
        },
        "logprobs" : {
          "refusal" : [ {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          }, {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          } ],
          "content" : [ {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          }, {
            "top_logprobs" : [ {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            }, {
              "logprob" : 7.061401241503109,
              "bytes" : [ 9, 9 ],
              "token" : "token"
            } ],
            "logprob" : 5.637376656633329,
            "bytes" : [ 2, 2 ],
            "token" : "token"
          } ]
        }
      } ],
      "system_fingerprint" : "system_fingerprint",
      "object" : "chat.completion"
    }

### Produces

This API call produces the following media types according to the Accept request header; the media type will be conveyed by the Content-Type response header.

*   `application/json`

### Responses

#### 200

A chat completion [CreateChatCompletionResponse](#CreateChatCompletionResponse)

* * *

Completions
===========

[Up](#__Methods)

    post /completions

Creates a completion for the provided prompt and parameters. (createCompletion)

### Consumes

This API call consumes the following media types via the Content-Type request header:

*   `application/json`

### Request body

CreateCompletionRequest [CreateCompletionRequest](#CreateCompletionRequest) (required)

Body Parameter —

### Return type

[CreateCompletionResponse](#CreateCompletionResponse)

### Example data

Content-Type: application/json

    {
      "created" : 5,
      "usage" : {
        "completion_tokens" : 2,
        "prompt_tokens" : 4,
        "completion_tokens_details" : {
          "accepted_prediction_tokens" : 1,
          "audio_tokens" : 1,
          "reasoning_tokens" : 1,
          "rejected_prediction_tokens" : 6
        },
        "prompt_tokens_details" : {
          "audio_tokens" : 7,
          "cached_tokens" : 1
        },
        "total_tokens" : 7
      },
      "model" : "model",
      "id" : "id",
      "choices" : [ {
        "finish_reason" : "stop",
        "index" : 0,
        "text" : "text",
        "logprobs" : {
          "top_logprobs" : [ {
            "key" : 5.962133916683182
          }, {
            "key" : 5.962133916683182
          } ],
          "token_logprobs" : [ 1.4658129805029452, 1.4658129805029452 ],
          "tokens" : [ "tokens", "tokens" ],
          "text_offset" : [ 6, 6 ]
        }
      }, {
        "finish_reason" : "stop",
        "index" : 0,
        "text" : "text",
        "logprobs" : {
          "top_logprobs" : [ {
            "key" : 5.962133916683182
          }, {
            "key" : 5.962133916683182
          } ],
          "token_logprobs" : [ 1.4658129805029452, 1.4658129805029452 ],
          "tokens" : [ "tokens", "tokens" ],
          "text_offset" : [ 6, 6 ]
        }
      } ],
      "system_fingerprint" : "system_fingerprint",
      "object" : "text_completion"
    }

### Produces

This API call produces the following media types according to the Accept request header; the media type will be conveyed by the Content-Type response header.

*   `application/json`

### Responses

#### 200

OK [CreateCompletionResponse](#CreateCompletionResponse)

* * *

Models
======

[Up](#__Methods)

    delete /models/{model}

Delete a fine-tuned model. You must have the Owner role in your organization to delete a model. (deleteModel)

### Path parameters

model (required)

Path Parameter — The model to delete default: null

### Return type

[DeleteModelResponse](#DeleteModelResponse)

### Example data

Content-Type: application/json

    {
      "deleted" : true,
      "id" : "id",
      "object" : "object"
    }

### Produces

This API call produces the following media types according to the Accept request header; the media type will be conveyed by the Content-Type response header.

*   `application/json`

### Responses

#### 200

OK [DeleteModelResponse](#DeleteModelResponse)

* * *

[Up](#__Methods)

    get /models

Lists the currently available models, and provides basic information about each one such as the owner and availability. (listModels)

### Return type

[ListModelsResponse](#ListModelsResponse)

### Example data

Content-Type: application/json

    {
      "data" : [ {
        "created" : 0,
        "owned_by" : "owned_by",
        "id" : "id",
        "object" : "model"
      }, {
        "created" : 0,
        "owned_by" : "owned_by",
        "id" : "id",
        "object" : "model"
      } ],
      "object" : "list"
    }

### Produces

This API call produces the following media types according to the Accept request header; the media type will be conveyed by the Content-Type response header.

*   `application/json`

### Responses

#### 200

OK [ListModelsResponse](#ListModelsResponse)

* * *

[Up](#__Methods)

    get /models/{model}

Retrieves a model instance, providing basic information about the model such as the owner and permissioning. (retrieveModel)

### Path parameters

model (required)

Path Parameter — The ID of the model to use for this request default: null

### Return type

[Model](#Model)

### Example data

Content-Type: application/json

    {
      "created" : 0,
      "owned_by" : "owned_by",
      "id" : "id",
      "object" : "model"
    }

### Produces

This API call produces the following media types according to the Accept request header; the media type will be conveyed by the Content-Type response header.

*   `application/json`

### Responses

#### 200

OK [Model](#Model)

* * *

Models
------

\[ Jump to [Methods](#__Methods) \]

### Table of Contents

1.  [`ChatCompletionDeleted` -](#ChatCompletionDeleted)
2.  [`ChatCompletionFunctionCallOption` -](#ChatCompletionFunctionCallOption)
3.  [`ChatCompletionFunctions` -](#ChatCompletionFunctions)
4.  [`ChatCompletionList` - ChatCompletionList](#ChatCompletionList)
5.  [`ChatCompletionMessageList` - ChatCompletionMessageList](#ChatCompletionMessageList)
6.  [`ChatCompletionMessageList_data_inner` -](#ChatCompletionMessageList_data_inner)
7.  [`ChatCompletionMessageToolCall` -](#ChatCompletionMessageToolCall)
8.  [`ChatCompletionMessageToolCallChunk` -](#ChatCompletionMessageToolCallChunk)
9.  [`ChatCompletionMessageToolCallChunk_function` -](#ChatCompletionMessageToolCallChunk_function)
10.  [`ChatCompletionMessageToolCall_function` -](#ChatCompletionMessageToolCall_function)
11.  [`ChatCompletionNamedToolChoice` -](#ChatCompletionNamedToolChoice)
12.  [`ChatCompletionNamedToolChoice_function` -](#ChatCompletionNamedToolChoice_function)
13.  [`ChatCompletionRequestAssistantMessage` - Assistant message](#ChatCompletionRequestAssistantMessage)
14.  [`ChatCompletionRequestAssistantMessageContentPart` -](#ChatCompletionRequestAssistantMessageContentPart)
15.  [`ChatCompletionRequestAssistantMessage_audio` -](#ChatCompletionRequestAssistantMessage_audio)
16.  [`ChatCompletionRequestAssistantMessage_content` -](#ChatCompletionRequestAssistantMessage_content)
17.  [`ChatCompletionRequestAssistantMessage_function_call` -](#ChatCompletionRequestAssistantMessage_function_call)
18.  [`ChatCompletionRequestDeveloperMessage` - Developer message](#ChatCompletionRequestDeveloperMessage)
19.  [`ChatCompletionRequestDeveloperMessage_content` -](#ChatCompletionRequestDeveloperMessage_content)
20.  [`ChatCompletionRequestFunctionMessage` - Function message](#ChatCompletionRequestFunctionMessage)
21.  [`ChatCompletionRequestMessage` -](#ChatCompletionRequestMessage)
22.  [`ChatCompletionRequestMessageContentPartAudio` - Audio content part](#ChatCompletionRequestMessageContentPartAudio)
23.  [`ChatCompletionRequestMessageContentPartAudio_input_audio` -](#ChatCompletionRequestMessageContentPartAudio_input_audio)
24.  [`ChatCompletionRequestMessageContentPartFile` - File content part](#ChatCompletionRequestMessageContentPartFile)
25.  [`ChatCompletionRequestMessageContentPartFile_file` -](#ChatCompletionRequestMessageContentPartFile_file)
26.  [`ChatCompletionRequestMessageContentPartImage` - Image content part](#ChatCompletionRequestMessageContentPartImage)
27.  [`ChatCompletionRequestMessageContentPartImage_image_url` -](#ChatCompletionRequestMessageContentPartImage_image_url)
28.  [`ChatCompletionRequestMessageContentPartRefusal` - Refusal content part](#ChatCompletionRequestMessageContentPartRefusal)
29.  [`ChatCompletionRequestMessageContentPartText` - Text content part](#ChatCompletionRequestMessageContentPartText)
30.  [`ChatCompletionRequestSystemMessage` - System message](#ChatCompletionRequestSystemMessage)
31.  [`ChatCompletionRequestSystemMessage_content` -](#ChatCompletionRequestSystemMessage_content)
32.  [`ChatCompletionRequestToolMessage` - Tool message](#ChatCompletionRequestToolMessage)
33.  [`ChatCompletionRequestToolMessage_content` -](#ChatCompletionRequestToolMessage_content)
34.  [`ChatCompletionRequestUserMessage` - User message](#ChatCompletionRequestUserMessage)
35.  [`ChatCompletionRequestUserMessageContentPart` -](#ChatCompletionRequestUserMessageContentPart)
36.  [`ChatCompletionRequestUserMessage_content` -](#ChatCompletionRequestUserMessage_content)
37.  [`ChatCompletionResponseMessage` -](#ChatCompletionResponseMessage)
38.  [`ChatCompletionResponseMessage_annotations_inner` -](#ChatCompletionResponseMessage_annotations_inner)
39.  [`ChatCompletionResponseMessage_annotations_inner_url_citation` -](#ChatCompletionResponseMessage_annotations_inner_url_citation)
40.  [`ChatCompletionResponseMessage_audio` -](#ChatCompletionResponseMessage_audio)
41.  [`ChatCompletionResponseMessage_function_call` -](#ChatCompletionResponseMessage_function_call)
42.  [`ChatCompletionStreamOptions` -](#ChatCompletionStreamOptions)
43.  [`ChatCompletionStreamResponseDelta` -](#ChatCompletionStreamResponseDelta)
44.  [`ChatCompletionStreamResponseDelta_function_call` -](#ChatCompletionStreamResponseDelta_function_call)
45.  [`ChatCompletionTokenLogprob` -](#ChatCompletionTokenLogprob)
46.  [`ChatCompletionTokenLogprob_top_logprobs_inner` -](#ChatCompletionTokenLogprob_top_logprobs_inner)
47.  [`ChatCompletionTool` -](#ChatCompletionTool)
48.  [`ChatCompletionToolChoiceOption` -](#ChatCompletionToolChoiceOption)
49.  [`CompletionUsage` -](#CompletionUsage)
50.  [`CompletionUsage_completion_tokens_details` -](#CompletionUsage_completion_tokens_details)
51.  [`CompletionUsage_prompt_tokens_details` -](#CompletionUsage_prompt_tokens_details)
52.  [`CreateChatCompletionRequest` -](#CreateChatCompletionRequest)
53.  [`CreateChatCompletionRequest_allOf_audio` -](#CreateChatCompletionRequest_allOf_audio)
54.  [`CreateChatCompletionRequest_allOf_function_call` -](#CreateChatCompletionRequest_allOf_function_call)
55.  [`CreateChatCompletionRequest_allOf_response_format` -](#CreateChatCompletionRequest_allOf_response_format)
56.  [`CreateChatCompletionResponse` -](#CreateChatCompletionResponse)
57.  [`CreateChatCompletionResponse_choices_inner` -](#CreateChatCompletionResponse_choices_inner)
58.  [`CreateChatCompletionResponse_choices_inner_logprobs` -](#CreateChatCompletionResponse_choices_inner_logprobs)
59.  [`CreateChatCompletionStreamResponse` -](#CreateChatCompletionStreamResponse)
60.  [`CreateChatCompletionStreamResponse_choices_inner` -](#CreateChatCompletionStreamResponse_choices_inner)
61.  [`CreateCompletionRequest` -](#CreateCompletionRequest)
62.  [`CreateCompletionRequest_model` -](#CreateCompletionRequest_model)
63.  [`CreateCompletionRequest_prompt` -](#CreateCompletionRequest_prompt)
64.  [`CreateCompletionResponse` -](#CreateCompletionResponse)
65.  [`CreateCompletionResponse_choices_inner` -](#CreateCompletionResponse_choices_inner)
66.  [`CreateCompletionResponse_choices_inner_logprobs` -](#CreateCompletionResponse_choices_inner_logprobs)
67.  [`CreateModelResponseProperties` -](#CreateModelResponseProperties)
68.  [`DeleteModelResponse` -](#DeleteModelResponse)
69.  [`FunctionObject` -](#FunctionObject)
70.  [`JSON_schema` - JSON schema](#JSON_schema)
71.  [`ListModelsResponse` -](#ListModelsResponse)
72.  [`Model` - Model](#Model)
73.  [`ModelIdsShared` -](#ModelIdsShared)
74.  [`ModelResponseProperties` -](#ModelResponseProperties)
75.  [`PredictionContent` - Static Content](#PredictionContent)
76.  [`PredictionContent_content` -](#PredictionContent_content)
77.  [`ReasoningEffort` -](#ReasoningEffort)
78.  [`ResponseFormatJsonObject` - JSON object](#ResponseFormatJsonObject)
79.  [`ResponseFormatJsonSchema` - JSON schema](#ResponseFormatJsonSchema)
80.  [`ResponseFormatText` - Text](#ResponseFormatText)
81.  [`ServiceTier` -](#ServiceTier)
82.  [`StopConfiguration` -](#StopConfiguration)
83.  [`VoiceIdsShared` -](#VoiceIdsShared)
84.  [`WebSearchContextSize` -](#WebSearchContextSize)
85.  [`WebSearchLocation` - Web search location](#WebSearchLocation)
86.  [`Web_search` - Web search](#Web_search)
87.  [`Web_search_user_location` -](#Web_search_user_location)
88.  [`updateChatCompletion_request` -](#updateChatCompletion_request)

### `ChatCompletionDeleted` - [Up](#__Models)

object

[String](#string) The type of object being deleted.

Enum:

chat.completion.deleted

id

[String](#string) The ID of the chat completion that was deleted.

deleted

[Boolean](#boolean) Whether the chat completion was deleted.

### `ChatCompletionFunctionCallOption` - [Up](#__Models)

Specifying a particular function via `{"name": "my_function"}` forces the model to call that function.

name

[String](#string) The name of the function to call.

### `ChatCompletionFunctions` - [Up](#__Models)

description (optional)

[String](#string) A description of what the function does, used by the model to choose when and how to call the function.

name

[String](#string) The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.

parameters (optional)

[map\[String, oas\_any\_type\_not\_mapped\]](#AnyType)

The parameters the functions accepts, described as a JSON Schema object. See the [guide](/docs/guides/function-calling) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.

Omitting `parameters` defines a function with an empty parameter list.

### `ChatCompletionList` - ChatCompletionList [Up](#__Models)

An object representing a list of Chat Completions.

object

[String](#string) The type of this object. It is always set to "list".

Enum:

list

data

[array\[CreateChatCompletionResponse\]](#CreateChatCompletionResponse) An array of chat completion objects.

first\_id

[String](#string) The identifier of the first chat completion in the data array.

last\_id

[String](#string) The identifier of the last chat completion in the data array.

has\_more

[Boolean](#boolean) Indicates whether there are more Chat Completions available.

### `ChatCompletionMessageList` - ChatCompletionMessageList [Up](#__Models)

An object representing a list of chat completion messages.

object

[String](#string) The type of this object. It is always set to "list".

Enum:

list

data

[array\[ChatCompletionMessageList\_data\_inner\]](#ChatCompletionMessageList_data_inner) An array of chat completion message objects.

first\_id

[String](#string) The identifier of the first chat message in the data array.

last\_id

[String](#string) The identifier of the last chat message in the data array.

has\_more

[Boolean](#boolean) Indicates whether there are more chat messages available.

### `ChatCompletionMessageList_data_inner` - [Up](#__Models)

content

[String](#string) The contents of the message.

refusal

[String](#string) The refusal message generated by the model.

tool\_calls (optional)

[array\[ChatCompletionMessageToolCall\]](#ChatCompletionMessageToolCall) The tool calls generated by the model, such as function calls.

annotations (optional)

[array\[ChatCompletionResponseMessage\_annotations\_inner\]](#ChatCompletionResponseMessage_annotations_inner) Annotations for the message, when applicable, as when using the [web search tool](/docs/guides/tools-web-search?api-mode=chat).

role

[String](#string) The role of the author of this message.

Enum:

assistant

function\_call (optional)

[ChatCompletionResponseMessage\_function\_call](#ChatCompletionResponseMessage_function_call)

audio (optional)

[ChatCompletionResponseMessage\_audio](#ChatCompletionResponseMessage_audio)

id

[String](#string) The identifier of the chat message.

### `ChatCompletionMessageToolCall` - [Up](#__Models)

id

[String](#string) The ID of the tool call.

type

[String](#string) The type of the tool. Currently, only `function` is supported.

Enum:

function

function

[ChatCompletionMessageToolCall\_function](#ChatCompletionMessageToolCall_function)

### `ChatCompletionMessageToolCallChunk` - [Up](#__Models)

index

[Integer](#integer)

id (optional)

[String](#string) The ID of the tool call.

type (optional)

[String](#string) The type of the tool. Currently, only `function` is supported.

Enum:

function

function (optional)

[ChatCompletionMessageToolCallChunk\_function](#ChatCompletionMessageToolCallChunk_function)

### `ChatCompletionMessageToolCallChunk_function` - [Up](#__Models)

name (optional)

[String](#string) The name of the function to call.

arguments (optional)

[String](#string) The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function.

### `ChatCompletionMessageToolCall_function` - [Up](#__Models)

The function that the model called.

name

[String](#string) The name of the function to call.

arguments

[String](#string) The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function.

### `ChatCompletionNamedToolChoice` - [Up](#__Models)

Specifies a tool the model should use. Use to force the model to call a specific function.

type

[String](#string) The type of the tool. Currently, only `function` is supported.

Enum:

function

function

[ChatCompletionNamedToolChoice\_function](#ChatCompletionNamedToolChoice_function)

### `ChatCompletionNamedToolChoice_function` - [Up](#__Models)

name

[String](#string) The name of the function to call.

### `ChatCompletionRequestAssistantMessage` - Assistant message [Up](#__Models)

Messages sent by the model in response to user messages.

content (optional)

[ChatCompletionRequestAssistantMessage\_content](#ChatCompletionRequestAssistantMessage_content)

refusal (optional)

[String](#string) The refusal message by the assistant.

role

[String](#string) The role of the messages author, in this case `assistant`.

Enum:

assistant

name (optional)

[String](#string) An optional name for the participant. Provides the model information to differentiate between participants of the same role.

audio (optional)

[ChatCompletionRequestAssistantMessage\_audio](#ChatCompletionRequestAssistantMessage_audio)

tool\_calls (optional)

[array\[ChatCompletionMessageToolCall\]](#ChatCompletionMessageToolCall) The tool calls generated by the model, such as function calls.

function\_call (optional)

[ChatCompletionRequestAssistantMessage\_function\_call](#ChatCompletionRequestAssistantMessage_function_call)

### `ChatCompletionRequestAssistantMessageContentPart` - [Up](#__Models)

type

[String](#string) The type of the content part.

Enum:

text

refusal

text

[String](#string) The text content.

refusal

[String](#string) The refusal message generated by the model.

### `ChatCompletionRequestAssistantMessage_audio` - [Up](#__Models)

Data about a previous audio response from the model. [Learn more](/docs/guides/audio).

id

[String](#string) Unique identifier for a previous audio response from the model.

### `ChatCompletionRequestAssistantMessage_content` - [Up](#__Models)

The contents of the assistant message. Required unless `tool_calls` or `function_call` is specified.

### `ChatCompletionRequestAssistantMessage_function_call` - [Up](#__Models)

Deprecated and replaced by `tool_calls`. The name and arguments of a function that should be called, as generated by the model.

arguments

[String](#string) The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function.

name

[String](#string) The name of the function to call.

### `ChatCompletionRequestDeveloperMessage` - Developer message [Up](#__Models)

Developer-provided instructions that the model should follow, regardless of messages sent by the user. With o1 models and newer, `developer` messages replace the previous `system` messages.

content

[ChatCompletionRequestDeveloperMessage\_content](#ChatCompletionRequestDeveloperMessage_content)

role

[String](#string) The role of the messages author, in this case `developer`.

Enum:

developer

name (optional)

[String](#string) An optional name for the participant. Provides the model information to differentiate between participants of the same role.

### `ChatCompletionRequestDeveloperMessage_content` - [Up](#__Models)

The contents of the developer message.

### `ChatCompletionRequestFunctionMessage` - Function message [Up](#__Models)

role

[String](#string) The role of the messages author, in this case `function`.

Enum:

function

content

[String](#string) The contents of the function message.

name

[String](#string) The name of the function to call.

### `ChatCompletionRequestMessage` - [Up](#__Models)

content

[String](#string) The contents of the function message.

role

[String](#string) The role of the messages author, in this case `function`.

Enum:

function

name

[String](#string) The name of the function to call.

refusal (optional)

[String](#string) The refusal message by the assistant.

audio (optional)

[ChatCompletionRequestAssistantMessage\_audio](#ChatCompletionRequestAssistantMessage_audio)

tool\_calls (optional)

[array\[ChatCompletionMessageToolCall\]](#ChatCompletionMessageToolCall) The tool calls generated by the model, such as function calls.

function\_call (optional)

[ChatCompletionRequestAssistantMessage\_function\_call](#ChatCompletionRequestAssistantMessage_function_call)

tool\_call\_id

[String](#string) Tool call that this message is responding to.

### `ChatCompletionRequestMessageContentPartAudio` - Audio content part [Up](#__Models)

Learn about [audio inputs](/docs/guides/audio).

type

[String](#string) The type of the content part. Always `input_audio`.

Enum:

input\_audio

input\_audio

[ChatCompletionRequestMessageContentPartAudio\_input\_audio](#ChatCompletionRequestMessageContentPartAudio_input_audio)

### `ChatCompletionRequestMessageContentPartAudio_input_audio` - [Up](#__Models)

data

[String](#string) Base64 encoded audio data.

format

[String](#string) The format of the encoded audio data. Currently supports "wav" and "mp3".

Enum:

wav

mp3

### `ChatCompletionRequestMessageContentPartFile` - File content part [Up](#__Models)

Learn about [file inputs](/docs/guides/text) for text generation.

type

[String](#string) The type of the content part. Always `file`.

Enum:

file

file

[ChatCompletionRequestMessageContentPartFile\_file](#ChatCompletionRequestMessageContentPartFile_file)

### `ChatCompletionRequestMessageContentPartFile_file` - [Up](#__Models)

filename (optional)

[String](#string) The name of the file, used when passing the file to the model as a string.

file\_data (optional)

[String](#string) The base64 encoded file data, used when passing the file to the model as a string.

file\_id (optional)

[String](#string) The ID of an uploaded file to use as input.

### `ChatCompletionRequestMessageContentPartImage` - Image content part [Up](#__Models)

Learn about [image inputs](/docs/guides/vision).

type

[String](#string) The type of the content part.

Enum:

image\_url

image\_url

[ChatCompletionRequestMessageContentPartImage\_image\_url](#ChatCompletionRequestMessageContentPartImage_image_url)

### `ChatCompletionRequestMessageContentPartImage_image_url` - [Up](#__Models)

url

[URI](#URI) Either a URL of the image or the base64 encoded image data. format: uri

detail (optional)

[String](#string) Specifies the detail level of the image. Learn more in the [Vision guide](/docs/guides/vision#low-or-high-fidelity-image-understanding).

Enum:

auto

low

high

### `ChatCompletionRequestMessageContentPartRefusal` - Refusal content part [Up](#__Models)

type

[String](#string) The type of the content part.

Enum:

refusal

refusal

[String](#string) The refusal message generated by the model.

### `ChatCompletionRequestMessageContentPartText` - Text content part [Up](#__Models)

Learn about [text inputs](/docs/guides/text-generation).

type

[String](#string) The type of the content part.

Enum:

text

text

[String](#string) The text content.

### `ChatCompletionRequestSystemMessage` - System message [Up](#__Models)

Developer-provided instructions that the model should follow, regardless of messages sent by the user. With o1 models and newer, use `developer` messages for this purpose instead.

content

[ChatCompletionRequestSystemMessage\_content](#ChatCompletionRequestSystemMessage_content)

role

[String](#string) The role of the messages author, in this case `system`.

Enum:

system

name (optional)

[String](#string) An optional name for the participant. Provides the model information to differentiate between participants of the same role.

### `ChatCompletionRequestSystemMessage_content` - [Up](#__Models)

The contents of the system message.

### `ChatCompletionRequestToolMessage` - Tool message [Up](#__Models)

role

[String](#string) The role of the messages author, in this case `tool`.

Enum:

tool

content

[ChatCompletionRequestToolMessage\_content](#ChatCompletionRequestToolMessage_content)

tool\_call\_id

[String](#string) Tool call that this message is responding to.

### `ChatCompletionRequestToolMessage_content` - [Up](#__Models)

The contents of the tool message.

### `ChatCompletionRequestUserMessage` - User message [Up](#__Models)

Messages sent by an end user, containing prompts or additional context information.

content

[ChatCompletionRequestUserMessage\_content](#ChatCompletionRequestUserMessage_content)

role

[String](#string) The role of the messages author, in this case `user`.

Enum:

user

name (optional)

[String](#string) An optional name for the participant. Provides the model information to differentiate between participants of the same role.

### `ChatCompletionRequestUserMessageContentPart` - [Up](#__Models)

type

[String](#string) The type of the content part.

Enum:

text

image\_url

input\_audio

file

text

[String](#string) The text content.

image\_url

[ChatCompletionRequestMessageContentPartImage\_image\_url](#ChatCompletionRequestMessageContentPartImage_image_url)

input\_audio

[ChatCompletionRequestMessageContentPartAudio\_input\_audio](#ChatCompletionRequestMessageContentPartAudio_input_audio)

file

[ChatCompletionRequestMessageContentPartFile\_file](#ChatCompletionRequestMessageContentPartFile_file)

### `ChatCompletionRequestUserMessage_content` - [Up](#__Models)

The contents of the user message.

### `ChatCompletionResponseMessage` - [Up](#__Models)

A chat completion message generated by the model.

content

[String](#string) The contents of the message.

refusal

[String](#string) The refusal message generated by the model.

tool\_calls (optional)

[array\[ChatCompletionMessageToolCall\]](#ChatCompletionMessageToolCall) The tool calls generated by the model, such as function calls.

annotations (optional)

[array\[ChatCompletionResponseMessage\_annotations\_inner\]](#ChatCompletionResponseMessage_annotations_inner) Annotations for the message, when applicable, as when using the [web search tool](/docs/guides/tools-web-search?api-mode=chat).

role

[String](#string) The role of the author of this message.

Enum:

assistant

function\_call (optional)

[ChatCompletionResponseMessage\_function\_call](#ChatCompletionResponseMessage_function_call)

audio (optional)

[ChatCompletionResponseMessage\_audio](#ChatCompletionResponseMessage_audio)

### `ChatCompletionResponseMessage_annotations_inner` - [Up](#__Models)

A URL citation when using web search.

type

[String](#string) The type of the URL citation. Always `url_citation`.

Enum:

url\_citation

url\_citation

[ChatCompletionResponseMessage\_annotations\_inner\_url\_citation](#ChatCompletionResponseMessage_annotations_inner_url_citation)

### `ChatCompletionResponseMessage_annotations_inner_url_citation` - [Up](#__Models)

A URL citation when using web search.

end\_index

[Integer](#integer) The index of the last character of the URL citation in the message.

start\_index

[Integer](#integer) The index of the first character of the URL citation in the message.

url

[String](#string) The URL of the web resource.

title

[String](#string) The title of the web resource.

### `ChatCompletionResponseMessage_audio` - [Up](#__Models)

If the audio output modality is requested, this object contains data about the audio response from the model. [Learn more](/docs/guides/audio).

id

[String](#string) Unique identifier for this audio response.

expires\_at

[Integer](#integer) The Unix timestamp (in seconds) for when this audio response will no longer be accessible on the server for use in multi-turn conversations.

data

[String](#string) Base64 encoded audio bytes generated by the model, in the format specified in the request.

transcript

[String](#string) Transcript of the audio generated by the model.

### `ChatCompletionResponseMessage_function_call` - [Up](#__Models)

Deprecated and replaced by `tool_calls`. The name and arguments of a function that should be called, as generated by the model.

arguments

[String](#string) The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function.

name

[String](#string) The name of the function to call.

### `ChatCompletionStreamOptions` - [Up](#__Models)

Options for streaming response. Only set this when you set `stream: true`.

include\_usage (optional)

[Boolean](#boolean)

If set, an additional chunk will be streamed before the `data: [DONE]` message. The `usage` field on this chunk shows the token usage statistics for the entire request, and the `choices` field will always be an empty array.

All other chunks will also include a `usage` field, but with a null value. **NOTE:** If the stream is interrupted, you may not receive the final usage chunk which contains the total token usage for the request.

### `ChatCompletionStreamResponseDelta` - [Up](#__Models)

A chat completion delta generated by streamed model responses.

content (optional)

[String](#string) The contents of the chunk message.

function\_call (optional)

[ChatCompletionStreamResponseDelta\_function\_call](#ChatCompletionStreamResponseDelta_function_call)

tool\_calls (optional)

[array\[ChatCompletionMessageToolCallChunk\]](#ChatCompletionMessageToolCallChunk)

role (optional)

[String](#string) The role of the author of this message.

Enum:

developer

system

user

assistant

tool

refusal (optional)

[String](#string) The refusal message generated by the model.

### `ChatCompletionStreamResponseDelta_function_call` - [Up](#__Models)

Deprecated and replaced by `tool_calls`. The name and arguments of a function that should be called, as generated by the model.

arguments (optional)

[String](#string) The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function.

name (optional)

[String](#string) The name of the function to call.

### `ChatCompletionTokenLogprob` - [Up](#__Models)

token

[String](#string) The token.

logprob

[BigDecimal](#number) The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely.

bytes

[array\[Integer\]](#integer) A list of integers representing the UTF-8 bytes representation of the token. Useful in instances where characters are represented by multiple tokens and their byte representations must be combined to generate the correct text representation. Can be `null` if there is no bytes representation for the token.

top\_logprobs

[array\[ChatCompletionTokenLogprob\_top\_logprobs\_inner\]](#ChatCompletionTokenLogprob_top_logprobs_inner) List of the most likely tokens and their log probability, at this token position. In rare cases, there may be fewer than the number of requested `top_logprobs` returned.

### `ChatCompletionTokenLogprob_top_logprobs_inner` - [Up](#__Models)

token

[String](#string) The token.

logprob

[BigDecimal](#number) The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely.

bytes

[array\[Integer\]](#integer) A list of integers representing the UTF-8 bytes representation of the token. Useful in instances where characters are represented by multiple tokens and their byte representations must be combined to generate the correct text representation. Can be `null` if there is no bytes representation for the token.

### `ChatCompletionTool` - [Up](#__Models)

type

[String](#string) The type of the tool. Currently, only `function` is supported.

Enum:

function

function

[FunctionObject](#FunctionObject)

### `ChatCompletionToolChoiceOption` - [Up](#__Models)

Controls which (if any) tool is called by the model. `none` means the model will not call any tool and instead generates a message. `auto` means the model can pick between generating a message or calling one or more tools. `required` means the model must call one or more tools. Specifying a particular tool via `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool.

`none` is the default when no tools are present. `auto` is the default if tools are present.

type

[String](#string) The type of the tool. Currently, only `function` is supported.

Enum:

function

function

[ChatCompletionNamedToolChoice\_function](#ChatCompletionNamedToolChoice_function)

### `CompletionUsage` - [Up](#__Models)

Usage statistics for the completion request.

completion\_tokens

[Integer](#integer) Number of tokens in the generated completion.

prompt\_tokens

[Integer](#integer) Number of tokens in the prompt.

total\_tokens

[Integer](#integer) Total number of tokens used in the request (prompt + completion).

completion\_tokens\_details (optional)

[CompletionUsage\_completion\_tokens\_details](#CompletionUsage_completion_tokens_details)

prompt\_tokens\_details (optional)

[CompletionUsage\_prompt\_tokens\_details](#CompletionUsage_prompt_tokens_details)

### `CompletionUsage_completion_tokens_details` - [Up](#__Models)

Breakdown of tokens used in a completion.

accepted\_prediction\_tokens (optional)

[Integer](#integer) When using Predicted Outputs, the number of tokens in the prediction that appeared in the completion.

audio\_tokens (optional)

[Integer](#integer) Audio input tokens generated by the model.

reasoning\_tokens (optional)

[Integer](#integer) Tokens generated by the model for reasoning.

rejected\_prediction\_tokens (optional)

[Integer](#integer) When using Predicted Outputs, the number of tokens in the prediction that did not appear in the completion. However, like reasoning tokens, these tokens are still counted in the total completion tokens for purposes of billing, output, and context window limits.

### `CompletionUsage_prompt_tokens_details` - [Up](#__Models)

Breakdown of tokens used in the prompt.

audio\_tokens (optional)

[Integer](#integer) Audio input tokens present in the prompt.

cached\_tokens (optional)

[Integer](#integer) Cached tokens present in the prompt.

### `CreateChatCompletionRequest` - [Up](#__Models)

metadata (optional)

[map\[String, String\]](#string)

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

temperature (optional)

[BigDecimal](#number) What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.

top\_p (optional)

[BigDecimal](#number)

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top\_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or `temperature` but not both.

user (optional)

[String](#string) A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. [Learn more](/docs/guides/safety-best-practices#end-user-ids).

service\_tier (optional)

[ServiceTier](#ServiceTier)

messages

[array\[ChatCompletionRequestMessage\]](#ChatCompletionRequestMessage) A list of messages comprising the conversation so far. Depending on the [model](/docs/models) you use, different message types (modalities) are supported, like [text](/docs/guides/text-generation), [images](/docs/guides/vision), and [audio](/docs/guides/audio).

model

[ModelIdsShared](#ModelIdsShared)

modalities (optional)

[array\[String\]](#string)

Output types that you would like the model to generate. Most models are capable of generating text, which is the default:

`["text"]`

The `gpt-4o-audio-preview` model can also be used to [generate audio](/docs/guides/audio). To request that this model generate both text and audio responses, you can use:

`["text", "audio"]`

Enum:

reasoning\_effort (optional)

[ReasoningEffort](#ReasoningEffort)

max\_completion\_tokens (optional)

[Integer](#integer) An upper bound for the number of tokens that can be generated for a completion, including visible output tokens and [reasoning tokens](/docs/guides/reasoning).

frequency\_penalty (optional)

[BigDecimal](#number) Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.

presence\_penalty (optional)

[BigDecimal](#number) Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.

web\_search\_options (optional)

[Web\_search](#Web_search)

top\_logprobs (optional)

[Integer](#integer) An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. `logprobs` must be set to `true` if this parameter is used.

response\_format (optional)

[CreateChatCompletionRequest\_allOf\_response\_format](#CreateChatCompletionRequest_allOf_response_format)

audio (optional)

[CreateChatCompletionRequest\_allOf\_audio](#CreateChatCompletionRequest_allOf_audio)

store (optional)

[Boolean](#boolean) Whether or not to store the output of this chat completion request for use in our [model distillation](/docs/guides/distillation) or [evals](/docs/guides/evals) products.

stream (optional)

[Boolean](#boolean) If set to true, the model response data will be streamed to the client as it is generated using [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format). See the [Streaming section below](/docs/api-reference/chat/streaming) for more information, along with the [streaming responses](/docs/guides/streaming-responses) guide for more information on how to handle the streaming events.

stop (optional)

[StopConfiguration](#StopConfiguration)

logit\_bias (optional)

[map\[String, Integer\]](#integer)

Modify the likelihood of specified tokens appearing in the completion.

Accepts a JSON object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.

logprobs (optional)

[Boolean](#boolean) Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the `content` of `message`.

max\_tokens (optional)

[Integer](#integer)

The maximum number of [tokens](/tokenizer) that can be generated in the chat completion. This value can be used to control [costs](https://openai.com/api/pricing/) for text generated via API.

This value is now deprecated in favor of `max_completion_tokens`, and is not compatible with [o-series models](/docs/guides/reasoning).

n (optional)

[Integer](#integer) How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep `n` as `1` to minimize costs.

prediction (optional)

[PredictionContent](#PredictionContent)

seed (optional)

[Integer](#integer) This feature is in Beta. If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result. Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend.

stream\_options (optional)

[ChatCompletionStreamOptions](#ChatCompletionStreamOptions)

tools (optional)

[array\[ChatCompletionTool\]](#ChatCompletionTool) A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for. A max of 128 functions are supported.

tool\_choice (optional)

[ChatCompletionToolChoiceOption](#ChatCompletionToolChoiceOption)

parallel\_tool\_calls (optional)

[Boolean](#boolean) Whether to enable [parallel function calling](/docs/guides/function-calling#configuring-parallel-function-calling) during tool use.

function\_call (optional)

[CreateChatCompletionRequest\_allOf\_function\_call](#CreateChatCompletionRequest_allOf_function_call)

functions (optional)

[array\[ChatCompletionFunctions\]](#ChatCompletionFunctions)

Deprecated in favor of `tools`.

A list of functions the model may generate JSON inputs for.

### `CreateChatCompletionRequest_allOf_audio` - [Up](#__Models)

Parameters for audio output. Required when audio output is requested with `modalities: ["audio"]`. [Learn more](/docs/guides/audio).

voice

[VoiceIdsShared](#VoiceIdsShared)

format

[String](#string) Specifies the output audio format. Must be one of `wav`, `mp3`, `flac`, `opus`, or `pcm16`.

Enum:

wav

aac

mp3

flac

opus

pcm16

### `CreateChatCompletionRequest_allOf_function_call` - [Up](#__Models)

Deprecated in favor of `tool_choice`.

Controls which (if any) function is called by the model.

`none` means the model will not call a function and instead generates a message.

`auto` means the model can pick between generating a message or calling a function.

Specifying a particular function via `{"name": "my_function"}` forces the model to call that function.

`none` is the default when no functions are present. `auto` is the default if functions are present.

name

[String](#string) The name of the function to call.

### `CreateChatCompletionRequest_allOf_response_format` - [Up](#__Models)

An object specifying the format that the model must output.

Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs which ensures the model will match your supplied JSON schema. Learn more in the [Structured Outputs guide](/docs/guides/structured-outputs).

Setting to `{ "type": "json_object" }` enables the older JSON mode, which ensures the message the model generates is valid JSON. Using `json_schema` is preferred for models that support it.

type

[String](#string) The type of response format being defined. Always `text`.

Enum:

text

json\_schema

json\_object

json\_schema

[JSON\_schema](#JSON_schema)

### `CreateChatCompletionResponse` - [Up](#__Models)

Represents a chat completion response returned by model, based on the provided input.

id

[String](#string) A unique identifier for the chat completion.

choices

[array\[CreateChatCompletionResponse\_choices\_inner\]](#CreateChatCompletionResponse_choices_inner) A list of chat completion choices. Can be more than one if `n` is greater than 1.

created

[Integer](#integer) The Unix timestamp (in seconds) of when the chat completion was created.

model

[String](#string) The model used for the chat completion.

service\_tier (optional)

[ServiceTier](#ServiceTier)

system\_fingerprint (optional)

[String](#string)

This fingerprint represents the backend configuration that the model runs with.

Can be used in conjunction with the `seed` request parameter to understand when backend changes have been made that might impact determinism.

object

[String](#string) The object type, which is always `chat.completion`.

Enum:

chat.completion

usage (optional)

[CompletionUsage](#CompletionUsage)

### `CreateChatCompletionResponse_choices_inner` - [Up](#__Models)

finish\_reason

[String](#string) The reason the model stopped generating tokens. This will be `stop` if the model hit a natural stop point or a provided stop sequence, `length` if the maximum number of tokens specified in the request was reached, `content_filter` if content was omitted due to a flag from our content filters, `tool_calls` if the model called a tool, or `function_call` (deprecated) if the model called a function.

Enum:

stop

length

tool\_calls

content\_filter

function\_call

index

[Integer](#integer) The index of the choice in the list of choices.

message

[ChatCompletionResponseMessage](#ChatCompletionResponseMessage)

logprobs

[CreateChatCompletionResponse\_choices\_inner\_logprobs](#CreateChatCompletionResponse_choices_inner_logprobs)

### `CreateChatCompletionResponse_choices_inner_logprobs` - [Up](#__Models)

Log probability information for the choice.

content

[array\[ChatCompletionTokenLogprob\]](#ChatCompletionTokenLogprob) A list of message content tokens with log probability information.

refusal

[array\[ChatCompletionTokenLogprob\]](#ChatCompletionTokenLogprob) A list of message refusal tokens with log probability information.

### `CreateChatCompletionStreamResponse` - [Up](#__Models)

Represents a streamed chunk of a chat completion response returned by the model, based on the provided input. [Learn more](/docs/guides/streaming-responses).

id

[String](#string) A unique identifier for the chat completion. Each chunk has the same ID.

choices

[array\[CreateChatCompletionStreamResponse\_choices\_inner\]](#CreateChatCompletionStreamResponse_choices_inner) A list of chat completion choices. Can contain more than one elements if `n` is greater than 1. Can also be empty for the last chunk if you set `stream_options: {"include_usage": true}`.

created

[Integer](#integer) The Unix timestamp (in seconds) of when the chat completion was created. Each chunk has the same timestamp.

model

[String](#string) The model to generate the completion.

service\_tier (optional)

[ServiceTier](#ServiceTier)

system\_fingerprint (optional)

[String](#string) This fingerprint represents the backend configuration that the model runs with. Can be used in conjunction with the `seed` request parameter to understand when backend changes have been made that might impact determinism.

object

[String](#string) The object type, which is always `chat.completion.chunk`.

Enum:

chat.completion.chunk

usage (optional)

[CompletionUsage](#CompletionUsage)

### `CreateChatCompletionStreamResponse_choices_inner` - [Up](#__Models)

delta

[ChatCompletionStreamResponseDelta](#ChatCompletionStreamResponseDelta)

logprobs (optional)

[CreateChatCompletionResponse\_choices\_inner\_logprobs](#CreateChatCompletionResponse_choices_inner_logprobs)

finish\_reason

[String](#string) The reason the model stopped generating tokens. This will be `stop` if the model hit a natural stop point or a provided stop sequence, `length` if the maximum number of tokens specified in the request was reached, `content_filter` if content was omitted due to a flag from our content filters, `tool_calls` if the model called a tool, or `function_call` (deprecated) if the model called a function.

Enum:

stop

length

tool\_calls

content\_filter

function\_call

index

[Integer](#integer) The index of the choice in the list of choices.

### `CreateCompletionRequest` - [Up](#__Models)

model

[CreateCompletionRequest\_model](#CreateCompletionRequest_model)

prompt

[CreateCompletionRequest\_prompt](#CreateCompletionRequest_prompt)

best\_of (optional)

[Integer](#integer)

Generates `best_of` completions server-side and returns the "best" (the one with the highest log probability per token). Results cannot be streamed.

When used with `n`, `best_of` controls the number of candidate completions and `n` specifies how many to return – `best_of` must be greater than `n`.

**Note:** Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for `max_tokens` and `stop`.

echo (optional)

[Boolean](#boolean) Echo back the prompt in addition to the completion

frequency\_penalty (optional)

[BigDecimal](#number)

Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.

[See more information about frequency and presence penalties.](/docs/guides/text-generation)

logit\_bias (optional)

[map\[String, Integer\]](#integer)

Modify the likelihood of specified tokens appearing in the completion.

Accepts a JSON object that maps tokens (specified by their token ID in the GPT tokenizer) to an associated bias value from -100 to 100. You can use this [tokenizer tool](/tokenizer?view=bpe) to convert text to token IDs. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.

As an example, you can pass `{"50256": -100}` to prevent the <|endoftext|> token from being generated.

logprobs (optional)

[Integer](#integer)

Include the log probabilities on the `logprobs` most likely output tokens, as well the chosen tokens. For example, if `logprobs` is 5, the API will return a list of the 5 most likely tokens. The API will always return the `logprob` of the sampled token, so there may be up to `logprobs+1` elements in the response.

The maximum value for `logprobs` is 5.

max\_tokens (optional)

[Integer](#integer)

The maximum number of [tokens](/tokenizer) that can be generated in the completion.

The token count of your prompt plus `max_tokens` cannot exceed the model's context length. [Example Python code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken) for counting tokens.

n (optional)

[Integer](#integer)

How many completions to generate for each prompt.

**Note:** Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for `max_tokens` and `stop`.

presence\_penalty (optional)

[BigDecimal](#number)

Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.

[See more information about frequency and presence penalties.](/docs/guides/text-generation)

seed (optional)

[Long](#long)

If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.

Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend.

format: int64

stop (optional)

[StopConfiguration](#StopConfiguration)

stream (optional)

[Boolean](#boolean) Whether to stream back partial progress. If set, tokens will be sent as data-only [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format) as they become available, with the stream terminated by a `data: [DONE]` message. [Example Python code](https://cookbook.openai.com/examples/how_to_stream_completions).

stream\_options (optional)

[ChatCompletionStreamOptions](#ChatCompletionStreamOptions)

suffix (optional)

[String](#string)

The suffix that comes after a completion of inserted text.

This parameter is only supported for `gpt-3.5-turbo-instruct`.

temperature (optional)

[BigDecimal](#number)

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

We generally recommend altering this or `top_p` but not both.

top\_p (optional)

[BigDecimal](#number)

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top\_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or `temperature` but not both.

user (optional)

[String](#string) A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. [Learn more](/docs/guides/safety-best-practices#end-user-ids).

### `CreateCompletionRequest_model` - [Up](#__Models)

ID of the model to use. You can use the [List models](/docs/api-reference/models/list) API to see all of your available models, or see our [Model overview](/docs/models) for descriptions of them.

### `CreateCompletionRequest_prompt` - [Up](#__Models)

The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.

Note that <|endoftext|> is the document separator that the model sees during training, so if a prompt is not specified the model will generate as if from the beginning of a new document.

### `CreateCompletionResponse` - [Up](#__Models)

Represents a completion response from the API. Note: both the streamed and non-streamed response objects share the same shape (unlike the chat endpoint).

id

[String](#string) A unique identifier for the completion.

choices

[array\[CreateCompletionResponse\_choices\_inner\]](#CreateCompletionResponse_choices_inner) The list of completion choices the model generated for the input prompt.

created

[Integer](#integer) The Unix timestamp (in seconds) of when the completion was created.

model

[String](#string) The model used for completion.

system\_fingerprint (optional)

[String](#string)

This fingerprint represents the backend configuration that the model runs with.

Can be used in conjunction with the `seed` request parameter to understand when backend changes have been made that might impact determinism.

object

[String](#string) The object type, which is always "text\_completion"

Enum:

text\_completion

usage (optional)

[CompletionUsage](#CompletionUsage)

### `CreateCompletionResponse_choices_inner` - [Up](#__Models)

finish\_reason

[String](#string) The reason the model stopped generating tokens. This will be `stop` if the model hit a natural stop point or a provided stop sequence, `length` if the maximum number of tokens specified in the request was reached, or `content_filter` if content was omitted due to a flag from our content filters.

Enum:

stop

length

content\_filter

index

[Integer](#integer)

logprobs

[CreateCompletionResponse\_choices\_inner\_logprobs](#CreateCompletionResponse_choices_inner_logprobs)

text

[String](#string)

### `CreateCompletionResponse_choices_inner_logprobs` - [Up](#__Models)

text\_offset (optional)

[array\[Integer\]](#integer)

token\_logprobs (optional)

[array\[BigDecimal\]](#number)

tokens (optional)

[array\[String\]](#string)

top\_logprobs (optional)

[array\[map\[String, BigDecimal\]\]](#map)

### `CreateModelResponseProperties` - [Up](#__Models)

metadata (optional)

[map\[String, String\]](#string)

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

temperature (optional)

[BigDecimal](#number) What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.

top\_p (optional)

[BigDecimal](#number)

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top\_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or `temperature` but not both.

user (optional)

[String](#string) A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. [Learn more](/docs/guides/safety-best-practices#end-user-ids).

service\_tier (optional)

[ServiceTier](#ServiceTier)

### `DeleteModelResponse` - [Up](#__Models)

id

[String](#string)

deleted

[Boolean](#boolean)

object

[String](#string)

### `FunctionObject` - [Up](#__Models)

description (optional)

[String](#string) A description of what the function does, used by the model to choose when and how to call the function.

name

[String](#string) The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.

parameters (optional)

[map\[String, oas\_any\_type\_not\_mapped\]](#AnyType)

The parameters the functions accepts, described as a JSON Schema object. See the [guide](/docs/guides/function-calling) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.

Omitting `parameters` defines a function with an empty parameter list.

strict (optional)

[Boolean](#boolean) Whether to enable strict schema adherence when generating the function call. If set to true, the model will follow the exact schema defined in the `parameters` field. Only a subset of JSON Schema is supported when `strict` is `true`. Learn more about Structured Outputs in the [function calling guide](docs/guides/function-calling).

### `JSON_schema` - JSON schema [Up](#__Models)

Structured Outputs configuration options, including a JSON Schema.

description (optional)

[String](#string) A description of what the response format is for, used by the model to determine how to respond in the format.

name

[String](#string) The name of the response format. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.

schema (optional)

[map\[String, oas\_any\_type\_not\_mapped\]](#AnyType) The schema for the response format, described as a JSON Schema object. Learn how to build JSON schemas [here](https://json-schema.org/).

strict (optional)

[Boolean](#boolean) Whether to enable strict schema adherence when generating the output. If set to true, the model will always follow the exact schema defined in the `schema` field. Only a subset of JSON Schema is supported when `strict` is `true`. To learn more, read the [Structured Outputs guide](/docs/guides/structured-outputs).

### `ListModelsResponse` - [Up](#__Models)

object

[String](#string)

Enum:

list

data

[array\[Model\]](#Model)

### `Model` - Model [Up](#__Models)

Describes an OpenAI model offering that can be used with the API.

id

[String](#string) The model identifier, which can be referenced in the API endpoints.

created

[Integer](#integer) The Unix timestamp (in seconds) when the model was created.

object

[String](#string) The object type, which is always "model".

Enum:

model

owned\_by

[String](#string) The organization that owns the model.

### `ModelIdsShared` - [Up](#__Models)

### `ModelResponseProperties` - [Up](#__Models)

metadata (optional)

[map\[String, String\]](#string)

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

temperature (optional)

[BigDecimal](#number) What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.

top\_p (optional)

[BigDecimal](#number)

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top\_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or `temperature` but not both.

user (optional)

[String](#string) A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. [Learn more](/docs/guides/safety-best-practices#end-user-ids).

service\_tier (optional)

[ServiceTier](#ServiceTier)

### `PredictionContent` - Static Content [Up](#__Models)

Static predicted output content, such as the content of a text file that is being regenerated.

type

[String](#string) The type of the predicted content you want to provide. This type is currently always `content`.

Enum:

content

content

[PredictionContent\_content](#PredictionContent_content)

### `PredictionContent_content` - [Up](#__Models)

The content that should be matched when generating a model response. If generated tokens would match this content, the entire model response can be returned much more quickly.

### `ReasoningEffort` - [Up](#__Models)

**o-series models only**

Constrains effort on reasoning for [reasoning models](https://platform.openai.com/docs/guides/reasoning). Currently supported values are `low`, `medium`, and `high`. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.

### `ResponseFormatJsonObject` - JSON object [Up](#__Models)

JSON object response format. An older method of generating JSON responses. Using `json_schema` is recommended for models that support it. Note that the model will not generate JSON without a system or user message instructing it to do so.

type

[String](#string) The type of response format being defined. Always `json_object`.

Enum:

json\_object

### `ResponseFormatJsonSchema` - JSON schema [Up](#__Models)

JSON Schema response format. Used to generate structured JSON responses. Learn more about [Structured Outputs](/docs/guides/structured-outputs).

type

[String](#string) The type of response format being defined. Always `json_schema`.

Enum:

json\_schema

json\_schema

[JSON\_schema](#JSON_schema)

### `ResponseFormatText` - Text [Up](#__Models)

Default response format. Used to generate text responses.

type

[String](#string) The type of response format being defined. Always `text`.

Enum:

text

### `ServiceTier` - [Up](#__Models)

Specifies the latency tier to use for processing the request. This parameter is relevant for customers subscribed to the scale tier service:

*   If set to 'auto', and the Project is Scale tier enabled, the system will utilize scale tier credits until they are exhausted.
*   If set to 'auto', and the Project is not Scale tier enabled, the request will be processed using the default service tier with a lower uptime SLA and no latency guarentee.
*   If set to 'default', the request will be processed using the default service tier with a lower uptime SLA and no latency guarentee.
*   If set to 'flex', the request will be processed with the Flex Processing service tier. [Learn more](/docs/guides/flex-processing).
*   When not set, the default behavior is 'auto'.

When this parameter is set, the response body will include the `service_tier` utilized.

### `StopConfiguration` - [Up](#__Models)

Not supported with latest reasoning models `o3` and `o4-mini`.

Up to 4 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.

### `VoiceIdsShared` - [Up](#__Models)

### `WebSearchContextSize` - [Up](#__Models)

High level guidance for the amount of context window space to use for the search. One of `low`, `medium`, or `high`. `medium` is the default.

### `WebSearchLocation` - Web search location [Up](#__Models)

Approximate location parameters for the search.

country (optional)

[String](#string) The two-letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1) of the user, e.g. `US`.

region (optional)

[String](#string) Free text input for the region of the user, e.g. `California`.

city (optional)

[String](#string) Free text input for the city of the user, e.g. `San Francisco`.

timezone (optional)

[String](#string) The [IANA timezone](https://timeapi.io/documentation/iana-timezones) of the user, e.g. `America/Los_Angeles`.

### `Web_search` - Web search [Up](#__Models)

This tool searches the web for relevant results to use in a response. Learn more about the [web search tool](/docs/guides/tools-web-search?api-mode=chat).

user\_location (optional)

[Web\_search\_user\_location](#Web_search_user_location)

search\_context\_size (optional)

[WebSearchContextSize](#WebSearchContextSize)

### `Web_search_user_location` - [Up](#__Models)

Approximate location parameters for the search.

type

[String](#string) The type of location approximation. Always `approximate`.

Enum:

approximate

approximate

[WebSearchLocation](#WebSearchLocation)

### `updateChatCompletion_request` - [Up](#__Models)

metadata

[map\[String, String\]](#string)

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.