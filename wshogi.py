import math as ma	# 画像回転に使用
import wx			# wxpython
import re			# 正規表現
from Board import Board
from AutoProcess import AutoProcess
# 定数設定

piece_w = int(360*0.14)	# 駒サイズ横
piece_h = int(443*0.14)	# 駒サイズ縦

board_w = int(735*0.8)	# 盤面サイズ横
board_h = int(800*0.8)	# 盤面サイズ縦

board_panel_w = board_w + (piece_w + 10)*2	# 盤面サイズ横
board_panel_h = board_h	# 盤面サイズ縦


left_panel_w  = piece_w + 10	# 左パネルサイズ横
right_panel_w = piece_w + 10	# 右パネルサイズ横
control_panel_w = 185			# 右パネルサイズ横
control_panel_h = board_h		# 右パネルサイズ縦

title = 30
menu = 0#20
tool = 0	# 16
status = 30
frame_w = board_panel_w + control_panel_w	# windowサイズ横
frame_h = board_h + title + menu + tool + status + 1		# windowサイズ縦

IdBase = 10000
IdXBase = 100

IdCont = 20000

# グローバル変数

mode = 1	# 駒選択
define_player = 1	# player選択
define_Turn = True
player = define_player
Turn = define_Turn

#[上側、下側]
#AutoFlag = [True,True]
AutoFlag = [True,False]
#AutoFlag = [False,True]
#AutoFlag = [False,False]


# 盤面パネルクラス
class BoardPanel(wx.Panel):
	def __init__(self, parent, id, frame):
		wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN, size=(board_panel_w, board_panel_h))
		self.SetBackgroundColour('#DDFF44')

		self.drawflag = False
		self.frame = frame
		self.board = frame.board

		# 背景画像作成
		file = 'texture/shogi_ban.png'								# 背景ファイル名
		image = wx.Image(file)										# ファイル読み込み(イメージ)
		image = image.Scale(board_w,board_h,wx.IMAGE_QUALITY_HIGH)	# 縮尺変更
		self.image = image.ConvertToBitmap()						# BMPに変換
		# パネルにBMP表示
		self.Bind(wx.EVT_PAINT, self.OnPaint)


		self.cp = frame.controlPanel

		self.frame.SetStatusText('あなたの番です', 0)
		self.frame.SetStatusText('mode = 1', 1)

		PATH = "texture/"
		filenames =	["",
						 PATH +"syougi14_fuhyou.png" ,		# 1
						 PATH +"syougi12_kyousya.png" ,		# 2
						 PATH +"syougi10_keima.png" ,		# 3
						 PATH +"syougi08_ginsyou.png" ,		# 4
						 PATH +"syougi07_kinsyou.png" ,		# 5
						 PATH +"syougi03_hisya.png" ,		# 6
						 PATH +"syougi05_gakugyou.png" ,	# 7
						 PATH +"syougi01_ousyou.png" ,		# 8
						 PATH +"syougi02_gyokusyou.png" ,	# 9
						 "",								# 10
						 PATH +"syougi15_tokin.png" ,		# 11
						 PATH +"syougi13_narikyou.png" ,	# 12
						 PATH +"syougi11_narikei.png" ,		# 13
						 PATH +"syougi09_narigin.png" ,		# 14
						 PATH +"syougi07_kinsyou.png" ,		# 15
						 PATH +"syougi04_ryuuou.png" ,		# 16
						 PATH +"syougi06_ryuuma.png" ,		# 17
						 PATH +"syougi01_ousyou.png" ,		# 18
						 PATH +"syougi02_gyokusyou.png" ]	# 19
		# bitmap作成
		self.bitmap = []
		self.rbitmap = []
		for filename in filenames:
			self.getTexture(filename)

		# ボタン表示
		self.reflesh()
		self.Bind(wx.EVT_BUTTON,self.OnClick)

	# 駒のBMP作成
	def getTexture(self,filename):
		if filename != "":
			image = wx.Image(filename)
			image = image.Scale(piece_w,piece_h,wx.IMAGE_QUALITY_HIGH)
			image2 = image.Rotate(ma.pi,wx.Point(int(image.GetWidth()/2),int(image.GetHeight()/2)))
			bitmap = image.ConvertToBitmap()
			bitmap2 = image2.ConvertToBitmap()
		else:
			bitmap = wx.Bitmap()
			bitmap2 = wx.Bitmap()
		self.bitmap.append(bitmap)
		self.rbitmap.append(bitmap2)

	# 駒のBMP取得
	def getBmp(self,piece):
		if piece < 0:
			return self.rbitmap[abs(piece)]
		return self.bitmap[piece]


	def OnPaint(self, evt):
		dc = wx.PaintDC(self)
		dc.Clear()
		dc.DrawBitmap(self.image, piece_w + 10, 0)

	def OnClick(self,event):
		global player
		global mode
		id = event.GetId() - IdBase
		tmpX = int(id / IdXBase)
		tmpY = int(id % IdXBase)
		if (not self.cp.isSelectionMaxRow()):
			wx.MessageBox("最新盤面の時のみ駒移動できます")
			return

		if mode == 1:	# 駒選択
			self.fromX = tmpX
			self.fromY = tmpY
			# 自分の駒ならOK

			if (tmpX > 8):	# 持ち駒の場合
				if (player==1 and tmpX!=10) or (player==-1 and tmpX!=9):	# play1は10以外対象外
					return
			else:		# 盤上の場合
				if self.board.getturn(tmpX, tmpY) == Turn :	# 空きか相手の駒なら対象外
					return

				# 現状は持ち駒も９個までなのでいっぱいの時は持ち駒出すだけ
				index = 10 if player==1 else 9
				if(self.board.getMochigomaLen(index) >= 9):
					wx.MessageBox("現状は持ち駒も９個までなのでいっぱいの時は持ち駒出すだけ")
					return

			# 移動可能範囲にボタンを配置
			self.possible_move = self.board.Possible([tmpX,tmpY])
			if(len(self.possible_move) == 0):	# 移動ができない場合、選択できない
				return

			# 移動可能範囲でループ
			for pos in self.possible_move:
				# 空きマスの場合ボタンを配置
				if self.board.getPiece(pos[0], pos[1])==0:
					bx = pos[0] * (piece_w + 11) + 25 + piece_w + 10
					by = pos[1] * (piece_h + 5) + 20
					button = wx.Button(self,IdBase+IdXBase*pos[0]+pos[1],pos=(bx,by),size=(piece_w,piece_h))
					self.button[pos[0]][pos[1]] = button
			# モード変更
			mode = 2
			self.frame.SetStatusText('mode = 2', 1)

		elif mode == 2:	# 移動先選択
			fmPos = [self.fromX,self.fromY]
			toPos = [tmpX,tmpY]
			if (toPos == fmPos):	# 同じ駒が押されたら
				mode = 1				# modeを1に戻す
				self.reflesh()			# ボタン再描画
				self.frame.SetStatusText('mode = 1', 1)
				return					# 終了

			if (tmpX > 8):	# 盤上じゃなかったら対象外
				return

			# 移動可能範囲ならOK
			if not( toPos in self.possible_move) :
				return

			#成れるかどうか判定
			promote = self.board.getPromote(fmPos,toPos)
			if(self.board.chkPromote(fmPos,toPos)):
				#成るかどうか確認
				dialog = wx.MessageDialog(None, '"成りますか？"', '将棋',style=wx.YES_NO)
				res = dialog.ShowModal()
				if(res == wx.ID_YES):
					promote = True
				dialog.Destroy()
			# 駒移動
			self.setPiece(fmPos,toPos,promote)
	def setPiece(self,fmPos,toPos,promote):
		global mode
		# 駒移動
		type = self.board.setPiece(fmPos,toPos,promote)	# 盤面更新
		mode = 1

		self.reflesh()			# ボタン再描画
		self.cp.addRecord(fmPos, toPos, type, promote)	#棋譜

		self.drawflag = True

	def SetDrawFlag(self,flag):
		self.drawflag = flag
	def GetDrawFlag(self):
		return self.drawflag
	def reflesh(self):
		self.DestroyChildren()

		self.button = [[0]*9] * 12
		# ボタン作成
		for y in range(9):
			for x in range(9):
				self.button[x][y] = 0
				piece = self.board.getPiece(x,y)
				if piece!=0:
					bitmap = self.getBmp(piece)
					bx = x * (piece_w + 11) + 25 + piece_w + 10
					by = y * (piece_h + 5) + 20
					button = wx.BitmapButton(
						self,IdBase+IdXBase*x+y,bitmap,pos=(bx,by),size=(piece_w,piece_h))
					self.button[x][y] = button
		# 持ち駒ボタン作成
		x=9
		for y in range(self.board.getMochigomaLen(x)):
			piece = self.board.getPiece(x,y)
			self.button[x][y] = 0
			if piece!=0:
				bitmap = self.getBmp(piece)
				bx = 10
				by = y * (piece_h + 5) + 20
				button = wx.BitmapButton(self,IdBase+IdXBase*x+y,bitmap,pos=(bx,by),size=(piece_w,piece_h))
				self.button[x][y] = button

		x=10
		for y in range(self.board.getMochigomaLen(x)):
			piece = self.board.getPiece(x,y)
			self.button[x][y] = 0
			if piece!=0:
				bitmap = self.getBmp(piece)
				bx = board_w + piece_w + 10
				by = (8 - y) * (piece_h + 5) + 20
				button = wx.BitmapButton(self,IdBase+IdXBase*x+y,bitmap,pos=(bx,by),size=(piece_w,piece_h))
				self.button[x][y] = button




# 制御クラス
class ControlPanel(wx.Panel):
	def __init__(self, parent, id, frame):
		wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN, size=(control_panel_w, control_panel_h))

		self.frame = frame
		self.board = frame.board

		self.SetBackgroundColour('#FFFFCC')

		# ボタン用画像
		fn1 = "icons/icon_first_32.png"
		fn2 = "icons/icon_left_32.png"
		fn3 = "icons/icon_right_32.png"
		fn4 = "icons/icon_last_32.png"

		# ボタン作成
		butR=wx.Button(self,IdCont+1,"読 込",pos=(5,5),size=(50,20))
		butW=wx.Button(self,IdCont+2,"保 存",pos=(60,5),size=(50,20))
		butO=wx.Button(self,IdCont+7,"出力",pos=(120,5),size=(35,20))
		wx.BitmapButton(self,IdCont+3,wx.Bitmap(fn1),pos=(5,30),size=(35,30))
		wx.BitmapButton(self,IdCont+4,wx.Bitmap(fn2),pos=(45,30),size=(35,30))
		wx.BitmapButton(self,IdCont+5,wx.Bitmap(fn3),pos=(85,30),size=(35,30))
		wx.BitmapButton(self,IdCont+6,wx.Bitmap(fn4),pos=(125,30),size=(35,30))
		# ボタン色
		butR.SetBackgroundColour('light blue')
		butW.SetBackgroundColour('light blue')
		butO.SetBackgroundColour('light blue')

		# ボタンイベント
		self.Bind(wx.EVT_BUTTON,self.OnClick)

		# 棋譜リストボックス作成
		self.listBox = wx.ListBox(self,pos=(5,65),size=(155, control_panel_h-70),style=wx.LB_SORT)
		self.listBox.Bind(wx.EVT_LISTBOX, self.OnSelect)
		self.listBox.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDoubleClick)
		self.piece_element = ["　","歩","香","桂","銀","金","飛","角","玉",""
							,"","と","成香","成桂","成銀","","龍","馬"]
		self.J_num = ["一","二","三","四","五","六","七","八","九"]
		self.j_num = ["１","２","３","４","５","６","７","８","９"]

		self.Seq = 0

		# フォント変更
		font = wx.Font(10,wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
		self.listBox.SetFont(font)

	# ボタンイベント
	def OnClick(self,event):
		id = event.GetId()
		print("Click", id)

		# 開く
		if (id == IdCont+1):
			filename = self.SelectFile()
			if(filename!=""):
				print("開く", filename)
				self.Load(filename)

		# 保存
		if (id == IdCont+2):
			filename = self.SelectFile(wx.FD_SAVE)
			if(filename!=""):
				print("保存", filename)
				self.Save(filename)

		# 出力
		if (id == IdCont+7):
			print("出力")
			self.pieceOut()

		# 先頭
		if (id == IdCont+3):
			self.Seq = 0
			self.listBox.SetSelection(-1)
			self.redo()

		# 戻る
		if (id == IdCont+4):
			self.Seq = self.listBox.GetSelection()-1
			if (self.Seq >= -1):
				self.listBox.SetSelection(self.Seq)
				self.redo()

		# 次
		if (id == IdCont+5):
			cnt = self.listBox.GetCount()-1
			self.Seq = self.listBox.GetSelection()+1
			if (self.Seq <= cnt):
				self.listBox.SetSelection(self.Seq)
				self.redo()

		# 最終
		if (id == IdCont+6):
			self.Seq = self.listBox.GetCount()-1
			self.listBox.SetSelection(self.Seq)
			self.redo()

	# ファイル選択ダイアログ表示
	def SelectFile(self, Style=wx.FD_OPEN):
		# ダイアログ作成
		dialog = wx.FileDialog(self, 'ファイルを選択してください', style=Style)
		dialog.SetDirectory("dat")			# 初期ディレクトリ
		dialog.SetFilename("record.kif")	# 初期ファイル
		dialog.SetWildcard("棋譜file(*.kif)|*.kif|All file(*.*)|*.*")
		# ダイアログ表示
		dialog.ShowModal()
		return dialog.GetPath()		# 選択されたファイル名を返す

	#リストをダブルクリック処理
	def OnDoubleClick(self, event):
		sel = self.listBox.GetSelection()+1
		cnt = self.listBox.GetCount()
		if sel %2 == 0:
			flag = AutoFlag[1]

		else:
			 flag = AutoFlag[0]
		if flag:
			wx.MessageBox("次の手が自動の時は消せません")
			return

		#消去かどうか確認
		dialog = wx.MessageDialog(None, str(sel+1)+'以降を消去します', '将棋',style=wx.YES_NO)
		res = dialog.ShowModal()
		if(res == wx.ID_YES):
			for Y in range(sel, cnt):
				self.listBox.Delete(sel)
			self.redo()
		dialog.Destroy()

	def OnSelect(self, event):
		self.redo()

	# 棋譜データの再生
	def redo(self):
		global player
		global mode
		global Turn
		mode = 1
		listBox = self.listBox
		n = listBox.GetSelection()
		if n == wx.NOT_FOUND:
			self.board.initBoard()
			self.frame.SetStatusText('あなたの番です', 0)
			player = 1
			self.frame.boardPanel.reflesh()			# ボタン再描画
			return

		if (n % 2 == 0):
			self.frame.SetStatusText('相手の番です', 0)
			player = define_player* -1
			Turn = not define_Turn
		else:
			self.frame.SetStatusText('あなたの番です', 0)
			player = define_player
			Trun =  define_Turn

		# 初期状態に戻す
		self.board.initBoard()

		# 棋譜を再実行
		for line in range(n+1):
			data = self.listBox.GetClientData(line)
			# data 0:toPosX 1:toPosY 2:piece 3:fromPosX 4:fromPosY 5:promote
			#成るかどうか(棋譜のデータから読み込む)
			promote = data[5]

			# 持ち駒出しの時fromのX,Yを取得する(load直後)
			fmpos = [data[3],data[4]]
			if(data[4] == -1):	# X=0
				#turn = False if line%2==0 else True
				fmpos = self.board.getMochigomaXY(data[2],data[3])

			self.board.setPiece(fmpos,[data[0],data[1]], promote)	# 盤面更新

		self.frame.boardPanel.reflesh()			# ボタン再描画

	def addRecord(self, fromPos, toPos, piece, promote):
		self.Seq = self.listBox.GetCount()
		pc = piece		# 表示用のindex
		if(promote):	# 成っていたら
			pc += 10	# 表示は成った駒
		da = ""

		msg =  '{0:0>3} {1}{2}{3}'.format(self.Seq+1
			, self.j_num[8-toPos[0]], self.J_num[toPos[1]], self.piece_element[pc])
		if(fromPos[0] > 8):	# 持ち駒出しなら
			msg += "打"		# 元データ無しで打を表示
		else:
			msg += '({0}{1})'.format(9-fromPos[0], fromPos[1]+1)

		data = [toPos[0], toPos[1], pc, fromPos[0], fromPos[1], promote]
		self.listBox.Append(msg,data)
		self.listBox.SetSelection(self.Seq)

	def isSelectionMaxRow(self):
		sel = self.listBox.GetSelection()
		max = self.listBox.GetCount()
		if (max == 0 or sel+1 == max):	# リストが無いか最新じゃない場合
			return True
		return False

	def Load(self, path):
		# リストをクリアする
		self.listBox.Clear()
		self.Seq = 0

		cnt = 0
		toPos = [0,0]
		fromPos = [0,0]
		with open(path, newline='\n', encoding="utf-8") as f:	# ファイルオープン
			for data in f:		# 1行読み込み  "1	７六歩(37) 00～"
				if(not("0" <= data[0] <= "9")):
					continue
				d = re.split(r'[ ()\n]', data)	# スペースか()で3個までスプリット
				d = [s for s in d if s != '']	# ''のデータ削除
				cnt += 1
				if(d[1] == "投了"):
					continue
				# 1個目は捨てる
				# 2個目の処理  "７六歩"
				if(d[1][0] != "同"):
					toPos[0] = 8-self.j_num.index(d[1][0])		# １～９(1文字目)
					toPos[1] = self.J_num.index(d[1][1])		# 一～九(2文字目)
				pd = d[1][2:]
				Flg = False			# 持ち駒出しフラグOFF
				fromPos = [-1,-1]	# 持ち駒出しの場合[0,0]に設定
				if(pd[-1] == "打"):	# 最後が打の場合
					Flg = True		# 持ち駒出しフラグON
					x = 9 if cnt%2==0 else 10
					pd = pd[:-1]	# 最後の文字削除
					fromPos[0] = x
				if(pd[-1] == "成"):	# 最後が成の場合
					pd = pd[:-1]	# 最後の文字削除
					piece = self.piece_element.index(pd)+10		# 駒	(3,4文字目)
				else:
					piece = self.piece_element.index(pd)		# 駒	(3,4文字目)
				promote = False
				if(piece > 10):		# 成っていたら
					piece -= 10
					promote = True
				# 3個目の処理  "37"
				if(not Flg):						# 盤上移動の場合
					fromPos[0] = 9-int(d[2][0])		# 元位置X
					fromPos[1] = int(d[2][1])-1		# 元位置Y

				self.addRecord(fromPos, toPos, piece, promote)		#リストに追加
		# 盤面更新
		self.redo()

	def Save(self, path):
		with open(path, mode='w', newline='', encoding="utf-8") as f:
			for Y in range(self.listBox.GetCount()):
				data = self.listBox.GetString(Y)	# 表示データ
				f.write(data+'\n')

	# 棋譜データから１手毎の駒データ出力
	def pieceOut(self):
		filename = "out.txt"
		n = self.listBox.GetSelection()

		# 初期状態に戻す
		self.board.initBoard()

		with open(filename, mode='w', newline='', encoding="utf-8") as f:
			for line in range(n+1):
				data = self.listBox.GetClientData(line)
				promote = data[5]
				fmpos = [data[3],data[4]]
				if(data[4] == -1):	# X=0
					#turn = False if line%2==0 else True
					fmpos = self.board.getMochigomaXY(data[2],data[3])
				self.board.setPiece(fmpos,[data[0],data[1]], promote)	# 盤面更新

				cntP=1
				f.write('{0:0>3}'.format(line+1))
				for pd in self.board.pieceGet():
					f.write('|{0:0>2}'.format(cntP))
					for pi in pd:
						f.write(','+str(pi))
					cntP+=1
				f.write('\n')
		wx.MessageBox("駒データを出力しました。\n"+ filename)
		# 盤面更新
		self.redo()

# メインフレームクラス
class MainFrame(wx.Frame):
	def __init__(self):
		Style=wx.SYSTEM_MENU|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX
		wx.Frame.__init__(self, None, -1, "将棋", size=(frame_w, frame_h),style=Style)

		# menuの作成
#		fileMenu = wx.Menu()
#		editMenu = wx.Menu()
#		helpMenu = wx.Menu()
#		load = fileMenu.Append(-1, '&Load')
#		save = fileMenu.Append(-1, '&Save')
#		exit = fileMenu.Append(-1, 'E&xit')

		# menuイベントの作成
#		self.Bind(wx.EVT_MENU, self.OnLoad, load)
#		self.Bind(wx.EVT_MENU, self.OnSave, save)
#		self.Bind(wx.EVT_MENU, self.OnExit, exit)

		# menuバーの作成
#		menubar = wx.MenuBar()
#		menubar.Append(fileMenu, '&File')
#		menubar.Append(editMenu, '&Edit')
#		menubar.Append(helpMenu, '&Help')
#		self.SetMenuBar(menubar)

		# toolバーの作成 http://drang.s4.xrea.com/program/lib/img/index.html
#		self.toolbar = self.CreateToolBar()
#		self.toolbar.SetToolBitmapSize((16,16))
#		self.toolbar.AddLabelTool(wx.ID_ANY, "", wx.Bitmap('icons/file_open.bmp'))
#		self.toolbar.AddLabelTool(wx.ID_EXIT, "", wx.Bitmap('icons/file_exit.bmp'))
#		self.toolbar.Realize()
#		self.Bind(wx.EVT_TOOL, self.OnLoad, id=3)
#		self.Bind(wx.EVT_TOOL, self.OnExit, id=wx.ID_EXIT)

		# ステータスバーの作成
		sb = self.CreateStatusBar()
		sb.SetFieldsCount(3)
		sb.SetStatusWidths([-1, -3, -1])
		self.SetStatusText('Left text', 0)
		self.SetStatusText('Center text', 1)
		self.SetStatusText('Right text', 2)

		# パネル作成
		self.board = Board()
		mainPanel = wx.Panel(self, -1)					# メインパネル
		self.controlPanel = ControlPanel(mainPanel, -1, self)	# 制御パネル
		self.boardPanel = BoardPanel(mainPanel, -1, self)		# 盤面パネル

		# パネル分けシザー作成
		hbox = wx.BoxSizer()
		hbox.Add(self.boardPanel, 1)	# 盤面パネル追加
		hbox.Add(self.controlPanel, 1)	# 制御パネル追加

		mainPanel.SetSizer(hbox)	# メインパネルにシザーを反映
		self.Show(True)				# ウィンドウ表示

	# ファイル読み込みイベント
	def OnLoad(self, event):
		self.controlPanel.Load("record.txt")
		wx.MessageBox('Loaded')

	# ファイル書き込みイベント
	def OnSave(self, event):
		self.controlPanel.Save("record.txt")
		wx.MessageBox('Saveed')

	# 終了イベント
	def OnExit(self, event):
		self.Close()



if __name__ == '__main__':
	app = wx.App()
	mf = MainFrame()
	ap = AutoProcess()
#	app.MainLoop()
	evtloop = wx.GUIEventLoop()
	evtloop = wx.EventLoop()
	wx.EventLoop.SetActive( evtloop)

	mf.boardPanel.SetDrawFlag(True)

	"""Drives the main wx event loop."""

	i =0
	while 1:
		while evtloop.Pending(): # if there is at least one event to be processed



			evtloop.Dispatch() # process one event

		#~ time.sleep(0.10)

			if mf.boardPanel.GetDrawFlag():
				print(Turn,player)


				mf.boardPanel.SetDrawFlag(False)
				if AutoFlag[Turn]:
					print(AutoFlag[Turn])
					fmPos ,toPos ,promote  = ap.Do(mf.board,Turn)
					mf.boardPanel.setPiece(fmPos,toPos,promote)
				Turn = not Turn
				player = player * -1

				mf.SetStatusText('mode = '+str(mode), 1)
				if (player == 1):
					mf.SetStatusText('相手の番です', 0)
					#player = -1
				else:
					mf.SetStatusText('あなたの番です', 0)
					#player = 1


			evtloop.ProcessIdle()
			#~ print "***",i




#end
