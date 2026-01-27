from rest_framework import viewsets, permissions
from .models import Announcement
from .serializers import AnnouncementSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_active=True)
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()] # Or check if user.role == 'MANAGER'
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
