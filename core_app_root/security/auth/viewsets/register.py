import django.contrib
from core_app_root.security import base_url
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import random
import string
from django.views import View
from rest_framework.response import Response
import resend
from core_app_root.security.auth.utils import generate_token
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError,force_str
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from core_app_root.security.auth.serializer.register import RegisterSerializer
# from email_msg_generator.models import OpenAiAdminModel,OpenAiUserModel
# from services.aichat.models im# The commented out lines in the code are likely imports that are not
# currently being used in the codebase. These lines are usually kept
# as comments for reference or in case they need to be re-enabled in
# the future.
from core_app_root.security.user.models import User
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
# from core.wallet.models import UsdModel
from core_app_root.security.auth.serializer.verify_serializer import VerifySerializer
@swagger_auto_schema(
    request_body=RegisterSerializer,
    responses={200: RegisterSerializer}
)

class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    
    def generate_random_link(self,length=20):
        # Define the characters allowed in the link
        characters = string.ascii_letters + string.digits

        # Generate a random link by selecting characters randomly
        random_link = ''.join(random.choice(characters) for _ in range(length))

        return random_link
    
    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        email=str(serializer.initial_data['email'])
        username=str(serializer.initial_data['username'])
        # print(serializer.initial_data['password'])
        password_length=int(len(serializer.initial_data['password']))
        print(password_length)
        print(type(password_length))
        error_list={}
        if not serializer.is_valid():
            print("not valid")
            if User.objects.filter(email=email).exists():
                # return Response({'message':'User with this email already exists','error':True,'field':'email'},status=status.HTTP_403_FORBIDDEN)
                error_list['email_error']='User with this email already exists'
            if password_length<8:
                # print(password_length)
                # print(type(password_length))
                error_list['password_error']='Password should be at least 8 characters'

            
            if User.objects.filter(username=username).exists():
                error_list['username_error']='username exist'
            # if str(serializer.initial_data['confirm_password'])!=str(serializer.initial_data['password']):
                # error_list['password_mismatch_error']='Password mismatch for confirm password'
            if str(serializer.initial_data['password'])!=str(serializer.initial_data['confirm_password']):
                error_list['error_msg']="Password mismatch"
            # error_list['error_msg']='Could not create account'
            error_list['status']=False
            return Response({'error_list':error_list},status=status.HTTP_406_NOT_ACCEPTABLE)
        # if serializer.is_valid():
        else:
            

            print("validated good")
            email=serializer.validated_data['email']

            user=serializer.save()

            # fullname=str(serializer.validated_data['first_name'])+", "+str(serializer.validated_data['last_name'])
            # return render(request,'account/register_done.html',{'fullname':fullname})
            user = get_object_or_404(User, email=email)
        
        # Update the _active field to True
            user.is_active=False
            user.save()
            refresh = RefreshToken.for_user(user)
            # unassigned_keys=OpenAiAdminModel.objects.filter(assigned=False).first()

            # if unassigned_keys:
            #     unassigned_keys.assigned=True

            #     open_api_key=unassigned_keys.open_ai_key

            #     unassigned_keys.save()

            #     OpenAiUserModel.objects.create(user=user,custom_user_key_id=unassigned_keys.custom_user_key_id,open_ai_key=open_api_key,time_of_assiging=timezone.now())
            # User.objects.get(email=request.user.email).is_active=False
            import resend
            resend.api_key = "re_QPQ9uUgC_AQgi1DuGsDWDMTxxUyo88XPi"
            from core_app_root.security.base_url import main_url
            from core_app_root.security import base_url
            full_url=main_url+self.generate_random_link()
            
            r = resend.Emails.send({
            "from": "send@christiankelechieze.com",
            "to": f"{email}",
            "subject": "Account Verification",
            "html": f"""<p>Congrats on Signing up <strong> with Codeblaze Academy</strong> click this link <a href="{base_url.main_url}account/verify/{email}/">{self.generate_random_link()}</a> to verify your account </p>"""
            })
            print("end")
            res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            'user_email':str(serializer.validated_data['email'])
            }
            serializer_data = serializer.data.copy()  # Create a copy of the serializer data
            serializer_data.pop('confirm_password', None) 
            return Response({
                "user": serializer_data,
                "refresh": res["refresh"],
                "token": res["access"],
                'user_email':res['user_email'],
                "is_active":False,
                "status":True,
                "success_msg":"Account creation successful, check email to verify your account"
            }, status=status.HTTP_201_CREATED)   
            
                
    # return Response({'error': 'No unassigned keys available.'}, status=status.HTTP_404_NOT_FOUND)
    # else:
    #     return Response({"error":"User with this Api have an existing api key"},status=status.HTTP_403_FORBIDDEN)
class ActivateAccountView(viewsets.ModelViewSet):
    serializer_class = VerifySerializer
    permission_classes=[AllowAny]
    queryset=User.objects.all()
    http_method_names=['get']
    @action(detail=False, url_path='verify/(?P<email>[^/]+)')
    def verify_account(self, request, email=None):
        # Your logic to activate the account using the email parameter
        user = get_object_or_404(User, email=email)
        
        # Update the _active field to True
        user.is_active=True
        
        user.save()
        return HttpResponseRedirect('https://codeblazeacademy-app.vercel.app/signin')
    
