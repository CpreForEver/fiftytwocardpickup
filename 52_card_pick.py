import tkinter as tk
from tkinter import messagebox
import random
import time
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Card:
    def __init__(self, rank, suit):
        self.value = rank
        self.suit = suit
        self.face_up = True
        self.rotation = 0
        
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

class CardWidget:
    def __init__(self, parent, card):
        self.parent = parent
        self.card = card
        self.widget = None
        
    def create_widget(self):
        rank_str = self.card.rank_str
        suit_char = self.card.suit_char
        
        canvas = tk.Canvas(self.parent, width=70, height=98)
        
        # Draw face-up card with rotation (centered) - each rotation shows different face
        if self.card.face_up:
            # Calculate centered positions for 70x98 card
            cx = 35  # center x (width/2)
            cy = 49  # center y (height/2)
            
            # Each rotation shows a unique representation
            if self.card.rotation == 1:
                canvas.create_text(cx, cy - 10, text=f"{rank_str}", 
                                  font=('Arial', 18, 'bold'), anchor='center', fill=self.card.suit_color)
            elif self.card.rotation == 2:
                canvas.create_text(cx, cy + 15, text=suit_char, 
                                  font=('Arial', 32), anchor='center', fill=self.card.suit_color)
            elif self.card.rotation == 3:
                canvas.create_text(cx, cy - 10, text=f"{rank_str} {suit_char}", 
                                  font=('Arial', 18), anchor='center', fill=self.card.suit_color)
            else:
                canvas.create_text(cx, cy, text=f"{rank_str}\n{suit_char}", 
                                  font=('Arial', 16, 'bold'), fill=self.card.suit_color)
            
            canvas.config(bg='#FFF8F0')
        else:
            # Face down card - blue back with no text
            canvas.create_rectangle(0, 0, 70, 98, fill='#2196F3')
        
        self.widget = canvas
        self.bind_click()
    
    def draw(self, x=None, y=None, rotation=0):
        """Draw card at specified coordinates with rotation"""
        if x is not None and y is not None:
            self.card.x = x
            self.card.y = y
        
        # Redraw the widget with updated position and appearance
        if self.widget:
            self.widget.destroy()
            self.create_widget()
            self.widget.place(x=self.card.x, y=self.card.y)
    
    def bind_click(self):
        """Bind click handler directly to this widget"""
        self.widget.bind('<Button-1>', lambda e: self.on_click(e))
    
    def on_click(self, event):
        """Handle card click - move to deck pile if face up."""
        if not self.card.face_up:
            return  # Only collect face-up cards
        
        logger.info(f"=== CARD CLICKED ===")
        logger.info(f"Card {self.card.value}: pos=({self.card.x},{self.card.y})")
        
        # Move card to deck pile and create new face-down widget at stack position
        game_instance.table_cards.remove(self.card)
        game_instance.deck_pile.append(self.card)
        game_instance.score += 10
        
        self.card.face_up = False
        
        # Single pile at top-left on deck container, max 5 cards high, then reset to starting position
        if len(game_instance.deck_pile) > 6:  # More than 5 cards in pile
            new_x = 25
            new_y = 60
        elif len(game_instance.deck_pile) > 1:
            last_card_idx = len(game_instance.deck_pile) - 2
            offset_x = 1  # 1 pixel horizontal offset
            offset_y = 1  # 1 pixel vertical offset
            
            new_x = game_instance.deck_pile[last_card_idx].x + offset_x
            new_y = game_instance.deck_pile[last_card_idx].y + offset_y
        else:
            new_x = 25
            new_y = 60
        
        self.card.x = new_x
        self.card.y = new_y
        
        # Update widget position and appearance to face-down
        self.widget.create_rectangle(0, 0, 70, 98, fill='#2196F3')
        self.widget.place(x=new_x, y=new_y)
        
        logger.info(f"Card {self.card.value} stacked at ({new_x},{new_y})")
        logger.info(f"Score: {game_instance.score}, Deck size: {len(game_instance.deck_pile)}")
        
        # Check if game won (all 52 cards collected)
        if len(game_instance.deck_pile) >= 52:
            self.show_win_screen()

    def show_win_screen(self):
        """Show win splash screen with play again button."""
        # Create centered window using game_instance.root
        win_window = tk.Toplevel(game_instance.root)
        win_window.title("You Win!!!")
        
        # Set size and appearance first
        win_window.geometry("300x200")
        win_window.configure(bg='#4caf50')
        win_window.transient(game_instance.root)
        
        # Center on screen
        x = (win_window.winfo_screenwidth() // 2) - 150
        y = (win_window.winfo_screenheight() // 2) - 100
        win_window.geometry("+{}+{}".format(x, y))
        
        # Create widgets before setting grab
        title_label = tk.Label(win_window, text="You Win!!!", 
                              font=('Arial', 24, 'bold'), bg='#4caf50', fg='white')
        title_label.pack(pady=20)
        
        score_label = tk.Label(win_window, text=f"Final Score: {game_instance.score}", 
                              font=('Arial', 16), bg='#4caf50', fg='white')
        score_label.pack()
        
        def play_again():
            game_instance.new_game()
            win_window.destroy()
        
        btn = tk.Button(win_window, text="Play Again", font=('Arial', 14), 
                        command=play_again, bg='#2e7d32', fg='white', 
                        activebackground='#1b5e20', activeforeground='white',
                        padx=30, pady=10)
        btn.pack(pady=20)
        
        # Ensure window is ready before grabbing
        win_window.update_idletasks()
        win_window.lift()
        win_window.grab_set()
        
        btn = tk.Button(win_window, text="Play Again", font=('Arial', 14), 
                        command=play_again, bg='#2e7d32', fg='white', 
                        activebackground='#1b5e20', activeforeground='white',
                        padx=30, pady=10)
        btn.pack(pady=20)

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("52 Card Pick")
        self.root.configure(bg='#3d7c42')
        
        # Set fixed window size: 1024x768 workspace
        self.root.geometry("1024x768")
        
        # Create main canvas with margin
        margin_left = 15
        margin_top = 15
        max_x = 1009
        max_y = 753
        
        self.canvas = tk.Canvas(self.root, width=max_x, height=max_y, bg='#1b5e20')
        self.canvas.pack(padx=margin_left, pady=margin_top)
        
        # Game state
        self.table_cards = []
        self.deck_pile = []
        self.score = 0
        self.time = 0
        self.last_time = time.time()
        self.status_var = tk.StringVar(value="Score: 0  Time: 0")
        
        # Canvas dimensions (for new_game)
        self.margin_left = margin_left
        self.margin_top = margin_top
        self.max_x = max_x
        self.max_y = max_y
        
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_separator()
        file_menu.add_command(label="Score", command=self.show_score)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.root.quit)
        
        # Start game
        self.new_game()
        self.update_timer()

    def new_game(self):
        """Initialize a new game with randomly placed cards."""
        logger.info("=== Starting new game ===")
        self.score = 0
        self.table_cards = []
        self.deck_pile = []
        
        # Clear existing widgets
        for widget in self.canvas.winfo_children():
            widget.destroy()
        
      # Create deck pile container at top-left (15,15)
        self.deck_container = tk.Frame(self.canvas, bg='#2e7d32', width=100, height=180)
        self.deck_container.place(x=15, y=15)

        # Generate 52 unique cards (Ace-King × 4 suits) and place them randomly
        decks_suits = ['H', 'D', 'C', 'S']
        
        for suit in decks_suits:
            ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
            for rank_val in ranks:
                self.table_cards.append(Card(rank_val, suit))
        
        
        # Now place each card at random position
        for card in self.table_cards:
            rand_x = random.randint(self.margin_left, self.max_x - 70)
            rand_y = random.randint(self.margin_top, self.max_y - 98)
            
            # Random orientation: 0=normal, 1=rotated 90°, 2=flipped 180°, 3=rotated 270°
            orientation = random.randint(0, 3)
            
            widget = CardWidget(self.canvas, card)
            widget.widget_id = id(widget)
            widget.create_widget()
            widget.draw(x=rand_x, y=rand_y, rotation=orientation)
            card.x = rand_x
            card.y = rand_y
            card.rotation = orientation
            
            logger.info(f"Card {card.value} initial pos: ({rand_x},{rand_y}) face_up={card.face_up} rot={orientation}")
        
 
    def update_timer(self):
        """Update timer every second."""
        self.time = int(time.time()) - self.last_time
        self.status_var.set(f"Score: {self.score}  Time: {self.time}")
        
        self.root.after(1000, self.update_timer)

    def show_score(self):
        """Show current score in dialog."""
        messagebox.showinfo("Score", f"Current Score: {self.score}")

if __name__ == "__main__":
    game_instance = None
    
    def log_click(event):
        """Log all clicks for debugging."""
        logger.info(f"=== CANVAS CLICKED AT ({event.x},{event.y}) ===")
    
    def log_card_state(card, index):
        """Log card state at specific position."""
        logger.info(f"Card {card.value} at index {index}: face_up={card.face_up}, pos=({card.x},{card.y}), rot={card.rotation}")

    game_instance = Game()
    game_instance.root.protocol("WM_DELETE_WINDOW", lambda: exit(0))
    game_instance.root.mainloop()
