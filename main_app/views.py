from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
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


# 1) Создать новую модель(минимум 3 поля)
# 2) Создать сериалайзер для новой модели
# 3) Создать АПИ:
#    GET -> Все записи из новой модели
#    POST -> Создать новую запись для новой модельки
