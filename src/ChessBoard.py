import os

from PIL import ImageGrab, Image
import numpy as np
import string

from misc import utils


class ChessBoard:
    def __init__(self, board_region):
        self.board_region = board_region  # (left, top, right, bottom)
        self.squares = np.empty((8, 8), dtype=object)

    def capture_board(self):
        """Takes a screenshot of the chessboard."""
        screenshot = ImageGrab.grab(self.board_region)
        return screenshot

    @staticmethod
    def extract_squares(image_path, output_dir):
        """Extracts 64 squares from a 720x720 chessboard image and saves them."""
        os.makedirs(output_dir, exist_ok=True)

        image = Image.open(image_path)
        square_size = 720 // 8  # 90 pixels per square

        for row in range(8):
            for col in range(8):
                left = col * square_size
                top = row * square_size
                right = (col + 1) * square_size
                bottom = (row + 1) * square_size

                square_img = image.crop((left, top, right, bottom))

                # Save each square (row, col) with an indexed filename
                square_filename = f"{os.path.basename(image_path).split('.')[0]}_{row}{col}.png"
                square_img.save(os.path.join(output_dir, square_filename))

    @staticmethod
    def fen_to_board(fen):
        """Converts a FEN string into a dictionary of piece positions."""
        rows = fen.split()[0].split("/")  # Get only the board part of FEN
        board = {}

        ranks = list(range(8, 0, -1))  # Chess ranks (8 to 1)
        files = list(string.ascii_uppercase[:8])  # Chess files (A to H)

        for row_idx, row in enumerate(rows):
            file_idx = 0
            for char in row:
                if char.isdigit():
                    file_idx += int(char)  # Empty squares
                else:
                    square = f"{files[file_idx]}{ranks[row_idx]}"  # Example: "E4"
                    board[square] = char
                    file_idx += 1

        return board

    @staticmethod
    def fen_to_square_mapping(fen):
        """Converts a FEN string to an 8x8 array representing piece positions."""
        rows = fen.split()[0].split("/")  # Extract only piece placement
        board = []

        for row in rows:
            expanded_row = []
            for char in row:
                if char.isdigit():
                    expanded_row.extend(["empty"] * int(char))  # Empty squares
                else:
                    expanded_row.append(char)  # Chess piece
            board.append(expanded_row)

        return board

if __name__ == "__main__":
    fen_str = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
    board_scr = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\images\chessboard\board.png"
    output_dir = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\output"
    board_map = ChessBoard.fen_to_square_mapping(fen_str)
    ChessBoard.extract_squares(board_scr, output_dir)
    print(board_map)
