from tournament.models import Player, Team

def populate_player_database(filename):
	with open(filename) as f:
		for line in f:
			# TODO change input format to CSV
			stripline = line.strip()
			splitline = stripline.split(' ')
			p = Player(*splitline)
			p.save()#might need to grab the team reference from the database - #TODO test that

def populate_team_database():
	teams = ["Asteroid Alpacas", "Belters", "Circus", "Donkeys"]
	for team in teams:
		Team(name=team).save()