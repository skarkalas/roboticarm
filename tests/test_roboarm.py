from roboticarm import RoboArm

def main():
        print("start executing main")
        arm = RoboArm()
        arm.do("gripper open", "wrist down", "elbow down", "shoulder backward", "base clockwise", "led on")
        arm.do("gripper close", "wrist up", "elbow up", "shoulder forward", "base counter-clockwise", "led off")
        print("stop executing main")

if __name__=="__main__":
        main()

