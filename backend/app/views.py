from rest_framework import status
from rest_framework.viewsets import ModelViewSet
import os
from django.http import HttpResponse, Http404
from django.conf import settings
from .models import Files
from app.models import Users, Files, Session
from app.serializers import UserSerializer, FileSerializer, SessionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import uuid


def check_user_session(request):
    cookie_key = "user_session_id"
    session_id = request.COOKIES.get(cookie_key, None)
    if session_id:
        session_user = Session.objects.filter(session_id=session_id)
        if session_user:
            return True

    return False

def set_session_id(response, user_login, user_password, search_user_data):
    cookie_key = "user_session_id"
    new_id = str(uuid.uuid4())
    add_session = Session(session_id=new_id, login=user_login, password=user_password, user_id=search_user_data[0]["id"])
    add_session.save()
    response.set_cookie(
        cookie_key,
        new_id,
        httponly=True,
        samesite='Lax',
        max_age=30 * 24 * 3600
    )
    return response

def delete_session_id(response, user_login):
    search_session = Session.objects.filter(login=user_login)
    if search_session:
        search_session.delete()
        cookie_key = "user_session_id"
        response.delete_cookie(cookie_key)
        return response
    return False



def add_postfix(filename, count):
    dot_index = filename.rfind('.')

    if dot_index <= 0:
        return f"{filename} ({count})"

    name = filename[:dot_index]
    extension = filename[dot_index:]

    return f"{name} (1){extension}"



class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class FilesViewSet(ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FileSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if check_user_session(request):

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

        else:
            return Response({"Error_message": "Ошибка авторизации"}, status=401)

    def create(self, request):
        if check_user_session(request):
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
        else:
            return Response({"Error_message": "Ошибка авторизации"}, status=401)

    def retrieve_by_link(self, request):
        if check_user_session(request):
            try:
                file_link = request.GET.get("link")
                file_instance = Files.objects.get(file_link=file_link)
                serializer = self.get_serializer(file_instance)
                return Response(serializer.data)
            except Files.DoesNotExist:
                return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Error_message": "Ошибка авторизации"}, status=401)



@api_view(['GET'])
def getLinkForFile(request, file_id):
    if check_user_session(request):
        print(request.COOKIES.get("user_session_id", "None"))
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
    else:
        return Response({"Error_message": "Ошибка авторизации"}, status=401)

@api_view(["POST"])
def login_view(request):
    try:
        user_login, user_password = request.data["login"], request.data["password"]
        search_user = Users.objects.filter(login=user_login, password=user_password)
        search_user_data = UserSerializer(search_user, many=True).data
        if search_user_data:
            if Session.objects.filter(login=user_login):
                return Response({
                    "status": 401,
                    "error_message": "Пользователь уже вошел в систему"
                }, status=401)


            return set_session_id(Response({
                "status_code": 200,
                "user": search_user_data
            }), user_login, user_password, search_user_data)

        return Response({"error_msg": "user not found"})
    except Exception as e:
        return Response({'er': f'{e}'}, status=500)


@api_view(["DELETE"])
def logout_view(request):
    try:
        user_login = request.data["login"]
        response = delete_session_id(Response({
                "status": "deleted"
            }, status=204), user_login)

        if response:
            return response

        return Response({"error_msg": "user not found"}, status=401)

    except Exception as e:
        return Response({'er': f'{e}'}, status=500)

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

        return Response({"error_message": "user not found"}, status=401)
    except Exception as e:
        return Response({'er': f'{e}'}, status=500)


@api_view(["GET"])
def get_files_user(request, user_id):
    if check_user_session(request):
        # print(request.COOKIES.get("user_session_id", "None"))
        files_user = Files.objects.filter(user_id=user_id)
        files_user_data = FileSerializer(files_user, many=True).data
        return Response(files_user_data)
    else:
        return Response({"Error_message": "Ошибка авторизации"}, status=401)

@api_view(['POST'])
def upload_file(request):
    if check_user_session(request):
        if request.method == 'POST':
            file = request.FILES["files"]
            user_id = int(request.data.get('user_id')) if request.data.get('user_id') != "undefined" else None

            if not file or not user_id:
                return Response({'error': 'Файл и user_id обязательны.'}, status=status.HTTP_400_BAD_REQUEST)

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

            return Response({ "files": FileSerializer(file_instance).data }, status=status.HTTP_201_CREATED)

        return Response({'error': 'Неверный метод запроса.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return Response({"Error_message": "Ошибка авторизации"}, status=401)

@api_view(['GET'])
def download_file(request, id):
    if check_user_session(request):
        try:
            file_obj = Files.objects.get(id=id)
            file_name_in_media = str(FileSerializer(file_obj).data["id"])
            file_path = os.path.join(settings.MEDIA_ROOT, file_name_in_media)
            print(file_path)
            if not os.path.exists(file_path):
                raise Http404("File does not exist")

            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{file_obj.file_name}"'
                return response
            return Response({"data": 123})
        except Files.DoesNotExist:
            raise Http404("File not found")
    else:
        return Response({"Error_message": "Ошибка авторизации"}, status=401)
