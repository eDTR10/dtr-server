from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Department
from .serializers import DepartmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AdminDeparmentViewSet(APIView):
    permission_classes = [IsAuthenticated]

    # GET: List all departments (Read)
    def get(self, request, *args, **kwargs):
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to view this resource.")
        
        queryset = Department.objects.all().order_by('deptid')
        serializer = DepartmentSerializer(queryset, many=True)
        return Response(serializer.data)

    # POST: Create a new department (Create)
    def post(self, request, *args, **kwargs):
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to create this resource.")
        
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT or PATCH: Update an existing department (Update)
    def put(self, request, pk, *args, **kwargs):
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to update this resource.")
        
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response({"error": "Department not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Remove a department (Delete)
    def delete(self, request, pk, *args, **kwargs):
        if request.user.access_lvl != 14:
            raise PermissionDenied("You do not have permission to delete this resource.")
        
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response({"error": "Department not found."}, status=status.HTTP_404_NOT_FOUND)

        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
