from statemachine import StateMachine, State
import time
cycleMatrix = [False, False, False, False, False, False, False]
class WoodGripper(StateMachine):

    #List of states
    Gripper_Idle = State("Waiting to begin sequence", initial=True)
    Slide_In_Tray = State("Extending gripper tray")
    Activate_Pressure = State("Lowering an applying pressure to suction cups")
    Gripping_Wood = State("Wood handled by gripper")
    Deactivate_Pressure = State("Deactivating pressure and suction cups")
    Slide_Out_Tray = State("Pulling out gripper tray")
    Emergency_Pressure = State("Emergency - pressure too low to pick up wood")
    Emergency_Extending = State("Tray blocked while extending")
    Emergency_Hiding = State("Tray blocked while hiding")


    #List of transitions
    position1_manipulator_lowered = Gripper_Idle.to(Slide_In_Tray)
    tray_extended = Slide_In_Tray.to(Activate_Pressure)
    pressure_applied = Activate_Pressure.to(Gripping_Wood)
    position2_ready_to_place = Gripping_Wood.to(Deactivate_Pressure)
    pressure_deactivated = Deactivate_Pressure.to(Slide_Out_Tray)
    tray_hidden = Slide_Out_Tray.to(Gripper_Idle)
    tray_blocked_extending = Slide_In_Tray.to(Emergency_Extending)
    tray_unlocked_extending = Emergency_Extending.to(Slide_In_Tray)
    tray_blocked_hiding = Slide_Out_Tray.to(Emergency_Hiding)
    tray_unlocked_hiding = Emergency_Hiding.to(Slide_Out_Tray)
    #Emergency transitions
    pressure_failure_1 = Activate_Pressure.to(Emergency_Pressure)
    pressure_failure_2 = Gripping_Wood.to(Emergency_Pressure)
    gripper_error_handled = Emergency_Pressure.to(Gripper_Idle)
    robot_failure = Gripping_Wood.to(Gripper_Idle)

    def on_position1_manipulator_lowered(self):
        print ('G: Transporter at endswitch 1, manipulator ready to pick up wood')
        time.sleep(1)
    def on_tray_extended(self):
        print ('G: Tray fully extended')
        time.sleep(1)
    def on_pressured_applied(self):
        print ('G: Suction cups gripping wood')
        time.sleep(1)
    def on_position2_ready_to_place(self):
        print ('G: Transporter at endswitch 2, manipulator ready to place wood')
        time.sleep(1)
    def on_pressure_deactivated(self):
        print ('G: Pressure deactivated, suction cups lifted ')
        time.sleep(1)
    def on_tray_hidden(self):
        print ('G: Tray hidden successfully ')
        time.sleep(1)
    def on_tray_blocked_extending(self):
        print ('G: Tray blocked, attempting to unlock ')
        time.sleep(1)
    def on_pressure_failure1(self):
        print('G: Insufficient pressure, manual maintenance required ')
        time.sleep(1)
    def on_pressure_failure2(self):
        print('G: Insufficient pressure, manual maintenance required ')
        time.sleep(1)
    def on_tray_blocked_hiding(self):
        print('G: Hiding tray unsuccessful, attempting to unlock ')
        time.sleep(1)
    def on_gripper_error_handled(self):
        n = input("G: Confirm pressure circuit maintanance (y): ")
        if n == "y":
            print('G: Pressure maintenance confirmed ')
        time.sleep(1)


    def on_robot_failure(self):
        print("G: Restart gripper because of robot error")
        time.sleep(1)


    def process(self):
        licznik = 0

        if licznik == 0:
            self.position1_manipulator_lowered()
            licznik = 1

        while licznik == 1:
            n = input("G: Choose tray behavior: (a - tray extended correctly, b - tray blocked while extending): ")
            if n == 'a':
                self.tray_extended()
                licznik = 2
            if n == 'b':
                self.tray_blocked_extending()
                self.tray_unlocked_extending()
                licznik = 1

        while licznik == 2:
            n = input("Pressure circuit status: (a - correct, b - fault): ")
            if n == "a":
                self.pressure_applied()
                licznik = 3
            if n == "b":
                self.pressure_failure_1()
                licznik = 6

        while licznik == 3:
            n = input("Pressure circuit status after picking wood: (a - correct, b - fault): ")
            if n == "a":
                self.position2_ready_to_place()
                licznik = 4
            if n == "b":
                self.pressure_failure_2()
                licznik = 6

        if licznik == 4:
            self.pressure_deactivated()
            licznik = 5

        while licznik == 5:
            n = input("Choose tray behavior: (a - tray hidden successfully, b - tray blocked while hiding): ")
            if (n == 'a'):
                self.tray_hidden()
                licznik = 0
            if (n == 'b'):
                self.tray_blocked_hiding()
                self.tray_unlocked_hiding()
                licznik = 5

        if licznik == 6:
            self.gripper_error_handled()
            licznik = 0


