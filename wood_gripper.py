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
    pressure_failure = Activate_Pressure.to(Emergency_Pressure)
    gripper_error_handled = Emergency_Pressure.to(Gripper_Idle)


    def on_position1_manipulator_lowered(self):
        print ('Transporter at endswitch 1, manipulator ready to pick up wood')
        time.sleep(1)
    def on_tray_extended(self):
        print ('Tray fully extended')
        time.sleep(1)
    def on_pressured_applied(self):
        print ('Suction cups gripping wood')
        time.sleep(1)
    def on_position2_ready_to_place(self):
        print ('Transporter at endswitch 2, manipulator ready to place wood')
        time.sleep(1)
    def on_pressure_deactivated(self):
        print ('Pressure deactivated, suction cups lifted')
        time.sleep(1)
    def on_tray_hidden(self):
        print ('Tray hidden successfully')
        time.sleep(1)
    def on_tray_blocked_extending(self):
        print ('Tray blocked, attempting to unlock')
        time.sleep(1)
    def on_pressure_failure(self):
        print('Insufficient pressure, manual maintenance required')
        n = input("Confirm pressure circuit maintanance (y): ")
        if n == "y":
            print('Pressure maintenance confirmed')
        time.sleep(1)
    def on_tray_blocked_hiding(self):
        print('Hiding tray unsuccessful, attempting to unlock')
        time.sleep(1)
    def on_gripper_error_handled(self):
        print('Manual maintenance confirmed')
        time.sleep(1)
    def process(self):
        if (cycleMatrix[0] == False and cycleMatrix[1] == False and cycleMatrix[2] == False and cycleMatrix[3] == False and cycleMatrix[4] == False and cycleMatrix[5] == False and cycleMatrix[6] == False):
            self.position1_manipulator_lowered()
            cycleMatrix[0] = True

        if (cycleMatrix[0] == True and cycleMatrix[1] == False and cycleMatrix[2] == False and cycleMatrix[3] == False and cycleMatrix[4] == False and cycleMatrix[5] == False and cycleMatrix[6] == False):
            n = input("Choose tray behavior: (a - tray extended correctly, b - tray blocked while extending) ")
            if n == 'a':
                self.tray_extended()
                cycleMatrix[0] = False
                cycleMatrix[1] = True
            if n == 'b':
                self.tray_blocked_extending()
                self.tray_unlocked_extending()
                cycleMatrix[0] = True

        if (cycleMatrix[0] == False and cycleMatrix[1] == True and cycleMatrix[2] == False and cycleMatrix[3] == False and cycleMatrix[4] == False and cycleMatrix[5] == False and cycleMatrix[6] == False):
            self.pressure_applied()
            cycleMatrix[1] = False
            cycleMatrix[2] = True


        if (cycleMatrix[0] == False and cycleMatrix[1] == False and cycleMatrix[2] == True and cycleMatrix[3] == False and cycleMatrix[4] == False and cycleMatrix[5] == False and cycleMatrix[6] == False):
            self.position2_ready_to_place()
            cycleMatrix[2] = False
            cycleMatrix[3] = True


        if (cycleMatrix[0] == False and cycleMatrix[1] == False and cycleMatrix[2] == False and cycleMatrix[3] == True and cycleMatrix[4] == False and cycleMatrix[5] == False and cycleMatrix[6] == False):
            self.pressure_deactivated()
            cycleMatrix[3] = False
            cycleMatrix[4] = True


        if (cycleMatrix[0] == False and cycleMatrix[1] == False and cycleMatrix[2] == False and cycleMatrix[3] == False and cycleMatrix[4] == True and cycleMatrix[5] == False and cycleMatrix[6] == False):
            n = input("Choose tray behavior: (a - tray hidden successfully, b - tray blocked while hiding")
            if (n == 'a'):
                self.tray_hidden()
                cycleMatrix[4] = False
            if (n == 'b'):
                self.tray_blocked_hiding()
                self.tray_unlocked_hiding()
                cycleMatrix[4] = True




        '''
        if (cycleMatrix[0] == False and cycleMatrix[1] == False and cycleMatrix[2] == False and cycleMatrix[3] == False and cycleMatrix[4] == False and cycleMatrix[5] == True and cycleMatrix[6] == False):
            self.on_tray_extended()
            cycleMatrix[6] = True
            cycleMatrix[5] = False
        '''
        '''
        if (cycleMatrix[0] == False and cycleMatrix[1] == False and cycleMatrix[2] == False and cycleMatrix[3] == False and cycleMatrix[4] == False and cycleMatrix[5] == False and cycleMatrix[6] == True):
            self.on_tray_extended()
            cycleMatrix[6] = False
        '''
