# powersupply.py
#
# Python class for power supplies.

import serial
import time

ps_names = []

class PowerSupply(object):

	def __init__(self, driver, terminal=1):
		driver_dict = self.driver_parser(driver, terminal)
		self.serial_connex=driver_dict['serial_connex']
		self.v_apply=driver_dict['v_apply']
		self.v_ask=driver_dict['v_ask']
		self.idn=driver_dict['idn']
		self.output=driver_dict['output']
		self.term=driver_dict['term']
		self.output_on=driver_dict['output_on']
		self.remote=driver_dict['remote']
		self.error_ask=driver_dict['error_ask']
		self.vmin=driver_dict['vmin']
		self.vmax=driver_dict['vmax']

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
		if not (voltage>=self.vmin and voltage<=self.vmax):
			print 'Voltage out of range!'
			return
		if self.output is not None:
			self.serial_connex.write(self.output + self.term)
			self.serial_connex.readline()
			self.serial_connex.write(self.output_on + self.term)
			self.serial_connex.readline()
		self.serial_connex.write(self.v_apply + ' ' + str(voltage) + self.term)

	def driver_parser(self, driverfile,terminal):
		agilent_1 = {'serial_connex':serial.Serial(port='/dev/ttyr00', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS, timeout=1),
			   'term': '\r\n',
			   'v_ask':'MEAS:VOLT?',
			   'v_apply':'APPL',
			   'idn':'*IDN?',
			   'output':'INST:SEL OUT1',
			   'output_on':'OUTP ON',
			   'remote':'SYST:REM',
			   'error_ask':'SYST:ERR?',
			   'vmin':0,
			   'vmax':35.0
			    }
		agilent_2 = {'serial_connex':serial.Serial(port='/dev/ttyr00', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS, timeout=1),
			   'term': '\r\n',
			   'v_ask':'MEAS:VOLT?',
			   'v_apply':'APPL',
			   'output':'INST:SEL OUT2',
			   'output_on':'OUTP ON',
			   'remote':'SYST:REM',
			   'error_ask':'SYST:ERR?',
			   'vmin':0.0,
			   'vmax':35.0
			    }
		if terminal==1:
			return agilent_1
		if terminal==2:
			return agilent_2
