from ..models import Tournament
from django.shortcuts import get_object_or_404

def tournament_add_user(user, tournament_pk):
    tournament = get_object_or_404(Tournament, pk=tournament_pk)
    if not user in tournament.players.all():
        tournament.players.add(user)
        
        
def tournament_delete_user(user, tournament_pk):
    tournament = get_object_or_404(Tournament, pk=tournament_pk)
    if user in tournament.players.all():
        tournament.players.remove(user)