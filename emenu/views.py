from rest_framework.viewsets import ModelViewSet

from emenu.models import Dish, DishCard
from emenu.serializers import DishSerializer, DishCardSerializer


class DishViewSet(ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DishCardViewSet(ModelViewSet):
    queryset = DishCard.objects.all()
    serializer_class = DishCardSerializer
