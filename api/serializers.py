from django.template import Context
from rest_framework import serializers
from rest_framework import *
from .models import *
from django.db.models.fields import *
import django_filters
from .filters import ConstructionBuildingFilter  # Import the filter class


#project serializer
class PSerializer(serializers.ModelSerializer):
    class Meta:
            model = Project
            fields = '__all__'  # You can specify the fields you want to include if not all fields are needed

        
    def create(self, validated_data):
        """
        Create and return a new `Project` instance, given the validated data.
        """
        return Project.objects.create(**validated_data)

# function to limit paps to current user i.e. pap owner or view only your created pap
class UserPap(serializers.SlugRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        paps = ProjectAffectedPerson.objects.all()

        if user.is_staff:  # Check if the user is an admin
            return paps  # Return all records for admin users
        else:
            return paps.filter(owner=user)  # Filter by the requesting user for non-admin users


    def get_search_results(self, queryset, search_term, request):
        # owner = self.request.user
        owner = self.context['request'].user
        queryset, use_distinct = super().get_search_results(queryset, search_term, request)
        paps = ProjectAffectedPerson.objects.all()
        queryset = paps.filter(owner=owner)
        return queryset, use_distinct


    


#construction serializer
class ConstructionListSerialier(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = ConstructionName
        fields = ['project', 'name', 'created', 'updated']

    def create(self, validated_data):
        """
        Create and return a new `ConstructionList` instance, given the validated data.
        """
        return ConstructionName.objects.create(**validated_data)


class ConstructionBuildingSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    pap = UserPap(queryset=ProjectAffectedPerson.objects.all(), slug_field='first_name')
    name = serializers.SlugRelatedField(queryset=ConstructionName.objects.all(), slug_field='name')

    class Meta:
        model = ConstructionBuilding
        fields = ['project', 'pap', 'name', 'construction_image', 'size', 'number_of_construction',
                  'rate', 'value_of_structures', 'created', 'updated']

    def create(self, validated_data):
        """
        Create and return a new `ConstructionBuilding` instance, given the validated data.
        """
        return ConstructionBuilding.objects.create(**validated_data)


# Construction search serializer
class ConstructionSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionBuilding
        fields = '__all__'


class CropListSerialier(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = CropName
        fields = ['project', 'name', 'rate', 'district', 'created', 'updated']

    def create(self, validated_data):
        """
        Create and return a new `CropList` instance, given the validated data.
        """
        return CropName.objects.create(**validated_data)


class CropSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    pap = UserPap(queryset=ProjectAffectedPerson.objects.all(), slug_field='first_name')
    crop_name = serializers.SlugRelatedField(queryset=CropName.objects.all(), slug_field='name')

    class Meta:
        model = Crop
        fields = ['project', 'crop_name', 'crop_image', 'description', 'quantity', 'quality', 'rate',
                  'pap', 'value_of_crops', 'created', 'updated']

    def create(self, validated_data):
        """
        Create and return a new `Crop` instance, given the validated data.
        """
        return Crop.objects.create(**validated_data)


class LandListSerialier(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = LandName
        fields = ['project', 'name', 'created', 'updated']

    def create(self, validated_data):
        """
        Create and return a new `LandList` instance, given the validated data.
        """
        return LandName.objects.create(**validated_data)


class TenureTypeSerialier(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = TenureType
        fields = ['project', 'name', 'created', 'updated']

    def create(self, validated_data):
        """
        Create and return a new `Tenure Type` instance, given the validated data.
        """
        return TenureType.objects.create(**validated_data)


class LandSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    pap = UserPap(queryset=ProjectAffectedPerson.objects.all(), slug_field='first_name')
    land_type = serializers.SlugRelatedField(queryset=LandName.objects.all(), slug_field='name')
    tenure = serializers.SlugRelatedField(queryset=TenureType.objects.all(), slug_field='name')

    class Meta:
        model = Land
        fields = ['project', 'land_type', 'land_image', 'survey_no', 'pap', 'tenure', 'size', 'location',
                  'land_use', 'land_services', 'rate', 'value_of_land', 'created', 'updated']

    def create(self, validated_data):
        """
        Create and return a new `Land` instance, given the validated data.
        """
        return Land.objects.create(**validated_data)


class TreeListSerialier(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = TreeName
        fields = ['project', 'name', 'rate', 'district', 'created', 'updated']

    def create(self, validated_data):
        """
        Create and return a new `TreeList` instance, given the validated data.
        """
        return TreeName.objects.create(**validated_data)


class TreeSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    pap = UserPap(queryset=ProjectAffectedPerson.objects.all(), slug_field='first_name')
    name = serializers.SlugRelatedField(queryset=TreeName.objects.all(), slug_field='name')

    class Meta:
        model = Tree
        fields = ['project', 'pap', 'name', 'description', 'tree_image', 'quantity', 'rate', 'value_of_trees',
                  'created', 'updated']

    def create(self, validated_data):
        """
        Create and return a new `Tree` instance, given the validated data.
        """
        return Tree.objects.create(**validated_data)


class ProjectAffectedPersonSerializer(serializers.ModelSerializer):
    pap_crops = CropSerializer(many=True, read_only=True)
    pap_lands = LandSerializer(many=True, read_only=True)
    pap_construction = ConstructionBuildingSerializer(many=True, read_only=True)
    pap_trees = TreeSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectAffectedPerson
        fields = ['id', 'first_name', 'last_name', 'pap_image', 'age', 'address',
                  'nin', 'email', 'phone_number', 'pap_crops', 'pap_lands', 'pap_trees',
                  'pap_construction', 'created', 'updated']

    def create(self, validated_data):
        """
        Create and return a new `ProjectAffectedPerson` instance, given the validated data.
        """
        return ProjectAffectedPerson.objects.create(**validated_data)


# CSV FILES UPLOADS
# CSV File Uploads
class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SaveFileSerializer(serializers.Serializer):

    class Meta:
        model = ProjectAffectedPerson
        fields = ['id', 'first_name', 'last_name', 'pap_image', 'age', 'address',
                  'nin', 'email', 'phone_number']


# CROPS CSV Uploads
class CropUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SaveCropFileSerializer(serializers.Serializer):

    class Meta:
        model = CropName
        fields = ['name', 'rate', 'district']


# LAND LIST NAMES CSV Uploads
class LandListUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SaveLandListFileSerializer(serializers.Serializer):

    class Meta:
        model = LandName
        fields = ['name']

    def create(self, validated_data):
        """
        Create and return a new `LandList` instance, given the validated data.
        """
        return LandName.objects.create(**validated_data)


# LAND TUNURE NAMES CSV Uploads
class TenureTypeUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SaveTenureTypeFileSerializer(serializers.Serializer):

    class Meta:
        model = TenureType
        fields = ['name']

    def create(self, validated_data):
        """
        Create and return a new `TenureType` instance, given the validated data.
        """
        return TenureType.objects.create(**validated_data)


# Construction Names CSV Uploads
class ConstructionNameListUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SaveConstructionNameListFileSerializer(serializers.Serializer):

    class Meta:
        model = ConstructionName
        fields = ['name']


# TREES CSV Uploads
class TreeUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SaveTreeFileSerializer(serializers.Serializer):

    class Meta:
        model = TreeName
        fields = ['name', 'rate', 'district']

