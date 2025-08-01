from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server.models.prediction_content_content import PredictionContentContent
from openapi_server import util

from openapi_server.models.prediction_content_content import PredictionContentContent  # noqa: E501

class PredictionContent(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, type=None, content=None):  # noqa: E501
        """PredictionContent - a model defined in OpenAPI

        :param type: The type of this PredictionContent.  # noqa: E501
        :type type: str
        :param content: The content of this PredictionContent.  # noqa: E501
        :type content: PredictionContentContent
        """
        self.openapi_types = {
            'type': str,
            'content': PredictionContentContent
        }

        self.attribute_map = {
            'type': 'type',
            'content': 'content'
        }

        self._type = type
        self._content = content

    @classmethod
    def from_dict(cls, dikt) -> 'PredictionContent':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PredictionContent of this PredictionContent.  # noqa: E501
        :rtype: PredictionContent
        """
        return util.deserialize_model(dikt, cls)

    @property
    def type(self) -> str:
        """Gets the type of this PredictionContent.

        The type of the predicted content you want to provide. This type is currently always `content`.   # noqa: E501

        :return: The type of this PredictionContent.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this PredictionContent.

        The type of the predicted content you want to provide. This type is currently always `content`.   # noqa: E501

        :param type: The type of this PredictionContent.
        :type type: str
        """
        allowed_values = ["content"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def content(self) -> PredictionContentContent:
        """Gets the content of this PredictionContent.


        :return: The content of this PredictionContent.
        :rtype: PredictionContentContent
        """
        return self._content

    @content.setter
    def content(self, content: PredictionContentContent):
        """Sets the content of this PredictionContent.


        :param content: The content of this PredictionContent.
        :type content: PredictionContentContent
        """
        if content is None:
            raise ValueError("Invalid value for `content`, must not be `None`")  # noqa: E501

        self._content = content
