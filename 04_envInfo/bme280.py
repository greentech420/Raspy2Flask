#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from smbus import SMBus
import time

class BME280:
	def __init__(self):
	
		self.bus_number  = 1
		self.i2c_address = 0x76

		self.bus = SMBus(self.bus_number)

		self.digT = []
		self.digP = []
		self.digH = []

		self.t_fine = 0.0
		
		self.osrs_t = 1			#Temperature oversampling x 1
		self.osrs_p = 1			#Pressure oversampling x 1
		self.osrs_h = 1			#Humidity oversampling x 1
		self.mode   = 3			#Normal mode
		self.t_sb   = 5			#Tstandby 1000ms
		self.filter = 0			#Filter off
		self.spi3w_en = 0			#3-wire SPI Disable

		self.ctrl_meas_reg = (self.osrs_t << 5) | (self.osrs_p << 2) | self.mode
		self.config_reg    = (self.t_sb << 5) | (self.filter << 2) | self.spi3w_en
		self.ctrl_hum_reg  = self.osrs_h

		self.writeReg(0xF2,self.ctrl_hum_reg)
		self.writeReg(0xF4,self.ctrl_meas_reg)
		self.writeReg(0xF5,self.config_reg)
		
	def writeReg(self,reg_address, data):
		self.bus.write_byte_data(self.i2c_address,reg_address,data)
	
	def get_calib_param(self):
		self.calib = []
		
		for i in range (0x88,0x88+24):
			self.calib.append(self.bus.read_byte_data(self.i2c_address,i))
		self.calib.append(self.bus.read_byte_data(self.i2c_address,0xA1))
		for i in range (0xE1,0xE1+7):
			self.calib.append(self.bus.read_byte_data(self.i2c_address,i))

		self.digT.append((self.calib[1] << 8) | self.calib[0])
		self.digT.append((self.calib[3] << 8) | self.calib[2])
		self.digT.append((self.calib[5] << 8) | self.calib[4])
		self.digP.append((self.calib[7] << 8) | self.calib[6])
		self.digP.append((self.calib[9] << 8) | self.calib[8])
		self.digP.append((self.calib[11]<< 8) | self.calib[10])
		self.digP.append((self.calib[13]<< 8) | self.calib[12])
		self.digP.append((self.calib[15]<< 8) | self.calib[14])
		self.digP.append((self.calib[17]<< 8) | self.calib[16])
		self.digP.append((self.calib[19]<< 8) | self.calib[18])
		self.digP.append((self.calib[21]<< 8) | self.calib[20])
		self.digP.append((self.calib[23]<< 8) | self.calib[22])
		self.digH.append( self.calib[24] )
		self.digH.append((self.calib[26]<< 8) | self.calib[25])
		self.digH.append( self.calib[27] )
		self.digH.append((self.calib[28]<< 4) | (0x0F & self.calib[29]))
		self.digH.append((self.calib[30]<< 4) | ((self.calib[29] >> 4) & 0x0F))
		self.digH.append( self.calib[31] )
		
		for i in range(1,2):
			if self.digT[i] & 0x8000:
				self.digT[i] = (-self.digT[i] ^ 0xFFFF) + 1

		for i in range(1,8):
			if self.digP[i] & 0x8000:
				self.digP[i] = (-self.digP[i] ^ 0xFFFF) + 1

		for i in range(0,6):
			if self.digH[i] & 0x8000:
				self.digH[i] = (-self.digH[i] ^ 0xFFFF) + 1  

	
	def readData(self):

		self.digT.clear()
		self.digP.clear()
		self.digH.clear()
		
		self.get_calib_param()
		self.data = []
		for i in range (0xF7, 0xF7+8):
			self.data.append(self.bus.read_byte_data(self.i2c_address,i))
		self.pres_raw = (self.data[0] << 12) | (self.data[1] << 4) | (self.data[2] >> 4)
		self.temp_raw = (self.data[3] << 12) | (self.data[4] << 4) | (self.data[5] >> 4)
		self.hum_raw  = (self.data[6] << 8)  |  self.data[7]
		
		self.t = float(self.compensate_T(self.temp_raw))
		self.p = float(self.compensate_P(self.pres_raw))
		self.h = float(self.compensate_H(self.hum_raw))
		return self.t,self.p,self.h

	def compensate_P(self,adc_P):
		#global  t_fine
		self.pressure = 0.0
		
		self.v1 = (self.t_fine / 2.0) - 64000.0
		self.v2 = (((self.v1 / 4.0) * (self.v1 / 4.0)) / 2048) * self.digP[5]
		self.v2 = self.v2 + ((self.v1 * self.digP[4]) * 2.0)
		self.v2 = (self.v2 / 4.0) + (self.digP[3] * 65536.0)
		self.v1 = (((self.digP[2] * (((self.v1 / 4.0) * (self.v1 / 4.0)) / 8192)) / 8)  + ((self.digP[1] * self.v1) / 2.0)) / 262144
		self.v1 = ((32768 + self.v1) * self.digP[0]) / 32768
		
		if self.v1 == 0:
			return 0
		self.pressure = ((1048576 - adc_P) - (self.v2 / 4096)) * 3125
		if self.pressure < 0x80000000:
			self.pressure = (self.pressure * 2.0) / self.v1
		else:
			self.pressure = (self.pressure / self.v1) * 2
		self.v1 = (self.digP[8] * (((self.pressure / 8.0) * (self.pressure / 8.0)) / 8192.0)) / 4096
		self.v2 = ((self.pressure / 4.0) * self.digP[7]) / 8192.0
		self.pressure = self.pressure + ((self.v1 + self.v2 + self.digP[6]) / 16.0)  

		#print "pressure : %7.2f hPa" % (pressure/100)
		if (self.pressure/100)>=1000.0:
			return "%7.2f" % (self.pressure/100)
		else:
			return "%6.2f" % (self.pressure/100)
		
	def compensate_T(self,adc_T):
		#global t_fine
		self.v1 = (adc_T / 16384.0 - self.digT[0] / 1024.0) * self.digT[1]
		self.v2 = (adc_T / 131072.0 - self.digT[0] / 8192.0) * (adc_T / 131072.0 - self.digT[0] / 8192.0) * self.digT[2]
		self.t_fine = self.v1 + self.v2
		self.temperature = self.t_fine / 5120.0
		#print "temp : %-6.2f ℃" % (temperature) 

		
		return "%.2f" % (self.temperature)

	def compensate_H(self,adc_H):
		#global t_fine
		self.var_h = self.t_fine - 76800.0
		if self.var_h != 0:
			self.var_h = (adc_H - (self.digH[3] * 64.0 + self.digH[4]/16384.0 * self.var_h)) * (self.digH[1] / 65536.0 * (1.0 + self.digH[5] / 67108864.0 * self.var_h * (1.0 + self.digH[2] / 67108864.0 * self.var_h)))
		else:
			return 0
		self.var_h = self.var_h * (1.0 - self.digH[0] * self.var_h / 524288.0)
		if self.var_h > 100.0:
			self.var_h = 100.0
		elif self.var_h < 0.0:
			self.var_h = 0.0
		#print "hum : %6.2f ％" % (var_h)
		return "%.2f" % (self.var_h)

if __name__ == "__main__":
	bme = BME280()
	
	t,p,h = bme.readData()
	
	print(f"Tempreture:{t}[*C]")
	print(f"Pressuer:{p}[hPa]")
	print(f"Humidity:{h}[%]")
