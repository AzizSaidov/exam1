
# Django REST Framework — Custom User + Token Authentication (APIView)

## 1. Custom User Model


```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model (can be extended later).
    """
    pass
````

---

## 2. Settings Configuration

**settings.py**

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'accounts',
]
```

```python
AUTH_USER_MODEL = 'accounts.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

---

## 3. Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 4. Register Serializer

**accounts/serializers.py**

```python
from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
```

---

## 5. Views (Register / Login / Profile)

**accounts/views.py**

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)

from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=HTTP_200_OK)

        return Response(
            {"error": "Invalid credentials"},
            status=HTTP_400_BAD_REQUEST
        )


class ProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"user": request.user.username})
```

---

## 6. URLs

**accounts/urls.py**

```python
from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ProfileAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("profile/", ProfileAPIView.as_view()),
]
```

**project urls.py**

```python
from django.urls import path, include

urlpatterns = [
    path("api/", include("accounts.urls")),
]
```

---

## 7. API Usage

### Register

`POST /api/register/`

```json
{
  "username": "john",
  "password": "12345"
}
```

Response:

```json
{
  "token": "abcd12345..."
}
```

---

### Login

`POST /api/login/`

```json
{
  "username": "john",
  "password": "12345"
}
```

Response:

```json
{
  "token": "abcd12345..."
}
```

---

### Profile (Protected)

`GET /api/profile/`

Header:

```
Authorization: Token abcd12345...
```

Response:

```json
{
  "user": "john"
}
```

---

# Swagger (Token Authentication)

## Option 1: drf-yasg

### Install

```bash
pip install drf-yasg
```

### settings.py

```python
INSTALLED_APPS += ['drf_yasg']
```

### urls.py

```python
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]
```

---

## Swagger Token Setup

```
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
```

In Swagger UI:

### 1. Click **Authorize**

### 2. Enter:

```
Token your_token_here
```

### 3. Format is IMPORTANT:

```
Token abc123xyz
```
 