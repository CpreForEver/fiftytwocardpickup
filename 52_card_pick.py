import tkinter as tk
from tkinter import messagebox
import random
import math
import time
import logging
from PIL import Image, ImageDraw, ImageTk, ImageColor, ImageFont


logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

card_width, card_height = 70, 98
background = '#1b5e20'
class CardRenderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        try:
            self.font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 24)
            self.symbol_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 36)
        except IOError:
            self.font = ImageFont.load_default()
            self.symbol_font = ImageFont.load_default()

    def render(self, card):
        fill = '#FFF6F3' if card.face_up else '#2196F3'
        outline = '#107d32'
        
        image = Image.new('RGBA', (self.width, self.height), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        rgba_fill = ImageColor.getrgb(fill)
        rgba_fill = (rgba_fill[0], rgba_fill[1], rgba_fill[2], 255)
        draw.rectangle([0, 0, self.width - 1, self.height - 1], fill=rgba_fill, outline=outline, width=2)
        
        if card.face_up:
            suit_color = card.suit_color
            draw.text((self.width // 2, self.height // 2 - 12), card.rank_str, fill=suit_color, anchor="mm", font=self.font)
            draw.text((self.width // 2, self.height // 2 + 24), card.suit_char, fill=suit_color, anchor="mm", font=self.symbol_font)
            
        rotated_image = image.rotate(math.degrees(-card.rotation), expand=True, fillcolor=(0, 0, 0, 0))
        return ImageTk.PhotoImage(rotated_image)

class Card:

    def __init__(self, rank, suit):
        self.value = rank
        self.suit = suit
        self.face_up = True
        self.rotation = random.uniform(0, math.pi)
        self.x = 0
        self.y = 0
        self.photo = None
        self.canvas_id = None
        
        # Pre-compute rank and suit info
        
        if rank == 1:
            self.rank_str = 'A'
        elif rank == 11:
            self.rank_str = 'J'
        elif rank == 12:
            self.rank_str = 'Q'
        elif rank == 13:
            self.rank_str = 'K'
        else:
            self.rank_str = str(rank)
        
        self.suit_char = {'H': '♥', 'D': '♦', 'C': '♣', 'S': '♠'}[suit]
        # Set text color based on suit (red for hearts/diamonds, black for clubs/spades)
        if suit in ['H', 'D']:
            self.suit_color = 'red'
        else:
            self.suit_color = 'black'

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("52 Card Pick")
        self.root.configure(bg='#3d7c42')
        self.root.geometry("1024x768")
        
        margin_left = 15
        margin_top = 15
        self.max_x = 1009
        self.max_y = 753
        
        self.canvas = tk.Canvas(self.root, width=self.max_x, height=self.max_y, bg=background)
        self.canvas.pack(padx=margin_left, pady=margin_top)
        
        self.table_cards = []
        self.deck_pile = []
        self.score = 0
        self.time = 0
        self.last_time = time.time()
        self.status_var = tk.StringVar(value="Score: 0  Time: 0")
        self.card_map = {}
        
        self.margin_left = margin_left
        self.margin_top = margin_top
        self.renderer = CardRenderer(card_width, card_height)
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_separator()
        file_menu.add_command(label="Score", command=self.show_score)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.root.quit)
        
        self.new_game()
        self.update_timer()
        self.canvas.bind('<Button-1>', self.on_canvas_click)
    def update_status(self):
        self.canvas.itemconfig(self.status_id, text=self.status_var.get())
    def new_game(self):
        logger.info("=== Starting new game ===")
        self.score = 0
        self.table_cards = []
        self.deck_pile = []
        self.card_map = {}
        self.canvas.delete("all")
        
        self.status_id = self.canvas.create_text(10, self.max_y - 30, anchor="sw", text="", font=("Arial", 14, "bold"), fill="white")
        self.update_status()
        decks_suits = ['H', 'D', 'C', 'S']
        for suit in decks_suits:
            for rank_val in range(1, 14):
                card = Card(rank_val, suit)
                self.table_cards.append(card)
        for card in self.table_cards:
            rand_x = random.randint(self.margin_left, self.max_x - card_width)
            rand_y = random.randint(self.margin_top, self.max_y - card_height)
            card.x = rand_x
            card.y = rand_y
            
            card.photo = self.renderer.render(card)
            card.canvas_id = self.canvas.create_image(card.x, card.y, image=card.photo, anchor="center", tags="card")
            self.card_map[card.canvas_id] = card
    def update_timer(self):
        self.time = int(time.time() - self.last_time)
        self.status_var.set(f"Score: {self.score}  Time: {self.time}")
        self.update_status()
        self.root.after(1000, self.update_timer)
    def on_canvas_click(self, event):
        item = self.canvas.find_withtag("current")
        if item:
            canvas_id = item[0]
            if canvas_id in self.card_map:
                card = self.card_map[canvas_id]
                if card.face_up:
                    # Geometric hit detection for rotated cards
                    dx = event.x - card.x
                    dy = event.y - card.y
                    cos_r = math.cos(card.rotation)
                    sin_r = math.sin(card.rotation)
                    rx = dx * cos_r - dy * sin_r
                    ry = dx * sin_r + dy * cos_r
                    
                    if abs(rx) <= card_width / 2 and abs(ry) <= card_height / 2:
                        self.collect_card(card)
    def collect_card(self, card):
        logger.info(f"=== COLLECTING CARD {card.value} ===")
        self.score += 10
        card.face_up = False
        card.rotation = 0
        self.table_cards.remove(card)
        self.deck_pile.append(card)
        
        if len(self.deck_pile) > 6:
            new_x, new_y = 50, 60
        elif len(self.deck_pile) > 1:
            last_card = self.deck_pile[-2]
            new_x, new_y = last_card.x + 2, last_card.y + 2
        else:
            new_x, new_y = 50, 60
        
        card.x, card.y = new_x, new_y
        self.redraw_card(card)
        
        if len(self.deck_pile) >= 52:
            self.show_win_screen()
    def redraw_card(self, card):
        card.photo = self.renderer.render(card)
        self.canvas.itemconfig(card.canvas_id, image=card.photo)
        self.canvas.coords(card.canvas_id, card.x, card.y)
    def show_score(self):
        messagebox.showinfo("Score", f"Current Score: {self.score}")
    def show_win_screen(self):
        win_window = tk.Toplevel(self.root)
        win_window.title("You Win!!!")
        win_window.geometry("300x200")
        win_window.configure(bg='#4caf50')
        win_window.transient(self.root)
        x = (win_window.winfo_screenwidth() // 2) - 150
        y = (win_window.winfo_screenheight() // 2) - 100
        win_window.geometry("+{}+{}".format(x, y))
        
        tk.Label(win_window, text="You Win!!!", font=('Arial', 24, 'bold'), bg='#4caf50', fg='white').pack(pady=20)
        tk.Label(win_window, text=f"Final Score: {self.score}", font=('Arial', 16), bg='#4caf50', fg='white').pack()
        
        def play_again():
            win_window.destroy()
            self.new_game()
            
        tk.Button(win_window, text="Play Again", font=('Arial', 14), command=play_again, bg='#2e7d32', fg='white', padx=30, pady=10).pack(pady=20)
        win_window.grab_set()
if __name__ == "__main__":
    game_instance = Game()
    game_instance.root.protocol("WM_DELETE_WINDOW", game_instance.root.destroy)
    game_instance.root.mainloop()
