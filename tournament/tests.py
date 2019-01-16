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

class GenMatchesViewTests(TestCase):
	def test_not_enough_players(self):
		url = reverse("genffa")
		r = self.client.get(url)
		self.assertEqual(r.status_code, 404)

	def test_one_match(self):
		url = reverse("genffa", args=(1,))

		dummy_t1 = Team(name="Alpacas").save()
        dummy_t2 = Team(name="Beltalawda").save()
        dummy_t3 = Team(name="Circus").save()
        dummy_t4 = Team(name="Donkeys").save()
        dummy_p1 = Player(name="Asimov", team=dummy_t1, bracket=2, stars=2, preference=7, availability=15).save()
        dummy_p2 = Player(name="Bradbury", team=dummy_t2, bracket=2, stars=2, preference=7, availability=15).save()
        dummy_p3 = Player(name="Clarke", team=dummy_t3, bracket=2, stars=2, preference=7, availability=15).save()
        dummy_p4 = Player(name="Heinlein", team=dummy_t4, bracket=2, stars=2, preference=7, availability=15).save()

        self.assertEqual(len(FFaMatch.objects.all()), 0)
        r = self.client.get(url)
        self.assertEqual(len(FFaMatch.objects.all()), 1)
        self.assertContains(r, "Heinlein")
        
