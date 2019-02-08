from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from tournament.models import *
from tournament.forms import *
from . import constants
from utils import calc_rating_change, parse_ajax_to_json, assign_location


class DayView(View):
    def get(self, request, day=None, start_match=-1):
        if not day:
            return HttpResponse("Invalid day")
        context = {}
        db_matches = Match.objects.filter(day=day, published=True).order_by('round')

        for match in db_matches:
            match.orderedplayers = match.players.all().order_by('team')

        context['start_match'] = start_match
        context["matches"] = db_matches

        return render(request, "schedule/day"+str(day)+".html", context)


class PlayerView(View):
    def get(self, request, player_id=None):

        if player_id:
            player = get_object_or_404(Player, id=player_id)
        else:
            return HttpResponse("Player not chosen")

        winloss = player.get_wins()
        awards = player.format_awards()
        award_score = awards[0]
        score = winloss[0] + award_score
        availability = []
        date = ["Jan 26", "Jan 27", "Feb 2", "Feb 3"]
        for i in range(4):
            if player.is_available(i+1): availability.append(1)
            else:
                availability.append(0)

        # "Mars 1" "Ceres 2" "Io 4"
        preference = [bool(player.preference&1), bool(player.preference&2), bool(player.preference&4)]

        return render(request, "playerdetail.html", {
            "player": player, "score": score, "award": awards[1], "availability": zip(availability, date),
            "loc": preference,
            })


class MatchStagingView(View):
    # TODO:
    #   Hovering over a player highlights all their occurances
    #   Automatically sort matches
    #   Multi select. When I click match frame, select all players in it.
    #   Prevent veto'd locations
    #
    #
    #
    def get(self, request, day=None):
        if day:   # TODO change p.name to anonmyous name
            players = [{'id': p.id, 'name': p.name + ' ({})'.format(p.bracket), 'bracket': p.bracket, 'team': p.team.id, 'played': p.get_num_matches()}
                       for p in Player.objects.all() if p.is_available(day)]
            response_matches = [[{'id': p.id, 'name': p.name + ' ({})'.format(p.bracket), 'bracket': p.bracket, 'team': p.team.id, 'played': p.get_num_matches()}
                       for p in m.get_players()] #SORRY!!!!!!!!!! CLOSE YOUR EYES!!! DONT READ THIS LINE!!!
                                for m in Match.objects.filter(day=day, published=False)]
            return JsonResponse({'players': players, "matches": response_matches})
        else:
            return render(request, 'matchmaking/staging.html', {"days": range(1, 1 + constants.days),
                                                                "num_matches": constants.matches})

    def post(self, request, day=None):
        Match.objects.filter(day=day, published=False).delete()
        if not request.POST:
            return HttpResponse("Found no matches")

        json_response = parse_ajax_to_json(request.body)
        matches = json_response['matches']
        for i, match in enumerate(matches):
            players = match['players']
            if players:
                m = Match(day=day, published=False, mode="F", round=i+1)
                m.save()
                for p in players:
                    #parse through the weird transofmration i did in javascript
                    parsed_id = p['id'][p['id'].find('-')+1:]
                    parsed_id = parsed_id[:parsed_id.find('-')]
                    player = Player.objects.get(id=parsed_id)
                    m.players.add(player)
                assign_location(m)
                m.save()


        return HttpResponse("Done")


class PlayersView(View):
    def get(self, request):
        teams = Team.objects.all().order_by('id')
        for t in teams:
            res = 0
            for player in t.player_set.all():
                res += player.get_score()
            t.teamscore = round(res,1)

        return render(request, 'players.html', {"teams": teams})


class ScoreMatchView(View):
    # TODO: stop taking num_awards as argument. instead add button to add or remove award forms at will in the template
    def get(self, request, match_id=None):
        if not match_id:
            return HttpResponse("Bad match id")
        match = Match.objects.get(id=match_id)
        if match.result:
            return HttpResponse("Match already scored!")
        players = match.get_players()
        scoreform = get_scorematch_form(players)(prefix='matchresult')
        awardform = get_award_formset(players)(prefix='award')
        return render(request, 'matchmaking/scorematch.html', {"scoreform": scoreform,
                                                               "awardformset": awardform,
                                                               "match_id": match_id})

    def post(self, request, match_id=None):
        if not match_id:
            return HttpResponse("Didn't get a match id in POST")
        match = Match.objects.get(id=match_id)
        if match.result:
            return HttpResponse("Match already scored? from POST")
        players = match.get_players()
        score_form = get_scorematch_form(players)(request.POST, prefix='matchresult')
        award_form = get_award_formset(players)(request.POST, prefix='award')

        if score_form.is_valid():
            print(score_form)

        if score_form.is_valid() and award_form.is_valid():
            if len(score_form.cleaned_data) > 1:
                return HttpResponse("Multiple score forms sent to ScoreMatchView - not supported")
            score_form = score_form[0]
            matchwinner = score_form.cleaned_data['matchwinner']
            matchresult = MatchResult(winner=matchwinner)
            matchresult.save()

            for p in players:
                b, s = calc_rating_change(p.bracket, p.stars, p == matchwinner, len(match.get_players()))
                ratingchange = RatingChange(player=p, matchresult=matchresult, bracket_before=p.bracket, bracket_after=b,
                                            stars_before=p.stars, stars_after=s)
                ratingchange.save()
                p.bracket = ratingchange.bracket_after
                p.stars = ratingchange.stars_after
                p.save()

            for award in award_form.cleaned_data:
                Award(player=award['winner'], award=award['award'], match=matchresult).save()

            match.result = matchresult
            match.save()

            if 'from' in request.GET:
                return redirect(request.GET['from'])

            return redirect('admin:index')

        return HttpResponse("Not good")
        # in ffa, winner gets 2 stars. in 1v1, winner gets 1 star
        # everyone else loses one star
        # if i go to -1 star bracket is -1 and star = 3
        # if i to to 4+ stars, bracket is +1 and star = 1


class MainView(View):
    def get(self, request):
        return render(request, 'matchmaking/matchmaking.html', {"object_list": Match.objects.all()})


class RemoveMatchView(View):
    def post(self, request, match_id=None):
        match = get_object_or_404(Match, id=match_id)
        match.delete()
        return HttpResponse("OK")


class MatchView(View):
    def get(self, request, match_id=None, rnd=0):
        r = rnd
        if match_id:
            ans = get_object_or_404(Match, id=match_id)
            awd = ans.get_awards()
        else:
            return HttpResponse("shouldn't happen")
        players = ans.players.all().order_by('team')
        if ans.result:
            for p in players:
                p.totalscore = len(ans.get_awards().filter(player=p)) * 0.2 + int(ans.result.winner == p)
                p.ratingchange = RatingChange.objects.filter(matchresult=ans.result, player=p)[0]

        return render(request, "matchmaking/detail.html", {"match": ans, "round": r, "award": awd, "players": players})

    def post(self, request):
        return HttpResponse("how did this happen?")