"""
The Views File which contains the views that will execute from the urls endpoints by the RestAPI structure. (see in `mainapp/urls.py`)
-------------

The decorators in each view function e.g. @api_view(["GET"]),
is for the view function to accept only specific HTTP Requests.

"""

# Custom Imports
from unicodedata import name
from mainapp.models import Message, MessageUser # Custom Models
from mainapp.serializers import MessageSerializer # Custom Serializers

#Django Imports
from django.core.exceptions import ObjectDoesNotExist 

# Django Rest Framework Imports
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status # For HTTP statuses
from rest_framework.permissions import IsAuthenticated,AllowAny # For User Authentication



# Basic IsAuthenticated(is the User is logged-in) implementation:
#permission_classes = (IsAuthenticated,)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_messages(request, *args, **kwargs):
    '''
    Returns all Messages of the logged-in User.

            Parameters:
                    request (HTTP Request) : contains various HTTP content 
                    *args (possible non-keyword arguments)
                    *kwargs (possible keyword arguments) : contains the username in the endpoint (for example: /user1/messages) user1 is the username)

            Returns:
                    Json Response (Json): if valid - returns the messages, if not - returns Http-Error Response
    '''

    username = kwargs["username"]

    if request.user.username != username:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        user_object = MessageUser.objects.get(username=username)
    except MessageUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    all_messages = MessageSerializer(user_object.messages.all(),many=True)

    return Response(all_messages.data)


@api_view(["GET","DELETE"])
@permission_classes([IsAuthenticated])
def message(request, *args, **kwargs):
    '''
    Returns specific Message of the logged-in User.

            Parameters:
                    request (HTTP Request) : contains various HTTP content 
                    *args (possible non-keyword arguments)
                    *kwargs (possible keyword arguments) : contains the username and the ID of the message in the endpoint (for example: /user1/messages/3) user1 is the username and 3 is the message ID)

            Returns:
                    Json Response (Json): if valid - returns the message, if not - returns Http-Error Response
    '''

    id = kwargs['id']
    username = kwargs["username"]

    if request.user.username != username:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method=='GET':
        
        try:
            user_object = MessageUser.objects.get(username=username)
            message = user_object.messages.get(id=id)
            message_serializer = MessageSerializer(message)

            message.is_read = True
            message.save() # update the 'is_read' attribute

            return Response(message_serializer.data)

        except ObjectDoesNotExist:
            return Response(status=404)

    elif request.method=='DELETE':
        
        try:
            user_object = MessageUser.objects.get(username=username)
            message = user_object.messages.get(id=id)
            user_object.messages.remove(message)
            
            return Response(status=200)

        except ObjectDoesNotExist:
            return Response(status=404)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def write_message(request, *args, **kwargs):
    '''
    Send a New Message for the logged-in User.


            The API works with JSON data. Example:

            {
            "sender": int id OR "user-name",
            "receiver": int id OR "user-name" ,
            "message_txt": "Message-Text",
            "subject": "Message-Subject"
            }

            Parameters:
                    request (HTTP Request) : contains various HTTP content, and in particular - 'data' which contains the New Message data to be sent.
                    *args (possible non-keyword arguments)
                    *kwargs (possible keyword arguments) : contains the username in the endpoint (for example: /user1/messages) user1 is the username)

            Returns:
                    Json Response (Json): if valid - returns the New Message that has been sent with a HTTP_201_CREATED status, if not - returns Http-Error Response
    '''
    # Gets the essential data
    username = kwargs["username"]
    receiver_id = request.data['receiver']
    sender_id = request.data['sender']

    # Checks if the user input the name of the sender/receiver (and the DB works with the Users IDs)
    if type(receiver_id)==str:
        request.data['receiver'] = MessageUser.objects.get(username=request.data['receiver']).id
        
    if type(sender_id)==str:
        request.data['sender'] =  MessageUser.objects.get(username=request.data['sender']).id
    
    # Updating the variables sender_id and receiver_id :
    receiver_id = request.data['receiver']
    sender_id = request.data['sender']
        

    # checks if the username that want to send is logged in and the message is not from someone else to himself:
    if request.user.username != username or request.user.id != sender_id: 
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    #de-serialize the message that the user sent(in JSNO format) to Python friendly data - in orser to save it as a Message Model.

    message_serializer = MessageSerializer(data = request.data)
    message_dict = request.data
    
    if message_serializer.is_valid():
        # gets the Users Objects
        receiver_user_object = MessageUser.objects.get(id=receiver_id)
        sender_user_object = MessageUser.objects.get(id=sender_id)

        #replacing the ID's in the message that the user sent - with actual User Object - for Django to bind it with the coressponding ForiegnKey - MessageUser:
        message_dict["receiver"] = receiver_user_object
        message_dict["sender"] = sender_user_object

        # converts the message dictionary (that it makes by de-serialize the JSON data the user sent) to a Message Object(for saving it in the DB)
        message = Message(**message_dict)
        message.save()

        # Saves the message in the DB for the receiver:
        receiver_user_object.messages.add(message)

        # Saves the message in the DB for the sender:
        message.is_read = True # The sender obviously saw the message..
        message.save()
        sender_user_object.messages.add(message)
        
        return Response(message_serializer.data, status=status.HTTP_201_CREATED)
    else:    
        return Response(message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_unread_messages(request, *args, **kwargs):
    '''
    Returns all Unread Messages of the logged-in User.

            Parameters:
                    request (HTTP Request) : contains various HTTP content 
                    *args (possible non-keyword arguments)
                    *kwargs (possible keyword arguments) : contains the username in the endpoint (for example: /user1/messages) user1 is the username)

            Returns:
                    Json Response (Json): if valid - returns the unread messages, if not - returns Http-Error Response
    '''
    username = kwargs["username"]

    if request.user.username != username:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    user_object = MessageUser.objects.get(username=username)
    unread_messages = MessageSerializer(user_object.messages.filter(is_read=False), many=True)
        
    return Response(unread_messages.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request, *args, **kwargs):
    """
    Create a User to perform API requests with it!

    Create user by JSON format:

    {
    "username": "your username here",
    "password": "yourpasswordhere"
    }

    """   

    user_dict = request.data
    print (user_dict)
    try:

        user_object = MessageUser.objects.create_user(**user_dict)
        return Response(status=status.HTTP_201_CREATED)

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)