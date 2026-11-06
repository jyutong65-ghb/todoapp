from django.shortcuts import render
from rest_framework import generics, permissions
from api.serializers import TodoSerializer, TodoToggleCompleteSerializer
from todo.models import Todo


class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)


class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.completed = not(serializer.instance.completed)
        serializer.save()


from django.db import IntegrityError

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)  # data is a dictionary
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse(data={'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(data={'error': 'username taken. choose another username'}, status=400)


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = JSONParser().parse(request)
        username, password = data['username'], data['password']
    except (ParseError, ValueError, KeyError, TypeError):
        return JsonResponse({'error': 'username and password are required'}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'unable to login. check username and password'}, status=400)
    token, _ = Token.objects.get_or_create(user=user)
    return JsonResponse({'token': token.key}, status=201)
