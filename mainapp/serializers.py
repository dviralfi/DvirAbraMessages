from rest_framework import serializers
from mainapp.models import Message,User
from rest_framework.response import Response



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message_txt', 'subject', 'creation_date','is_read']

"""

    def create(self, validated_data):
        ""
        Create and return a new `Message` instance, with the validated data.
        ""
        return Message.objects.create(**validated_data)

    def delete(self, instance):
        ""
        Delete an existing `Message` instance, with the validated data.
        ""
        if instance.exists():
            instance.delete()
            return Response({'data':"Deleted"},status=200)
        else:
            message_not_exist_txt = 'Message {} Not Exist'.format(instance)
            return Response({'data':message_not_exist_txt},status=404)
        

"""