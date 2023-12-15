import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel
from llm_chat import *

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建左右两个垂直布局
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # 创建左侧的两个文本框和一个按钮，并添加到左侧布局中
        self.left_input = QLabel('输入')
        self.left_textbox1 = QTextEdit()
        self.left_output = QLabel('输出')
        self.left_textbox2 = QTextEdit()
        self.left_button = QPushButton("生成回复")
        left_layout.addWidget(self.left_input)
        left_layout.addWidget(self.left_textbox1)
        left_layout.addWidget(self.left_output)
        left_layout.addWidget(self.left_textbox2)
        left_layout.addWidget(self.left_button)

        # 创建右侧的一个文本框，一个按钮，一个文本框，并将它们添加到右侧布局中
        self.right_input = QLabel('需要修改的文字')
        self.right_textbox1 = QTextEdit()
        self.right_button = QPushButton("修改选中内容")
        self.right_output = QLabel('修改结果')
        self.right_textbox2 = QTextEdit()
        right_layout.addWidget(self.right_input)
        right_layout.addWidget(self.right_textbox1)
        right_layout.addWidget(self.right_button)
        right_layout.addWidget(self.right_output)
        right_layout.addWidget(self.right_textbox2)

        self.left_textbox2.mouseReleaseEvent = self.set_selected_text
        self.left_button.clicked.connect(self.generate_content)
        self.right_button.clicked.connect(self.modify_content)

        # 创建一个水平布局，将左右两个垂直布局添加到水平布局中
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # 设置主窗口的布局为我们刚刚创建的水平布局
        self.setLayout(main_layout)

        # 设置窗口的位置和大小
        self.setGeometry(300, 300, 800, 300)
        self.setWindowTitle('赛题二样例')
        self.show()

    def set_selected_text(self, event):
        cursor = self.left_textbox2.textCursor()
        self.right_textbox1.setText(cursor.selectedText())

    def generate_content(self):
        question = self.left_textbox1.toPlainText()
        first_answer = get_llm_answer(question)
        self.left_textbox2.setText(first_answer)

    def modify_content(self):
        question = self.left_textbox1.toPlainText()
        first_answer = self.left_textbox2.toPlainText()
        choosed_text = self.right_textbox1.toPlainText()
        prompt = \
        f"""
        我对你给定的内容中，有一部分不太满意，请帮我重新对这部分进行生成，并且以json的形式返回给我。
        原有生成结果中，我不满意的片段是{choosed_text}
        Json返回的内容格式为：
        {str('{')}"
        "修改后的内容":str
        {str('}')}
        """

        messages = [{'role': 'user', 'content': question},
                    {'role': 'assistant', 'content': first_answer},
                    {'role': 'user', 'content': prompt}
                    ]
        sencond_answer = get_llm_answer_with_msg(messages)
        json_dict = extract_json_from_llm_answer(sencond_answer)
        replace_text = json_dict["修改后的内容"]
        self.right_textbox2.setText(first_answer.replace(choosed_text, replace_text))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
