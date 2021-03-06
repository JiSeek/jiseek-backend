from django.db import models


class Food(models.Model):

    name = models.CharField(max_length=40)
    classification = models.CharField(max_length=40)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    kcal = models.DecimalField(max_digits=10, decimal_places=2)
    moisture = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    protein = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    fat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    carbohydrate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_sugar = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dietary_fiber = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Ca = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Fe = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Mg = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    P = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    K = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Na = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Zn = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Cu = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Vitamin_D = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Vitamin_K = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Vitamin_B1 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Vitamin_B2 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Vitamin_B12 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Vitamin_C = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_amino_acids = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    essential_amino_acids = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    Phenylalanine = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Cholesterol = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_fatty_acids = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_essential_fatty_acids = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    total_saturated_fatty_acids = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    total_polyunsaturated_fatty_acids = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    Omega_3_fatty_acids = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )

    trans_fatty_acids = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    folate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    image1 = models.CharField(max_length=100)
    image2 = models.CharField(max_length=100)
    image3 = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


"""
# food table columns
[
    '?????????': 'name',
    '??????????????????': 'classification',
    '1????????????': 'size',
    '?????????(???)': 'kcal',
    '??????(g)': 'moisture',
    '?????????(g)': 'protein',
    '??????(g)': 'fat',
    '????????????(g)': 'carbohydrate',
    '?????????(g)': 'total_sugar',
    '??? ????????????(g)': 'dietary_fiber',
    '??????(???)': 'Ca',
    '???(???)': 'Fe',
    '????????????(???)': 'Mg',
    '???(???)': 'P',
    '??????(???)': 'K',
    '?????????(???)': 'Na',
    '??????(???)': 'Zn',
    '??????(???)': 'Cu',
    '????????? D(D2+D3)(???)': 'Vitamin_D',
    '????????? K(???)': 'Vitamin_K',
    '????????? B1(???)': 'Vitamin_B1',
    '????????? B2(???)': 'Vitamin_B2',
    '????????? B12(???)': 'Vitamin_B12',
    '????????? C(???)': 'Vitamin_C',
    '??? ????????????(???)': 'total_amino_acids',
    '?????? ????????????(???)': 'essential_amino_acids',
    '???????????????(???)': 'Phenylalanine',
    '???????????????(???)': 'Cholesterol',
    '??? ?????????(g)': 'total_fatty_acids',
    '??? ?????? ?????????(g)': 'total_essential_fatty_acids',
    '??? ?????? ?????????(g)': 'total_saturated_fatty_acids',
    '??? ?????? ??????????????????(g)': 'total_polyunsaturated_fatty_acids',
    '????????? 3 ?????????(g)': 'Omega_3_fatty_acids',
    '????????? ?????????(g)': 'trans_fatty_acids',
    '??????(???)': 'folate',
]
"""
