import operator
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.template import loader
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.serializers import SBSMessageSerializer

from .models import SBSMessage


def index(request):
    # filter by transmission_type 3 or 4 for now (messages have more info)
    qs = SBSMessage.objects.filter(Q(transmission_type=3) | Q(transmission_type=4)).order_by(
        "-date_message_generated", "-time_message_generated"
    )
    # paginate the results
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    template = loader.get_template("index.html")
    context = {"page_obj": page_obj}
    return HttpResponse(template.render(context, request))


def heard_on_date(request):
    template = loader.get_template("planesByDate.html")
    context = {}
    if request.POST:
        submitted_date = request.POST["selecteddate"]
        if submitted_date is not None:
            latest_sbs_messages = SBSMessage.objects.filter(
                Q(date_message_generated=submitted_date) & (Q(transmission_type="1") | Q(transmission_type="5"))
            ).distinct("hex_ident")

            sbs_messages_ordered = sorted(
                latest_sbs_messages,
                key=operator.attrgetter("time_message_generated"),
                reverse=True,
            )
            context = {
                "latest_sbs_messages": sbs_messages_ordered,
                "selected_date": submitted_date,
            }
    return HttpResponse(template.render(context, request))


def heard_today(request):
    """display plans heard today, in descending dat/time order"""

    today = datetime.now().date()

    sbs_messages = SBSMessage.objects.filter(
        Q(date_message_generated=today) & (Q(transmission_type="1") | Q(transmission_type="5"))
    ).distinct("hex_ident")

    sbs_messages_ordered = sorted(sbs_messages, key=operator.attrgetter("time_message_generated"), reverse=True)

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
