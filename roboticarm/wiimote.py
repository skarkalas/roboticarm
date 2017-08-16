import cwiid, time

class Wiimote:
	'This is a class that represents wii devices'

	#class variable to define action command codes
	command_codes = {}
	command_codes[cwiid.BTN_B] = "gripper open"
	command_codes[cwiid.BTN_A] = "gripper close"
	command_codes[cwiid.BTN_MINUS] = "wrist down"
	command_codes[cwiid.BTN_PLUS] = "wrist up"
	command_codes[cwiid.BTN_2] = "elbow down"
	command_codes[cwiid.BTN_1] = "elbow up"
	command_codes[cwiid.BTN_UP] = "shoulder forward"
	command_codes[cwiid.BTN_DOWN] = "shoulder backward"
	command_codes[cwiid.BTN_RIGHT] = "base clockwise"
	command_codes[cwiid.BTN_LEFT] = "base counter-clockwise"
	#command_codes[] = "led off"
	#command_codes[] = "led on"

	#class method to retrieve symbolic action command for arm based on wii state
	@classmethod
	def get_command_code(cls, key):
		code = cls.command_codes.get(key, None)
		if code is None:
			raise ValueError("invalid command")
		return code	
	
	#constructor
	def __init__(self):
		#attempt to connect
		print('Press 1 and 2 to connect to wiimote')
		self.wii = None
		while(self.wii == None):
			try:
				print('Establishing connection... ')
				self.wii = cwiid.Wiimote()
			except RuntimeError:
				print('Error connecting to the wiimote.')
				answer = input('Press y to try again?').lower()
				if(answer != 'y'):
					break
		#if there is no connection return
		if(self.wii == None):
			print('Connection is not established... ')
			return

		#rumble to indicate that a connection is established
		self.wii.rumble = 1
		print('Connection established... ')
		time.sleep(1)
		self.wii.rumble = 0
		print('Press home button to quit')

	#method to execute commands
	def execute(self, do):
		#set button read mode
		self.wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

		while(True):
			buttons = self.wii.state['buttons']
			if(buttons & cwiid.BTN_HOME):
				print('Connection terminated... ')
				break

			command = ''
			
			if(buttons & cwiid.BTN_A):
				command = Wiimote.get_command_code(cwiid.BTN_A)
			elif(buttons & cwiid.BTN_B):
				command = Wiimote.get_command_code(cwiid.BTN_B)
			elif (buttons & cwiid.BTN_1):
				command = Wiimote.get_command_code(cwiid.BTN_1)
			elif (buttons & cwiid.BTN_2):
				command = Wiimote.get_command_code(cwiid.BTN_2)
			elif (buttons & cwiid.BTN_MINUS):
				command = Wiimote.get_command_code(cwiid.BTN_MINUS)
			elif (buttons & cwiid.BTN_PLUS):
				command = Wiimote.get_command_code(cwiid.BTN_PLUS)
			elif (buttons & cwiid.BTN_UP):
				command = Wiimote.get_command_code(cwiid.BTN_UP)
			elif (buttons & cwiid.BTN_DOWN):
				command = Wiimote.get_command_code(cwiid.BTN_DOWN)
			elif (buttons & cwiid.BTN_LEFT):
				command = Wiimote.get_command_code(cwiid.BTN_LEFT)
			elif (buttons & cwiid.BTN_RIGHT):
				command = Wiimote.get_command_code(cwiid.BTN_RIGHT)

			if(command != '' and do is not None):
				do(command)

			time.sleep(0.5)
