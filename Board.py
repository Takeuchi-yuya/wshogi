#import numpy as np
#import copy

from Piece import Piece,Type

#-------------------------------------------------------
class Board():
	def __init__(self):
		move_1 = [[0,1]]															#"歩"　１
		move_2 = [[0,10]]															#"香"　２
		move_3 = [[1,2],[-1,2]]														#"桂"　３
		move_4 = [[1,1],[0,1],[-1,1],[1,-1],[-1,-1]]								#"銀"　４
		move_5 = [[1,1],[0,1],[-1,1],[1,0],[-1,0],[0,-1]]							#"金"　５
		move_6 = [[0,10],[10,0],[-10,0],[0,-10]]									#"飛"　６
		move_7 = [[10,10],[-10,10],[10,-10],[-10,-10]]								#"角"　７
		move_8 = [[1,1],[0,1],[-1,1],[1,0],[-1,0],[1,-1],[0,-1],[-1,-1]]			#"王"　８
		move_16 =[[1,1],[0,10],[-1,1],[10,0],[-10,0],[1,-1],[0,-10],[-1,-1]]		#"竜"　16
		move_17 =[[10,10],[0,1],[-10,10],[1,0],[-1,0],[10,-10],[0,-1],[-10,-10]]	#"馬"　17
		self.move = [[],move_1,move_2,move_3,move_4,move_5,move_6 ,move_7 ,move_8,move_8,
					[], move_5,move_5,move_5,move_5,move_5,move_16,move_17,move_8,move_8]
		self.initBoard()

	def initBoard(self):
		self.piece = []
		turn = False

		y = 0
		self.makePiece(Type.lance,		0,y,	turn)
		self.makePiece(Type.knight,		1,y,	turn)
		self.makePiece(Type.silver,		2,y,	turn)
		self.makePiece(Type.gold,		3,y,	turn)
		self.makePiece(Type.king,		4,y,	turn)
		self.makePiece(Type.gold,		5,y,	turn)
		self.makePiece(Type.silver,		6,y,	turn)
		self.makePiece(Type.knight,		7,y,	turn)
		self.makePiece(Type.lance,		8,y,	turn)
		y = 1
		self.makePiece(Type.rook,		1,y,	turn)
		self.makePiece(Type.bishop,		7,y,	turn)
		y = 2
		for x in range(9):
			self.makePiece(Type.pawn,	x,y,	turn)

		turn = True
		y = 6
		for x in range(9):
			self.makePiece(Type.pawn,	x,y,	turn)
		y = 7
		self.makePiece(Type.rook,		7,y,	turn)
		self.makePiece(Type.bishop,		1,y,	turn)
		y = 8
		self.makePiece(Type.lance,		0,y,	turn)
		self.makePiece(Type.knight,		1,y,	turn)
		self.makePiece(Type.silver,		2,y,	turn)
		self.makePiece(Type.gold,		3,y,	turn)
		self.makePiece(Type.king,		4,y,	turn)
		self.makePiece(Type.gold,		5,y,	turn)
		self.makePiece(Type.silver,		6,y,	turn)
		self.makePiece(Type.knight,		7,y,	turn)
		self.makePiece(Type.lance,		8,y,	turn)

		# Map更新
		self.makeMap()

	# MAP作成
	def makeMap(self):
		self.board = [[-1 for i in range(9)] for j in range(9)]	#MAPを-1で初期化
		self.board.append([])
		self.board.append([])
		for p in self.piece:	# 駒情報をループ
			pos = p.getPos()
			if pos[0] == 10 or pos[0] == 9:
				ID =self.piece.index(p)
				self.board[pos[0]].append(ID)
				p.setY(self.board[pos[0]].index(ID))
			else:
				self.board[pos[0]][pos[1]] = self.piece.index(p)	# 更新

	def makePiece(self,type,x,y,turn):
		self.piece.append(Piece(type,x,y,turn))

	# 駒情報取得
	def getPiece(self, PosX, PosY):
		bd = self.board[PosX][PosY]
		if (bd == -1):
			return 0
		pc = self.piece[bd]
		turn = 1 if pc.turn else -1
		pro = 10 if pc.promote else 0
		return (pc.type.value + pro) * turn
	def getturn(self,PosX,PosY):
		bd = self.board[PosX][PosY]
		if (bd == -1):
			return 0
		pc = self.piece[bd]
		return pc.turn
	# 持ち駒の数取得
	def getMochigomaLen(self, PosX):
		return len(self.board[PosX])

	# 持ち駒のXY取得
	def getMochigomaXY(self, type, x):
		res = [0,0]
		for p in self.piece:	# 駒情報をループ
			if(p.getType().value == type):
				pos = p.getPos()
				if(pos[0] == x):
					res = pos
					break
		return res

	# 成れるか判定
	def chkPromote(self, fromPos, toPos):
		# fromに駒がないのはありえない
		fm = self.piece[self.board[fromPos[0]][fromPos[1]]]
		promote = fm.chkPromote(fromPos[1],toPos[1])	# 成れるか判定
		return promote

	# 成り情報取得
	def getPromote(self, fromPos, toPos):
		# fromに駒がないのはありえない
		fm = self.piece[self.board[fromPos[0]][fromPos[1]]]
		return fm.getPromote()	# 成り情報取得


	def setPiece(self, fromPos, toPos, promote):
		# fromに駒がないのはありえない
		bi = self.board[fromPos[0]][fromPos[1]]
		fm = self.piece[bi]

		# 駒タイプを返すために取得しておく
		type = fm.getType().value

		# 相手の駒があったら自分の持ち駒に入れる
		indexTo = self.board[toPos[0]][toPos[1]]
		if(indexTo != -1):		# toに駒がある場合
			x = fm.getIndexM()
			y = len(self.board[x])
			self.piece[indexTo].chgPiece(x,y)

		# 駒移動
		fm.setPiece(toPos[0], toPos[1], promote)
		self.makeMap()

		return type

	#移動可能な座標の抽出
	def Possible(self, choice):
		possible_move = []

		piece = self.piece[self.board[choice[0]][choice[1]]]
		turn = piece.getTurn()

		if choice[0] < 9:		# 盤面の駒なら
			if piece.getTurn():
				player = 1
			else:
				player = -1
			for move in self.move[piece.getTypeV()]:
				#連続移動が可能なら
				if abs(move[0]) == 10 or abs(move[1]) == 10:
					xVec = self.setOne(move[0]) * player
					yVec = self.setOne(move[1]) * player
					# 1からカウントアップ
					for n in range(1,9):
						x = int(choice[0] - n * xVec)
						y = int(choice[1] - n * yVec)
						# xyが0から8を外れたら終了
						if not 0<=x<=8 or not 0<=y<=8:
							break
						#そこが自分の駒じゃなければ対象
						index = self.board[x][y]
						if index == -1:		# 空きマスの場合
							possible_move.append([x,y])
							continue
						if self.piece[index].getTurn() != turn:		#相手の駒の時その駒まで
							possible_move.append([x,y])
							break
						else:	#自分の駒の場合その手前まで
							break

				else:	# 1マス移動の場合
					x = choice[0] - move[0] * player
					y = choice[1] - move[1] * player
					# xyが0から8を外れたら終了
					if not 0<=x<=8 or not 0<=y<=8:
						continue

					# 空きか相手の駒なら追加
					index = self.board[x][y]
					if index == -1 or self.piece[index].getTurn() != turn:
						possible_move.append([x,y])

		else:		# 持ち駒なら
			line = 0
			xPawn = []
			type = piece.getType()
			if (type==Type.pawn):	# 歩なら先1列はダメ
				xPawn = self.validPawn(turn)	# 歩が存在している列を取得
				line = 1
			elif (type==Type.lance):	# 香なら先1列はダメ
				line = 1
			elif (type==Type.knight):					# 桂なら先2列はダメ
				line = 2

			for x in range(9):
				# 2歩チェック
				if x in xPawn:	# x列に歩が存在していたら対象外
					continue
				for y in range(9):
					if self.board[x][y]==-1:
						if(turn):		# プレイヤ判断
							if(y<line):
								continue
						else:
							if(y>8-line):
								continue
						possible_move.append([x,y])
		return possible_move

	def setOne(self,v):
		res = -1 if v < 0 else 1 if v > 0 else 0
		return res

	def validPawn(self, turn):
		valid = []
		for p in self.piece:	# 駒情報をループ
			valid.append(p.isPawn(turn))	# 駒のXをリストに入れる
		valid = set(valid)		# 重複を削除
		return valid

	def Dump(self):
		for p in self.piece:	# 駒情報をループ
			i = self.piece.index(p)
			p.Dump(i)
		self.DumpBoard(True)
		self.DumpBoard(False)

	def DumpBoard(self,flg):
		w=3
		sp=' '*w
		hf='-'*w
		print(' '+sp+'0'+sp+'1'+sp+'2'+sp+'3'+sp+'4'+sp+'5'+sp+'6'+sp+'7'+sp+'8')
		for y in range(9):
			d=[0]*9
			form = ' '+str(y)+'|'
			form2 = '  +'
			for x in range(9):
				form  += '{'+str(x)+':>'+str(w)+'}|'
				form2 += '{0:>'+str(w)+'}+'
				if(flg):
					d[x] = self.getPiece(x,y)
				else:
					d[x] = self.board[x][y]
			print(form2.format(hf))
			print(form.format(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8]))
		print(form2.format(hf))


	def pieceGet(self):
		res=[]
		for p in self.piece:	# 駒情報をループ
			res.append(p.getAll())
		return(res)
