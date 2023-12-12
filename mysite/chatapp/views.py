import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from .models import ChatRoom,ChatMessage,UserProfile
from django.db.models import Count
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
def index(request,username):
    user = User.objects.get(username=username)
    chatrooms = ChatRoom.objects.filter(users=user)
    return render(request,'chatapp/index.html',{'chatrooms':chatrooms})


def chatroom(request,slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    messages = ChatMessage.objects.filter(room=chatroom)[0:30]
    return render(request,'chatapp/room.html',{'chatroom':chatroom,'messages':messages})

@csrf_exempt
def test(request):
    user1 = User.objects.get(id='4')
    user2 = User.objects.get(id='3')
    chat_rooms_for_both_users = ChatRoom.objects.filter(
    users__in=[user1, user2], 
    chat_type='personal'
)
    
    # If such a room exists, get its messages
    if chat_rooms_for_both_users.exists():
        chatroom = chat_rooms_for_both_users.first()
        messages = ChatMessage.objects.filter(room=chatroom)[0:30]
        return render(request, 'chatapp/room.html', {'chatroom': chatroom, 'messages': messages})
    else:
        new_chatroom = ChatRoom.objects.create(slug='test1',name='test2')
        new_chatroom.users.add(user1)
        new_chatroom.users.add(user2)
        new_chatroom.save()

@csrf_exempt
def create_privateroom(request):
    body = json.loads(request.body)
    current_user_id = body.get('user1')
    other_user_id = body.get('user2')
    slug=body.get('slug')
    name=body.get('name')

    try:
        user1 = User.objects.get(id=current_user_id)
        user2 = User.objects.get(id=other_user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist."}, status=404)
    
    chat_rooms_for_user1 = ChatRoom.objects.filter(users=user1, chat_type='personal')

    for chat_room in chat_rooms_for_user1:
        if len(chat_room.users.filter(id=user2.id))>0:
            #chatroom = ChatRoom.objects.get(slug=chat_room.slug)
            messages = ChatMessage.objects.filter(room=chatroom)[0:30]
            return render(request,'chatapp/room.html',{'chatroom':chat_room,'messages':messages})

    # If the chat room doesn't exist, create a new one
    new_chatroom = ChatRoom.objects.create(slug=slug,name=name)
    new_chatroom.users.add(user1)
    new_chatroom.users.add(user2)
    new_chatroom.save()

    # Redirect to the newly created chat room
    return render(request,'chatapp/room.html',{'chatroom':new_chatroom,'messages':''})


def create_group_chatroom(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        groupName=request.POST('groupName')
        # Create a new chat room
        new_chatroom = ChatRoom.objects.create(slug=groupName)
        # Add the users to the chat room
        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
                new_chatroom.users.add(user)
            except User.DoesNotExist:
                # Handle the case where a user does not exist
                new_chatroom.delete()  # Delete the chat room if a user is not found
                return JsonResponse({"error": f"User with ID {user_id} does not exist."}, status=404)

        # Redirect to the newly created chat room
        return JsonResponse({"message": "Group chat room created.", "slug": new_chatroom.slug})

    # Handle GET request (render a form to create a group chat)
    return JsonResponse({"message": "Chat room created.", "slug": new_chatroom.slug})
def delete_chatroom(request, slug):
    chat_room = get_object_or_404(ChatRoom, slug=slug)
    chat_room.delete()
    return HttpResponse("chatRoom Deleted")  # Replace 'chatroom_list' with the appropriate UmeRL na