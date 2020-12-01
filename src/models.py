from django.db import models


class Category(models.Model):
    name = models.CharField(default='', max_length=1000)

    def __str__(self):
        return self.name


class City(models.Model):
    city_name = models.CharField(default='', max_length=500)

    def __str__(self):
        return self.city_name


class Ad(models.Model):
    # publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=500)

    def __str__(self):
        return self.name


class Publication(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    publication_name = models.CharField(default='', max_length=1000)
    publication_img = models.ImageField()

    def __str__(self):
        return self.publication_name


class AdType(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    sample_ad_text = models.CharField(default='sample ad text', max_length=2000)
    price = models.IntegerField()

    def __str__(self):
        return str(self.id)


class SampleAds(models.Model):
    ad_type = models.ForeignKey(AdType, on_delete=models.CASCADE)
    ad_text = models.CharField(default='', max_length=1000)

    def __str__(self):
        return str(self.id)
# class Country(models.Model):
#     name = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.name
#
# class City(models.Model):
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.name
#
# class Person(models.Model):
#     name = models.CharField(max_length=100)
#     birthdate = models.DateField(null=True, blank=True)
#     country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
#     city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
#
#     def __str__(self):
#         return self.name
