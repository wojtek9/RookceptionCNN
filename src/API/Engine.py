from stockfish import Stockfish

from src.misc import utils

STOCKFISH_PATH = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\stockfish\stockfish-windows-x86-64-avx2.exe"

class Engine:
    """Handles interaction with the Stockfish engine."""

    def __init__(self):
        """Initialize Stockfish engine."""
        self.stockfish = self.start_stockfish()
        self.game_fen = None

    @staticmethod
    def start_stockfish():
        """Starts a new Stockfish process."""
        try:
            return Stockfish(STOCKFISH_PATH)
        except Exception as e:
            print(f"[ERROR] Failed to start Stockfish: {e}")
            return None

    def get_next_move(self, board_state, turn):
        """Returns the best move from Stockfish given a board state and updates game state."""
        if not self.is_alive():
            self.restart_stockfish()

        # Update game state before getting the best move
        self.update_game_state(board_state, turn)
        best_move = self.stockfish.get_best_move()

        # Apply the move and update the FEN
        self.stockfish.make_moves_from_current_position([best_move])
        self.game_fen = self.stockfish.get_fen_position()

        return best_move

    def is_alive(self):
        """Checks if Stockfish is still responsive."""
        if self.stockfish is None:
            return False

        try:
            # Try getting a move to see if Stockfish is still alive
            self.stockfish.get_best_move()
            return True  # Stockfish is alive
        except Exception:
            return False  # Stockfish has crashed

    def restart_stockfish(self):
        """Restarts Stockfish if it crashes."""
        print("[ERROR] -- Stockfish crashed. Restarting...")
        self.stockfish = self.start_stockfish()

    def get_game_state(self):
        """Returns the current game state including castling rights and en passant target."""
        if self.game_fen is None:
            return None

        fen_parts = self.game_fen.split(" ")
        return {
            "fen": self.game_fen,
            "castling_rights": fen_parts[2],  # Castling rights (KQkq or -)
            "en_passant": fen_parts[3]  # En passant target square (e.g., "e3" or "-")
        }

    def update_game_state(self, board_state, turn):
        """Updates game state by setting the FEN based on the board state, including castling rights and en passant."""

        # If it's the first move, assume all castling rights are available
        if self.game_fen is None:
            castling_rights = "KQkq"
            en_passant = "-"
            halfmove = "0"
            fullmove = "1"
        else:
            # Extract previous castling rights & en passant info from FEN
            fen_parts = self.game_fen.split(" ")
            castling_rights = fen_parts[2] if len(fen_parts) > 2 else "-"
            en_passant = fen_parts[3] if len(fen_parts) > 3 else "-"
            halfmove = fen_parts[4] if len(fen_parts) > 4 else "0"
            fullmove = fen_parts[5] if len(fen_parts) > 5 else "1"

        # Generate updated FEN
        self.game_fen = utils.board_to_fen(
            board_state=board_state,
            turn=turn,
            castling_rights=castling_rights,
            en_passant=en_passant,
            halfmove=halfmove,
            fullmove=fullmove
        )

        # Set the updated FEN position in Stockfish
        self.stockfish.set_fen_position(self.game_fen)