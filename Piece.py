from enum import Enum

class Type(Enum):
	pawn	= 1		#"歩"　１
	lance	= 2		#"香"　２
	knight	= 3		#"桂"　３
	silver	= 4		#"銀"　４
	gold	= 5		#"金"　５
	rook	= 6		#"飛"　６
	bishop	= 7		#"角"　７
	king	= 8		#"王"　８

#-------------------------------------------------------
class Piece:
	def __init__(self,type,x,y,turn,promote=False):
		self.type = type
		self.x = int(x)
		self.y = int(y)
		self.turn = turn
		self.promote = promote

	# 駒移動
	def setPiece(self, x, y, promote):
		self.x = x
		self.y = y
		if(not self.promote):
			self.promote = promote

	# Y設定
	def setY(self, y):
		self.y = y

	# 駒を取り上げる
	def chgPiece(self,x,y):
		self.x = x
		self.y = y
		self.turn = not self.turn
		self.promote = False

	# 成り判定
	def chkPromote(self, fromY, toY):
		res = False

		# 持ち駒を出す場合成らない
		if (self.x >= 9 ):
			return res

		# 成れない駒(金王)は対象外
		if (self.type == Type.gold or self.type == Type.king ):
			return res

		if(not self.promote):	# 成っていない駒の場合
			if(self.turn):		# プレイヤ判断
				if(toY <= 2 or fromY <= 2):		# 0から2の場合
					res = True
			else:
				if(toY >= 6 or fromY >= 6):		# 6から8の場合
					res = True
		return res

	# 2歩チェック
	def isPawn(self, turn):
		if(self.type == Type.pawn and turn == self.turn):
			return self.x
		return -1

	# タイプ取得(数値)
	def getTypeV(self):
		if(self.promote):
			return self.type.value + 10
		return self.type.value

	# タイプ取得
	def getType(self):
		return self.type

	# 成り情報取得
	def getPromote(self):
		return self.promote

	# プレイヤ取得
	def getTurn(self):
		return self.turn

	# ポジション取得
	def getPos(self):
		return [self.x,self.y]

	# 持ち駒インデックス取得
	def getIndexM(self):
		index = 10 if self.getTurn() else 9
		return index

	def Dump(self,i):
		print("Dump",i, self.type,self.x,self.y,self.turn,self.promote)

	def getAll(self):
		turn=1 if self.turn else 0
		promote=1 if self.promote else 0
		return([self.type.value,self.x,self.y,turn,promote])
