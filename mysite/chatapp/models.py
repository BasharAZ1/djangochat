from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', related_name='user_friends')

CHAT_TYPES = (
    ('personal', 'Personal'),
    ('group', 'Group'),
)
MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
MESSAGE_TYPES = (
    ('text', 'Text'),
    ('media', 'Media'),
)
EMOJI_REACTIONS = (
    ('thumbs_up', '👍'),
    ('thumbs_down', '👎'),
    ('heart', '❤️'),
)
class ChatRoom(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36,db_index=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    users = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    chat_type = models.CharField(max_length=10, choices=CHAT_TYPES, default='personal')
    class Meta:
        ordering = ['created_at']
        db_table = 'ChatRooms'
    
    
class ChatMessage(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36,db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message_content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    media = models.ManyToManyField('chatapp.Media', blank=True, related_name='related_chat') 
    class Meta:
        ordering=('date',)
        db_table = 'Messages'
class Media(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    type = models.CharField(choices=MEDIA_TYPES, max_length=10)
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    thumbnail_url = models.URLField(null=True, blank=True)
    size = models.PositiveIntegerField()
    format = models.CharField(max_length=10)

    class Meta:
        db_table = 'Media'
        ordering = ['uploaded_at']