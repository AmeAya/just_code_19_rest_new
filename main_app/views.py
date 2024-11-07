from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


class BookApiView(APIView):
    permission_classes = [AllowAny]
    # permission_classes -> Какие права доступа, применять на этот АПИ
    # AllowAny -> Доступен любому

    def get(self, request):
        book_id = request.GET.get('id')
        # request.GET.get('<КЛЮЧ>') -> Берет данные по <КЛЮЧ> из гет запроса
        if book_id is None:
            books = Book.objects.all()  # Вытащить все книги из БД
            data = BookSerializer(books, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            if book_id.isnumeric():
                book = Book.objects.get(id=book_id)
                data = BookSerializer(book, many=False).data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'id must be integer!'},
                                status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # name = request.data.get('name')
        # if name is None:
        #     return Response({'message': 'name is required!'},
        #                     status=status.HTTP_400_BAD_REQUEST)
        #
        # description = request.data.get('description')
        # year = request.data.get('year')
        #
        # book = Book(name=name, description=description, year=year)
        # book.save()

        book = BookSerializer(data=request.data)
        if book.is_valid():
            # is_valid() -> Проверяет правильные ли данные
            book.save()
            return Response({'message': 'book created!'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(book.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        book_id = request.data.get('id')
        # request.data.get('<KEY>') -> Берет значение из запроса по ключу <KEY>,
        #   если такого ключа нету в теле запроса, то вернет None
        if book_id is None:
            return Response(data={'detail': 'Ты забыл добавить id! косяк!'}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     book = Book.objects.get(id=book_id)
        # except Book.DoesNotExist:
        #     return Response(data={'message': 'Book does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        from django.shortcuts import get_object_or_404
        book = get_object_or_404(Book, id=book_id)
        # get_object_or_404 -> Берет объект из БД по указанному условию,
        #   если не находит, то возвращает 404

        book_serializer = BookSerializer(book, data=request.data, partial=True)
        if book_serializer.is_valid():
            book_serializer.save()
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(data=book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        book_id = request.data.get('id')
        if book_id is None:
            return Response(data={'detail': 'Ты забыл добавить id! косяк!'}, status=status.HTTP_400_BAD_REQUEST)

        from django.shortcuts import get_object_or_404
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return Response(data={'detail': 'Book deleted!'}, status=status.HTTP_200_OK)


class SecretApiView(APIView):
    permission_classes = [IsAdminUser]  # Проверяет авторизован ли пользователь

    def get(self, request):
        return Response(data={'secret': '1+1=11'}, status=status.HTTP_200_OK)


class RegistrationApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):  # Чисто ради примера, ради дебагинга!
        from django.contrib.auth.models import User
        users = User.objects.all()
        data = UserSerializer(users, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        from django.contrib.auth.models import User
        from django.db import IntegrityError
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            User.objects.create_user(username=username, password=password)
            return Response(data={'message': 'Registration success'}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(data={'message': 'Username is already registered'}, status=status.HTTP_400_BAD_REQUEST)


class AuthApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth import login, authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(data={'message': 'Invalid username/password'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            login(request, user)
            return Response(data={'message': 'Auth success!'}, status=status.HTTP_200_OK)


# Создать новый APIView.
# Выставить permission_classes - IsAuthenticated
# На ГЕТ запрос должна возвращать данные об этом пользователе(request.user засунуть в UserSerializer)
# Протестировать АПИ через постман
