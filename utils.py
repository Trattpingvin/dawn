from tournament.models import Player, Team

def populate_player_database(filename="players.csv"):
	with open(filename) as f:
		for line in f:
			stripline = line.strip()
			splitline = stripline.split(',')

			try:
				assert len(splitline)==9
				p = Player(*splitline)
				p.save()
			except:
				import pdb
				pdb.set_trace()
				print("hi")
				raise

def populate_team_database():
	teams = ["Team A", "Team B", "Team C", "Team D"]
	for team in teams:
		Team(name=team).save()

def empty_player_database():
	for p in Player.objects.all():
		p.delete()

def reset():
	empty_player_database()
	populate_player_database()
