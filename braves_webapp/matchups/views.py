from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django_pandas.io import read_frame
from django.db.models import Avg, Count, Q, Sum, Case, When, IntegerField, F
from .models import MyTable
from .serializers import (
    MyTableSerializer,
    BatterSerializer,
    PitcherSerializer,
)
import numpy as np
import pandas as pd
import logging
import datetime

logger = logging.getLogger(__name__)


class StatisticalAnalysisView(APIView):
    def get(self, request):

        queryset = MyTable.objects.all()
        df = read_frame(
            queryset,
            fieldnames=[
                "LAUNCH_ANGLE",
                "HANG_TIME",
                "HIT_DISTANCE",
                "EXIT_SPEED",
                "EXIT_DIRECTION",
                "HIT_SPIN_RATE",
            ],
        )

        df.replace("NULL", np.nan, inplace=True)

        numeric_columns = [
            "LAUNCH_ANGLE",
            "HANG_TIME",
            "HIT_DISTANCE",
            "EXIT_SPEED",
            "EXIT_DIRECTION",
            "HIT_SPIN_RATE",
        ]
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")
        df.dropna(inplace=True)
        correlations = df.corr().to_dict()
        response_data = {
            "correlations": correlations,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class PredictionView(APIView):
    def get(self, request):
        batter_id = request.GET.get("batter_id")
        pitcher_id = request.GET.get("pitcher_id")

        if batter_id and pitcher_id:
            try:
                batter_id = float(batter_id)
                pitcher_id = float(pitcher_id)
            except ValueError:
                return Response(
                    {"error": "Invalid batter_id or pitcher_id"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            hit_terms = ["Hit", "Single", "Double", "Triple", "Home Run"]
            strikeout_terms = [
                "Strikeout",
                "K",
                "Strikeout Swinging",
                "Strikeout Looking",
            ]

            matchup_data = MyTable.objects.filter(
                BATTER_ID=batter_id, PITCHER_ID=pitcher_id
            )

            if matchup_data.exists():
                total_at_bats = matchup_data.count()
                hits = matchup_data.filter(PLAY_OUTCOME__in=hit_terms).count()
                strikeouts = matchup_data.filter(
                    PLAY_OUTCOME__in=strikeout_terms
                ).count()

                outcome_counts = matchup_data.values("PLAY_OUTCOME").annotate(
                    count=Count("PLAY_OUTCOME")
                )

                total_bases = (
                    matchup_data.aggregate(
                        total_bases=Sum(
                            Case(
                                When(PLAY_OUTCOME="Single", then=1),
                                When(PLAY_OUTCOME="Double", then=2),
                                When(PLAY_OUTCOME="Triple", then=3),
                                When(PLAY_OUTCOME="Home Run", then=4),
                                default=0,
                                output_field=IntegerField(),
                            )
                        )
                    )["total_bases"]
                    or 0
                )

                slugging_percentage = (
                    total_bases / total_at_bats if total_at_bats > 0 else 0
                )

                performance_data = (
                    matchup_data.annotate(date=F("GAME_DATE"))
                    .values("date")
                    .annotate(
                        hits=Sum(
                            Case(
                                When(PLAY_OUTCOME__in=hit_terms, then=1),
                                default=0,
                                output_field=IntegerField(),
                            )
                        ),
                        at_bats=Count("VIDEO_LINK"),
                    )
                    .order_by("date")
                )

                performance_over_time = []
                for entry in performance_data:
                    date = entry["date"]
                    hits_entry = entry["hits"]
                    at_bats_entry = entry["at_bats"]
                    batting_average = (
                        hits_entry / at_bats_entry if at_bats_entry > 0 else 0
                    )
                    performance_over_time.append(
                        {
                            "date": (
                                date.strftime("%Y-%m-%d")
                                if isinstance(date, datetime.date)
                                else date
                            ),
                            "batting_average": round(batting_average, 3),
                        }
                    )

                video_links = list(matchup_data.values_list("VIDEO_LINK", flat=True))

            else:

                batter_data = MyTable.objects.filter(BATTER_ID=batter_id)
                total_at_bats = batter_data.count()
                hits = batter_data.filter(PLAY_OUTCOME__in=hit_terms).count()
                strikeouts = batter_data.filter(
                    PLAY_OUTCOME__in=strikeout_terms
                ).count()

                outcome_counts = batter_data.values("PLAY_OUTCOME").annotate(
                    count=Count("PLAY_OUTCOME")
                )

                total_bases = (
                    batter_data.aggregate(
                        total_bases=Sum(
                            Case(
                                When(PLAY_OUTCOME="Single", then=1),
                                When(PLAY_OUTCOME="Double", then=2),
                                When(PLAY_OUTCOME="Triple", then=3),
                                When(PLAY_OUTCOME="Home Run", then=4),
                                default=0,
                                output_field=IntegerField(),
                            )
                        )
                    )["total_bases"]
                    or 0
                )

                slugging_percentage = (
                    total_bases / total_at_bats if total_at_bats > 0 else 0
                )

                performance_data = (
                    batter_data.annotate(date=F("GAME_DATE"))
                    .values("date")
                    .annotate(
                        hits=Sum(
                            Case(
                                When(PLAY_OUTCOME__in=hit_terms, then=1),
                                default=0,
                                output_field=IntegerField(),
                            )
                        ),
                        at_bats=Count("VIDEO_LINK"),
                    )
                    .order_by("date")
                )

                performance_over_time = []
                for entry in performance_data:
                    date = entry["date"]
                    hits_entry = entry["hits"]
                    at_bats_entry = entry["at_bats"]
                    batting_average = (
                        hits_entry / at_bats_entry if at_bats_entry > 0 else 0
                    )
                    performance_over_time.append(
                        {
                            "date": (
                                date.strftime("%Y-%m-%d")
                                if isinstance(date, datetime.date)
                                else date
                            ),
                            "batting_average": round(batting_average, 3),
                        }
                    )

                video_links = list(batter_data.values_list("VIDEO_LINK", flat=True))

            batting_average = hits / total_at_bats if total_at_bats > 0 else 0

            data = {
                "batting_average": round(batting_average, 3),
                "slugging_percentage": round(slugging_percentage, 3),
                "total_at_bats": total_at_bats,
                "hits": hits,
                "strikeouts": strikeouts,
                "outcome_counts": list(outcome_counts),
                "performance_over_time": performance_over_time,
                "video_links": video_links,
            }

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "batter_id and pitcher_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BatterListView(generics.ListAPIView):
    queryset = MyTable.objects.values("BATTER_ID", "BATTER").distinct()
    serializer_class = BatterSerializer


class PitcherListView(generics.ListAPIView):
    queryset = MyTable.objects.values("PITCHER_ID", "PITCHER").distinct()
    serializer_class = PitcherSerializer
