from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework import permissions, viewsets
from dashboard.serializers import SBSMessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Q
from datetime import date, datetime
from .models import SBSMessage
import operator

def index(request):
    # filter by transmission_type 3 or 4 for now (messages have more info)
    latest_sbs_messages = SBSMessage.objects \
        .filter(Q(transmission_type = 3) | Q(transmission_type = 4)) \
        .order_by("-date_message_generated", "-time_message_generated")[:60]
    template = loader.get_template("index.html")
    context = {"latest_sbs_messages": latest_sbs_messages}
    return HttpResponse(template.render(context, request))

def heard_on_date(request):
    latest_sbs_messages = SBSMessage.objects.filter(date_message_generated = date.today()) \
        .order_by("hex_ident", "-date_message_generated") \
        .distinct("hex_ident")[:20]
    template = loader.get_template("planesByDate.html")
    context = {"latest_sbs_messages": latest_sbs_messages}
    return HttpResponse(template.render(context, request))

def heard_today(request):
    """ display plans heard today, in descending dat/time order"""

    today = datetime.now().date()

    sbs_messages = SBSMessage.objects \
        .filter(Q(date_message_generated = today) ) \
        .distinct("hex_ident")
    
    sbs_messages_ordered = sorted(sbs_messages, key=operator.attrgetter('time_message_generated'), reverse=True)

    template = loader.get_template("today.html")
    context = {"latest_sbs_messages": sbs_messages_ordered}
    return HttpResponse(template.render(context, request))

# todo doesn't work as expected? replaced with APIVIew
# class SBSMessageViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows SBSMessages to be viewed or edited.
#     """
#     queryset = SBSMessage.objects.all().order_by("-date_message_generated")
#     serializer_class = SBSMessageSerializer
#     #permission_classes = [permissions.IsAuthenticated]

class SBSMessageList(APIView):
    """
    List all SBSMessages, or create a new SBSMessage.
    """
    def get(self, request, format=None):
        msg = SBSMessage.objects.all()
        serializer = SBSMessageSerializer(msg, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print("SBSMessageList.post() :")
        print(request)
        print("request.headers :")
        print(request.headers)
        print("request.data:")
        print(request.data)
        serializer = SBSMessageSerializer(data=request.data)
        if serializer.is_valid():
            print("SBSMessageList.post() is_valid : true")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("SBSMessageList.post() is_valid : false")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SBSMessageDetail(APIView):
    """
    Retrieve, update or delete a SBSMessage instance.
    """
    def get_object(self, pk):
        try:
            return SBSMessage.objects.get(pk=pk)
        except SBSMessage.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SBSMessageSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SBSMessageSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)