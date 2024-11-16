from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from .permissions import *


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


class TestApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):  # Записываем в сесии book_id и example
        book_id = request.data.get('book_id')
        request.session['book_id'] = book_id
        request.session['example'] = 'Hello, World!'
        return Response(data=request.session, status=status.HTTP_200_OK)


class CheckApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):  # Возвращает все что есть в сессиях
        return Response(data=request.session, status=status.HTTP_200_OK)


class CabinetApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user -> Если пользователь авторизован, то юзер лежит в request.user
        data = UserSerializer(request.user, many=False).data
        data['cart'] = request.session.get('example')
        return Response(data=data, status=status.HTTP_200_OK)

    def delete(self, request):
        request.user.delete()
        return Response(data={'message': 'OK!'}, status=status.HTTP_200_OK)


class BookSearchApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        search = request.GET.get('search')
        book_by_name = Book.objects.filter(name__contains=search)
        # __search -> Ищет слово целиком
        # __contains -> Ищет символы без регистра
        # __icontains -> Ищет символы c регистра

        authors1 = Author.objects.filter(name__contains=search)
        authors2 = Author.objects.filter(surname__contains=search)

        books = set()

        for author1 in authors1:
            book_by_author1 = Book.objects.filter(author=author1)
            books = books.union(book_by_author1)

        for author2 in authors2:
            book_by_author2 = Book.objects.filter(author=author2)
            books = books.union(book_by_author2)

        books = books.union(book_by_name)
        data = BookSerializer(books, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class BookOrderApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # desc(Descending) убывание, asc(Ascending) возврастанию
        year = request.GET.get('year')
        name = request.GET.get('name')
        books = Book.objects.all()

        if year is not None:
            if year == 'desc':
                books = books.order_by('-year')  # 9 -> 0
            elif year == 'asc':
                books = books.order_by('year')  # 0 -> 9

        if name is not None:
            if name == 'desc':
                books = books.order_by('-name')  # Z -> A
            elif name == 'asc':
                books = books.order_by('name')  # A -> Z
        data = BookSerializer(books, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


from rest_framework.pagination import PageNumberPagination
class BookPaginatedApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        books = Book.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated_books = paginator.paginate_queryset(books, request)
        data = BookSerializer(paginated_books, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class CocktailApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        import requests  # pip install requests
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
        if response.status_code != 200:
            return Response(data={'Message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            cocktail = response.json()
            data = {
                'name': cocktail['drinks'][0]['strDrink']
            }
            return Response(data=data, status=status.HTTP_200_OK)
