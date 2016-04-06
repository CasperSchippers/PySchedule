import sys
from PyQt4 import QtGui, QtCore

# import time
from datetime import date
import random
import math

class Window(QtGui.QWidget):
	def __init__(self):
		super(Window, self).__init__()

		self.initUI()

	def initUI(self):
		# define GUI here
		self.show()
		self.scheduler()

	def scheduler(self):
		print("scheduler")
		self.dates = [date(2016, 1, 1), date(2016, 1, 2), date(2016, 1, 3), date(2016, 1, 4), date(2016, 1, 5), date(2016, 1, 6), date(2016, 1, 7)]
		self.datesnum = len(self.dates)
		self.people = ['Albert', 'Ben', 'Casper', 'Daan', 'Elroy', 'Floor', 'Geert', 'Henk', 'Ilias', 'Jonathan', 'Karel', 'Leo', 'Marc', 'Nastrobya']
		self.peoplenum = len(self.people)
		self.numperday = 5

		PickingList = [x for x in range(self.peoplenum)] * math.ceil((self.numperday*self.datesnum)/self.peoplenum)
		print(PickingList)

		# Make a list of an integer times all people so that items on that list > total number of places and randomly pick (and remove) a person from that list for each moment
		# then check if same person is not left over more than once



		self.schedule = [x[:] for x in [[[None]]*self.numperday]*self.datesnum]
		
		# initial filling of the schedule
		for dayID in range(self.datesnum):
			for placeID in range(self.numperday):
				i = random.randrange(len(PickingList))
				print(i)
				while self.schedule[dayID].count(PickingList[i]) != 0:
					i = random.randrange(len(PickingList))
					print(i)
				self.schedule[dayID][placeID] = PickingList[i]
				del PickingList[i]
				print(PickingList)
		print(self.schedule)
		check = self.checkschedule()
		if check:
			print('good')
		elif not check:
			print('bad')

	def checkschedule(self):
		return True

	# def correctschedule(self):

	# define other functions of window class

def main():
	app = QtGui.QApplication(sys.argv)

	window = Window()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()