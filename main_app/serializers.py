from rest_framework.serializers import ModelSerializer
from .models import *


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # to_representation -> Функция в сериалайзере, которая конвертирует из Объекта в JSON
    def to_representation(self, instance):  # instance -> Джанговский Объект, который конвертируем
        # representation = {}
        # representation['name'] = instance.name.upper()

        representation = super().to_representation(instance)  # JSON где id вместо author и genres

        representation['author'] = AuthorSerializer(instance.author, many=False).data
        representation['genres'] = GenreSerializer(instance.genres, many=True).data
        # Конверитую автора через AuthorSerializer и запихиваю в ключик 'author'

        # representation['author'] = {
        #     'id': instance.author.id,
        #     'name': instance.author.name,
        #     'surname': instance.author.surname
        # }

        representation['publisher'] = 'ABC Public Library'
        return representation


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


from django.contrib.auth.models import User
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


# Создать две новые модели Country(name, capital_city), Language(name)
# Добавить к модели Author два новых поля: country(Страна рождения автора) и languages(Какими языками владел автор)
# Изменить AuthorSerializer таким образом, чтобы поля country и languages показывались как dict с полями, а не как id
# Проверить через ГЕТ запрос на http://127.0.0.1:8000/books
