from rest_framework import status
from rest_framework.response import Response
from .models import Holiday
from .serializers import HolidaySerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied



# INSERT INTO Holiday (fromDate, toDate, status, period, description, createdAt, updatedAt, USERID_id)
# VALUES
# ('2024-01-01', '2024-01-01', 6, 1, 'New Year\'s Day', NOW(), NOW(), 3),
# ('2024-02-10', '2024-02-10', 6, 1, 'Chinese New Year', NOW(), NOW(), 3),
# ('2024-03-28', '2024-03-28', 6, 1, 'Maundy Thursday', NOW(), NOW(), 3),
# ('2024-03-29', '2024-03-29', 6, 1, 'Good Friday', NOW(), NOW(), 3),
# ('2024-04-09', '2024-04-09', 6, 1, 'Araw ng Kagitingan', NOW(), NOW(), 3),
# ('2024-05-01', '2024-05-01', 6, 1, 'Labor Day', NOW(), NOW(), 3),
# ('2024-06-12', '2024-06-12', 6, 1, 'Independence Day', NOW(), NOW(), 3),
# ('2024-08-26', '2024-08-26', 6, 1, 'National Heroes Day', NOW(), NOW(), 3),
# ('2024-11-01', '2024-11-01', 6, 1, 'All Saints\' Day', NOW(), NOW(), 3),
# ('2024-12-25', '2024-12-25', 6, 1, 'Christmas Day', NOW(), NOW(), 3),
# ('2024-12-30', '2024-12-30', 6, 1, 'Rizal Day', NOW(), NOW(), 3),
# ('2024-12-31', '2024-12-31', 6, 1, 'New Year\'s Eve', NOW(), NOW(), 3);



class AdminHolidayViewSet(APIView):
     def get(self, request, pk=None, *args, **kwargs):
       
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to view this resource.")
        else:
            # Otherwise, list all holidayss for the user
            holidayss = Holiday.objects.filter(USERID=pk).order_by('fromDate')
            custom_data = []
            for act in holidayss:
                custom_data.append({
                    "holiday_id": act.holiday_id,
                    "fromDate": act.fromDate,
                    "toDate": act.toDate,
                    "status": act.status,
                    "description": act.description,
                    "period":act.period
                })
            return Response(custom_data, status=status.HTTP_200_OK)


class HolidayViewSet(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Handle POST and GET requests for list and creation
    def post(self, request, *args, **kwargs):
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to view this resource.")
        data = request.data.copy()
        if 'USERID' not in data:
            data['USERID'] = request.user.uid
        serializer = HolidaySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, *args, **kwargs):
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to view this resource.")
        if pk:
            # If pk is provided, retrieve a single holiday
            holiday = get_object_or_404(Holiday, pk=pk)
            serializer = HolidaySerializer(holiday)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Otherwise, list all holidayss for the user
            holidayss = Holiday.objects.order_by('fromDate')
            custom_data = []
            for act in holidayss:
                custom_data.append({
                    "holiday_id": act.holiday_id,
                    "fromDate": act.fromDate,
                    "toDate": act.toDate,
                    "status": act.status,
                    "description": act.description,
                    "period":act.period
                })
            return Response(custom_data, status=status.HTTP_200_OK)

    # Handle PUT requests to update an holiday
    def put(self, request, pk, *args, **kwargs):
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to view this resource.")
        holiday = get_object_or_404(Holiday, pk=pk)
        serializer = HolidaySerializer(holiday, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle DELETE requests to delete an holiday
    def delete(self, request, pk, *args, **kwargs):
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to view this resource.")
        use = Holiday.objects
        holiday = get_object_or_404(use, pk=pk)
        holiday.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
