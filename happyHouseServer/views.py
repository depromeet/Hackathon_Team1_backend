import requests, json, os, jwt,base64

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from happyHouseServer.models import User

from happyHouseServer.serializers import (
    UserModelSerializer,
    FamilyModelSerializer,
    HouseWorkModelSerializer,
    HouseworkCheckModelSerializer
    )
from django.http import Http404

from happyHouseServer.logger_handler import LoggerHandler

class UserSignInAPIView(APIView):
    serializer_class = UserModelSerializer

    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    # [POST] /api/signin 로그인
    def post(self,request, *args, **kwargs):

        is_valid, user_unique_id, user_profile_image, user_nickname = self.is_valid_token(request)

        user_pk = self.signin(user_unique_id)

        if user_pk != 0:
            encoded_num = self.get_encoded_num(user_pk)

            result_msg = 'SignIn Success'
            result_data = {'user_uid': encoded_num, 'nickname': user_nickname, 'profile_url': user_profile_image}

            return Response({'msg': result_msg, 'result': result_data}, status=status.HTTP_200_OK)


        if (is_valid):
            family_data = {'family_name':"family"}
            family_serializer = FamilyModelSerializer(data=family_data)

            if family_serializer.is_valid():
                family_serializer.save()
                # LoggerHandler.server_logger.debug(family_serializer.data)
                family_id = family_serializer.data['id']
                LoggerHandler.server_logger.debug(family_id)
            else:
                family_serializer.errors()


            user_data = {'user_unique_id': user_unique_id, 'user_name': user_nickname, 'user_profile_image':user_profile_image, 'family_id' : family_id}

            user_data = json.dumps(user_data)
            # print(type(user_data))
            LoggerHandler.server_logger.debug(user_data)
            user_data = json.loads(user_data)
            # print(type(user_data))

            serializer = UserModelSerializer(data=user_data)

            if serializer.is_valid():
                serializer.save()
                user_id = str(serializer.data['id'])

                # encoded_id = self.get_encoded_id(user_id)

                encoded_num = self.get_encoded_num(user_id)

                user_profile_image = serializer.data['user_profile_image']

                result_msg = 'SignIn Success'
                result_data = {'user_uid':encoded_num,'nickname': user_nickname, 'profile_url': user_profile_image}

            else:
                serializer.errors()
                return Response({'msg':'Server Error'}, status=status.HTTP_200_OK)

        else:
            result_msg = 'SignIn Failed'

        return Response({'msg':result_msg, 'result':result_data}, status=status.HTTP_200_OK)


    def is_valid_token(self,request, *args,**kwargs):
        # access_token = 'vV7SBtxY6pvCyuODZFoltdXVLSyIzRayanqmlAo9dZsAAAFqg0iMnw'

        # access_token = 'Z2YLCsIYOqHB8FhjnCFhhbrEmJhVn7dRr82Gygo9dZoAAAFqgw66tQ'
        access_token = request.data['access_token']

        access_token = 'Bearer '+access_token

        headers = {'Authorization' : access_token}

        r = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)

        result = r.json()

        # print(result)

        result = json.dumps(result)
        result = json.loads(result)


        if not (self.is_errmsg_exist(result)): # 로그인 Suceess
            user_data = {'user_unique_id':result['id'], 'user_name': result['properties']['nickname']}
            # print(user_data)
            user_unique_id = result['id']

            if self.is_profile_exist(result['properties']):
                user_profile_image = result['properties']['profile_image']
                user_nickname = result['properties']['nickname']
               # print("dddddddd")
               # print(user_profile_image)
            else:
                user_profile_image = None
                user_nickname = result['properties']['nickname']

            return True, user_unique_id, user_profile_image, user_nickname
        else: # 로그인 Failed
            return False, None, None, None


    def is_errmsg_exist(self,result, *args, **kwargs):
        if hasattr(result, 'msg'):
            return True
        else:
            return False

    def is_profile_exist(self, result, *args, **kwargs):
        if 'profile_image' in result:
            return True
        else:
            return False

    # def get_encoded_id(self,user_id, *args, **kwargs):
    #     # payload = {
    #     #     'str1' : 'depromeet',
    #     #     'user_id': user_id,
    #     #     'str2': 'happyhouse'
    #     # }
    #     #
    #     # encoded_id = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')
    #     #
    #     # return encoded_id
    #     # key = "depromeet" + str(user_id) + "happyhouse"
    #
    #     barr = bytes(user_id, 'utf-8')
    #     print(barr)
    #     print(type(barr))
    #
    #     cipher_text = self.cipher_suite.encrypt(barr)
    #     # plain_text = cipher_suite.decrypt(cipher_text)
    #
    #     print(cipher_text)
    #
    #     return cipher_text
    #
    # def get_decrypted_id(self,encrypted_id,*args,**kwargs):
    #     decoded_id = self.cipher_suite.decrypt(encrypted_id)
    #     return decoded_id


    def signin(self,user_unique_id, *args, **kwargs):
        serializer = UserModelSerializer
        try:
            query = User.objects.get(user_unique_id=user_unique_id)
            return query.pk
        except:
            return 0


    def get_encoded_num(self, user_id, *args, **kwargs):
        encoded_num = 256780+int(user_id)
        return encoded_num

    def get_decoded_num(self, encoded_num, *args, **kwargs):
        decoded_num = encoded_num - 256780
        return decoded_num


class AddHouseworkAPIView(APIView):
    # [POST] /api/task 할 일 추가
    def post(self, request, *args, **kwargs):
        housework_name = request.data['housework_name']
        assignee_id = request.data['assignee_id']

        LoggerHandler.server_logger.debug(assignee_id)

        assignee_id = UserSignInAPIView.get_decoded_num(self,int(request.data['assignee_id']))

        LoggerHandler.server_logger.debug(housework_name)
        LoggerHandler.server_logger.debug(assignee_id)

        housework_data = {'housework_name': housework_name, 'assignee_id': assignee_id}

        housework_data = json.dumps(housework_data)
        LoggerHandler.server_logger.debug(housework_data)
        housework_data = json.loads(housework_data)

        serializer = HouseWorkModelSerializer(data=housework_data)

        if serializer.is_valid():
            serializer.save()

            housework_id = serializer.data['id']
            created_time = serializer.data['created_time']
            housework_name = serializer.data['housework_name']
            assignee_id = serializer.data['assignee_id']

            assignee_id = UserSignInAPIView.get_encoded_num(self,assignee_id)


            LoggerHandler.server_logger.debug(created_time)
            LoggerHandler.server_logger.debug(housework_id)

            result_data = {'housework_id':housework_id, 'housework_name':housework_name,'assignee_id':assignee_id,'created_time':created_time}
            result_data = json.dumps(result_data)
            result_data = json.loads(result_data)

        else:
            serializer.errors()

            return Response({'msg': 'Server Error'}, status=status.HTTP_200_OK)

        return Response({'msg': 'Create Housework Success', 'result': result_data}, status=status.HTTP_200_OK)


class HouseWorkListAPIView(APIView):
    # [POST] /api/tasklist 할 일 리스트 보기
    # def post(self,request, *args,**kwargs):
    pass


class ShareAPIView(APIView):
    # [POST] /api/share/{userId} 할 일 리스트 보기
    def post(self,request, *args, **kwargs):
        sharing_user_id = request.data['sharing_user_id'] # 공유할 사용자 id






