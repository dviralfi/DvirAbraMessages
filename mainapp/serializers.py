from mainapp.models import Message
from rest_framework import serializers 


"""
This is the Serializers file.

In order to send proper JSON formatted data to the clients (as REST API suggests), we need to serialize the data from the Objects/Models/other Python data that we handle in the back-end.

I used the default Serializers Class that 3rd party package rest_framwork(Django Rest Framework) is providing.

"""


class MessageSerializer(serializers.ModelSerializer):
    """
    A class to Serialize a Message.

    Attributes
    ----------
    Modifing the Meta Class from the default inherted ModelSerializer
    so that the model is set to the custom model - `Message`.

    also inputing the required fields in the Message.
    """
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message_txt', 'subject', 'creation_date']  # `is_read` attribute is not included - it's not required in the data, just for the back-end.
       