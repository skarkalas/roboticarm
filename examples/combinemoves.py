from roboticarm import RoboArm
from roboticarm import Wiimote

def main():
        print("starting...")
        arm = RoboArm()
	wii = Wiimote()
	wii.execute(arm.do)
        #arm.do("gripper open", "wrist down", "elbow down", "shoulder backward", "base clockwise", "led on")
        #arm.do("gripper close", "wrist up", "elbow up", "shoulder forward", "base counter-clockwise", "led off")
        print("terminating...")

if __name__=="__main__":
        main()

