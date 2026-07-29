from django.db import models


class SBSMessage(models.Model):

    # 0
    message_type = models.CharField(max_length=3, default="")  # SEL, ID, AIR, STA, CLK, MSG

    # 1
    transmission_type = models.IntegerField(default=0)  # 1..8

    # 2
    session_id = models.IntegerField(blank=True, null=True)

    # 3
    aircraft_id = models.IntegerField(blank=True, null=True)

    # 4
    hex_ident = models.CharField(max_length=6, default="")  # ICAO airframe id

    # 5
    flight_id = models.CharField(max_length=8, blank=True, default="")

    # 6
    date_message_generated = models.DateField(auto_now=True)

    # 7
    time_message_generated = models.TimeField(auto_now=True)

    # 8
    date_message_logged = models.DateField(auto_now=True)

    # 9
    time_message_logged = models.TimeField(auto_now=True)

    # 10
    callsign = models.CharField(max_length=8, blank=True, default="")

    # 11
    altitude = models.IntegerField(blank=True, null=True)

    # 12
    ground_speed = models.IntegerField(blank=True, null=True)

    # 13
    track = models.CharField(max_length=3, blank=True, default="")

    # 14
    latitude = models.CharField(max_length=9, blank=True, default="")

    # 15
    longitude = models.CharField(max_length=9, blank=True, default="")

    # 16
    vertical_rate = models.IntegerField(blank=True, null=True)

    # 17
    squawk = models.CharField(max_length=4, blank=True, default="")

    # 18
    alert_squawk_change = models.CharField(max_length=4, blank=True, default="")

    # 19
    emergency = models.CharField(max_length=1, blank=True, default="")

    # 20
    spi = models.CharField(max_length=1, blank=True, default="")

    # 21
    on_ground = models.CharField(max_length=1, blank=True, default="")

    # additional aircraft details
    aircraft_type = models.CharField(max_length=30, blank=True, default="")
    aircraft_full_type = models.CharField(max_length=60, blank=True, default="")
