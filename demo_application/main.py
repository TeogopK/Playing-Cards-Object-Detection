import streamlit as st
import cv2
from utils.game_logic import Game, GameMode
from utils.card_game_detector import CardGameDetector
from utils.constants import MODEL_PATH, CLASS_NAMES

detector = CardGameDetector(MODEL_PATH, CLASS_NAMES)

# Initialize session state variables
if "game" not in st.session_state:
    st.session_state.game = Game()
if "cards_team_a" not in st.session_state:
    st.session_state.cards_team_a = []
if "cards_team_b" not in st.session_state:
    st.session_state.cards_team_b = []
if "team_a_last10" not in st.session_state:
    st.session_state.team_a_last10 = False  # Initialize with a default value (False)

# Streamlit setup
st.set_page_config(page_title="Card Game Tracker", layout="wide")
st.title("Card Game Tracker")

col1, spacer, col2 = st.columns([1, 0.2, 2])

with col1:
    st.subheader("Team Scores")
    team_a_scores = st.session_state.game.get_team_belotscore_history(0)
    team_b_scores = st.session_state.game.get_team_belotscore_history(1)

    table_data = []
    for i, (team_a, team_b) in enumerate(zip(team_a_scores, team_b_scores), 1):
        table_data.append({"Team A": team_a, "Team B": team_b})

    st.table(table_data)

with col2:
    st.subheader("Stats Actions")

    st.write(
        f"Cards for Team A - {st.session_state.game.get_points(st.session_state.cards_team_a, st.session_state.team_a_last10)} points:"
    )
    st.write(", ".join(str(card) for card in st.session_state.cards_team_a) if st.session_state.cards_team_a else "")
    st.write(
        f"Cards for Team B - {st.session_state.game.get_points(st.session_state.cards_team_b, not st.session_state.team_a_last10)} points:"
    )
    st.write(", ".join(str(card) for card in st.session_state.cards_team_b) if st.session_state.cards_team_b else "")

    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        if st.button("Take Snapshot"):
            st.write("Capturing cards... Please wait.")
            cap = cv2.VideoCapture(0)
            cap.set(3, 640)
            cap.set(4, 480)

            frame_placeholder = st.empty()
            detected_classes = []
            for i in range(10):
                ret, frame = cap.read()
                if ret:
                    frame_placeholder.image(frame, channels="BGR")
                    detected_classes.extend(detector.capture_a_frame(cap))
            cap.release()
            frame_placeholder.empty()
            detections = detector.aggregate_detections(detected_classes)
            detected_cards = st.session_state.game.sort_cards(detector.parse_cards(detections))

            if detected_cards:
                st.success("Cards detected successfully!")
                st.session_state.cards_team_a = detected_cards
                print("DETECTED CARDS", detected_cards)
                st.session_state.cards_team_b = st.session_state.game.get_other_cards(detected_cards)
            else:
                st.error("No valid cards detected. Please try again.")
            st.rerun()

    with sub_col2:
        if st.button("Flip cards"):
            st.session_state.cards_team_a, st.session_state.cards_team_b = (
                st.session_state.cards_team_b,
                st.session_state.cards_team_a,
            )
            st.rerun()

    st.markdown("---")

    st.subheader("Scoring Options")

    if "current_game_mode" not in st.session_state:
        st.session_state.current_game_mode = "All Trumps"

    mode_choice = st.selectbox("Select Game Mode", ["All Trumps", "No Trumps", "Spades", "Hearts", "Diamonds", "Clubs"])
    game_mode_map = {
        "All Trumps": GameMode.ALL_TRUMPS,
        "No Trumps": GameMode.NO_TRUMPS,
        "Spades": GameMode.SPADES,
        "Hearts": GameMode.HEARTS,
        "Diamonds": GameMode.DIAMONDS,
        "Clubs": GameMode.CLUBS,
    }

    if mode_choice != st.session_state.current_game_mode:
        st.session_state.game.change_gamemode(game_mode_map[mode_choice])
        st.session_state.current_game_mode = mode_choice

        st.session_state.cards_team_a = st.session_state.game.sort_cards(st.session_state.cards_team_a)
        st.session_state.cards_team_b = st.session_state.game.sort_cards(st.session_state.cards_team_b)
        st.rerun()

    team_a_bonus = st.number_input("Bonus Points (Team A)", min_value=0, step=1, key="bonus_a")
    team_b_bonus = st.number_input("Bonus Points (Team B)", min_value=0, step=1, key="bonus_b")
    bool_10 = st.checkbox("Team A won last 10?", value=st.session_state.team_a_last10)

    if bool_10 != st.session_state.team_a_last10:
        st.session_state.team_a_last10 = bool_10
        st.rerun()

    if st.button("Update Scores"):
        st.session_state.game.add_current_round_points(
            taken_cards=st.session_state.cards_team_a,
            team_index=0,
            has_taken_last=st.session_state.team_a_last10,
            bonuses_points=team_a_bonus,
            enemy_bonuses_points=team_b_bonus,
        )
        st.success("Scores updated successfully!")
        st.rerun()
