from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from datetime import date
from checkinout.models import CheckinOut
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from .models import UserAccount
from activity.models import Activity  # Import the Activity model
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .serializers import UserCreateSerializer

User = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page, adjust as needed
    page_size_query_param = 'page_size'  # Allow clients to set the page size with ?page_size=
    max_page_size = 100  # Maximum items per page


class ListUsersViewSummary(APIView):
    def get(self, request, format=None):
        # Fetch all UserAccount entries
        users = UserAccount.objects.all()
        
        # Count the total number of employees
        total_employees = users.count()

        # Get today's date
        today = timezone.localtime().date()

        # Fetch CheckinOut records for today with CHECKTYPE "I"
        checkinouts = CheckinOut.objects.filter(CHECKTIME__date=today, CHECKTYPE="I")
        count_in = checkinouts.count()

        # Check for users celebrating their birthday today
        birthday_celebrants = users.filter(birthday__month=today.month, birthday__day=today.day)
        birthday_celebrants_count = birthday_celebrants.count()

        # **New Logic**: Update User Status Based on Activity
        # Fetch activities for today
        activities_today = Activity.objects.filter(fromDate__lte=today, toDate__gte=today)

        # Update user status based on the related activity
        for activity in activities_today:
            user = activity.USERID  # USERID is the ForeignKey to UserAccount
            if user:
                user.status = activity.status
                user.save()

        # Recalculate the status counts after updates
        in_office_count = users.filter(status=1).count()
        out_of_office_count = users.filter(status=2).count()
        on_travel_count = users.filter(status=3).count()
        on_leave_count = users.filter(status=4).count()
        on_workhome_count = users.filter(status=5).count()

        # Prepare response data
        response_data = {
            'total_employees': total_employees,
            "total_in_today": count_in,
            'birthday_celebrants': UserCreateSerializer(birthday_celebrants, many=True).data,
            'birthday_celebrants_count': birthday_celebrants_count,
            'status_summary': {
                'in_office': in_office_count,
                'out_of_office': out_of_office_count,
                'on_travel': on_travel_count,
                'on_leave': on_leave_count,
                'on_home': on_workhome_count
            }
        }

        return Response(response_data)

      


class UsersDetails(APIView):
    queryset = UserAccount.objects.all()

    def put(self, request, *args, **kwargs):
        user_uid = kwargs.get('uid', request.user.uid)

        if request.user.uid == user_uid:
            try:
                user = UserAccount.objects.get(uid=user_uid)
            except UserAccount.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            data = request.data.copy()  # Create a mutable copy of request.data

            # Handle password hashing
            password = data.get('password')
            print(password)
            if password:
                data['password'] = make_password(password)  # hash the password

            # Initialize serializer with the existing user instance and new data
            serializer = UserCreateSerializer(user, data=data, partial=True)  # partial update
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            print(serializer.errors)  # Log errors for debugging

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)
     

    def get(self, request, *args, **kwargs):
        # Check if the 'uid' is provided in the URL parameters or use request.user.uid
        user_uid = kwargs.get('uid', request.user.uid)

        try:
            # Fetch the specific user by uid
            user = UserAccount.objects.get(uid=user_uid)
        except UserAccount.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare the custom response data for the found user
        custom_data = {
            "email": user.email,
            "full_name": user.full_name,
            "uid": user.uid,
            "card": user.card,
            "access_lvl": user.access_lvl,
            "sex": user.sex,
            "job_title": user.job_title,
            "email2": user.email2,
            "birthday": user.birthday,
            "hiredday": user.hiredday,
            "street": user.street,
            "city": user.city,
            "state": user.state,
            "zip": user.zip,
            "ophone": user.ophone,
            "deptid": user.deptid.deptid,
            "photos": user.photos.url if user.photos and user.photos.name else None,
            "status":user.status
        }

        # Return the response for the specific user
        return Response(custom_data)   
    
class ListUsersViewForReport(APIView):
    def get(self, request, *args, **kwargs):
        # Assuming 'acc_lvl' is a field on the User model
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to view this resource.")
        
        # Query the data and order it by 'attendance_number'
        users = UserAccount.objects.all().order_by('uid')

        # Paginate the query results
        serializer = UserCreateSerializer(users, many=True)
        # Return the paginated response
        return Response(serializer.data) 

class ListUsersView(APIView):

    queryset = UserAccount.objects.all()

    def get(self, request, *args, **kwargs):
        # Assuming 'acc_lvl' is a field on the User model
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to view this resource.")
        
        # Query the data and order it by 'attendance_number'
        users = UserAccount.objects.order_by('uid')

        # Paginate the query results
        paginator = CustomPagination()
        paginated_users = paginator.paginate_queryset(users, request)

        # Prepare the custom response data
        custom_data = []
        for user in paginated_users:
            custom_data.append({
                "email": user.email,
                "full_name": user.full_name,
                "uid": user.uid,
                "card": user.card,
                "access_lvl": user.access_lvl,
                "sex": user.sex,
                "job_title": user.job_title,
                "email2": user.email2,
                "birthday": user.birthday,
                "hiredday": user.hiredday,
                "street": user.street,
                "city": user.city,
                "state": user.state,
                "zip": user.zip,
                "ophone": user.ophone,
                "deptid": user.deptid.deptid,
                "photos": user.photos.url if user.photos and user.photos.name else None,
                "status":user.status
            })

        # Return the paginated response
        return paginator.get_paginated_response(custom_data)
    

    def post(self, request, format=None):
        if request.user.access_lvl == 14:
            users = UserAccount.objects.all()  # Fetch all UserAccount entries
            serializer = UserCreateSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
    
    def put(self, request, id=None, format=None):
        """
        Update a user.
        """
        # Check if the user is a superuser
        if request.user.access_lvl == 14:
            user = User.objects.get(uid=id)
            data = request.data.copy()  # copy the request data

            # Check if the password is in the request data
            password = data.get('password')
            if password:
                data['password'] = make_password(password)  # hash the password

            serializer = UserCreateSerializer(user, data=data, partial=True)  # set partial=True to update a subset of the fields
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
   
# Add this new class after your existing views
class BulkCreateUsersView(APIView):
    def post(self, request, format=None):
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to perform this action.")

        users_data = request.data
        if not isinstance(users_data, list):
            return Response(
                {"detail": "Expected a list of users"},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_users = []
        errors = []

        for user_data in users_data:
            try:
                # Hash password before validation
                if 'password' in user_data:
                    user_data['password'] = make_password(user_data['password'])
                
                serializer = UserCreateSerializer(data=user_data)
                if serializer.is_valid():
                    user = serializer.save()
                    created_users.append(serializer.data)
                else:
                    errors.append({
                        'data': user_data,
                        'errors': serializer.errors
                    })
            except Exception as e:
                errors.append({
                    'data': user_data,
                    'errors': str(e)
                })

        response_data = {
            'created_users': created_users,
            'errors': errors,
            'total_created': len(created_users),
            'total_failed': len(errors)
        }

        if errors:
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
        return Response(response_data, status=status.HTTP_201_CREATED)
# INSERT INTO accounts_useraccount (
#     password,
#     last_login,
#     is_superuser,
#     email,
#     full_name,
#     is_active,
#     is_staff,
#     uid,
#     card,
#     access_lvl,
#     birthday,
#     city,
#     deptid_id,
#     email2,
#     hiredday,
#     job_title,
#     ophone,
#     photos,
#     sex,
#     state,
#     street,
#     zip,
#     status
# ) VALUES 
# (
#     -- Admin user
#     'pbkdf2_sha256$600000$OKwE9jfxntnY02MaQ4TAKH$mrvwzxA84JTMzN1MRdF/Zhupb2WW9tnfswxWZeIjkw4=',
#     NOW(),
#     1,
#     'zero@dict.gov.ph',
#     'Joker',
#     1,
#     1,
#     1000,
#     1000,
#     14,
#     '1990-01-01',
#     'Cagayan de Oro',
#     1,
#     NULL,
#     '2023-01-01',
#     'System Administrator',
#     '09123456789',
#     NULL,
#     'M',
#     'MO',
#     '123 Main St',
#     '9000',
#     1
# ),



