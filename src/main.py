
if __name__ == "__main__":
    from stockfish import Stockfish

    STOCKFISH_PATH = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\stockfish\stockfish-windows-x86-64-avx2.exe"
    stockfish = Stockfish(STOCKFISH_PATH)

    stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    print(stockfish.get_best_move())
