from django.shortcuts import render
from api.models import *
from api.serializers import *
from .filters import ConstructionBuildingFilter  #New
import django_filters
from rest_framework.renderers import *
from rest_framework.parsers import *
from rest_framework import viewsets
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, renderers, filters
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
import django_filters.rest_framework
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import *
from rest_framework import status
from django.contrib.auth import logout, login

#authentication views
from dj_rest_auth.views import (
    LoginView as DjLoginView,
    PasswordChangeView as DjPasswordChangeView,
    PasswordResetConfirmView as DjPasswordResetConfirmView,
    PasswordResetView as DjPasswordResetView,
    UserDetailsView as DjUserDetailsView,
)

import io, csv, pandas as pd

@api_view(['GET'])
def api_root(request, format = None):
   return Response({
      'paps': reverse('pap-list', request = request, format = format),
      'land_names': reverse('land-list-name', request = request, format = format),
      'land_tenure_types': reverse('tenure-types', request = request, format = format),
      'crop_names': reverse('crop-list-names', request = request, format = format),
      'construction_names': reverse('construction-list-name', request = request, format = format),
      'tree_names': reverse('tree-list-name', request = request, format = format),
      'land': reverse('land-list', request = request, format = format),
      'construction': reverse('construction-list', request = request, format = format),
      'trees': reverse('tree-list', request = request, format = format),
      'crops': reverse('crop-list', request = request, format = format),
      'upload_pap_csv_file': reverse('upload-pap-file-csv', request = request, format = format),
      'upload_crops_csv_file': reverse('upload-crop-file-csv', request = request, format = format),
      'upload_construction_csv_file': reverse('upload-construction-file-csv', request = request, format = format),
      'upload_tenure_csv_file': reverse('upload-tenure-file-csv', request = request, format = format)
   })


#project view
class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = PSerializer

class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = PSerializer


#Authentication
class CustomLoginView(DjLoginView):
    """
    Custom LoginView.

    Inherits from DjLoginView provided by dj_rest_auth.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.

        Calls parent's post method to process the request.
        """
        response = super().post(request, *args, **kwargs)
        return response


class CustomPasswordChangeView(DjPasswordChangeView):
    """
    Custom PasswordChangeView.

    Inherits from DjPasswordChangeView provided by dj_rest_auth.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.

        Calls parent's post method to process the request.
        """
        response = super().post(request, *args, **kwargs)
        return response


class CustomPasswordResetConfirmView(DjPasswordResetConfirmView):
    """
    Custom PasswordResetConfirmView.

    Inherits from DjPasswordResetConfirmView provided by dj_rest_auth.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.

        Calls parent's post method to process the request.
        """
        response = super().post(request, *args, **kwargs)
        return response


class CustomPasswordResetView(DjPasswordResetView):
    """
    Custom PasswordResetView.

    Inherits from DjPasswordResetView provided by dj_rest_auth.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.

        Calls parent's post method to process the request.
        """
        response = super().post(request, *args, **kwargs)
        return response


class CustomUserDetailsView(DjUserDetailsView):
    """
    Custom UserDetailsView.

    Inherits from DjUserDetailsView provided by dj_rest_auth.
    """
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.

        Calls parent's get method to process the request.
        """
        response = super().get(request, *args, **kwargs)
        return response



#logout view
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)

    def get(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)


# A custom function to check if the user is an admin
def is_admin(user):
    return user.is_staff

#projected affected person
class ProjectAffectedPersonList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProjectAffectedPerson.objects.all().order_by('-created')
    serializer_class = ProjectAffectedPersonSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'id_no']


    def get_queryset(self):
        queryset = super().get_queryset()

        """
        This view should return a list of all the project_affected_persons
        for the currently authenticated user.
        """
         # Check if the user is an admin
        if is_admin(self.request.user):
            # Return all project affected people if the user is an admin
            queryset = ProjectAffectedPerson.objects.all().order_by('-created')
        else:
            # Filter project affected people by the request.user if not an admin
            queryset = ConstructionBuilding.objects.filter(owner=self.request.user)

        return queryset
    
    
    def perform_create(self, serializer):
        owner = self.request.user
        #serializer holds a django model
        serializer.save(owner=owner)

#project affected person details with id
class ProjectAffectedPersonDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProjectAffectedPerson.objects.all().order_by('-created')
    serializer_class = ProjectAffectedPersonSerializer


    def get_queryset(self):
        """
        This view should return a list of all the project_affected_person_details
        for the currently authenticated user.
        """
        owner = self.request.user
        return ProjectAffectedPerson.objects.filter(owner=owner).order_by('-created')

#project affected person details with name
class ProjectAffectedPersonNameView(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProjectAffectedPerson.objects.all().order_by('-created')
    serializer_class = ProjectAffectedPersonSerializer

    try:
        def list(self, request, first_name):
            pap = ProjectAffectedPerson.objects.get(first_name=first_name)
            serializer = ProjectAffectedPersonSerializer(pap)
            return Response(serializer.data)
    except ProjectAffectedPerson.DoesNotExist:
            raise Http404

    def get_queryset(self):
        """
        This view should return a list of all the project_affected_person_details
        for the currently authenticated user.
        """
        owner = self.request.user
        return ProjectAffectedPerson.objects.filter(owner=owner).order_by('-created')

#Construction list names
class ConstructionListName(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ConstructionName.objects.all().order_by('-created')
    serializer_class = ConstructionListSerialier
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def perform_create(self, serializer):
        owner = self.request.user
        #serializer holds a django model
        serializer.save(owner=owner)
        
#construction details
class ConstructionListDetailName(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ConstructionName.objects.all().order_by('-created')
    serializer_class = ConstructionListSerialier
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']

    
#list of constructions
class ConstructionBuildingList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ConstructionBuilding.objects.all().order_by('name')
    serializer_class = ConstructionBuildingSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']


    def get_queryset(self):
        queryset = super().get_queryset()

        """
        This view should return a list of all the project_affected_persons
        for the currently authenticated user.
        """
         # Check if the user is an admin
        if is_admin(self.request.user):
            # Return all constructions if the user is an admin
            queryset = ConstructionBuilding.objects.all().order_by('-rate')
        else:
            # Filter constructions by the request.user if not an admin
            queryset = ConstructionBuilding.objects.filter(owner=self.request.user)

        return queryset
    
        
    
    def perform_create(self, serializer):
        owner = self.request.user
        #serializer holds a django model
        serializer.save(owner=owner)



#construction details for construction object with id
class ConstructionBuildingDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ConstructionBuilding.objects.all().order_by('-rate')
    serializer_class = ConstructionBuildingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()

        """
        This view should return a list of all the project_affected_persons
        for the currently authenticated user.
        """
         # Check if the user is an admin
        if is_admin(self.request.user):
            # Return all constructions if the user is an admin
            queryset = ConstructionBuilding.objects.all().order_by('-rate')
        else:
            # Filter constructions by the request.user if not an admin
            queryset = ConstructionBuilding.objects.filter(owner=self.request.user)

        return queryset
    

#construction details details with name
class ConstructionDetailNameView(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ConstructionBuilding.objects.all().order_by('-rate')
    serializer_class = ConstructionBuildingSerializer

    try:
        def list(self, request, name):
            construction = ConstructionBuilding.objects.filter(name=name)
            serializer = ConstructionBuildingSerializer(construction, many=True)
            return Response(serializer.data)
    except ConstructionBuilding.DoesNotExist:
            raise Http404

    #count number of construction names
    try:
        def count_construction(self, request,name):
            construction_count = ConstructionBuilding.objects.filter(name=name).order_by('-created').aggregate(Count('name'))
            return Response(construction_count)
    except ConstructionBuilding.DoesNotExist:
            raise Http404
            
    
    def get_queryset(self):
        """
        This view should return a list of all the construction details
        for the currently authenticated user.
        """
        owner = self.request.user
        return ConstructionBuilding.objects.filter(owner=owner).order_by('-created')

#tree list names
class TreeListName(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TreeName.objects.all().order_by('-created')
    serializer_class = TreeListSerialier
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
            queryset = super().get_queryset()

            # Check if the user is an admin
            if is_admin(self.request.user):
                # Return all names of trees if the user is an admin
                queryset = TreeName.objects.all().order_by('-rate')
            else:
                # Filter all names of trees by the request.user if not an admin
                queryset = TreeName.objects.filter(owner=self.request.user)

            return queryset

    def perform_create(self, serializer):
        owner = self.request.user
        #serializer holds a django model
        serializer.save(owner=owner)
        
#tree details name
class TreeListDetailName(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TreeName.objects.all().order_by('-created')
    serializer_class = TreeListSerialier
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

#list of trees
class TreeList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Tree.objects.all().order_by('-rate')
    serializer_class = TreeSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
            queryset = super().get_queryset()

            # Check if the user is an admin
            if is_admin(self.request.user):
                # Return all trees if the user is an admin
                queryset = Tree.objects.all().order_by('-rate')
            else:
                # Filter all trees by the request.user if not an admin
                queryset = Tree.objects.filter(owner=self.request.user)

            return queryset
    
    def perform_create(self, serializer):
        owner = self.request.user
        #serializer holds a django model
        serializer.save(owner=owner)

#tree details  
class TreeDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Tree.objects.all().order_by('-rate')
    serializer_class = TreeSerializer

    def get_queryset(self):
            queryset = super().get_queryset()

            # Check if the user is an admin
            if is_admin(self.request.user):
                # Return all trees if the user is an admin
                queryset = Tree.objects.all().order_by('-rate')
            else:
                # Filter all trees by the request.user if not an admin
                queryset = Tree.objects.filter(owner=self.request.user)

            return queryset
    

#Tree details details with name
class TreeDetailNameView(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Tree.objects.all().order_by('-rate')
    serializer_class = TreeSerializer
    #tree details details with name
    try:
        def list(self, request, name):
            tree = Tree.objects.filter(name=name).order_by('-created')
            serializer = TreeSerializer(tree, many=True)
            return Response(serializer.data)
    except Tree.DoesNotExist:
            raise Http404

    #count number of tree names
    try:
        def count_tree(self, request,name):
            trees_count = Tree.objects.filter(name=name).order_by('-created').aggregate(Count('name'))
            return Response(trees_count)
    except Tree.DoesNotExist:
            raise Http404
            

    def get_queryset(self):
        """
        This view should return tree details
        for the currently authenticated user.
        """
        owner = self.request.user
        return Tree.objects.filter(owner=owner).order_by('-created')

#Crop list names and rate
class CropListName(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CropName.objects.all().order_by('-created')
    serializer_class = CropListSerialier
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'district']
    

    def perform_create(self, serializer):
        owner = self.request.user
        #serializer holds a django model
        serializer.save(owner=owner)
        

#crop details
class CropListDetailName(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CropName.objects.all().order_by('-created')
    serializer_class = CropListSerialier
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'district']

    

# Create your views here.
# Crop list
class CropList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Crop.objects.all().order_by('-created')
    serializer_class = CropSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def get_queryset(self):
            queryset = super().get_queryset()

            # Check if the user is an admin
            if is_admin(self.request.user):
                # Return all crops if the user is an admin
                queryset = Crop.objects.all().order_by('-created')
            else:
                # Filter all crops by the request.user if not an admin
                queryset = Crop.objects.filter(owner=self.request.user)

            return queryset
    

    def perform_create(self, serializer):
        owner = self.request.user
        #serializer holds a django model
        serializer.save(owner=owner)

#crop details
class CropDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Crop.objects.all().order_by('-created')
    serializer_class = CropSerializer

    def get_queryset(self):
            queryset = super().get_queryset()

            # Check if the user is an admin
            if is_admin(self.request.user):
                # Return all crops if the user is an admin
                queryset = Crop.objects.all().order_by('-created')
            else:
                # Filter all crops by the request.user if not an admin
                queryset = Crop.objects.filter(owner=self.request.user)

            return queryset

#crop details details with name
class CropDetailNameView(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

    try:
        def list(self,request, name):
            crop = Crop.objects.filter(name=name)
            serializer = CropSerializer(crop, many=True)
            return Response(serializer.data)
    except Crop.DoesNotExist:
            raise Http404

    #count number of crop names
    try:
        def count_crops(self, request,name):
            crops_count = Crop.objects.filter(name=name).order_by('-created').aggregate(Count('name'))
            return Response(crops_count)
    except Crop.DoesNotExist:
            raise Http404
            

    def get_queryset(self):
                queryset = super().get_queryset()

                # Check if the user is an admin
                if is_admin(self.request.user):
                    # Return all crops if the user is an admin
                    queryset = Crop.objects.all().order_by('-created')
                else:
                    # Filter all crops by the request.user if not an admin
                    queryset = Crop.objects.filter(owner=self.request.user)

                return queryset
        
#pap_crops
# ViewSets define the view behavior.
class PapCrop(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    """
    View to list all crops belonging to a pap in the system.
    """
    try:
        def list(self, request, first_name):
            pap = ProjectAffectedPerson.objects.get(first_name=first_name)
            pap_crops = Crop.objects.filter(pap=pap).order_by('-created')
            serializer = CropSerializer(pap_crops, many=True)
            return Response(serializer.data)
    except Crop.DoesNotExist:
            raise Http404
    
    def get_queryset(self):
        """
        This view should return a list of all the paps
        for the currently authenticated user.
        """
        owner = self.request.user
        return ProjectAffectedPerson.objects.filter(owner=owner).order_by('-created')
    
#land list names
class LandListName(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = LandName.objects.all().order_by('-created')
    serializer_class = LandListSerialier
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def perform_create(self, serializer):
        owner = self.request.user
        #serializer holds a django model
        serializer.save(owner=owner)
        
#land details name
class LandListDetailName(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = LandName.objects.all().order_by('-created')
    serializer_class = LandListSerialier
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

#tenure types
class TenureList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TenureType.objects.all().order_by('-created')
    serializer_class = TenureTypeSerialier
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def perform_create(self, serializer):
        owner = self.request.user
        #serializer holds a django model
        serializer.save(owner=owner)
        
#tenure type details
class TenureDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TenureType.objects.all().order_by('-created')
    serializer_class = TenureTypeSerialier
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


#list of land
class LandList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Land.objects.all().order_by('-rate')
    serializer_class = LandSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['land_type']

    def get_queryset(self):
            user = self.request.user
            queryset = super().get_queryset()

            # Check if the user is an admin
            if is_admin(self.request.user):
                # Return all land if the user is an admin
                queryset = Land.objects.all().order_by('-rate')
            else:
                # Filter all land by the request.user if not an admin
                queryset = Land.objects.filter(user=user)

            return queryset
    
    def perform_create(self, serializer):
        user = self.request.user
        #serializer holds a django model
        serializer.save(user=user)

    def get_queryset(self):
        """
        This view should return a list of all the project_affected_person land
        for the currently authenticated user.
        """
        user = self.request.user
        return Land.objects.filter(user=user).order_by('-rate')
    
#land details with id
class LandDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Land.objects.all().order_by('-rate')
    serializer_class = LandSerializer

#land details details with name
class LandDetailNameView(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Land.objects.all().order_by('-rate')
    serializer_class = ConstructionBuildingSerializer

    try:
        def list(self, request, land_type):
            land = Land.objects.filter(land_type=land_type)
            serializer = LandSerializer(land, many=True)
            return Response(serializer.data)
    except Land.DoesNotExist:
            raise Http404
    
    #count number of land names
    try:
        def count_land(self, request,name):
            land_count = Land.objects.filter(name=name).order_by('-created').aggregate(Count('name'))
            return Response(land_count)
    except Land.DoesNotExist:
            raise Http404

    def get_queryset(self):
        """
        This view should return land details
        for the currently authenticated user.
        """
        owner = self.request.user
        return Land.objects.filter(owner=owner).order_by('-created')

#pap_land
# ViewSets define the view behavior.
class PapLandView(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['land_type']
    """
    View to list all land belonging to a particular pap.
    """
    try:
        def list(self, request,first_name,format=None):
            pap = ProjectAffectedPerson.objects.get(first_name=first_name)
            pap_land = Land.objects.filter(pap=pap).order_by('-rate')
            serializer = LandSerializer(pap_land, many=True)
            return Response(serializer.data)
    except Land.DoesNotExist:
            raise Http404
    
    def get_queryset(self):
        """
        This view should return a list of all the paps
        for the currently authenticated user.
        """
        user = self.request.user
        return Land.objects.filter(user=user).order_by('-rate')

#pap_trees
# ViewSets define the view behavior.
class PapTreeView(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    """
    View to list all trees belonging to a particular pap.
    """
    try:
        def list(self, request, first_name):
            pap = ProjectAffectedPerson.objects.get(first_name=first_name)
            pap_trees = Tree.objects.filter(pap=pap).order_by('-created')
            serializer = TreeSerializer(pap_trees, many=True)
            return Response(serializer.data)
    except Tree.DoesNotExist:
            raise Http404
    
    def get_queryset(self):
        """
        This view should return a list of all the paps
        for the currently authenticated user.
        """
        owner = self.request.user
        return Tree.objects.filter(owner=owner).order_by('-created')

#pap_construction
# ViewSets define the view behavior.
class PapConstructionView(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['-created']
    """
    View to list all construction belonging to a particular pap.
    """
    try:
        def list(self, request,first_name,format=None):
            pap = ProjectAffectedPerson.objects.get(first_name=first_name)
            pap_construction = ConstructionBuilding.objects.filter(pap=pap).order_by('-rate')
            serializer = ConstructionBuildingSerializer(pap_construction, many=True)
            return Response(serializer.data)
    except ConstructionBuilding.DoesNotExist:
            raise Http404
    
    def get_queryset(self):
        """
        This view should return a list of all the paps
        for the currently authenticated user.
        """
        owner = self.request.user
        return ConstructionBuilding.objects.filter(owner=owner).order_by('-rate')
    

#CSV FILE UPLOADS
class UploadFileView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FileUploadSerializer
    
    def create(self, request, *args, **kwargs):
        owner = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file)
        for _, row in reader.iterrows():
            new_file = ProjectAffectedPerson(
                       id = row['id'],
                       first_name= row["first_name"],
                       last_name= row['last_name'],
                       age= row["age"],
                       address= row["address"],
                       id_no= row["id_no"],
                       email= row["email"],
                       phone_number= row["phone_number"],
                       owner = owner
                       )
            new_file.save()
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)

#Crop CSV FILE UPLOADS
class UploadCropFileView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CropUploadSerializer
    
    def create(self, request, *args, **kwargs):
        owner = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file)
        for _, row in reader.iterrows():
            new_file = CropName(
                       owner = owner,
                       name= row["name"],
                       rate= row['rate'],
                       district= row["district"]
                       )
            new_file.save()
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)

#Construction CSV FILE UPLOADS
class UploadConstructionFileView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ConstructionNameListUploadSerializer
    
    def create(self, request, *args, **kwargs):
        owner = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file)
        for _, row in reader.iterrows():
            new_file = ConstructionName(
                       owner = owner,
                       name= row["name"]
                       )
            new_file.save()
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


#Tenure CSV FILE UPLOADS
class UploadTenureFileView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TenureTypeUploadSerializer

    def create(self, request, *args, **kwargs):
        owner = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file)
        for _, row in reader.iterrows():
            new_file = TenureType(
                       owner = owner,
                       name= row["name"],
                       )
            new_file.save()
        return Response({"status": "success"},status.HTTP_201_CREATED)




#construction search view
class GenericSearchListView(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ConstructionBuilding.objects.all().order_by('name')
    serializer_class = ConstructionBuildingSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ConstructionBuildingFilter
    search_fields = ['name']


    def get_queryset(self):
        queryset = super().get_queryset()

        # filter based on the authenticated user's data:
        constructions = ConstructionBuilding.objects.all().order_by('name')
        queryset = constructions.filter(owner=self.request.user)

        return queryset
    

