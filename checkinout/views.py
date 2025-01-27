from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import CheckinOut
from activity.models import Activity
from holiday.models import Holiday



from django.utils import timezone
from .serializers import CheckinOutSerializer
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .serializers import CheckinOutSerializer
from .models import CheckinOut
from accounts.models import UserAccount

class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page, adjust as needed
    page_size_query_param = 'page_size'  # Allow clients to set the page size with ?page_size=
    max_page_size = 100  # Maximum items per page
class UserCheckinOutViewSet(APIView):
    queryset = CheckinOut.objects.all().order_by('-attendance_number')
    serializer_class = CheckinOutSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('uid', request.user.uid)
        # Assuming 'acc_lvl' is a field on the User model
        
        
        # Query the data and order it by 'attendance_number'
        checkinouts = CheckinOut.objects.filter(USERID=user_id).order_by('-attendance_number')

        # Paginate the query results
        paginator = CustomPagination()
        paginated_checkinouts = paginator.paginate_queryset(checkinouts, request)

        # Prepare the custom response data
        custom_data = []
        for checkin in paginated_checkinouts:
            custom_data.append({
                "attendance_number": checkin.attendance_number,
                "CHECKTIME": checkin.CHECKTIME,
                "CHECKTYPE": checkin.CHECKTYPE,
                "USERID": checkin.USERID.uid,  
                "full_name": checkin.USERID.full_name  
            })

        # Return the paginated response
        return paginator.get_paginated_response(custom_data)

    def post(self, request, **kwargs):
        user_id = kwargs.get('uid', request.user.uid)
        from_date = request.data.get('fromDate')
        to_date = request.data.get('toDate')

        # if not user_id or not from_date or not to_date:
        #     return Response({"error": "Please provide userId, fromDate, and toDate"}, status=400)

        try:
            # Parse the from_date and to_date from the request body
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        # Filter CheckinOut records by USERID and date range
        checkinouts = CheckinOut.objects.filter(
            USERID=user_id,
            CHECKTIME__date__gte=from_date,
            CHECKTIME__date__lte=to_date
        ).order_by('attendance_number')

        # Query the Activity data for the user within the date range
        activities = Activity.objects.filter(
            USERID=user_id,
            fromDate__lte=to_date,
            toDate__gte=from_date
        ).order_by('-createdAt')
        holidays = Holiday.objects.filter(
            fromDate__lte=to_date,
            toDate__gte=from_date
        ).order_by('-createdAt')

        # Prepare the checkinout data
        checkinout_data = [
            {
                "attendance_number": checkin.attendance_number,
                "CHECKTIME": checkin.CHECKTIME,
                "CHECKTYPE": checkin.CHECKTYPE,
                "USERID": checkin.USERID.uid,
                "full_name": checkin.USERID.full_name
            }
            for checkin in checkinouts
        ]

        # Prepare the activity data
        activity_data = [
            {
                "activity_id": activity.activity_id,
                "fromDate": activity.fromDate,
                "toDate": activity.toDate,
                "status": activity.status,
                "period":activity.period,
                "description": activity.description,
            }
            for activity in activities
        ]

        holidays_data = [
            {
                "holiday_id": holiday.holiday_id,
                "fromDate": holiday.fromDate,
                "toDate": holiday.toDate,
                "status": holiday.status,
                "period":holiday.period,
                "description": holiday.description,
            }
            for holiday in holidays
        ]
        for holiday in holidays:
            activity_data.append({
                "activity_id": holiday.holiday_id,  # Use holiday_id as activity_id
                "fromDate": holiday.fromDate,
                "toDate": holiday.toDate,
                "status": holiday.status,
                "period": holiday.period,
                "description": holiday.description,
            })

        # Return the response in the desired format
        return Response({
            "results": checkinout_data,
            "activities": activity_data,
            "holidays":holidays_data
        })
class AdminCheckinOutViewSet(viewsets.ModelViewSet):
    queryset = CheckinOut.objects.all().order_by('-attendance_number')
    serializer_class = CheckinOutSerializer
    permission_classes = [IsAuthenticated]

    # Override the list method to restrict access to users with acc_lvl=14
    def list(self, request, *args, **kwargs):
        # Assuming 'acc_lvl' is a field on the User model
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to view this resource.")
        
        # Query the data and order it by 'attendance_number'
        checkinouts = CheckinOut.objects.order_by('-attendance_number')

        # Paginate the query results
        paginator = CustomPagination()
        paginated_checkinouts = paginator.paginate_queryset(checkinouts, request)

        # Prepare the custom response data
        custom_data = []
        for checkin in paginated_checkinouts:
            custom_data.append({
                "attendance_number": checkin.attendance_number,
                "CHECKTIME": checkin.CHECKTIME,
                "CHECKTYPE": checkin.CHECKTYPE,
                "USERID": checkin.USERID.uid,  
                "full_name": checkin.USERID.full_name  
            })

        # Return the paginated response
        return paginator.get_paginated_response(custom_data)

    # Additional custom action to filter by the current user's USERID
    @action(detail=False, methods=['get'])
    def by_user(self, request, *args, **kwargs):
        user_id = kwargs.get('uid', request.user.uid)
        checkinouts = CheckinOut.objects.filter(USERID=user_id).order_by('-attendance_number')
        paginator = CustomPagination()
        paginated_checkinouts = paginator.paginate_queryset(checkinouts, request)
        # Prepare the custom response data
        custom_data = []
        for checkin in paginated_checkinouts:
            custom_data.append({
                "attendance_number": checkin.attendance_number,
                "CHECKTIME": checkin.CHECKTIME,
                "CHECKTYPE": checkin.CHECKTYPE,
                "USERID": checkin.USERID.uid,  
                "full_name": checkin.USERID.full_name  
            })

        # Return the paginated response
        return paginator.get_paginated_response(custom_data)
     
    
    def today_records(self, request):

        # Get the current date
        today = timezone.localtime().date()
        print(today)

        # Filter CheckinOut records for the current date and include related UserAccount info
        checkinouts = CheckinOut.objects.filter(CHECKTIME__date=today).order_by('-attendance_number')

        # Prepare the custom response data
        custom_data = []
        for checkin in checkinouts:
            custom_data.append({
                "attendance_number": checkin.attendance_number,
                "CHECKTIME": checkin.CHECKTIME,
                "CHECKTYPE": checkin.CHECKTYPE,
                "USERID": checkin.USERID.uid,  
                "full_name": checkin.USERID.full_name  
            })

        # Return the custom response data
        return Response(custom_data)
    @action(detail=False, methods=['post'], url_path='filter_by_user_date')
    def filter_by_user_date(self, request):
        user_id = request.data.get('userId')
        from_date = request.data.get('fromDate')
        to_date = request.data.get('toDate')

        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to view this resource.")

        if not user_id or not from_date or not to_date:
            return Response({"error": "Please provide userId, fromDate, and toDate"}, status=400)

        try:
            # Parse the from_date and to_date from the request body
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        # Filter CheckinOut records by USERID and date range
        checkinouts = CheckinOut.objects.filter(
            USERID=user_id,
            CHECKTIME__date__gte=from_date,
            CHECKTIME__date__lte=to_date
        ).order_by('attendance_number')

        # Query the Activity data for the user within the date range
        activities = Activity.objects.filter(
            USERID=user_id,
            fromDate__lte=to_date,
            toDate__gte=from_date
        ).order_by('-createdAt')

        # Query the Holiday data for the user within the date range
        holidays = Holiday.objects.filter(
            fromDate__lte=to_date,
            toDate__gte=from_date
        ).order_by('-createdAt')

        # Prepare the checkinout data
        checkinout_data = [
            {
                "attendance_number": checkin.attendance_number,
                "CHECKTIME": checkin.CHECKTIME,
                "CHECKTYPE": checkin.CHECKTYPE,
                "USERID": checkin.USERID.uid,
                "full_name": checkin.USERID.full_name
            }
            for checkin in checkinouts
        ]

        # Prepare the activity data
        activity_data = [
            {
                "activity_id": activity.activity_id,
                "fromDate": activity.fromDate,
                "toDate": activity.toDate,
                "status": activity.status,
                "period": activity.period,
                "description": activity.description,
            }
            for activity in activities
        ]

        # Prepare the holiday data and merge it into the activity data
        for holiday in holidays:
            activity_data.append({
                "activity_id": holiday.holiday_id,  # Use holiday_id as activity_id
                "fromDate": holiday.fromDate,
                "toDate": holiday.toDate,
                "status": holiday.status,
                "period": holiday.period,
                "description": holiday.description,
            })

        # Return the response with merged activities and an empty holidays array
        return Response({
            "results": checkinout_data,
            "activities": activity_data,  # Merged activities and holidays
        })

    

    @action(detail=False, methods=['get'], url_path='my_records')
    def my_records(self, request):

        checkinouts = CheckinOut.objects.filter(USERID=request.user.uid).order_by('-attendance_number')
        serializer = self.get_serializer(checkinouts, many=True)
        return Response(serializer.data)
class BulkCreateCheckinOutView(APIView):
    def post(self, request, format=None):
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to perform this action.")

        records_data = request.data
        if not isinstance(records_data, list):
            return Response(
                {"detail": "Expected a list of records"},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_records = []
        errors = []

        for record in records_data:
            try:
                # Get the user instance
                user_id = record.get('USERID')
                try:
                    user = UserAccount.objects.get(uid=user_id)
                    record['USERID'] = user.uid
                except UserAccount.DoesNotExist:
                    raise ValueError(f"User with ID {user_id} does not exist")

                serializer = CheckinOutSerializer(data=record)
                if serializer.is_valid():
                    checkinout = serializer.save()
                    created_records.append(serializer.data)
                else:
                    errors.append({
                        'data': record,
                        'errors': serializer.errors
                    })
            except Exception as e:
                errors.append({
                    'data': record,
                    'errors': str(e)
                })

        response_data = {
            'created_records': created_records,
            'errors': errors,
            'total_created': len(created_records),
            'total_failed': len(errors)
        }

        if errors:
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
        return Response(response_data, status=status.HTTP_201_CREATED)