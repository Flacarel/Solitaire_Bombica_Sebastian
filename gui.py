import tkinter as tk
from PIL import Image, ImageTk
from game_logic import Solitaire


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