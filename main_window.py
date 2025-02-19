import os
import pickle
from functools import partial
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qt

class MainWindow(Qw.QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("MainWindow")
    self.setGeometry(100, 50, 640, 240)

    # ステータスバーの初期化
    self.sb_status = Qw.QStatusBar()
    self.setStatusBar(self.sb_status)
    self.sb_status.setSizeGripEnabled(False)
    self.sb_status.showMessage("ハロー(^▽^)/")

    self.data_file = './qt-05.dat'
    self.text_file = './qt-05-text.dat'  # テキストデータの保存先

    # データファイルが存在すれば読み込む
    if os.path.isfile(self.data_file):
      with open(self.data_file, 'rb') as file:
        data = pickle.load(file)
        self.card_counts = data.get('card_counts', {})
        self.charges = data.get('charges', {})
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

    # テキストボックスを右寄せしつつレスポンシブにする
    text_layout = Qw.QHBoxLayout()
    text_layout.addStretch(2)

    self.tb_log = Qw.QTextEdit()
    self.tb_log.setPlaceholderText('ここに文字を打つことができます')
    self.tb_log.setSizePolicy(
        Qw.QSizePolicy.Policy.Expanding, Qw.QSizePolicy.Policy.Expanding)

    # ✅ 保存されたテキストを読み込む
    if os.path.isfile(self.text_file):
      with open(self.text_file, 'r', encoding='utf-8') as file:
        self.tb_log.setPlainText(file.read())

    text_layout.addWidget(self.tb_log, stretch=3)
    main_layout.addLayout(text_layout)

  def update_status(self):
    """ ステータスバーの更新処理 """
    self.sb_status.showMessage('データを読み込みました。')

  def on_button_clicked(self, t):
    """ボタンがクリックされたとき、カーソル位置に文字を挿入し、フォーカスを戻す"""
    cursor = self.tb_log.textCursor()

    if t == "|":
      cursor = self.tb_log.textCursor()
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

    self.tb_log.setTextCursor(cursor)
    self.tb_log.setFocus()

  def closeEvent(self, event):
    """プログラム終了時にデータとテキストを保存"""
    # ✅ テキスト内容を保存
    with open(self.text_file, 'w', encoding='utf-8') as file:
      file.write(self.tb_log.toPlainText())

    # ✅ データを保存
    with open(self.data_file, 'wb') as file:
      data = {
          'card_counts': self.card_counts,
          'charges': self.charges
      }
      pickle.dump(data, file)
      print('データファイルを更新セーブしました。')

    event.accept()
