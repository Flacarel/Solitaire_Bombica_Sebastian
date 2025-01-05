import random

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        value_names = {1: "As", 11: "Jack", 12: "Queen", 13: "King"}
        value_str = value_names.get(self.value, str(self.value))
        return f"{value_str} of {self.suit}"

    def __repr__(self):
        return str(self)


class Deck:
    def __init__(self):
        self.cards = self.create_deck()

    def create_deck(self):
        """Creeaza un pachet complet de carti cu toate valorile si culorile posibile."""
        suits = ["hearts", "diamonds", "spades", "clubs"]
        values = list(range(1, 14))
        return [Card(value, suit) for suit in suits for value in values]

    def shuffle(self):
        """Amesteca cartile din pachet."""
        random.shuffle(self.cards)

    def deal_one(self):
        """Returneaza si elimina o carte din pachet."""
        if self.cards:
            return self.cards.pop()
        else:
            raise ValueError("The deck is empty")

    def __str__(self):
        return f"Deck with {len(self.cards)} cards: {self.cards}"
