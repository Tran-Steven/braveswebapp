from django.db import models


class MyTable(models.Model):
    BATTER_ID = models.FloatField()
    BATTER = models.CharField(max_length=100)
    PITCHER_ID = models.FloatField()
    PITCHER = models.CharField(max_length=100)
    GAME_DATE = models.DateField()
    LAUNCH_ANGLE = models.FloatField(null=True, blank=True)
    EXIT_SPEED = models.FloatField(null=True, blank=True)
    EXIT_DIRECTION = models.FloatField(null=True, blank=True)
    HIT_DISTANCE = models.FloatField(null=True, blank=True)
    HANG_TIME = models.FloatField(null=True, blank=True)
    HIT_SPIN_RATE = models.FloatField(null=True, blank=True)
    PLAY_OUTCOME = models.CharField(max_length=50)
    VIDEO_LINK = models.URLField(primary_key=True)

    class Meta:
        db_table = "mytable"
        managed = False

    def __str__(self):
        return f"{self.BATTER} vs {self.PITCHER} on {self.GAME_DATE}"
