from .models import userProfile
from .serializers import ProfileSerialier, UserSerializer
from django.contrib.auth.models import User
from django.contrib import auth
from core.recommendation import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.



class SignInView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data

        try:
            user = auth.authenticate(username=data['username'], password=data['password'])
            if user is not None:
                auth.login(request, user)
                
                refresh = RefreshToken.for_user(user)
                
                return Response({'message': 'logged in successfully', 'username': data['username'], 
                                'refresh': str(refresh),
                                'access': str(refresh.access_token)})
            else:
                return Response({'message': 'error in credentials'})
        except:
            return Response({'error':'error in sign in'}) 

class SignOutView(APIView):

    def post(self, request):
        try:
            auth.logout(request)
            return Response({'message': 'logged out'})
        except:
            Response({'error':'error when logging out'})


###use seesion to get current user
class RecommendMealView(APIView):
    
    def post(self, request, format=None):
        
        try:
            user = self.request.user
            data = request.data
            user = User.objects.get(id=user.id)
            profile = userProfile.objects.get(user = user)
            serializer = ProfileSerialier(profile)
            rec_food = recommendmeal( time=data['time'], username=user.username)
            macro_nut = calculate_user_macronutrients(user_name=user.username)
            return Response(
                {
                    "user":user.username,
                    "time":data['time'],
                    "nutrition format" : "energy(kcal),carbohydrate(gm),fats(gm),protein(gm)",
                    "recommended calories": macro_nut[0],
                    "recommended carbohydrates(gm) min":macro_nut[1],
                    "recommended carbohydrates(gm) max":macro_nut[2],
                    "recommended fats(gm) min":macro_nut[3],
                    "recommended fats(gm) max":macro_nut[4],
                    "recommended protein(gm) min":macro_nut[5],
                    "recommended protein(gm) max":macro_nut[6],
                    "food":rec_food
                }
                )
        except:
            return Response({'error':'error in recommend meal'})

class RateMealView(APIView):
   
    def post(self, request, format=None):
        
        try:
            user = self.request.user
            data = request.data
            user = User.objects.get(id=user.id)
            profile = userProfile.objects.get(user = user)
            serializer = ProfileSerialier(profile)
            give_rating(rec_food=data['food'],user_name=user.username, rating=data['rating'], time=data['time'])
            return Response(
                {
                    "food":data['food'],
                    "rating":data['rating']
                }
            )
        except:
            return Response({'error':'error in rate meal'})

class GetHistoryView(APIView):
   
    def post(self, request, format=None):
        try:
            user = self.request.user
            user = User.objects.get(id=user.id)
            history = load_req_data('user_data.csv')
            history = history[history.username == user.username]
            history = history.drop('username',axis=1)
            history_dict = history.to_dict('list')
            return Response(
                {
                    "user":user.username,
                    "history":history_dict
                }
            )
        except:
            return Response({'error':'error in getting history'})




class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        try:
            if data['password1'] == data['password2']:
                try:
                    user = User.objects.get(username=data['username'])
                    return Response({'message': 'username exists'}, status=status.HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password1'])
                    userprofile = userProfile.objects.create(user=user, height=data['height'], weight=data['weight'], age=data['age'],
                    sex=data['sex'], lifestyle=data['lifestyle'], tags=data['tags'], diet=data['diet'], disease=data['disease'], allergy=data['allergy'])
                    userprofile.save()
                    userinfo = user_dataframe(username=data['username'], name=data['username'], age=data['age'], weight=data['weight'],
                    height=data['height'], sex=data['sex'], lifestyle=data['lifestyle'], tags=data['tags'], diet=data['diet'],
                    disease=data['disease'], allergy=data['allergy'])
                    load_data_to_csv('user_info.csv', userinfo)
                    return Response({'message': 'user created'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error':'passwords do not match'})
            return Response({'message': 'error in creation'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error':'something went wrong in signing up user'})

class UserDetails(APIView):
    
    # def get_object(self,request):
    #     try:
    #         user = self.request.user
    #         user = User.objects.get(id=user.id)
    #         profile = userProfile.objects.get(user=user)
    #         return user, profile
    #     except User.DoesNotExist:
    #         raise NotFound(detail='User not found')

    def post(self, request, format = None):
        try:
            user = self.request.user
            user = User.objects.get(id=user.id)
            profile = userProfile.objects.get(user=user)
            userserializer = UserSerializer(user)
            serializer = ProfileSerialier(profile)
            return Response(
                    serializer.data
                )
        except:
            return Response({'error':'something went wrong in fetchin user'})
    def delete(self, request, format = None):
        try:
            user = self.request.user
            user = User.objects.get(id=user.id)
            profile = userProfile.objects.get(user=user)
            user_df = load_req_data('user_info.csv')
            user_df = user_df[user_df.username != user.username]
            write_data_to_csv('user_info.csv', user_df)
            user.delete()
            return Response({'message': 'deleted'})
        except:
            return Response({'error':'something went wrong in deleting user'})

    def put(self, request, format = None):
        try:
            user = self.request.user
            user = User.objects.get(id=user.id)
            profile = userProfile.objects.get(user=user)
            data = request.data
            profile.height = data['height']
            profile.weight = data['weight']
            profile.age = data['age']
            profile.sex = data['sex']
            profile.diet = data['diet']
            profile.lifestyle = data['lifestyle']
            profile.tags = data['tags']
            profile.disease = data['disease']
            profile.allergy = data['allergy']
            profile.save()
            user_df = load_req_data('user_info.csv')
            user_df = user_df[user_df.username != user.username]
            userinfo = user_dataframe(username=user.username, name=user.username, age=data['age'], weight=data['weight'],
                    height= data['height'], sex= data['sex'], lifestyle=data['lifestyle'], tags=data['tags'], diet=data['diet'],
                    disease=data['disease'], allergy=data['allergy'])
            new_info = pd.concat([user_df,userinfo], ignore_index=True)
            write_data_to_csv('user_info.csv', new_info)
            userserializer = UserSerializer(user)
            serializer = ProfileSerialier(profile)
            return Response(
                    serializer.data
                )
        except:
            return Response({'error':'something went wrong in putting user details'})


class ProfileListView(APIView):
    
    def get(self, request, format = None):
        try:
            profiles = userProfile.objects.all()
            serializer = ProfileSerialier(profiles, many=True)
            return Response(serializer.data)
        except:
            return Response({'error':'something went wrong in profile list view'})

class UsersListView(APIView):
    def get(self, request, format = None):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except:
            return Response({'error':'something went wrong in user list view'})


"""
class UserFoodView(APIView):
    def put(self, request, form=None):
        user = self.request.user
        user = User.objects.get(id=user.id)
        profile = userProfile.objects.get(user=user)
        data = request.data
        userfood = food_dataframe(user_name=user.username, name=data['name'], description=data['description'], 
        nutrition, ingredient, time, diet, type_food)"""