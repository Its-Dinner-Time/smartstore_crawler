from PyQt5 import QtWidgets

from smartstore_review_crawler import crawler

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("스마트 스토어 리뷰 크롤러")
        self.resize(800, 200)

        # 입력 정보 가이드 위젯
        self.input_guide_label = QtWidgets.QLabel("https://smartstore.naver.com/( 스마트 스토어 shop이름 )/products/( 제품번호 )")

        # 스마트 스토어 URL 입력 위젯
        self.smartstore_shop_input = QtWidgets.QLineEdit()
        self.smartstore_shop_input.setPlaceholderText("스마트 스토어 shop이름")

        # 제품번호 입력 위젯
        self.product_no_input = QtWidgets.QLineEdit()
        self.product_no_input.setPlaceholderText("제품번호")

        # 실행 버튼
        self.run_button = QtWidgets.QPushButton("크롤링 실행")
        self.run_button.clicked.connect(self.run_crawler)

        # 결과 출력 라벨
        self.result_label = QtWidgets.QLabel("결과가 여기에 표시됩니다.")

        # 전체 레이아웃
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.input_guide_label)
        layout.addWidget(self.smartstore_shop_input)
        layout.addWidget(self.product_no_input)
        layout.addWidget(self.run_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def run_crawler(self):
        # 입력한 스마트 스토어 URL 및 제품번호 가져오기
        shop = self.smartstore_shop_input.text()
        product_no = self.product_no_input.text()

        crawler(shop=shop, product_no=product_no)

        # 결과 라벨에 출력
        self.result_label.setText(f'{shop}/{product_no}.json에 크롤링 결과가 저장되었습니다.')

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Window()
    window.show()
    app.exec_()
