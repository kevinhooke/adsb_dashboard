from rest_framework import serializers

from .models import SBSMessage


class SBSMessageSerializer(serializers.Serializer):
    message_type = serializers.CharField()
    transmission_type = serializers.IntegerField()
    session_id = serializers.IntegerField()
    aircraft_id = serializers.IntegerField(required=False)
    hex_ident = serializers.CharField()
    flight_id = serializers.CharField(required=False, allow_blank=True)
    date_message_generated = serializers.DateField()
    date_message_logged = serializers.DateField()
    callsign = serializers.CharField(required=False, allow_blank=True)
    altitude = serializers.IntegerField(required=False)
    ground_speed = serializers.IntegerField(required=False)
    track = serializers.CharField(required=False, allow_blank=True)
    latitude = serializers.CharField(required=False, allow_blank=True)
    longitude = serializers.CharField(required=False, allow_blank=True)
    vertical_rate = serializers.IntegerField(required=False)
    squawk = serializers.CharField(required=False, allow_blank=True)
    alert_squawk_change = serializers.CharField(required=False, allow_blank=True)
    emergency = serializers.CharField(required=False, allow_blank=True)
    spi = serializers.CharField(required=False, allow_blank=True)
    on_ground = serializers.CharField(required=False, allow_blank=True)
    # code = serializers.CharField(style={'base_template': 'textarea.html'})
    # linenos = serializers.BooleanField(required=False)
    # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    # style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `SBSMessage` instance, given the validated data.
        """
        return SBSMessage.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `SBSMessage` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance


# didn't work
# class SBSMessageSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = SBSMessage
#         fields = [
#             'message_type',
#             'transmission_type',
#             'session_id',
#             'date_message_generated',
#             'time_message_generated',
#             'aircraft_id',
#             'hex_ident',
#             'flight_id',
#             'date_message_logged',
#             'time_message_logged',
#             'callsign',
#             'altitude',
#             'ground_speed',
#             'track',
#             'atitude',
#             'longitude',
#             'vertical_rate',
#             'squawk',
#             'alert_squawk_change',
#             'emergency',
#             'spi',
#             'on_ground'
#         ]

#     def create(self, request):
#         post_data = request
#         print("Received request: ")
#         print(request)
#         return Response(data="ok")

#     @property
#     def errors(self):
#         # get errors
#         errors = super().errors
#         print("**** Serializer errors:")
#         print(errors)
