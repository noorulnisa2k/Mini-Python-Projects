import tkinter as tk
from tkinter import messagebox
import random


from PIL import Image, ImageTk
import os


# Player starts with $1000
player_balance = 1000


player_card_labels = []


# Function to deal a card
def dealCard(hand, deck):
    card = random.choice(deck)
    hand.append(card)
    deck.remove(card)


# Function to calculate the total value of a hand
def total(hand):
    total_value = 0
    face_cards = ['J', 'Q', 'K']
    ace_count = 0
    for card in hand:
        if isinstance(card, int):
            total_value += card
        elif card in face_cards:
            total_value += 10
        else:  # Ace case
            ace_count += 1
            total_value += 11


    # Adjust for aces if the total goes over 21
    while total_value > 21 and ace_count > 0:
        total_value -= 10
        ace_count -= 1


    return total_value


# Initialize game variables
playerHand = []
dealerHand = []
deck = []
bet = 0
player_card_labels = []


def resetDeck():
    global deck
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4


# Function to start the game
def startGame():
    global playerHand, dealerHand, bet, deck
    resetDeck()
    playerHand.clear()
    dealerHand.clear()


    # Get the player's bet
    try:
        bet = int(bet_entry.get())
        if bet > player_balance:
            messagebox.showerror("Error", "You don't have enough balance!")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid bet.")
        return


    # Deal cards
    dealCard(playerHand, deck)
    dealCard(dealerHand, deck)
    dealCard(playerHand, deck)
    dealCard(dealerHand, deck)


    updateUI()


    # Enable "Hit" and "Stand" buttons
    hit_button.config(state=tk.NORMAL)
    stand_button.config(state=tk.NORMAL)


# Update the GUI elements to display the hands and totals
def updateUI():
    player_total = total(playerHand)
    dealer_total = total(dealerHand)
   
    player_hand_str.set(f"Player Hand: {playerHand} | Total: {player_total}")
    dealer_hand_str.set(f"Dealer Hand: {dealerHand[0]} and ?")  # Show only one dealer card


    # Update balance
    balance_var.set(f"Current Balance: ${player_balance}")


    # Clear previous card images
    for cardImage in player_card_labels:
        cardImage.destroy()
    player_card_labels.clear()


    # Load and display images for each card in the player's hand
    for card in playerHand:
        # Build image filename
        cardSymbol = str(card)


        suit = random.choice(['H', 'D', 'C', 'S'])
        img_path = f"./Images/{cardSymbol}{suit}.png"
        if os.path.isfile(img_path):
            img = Image.open(img_path)
            img = img.resize((100, 150), Image.LANCZOS)  # Resize as needed
            card_image = ImageTk.PhotoImage(img)
            cardImage = tk.Label(root, image=card_image)
            cardImage.image = card_image  # Keep a reference to avoid garbage collection
            cardImage.pack()
            player_card_labels.append(cardImage)


def updateUI(showDealerCards=False):
    player_total = total(playerHand)
   
    # Clear previous card images for player and dealer
    for cardImage in player_card_labels:
        cardImage.destroy()
    player_card_labels.clear()


    # Dealer hand update
    if showDealerCards:
        dealer_total = total(dealerHand)
        dealer_hand_str.set(f"Dealer Hand: {dealerHand} | Total: {dealer_total}")
    else:
        dealer_hand_str.set(f"Dealer Hand: {dealerHand[0]} and [ ? ]")
   
    dealer_hand_label.config(textvariable=dealer_hand_str)


    # Display the first dealer card
    dealer_card_image = dealerHand[0]
    suit = random.choice(['H', 'D', 'C', 'S'])
    img_path = f"./Images/{dealer_card_image}{suit}.png"
    if os.path.isfile(img_path):
        img = Image.open(img_path)
        img = img.resize((100, 150), Image.LANCZOS)
        card_image = ImageTk.PhotoImage(img)
        dealer_card_label = tk.Label(root, image=card_image)
        dealer_card_label.image = card_image
        dealer_card_label.pack()
        player_card_labels.append(dealer_card_label)


    # Display the '?' or actual dealer cards if revealed
    if showDealerCards:
        for card in dealerHand[1:]:
            cardSymbol = str(card)
            suit = random.choice(['H', 'D', 'C', 'S'])
            img_path = f"./Images/{cardSymbol}{suit}.png"
            if os.path.isfile(img_path):
                img = Image.open(img_path)
                img = img.resize((100, 150), Image.LANCZOS)
                card_image = ImageTk.PhotoImage(img)
                cardImage = tk.Label(root, image=card_image)
                cardImage.image = card_image
                cardImage.pack()
                player_card_labels.append(cardImage)
    else:
        mystery_card_label = tk.Label(root, text="?", font=("Arial", 72), width=4, height=2, borderwidth=2, relief="solid")
        mystery_card_label.pack()
        player_card_labels.append(mystery_card_label)


    # Player hand update
    player_hand_str.set(f"Player Hand: {playerHand} | Total: {player_total}")
    player_hand_label.config(textvariable=player_hand_str)


    # Load and display images for each card in the player's hand
    for card in playerHand:
        cardSymbol = str(card)
        suit = random.choice(['H', 'D', 'C', 'S'])
        img_path = f"./Images/{cardSymbol}{suit}.png"
        if os.path.isfile(img_path):
            img = Image.open(img_path)
            img = img.resize((100, 150), Image.LANCZOS)
            card_image = ImageTk.PhotoImage(img)
            cardImage = tk.Label(root, image=card_image)
            cardImage.image = card_image
            cardImage.pack()
            player_card_labels.append(cardImage)


    # Update balance
    balance_var.set(f"Current Balance: ${player_balance}")




# Function for when the player chooses to "Hit"
def hit():
    global playerHand, deck
    dealCard(playerHand, deck)
    updateUI()
   
    if total(playerHand) > 21:
        messagebox.showinfo("Game Over", "You busted! Dealer wins.")
        endGame()


# Function for when the player chooses to "Stand"
def stand():
    global dealerHand, playerHand, bet, player_balance
    dealer_total = total(dealerHand)


    # Dealer must hit until they reach 17 or higher
    while dealer_total < 17:
        dealCard(dealerHand, deck)
        dealer_total = total(dealerHand)


    updateUI()
    player_total = total(playerHand)
    dealer_total = total(dealerHand)


    # Determine the result of the game
    if dealer_total > 21:
        messagebox.showinfo("Congratulations", "Dealer busted! You win.")
        player_balance += bet
    elif player_total > dealer_total:
        messagebox.showinfo("Congratulations", "You win!")
        player_balance += bet
    elif player_total == dealer_total:
        messagebox.showinfo("Stand-off", "It's a tie!")
    else:
        messagebox.showinfo("Game Over", "Dealer wins.")
        player_balance -= bet


    endGame()


# Function to end the game and disable "Hit" and "Stand"
def endGame():
    hit_button.config(state=tk.DISABLED)
    stand_button.config(state=tk.DISABLED)


    # Update final hands
    dealer_hand_str.set(f"Dealer Hand: {dealerHand} | Total: {total(dealerHand)}")
    player_hand_str.set(f"Player Hand: {playerHand} | Total: {total(playerHand)}")


    # Update balance
    balance_var.set(f"Current Balance: ${player_balance}")


    if player_balance <= 0:
        messagebox.showwarning("Bankrupt", "You're out of money! Game over.")


# Function to reset the game
def reset_game():
    global player_balance
    player_balance = 1000
    balance_var.set(f"Current Balance: ${player_balance}")
    player_hand_str.set("Player Hand: ")
    dealer_hand_str.set("Dealer Hand: ")
    bet_entry.delete(0, tk.END)


# Function to display Blackjack rules
def display_rules():
    rules = """
    Rules of Blackjack:
    1. The goal is to beat the dealer by having a hand total closer to 21 without going over.
    2. Number cards (2-10) are worth their face value.
    3. Face cards (J, Q, K) are worth 10.
    4. Aces can be worth either 1 or 11.
    5. Both you and the dealer are dealt two cards. You can see one of the dealer's cards.
    6. You can choose to "hit" (take another card) or "stand" (keep your current hand).
    7. If you go over 21, you "bust" and lose the game.
    8. Dealer must hit until they reach 17 or higher.
    9. The player wins if their hand total is higher than the dealer's without busting.
    """
    messagebox.showinfo("Blackjack Rules", rules)


# GUI Setup
# root = tk.Tk()
# root.title("Blackjack Game")

# root.configure(bg="#9db094")

# # Variables
# balance_var = tk.StringVar(value=f"Current Balance: ${player_balance}")
# player_hand_str = tk.StringVar(value="Player Hand: ")
# dealer_hand_str = tk.StringVar(value="Dealer Hand: ")


# # Create a Menu bar
# menu_bar = tk.Menu(root)


# # Create "Game" menu
# game_menu = tk.Menu(menu_bar, tearoff=0)
# game_menu.add_command(label="Rules", command=display_rules)
# game_menu.add_command(label="Check Balance", command=lambda: messagebox.showinfo("Balance", f"Current Balance: ${player_balance}"))
# game_menu.add_command(label="Reset Game", command=reset_game)
# menu_bar.add_cascade(label="Game", menu=game_menu)


# # Add the Menu bar to the window
# root.config(menu=menu_bar)


# # GUI Components
# balance_label = tk.Label(root, textvariable=balance_var)
# balance_label.pack()


# bet_label = tk.Label(root, text="Enter your bet:")
# bet_label.pack()


# bet_entry = tk.Entry(root)
# bet_entry.pack()


# deal_button = tk.Button(root, text="Start Game", command=startGame)
# deal_button.pack()


# hit_button = tk.Button(root, text="Hit", state=tk.DISABLED, command=hit)
# hit_button.pack()


# stand_button = tk.Button(root, text="Stand", state=tk.DISABLED, command=stand)
# stand_button.pack()


# player_hand_label = tk.Label(root, textvariable=player_hand_str)
# player_hand_label.pack()


# dealer_hand_label = tk.Label(root, textvariable=dealer_hand_str)
# dealer_hand_label.pack()


# reset_button = tk.Button(root, text="Reset Game", command=reset_game)
# reset_button.pack()


# # Run the main loop
# root.mainloop()




# GUI Setup
root = tk.Tk()
root.title("Blackjack Game")
root.configure(bg="#f0f8ff")  # Background for the entire window

# Variables
balance_var = tk.StringVar(value=f"Current Balance: ${player_balance}")
player_hand_str = tk.StringVar(value="Player Hand: ")
dealer_hand_str = tk.StringVar(value="Dealer Hand: ")

# Create a Menu bar
menu_bar = tk.Menu(root, bg="#486b8a", fg="white", activebackground="white", activeforeground="#486b8a")
root.config(menu=menu_bar)

# Create "Game" menu
game_menu = tk.Menu(menu_bar, tearoff=0, bg="white", fg="#486b8a", activebackground="#486b8a", activeforeground="white")
game_menu.add_command(label="Rules", command=display_rules)
game_menu.add_command(label="Check Balance", command=lambda: messagebox.showinfo("Balance", f"Current Balance: ${player_balance}"))
game_menu.add_command(label="Reset Game", command=reset_game)
menu_bar.add_cascade(label="Game", menu=game_menu)

# Add the Menu bar to the window
root.config(menu=menu_bar)

# GUI Components
balance_label = tk.Label(root, textvariable=balance_var, bg="#f0f8ff", fg="#000080", font=("Arial", 14))
balance_label.pack(pady=10)

bet_label = tk.Label(root, text="Enter your bet:", bg="#f0f8ff", fg="#000080", font=("Arial", 12))
bet_label.pack()

bet_entry = tk.Entry(root, bg="white", fg="black", font=("Arial", 12))
bet_entry.pack()

deal_button = tk.Button(root, text="Start Game", command=startGame, bg="white", fg="#1b5701", activebackground="#1b5701", activeforeground="white")
deal_button.pack(pady=5)

hit_button = tk.Button(root, text="Hit", state=tk.DISABLED, command=hit, bg="#486b8a", fg="white", activebackground="white", activeforeground="#486b8a")
hit_button.pack(pady=5)

stand_button = tk.Button(root, text="Stand", state=tk.DISABLED, command=stand, bg="#486b8a", fg="white", activebackground="white", activeforeground="#486b8a")
stand_button.pack(pady=5)

player_hand_label = tk.Label(root, textvariable=player_hand_str, bg="#f0f8ff", fg="darkblue", font=("Arial", 12))
player_hand_label.pack(pady=5)

dealer_hand_label = tk.Label(root, textvariable=dealer_hand_str, bg="#f0f8ff", fg="darkred", font=("Arial", 12))
dealer_hand_label.pack(pady=5)

reset_button = tk.Button(root, text="Reset Game", command=reset_game, bg="#e3a302", fg="white", activebackground="white", activeforeground="#e3a302")
reset_button.pack(pady=10)

# Run the main loop
root.mainloop()
