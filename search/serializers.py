from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import SearchImage, SearchResult
from foods.models import Food
from django.conf import settings
from darknet.result import get_result


class SearchResultSerializer(ModelSerializer):
    # food = FoodsSerializer()
    photo = SerializerMethodField()

    def get_photo(self, obj):
        photo_key = SearchImage.objects.get(pk=obj.photo.id).photo
        photo = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}{settings.MEDIA_URL}{str(photo_key)}"
        return photo

    class Meta:
        model = SearchResult
        fields = "__all__"


class SearchImageSerializer(ModelSerializer):
    result = SerializerMethodField()
    food = SerializerMethodField()

    def get_result(self, obj):
        photo_key = self.instance.photo
        photo = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}{settings.MEDIA_URL}{str(photo_key)}"
        photo_data = get_result(photo)
        for data in photo_data:
            SearchResult.objects.create(
                class_num=data[0],
                class_name=data[1],
                similarity=data[2],
                x_cord=data[3],
                y_cord=data[4],
                width=data[5],
                height=data[6],
                user=self.instance.user,
                photo=SearchImage.objects.get(photo=photo_key),
                food=Food.objects.get(pk=data[0]),
            )

        result_list = SearchResult.objects.filter(photo_id=obj.id)

        return [res for res in result_list.values()]

    def get_food(self, obj):
        result_list = SearchResult.objects.filter(photo_id=obj.id)
        food_list = [res.get("food_id") for res in result_list.values()]
        res = list()
        for food_id in food_list:
            res.extend(Food.objects.filter(pk=food_id).values())
        return res

    class Meta:
        model = SearchImage
        fields = "__all__"
        read_only_fields = ("id", "user", "result", "food")
