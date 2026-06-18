import unittest
from datetime import date

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from dashboard.models import SBSMessage


def make_message(**kwargs):
    defaults = {
        "message_type": "MSG",
        "transmission_type": 3,
        "session_id": 1,
        "aircraft_id": 1,
        "hex_ident": "ABC123",
    }
    defaults.update(kwargs)
    return SBSMessage.objects.create(**defaults)


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_returns_200(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_type3_messages_included_in_context(self):
        msg = make_message(transmission_type=3, hex_ident="AAA111")
        response = self.client.get(reverse("index"))
        self.assertIn(msg, list(response.context["latest_sbs_messages"]))

    def test_type4_messages_included_in_context(self):
        msg = make_message(transmission_type=4, hex_ident="BBB222")
        response = self.client.get(reverse("index"))
        self.assertIn(msg, list(response.context["latest_sbs_messages"]))

    def test_type1_messages_excluded_from_context(self):
        msg = make_message(transmission_type=1, hex_ident="CCC333")
        response = self.client.get(reverse("index"))
        self.assertNotIn(msg, list(response.context["latest_sbs_messages"]))

    def test_type2_messages_excluded_from_context(self):
        msg = make_message(transmission_type=2, hex_ident="DDD444")
        response = self.client.get(reverse("index"))
        self.assertNotIn(msg, list(response.context["latest_sbs_messages"]))

    def test_results_limited_to_60(self):
        for i in range(70):
            make_message(transmission_type=3, hex_ident=f"{i:06d}")
        response = self.client.get(reverse("index"))
        self.assertLessEqual(len(list(response.context["latest_sbs_messages"])), 60)


class HeardOnDateViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_returns_200(self):
        response = self.client.get(reverse("planesByDate"))
        self.assertEqual(response.status_code, 200)

    def test_get_has_no_messages_in_context(self):
        response = self.client.get(reverse("planesByDate"))
        self.assertNotIn("latest_sbs_messages", response.context)

    def test_post_returns_200(self):
        today = date.today().isoformat()
        response = self.client.post(reverse("planesByDate"), {"selecteddate": today})
        self.assertEqual(response.status_code, 200)

    def test_post_type1_messages_included_in_context(self):
        msg = make_message(transmission_type=1, hex_ident="DEF456")
        today = date.today().isoformat()
        response = self.client.post(reverse("planesByDate"), {"selecteddate": today})
        self.assertIn(msg, response.context["latest_sbs_messages"])

    def test_post_type5_messages_included_in_context(self):
        msg = make_message(transmission_type=5, hex_ident="GHI789")
        today = date.today().isoformat()
        response = self.client.post(reverse("planesByDate"), {"selecteddate": today})
        self.assertIn(msg, response.context["latest_sbs_messages"])

    def test_post_type3_messages_excluded_from_context(self):
        msg = make_message(transmission_type=3, hex_ident="JKL012")
        today = date.today().isoformat()
        response = self.client.post(reverse("planesByDate"), {"selecteddate": today})
        self.assertNotIn(msg, response.context["latest_sbs_messages"])

    def test_post_deduplicates_by_hex_ident(self):
        make_message(transmission_type=1, hex_ident="MNO345")
        make_message(transmission_type=1, hex_ident="MNO345")
        today = date.today().isoformat()
        response = self.client.post(reverse("planesByDate"), {"selecteddate": today})
        hex_idents = [m.hex_ident for m in response.context["latest_sbs_messages"]]
        self.assertEqual(hex_idents.count("MNO345"), 1)

    def test_post_returns_selected_date_in_context(self):
        today = date.today().isoformat()
        response = self.client.post(reverse("planesByDate"), {"selecteddate": today})
        self.assertEqual(response.context["selected_date"], today)


class HeardTodayViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_returns_200(self):
        response = self.client.get(reverse("today"))
        self.assertEqual(response.status_code, 200)

    def test_type1_messages_included_in_context(self):
        msg = make_message(transmission_type=1, hex_ident="PQR678")
        response = self.client.get(reverse("today"))
        self.assertIn(msg, response.context["latest_sbs_messages"])

    def test_type5_messages_included_in_context(self):
        msg = make_message(transmission_type=5, hex_ident="STU901")
        response = self.client.get(reverse("today"))
        self.assertIn(msg, response.context["latest_sbs_messages"])

    def test_type3_messages_excluded_from_context(self):
        msg = make_message(transmission_type=3, hex_ident="VWX234")
        response = self.client.get(reverse("today"))
        self.assertNotIn(msg, response.context["latest_sbs_messages"])

    def test_deduplicates_by_hex_ident(self):
        make_message(transmission_type=1, hex_ident="YZA567")
        make_message(transmission_type=1, hex_ident="YZA567")
        response = self.client.get(reverse("today"))
        hex_idents = [m.hex_ident for m in response.context["latest_sbs_messages"]]
        self.assertEqual(hex_idents.count("YZA567"), 1)


class SBSMessageListAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_returns_200(self):
        response = self.client.get("/api/sbsmessage/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_all_messages(self):
        make_message(hex_ident="LST001")
        make_message(hex_ident="LST002")
        response = self.client.get("/api/sbsmessage/")
        hex_idents = [m["hex_ident"] for m in response.data]
        self.assertIn("LST001", hex_idents)
        self.assertIn("LST002", hex_idents)

    def test_post_creates_message(self):
        today = date.today().isoformat()
        payload = {
            "message_type": "MSG",
            "transmission_type": 3,
            "session_id": 1,
            "hex_ident": "PST001",
            "date_message_generated": today,
            "date_message_logged": today,
        }
        response = self.client.post("/api/sbsmessage/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SBSMessage.objects.filter(hex_ident="PST001").exists())

    def test_post_returns_created_data(self):
        today = date.today().isoformat()
        payload = {
            "message_type": "MSG",
            "transmission_type": 4,
            "session_id": 2,
            "hex_ident": "PST002",
            "date_message_generated": today,
            "date_message_logged": today,
        }
        response = self.client.post("/api/sbsmessage/", payload, format="json")
        self.assertEqual(response.data["hex_ident"], "PST002")

    def test_post_with_missing_required_fields_returns_400(self):
        response = self.client.post("/api/sbsmessage/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SBSMessageDetailAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.msg = make_message(hex_ident="DET001")

    def test_get_existing_returns_200(self):
        response = self.client.get(f"/api/sbsmessage/{self.msg.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_correct_hex_ident(self):
        response = self.client.get(f"/api/sbsmessage/{self.msg.pk}/")
        self.assertEqual(response.data["hex_ident"], "DET001")

    def test_get_nonexistent_returns_404(self):
        response = self.client.get("/api/sbsmessage/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @unittest.skip("SBSMessageSerializer.update() is not implemented — PUT will raise NotImplementedError")
    def test_put_updates_message(self):
        pass
