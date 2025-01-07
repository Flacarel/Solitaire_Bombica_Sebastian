import tkinter as tk
from PIL import Image, ImageTk
from game_logic import Solitaire
from tkinter import Button


class SolitaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solitaire")

        self.game = Solitaire()
        self.selected_stack = None
        self.selected_card_index = None

        self.canvas_width = 1600
        self.canvas_height = 1200
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height, bg="green"
        )
        self.canvas.pack()

        self.card_width = 100
        self.card_height = 150
        self.padding = 25

        self.card_images = self.load_card_images()

        self.move_count = 0

        self.setup_ui()
        self.draw_game()

    def load_card_images(self):
        """Incarca si redimensioneaza imaginile cartilor din fisiere. Returneaza un dictionar cu imaginile cartilor."""
        images = {}
        suits = ["hearts", "diamonds", "clubs", "spades"]
        for suit in suits:
            for value in range(1, 14):
                image_name = f"cards/{value}_of_{suit}.png"
                original_image = Image.open(image_name)
                resized_image = original_image.resize(
                    (self.card_width, self.card_height), Image.LANCZOS
                )
                images[(value, suit)] = ImageTk.PhotoImage(resized_image)

        back_image = Image.open("cards/back2.png")
        resized_back = back_image.resize(
            (self.card_width, self.card_height), Image.LANCZOS
        )
        images["back"] = ImageTk.PhotoImage(resized_back)
        return images
    
    def setup_ui(self):
        """Configureaza butoanele de interfata pentru resetarea jocului si pentru setarea unei stari aproape castigatoare."""
        self.canvas.bind("<Button-1>", self.on_click)

        button_width = 12
        button_height = 2
        button_padding = 20
        button_x = self.canvas_width - 180
        button_y_start = 20

        reset_button = Button(
            self.root,
            text="Reset Game",
            command=self.reset_game,
            width=button_width,
            height=button_height,
            bg="red",
            fg="white",
        )
        reset_button.place(x=button_x, y=button_y_start)

        almost_win_button = Button(
            self.root,
            text="Almost Win",
            command=self.reset_to_almost_win,
            width=button_width,
            height=button_height,
            bg="blue",
            fg="white",
        )
        almost_win_button.place(
            x=button_x, y=button_y_start + button_padding + (button_height * 20)
        )

    def reset_to_almost_win(self):
        """Seteaza jocul intr-o stare aproape castigatoare. Reseteaza numarul de mutari si redeseneaza jocul."""
        self.game.setup_almost_win_state()
        self.move_count = 0
        self.draw_game()
        print("Game set to an almost-win state.")

    def reset_game(self):
        """Reseteaza jocul la starea initiala, creand o instanta noua a jocului si actualizand interfata."""
        self.game = Solitaire()
        self.selected_stack = None
        self.selected_card_index = None
        self.move_count = 0
        self.draw_game()
        print("Game has been reset.")

    
    def draw_game(self):
        """Deseneaza starea curenta a jocului pe canvas, incluzand stivele de carti si mesajele relevante."""
        self.canvas.delete("all")

        x_offset = (self.canvas_width - (7 * (self.card_width + self.padding))) // 2

        self.canvas.create_text(
            100, 50, text=f"Moves: {self.move_count}", font=("Arial", 16), fill="white"
        )

        if self.game.stock.is_empty():
            self.draw_empty_stock_button(x_offset, 10)
        else:
            self.draw_pile(self.game.stock.cards, x_offset, 10, "Stock", hidden=True)

        self.draw_pile(
            self.game.waste.cards[-1:],
            x_offset + self.card_width + self.padding,
            10,
            "Waste",
        )

        suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        for i, foundation in enumerate(self.game.foundation):
            x = x_offset + (2 + i) * (self.card_width + self.padding)
            self.draw_pile(foundation.cards[-1:], x, 10, suits[i])

        for i, tableau in enumerate(self.game.tableau):
            x = x_offset + i * (self.card_width + self.padding)
            self.draw_tableau(tableau, x, 250)

        if self.game.check_win():
            self.display_win_message()

    def display_win_message(self):
        """Afiseaza un mesaj de castig pe ecran cand jucatorul a castigat"""
        self.canvas.create_text(
            self.canvas_width / 2,
            self.canvas_height / 2,
            text="Congratulations! You won!",
            font=("Arial", 32),
            fill="white",
        )

    def draw_empty_stock_button(self, x, y):
        """Deseneaza un buton pentru reciclarea stivei Stock atunci cand aceasta este goala."""
        button = Button(
            self.root,
            text="Recycle Stock",
            command=self.recycle_stock,
            width=12,
            height=2,
            bg="yellow",
        )
        self.canvas.create_window(
            x + self.card_width / 2, y + self.card_height / 2, window=button
        )

    def recycle_stock(self):
        """Reumple stiva Stock din cartile Waste. Actualizeaza interfata si gestioneaza erorile."""
        try:
            self.game.recycle_stock()
            self.draw_game()
        except ValueError as e:
            print(f"Recycle error: {e}")

    def draw_pile(self, cards, x, y, label, hidden=False):
        """Deseneaza o stiva de carti pe canvas. Poate afisa ultima carte sau o stiva goala."""
        if cards:
            card = cards[-1]
            self.draw_card(card, x, y, face_up=not hidden)
        else:
            self.draw_empty_slot(x, y)

        self.canvas.create_text(
            x + self.card_width / 2, y + self.card_height + 10, text=label, fill="white"
        )

    def draw_tableau(self, tableau, x, y):
        """Deseneaza o stiva Tableau, incluzand cartile vizibile si ascunse."""
        for i, card in enumerate(tableau.cards):
            if isinstance(card, list):
                card = card[0]
            offset_y = y + i * 20
            face_up = i >= len(tableau.cards) - tableau.face_up_cards
            self.draw_card(card, x, offset_y, face_up=face_up)

    def draw_card(self, card, x, y, face_up=True):
        """Deseneaza o carte specifica la o anumita pozitie pe canvas, fie cu fata in sus, fie cu spatele."""
        if face_up:
            card_image = self.card_images.get((card.value, card.suit))
            if card_image:
                self.canvas.create_image(x, y, anchor="nw", image=card_image)
            else:
                self.canvas.create_rectangle(
                    x,
                    y,
                    x + self.card_width,
                    y + self.card_height,
                    fill="white",
                    outline="black",
                )
                self.canvas.create_text(
                    x + self.card_width / 2,
                    y + self.card_height / 2,
                    text=str(card),
                    fill="black",
                )
        else:
            back_image = self.card_images["back"]
            self.canvas.create_image(x, y, anchor="nw", image=back_image)

    def draw_empty_slot(self, x, y):
        """Deseneaza un spatiu gol pentru o stiva de carti."""
        self.canvas.create_rectangle(
            x,
            y,
            x + self.card_width,
            y + self.card_height,
            fill="",
            outline="white",
            dash=(3, 5),
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()
