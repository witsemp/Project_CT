from statemachine import StateMachine, State
class RobotPlatform(StateMachine):
    #List of states
    Robot_Idle = State("Waiting to begin sequence", initial=True)
    Lowering_Arm_To_Pickup = State("Lowering arm to pick up wood")
    Gripper_Activation = State("Gripper activation, catching wood")
    Lifing_Arm_W_Wood = State("Lifting up manipulator with wood picked up")
    Rotation_I_Moving_To_E2 = State("Rotating manipulator to place wood, transporter goes to endswitch 2")
    Lowering_Arm_To_Place = State("Lowering arm to place wood")
    Gripper_Deactivation = State("Gripper deactivation, placing wood")
    Lifting_Arm_WO_Wood = State("Lifting up manipulator without wood")
    Rotation_II_Moving_To_E1 = State("Rotating manipulator to pick up wood, transporter goes to endswitch1")
    Endswitch_Error = State("Endswitch 1/2 in error state, manual maintenance required")

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

    def on_wood_detected(self):
        print('Wood detected, lowering arm to pickup wood')
    def on_manipulator_lowered_to_pickup(self):
        print('Manipulator lowered')
    def on_gripper_activated(self):
        print('Manipulator lifted with wood')
    def on_manipulator_lowered_to_place(self):
        print('Manipulator lowered to place')
    def on_rotated_endswitch_2(self):
        print("Manipulator rotated, platform at endswitch 2")
    def on_gripper_deactivated(self):
        print('Suction cups deactivated')
    def on_manipulator_lifted_wo_wood(self):
        print('Manipulator in upper position, without wood')
    def on_rotated_endswitch_1(self):
        print('Manipulator rotated, platform at endswitch 1')

