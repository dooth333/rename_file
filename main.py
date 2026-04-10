# nuitka-project: --standalone
# nuitka-project: --windows-console-mode=disable
# nuitka-project: --mingw64
# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --windows-icon-from-ico=rename_file.ico
# nuitka-project: --company-name="wenc"
# nuitka-project: --product-name="rename_file"
# nuitka-project: --file-version=1.0.0.0
# nuitka-project: --product-version=1.0.0.0
# nuitka-project: --file-description="自动重命名工具"
# nuitka-project: --output-filename=ReFile.exe
# nuitka-project: --copyright="Copyright (c) 2026 by wenc. All rights reserved."

import os
import re
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                               QFileDialog, QLabel, QHBoxLayout, QLineEdit, QMessageBox, QPlainTextEdit)
from PySide6.QtGui import QFont
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QSoundEffect  # 使用 QSoundEffect 代替 QSound

class ReFileApp(QWidget):
    def __init__(self):
        super().__init__()
        self.file_name = ""
        self.init_ui()
        self.sound_effect = QSoundEffect()  # 初始化音效对象

    def init_ui(self):
        # 设置窗口标题、大小和字体
        self.setWindowTitle("ReFile - 文件重命名工具")
        self.setGeometry(400, 200, 500, 300)

        # 创建主布局
        layout = QVBoxLayout()

        # 设置标题标签
        title_label = QLabel("ReFile - 自动文件重命名")
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setStyleSheet("color: #3498db; margin-bottom: 15px;")
        layout.addWidget(title_label)

        # 创建并设置"选择文件夹"按钮
        self.button = QPushButton("选择文件夹")
        self.button.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px;")
        self.button.clicked.connect(self.open_folder_dialog)

        # 文件夹路径显示标签
        self.label = QLabel("未选择文件夹")
        self.label.setFont(QFont('Arial', 10))
        self.label.setStyleSheet("color: #e74c3c; margin-bottom: 10px;")

        # 输入框和标签：文件后缀名
        self.suffix_name_layout = QHBoxLayout()
        self.suffix_name_label = QLabel("文件后缀名:")
        self.suffix_name_input = QLineEdit(".wav")
        self.suffix_name_input.setStyleSheet("padding: 5px;")
        self.suffix_name_layout.addWidget(self.suffix_name_label)
        self.suffix_name_layout.addWidget(self.suffix_name_input)

        # 输入框和标签：起始序号
        self.start_index_layout = QHBoxLayout()
        self.start_index_label = QLabel("起始序号:")
        self.start_index_input = QLineEdit("1")
        self.start_index_input.setStyleSheet("padding: 5px;")
        self.start_index_layout.addWidget(self.start_index_label)
        self.start_index_layout.addWidget(self.start_index_input)

        # 输入框和标签：新文件名数字宽度
        self.name_width_layout = QHBoxLayout()
        self.name_width_label = QLabel("数字宽度:")
        self.name_width_input = QLineEdit("3")
        self.name_width_input.setStyleSheet("padding: 5px;")
        self.name_width_layout.addWidget(self.name_width_label)
        self.name_width_layout.addWidget(self.name_width_input)

        # 开始重命名按钮
        self.start_button = QPushButton("开始重命名")
        self.start_button.setStyleSheet("background-color: #f39c12; color: white; padding: 10px;")
        self.start_button.clicked.connect(self.start_rename)

        # 日志输出区域
        self.log_text_edit = QPlainTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setStyleSheet("background-color: #ecf0f1;")
        self.log_text_edit.setStyleSheet("color: #2c3e50;")  # 设置日志文本颜色
        self.log_text_edit.setStyleSheet("border: 1px solid #bdc3c7;")  # 添加边框使日志区域更清晰
        self.log_text_edit.setStyleSheet("padding: 10px;")  # 添加内边距使日志区域更美观

        # 将控件添加到主布局
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.addLayout(self.suffix_name_layout)
        layout.addLayout(self.start_index_layout)
        layout.addLayout(self.name_width_layout)
        layout.addWidget(self.start_button)
        layout.addWidget(self.log_text_edit)

        # 设置窗口布局
        self.setLayout(layout)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.file_name = folder_path
            self.label.setText(f"选中的文件夹: {folder_path}")
            self.label.setStyleSheet("color: #2ecc71;")  # 改变颜色提示
        else:
            self.label.setText("未选择文件夹")
            self.label.setStyleSheet("color: #e74c3c;")

    def start_rename(self):
        suffix_name = self.suffix_name_input.text().strip()
        if not self.file_name:
            QMessageBox.warning(self, "提示", "请先选择文件夹!")
            return

        try:
            start_index = int(self.start_index_input.text())
        except ValueError:
            QMessageBox.warning(self, "提示", "起始序号必须是整数!")
            return

        # 确认操作
        if self.confirmation_dialog():
            self.play_sound("start.wav")  # 播放音效
            self.rename_files_with_new_index(self.file_name, start_index, suffix_name)

    def confirmation_dialog(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("确认操作")
        msg_box.setText("你确定要继续吗？")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        response = msg_box.exec()
        return response == QMessageBox.Yes
    
    def rename_files_with_new_index(self, folder_path, start_index, suffix_name):
        try:
            files = [f for f in os.listdir(folder_path) if f.endswith(suffix_name)]
            if not files:
                QMessageBox.information(self, "提示", "文件夹中没有符合后缀的文件!")
                return

            # 依然保留自然排序，确保提取出来重命名时，原文件顺序是对的
            def natural_sort_key(s):
                return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]
            
            files_sorted = sorted(files, key=natural_sort_key)

            # 设定新文件名的数字宽度
            if not self.name_width_input.text().isdigit():
                QMessageBox.warning(self, "提示", "数字宽度必须是整数!")
                return

            name_width = int(self.name_width_input.text())

            for i, file_name in enumerate(files_sorted, start=start_index):
                
                new_file_name = f"{i:0{name_width}d}{suffix_name}"
                
                old_file_path = os.path.join(folder_path, file_name)
                new_file_path = os.path.join(folder_path, new_file_name)
                
                os.rename(old_file_path, new_file_path)
                self.log_text_edit.appendPlainText(f"Renamed: {file_name} -> {new_file_name}")

            QMessageBox.information(self, "提示", "重命名完成!")
            self.play_sound("completed.wav")  # 播放完成音效

        except Exception as e:
            QMessageBox.critical(self, "错误", f"重命名失败: {str(e)}")

    def play_sound(self, sound_file):
        self.sound_effect.setSource(QUrl.fromLocalFile(sound_file))
        self.sound_effect.setVolume(0.5)  # 设置音量
        self.sound_effect.play()


# 主程序
if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = ReFileApp()
    demo.show()
    sys.exit(app.exec())
