import sys
import PySide6.QtWidgets as Qw
from main_window import MainWindow  # 分割したファイルをインポート

# 本体
if __name__ == "__main__":
  app = Qw.QApplication(sys.argv)
  main_window = MainWindow()
  main_window.show()
  sys.exit(app.exec())
