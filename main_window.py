import os
import pickle
from functools import partial
import PySide6.QtWidgets as Qw
from PySide6.QtGui import QTextCursor
import re


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
    self.data_file = './1.dat'
    self.text_file = './text1.dat'
    self.data_file2 = './2.dat2'
    self.text_file2 = './text2.dat2'

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

  def count_hiragana_alnum(self, text):
    # ひらがな・全角数字・英字・半角数字・丸数字の正規表現パターン
    hiragana_pattern = r'[\u3041-\u3096\u30FC\uFF10-\uFF19\u3000\u2460-\u2473]+'
    # アルファベット（小文字・大文字）+ 半角数字 + - の正規表現パターン
    alnum_pattern = r'[a-zA-Z0-9\-\u0020]+'

    # 先ほどの正規表現にしたがって半角、全角文字をそれぞれ抽出
    hiragana_matches = re.findall(hiragana_pattern, text)
    alnum_matches = re.findall(alnum_pattern, text)

    # 各文字の総数をカウント
    hiragana_count = sum(len(match) for match in hiragana_matches)
    alnum_count = sum(len(match) for match in alnum_matches)

    return hiragana_count, alnum_count

  # ボタンクリック時の処理
  def on_button_clicked(self, t):
    """ボタンがクリックされたとき、カーソル位置に文字を挿入し、フォーカスを戻す"""
    cursor = self.tb_log2.textCursor()

    if t == "|":
      full_text = 0
      harf_text = 0
      print("full_text: ", full_text)
      print("harf_text: ", harf_text)
      cursor = self.tb_log2.textCursor()
      block = cursor.block()
      line_text = block.text()
      text = line_text
      hiragana_count, alnum_count = self.count_hiragana_alnum(text)
      for i in range(hiragana_count):
        full_text += 1
      for i in range(alnum_count):
        harf_text += 1

      cursor.insertText("\n")
      for i in range(full_text):
        cursor.insertText("  ")

      for i in range(harf_text):
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
