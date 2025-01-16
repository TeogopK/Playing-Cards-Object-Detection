import cv2
import time
from utils.game_logic import Game, GameMode
from utils.card_game_detector import CardGameDetector

# Configuration
MODEL_PATH = "../final_models/yolov8m_synthetic.pt"
CLASS_NAMES = [
    "10c",
    "10d",
    "10h",
    "10s",
    "2c",
    "2d",
    "2h",
    "2s",
    "3c",
    "3d",
    "3h",
    "3s",
    "4c",
    "4d",
    "4h",
    "4s",
    "5c",
    "5d",
    "5h",
    "5s",
    "6c",
    "6d",
    "6h",
    "6s",
    "7c",
    "7d",
    "7h",
    "7s",
    "8c",
    "8d",
    "8h",
    "8s",
    "9c",
    "9d",
    "9h",
    "9s",
    "Ac",
    "Ad",
    "Ah",
    "As",
    "Jc",
    "Jd",
    "Jh",
    "Js",
    "Kc",
    "Kd",
    "Kh",
    "Ks",
    "Qc",
    "Qd",
    "Qh",
    "Qs",
]

# Initialize
detector = CardGameDetector(MODEL_PATH, CLASS_NAMES)
game = Game()

# Start Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


def print_menu():
    print("\n--- Card Game Menu ---")
    print("1. Set Game Mode")
    print("2. Capture and Add Cards")
    print("3. Sort and Display All Cards")
    print("4. Show Team Scores")
    print("5. Display Game Stats")
    print("6. Add Last Hand Score")
    print("7. Quit")
    print("----------------------")


def set_game_mode():
    print("\nAvailable Game Modes:")
    print("1. All Trumps")
    print("2. No Trumps")
    print("3. Spades")
    print("4. Hearts")
    print("5. Diamonds")
    print("6. Clubs")
    mode_choice = input("Choose a mode (1-6): ")

    game_mode_map = {
        "1": GameMode.ALL_TRUMPS,
        "2": GameMode.NO_TRUMPS,
        "3": GameMode.SPADES,
        "4": GameMode.HEARTS,
        "5": GameMode.DIAMONDS,
        "6": GameMode.CLUBS,
    }
    game_mode = game_mode_map.get(mode_choice, GameMode.NO_TRUMPS)
    game.change_gamemode(game_mode)
    print(f"Game mode set to {game_mode.name}.")


def capture_and_add_cards():
    print("Capturing cards... Please hold steady.")
    detected_classes = detector.capture_and_process_frames(cap)
    detected_cards = game.sort_cards(detector.parse_cards(detected_classes))

    if detected_cards:
        print(f"Detected Cards: {detected_cards}")
        confirm = input("Do you want to accept these detected cards? (y/n): ")
        if confirm.lower() == "y":
            game.add_current_round_points(detected_cards)
            print("Cards successfully added to the game.")
        else:
            print("Cards rejected. No changes made.")
    else:
        print("No valid cards detected. Try again.")


def add_last_hand_score():
    print("\n--- Last Hand Score ---")
    add_score = input("Do you want to add the score of the last hand to the total? (y/n): ")
    if add_score.lower() == "y":
        game.add_current_round_scores(game.team_scores[0].cards_for_all_rounds[-1])  # Using the last round's cards
        print("Last hand score successfully added.")
    else:
        print("Last hand score not added.")


def sort_and_display_cards():
    sorted_cards = game.sort_cards()
    print("\n--- Sorted Cards ---")
    for card in sorted_cards:
        print(card, end=" ")
    print("\n---------------------")


def display_team_scores():
    print("\n--- Team Scores ---")
    for i, team_score in enumerate(game.team_scores):
        print(f"Team {i + 1}: {team_score.total_points} points")
    print("--------------------")


def display_game_stats():
    print("\n--- Game Stats ---")
    print(f"Game Mode: {game.game_mode.name}")
    print(f"Maximum Possible Points: {game.get_max_points()} points")
    for i, team_score in enumerate(game.team_scores):
        print(f"Team {i + 1}: {team_score.total_belotscore} points")
        print(f"Cards for Team {i + 1}: {team_score.get_last_hand()}")
    print("-------------------")


# Main Menu Loop
while True:
    print_menu()
    choice = input("Choose an option: ")

    if choice == "1":
        set_game_mode()
    elif choice == "2":
        capture_and_add_cards()
    elif choice == "3":
        sort_and_display_cards()
    elif choice == "4":
        display_team_scores()
    elif choice == "5":
        display_game_stats()
    elif choice == "6":
        add_last_hand_score()
    elif choice == "7":
        print("Exiting the game. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

cap.release()
cv2.destroyAllWindows()
