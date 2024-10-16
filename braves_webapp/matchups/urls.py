from django.urls import path
from .views import (
    StatisticalAnalysisView,
    PredictionView,
    BatterListView,
    PitcherListView,
)

urlpatterns = [
    path("analysis/", StatisticalAnalysisView.as_view(), name="statistical_analysis"),
    path("predict/", PredictionView.as_view(), name="prediction"),
    path("batters/", BatterListView.as_view(), name="batter_list"),
    path("pitchers/", PitcherListView.as_view(), name="pitcher_list"),
]
