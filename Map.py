import sys
from Piece import Piece,Type

#-------------------------------------------------------
class Map():
	def __init__(self,data):
		# 手数保存
		self.id = data[:3]
		self.piece = []
		# データ読み込み
		for piece in data[4:].split("|"):	# スプリット
			p = piece.split(",")		# スプリット
			# p[] 0:id,1:type,2:x,3:y,4:turn,5:promote
			turn = False if p[4][0]=='0' else True
			promote = False if p[5][0]=='0' else True
			# 駒データ作成
			self.piece.append(Piece(Type(int(p[1])),p[2],p[3],turn,promote))

		# Map作成
		self.makeMap()

	# MAP作成
	def makeMap(self):
		self.board = [[-1 for i in range(9)] for j in range(9)]	#MAPを-1で初期化
		self.board.append([])
		self.board.append([])
		for p in self.piece:	# 駒情報をループ
			pos = p.getPos()
			ID =self.piece.index(p)
			if pos[0] == 10 or pos[0] == 9:
				self.board[pos[0]].append(ID)
				p.setY(self.board[pos[0]].index(ID))
			else:
				self.board[pos[0]][pos[1]] = ID	# 更新

	# マップをコンソールに出力
	def DumpBoard(self,flg):
		print("")
		print(self.id)
		
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


	# 駒情報取得(正負でプレイヤ、+10で成) 歩:1 香:2 桂:3 銀:4 金:5 飛:6 角:7 王:8
	def getPiece(self, PosX, PosY):
		bd = self.board[PosX][PosY]
		if (bd == -1):
			return 0
		pc = self.piece[bd]
		turn = 1 if pc.turn else -1
		pro = 10 if pc.promote else 0
		return (pc.type.value + pro) * turn

# 手数分MAPを作成する
def Run(path):

	# 手数分のMAP
	mapList=[]

	# ファイルオープン
	with open(path, newline='', encoding="utf-8") as f:	# ファイルオープン
		for data in f:		# 1行読み込み 
			# MAP作成
			mapList.append(Map(data))

	# 手数分のマップをコンソールに出力
	for m in mapList:
		m.DumpBoard(True)

if __name__ == '__main__':
	# 実行引数取得
	args = sys.argv
#	print(args)
	# 引数にファイル名が設定されていなければエラー
	if(len(args) == 2):
		Run(args[1])
	else:
		print("引数エラー")

