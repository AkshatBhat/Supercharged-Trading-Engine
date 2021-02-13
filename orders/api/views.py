import json

from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics, mixins
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .permissions import IsOwnerOrReadOnly
from .serializers import OrderSerializer, TradeSerializer
from ..models import Order, Trade

class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class TradeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

class TradeAPIView(generics.ListAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def signup(request):
    # print(json.loads(request.body)['username'])
    # print(json.loads(request.body)['password'])
    body = json.loads(request.body)
    email = body['email']
    username = body['username']
    password = body['password']
    user = User.objects.create_user(email=email, username=username, password=password)
    token = Token.objects.create(user=user)
    # print(token.key)
    return Response('Registration successful')