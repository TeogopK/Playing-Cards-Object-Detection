import cv2
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
    print("\nMenu:")
    print("1. Set Game Mode")
    print("2. Capture Cards")
    print("3. Show Score")
    print("4. Quit")


while True:
    print_menu()
    choice = input("Choose an option: ")

    if choice == "1":
        print("Game Modes: 1. All Trumps, 2. No Trumps, 3. Spades, 4. Hearts, 5. Diamonds, 6. Clubs")
        mode_choice = input("Choose a mode: ")
        game_mode_map = {
            "1": GameMode.ALL_TRUMPS,
            "2": GameMode.NO_TRUMPS,
            "3": GameMode.SPADES,
            "4": GameMode.HEARTS,
            "5": GameMode.DIAMONDS,
            "6": GameMode.CLUBS,
        }
        game.change_gamemode(game_mode_map.get(mode_choice, GameMode.NO_TRUMPS))
        print(f"Game mode set to {game.game_mode.name}.")
    elif choice == "2":
        print("Capturing cards...")
        detected_classes = detector.capture_and_process_frames(cap)
        detected_cards = detector.parse_cards(detected_classes)
        print(f"Detected Cards: {detected_cards}")
        game.add_current_round_scores(detected_cards)
    elif choice == "3":
        print(f"Current Score: {game.get_team_score()}")
    elif choice == "4":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")

cap.release()
cv2.destroyAllWindows()
