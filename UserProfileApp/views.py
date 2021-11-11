from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import UserJSONRenderer
from .serializers import (LoginSerializer)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer_data = {}
        for i, item in enumerate(request.data):
            data = request.data.get(item, None)
            if data is not None:
                serializer_data.update({f'{item}': data})
        serializer = self.serializer_class(data=serializer_data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
