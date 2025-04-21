from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QLabel, QMessageBox,
    QHBoxLayout, QLineEdit
)
from isreachable import parse_grammar, find_reachable_nonterminals, filter_reachable_grammar
from print_words import derivation_to_nonterminal


class GrammarAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ достижимости в КС‑грамматике")
        self.setGeometry(100, 100, 700, 650)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()


        main_layout.addWidget(QLabel("КС-грамматика"))
        self.grammar_input = QTextEdit()
        self.grammar_input.setPlaceholderText(
            "S→AB|CD\nA→EF\nG→AD\nC→c"
        )
        main_layout.addWidget(self.grammar_input)


        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Стартовый символ:"))
        self.start_input = QLineEdit()
        self.start_input.setText("S")
        self.start_input.setMaximumWidth(50)
        start_layout.addWidget(self.start_input)
        start_layout.addStretch()
        main_layout.addLayout(start_layout)

        btn_layout = QHBoxLayout()
        load_btn = QPushButton("Загрузить из файла")
        load_btn.clicked.connect(self.load_from_file)
        btn_layout.addWidget(load_btn)

        analyze_btn = QPushButton("Анализировать")
        analyze_btn.clicked.connect(self.analyze_grammar)
        btn_layout.addWidget(analyze_btn)

        main_layout.addLayout(btn_layout)

        main_layout.addWidget(QLabel("Результат:"))
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        main_layout.addWidget(self.output_box)

        self.setLayout(main_layout)

    def load_from_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл грамматики", "", "Text Files (*.txt);;All Files (*)"
        )
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.grammar_input.setText(f.read())
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл:\n{e}")

    def analyze_grammar(self):
        raw_lines = self.grammar_input.toPlainText().strip().splitlines()
        if not raw_lines:
            QMessageBox.warning(self, "Ошибка", "Грамматика не введена!")
            return

        start_symbol = self.start_input.text().strip()
        if not start_symbol:
            QMessageBox.warning(self, "Ошибка", "Введите стартовый символ!")
            return
        if len(start_symbol) != 1 or not start_symbol.isupper():
            QMessageBox.warning(
                self, "Ошибка",
                "Стартовый символ должен быть одним заглавным нетерминалом (A–Z)."
            )
            return

        try:
            productions = parse_grammar(raw_lines)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка разбора грамматики:\n{e}")
            return
        if start_symbol not in productions:
            QMessageBox.warning(
                self, "Ошибка",
                f"Стартовый символ '{start_symbol}' отсутствует в левой части"
            )
            return

        reachable = find_reachable_nonterminals(productions, start_symbol)
        filtered = filter_reachable_grammar(productions, reachable)

        out_lines = []
        out_lines.append(f"Достижимые нетерминалы из '{start_symbol}': {', '.join(sorted(reachable))}\n")

        for nt in sorted(reachable):
            deriv = derivation_to_nonterminal(productions, start_symbol, nt)
            out_lines.append(f"Вывод для {nt}: {deriv if deriv else 'Не найдено'}")

        out_lines.append("\nГрамматика без недостижимых нетерминалов:")
        keys = list(filtered.keys())
        keys.sort()
        if start_symbol in keys:
            keys.remove(start_symbol)
            keys.insert(0, start_symbol)
        for nt in keys:
            prods = ' | '.join(filtered[nt])
            out_lines.append(f"{nt} → {prods}")

        self.output_box.setText('\n'.join(out_lines))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = GrammarAnalyzer()
    win.show()
    sys.exit(app.exec())
