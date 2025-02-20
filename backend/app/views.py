from lib2to3.fixes.fix_input import context

# from app.models import Session
# from Scripts.bottle import response
from django.contrib.auth import login
from django.core.files.storage import default_storage
from django.http import HttpResponse, FileResponse, Http404
from django.template.defaultfilters import first
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet

from app.models import Users, Files, Session
from app.serializers import UserSerializer, FileSerializer, SessionSerializer
# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import uuid

# Create your views here.

HOST_NAME = 'http://127.0.0.1:8000/'


def add_postfix(filename, count):
    # Находим последнюю точку в имени файла
    dot_index = filename.rfind('.')

    # Если точки нет или она в начале, расширения нет
    if dot_index <= 0:
        return f"{filename} ({count})"

    # Разделяем имя и расширение
    name = filename[:dot_index]
    extension = filename[dot_index:]

    # Собираем новое имя
    return f"{name} (1){extension}"

# @api_view(["GET"])
# def get_all_users(req):
#     users = Users.objects.all()
#     user_ser = UserSerializer(users, many=True)
#     return Response(user_ser.data)
#
# @api_view(["GET"])
# def create_admin(req):
#     user = Users(id=1, name="admin", login="admin", password="1", admin=True)
#     user.save()
#     user_ser = UserSerializer(user)
#     cont = {
#         "code": 200,
#         "msg": "READY",
#         "user_info": user_ser.data
#     }
#     return Response(cont)
#     # return Response(UserSerializer(user).data)

class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class FilesViewSet(ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FileSerializer

    def update(self, request, *args, **kwargs):
        # Получаем объект по его ID
        instance = self.get_object()

        # Обновляем только поле file_name
        file_name = request.data.get('file_name')
        if file_name is not None:
            instance.file_name = file_name
            instance.save()
            serializer = self.get_serializer(instance)
            return Response({
                "status_code": 200,
                "file": serializer.data
            })

        return Response({"detail": "file_name is required."}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        file_name, user_id = request.data["file_name"], request.data["user_id"]
        file = Files(file_name=file_name, file_link="", user_id=user_id)
        file.save()
        file_data = FileSerializer(file).data
        content = {
            "status_code": 200,
            "status": "OK",
            "create_object": file_data
        }
        return Response(content)

    def retrieve_by_link(self, request):
        try:
            file_link = request.GET.get("link")
            file_instance = Files.objects.get(file_link=file_link)
            serializer = self.get_serializer(file_instance)
            return Response(serializer.data)
        except Files.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getLinkForFile(request, file_id):

    file_link = str(uuid.uuid5(uuid.NAMESPACE_URL, file_id))

    counts_update = Files.objects.filter(id=file_id).update(file_link=file_link)


    if counts_update:
        content = {
            "status_code": 200,
            "status": "OK",
            "file_id": file_id,
            "file_link": file_link,
        }
    else:
        content = {
            "status_code": 400,
            "status": "ERROR",
            "error_message": "Ничего не обновилось, хер знает почему"
        }


    return Response(content)

@api_view(["POST"])
def check_password(req):
    # print(req.data)
    user_login, user_password = req.data["login"], req.data["password"]
    search_user = Users.objects.filter(login=user_login, password=user_password)
    user_data = UserSerializer(search_user, many=True).data
    if search_user:
        print("все ок")
        context = {
            "status_code": 200,
            "status": "OK",
            "user": user_data
        }
    else:
        print("нифига не ок")
        context = {
            "status_code": 400,
            "status": "ERROR",
            "error_message": "Неверный логин или пароль"
        }

    return Response(context)

@api_view(["POST"])
def login_view(request):
    try:
        user_login, user_password = request.data["login"], request.data["password"]
        search_user = Users.objects.filter(login=user_login, password=user_password)
        search_user_data = UserSerializer(search_user, many=True).data
        if search_user_data:
            if Session.objects.filter(login=user_login):
                return Response({
                    "status": False,
                    "error_message": "Пользователь уже вошел в систему"
                })

            add_session = Session(login=user_login, password=user_password, user_id=search_user_data[0]["id"])
            add_session.save()
            # add_session_data = SessionSerializer(search_user_data, many=True).data

            return Response({
                "status_code": 200,
                "user": search_user_data
            })

        return Response({"error_msg": "user not found"})
    except Exception as e:
        return Response({'er': f'{e}'})


@api_view(["DELETE"])
def logout_view(request):
    try:
        user_login = request.data["login"]
        search_session = Session.objects.filter(login=user_login)

        if search_session:
            search_session.delete()
            return Response({
                "status": "deleted"
            })

        return Response({"error_msg": "user not found"})
    except Exception as e:
        return Response({'er': f'{e}'})

@api_view(["POST"])
def check_session(request):
    try:
        user_login, user_password = request.data["login"], request.data["password"]
        search_session = Session.objects.filter(login=user_login, password=user_password)
        if search_session:
            search_user_data = UserSerializer(Users.objects.filter(login=user_login), many=True).data
            return Response({
                "status_code": 200,
                "status": True,
                "user": search_user_data
            })

        return Response({"error_msg": "user not found"})
    except Exception as e:
        return Response({'er': f'{e}'})


@api_view(["GET"])
def get_files_user(req, user_id):
    files_user = Files.objects.filter(user_id=user_id)
    files_user_data = FileSerializer(files_user, many=True).data
    return Response(files_user_data)

@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        # Проверяем, что файл был загружен
        file = request.FILES["files"]
        user_id = int(request.data.get('user_id')) if request.data.get('user_id') != "undefined" else None

        if not file or not user_id:
            return Response({'error': 'Файл и user_id обязательны.'}, status=status.HTTP_400_BAD_REQUEST)

            # Создаем запись в базе данных
        # files_with_this_name = Files.objects.all()
        files_with_this_name_data = FileSerializer(Files.objects.all(), many=True).data
        prefix = 0
        for elem in files_with_this_name_data:
            if elem["file_name"] == file.name:
                prefix += 1

        if prefix == 0:
            new_file_name = file.name
        else:
            new_file_name = add_postfix(file.name, prefix)

        file_instance = Files(
            file_name=new_file_name,
            file_link="",
            user_id=user_id
        )
        file_instance.save()

            # Сохраняем файл на жестком диске
        file_name = default_storage.save(str(file_instance.id), file)

            # files_return.append(FileSerializer(file_instance).data)

        return Response({ "files": FileSerializer(file_instance).data }, status=status.HTTP_201_CREATED)

    return Response({'error': 'Неверный метод запроса.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

import os
from django.http import HttpResponse, Http404
from django.conf import settings
from .models import Files

@api_view(['GET'])
def download_file(request, id):
    try:
        # Получаем объект файла по ID
        file_obj = Files.objects.get(id=id)
        file_name_in_media = str(FileSerializer(file_obj).data["id"])
        # print(FileSerializer(file_obj).data["id"])
        # Полный путь к файлу
        file_path = os.path.join(settings.MEDIA_ROOT, file_name_in_media)
        print(file_path)
        # Проверяем, существует ли файл
        if not os.path.exists(file_path):
            raise Http404("File does not exist")

        # Открываем файл для чтения в бинарном режиме
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_obj.file_name}"'
            return response
        return Response({"data": 123})
    except Files.DoesNotExist:
        raise Http404("File not found")
    # return Response({"data": id})
