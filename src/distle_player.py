from edit_dist_utils import *
import random
from typing import *


class DistlePlayer:
    def start_new_game(self, dictionary: Set[str], max_guesses: int) -> None:
        self.dictionary: Set[str] = dictionary
        self.max_guesses: int = max_guesses
        self.possible_words: Set[str] = set(dictionary)
        self.previous_guesses: Set[str] = set()

    def make_guess(self) -> str:
        guess: str = random.choice(list(self.possible_words - self.previous_guesses))
        self.previous_guesses.add(guess)
        return guess

    def get_length(self, guess: str, transforms: List[str]) -> int:
        count: int = 0
        for char in transforms:
            if char == "I":
                count += 1
            elif char == "D":
                count -= 1
        length: int = len(guess) + count
        return length

    def get_feedback(self, guess: str, edit_dist: int, transforms: List[str]) -> None:
        length: int = self.get_length(guess, transforms)
        remove_words: Set[str] = set()
        for word in self.possible_words.copy():
            if len(word) != length:
                remove_words.add(word)
            elif edit_dist != edit_distance(guess, word):
                remove_words.add(word)
            elif transforms != get_transformation_list(guess, word):
                remove_words.add(word)

        self.possible_words -= remove_words
