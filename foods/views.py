from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from foods.models import Food
from foods.serializers import FoodSerializer, FoodsSerializer


class FoodViewSet(ReadOnlyModelViewSet):
    queryset = Food.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            serializer = FoodsSerializer
        else:
            serializer = FoodSerializer
        return serializer

    @action(detail=False)
    def search(self, request):
        name = request.GET.get("name", None)
        size = request.GET.get("size", None)
        kcal = request.GET.get("kcal", None)
        moisture = request.GET.get("moisture", None)
        protein = request.GET.get("protein", None)
        fat = request.GET.get("fat", None)
        carbohydrate = request.GET.get("carbohydrate", None)
        total_sugar = request.GET.get("total_sugar", None)
        dietary_fiber = request.GET.get("dietary_fiber", None)
        Ca = request.GET.get("Ca", None)
        Fe = request.GET.get("Fe", None)
        Mg = request.GET.get("Mg", None)
        P = request.GET.get("P", None)
        K = request.GET.get("K", None)
        Na = request.GET.get("Na", None)
        Zn = request.GET.get("Zn", None)
        Cu = request.GET.get("Cu", None)
        Vitamin_D = request.GET.get("Vitamin_D", None)
        Vitamin_K = request.GET.get("Vitamin_K", None)
        Vitamin_B1 = request.GET.get("Vitamin_B1", None)
        Vitamin_B2 = request.GET.get("Vitamin_B2", None)
        Vitamin_B12 = request.GET.get("Vitamin_B12", None)
        Vitamin_C = request.GET.get("Vitamin_C", None)
        total_amino_acids = request.GET.get("total_amino_acids", None)
        essential_amino_acids = request.GET.get("essential_amino_acids", None)
        Phenylalanine = request.GET.get("Phenylalanine", None)
        Cholesterol = request.GET.get("Cholesterol", None)
        total_fatty_acids = request.GET.get("total_fatty_acids", None)
        total_essential_fatty_acids = request.GET.get(
            "total_essential_fatty_acids", None
        )
        total_saturated_fatty_acids = request.GET.get(
            "total_saturated_fatty_acids", None
        )
        total_polyunsaturated_fatty_acids = request.GET.get(
            "total_polyunsaturated_fatty_acids", None
        )
        Omega_3_fatty_acids = request.GET.get("Omega_3_fatty_acids", None)
        trans_fatty_acids = request.GET.get("trans_fatty_acids", None)
        folate = request.GET.get("folate", None)

        queries = {
            "size": size,
            "kcal": kcal,
            "moisture": moisture,
            "protein": protein,
            "fat": fat,
            "carbohydrate": carbohydrate,
            "total_sugar": total_sugar,
            "dietary_fiber": dietary_fiber,
            "Ca": Ca,
            "Fe": Fe,
            "Mg": Mg,
            "P": P,
            "K": K,
            "Na": Na,
            "Zn": Zn,
            "Cu": Cu,
            "Vitamin_D": Vitamin_D,
            "Vitamin_K": Vitamin_K,
            "Vitamin_B1": Vitamin_B1,
            "Vitamin_B2": Vitamin_B2,
            "Vitamin_B12": Vitamin_B12,
            "Vitamin_C": Vitamin_C,
            "total_amino_acids": total_amino_acids,
            "essential_amino_acids": essential_amino_acids,
            "Phenylalanine": Phenylalanine,
            "Cholesterol": Cholesterol,
            "total_fatty_acids": total_fatty_acids,
            "total_essential_fatty_acids": total_essential_fatty_acids,
            "total_saturated_fatty_acids": total_saturated_fatty_acids,
            "total_polyunsaturated_fatty_acids": total_polyunsaturated_fatty_acids,
            "Omega_3_fatty_acids": Omega_3_fatty_acids,
            "trans_fatty_acids": trans_fatty_acids,
            "folate": folate,
        }

        filter_kwargs = dict()
        if name is not None:
            filter_kwargs["name__contains"] = name
        for key, val in queries.items():
            if val is not None:
                filter_kwargs[f"{key}__gte"] = val
        try:
            foods = Food.objects.filter(**filter_kwargs)
        except ValueError:
            foods = Food.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        results = paginator.paginate_queryset(foods, request)
        serializer = FoodsSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
