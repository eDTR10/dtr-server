from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from datetime import datetime

from .models import CheckinOutRegion
from .serializers import CheckinOutRegionSerializer
from activity.models import Activity
from holiday.models import Holiday
from accounts.models import UserAccount

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserCheckinOutRegionViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('uid', request.user.uid)
        
        checkinouts = CheckinOutRegion.objects.filter(
            USERID=user_id
        ).order_by('-attendance_number')

        paginator = CustomPagination()
        paginated_checkinouts = paginator.paginate_queryset(checkinouts, request)

        custom_data = [{
            "attendance_number": checkin.attendance_number,
            "CHECKTIME": checkin.CHECKTIME,
            "CHECKTYPE": checkin.CHECKTYPE,
            "USERID": checkin.USERID.uid,
            "full_name": checkin.USERID.full_name
        } for checkin in paginated_checkinouts]

        return paginator.get_paginated_response(custom_data)

class AdminCheckinOutRegionViewSet(viewsets.ModelViewSet):
    queryset = CheckinOutRegion.objects.all()
    serializer_class = CheckinOutRegionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to view this resource.")
        
        checkinouts = CheckinOutRegion.objects.all().order_by('-attendance_number')

        paginated_checkinouts = self.paginate_queryset(checkinouts)
        custom_data = [{
            "attendance_number": checkin.attendance_number,
            "CHECKTIME": checkin.CHECKTIME,
            "CHECKTYPE": checkin.CHECKTYPE,
            "USERID": checkin.USERID.uid,
            "full_name": checkin.USERID.full_name
        } for checkin in paginated_checkinouts]

        return self.get_paginated_response(custom_data)

    @action(detail=False, methods=['get'])
    def today_records(self, request):
        today = timezone.localtime().date()
        
        checkinouts = CheckinOutRegion.objects.filter(
            CHECKTIME__date=today
        ).order_by('-attendance_number')

        custom_data = [{
            "attendance_number": checkin.attendance_number,
            "CHECKTIME": checkin.CHECKTIME,
            "CHECKTYPE": checkin.CHECKTYPE,
            "USERID": checkin.USERID.uid,
            "full_name": checkin.USERID.full_name
        } for checkin in checkinouts]

        return Response(custom_data)

class BulkCreateCheckinOutRegionView(APIView):
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
                user_id = record.get('USERID')
                try:
                    user = UserAccount.objects.get(uid=user_id)
                    record['USERID'] = user.uid
                except UserAccount.DoesNotExist:
                    raise ValueError(f"User with ID {user_id} does not exist")

                serializer = CheckinOutRegionSerializer(data=record)
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