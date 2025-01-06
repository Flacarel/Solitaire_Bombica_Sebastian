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

class Solitaire:
    def __init__(self):
        self.stock = Stock()
        self.waste = Pile()
        self.tableau = [Tableau() for _ in range(7)]
        self.foundation = [
            Foundation(suit) for suit in ["hearts", "diamonds", "spades", "clubs"]
        ]
        self.setup_game()

    def draw_from_stock(self):
        """Trage o carte din stiva Stock in Waste."""
        if self.stock.is_empty():
            raise ValueError("Stock is empty!")
        card = self.stock.remove_card()
        self.waste.add_card(card)
        return card

    def move_from_waste_to_tableau(self, tableau_index):
        """Muta o carte din Waste pe o stiva Tableau."""
        if self.waste.is_empty():
            raise ValueError("Waste is empty!")
        card = self.waste.peek()
        tableau = self.tableau[tableau_index]
        if tableau.can_add_card(card):
            tableau.cards.append(self.waste.remove_card())
            tableau.face_up_cards += 1
            return True
        raise ValueError(f"Cannot move {card} to Tableau {tableau_index + 1}")

    def move_from_waste_to_foundation(self):
        """Muta o carte din Waste intr-o stiva Foundation."""
        if self.waste.is_empty():
            raise ValueError("Waste is empty!")
        card = self.waste.peek()
        for foundation in self.foundation:
            if foundation.can_add_card(card):
                foundation.add_card(self.waste.remove_card())
                return True
        raise ValueError(f"Cannot move {card} to any Foundation")

    def recycle_stock(self):
        """Reumple Stock cu cartile din Waste."""
        if not self.stock.is_empty():
            raise ValueError("Stock is not empty! You cannot recycle")
        self.stock.cards = list(reversed(self.waste.cards))
        self.waste.cards = []

    def setup_game(self):
        """Initializeaza jocul distribuind cartile."""
        deck = Deck()
        deck.shuffle()

        for i in range(7):
            for j in range(i + 1):
                card = deck.deal_one()
                self.tableau[i].add_card(card)
                if j == i:
                    self.tableau[i].face_up_cards += 1
        self.stock.cards = deck.cards

    def setup_almost_win_state(self):
        """Configureaza jocul intr-o stare aproape castigatoare."""
        self.stock.cards = []
        self.waste.cards = []
        self.tableau = []
        self.foundation = []

        suits = ["hearts", "diamonds", "clubs", "spades"]
        for suit in suits:
            foundation_cards = [Card(value, suit) for value in range(1, 13)]
            foundation = Foundation(suit)
            for card in foundation_cards:
                foundation.add_card(card)
            self.foundation.append(foundation)

        for suit in suits:
            tableau = Tableau()
            king_card = Card(13, suit)
            tableau.add_cards([king_card])
            tableau.face_up_cards = 1
            self.tableau.append(tableau)

    def __str__(self):
        """Debug"""
        tableau_str = "\n".join(
            [f"Tableau {i + 1}: {str(t)}" for i, t in enumerate(self.tableau)]
        )
        foundation_str = "\n".join([str(f) for f in self.foundation])
        return (
            f"Stock: {len(self.stock.cards)} cards\n\n{tableau_str}\n\n{foundation_str}"
        )

    def move_to_foundation(self, tableau_index):
        """Muta o carte din Tableau intr-un Foundation."""
        tableau = self.tableau[tableau_index]
        card = tableau.peek()
        if card:
            for foundation in self.foundation:
                if foundation.can_add_card(card):
                    foundation.add_card(tableau.remove_card())
                    tableau.reveal_card()
                    return True
        return False

    def move_within_tableau(self, from_index, to_index, start_card_index):
        """Mută o secvență de cărți de la un Tableau la altul."""
        from_tableau = self.tableau[from_index]
        to_tableau = self.tableau[to_index]

        print(
            f"Attempting to move from Tableau {from_index + 1} to Tableau {to_index + 1}"
        )
        print(f"Cards to move: {from_tableau.cards[start_card_index:]}")
        print(f"Target tableau top card: {to_tableau.peek()}")

        if start_card_index < len(from_tableau.cards) - from_tableau.face_up_cards:
            raise ValueError("Cannot move hidden cards")

        cards_to_move = from_tableau.cards[start_card_index:]

        if not to_tableau.can_add_card(cards_to_move[0]):
            print(
                f"Move not allowed: {cards_to_move[0]} cannot be placed on {to_tableau.peek()}"
            )
            raise ValueError("Invalid move according to Solitaire rules")

        from_tableau.cards = from_tableau.cards[:start_card_index]
        from_tableau.face_up_cards = max(
            0, from_tableau.face_up_cards - len(cards_to_move)
        )
        to_tableau.add_cards(cards_to_move)

        from_tableau.reveal_card()

        print(f"Move successful. Tableau {to_index + 1} now has: {to_tableau.cards}")

    def move_from_stock_to_tableau(self, tableau_index):
        """Muta o carte din Stock pe un Tableau."""
        if self.stock.is_empty():
            raise ValueError("Stock is empty!")

        card = self.stock.peek()
        tableau = self.tableau[tableau_index]
        print(f"Attempting to move {card} from Stock to Tableau {tableau_index + 1}")
        if tableau.can_add_card(card):
            tableau.add_cards([self.stock.remove_card()])
            print(f"Move successful: {card} added to Tableau {tableau_index + 1}")
            return True
        raise ValueError(f"Cannot move {card} to Tableau {tableau_index + 1}")

    def move_from_stock_to_foundation(self):
        """Muta o carte din Stock intr-un Foundation."""
        if self.stock.is_empty():
            raise ValueError("Stock is empty!")

        card = self.stock.peek()

        for foundation in self.foundation:
            if foundation.can_add_card(card):
                foundation.add_card(self.stock.remove_card())
                return True
        raise ValueError(f"Cannot move {card} to any Foundation")

    def check_win(self):
        """Verifica daca jocul este castigat."""
        return all(len(f.cards) == 13 for f in self.foundation)


