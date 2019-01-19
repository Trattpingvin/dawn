from tournament.models import Player, Team

def populate_player_database(filename):
	with open(filename) as f:
		for line in f:
			stripline = line.strip()
			splitline = stripline.split(',')
			try:
				p = Player(*splitline)
				p.save()
			except ValueError:
				import pdb
				pdb.set_trace()
				print("hi")
				raise

def populate_team_database():
	teams = ["Asteroid Alpacas", "Belters", "Circus", "Donkeys"]
	for team in teams:
		Team(name=team).save()

def empty_player_database():
	for p in Player.objects.all():
		p.delete()