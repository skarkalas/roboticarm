import usb.core, usb.util, time, sys, re

class RoboArm:
	'This is a class that represents the notion of a robotic arm'

	#class variable to define action command codes - these codes are common to all robotic arms
	command_codes = {}
	command_codes["gripper unchanged"] = '00'
	command_codes["gripper open"] = '10'
	command_codes["gripper close"] = '01'
	command_codes["wrist unchanged"] = '00'
	command_codes["wrist down"] = '10'
	command_codes["wrist up"] = '01'
	command_codes["elbow unchanged"] = '00'
	command_codes["elbow down"] = '10'
	command_codes["elbow up"] = '01'
	command_codes["shoulder unchanged"] = '00'
	command_codes["shoulder forward"] = '10'
	command_codes["shoulder backward"] = '01'
	command_codes["base unchanged"] = '00'
	command_codes["base clockwise"] = '01'
	command_codes["base counter-clockwise"] = '10'
	command_codes["led off"] = '00'
	command_codes["led on"] = '01'

	#class method to retrieve action command codes based on symbolic commands
	@classmethod
	def get_command_code(cls, key):
		def get_key_stripped():
			#remove all whitespace characters before, after and leave only a space in between
			return re.sub('\s+', ' ', key).strip()
		key = get_key_stripped()	
		code = cls.command_codes.get(key, None)
		if code is None:
			raise ValueError("invalid command")
		return (key.split()[0], code)

	#constructor defaults to the OWI-535 (Maplin) Robotic Arm but could be used with other devices as well
	def __init__(self, id_vendor=0x1267, id_product=0, duration=1):
		self.id_vendor = id_vendor
		self.id_product = id_product
		self.duration = duration		#sleep time for smooth operation of motors

		#get a reference to the robotic arm
		self.robo_arm = usb.core.find(idVendor=self.id_vendor, idProduct=self.id_product)
		
		#if arm cannot be found stop with an exception
		if self.robo_arm is None:
			raise ValueError("Arm not found")

	#method to display device configuration
	def display_configuration(self):
		for configuration in self.robo_arm:
			sys.stdout.write("configuration " + str(configuration.bConfigurationValue) + "\n")
			sys.stdout.write("----------------- \n")
			for interface in configuration:
				sys.stdout.write("\tinterface " + \
				str(interface.bInterfaceNumber) + \
				"," + \
				str(interface.bAlternateSetting) + \
				"\n")
				sys.stdout.write("\t----------------- \n")
				for endpoint in interface:
					sys.stdout.write("\t\tendpoint " + \
					str(endpoint.bEndpointAddress) + "\n")
					sys.stdout.write("\t\t----------------- \n")

	#method to process requested action(s)
	def do(self, *args):

		#function to unify requested actions into a single command
		def get_command():

			#set default values - unpack tuples
			command_values = {}
			motor, command = RoboArm.get_command_code("gripper unchanged")
			command_values[motor] = command
			motor, command = RoboArm.get_command_code("wrist unchanged")
			command_values[motor] = command
			motor, command = RoboArm.get_command_code("elbow unchanged")
			command_values[motor] = command
			motor, command = RoboArm.get_command_code("shoulder unchanged")
			command_values[motor] = command
			motor, command = RoboArm.get_command_code("base unchanged")
			command_values[motor] = command
			motor, command = RoboArm.get_command_code("led off")
			command_values[motor] = command

			#update values with arguments
			for arg in args:
				motor, command = RoboArm.get_command_code(arg)
				command_values[motor] = command
				
			shoulder_elbow_wrist_gripper = ""
			shoulder_elbow_wrist_gripper += command_values.get("shoulder")
			shoulder_elbow_wrist_gripper += command_values.get("elbow")
			shoulder_elbow_wrist_gripper += command_values.get("wrist")
			shoulder_elbow_wrist_gripper += command_values.get("gripper")

			base = command_values.get("base")
			
			led = command_values.get("led")

			full_command = [int(shoulder_elbow_wrist_gripper, 2), int(base, 2), int(led, 2)]
			return full_command

		#if arm is not available stop with an exception
		if self.robo_arm is None:
			raise ValueError("Arm not available")			
			
		#get full command
		command = get_command()
		print("*** executing --> " + ",".join(args) + " (" + ",".join(str(e) for e in command) + ")")

		#execute command
		self.robo_arm.ctrl_transfer(0x40,6,0x100,0,command,1000)

		#suspend execution for some time - give time to the move to complete
		time.sleep(self.duration)

		#stop move - set everything to unchanged apart from led
		self.robo_arm.ctrl_transfer(0x40,6,0x100,0,[0,0,command[2]],1000)
