from rest_framework import status
from rest_framework.response import Response
from .models import Activity
from .serializers import ActivitySerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
class AdminActivityViewSet(APIView):
     def get(self, request, pk=None, *args, **kwargs):
        print(pk)
       
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to view this resource.")
        else:
            # Otherwise, list all activities for the user
            activities = Activity.objects.filter(USERID=pk).order_by('activity_id')
            custom_data = []
            for act in activities:
                custom_data.append({
                    "activity_id": act.activity_id,
                    "fromDate": act.fromDate,
                    "toDate": act.toDate,
                    "status": act.status,
                    "description": act.description,
                    "full_name": act.USERID.full_name,
                    "period":act.period
                })
            return Response(custom_data, status=status.HTTP_200_OK)


class ActivityViewSet(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Handle POST and GET requests for list and creation
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'USERID' not in data:
            data['USERID'] = request.user.uid
        serializer = ActivitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            # If pk is provided, retrieve a single activity
            activity = get_object_or_404(Activity, pk=pk)
            serializer = ActivitySerializer(activity)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Otherwise, list all activities for the user
            user_id = kwargs.get('uid', request.user.uid)
            activities = Activity.objects.filter(USERID=user_id).order_by('activity_id')
            custom_data = []
            for act in activities:
                custom_data.append({
                    "activity_id": act.activity_id,
                    "fromDate": act.fromDate,
                    "toDate": act.toDate,
                    "status": act.status,
                    "description": act.description,
                    "full_name": act.USERID.full_name,
                    "period":act.period
                })
            return Response(custom_data, status=status.HTTP_200_OK)

    # Handle PUT requests to update an activity
    def put(self, request, pk, *args, **kwargs):
        activity = get_object_or_404(Activity, pk=pk)
        serializer = ActivitySerializer(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle DELETE requests to delete an activity
    def delete(self, request, pk, *args, **kwargs):
        user_id = kwargs.get('uid', request.user.uid)
        use = Activity.objects.filter(USERID=user_id)
        activity = get_object_or_404(use, pk=pk)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
