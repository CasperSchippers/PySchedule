import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# import time
from datetime import date
import random
import math

class Window(QWidget):
	def __init__(self):
		super(Window, self).__init__()

		self.initUI()
		self.fakedata()

	def initUI(self):
		# define GUI here
		self.box = QVBoxLayout()
		self.inputbox = QHBoxLayout()
		self.middlebuttonbox = QHBoxLayout()
		self.outputbox = QHBoxLayout()
		self.box.addLayout(self.inputbox)
		self.box.addLayout(self.middlebuttonbox)
		self.box.addLayout(self.outputbox)

		# input box
		self.persontable = QTableWidget()
		self.persontable.setRowCount(0)
		self.persontable.setColumnCount(4)
		self.persontable.setHorizontalHeaderLabels("Naam;1;2;3".split(";"))
		self.inputbox.addWidget(self.persontable)

		self.datatable = QTableWidget()
		self.datatable.setRowCount(0)
		self.datatable.setColumnCount(2)
		self.inputbox.addWidget(self.datatable)

		self.cal = QCalendarWidget()
		self.inputbox.addWidget(self.cal)

		# middle button box
		self.startschedulebutton = QPushButton('Maak rooster')
		self.startschedulebutton.clicked.connect(self.scheduler)
		self.middlebuttonbox.addStretch(1)
		self.middlebuttonbox.addWidget(self.startschedulebutton)
		self.middlebuttonbox.addStretch(1)

		# output box
		self.outputtable = QTableWidget()
		self.outputtable.setRowCount(0)
		self.outputtable.setColumnCount(0)
		self.outputtable.setHorizontalHeaderLabels("Datum")
		self.outputbox.addWidget(self.outputtable)

		self.setLayout(self.box)
		self.show()

	def fakedata(self):
		self.people = ['Albert', 'Ben', 'Casper', 'Daan', 'Elroy', 'Floor', 'Geert', 'Henk', 'Ilias', 'Jonathan', 'Karel', 'Leo', 'Marc', 'Nastrobya']
		for i in range(len(self.people)):
			self.persontable.insertRow(self.persontable.rowCount())
			self.persontable.setItem(i,0, QTableWidgetItem(self.people[i]))
		del self.people

		self.dates = [date(2016, 1, 1), date(2016, 1, 2), date(2016, 1, 3), date(2016, 1, 4), date(2016, 1, 5), date(2016, 1, 6), date(2016, 1, 7)]
		for i in range(len(self.dates)):
			self.datatable.insertRow(self.datatable.rowCount())
			self.datatable.setItem(i,0, QTableWidgetItem(self.dates[i].strftime("%d/%m")))


	def scheduler(self):
		self.peoplenum = self.persontable.rowCount()
		self.datesnum = len(self.dates)

		self.numperday = 5

		PickingList = [x for x in range(self.peoplenum)] * math.ceil((self.numperday*self.datesnum)/self.peoplenum)

		# Make a list of an integer times all people so that items on that list > total number of places and randomly pick (and remove) a person from that list for each moment
		# then check if same person is not left over more than once



		self.schedule = [x[:] for x in [[[None]]*self.numperday]*self.datesnum]
		
		# initial filling of the schedule
		for dayID in range(self.datesnum):
			for placeID in range(self.numperday):
				i = random.randrange(len(PickingList))

				while self.schedule[dayID].count(PickingList[i]) != 0:
					i = random.randrange(len(PickingList))

				self.schedule[dayID][placeID] = PickingList[i]

				del PickingList[i]

		check = self.checkschedule()
		if check:
			print('good')
			self.publishschedule()
		elif not check:
			print('bad')

	def publishschedule(self):
		self.people = []
		for i in range(self.peoplenum):
			self.people.append(self.persontable.item(i,0).text())
		
		self.outputtable.setColumnCount(self.numperday+1)
		self.outputtable.setRowCount(self.datesnum)

		HeaderString = "Datum"
		for x in range(5):
			HeaderString += ";Persoon %s" % str(x+1)
		self.outputtable.setHorizontalHeaderLabels(HeaderString.split(';'))

		for i in range(len(self.schedule)):
			self.outputtable.setItem(i,0, QTableWidgetItem(self.dates[i].strftime("%d / %m / %Y")))

			for j in range(len(self.schedule[i])):
				self.outputtable.setItem(i,j+1, QTableWidgetItem(self.people[self.schedule[i][j]]))


	def checkschedule(self):
		return True

	# def correctschedule(self):

	# define other functions of window class

def main():
	app = QApplication(sys.argv)

	window = Window()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()