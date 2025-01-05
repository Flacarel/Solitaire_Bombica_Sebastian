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

class Pile:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """Adauga o carte in stiva."""
        self.cards.append(card)

    def remove_card(self):
        """Scoate ultima carte din stiva."""
        if self.cards:
            return self.cards.pop()
        else:
            raise ValueError("Pile is empty")

    def is_empty(self):
        """Verifica daca stiva este goala."""
        return len(self.cards) == 0

    def peek(self):
        """Returneaza ultima carte din stiva fara a o elimina."""
        if not self.is_empty():
            return self.cards[-1]
        else:
            return None

    def __str__(self):
        return f"Pile({len(self.cards)} cards): {self.cards}"


class Stock(Pile):
    def __init__(self, cards=None):
        super().__init__()
        if cards:
            self.cards = cards
        else:
            self.cards = []

    def draw_card(self):
        """Extrage o carte din stiva."""
        if not self.is_empty():
            return self.remove_card()
        else:
            raise ValueError("Stock is empty")

    def refill(self, cards):
        """Reumple stiva cu un set de carti."""
        self.cards.extend(cards)

    def __str__(self):
        return f"Stock({len(self.cards)} cards)"


class Foundation(Pile):
    def __init__(self, suit):
        super().__init__()
        self.suit = suit

    def can_add_card(self, card):
        """Verifica daca o carte poate fi adaugata la aceasta stiva."""
        print(f"Checking if {card} can be added to {self.peek()}")
        if card.suit != self.suit:
            return False
        else:
            if self.is_empty():
                return card.value == 1  # as
            return card.value == self.peek().value + 1

    def add_card(self, card):
        """Adauga o carte la stiva daca aceasta este valida."""
        if self.can_add_card(card):
            super().add_card(card)
        else:
            raise ValueError(f"Cannot add {card} to Foundation of {self.suit}")

    def __str__(self):
        return f"Foundation({self.suit}, {len(self.cards)} cards): {self.cards}"


class Tableau(Pile):
    def __init__(self):
        super().__init__()
        self.face_up_cards = 0

    def can_add_card(self, card):
        """Verifica daca o carte poate fi adaugata pe stiva conform regulilor."""
        top_card = self.peek()
        print(f"Checking if {card} can be added to {top_card}")
        if self.is_empty():
            return card.value == 13
        return card.value == top_card.value - 1 and (
            (
                card.suit in ["hearts", "diamonds"]
                and top_card.suit in ["spades", "clubs"]
            )
            or (
                card.suit in ["spades", "clubs"]
                and top_card.suit in ["hearts", "diamonds"]
            )
        )

    def add_cards(self, cards):
        """Adauga un set de carti pe stiva."""
        if not cards:
            raise ValueError("No cards to add to the pile")
        if self.can_add_card(cards[0]):
            self.cards.extend(cards)
            self.face_up_cards += len(cards)
        else:
            raise ValueError(f"Cannot add this cards to the pile {cards}")

    def remove_cards(self, index):
        """Scoate toate cartile de la un anumit index."""
        if index < 0:
            index += len(self.cards)
        if index < len(self.cards) - self.face_up_cards:
            raise ValueError("Cannot remove hidden cards")
        removed = self.cards[index:]
        print(f"Removing cards: {removed} from Tableau")
        self.cards = self.cards[:index]
        self.face_up_cards = max(0, self.face_up_cards - len(removed))
        return removed

    def remove_card(self):
        """Scoate ultima carte vizibila din stiva."""
        if not self.is_empty():
            removed_card = self.cards.pop()
            self.face_up_cards = max(0, self.face_up_cards - 1)
            self.reveal_card()
            return removed_card
        else:
            raise ValueError("Cannot remove a card from an empty tableau.")

    def reveal_card(self):
        """Expune o carte cu fata in jos daca toate cartile vizibile au fost eliminate."""
        if self.is_empty():
            self.face_up_cards = 0
        elif self.face_up_cards == 0:
            self.face_up_cards = 1

    def __str__(self):
        hidden_count = len(self.cards) - self.face_up_cards
        return f"Tableau({hidden_count} hidden, {self.face_up_cards} visible): {self.cards[-self.face_up_cards:]}"
