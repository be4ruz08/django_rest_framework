from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from olcha.serializers import GroupModelSerializer
from olcha.models import Group


class GroupCreateAPIView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer


class GroupListAPIView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer


# class GroupListAPIView(APIView):
#     def get(self, request, format=None):
#         groups = Group.objects.all()
#         serializer = GroupModelSerializer(groups, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)


class GroupDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    lookup_field = 'slug'
