import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QGridLayout, QPushButton, QLineEdit)
from PySide6.QtCore import Qt

class CalculatorModel:
    def __init__(self):
        self.expression = ""

    def add_to_expression(self, value):
        self.expression += str(value)
        return self.expression

    def clear(self):
        self.expression = ""
        return self.expression

    def calculate(self):
        try:
            # eval() se usa aquí solo para propósitos educativos simples
            result = str(eval(self.expression))
            self.expression = result
            return result
        except Exception:
            self.expression = ""
            return "Error"

class CalculatorView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora")
        self.setFixedSize(300, 400)
        
        self.general_layout = QVBoxLayout()
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self.general_layout)

        self.display = QLineEdit()
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.general_layout.addWidget(self.display)

        self.buttons = {}
        buttons_layout = QGridLayout()
        buttons = {
            '7': (0, 0), '8': (0, 1), '9': (0, 2), '/': (0, 3),
            '4': (1, 0), '5': (1, 1), '6': (1, 2), 'X': (1, 3),
            '1': (2, 0), '2': (2, 1), '3': (2, 2), '-': (2, 3),
            '0': (3, 0), 'C': (3, 1), '=': (3, 2), '+': (3, 3),
        }
        
        for btn_text, pos in buttons.items():
            self.buttons[btn_text] = QPushButton(btn_text)
            self.buttons[btn_text].setFixedSize(60, 60)
            buttons_layout.addWidget(self.buttons[btn_text], pos[0], pos[1])
            
        self.general_layout.addLayout(buttons_layout)

    def set_display_text(self, text):
        self.display.setText(text)
        self.display.setFocus()

class CalculatorController:
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._connect_signals()

    def _calculate_result(self):
        result = self._model.calculate()
        self._view.set_display_text(result)

    def _build_expression(self, sub_expression):
        expression = self._model.add_to_expression(sub_expression)
        self._view.set_display_text(expression)

    def _clear_display(self):
        self._model.clear()
        self._view.set_display_text("")

    def _connect_signals(self):
        for btn_text, btn in self._view.buttons.items():
            if btn_text not in {'=', 'C'}:
                btn.clicked.connect(lambda checked=False, text=btn_text: self._build_expression(text))

        self._view.buttons['='].clicked.connect(self._calculate_result)
        self._view.buttons['C'].clicked.connect(self._clear_display)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = CalculatorModel()
    view = CalculatorView()
    controller = CalculatorController(model, view)
    view.show()
    sys.exit(app.exec())