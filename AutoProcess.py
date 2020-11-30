import random as rand
from Board import Board


class AutoProcess():
    def Do(self,board,Turn):
        tmp_piece = []
        for piece in board.piece:
            if piece.getTurn() == Turn:
                tmp_piece.append(piece)

        while 1:
            choi =  rand.choice(tmp_piece)
            fromPos = choi.getPos()
            possible_move = board.Possible(fromPos)
            if not possible_move:
                continue
            else:
                toPos = rand.choice(possible_move)
                break



        promote = False




        return fromPos,toPos,promote
