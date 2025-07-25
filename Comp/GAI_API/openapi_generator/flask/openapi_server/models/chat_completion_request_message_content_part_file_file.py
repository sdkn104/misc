from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class ChatCompletionRequestMessageContentPartFileFile(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, filename=None, file_data=None, file_id=None):  # noqa: E501
        """ChatCompletionRequestMessageContentPartFileFile - a model defined in OpenAPI

        :param filename: The filename of this ChatCompletionRequestMessageContentPartFileFile.  # noqa: E501
        :type filename: str
        :param file_data: The file_data of this ChatCompletionRequestMessageContentPartFileFile.  # noqa: E501
        :type file_data: str
        :param file_id: The file_id of this ChatCompletionRequestMessageContentPartFileFile.  # noqa: E501
        :type file_id: str
        """
        self.openapi_types = {
            'filename': str,
            'file_data': str,
            'file_id': str
        }

        self.attribute_map = {
            'filename': 'filename',
            'file_data': 'file_data',
            'file_id': 'file_id'
        }

        self._filename = filename
        self._file_data = file_data
        self._file_id = file_id

    @classmethod
    def from_dict(cls, dikt) -> 'ChatCompletionRequestMessageContentPartFileFile':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ChatCompletionRequestMessageContentPartFile_file of this ChatCompletionRequestMessageContentPartFileFile.  # noqa: E501
        :rtype: ChatCompletionRequestMessageContentPartFileFile
        """
        return util.deserialize_model(dikt, cls)

    @property
    def filename(self) -> str:
        """Gets the filename of this ChatCompletionRequestMessageContentPartFileFile.

        The name of the file, used when passing the file to the model as a  string.   # noqa: E501

        :return: The filename of this ChatCompletionRequestMessageContentPartFileFile.
        :rtype: str
        """
        return self._filename

    @filename.setter
    def filename(self, filename: str):
        """Sets the filename of this ChatCompletionRequestMessageContentPartFileFile.

        The name of the file, used when passing the file to the model as a  string.   # noqa: E501

        :param filename: The filename of this ChatCompletionRequestMessageContentPartFileFile.
        :type filename: str
        """

        self._filename = filename

    @property
    def file_data(self) -> str:
        """Gets the file_data of this ChatCompletionRequestMessageContentPartFileFile.

        The base64 encoded file data, used when passing the file to the model  as a string.   # noqa: E501

        :return: The file_data of this ChatCompletionRequestMessageContentPartFileFile.
        :rtype: str
        """
        return self._file_data

    @file_data.setter
    def file_data(self, file_data: str):
        """Sets the file_data of this ChatCompletionRequestMessageContentPartFileFile.

        The base64 encoded file data, used when passing the file to the model  as a string.   # noqa: E501

        :param file_data: The file_data of this ChatCompletionRequestMessageContentPartFileFile.
        :type file_data: str
        """

        self._file_data = file_data

    @property
    def file_id(self) -> str:
        """Gets the file_id of this ChatCompletionRequestMessageContentPartFileFile.

        The ID of an uploaded file to use as input.   # noqa: E501

        :return: The file_id of this ChatCompletionRequestMessageContentPartFileFile.
        :rtype: str
        """
        return self._file_id

    @file_id.setter
    def file_id(self, file_id: str):
        """Sets the file_id of this ChatCompletionRequestMessageContentPartFileFile.

        The ID of an uploaded file to use as input.   # noqa: E501

        :param file_id: The file_id of this ChatCompletionRequestMessageContentPartFileFile.
        :type file_id: str
        """

        self._file_id = file_id
