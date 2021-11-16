from django.db import models


class Food(models.Model):

    name = models.CharField(max_length=40)
    classification = models.DecimalField(max_digits=30, decimal_places=20)
    size = models.DecimalField(max_digits=30, decimal_places=20)
    kcal = models.DecimalField(max_digits=30, decimal_places=20)
    moisture = models.DecimalField(max_digits=30, decimal_places=20)
    protein = models.DecimalField(max_digits=30, decimal_places=20)
    fat = models.DecimalField(max_digits=30, decimal_places=20)
    carbohydrate = models.DecimalField(max_digits=30, decimal_places=20)
    Total = models.DecimalField(max_digits=30, decimal_places=20)
    dietary_fiber = models.DecimalField(max_digits=30, decimal_places=20)
    Ca = models.DecimalField(max_digits=30, decimal_places=20)
    Fe = models.DecimalField(max_digits=30, decimal_places=20)
    Mg = models.DecimalField(max_digits=30, decimal_places=20)
    P = models.DecimalField(max_digits=30, decimal_places=20)
    K = models.DecimalField(max_digits=30, decimal_places=20)
    Na = models.DecimalField(max_digits=30, decimal_places=20)
    Zn = models.DecimalField(max_digits=30, decimal_places=20)
    Cu = models.DecimalField(max_digits=30, decimal_places=20)
    Vitamin_D = models.DecimalField(max_digits=30, decimal_places=20)
    Vitamin_K = models.DecimalField(max_digits=30, decimal_places=20)
    Vitamin_B1 = models.DecimalField(max_digits=30, decimal_places=20)
    Vitamin_B2 = models.DecimalField(max_digits=30, decimal_places=20)
    Vitamin_B12 = models.DecimalField(max_digits=30, decimal_places=20)
    Vitamin_C = models.DecimalField(max_digits=30, decimal_places=20)
    total_amino_acids = models.DecimalField(max_digits=30, decimal_places=20)
    essential_amino_acids = models.DecimalField(max_digits=30, decimal_places=20)
    Phenylalanine = models.DecimalField(max_digits=30, decimal_places=20)
    Cholesterol = models.DecimalField(max_digits=30, decimal_places=20)
    total_fatty_acids = models.DecimalField(max_digits=30, decimal_places=20)
    total_essential_fatty_acids = models.DecimalField(max_digits=30, decimal_places=20)
    total_saturated_fatty_acids = models.DecimalField(max_digits=30, decimal_places=20)
    total_polyunsaturated_fatty_acids = models.DecimalField(
        max_digits=30, decimal_places=20
    )
    Omega_3_fatty_acids = models.DecimalField(max_digits=30, decimal_places=20)
    trans_fatty_acids = models.DecimalField(max_digits=30, decimal_places=20)
    folate = models.DecimalField(max_digits=30, decimal_places=20)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


"""
# food table columns
[
    '식품명': 'name',
    '식품상세분류': 'classification',
    '1회제공량': 'size',
    '에너지(㎉)': 'kcal',
    '수분(g)': 'moisture',
    '단백질(g)': 'protein',
    '지방(g)': 'fat',
    '탄수화물(g)': 'carbohydrate',
    '총당류(g)': 'Total sugar',
    '총 식이섬유(g)': 'dietary_fiber',
    '칼슘(㎎)': 'Ca',
    '철(㎍)': 'Fe',
    '마그네슘(㎎)': 'Mg',
    '인(㎎)': 'P',
    '칼륨(㎎)': 'K',
    '나트륨(㎎)': 'Na',
    '아연(㎎)': 'Zn',
    '구리(㎎)': 'Cu',
    '비타민 D(D2+D3)(㎍)': 'Vitamin_D',
    '비타민 K(㎍)': 'Vitamin_K',
    '비타민 B1(㎎)': 'Vitamin_B1',
    '비타민 B2(㎎)': 'Vitamin_B2',
    '비타민 B12(㎍)': 'Vitamin_B12',
    '비타민 C(㎎)': 'Vitamin_C',
    '총 아미노산(㎎)': 'total_amino_acids',
    '필수 아미노산(㎎)': 'essential_amino_acids',
    '페닐알라닌(㎎)': 'Phenylalanine',
    '콜레스테롤(㎎)': 'Cholesterol',
    '총 지방산(g)': 'total_fatty_acids',
    '총 필수 지방산(g)': 'total_essential_fatty_acids',
    '총 포화 지방산(g)': 'total_saturated_fatty_acids',
    '총 다중 불포화지방산(g)': 'total_polyunsaturated_fatty_acids',
    '오메가 3 지방산(g)': 'Omega_3_fatty_acids',
    '트랜스 지방산(g)': 'trans_fatty_acids',
    '엽산(㎍)': 'folate',
]
"""
