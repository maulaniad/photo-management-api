from rest_framework.generics import ListCreateAPIView

from api.photo.serializers import ValidateCreatePhotos, PhotoDataSerializer
from api.photo.services import PhotoService
from core.authentication import JWTAuthentication
from helpers import HttpError, StandardPagination, Request, Response


class PhotoView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = PhotoDataSerializer
    pagination_class = StandardPagination
    service = PhotoService

    def get_queryset(self):
        photo_query, _ = self.service.get_photos(self.kwargs['session_id'], lazy=True)
        return photo_query.order_by('-date_created')

    def post(self, request: Request, session_id: str):
        payload = ValidateCreatePhotos(data=request.FILES)

        if not payload.is_valid():
            raise HttpError._400_(payload.errors)

        photos, error = self.service.create_photos(session_id, payload.validated_data['files'])
        if error:
            raise HttpError._500_(error)

        return Response(photos, status=201, message="Photos Uploaded")
