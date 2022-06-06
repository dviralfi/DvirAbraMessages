

from rest_framework.response import Response
from rest_framework.decorators import api_view
from mainapp.models import Message,User
from .serializers import MessageSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.db.models import Q
from rest_framework.parsers import JSONParser

@api_view(["GET"])
def get_all_messages(request, *args, **kwargs):
    username = kwargs["username"]

    """
    all_messages = MessageSerializer(

    Message.objects.filter
    (
    Q(sender = User.objects.get(username=username))|
    Q(receiver = User.objects.get(username=username))
    )
    ,many=True
    )
    """

    user_object = User.objects.get(username=username)
    all_messages = MessageSerializer(user_object.messages.all(),many=True)

    return Response(all_messages.data)


@api_view(["GET","DELETE"])
def message(request, *args, **kwargs):
    id = kwargs['id']
    username = kwargs["username"]

    if request.method=='GET':
        
        try:
            user_object = User.objects.get(username=username)
            message = user_object.messages.get(id=id)
            message_serializer = MessageSerializer(message)

            message.is_read = True
            message.save() # update the 'is_read' attribute

            return Response(message_serializer.data)

        except ObjectDoesNotExist:
            return Response(status=404)

    elif request.method=='DELETE':
        
        try:
            user_object = User.objects.get(username=username)
            message = user_object.messages.get(id=id)
            user_object.messages.remove(message)
            
            return Response(status=200)

        except ObjectDoesNotExist:
            return Response(status=404)



@api_view(["POST"])
def write_message(request, format=None, *args, **kwargs):
    parser_classes = (JSONParser,)

    print(request.data)

    receiver_id = request.data['receiver']
    sender_id = request.data['sender']


    #message_serializer = JSONParser.parse(stream=request.data)
    
    message_serializer = MessageSerializer(data = request.data)
    #print(message_serializer, type(message_serializer))
    print(request.data, type(request.data))
    message_dict = request.data
    
    
    if message_serializer.is_valid():
        receiver_user_object = User.objects.get(id=receiver_id)
        sender_user_object = User.objects.get(id=sender_id)

        message_dict["receiver"] = receiver_user_object
        message_dict["sender"] = sender_user_object

        message = Message(**message_dict)
        message.save()

        # Saves the message for the receiver:
        receiver_user_object.messages.add(message)

        # Saves the message for the sender:
        sender_user_object.messages.add(message)
        
        return Response(message_serializer.data, status=status.HTTP_201_CREATED)
    else:    
        return Response(message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def get_unread_messages(request, *args, **kwargs):

    username = kwargs["username"]
    user_object = User.objects.get(username=username)
    unread_messages = MessageSerializer(user_object.messages.filter(is_read=False), many=True)
        
    return Response(unread_messages.data)