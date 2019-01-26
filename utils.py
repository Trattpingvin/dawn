from tournament.models import Player, Team, Match


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


def parse_weeks_matches(day):
	try:
		matches = Match.objects.filter(day=day, parsed=False)
		for match in matches:
			if not match.result: #should probably have this in the filter but i'm not sure how
				continue
			match.parsed = True
			res = match.result
			for rc in res.ratingchange_set.all():
				rc.player.stars = rc.stars_after
				rc.player.bracket = rc.bracket_after
				rc.player.save()
			match.save()
	except:
		import pdb
		pdb.set_trace()
		raise


def reset():
	empty_player_database()
	populate_player_database()


def calc_rating_change(bracketbefore, starsbefore, winner, ffa):
	MAX_STAR = 3
	MIN_STAR = 0
	MAX_BRACKET = 5
	MIN_BRACKET = 1

	STAR_AFTER_UPGRADE = 1
	STAR_AFTER_DOWNGRADE = 3
	bracketafter, starsafter = bracketbefore, starsbefore
	if ffa:
		stars_gained = 2
	else:
		stars_gained = 1
	if winner:
		starsafter = starsbefore + stars_gained
	else:
		starsafter = starsbefore - 1

	if starsafter < MIN_STAR:
		if bracketbefore > MIN_BRACKET:
			bracketafter -= 1
			starsafter = STAR_AFTER_DOWNGRADE
		else:
			bracketafter = MIN_BRACKET
			starsafter = MIN_STAR

	if starsafter >= MAX_STAR + 1:
		if bracketbefore < MAX_BRACKET:
			bracketafter = bracketbefore + 1
			starsafter = STAR_AFTER_UPGRADE
		else:
			bracketafter = MAX_BRACKET
			starsafter = MAX_STAR

	return bracketafter, starsafter
