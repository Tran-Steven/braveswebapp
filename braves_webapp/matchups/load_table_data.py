from django.core.management.base import BaseCommand
from django.db import connection
from .views import BatterViewSet, PitcherViewSet, MyTableViewSet


class Command(BaseCommand):
    help = "Load data from mytable into Django models"

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM "mytable"')
        rows = cursor.fetchall()

        batter_cache = {}
        pitcher_cache = {}

        for row in rows:
            batter_id = int(row[0])
            batter_name = row[1]
            pitcher_id = int(row[2])
            pitcher_name = row[3]
            launch_angle = row[5]
            exit_speed = row[6]
            hit_distance = row[8]
            hang_time = float(row[9]) if row[9] != "0" else None
            hit_spin_rate = float(row[10]) if row[10] != "0" else None

            if batter_id not in batter_cache:
                batter, _ = Batter.objects.get_or_create(
                    batter_id=batter_id, defaults={"name": batter_name}
                )
                batter_cache[batter_id] = batter
            else:
                batter = batter_cache[batter_id]

            if pitcher_id not in pitcher_cache:
                pitcher, _ = Pitcher.objects.get_or_create(
                    pitcher_id=pitcher_id, defaults={"name": pitcher_name}
                )
                pitcher_cache[pitcher_id] = pitcher
            else:
                pitcher = pitcher_cache[pitcher_id]

            Matchup.objects.create(
                batter=batter,
                pitcher=pitcher,
                launch_angle=launch_angle,
                exit_speed=exit_speed,
                hit_distance=hit_distance,
                hang_time=hang_time,
                hit_spin_rate=hit_spin_rate,
            )

        self.stdout.write(self.style.SUCCESS("Data loaded successfully."))
