from django.core.management.base import BaseCommand
from foods.models import Food
import csv


class Command(BaseCommand):

    help = "Add food nutrient data to database"

    def handle(self, *args, **options):
        with open("data/food_nutrient.csv") as file:
            reader = csv.DictReader(file, delimiter="|")
            for r in reader:
                Food.objects.create(
                    name=r["식품명"],
                    classification=r["식품상세분류"],
                    size=r["1회제공량"],
                    kcal=r["에너지(㎉)"],
                    moisture=r["수분(g)"],
                    protein=r["단백질(g)"],
                    fat=r["지방(g)"],
                    carbohydrate=r["탄수화물(g)"],
                    total_sugar=r["총당류(g)"],
                    dietary_fiber=r["총 식이섬유(g)"],
                    Ca=r["칼슘(㎎)"],
                    Fe=r["철(㎍)"],
                    Mg=r["마그네슘(㎎)"],
                    P=r["인(㎎)"],
                    K=r["칼륨(㎎)"],
                    Na=r["나트륨(㎎)"],
                    Zn=r["아연(㎎)"],
                    Cu=r["구리(㎎)"],
                    Vitamin_D=r["비타민 D(D2+D3)(㎍)"],
                    Vitamin_K=r["비타민 K(㎍)"],
                    Vitamin_B1=r["비타민 B1(㎎)"],
                    Vitamin_B2=r["비타민 B2(㎎)"],
                    Vitamin_B12=r["비타민 B12(㎍)"],
                    Vitamin_C=r["비타민 C(㎎)"],
                    total_amino_acids=r["총 아미노산(㎎)"],
                    essential_amino_acids=r["필수 아미노산(㎎)"],
                    Phenylalanine=r["페닐알라닌(㎎)"],
                    Cholesterol=r["콜레스테롤(㎎)"],
                    total_fatty_acids=r["총 지방산(g)"],
                    total_essential_fatty_acids=r["총 필수 지방산(g)"],
                    total_saturated_fatty_acids=r["총 포화 지방산(g)"],
                    total_polyunsaturated_fatty_acids=r["총 다중 불포화지방산(g)"],
                    Omega_3_fatty_acids=r["오메가 3 지방산(g)"],
                    trans_fatty_acids=r["트랜스 지방산(g)"],
                    folate=r["엽산(㎍)"],
                )
