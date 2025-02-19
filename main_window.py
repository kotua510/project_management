import os
import pickle
from functools import partial
import PySide6.QtWidgets as Qw

class MainWindow(Qw.QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("MainWindow")
    self.setGeometry(100, 50, 640, 240)

    # ステータスバーの初期化
    self.sb_status = Qw.QStatusBar()
    self.setStatusBar(self.sb_status)
    self.sb_status.setSizeGripEnabled(False)
    self.sb_status.showMessage("ファイト!")

    # テキストデータの保存先
    self.data_file = './qt-05.dat'
    self.text_file = './qt-05-text.dat'
    self.data_file2 = './qt-05.dat2'
    self.text_file2 = './qt-05-text.dat2'

    self.card_counts = {}
    self.charges = {}
    self.card_counts2 = {}
    self.charges2 = {}

    # データファイルが存在すれば読み込む
    if os.path.isfile(self.data_file):
      with open(self.data_file, 'rb') as file:
        data = pickle.load(file)
        self.card_counts = data.get('card_counts', {})
        self.charges = data.get('charges', {})
        self.update_status()
    else:
      self.sb_status.showMessage('プログラムを起動しました。')

    if os.path.isfile(self.data_file2):
      with open(self.data_file2, 'rb') as file2:
        data = pickle.load(file2)
        self.card_counts2 = data.get('card_counts2', {})
        self.charges2 = data.get('charges2', {})
        self.update_status()
    else:
      self.sb_status.showMessage('プログラムを起動しました。')

    # メインウィジェットとレイアウト設定
    central_widget = Qw.QWidget()
    self.setCentralWidget(central_widget)
    main_layout = Qw.QVBoxLayout(central_widget)

    # ボタン配置用のレイアウト
    button_layout = Qw.QHBoxLayout()
    btn_thing = ['|', 'ー', '①', '②', '③',
                 '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '☑']

    button_layout.addStretch()
    for text in btn_thing:
      btn = Qw.QPushButton(text)
      btn.setMinimumSize(40, 40)
      btn.clicked.connect(partial(self.on_button_clicked, text))
      button_layout.addWidget(btn)
    button_layout.addStretch()

    main_layout.addLayout(button_layout)

    # テキストボックスの配置
    text_layout = Qw.QHBoxLayout()

    self.tb_log = Qw.QTextEdit()
    self.tb_log.setPlaceholderText('ここはメモなどに使ってください')
    self.tb_log.setSizePolicy(Qw.QSizePolicy.Policy.Expanding,
                              Qw.QSizePolicy.Policy.Expanding)
    # 保存されたテキストを読み込む
    if os.path.isfile(self.text_file):
      with open(self.text_file, 'r', encoding='utf-8') as file:
        self.tb_log.setPlainText(file.read())

    text_layout.addWidget(self.tb_log, stretch=1)
    main_layout.addLayout(text_layout)

    text_layout2 = Qw.QHBoxLayout()
    text_layout2.addStretch(2)

    self.tb_log2 = Qw.QTextEdit()
    self.tb_log2.setPlaceholderText('ここでプロジェクト管理ができます')
    self.tb_log2.setSizePolicy(
        Qw.QSizePolicy.Policy.Expanding, Qw.QSizePolicy.Policy.Expanding)

    if os.path.isfile(self.text_file2):
      with open(self.text_file2, 'r', encoding='utf-8') as file2:
        self.tb_log2.setPlainText(file2.read())

    text_layout.addWidget(self.tb_log2, stretch=3)
    main_layout.addLayout(text_layout2)

  def update_status(self):
    """ ステータスバーの更新処理 """
    self.sb_status.showMessage('データを読み込みました。')

  # ボタンクリック時の処理
  def on_button_clicked(self, t):
    """ボタンがクリックされたとき、カーソル位置に文字を挿入し、フォーカスを戻す"""
    cursor = self.tb_log2.textCursor()

    if t == "|":
      cursor = self.tb_log2.textCursor()
      block = cursor.block()
      line_text = block.text()
      line_length = len(line_text)
      print(f"現在の行の文字数: {line_length}")
      line_length -= 1

      cursor.insertText("\n")
      for i in range(line_length):
        cursor.insertText(" ")
      cursor.insertText("|")
    else:
      cursor.insertText(t)

    self.tb_log2.setTextCursor(cursor)
    self.tb_log2.setFocus()

  def closeEvent(self, event):
    # プログラム終了時にデータとテキストを保存
    # テキスト内容を保存
    with open(self.text_file, 'w', encoding='utf-8') as file:
      file.write(self.tb_log.toPlainText())

    with open(self.text_file2, 'w', encoding='utf-8') as file2:
      file2.write(self.tb_log2.toPlainText())

    # データを保存
    with open(self.data_file, 'wb') as file:
      data = {
          'card_counts': self.card_counts,
          'charges': self.charges
      }
      pickle.dump(data, file)

    with open(self.data_file2, 'wb') as file2:
      data = {
          'card_counts2': self.card_counts2,
          'charges2': self.charges2
      }
      pickle.dump(data, file2)

    print('データファイルを更新セーブしました。')

    event.accept()
