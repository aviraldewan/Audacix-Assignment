from django.urls import path
from . import views

# declare the app name
app_name = "hangman_game"

# url patterns for our app
""" "game/new"
    Method- GET
    AIM- starts a new game """
""" "game/<int:id>"
    Method- GET
    AIM- gives the current state of game with id """
""" "game/<int:id>/guess"
     Method- GET 
     AIM- Returns an HTML form page
     Method- POST
     AIM- submits the guessed character by user and returns 
          game state and whether guessed char by user is
          correct or incorrect """
urlpatterns = [
    path("game/new", views.create_new_game, name="create_new_game"),
    path("game/<int:id>", views.get_game_state, name="get_game_state"),
    path("game/<int:id>/guess", views.guess_char, name="guess_char")
]
