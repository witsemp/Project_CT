from statemachine import StateMachine, State
import time

class RobotPlatform(StateMachine):
    #List of states
    Robot_Idle = State("Waiting to begin sequence ", initial=True)
    Lowering_Arm_To_Pickup = State("Lowering arm to pick up wood ")
    Gripper_Activation = State("Gripper activation, catching wood ")
    Lifing_Arm_W_Wood = State("Lifting up manipulator with wood picked up ")
    Rotation_I_Moving_To_E2 = State("Rotating manipulator to place wood, transporter goes to endswitch 2 ")
    Lowering_Arm_To_Place = State("Lowering arm to place wood ")
    Gripper_Deactivation = State("Gripper deactivation, placing wood ")
    Lifting_Arm_WO_Wood = State("Lifting up manipulator without wood ")
    Rotation_II_Moving_To_E1 = State("Rotating manipulator to pick up wood, transporter goes to endswitch1 ")
    Endswitch_Error = State("Endswitch 1/2 in error state, manual maintenance required ")

    # List of transitions
    wood_detected = Robot_Idle.to(Lowering_Arm_To_Pickup)
    manipulator_lowered_to_pickup = Lowering_Arm_To_Pickup.to(Gripper_Activation)
    gripper_activated = Gripper_Activation.to(Lifing_Arm_W_Wood)
    manipulator_lifted_w_wood = Lifing_Arm_W_Wood.to(Rotation_I_Moving_To_E2)
    rotated_endswitch_2 = Rotation_I_Moving_To_E2.to(Lowering_Arm_To_Place)
    manipulator_lowered_to_place = Lowering_Arm_To_Place.to(Gripper_Deactivation)
    gripper_deactivated = Gripper_Deactivation.to(Lifting_Arm_WO_Wood)
    manipulator_lifted_wo_wood = Lifting_Arm_WO_Wood.to(Rotation_II_Moving_To_E1)
    rotated_endswitch_1 = Rotation_II_Moving_To_E1.to(Robot_Idle)
    endswitch2_no_confirmation = Rotation_I_Moving_To_E2.to(Rotation_I_Moving_To_E2)
    endswitch1_no_confirmation = Rotation_II_Moving_To_E1.to(Rotation_II_Moving_To_E1)
    endswitch2_error = Rotation_I_Moving_To_E2.to(Endswitch_Error)
    endswitch1_error = Rotation_II_Moving_To_E1.to(Endswitch_Error)
    endswitch_error_confirmed = Endswitch_Error.to(Robot_Idle)

    gripper_error = Gripper_Activation.to(Robot_Idle)

    def on_wood_detected(self):
        print('Wood detected, lowering arm to pickup wood ')
        time.sleep(1)
    def on_manipulator_lowered_to_pickup(self):
        print('Manipulator lowered ')
        time.sleep(1)
    def on_gripper_activated(self):
        print('Manipulator lifted with wood ')
        time.sleep(1)
    def on_manipulator_lowered_to_place(self):
        print('Manipulator lowered to place ')
        time.sleep(1)
    def on_rotated_endswitch_2(self):
        print("Manipulator rotated, platform at endswitch 2 ")
        time.sleep(1)
    def on_gripper_deactivated(self):
        print('Suction cups deactivated')
        time.sleep(1)
    def on_manipulator_lifted_wo_wood(self):
        print('Manipulator in upper position, without wood ')
        time.sleep(1)
    def on_rotated_endswitch_1(self):
        print('Manipulator rotated, platform at endswitch 1 ')
        time.sleep(1)
    def on_endswitch2_no_confirmation(self):
        print("Awaiting confirmation from endswitch 2 ")
        time.sleep(1)
    def on_endswitch1_no_confirmation(self):
        print("Awaiting confirmation from endswitch 1 ")
        time.sleep(1)
    def on_endswitch2_error(self):
        print("No confirmation from endswitch 2 ")
        time.sleep(1)
    def on_endswitch1_error(self):
        print("No confirmation from endswitch 1 ")
        time.sleep(1)
    def on_endswitch_error_confirmed(self):
        n=input("Endswitch repair and confirmation needed (y) - confirm maintenance: ")
        if n == "y":
            print("Maintenance confirmed ")
        time.sleep(1)

    def on_gripper_error(self):
        print("Restart robot because of gripper error")
        time.sleep(1)

    def process(self):
        counter = 0
        if counter == 0:
            self.wood_detected()
            counter = 10
        if counter == 10:
            self.manipulator_lowered_to_pickup()
            counter = 20
        if counter == 20:
            self.gripper_activated()
            counter = 30
        if counter == 30:
            self.manipulator_lifted_w_wood()
            counter = 40
        while counter == 40:
            n = input("Platform at endswitch 2? (y/n/e): ")
            if n == "y":
                self.rotated_endswitch_2()
                counter = 50
            if n == "n":
                self.endswitch2_no_confirmation()
                counter = 40
            if n == "e":
                self.endswitch2_error()
                counter = 90
        if counter == 50:
            self.manipulator_lowered_to_place()
            counter = 60
        if counter == 60:
            self.gripper_deactivated()
            counter = 70
        if counter == 70:
            self.manipulator_lifted_wo_wood()
            counter = 80
        while counter == 80:
            n = input("Platform at endswitch 1? (y/n/e): ")
            if n == "y":
                self.rotated_endswitch_1()
                counter = 0
            if n == "n":
                self.endswitch1_no_confirmation()
                counter = 80
            if n == "e":
                self.endswitch1_error()
                counter = 90
        if counter == 90:
            self.endswitch_error_confirmed()
            counter = 0
