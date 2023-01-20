from django.db import models

# Game Model
""" stores:-
    -> game state
    -> actual word(randomly selected by program)
    -> current state of word
    -> next character to be guessed
    -> wrong guesses made by the user
    -> wrong guesses left  """
class Game(models.Model):
    game_state = models.CharField(max_length=10)
    actual_word = models.CharField(max_length=7)
    word_state = models.CharField(max_length=7)
    curr_char_pos = models.IntegerField()
    wrong_guesses_made = models.IntegerField()
    wrong_guesses_left = models.IntegerField()

    # returns all information of the game
    def __str__(self):
        return f"{self.id}: Game State- {self.game_state}, Actual Word- {self.actual_word}, Word State- {self.word_state}, Attempts Used- {self.wrong_gusses_made}, Attemps Left- {self.wrong_guesses_left}"
