from django.test import TestCase
from django.urls import reverse
from .models import Player, Team


class PlayerModelTests(TestCase):
	def setUp(self):
		Team.objects.create(name="Evil Geniuses")

	def test_availability(self):
		player = Player(name="Arteezy", team=Team.objects.get(name="Evil Geniuses"), bracket=200, stars=250, preference=0, availability=4)
		availability = 4
		for i in range(12):
			if i==3:
				self.assertTrue(player.is_available(i))
			else:
				self.assertFalse(player.is_available(i))

