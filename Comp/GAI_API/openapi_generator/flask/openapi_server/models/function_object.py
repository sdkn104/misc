from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class FunctionObject(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, description=None, name=None, parameters=None, strict=False):  # noqa: E501
        """FunctionObject - a model defined in OpenAPI

        :param description: The description of this FunctionObject.  # noqa: E501
        :type description: str
        :param name: The name of this FunctionObject.  # noqa: E501
        :type name: str
        :param parameters: The parameters of this FunctionObject.  # noqa: E501
        :type parameters: Dict[str, object]
        :param strict: The strict of this FunctionObject.  # noqa: E501
        :type strict: bool
        """
        self.openapi_types = {
            'description': str,
            'name': str,
            'parameters': Dict[str, object],
            'strict': bool
        }

        self.attribute_map = {
            'description': 'description',
            'name': 'name',
            'parameters': 'parameters',
            'strict': 'strict'
        }

        self._description = description
        self._name = name
        self._parameters = parameters
        self._strict = strict

    @classmethod
    def from_dict(cls, dikt) -> 'FunctionObject':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The FunctionObject of this FunctionObject.  # noqa: E501
        :rtype: FunctionObject
        """
        return util.deserialize_model(dikt, cls)

    @property
    def description(self) -> str:
        """Gets the description of this FunctionObject.

        A description of what the function does, used by the model to choose when and how to call the function.  # noqa: E501

        :return: The description of this FunctionObject.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this FunctionObject.

        A description of what the function does, used by the model to choose when and how to call the function.  # noqa: E501

        :param description: The description of this FunctionObject.
        :type description: str
        """

        self._description = description

    @property
    def name(self) -> str:
        """Gets the name of this FunctionObject.

        The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.  # noqa: E501

        :return: The name of this FunctionObject.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this FunctionObject.

        The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.  # noqa: E501

        :param name: The name of this FunctionObject.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def parameters(self) -> Dict[str, object]:
        """Gets the parameters of this FunctionObject.

        The parameters the functions accepts, described as a JSON Schema object. See the [guide](/docs/guides/function-calling) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.   Omitting `parameters` defines a function with an empty parameter list.  # noqa: E501

        :return: The parameters of this FunctionObject.
        :rtype: Dict[str, object]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: Dict[str, object]):
        """Sets the parameters of this FunctionObject.

        The parameters the functions accepts, described as a JSON Schema object. See the [guide](/docs/guides/function-calling) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.   Omitting `parameters` defines a function with an empty parameter list.  # noqa: E501

        :param parameters: The parameters of this FunctionObject.
        :type parameters: Dict[str, object]
        """

        self._parameters = parameters

    @property
    def strict(self) -> bool:
        """Gets the strict of this FunctionObject.

        Whether to enable strict schema adherence when generating the function call. If set to true, the model will follow the exact schema defined in the `parameters` field. Only a subset of JSON Schema is supported when `strict` is `true`. Learn more about Structured Outputs in the [function calling guide](docs/guides/function-calling).  # noqa: E501

        :return: The strict of this FunctionObject.
        :rtype: bool
        """
        return self._strict

    @strict.setter
    def strict(self, strict: bool):
        """Sets the strict of this FunctionObject.

        Whether to enable strict schema adherence when generating the function call. If set to true, the model will follow the exact schema defined in the `parameters` field. Only a subset of JSON Schema is supported when `strict` is `true`. Learn more about Structured Outputs in the [function calling guide](docs/guides/function-calling).  # noqa: E501

        :param strict: The strict of this FunctionObject.
        :type strict: bool
        """

        self._strict = strict
