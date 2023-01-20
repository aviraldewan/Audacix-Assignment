from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Game
import random
import math

""" word_list stores the list of words which can be randomly
    selected by the program when "game/new" route is accessed """
word_list = ["Hangman", "Python", "Audacix", "Bottle", "Pen"]


""" route- "game/new"
    AIM- create a new game """
def create_new_game(request):

    # select a random word from word_list for this game
    curr_game_word = random.choice(word_list)
    
    word_size = len(curr_game_word)

    # initial state of word is number of underscores("_") as the word length
    initial_word_state = "_" * word_size

    # user will have attempts equal to half the size of randomly selected word
    initial_attempts_left = math.ceil(word_size/2)

    # create a new game in database
    create_game = Game(game_state="InProgress", actual_word=curr_game_word, word_state=initial_word_state,
                       curr_char_pos=0, wrong_guesses_made=0, wrong_guesses_left=initial_attempts_left)
    
    # save all the changes in database
    create_game.save()

    # return the created game's ID
    return JsonResponse({"Game ID": create_game.id})


""" route- "game/<int:id>"
    AIM- returns the state of game with id = id """
def get_game_state(request, id):

    # check whether game with given id exists, otherwise raise error
    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        raise JsonResponse({"Error": "Game with entered id doesn't exist"})

    # extract the information of game with provided id
    curr_state = game.game_state
    word_state = game.word_state
    wrong_guesses_made = game.wrong_guesses_made
    wrong_guesses_left = game.wrong_guesses_left

    # store the game's information in an object
    game_data = {
        "Game State": curr_state,
        "Word State": word_state,
        "Attempts Made": wrong_guesses_made,
        "Attempts Left": wrong_guesses_left
    }

    # return the game's data in JSON format
    return JsonResponse(game_data)


""" route- "game/<int:id>/guess
    AIM- check whether inputted character is correct or not
         and return the game's state """
def guess_char(request, id):

    # if method is "GET" return an HTML form page
    if request.method == "GET":
        return JsonResponse({"Error": "HTML form page here"})

    # check if game with given id exists, otherwise raise error
    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        raise JsonResponse({"Error": "Game with entered id doesn't exist"})

    # check whether game has already ended
    if game.curr_char_pos == len(game.actual_word):
        return JsonResponse({"Game State": game.game_state, "Verdict": "Game is already over"})

    # check if the user has enterd a valid single character or not
    if request.guessed_char.isalpha() == False:
        return JsonResponse({"Error": "Input contains invalid characters"})
    elif len(request.guessed_char) > 1:
        return JsonResponse({"Error": "Input must contain only 1 character"})

    # curr_pos stores the current character of actual word which user needs to identify
    curr_pos = game.curr_char_pos

    if game.actual_word[curr_pos] == request.guessed_char:

        # if this is the final character and user guessed it right then the game is "WON"
        if curr_pos + 1 == len(game.actual_word):
            game.game_state = "WON"

        # update the changes in database
        updated_word_state = game.word_state
        updated_word_state[curr_pos] = request.guessed_char
        game.word_state = updated_word_state

        game.curr_char_pos = curr_pos + 1
        game.save()

        # store the updated information in an object
        game_data = {
            "Game State": game.game_state,
            "Verdict": "Correct Guess"
        }

        # return the information in JSON format
        return JsonResponse(game_data)
    else:
        
        # the guess was wrong
        # update the wrong guesses made and attempts left by user
        game.wrong_guesses_made = game.wrong_guesses_made + 1
        game.wrong_guesses_left = game.wrong_guesses_left - 1

        # if no more attempts are left, then the user has "LOST"
        if game.wrong_guesses_left == 0:
            game.game_state = "LOST"

        # save the changes in DB
        game.save()

        # store the new information in an object
        game_data = {
            "Game State": game.game_state,
            "Verdict": "Wrong Guess"
        }

        # return the data in JSON format
        return JsonResponse(game_data)
