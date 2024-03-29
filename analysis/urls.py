from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from analysis import views

# Define urlpatterns for API endpoints
urlpatterns = [
    # Root endpoint
    path('', views.Analysis_root),

    # Crop-related endpoints
    path('crops/number_of_crops/', views.CropAnalysisView.as_view(), name='number-of-crops'),
    path('crops/sum/<int:id>/', views.TotalCropValueView.as_view(), name='total-crop-value'),

    # Construction-related endpoints
    path('construction/sum/<int:id>/', views.TotalConstructionValueView.as_view(), name='total-construction-value'),

    # Tree-related endpoints
    path('trees/sum/<int:id>/', views.TotalTreeValueView.as_view(), name='total-tree-value'),

    # Land-related endpoints
    path('land/sum/<int:id>/', views.TotalLandValueView.as_view(), name='total-land-value'),

    # Award-related endpoint
    path('award/<int:id>/', views.AwardView.as_view(), name='total-award'),

    # Crop rate endpoints
    path('crops/rate/total/', views.CropRateSumView.as_view(), name='total-crops-rate'),
    path('crops/rate/minimum/', views.MinimumCropRateView.as_view(), name='minimum-crop-rate'),
    path('crops/rate/maximum/', views.MaximumCropRateView.as_view(), name='maximum-crop-rate'),
    path('crops/rate/average/', views.AverageCropRateView.as_view(), name='average-crop-rate'),
    path('crops/rate/difference/', views.CropRateDifferenceView.as_view(), name='crop-rate-difference'),

    # Crop rating endpoints
    path('crops/rating/maximum/', views.CropRatingHighView.as_view(), name='crop-rating-maximum'),
    path('crops/rating/', views.CropRatingLowView.as_view(), name='crop-rating-minimum'),
    path('crops/rating/average/', views.CropRatingAverageView.as_view(), name='crop-rating-average'),
    path('crops/rating/difference/', views.CropRatingDifferenceView.as_view(), name='crop-rating-difference'),

    # Land rate endpoints
    path('land/number_of_land/', views.LandAnalysisView.as_view(), name='number-of-land'),
    path('land/rate/total/', views.LandRateSumView.as_view(), name='total-land-rate'),
    path('land/rate/minimum/', views.MinimumLandRateView.as_view(), name='minimum-land-rate'),
    path('land/rate/maximum/', views.MaximumLandRateView.as_view(), name='maximum-land-rate'),
    path('land/rate/average/', views.AverageLandRateView.as_view(), name='average-land-rate'),
    path('land/rate/difference/', views.LandRateDifferenceView.as_view(), name='land-rate-difference'),

    # Construction endpoints
    path('construction/number_of_construction/', views.ConstructionAnalysisView.as_view(), name='number-of-construction'),
    path('construction/rate/total/', views.ConstructionRateSumView.as_view(), name='total-construction-rate'),
    path('construction/rate/minimum/', views.MinimumConstructionRateView.as_view(), name='minimum-construction-rate'),
    path('construction/rate/maximum/', views.MaximumConstructionRateView.as_view(), name='maximum-construction-rate'),
    path('construction/rate/average/', views.AverageConstructionRateView.as_view(), name='average-construction-rate'),
    path('construction/rate/difference/', views.ConstructionRateDifferenceView.as_view(), name='construction-rate-difference'),

    # Tree endpoints
    path('trees/number_of_trees/', views.TreeAnalysisView.as_view(), name='number-of-trees'),
    path('trees/rate/total/', views.TreeRateSumView.as_view(), name='total-tree-rate'),
    path('trees/rate/minimum/', views.MinimumTreeRateView.as_view(), name='minimum-tree-rate'),
    path('trees/rate/maximum/', views.MaximumTreeRateView.as_view(), name='maximum-tree-rate'),
    path('trees/rate/average/', views.AverageTreeRateView.as_view(), name='average-tree-rate'),
    path('trees/rate/difference/', views.TreeRateDifferenceView.as_view(), name='tree-rate-difference')
]

# Apply format suffix patterns to urlpatterns
urlpatterns = format_suffix_patterns(urlpatterns)
