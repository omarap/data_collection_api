from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProjectAffectedPerson(models.Model):
    project = models.ForeignKey(Project, related_name='project_affected_people', on_delete=models.CASCADE, null = True)
    pap_image = models.ImageField(upload_to='pap_uploads', blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    address = models.CharField(max_length=128)
    nin = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='owners', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.nin}"


class ConstructionName(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='construction_list_names', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ConstructionBuilding(models.Model):
    project = models.ForeignKey(Project, related_name='construction_buildings', on_delete=models.CASCADE, null =True)
    pap = models.ForeignKey(ProjectAffectedPerson, related_name='pap_construction', on_delete=models.CASCADE)
    name = models.ForeignKey(ConstructionName, related_name='list_of_construction', on_delete=models.CASCADE)
    construction_image = models.ImageField(upload_to='construction_uploads', blank=True)
    size = models.FloatField(default=0)
    number_of_construction = models.PositiveSmallIntegerField(default=0)
    rate = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True,null =True)
    updated = models.DateTimeField(auto_now=True, null =True)
    owner = models.ForeignKey(User, related_name='construction_list_owners', on_delete=models.CASCADE)

    def __str__(self):
        return self.name.name


class TreeName(models.Model):
    name = models.CharField(max_length=100)
    rate = models.PositiveIntegerField(default=0, blank=True)
    district = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, related_name='tree_list_owners', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null =True)
    updated = models.DateTimeField(auto_now=True, null =True)

    def __str__(self):
        return self.name


class Tree(models.Model):
    project = models.ForeignKey(Project, related_name='trees', on_delete=models.CASCADE, null =True)
    pap = models.ForeignKey(ProjectAffectedPerson, related_name='pap_trees', on_delete=models.CASCADE)
    name = models.ForeignKey(TreeName, related_name='list_of_trees', on_delete=models.CASCADE)
    description = models.CharField(max_length=50, blank=True)
    tree_image = models.ImageField(upload_to='tree_uploads', blank=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    rate = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null =True)
    updated = models.DateTimeField(auto_now=True, null =True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.name


class CropName(models.Model):
    name = models.CharField(max_length=50)
    rate = models.PositiveIntegerField()
    district = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, related_name='crop_list_owners', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null =True)
    updated = models.DateTimeField(auto_now=True, null =True)

    def __str__(self):
        return f"{self.name} {self.district}"


class Crop(models.Model):
    project = models.ForeignKey(Project, related_name='crops', on_delete=models.CASCADE, null =True)
    crop_name = models.ForeignKey(CropName, related_name='crop_list', on_delete=models.CASCADE)
    crop_image = models.ImageField(upload_to='crop_uploads', blank=True)
    description = models.CharField(max_length=50, blank=True)
    quantity = models.PositiveIntegerField()
    quality = models.CharField(max_length=20)
    rate = models.PositiveIntegerField()
    pap = models.ForeignKey(ProjectAffectedPerson, related_name='pap_crops', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null =True)
    updated = models.DateTimeField(auto_now=True, null =True)

    def __str__(self):
        return f"{self.crop_name} {self.pap} {self.quantity}"


class LandName(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='land_list_owners', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null =True)
    updated = models.DateTimeField(auto_now=True, null =True)

    def __str__(self):
        return self.name


class TenureType(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='user_tenures', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null =True)
    updated = models.DateTimeField(auto_now=True, null =True)

    def __str__(self):
        return self.name


class Land(models.Model):
    project = models.ForeignKey(Project, related_name='lands', on_delete=models.CASCADE, null =True)
    land_type = models.ForeignKey(LandName, related_name='list_of_land', on_delete=models.CASCADE)
    land_image = models.ImageField(upload_to='land_uploads', blank=True)
    survey_no = models.CharField(max_length=200, blank=True, unique=True, null=True)
    pap = models.ForeignKey(ProjectAffectedPerson, related_name='pap_lands', on_delete=models.CASCADE)
    tenure = models.ForeignKey(TenureType, related_name='tenure_types', on_delete=models.CASCADE)
    size = models.FloatField(blank=True)
    location = models.CharField(max_length=255)
    land_use = models.TextField(blank=True)
    land_services = models.TextField(blank=True)
    rate = models.PositiveIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null =True)
    updated = models.DateTimeField(auto_now=True, null =True)
    user = models.ForeignKey(User, related_name='user_lands', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.land_type} {self.pap}"

    @property
    def value_of_land(self):
        return self.size * self.rate
