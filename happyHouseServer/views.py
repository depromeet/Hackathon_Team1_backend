import requests, json, os, jwt,

from

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from happyHouseServer.serializers import (
    UserModelSerializer,
    FamilyModelSerializer,
    HouseWorkModelSerializer,
    HouseworkCheckModelSerializer
    )
from django.http import Http404

class UserSignInAPIView(APIView):
    serializer_class = UserModelSerializer

    # [POST] /api/signin 로그인
    def post(self,request, *args, **kwargs):

        is_valid, user_unique_id,user_profile_image, user_nickname = self.is_valid_token(request)


        if (is_valid):
            user_data = {'user_unique_id': user_unique_id, 'user_name': user_nickname, 'user_profile_image':user_profile_image, 'family_id' : None}

            user_data = json.dumps(user_data)
            # print(type(user_data))
            user_data = json.loads(user_data)
            # print(type(user_data))

            serializer = UserModelSerializer(data=user_data)

            if serializer.is_valid():
                serializer.save()
                user_id = serializer.data['id']

                encoded_id = self.get_encoded_id(user_id)


                result_msg = 'SignIn Success'
                result_data = {'user_uid':encoded_id,'nickname': user_nickname, 'profile_url': user_profile_image}

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

        # print(result['id'])

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
                user_profile_image = ""
                user_nickname = result['properties']['nickname']

            return True, user_unique_id, user_profile_image, user_nickname
        else: # 로그인 Failed
            return False, "", ""


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

    def get_encoded_id(self,user_id, *args, **kwargs):
        # payload = {
        #     'str1' : 'depromeet',
        #     'user_id': user_id,
        #     'str2': 'happyhouse'
        # }
        #
        # encoded_id = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')
        #
        # return encoded_id



        return encoded_id


    def signin(self,request, *args, **kwargs):
        is_valid, user_unique_id, user_profile_image, user_nickname = self.is_valid_token(request)






