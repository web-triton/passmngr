# cd C:\progs\passmngr
# python passmngr.py

import sys
import os.path
from os.path import abspath
import sqlite3

from PyQt5 import QtGui
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QListWidget, QListView, QLabel, QLineEdit)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import (pyqtSlot, Qt)

class passmngr(QWidget):

	db = 'passmngr.db'

	def __init__(self):
		super().__init__()
		file_db = os.path.exists(self.db)
		if file_db:
			self.setStyleSheet("background-color: #202124;")
			self.initUI()
		else:
			print(f'Файл: {self.db} не существует!')
			my_file = open(self.db, "w+")
			my_file.close()

			connect = sqlite3.connect(self.db)
			cursor = connect.cursor()
			cursor.execute("""CREATE TABLE pwds (
				id       INTEGER       PRIMARY KEY AUTOINCREMENT NOT NULL,
				link     VARCHAR (255) NOT NULL,
				login    VARCHAR (255) NOT NULL,
				password VARCHAR (255) NOT NULL
			);""")
			connect.commit()
			self.setStyleSheet("background-color: #202124;")
			self.initUI()

	def add_password(self):
		link = self.input_link.text()
		login = self.input_login.text()
		password = self.input_password.text()
		if link and login and password:
			data = [
				(link, login, password),
			]
			with self.connect:
				self.cursor.executemany('INSERT INTO pwds(link, login, password) VALUES (?,?,?)', data)
				self.connect.commit()
				self.list_widget.addItem(link)

			self.input_link.clear()
			self.input_login.clear()
			self.input_password.clear()

	def add_btn(self):
		add_btn = QPushButton('Добавить', self)
		add_btn.setFont(QtGui.QFont("Arial", 12)) # F2C73C
		add_btn.setStyleSheet("background-color: #F2C73C; color: #202124;padding: 10px; border-radius: 20px; border: 2px solid #F2C73C;")
		add_btn.resize(220, 50)
		add_btn.move(560, 230)
		add_btn.clicked.connect(self.add_password)

	def click_link(self, item):
		logpass = self.cursor.execute("SELECT link, login, password from pwds WHERE link='"+item.text()+"'").fetchall()
		self.link.setText(logpass[0][0])
		self.login.setText(logpass[0][1])
		self.password.setText(logpass[0][2])
		
	def initUI(self):
		self.connect = sqlite3.connect(self.db)
		self.cursor = self.connect.cursor()

		self.list_widget = QListWidget(self)
		self.list_widget.setGeometry(20, 20, 180, 360)
		self.list_widget.setStyleSheet("color: #fff;padding: 10px;line-height: 2; border-radius: 20px; border: 2px solid #F2C73C;")
		for link in self.cursor.execute('SELECT `link` FROM pwds'):
			self.list_widget.addItem(link[0])
		self.list_widget.setMovement(QListView.Free)
		self.list_widget.itemClicked.connect(self.click_link)

		self.input_link = QLineEdit(self)
		self.input_link.setStyleSheet("color: #fff;padding: 10px; border-radius: 20px; border: 2px solid #F2C73C;")
		self.input_link.setFont(QtGui.QFont("Arial", 12))
		self.input_link.setPlaceholderText("Домен") 
		self.input_link.move(540, 20)
		self.input_link.resize(240, 50)

		self.input_login = QLineEdit(self)
		self.input_login.setStyleSheet("color: #fff;padding: 10px; border-radius: 20px; border: 2px solid #F2C73C;")
		self.input_login.setFont(QtGui.QFont("Arial", 12))
		self.input_login.setPlaceholderText("Логин") 
		self.input_login.move(540, 90)
		self.input_login.resize(240, 50)

		self.input_password = QLineEdit(self)
		self.input_password.setStyleSheet("color: #fff;padding: 10px; border-radius: 20px; border: 2px solid #F2C73C;")
		self.input_password.setFont(QtGui.QFont("Arial", 12))
		self.input_password.setPlaceholderText("Пароль") 
		self.input_password.move(540, 160)
		self.input_password.resize(240, 50)

		self.add_btn()

		self.link = QLabel("example.com", self)
		self.link.setFont(QtGui.QFont("Arial", 12))
		self.link.resize(300, 50)
		self.link.setStyleSheet("color: #fff;padding: 10px; border-radius: 20px; border: 2px solid #F2C73C;")
		self.link.move(220, 20)

		self.login = QLabel("no-reply@example.com", self)
		self.login.setFont(QtGui.QFont("Arial", 12))
		self.login.resize(300, 50)
		self.login.setStyleSheet("color: #fff;padding: 10px; border-radius: 20px; border: 2px solid #F2C73C;")
		self.login.move(220, 90)

		self.password = QLabel("12345678", self)
		self.password.setFont(QtGui.QFont("Arial", 12))
		self.password.resize(300, 50)
		self.password.setStyleSheet("color: #fff;padding: 10px; border-radius: 20px; border: 2px solid #F2C73C;")
		self.password.move(220, 160)

		self.setFixedSize(800, 400)
		self.setWindowTitle('Менеджер паролей (пароль.kz)')
		self.setWindowIcon(QtGui.QIcon('icon.png'))
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	check = passmngr()
	sys.exit(app.exec_())
