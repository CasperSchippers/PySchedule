import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# import time
from datetime import datetime
import random
import math

class Window(QWidget):
	def __init__(self):
		super(Window, self).__init__()

		self.initUI()
		self.fakedata()

	def initUI(self):
		# define GUI here
		box = QVBoxLayout()
		inputbox = QHBoxLayout()
		middlebuttonbox = QHBoxLayout()
		outputbox = QHBoxLayout()
		box.addLayout(inputbox)
		box.addLayout(middlebuttonbox)
		box.addLayout(outputbox)

		# input box
		## Persontabel
		personbox = QVBoxLayout()
		inputbox.addLayout(personbox)

		self.persontable = QTableWidget()
		self.persontable.setRowCount(0)
		self.persontable.setColumnCount(4)
		self.persontable.setHorizontalHeaderLabels("Naam;1;2;3".split(";"))
		personbox.addWidget(self.persontable)

		personbuttonbox = QHBoxLayout()
		personbox.addLayout(personbuttonbox)

		addpersonrowbutton = QPushButton("Persoon toevoegen")
		addpersonrowbutton.clicked.connect(self.addpersonrow)
		personbuttonbox.addWidget(addpersonrowbutton)

		deletepersonrowbutton = QPushButton("Persoon verwijderen")
		deletepersonrowbutton.clicked.connect(self.removepersonrow)
		personbuttonbox.addWidget(deletepersonrowbutton)

		## Datatabel
		databox = QVBoxLayout()
		inputbox.addLayout(databox)

		self.datatable = QTableWidget()
		self.datatable.setRowCount(0)
		self.datatable.setColumnCount(2)
		self.datatable.setHorizontalHeaderLabels(["Datum", "Tijd (optioneel)"])
		databox.addWidget(self.datatable)

		databuttonbox = QHBoxLayout()
		databox.addLayout(databuttonbox)

		adddatumrowbutton = QPushButton('Voeg rij toe')
		adddatumrowbutton.clicked.connect(self.adddatumrow)
		databuttonbox.addWidget(adddatumrowbutton)

		deletedatumrowbutton = QPushButton('Verwijder Datum')
		deletedatumrowbutton.clicked.connect(self.removedatumrow)
		databuttonbox.addWidget(deletedatumrowbutton)

		## Calendar
		calbox = QVBoxLayout()
		inputbox.addLayout(calbox)

		self.cal = QCalendarWidget()
		calbox.addWidget(self.cal)

		caltimebox = QHBoxLayout()
		inputbox.addLayout(caltimebox)

		# middle button box
		startschedulebutton = QPushButton('Maak rooster')
		startschedulebutton.clicked.connect(self.scheduler)
		middlebuttonbox.addStretch(1)
		middlebuttonbox.addWidget(startschedulebutton)
		middlebuttonbox.addStretch(1)

		# output box
		self.outputtable = QTableWidget()
		self.outputtable.setRowCount(0)
		self.outputtable.setColumnCount(0)
		self.outputtable.setHorizontalHeaderLabels(["Datum",])
		outputbox.addWidget(self.outputtable)

		self.setLayout(box)
		self.resize(1100,700)
		self.show()

	def fakedata(self):
		people = ['Albert', 'Ben', 'Casper', 'Daan', 'Elroy', 'Floor', 'Geert', 'Henk', 'Ilias', 'Jonathan', 'Karel', 'Leo', 'Marc', 'Nastrobya']
		for i in range(len(people)):
			self.persontable.insertRow(self.persontable.rowCount())
			self.persontable.setItem(i,0, QTableWidgetItem(people[i]))
		# del self.people

		dates = [datetime(2016, 1, 1), datetime(2016, 1, 2), datetime(2016, 1, 3), datetime(2016, 1, 4), datetime(2016, 1, 5), datetime(2016, 1, 6), datetime(2016, 1, 7)]
		for i in range(len(dates)):
			self.datatable.insertRow(self.datatable.rowCount())
			self.datatable.setItem(i,0, QTableWidgetItem(dates[i].strftime("%d/%m/%Y")))
		# del self.dates

	def scheduler(self):
		self.peoplenum = self.persontable.rowCount()
		self.datesnum = self.datatable.rowCount()

		self.people = []
		for i in range(self.peoplenum):
			self.people.append(self.persontable.item(i,0).text())
		
		self.dates = []
		for i in range(self.datesnum):
			datestr = self.datatable.item(i,0).text()
			self.dates.append(datetime.strptime(datestr, "%d/%m/%Y"))

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
		self.outputtable.setColumnCount(self.numperday+1)
		self.outputtable.setRowCount(self.datesnum)

		HeaderString = "Datum"
		for x in range(5):
			HeaderString += ";Persoon %s" % str(x+1)
		self.outputtable.setHorizontalHeaderLabels(HeaderString.split(';'))

		for i in range(len(self.schedule)):
			self.outputtable.setItem(i,0, QTableWidgetItem(self.dates[i].strftime("%d / %m / %Y  %H:%M")))

			for j in range(len(self.schedule[i])):
				self.outputtable.setItem(i,j+1, QTableWidgetItem(self.people[self.schedule[i][j]]))


	def checkschedule(self):
		return True

	def addpersonrow(self):
		self.persontable.insertRow(self.persontable.rowCount())

	def removepersonrow(self):
		selected = self.persontable.currentRow()
		self.persontable.removeRow(selected)

	def adddatumrow(self):
		self.datatable.insertRow(self.datatable.rowCount())

	def removedatumrow(self):
		selected = self.datatable.currentRow()
		self.datatable.removeRow(selected)

	# def correctschedule(self):

	# define other functions of window class

def main():
	app = QApplication(sys.argv)

	window = Window()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()