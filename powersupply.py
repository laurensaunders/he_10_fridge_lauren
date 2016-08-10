# powersupply.py
#
# Python class for power supplies connected via serial ports.

import serial
import time

class PowerSupply(object):

	def __init__(self, driver, terminal=1):
		driver_dict = self.driver_parser(driver,terminal)
		if driver_dict['parity']==odd:
			parity=serial.PARITY_ODD
		if driver_dict['parity']==even:
			parity=serial.PARITY_EVEN
		if driver_dict['parity']==none:
			parity=serial.PARITY_NONE
		if driver_dict['stopbits']==1:
			stopbits=serial.STOPBITS_ONE
		if driver_dict['stopbits']==2:
			stopbits=serial.STOPBITS_TW0
		if driver_dict['bytesize']==5:
			bytesize=serial.FIVEBITS
		if driver_dict['bytesize']==6:
			bytesize=serial.SIXBITS
		if driver_dict['bytesize']==7:
			bytesize=serial.SEVENBITS
		if driver_dict['bytesize']==8:
			bytesize=serial.EIGHTBITS
		self.serial_connex=serial.Serial(port=str(driver_dict['port']), baudrate=driver_dict['baudrate'], parity=parity, stopbits=stopbits, bytesize=bytesize, timeout=driver_dict['timeout'])
		self.v_apply=str(driver_dict['v_apply'])
		self.v_ask=str(driver_dict['v_ask'])
		self.idn=str(driver_dict['idn'])
		self.term=driver_dict['term']
		self.output_on=str(driver_dict['output_on'])
		self.remote=str(driver_dict['remote'])
		self.error_ask=str(driver_dict['error_ask'])
		self.vmin=str(driver_dict['vmin'])
		self.vmax=str(driver_dict['vmax'])
		pass

	# Identification command
	def who_am_i(self):
		self.serial_connex.write(self.idn + self.term)
		return self.serial_connex.readline()

	# Set the power supply to operate remotely
	def remote_set(self):
		if self.remote is not None:
			self.serial_connex.write(self.remote + self.term)
		else:
			pass

	# Ask the power supply for an error message
	def error(self):
		self.serial_connex.write(self.error_ask + self.term)
		return self.serial_connex.readline()

	# Turn a particular output on and do nothing else
	def turn_output_on(self):
		if self.output_on==None:
			pass
		else:
			self.serial_connex.write(self.output_on + self.term)

	# Read voltages from the power supply
	def read_voltage(self):
		if self.output is not None:
			self.serial_connex.write(self.output + self.term)
			self.serial_connex.readline()
			self.serial_connex.write(self.output_on + self.term)
			self.serial_connex.readline()
		self.serial_connex.write(self.v_ask + self.term)
		x=self.serial_connex.readline()
		return x

	# Set voltages
	def set_voltage(self, voltage):
		if not (abs(voltage)>=self.vmin and abs(voltage)<=self.vmax):
			print 'Voltage out of range!'
			return
		if self.output is not None:
			self.serial_connex.write(self.output_on + self.term)
			self.serial_connex.readline()
		self.serial_connex.write(self.v_apply + ' ' + str(voltage) + self.term)

	# Program draws the driver dictionaries from driver files.  Currently test files, need to update to actual driver files.
	def driver_parser(self,driverfile,terminal):
		if terminal==1:
			out1 = {}
			with open('test_1.txt','r') as f:
				for line in f:
					listedline = line.strip().decode('unicode-escape').split('=')
					if len(listedline)>1:
						out1[listedline[0]] = listedline[1]
				f.close()
				return out1
		if terminal==2:
			out2 = {}
			with open('test_2.txt','r') as f:
				for line in f:
					listedline = line.strip().split('=')
					if len(listedline)>1:
						out2[listedline[0]=listedline[1]]
