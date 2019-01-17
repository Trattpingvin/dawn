from tournament.models import Player

def populate_player_database(filename):
	with open(filename) as f:
		for line in f:
			splitline = line.splitline()
			Player(*splitline).save()
