
# Django Chat Application

This is a Django-based chat application where users can join chat rooms and send messages using WebSockets. The project utilizes Django Channels to handle WebSocket connections, allowing real-time communication.

## Features

- User authentication and profile management
- Create and join chat rooms
- Send and receive messages in real-time
- Support for personal and group chats
- Media sharing (images and videos)

## Models

### UserProfile

Represents a user's profile and their friends.

```python
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', related_name='user_friends')
```

### ChatRoom

Represents a chat room which can be either personal or group.

```python
from django.db import models
import uuid
from django.contrib.auth.models import User

CHAT_TYPES = (
    ('personal', 'Personal'),
    ('group', 'Group'),
)

class ChatRoom(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36, db_index=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    users = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    chat_type = models.CharField(max_length=10, choices=CHAT_TYPES, default='personal')

    class Meta:
        ordering = ['created_at']
        db_table = 'ChatRooms'
```

### ChatMessage

Represents a message sent in a chat room.

```python
from django.db import models
import uuid
from django.contrib.auth.models import User

MESSAGE_TYPES = (
    ('text', 'Text'),
    ('media', 'Media'),
)

class ChatMessage(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message_content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    media = models.ManyToManyField('Media', blank=True, related_name='related_chat')

    class Meta:
        ordering = ('date',)
        db_table = 'Messages'
```

### Media

Represents media files shared in chat messages.

```python
from django.db import models
import uuid

MEDIA_TYPES = (
    ('image', 'Image'),
    ('video', 'Video'),
)

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
```

## Setup

### Prerequisites

- Python 3.x
- Django
- Django Channels
- Djongo (for MongoDB)

### Installation

1. Clone the repository:
   ```sh
   git clone [https://github.com/your-username/django-chat.git](https://github.com/BasharAZ1/djangochat.git)
   cd mysite
   ```

2. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```sh
   python manage.py migrate
   ```

5. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```sh
   python manage.py runserver
   ```

### Configuration

In `settings.py`, ensure that the `CHANNEL_LAYERS` setting is configured correctly for your environment:

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
```

## Usage

1. Access the admin interface at `http://127.0.0.1:8000/admin` to manage users and chat rooms.
2. Join chat rooms and start sending messages in real-time.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any features, bug fixes, or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
