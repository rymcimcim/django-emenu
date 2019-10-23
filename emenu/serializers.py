from rest_framework.serializers import ModelSerializer

from emenu.models import Dish, DishCard


class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'prep_time', 'vegetarian']


class DishCardSerializer(ModelSerializer):
    dishes = DishSerializer(many=True, required=False)

    class Meta:
        model = DishCard
        fields = ['id', 'name', 'description', 'dishes']

    def create(self, validated_data):
        dishes_data = validated_data.pop('dishes', None)
        dish_card = DishCard.objects.create(**validated_data)

        try:
            for dish_data in dishes_data:
                dish_card.dishes.create(**dish_data)
        except TypeError:
            pass

        return dish_card

    def update(self, instance, validated_data):
        dishes_data = validated_data.pop('dishes', None)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        try:
            for dish_data in dishes_data:
                instance.dishes.create(**dish_data)
        except TypeError:
            pass

        instance.save()
        return instance
