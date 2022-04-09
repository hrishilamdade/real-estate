from rest_framework import generics,permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import NotYourProfile,ProfileNotFound
from .models import Profile
from .serializers import ProfileSerializer,UpdateProfileSerializer
from .renderers import ProfileJSONRenderer

class AgentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(is_agent=True)
    serializer_class = ProfileSerializer



"""
    from rest_framework import api_view,permissions

    @api_view(['GET'])
    @permission_classes((permissions.IsAuthenticated,))
    def get_all_agents(request):
        agents = Profile.objects.filter(is_agent=True)
        serializer = ProfileSerializer(agents,many=True)
        name_spaced_results = { "agents": serializer.data }
        return Response(name_spaced_results, status=status.HTTP_200_OK)
"""

class TopAgentsListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(top_agent=True)
    serializer_class = ProfileSerializer

class GetProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    def get(self,request):
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile,context={"request":request})
        return Response(serializer.data,status=status.HTTP_200_OK)

class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer

    def patch(self,request,username):
        user = self.request.user
        try:
            Profile.objects.get(user_username = username)
        except Profile.DoesNotExist:
            raise ProfileNotFound
        
        if username != request.user.username: 
            raise NotYourProfile
        
        user_profile = Profile.objects.get(user=user)
        serializer = UpdateProfileSerializer(user_profile,data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
