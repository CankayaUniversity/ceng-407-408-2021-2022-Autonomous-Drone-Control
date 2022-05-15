#Autopilot communication commands receiving and exporting some necessary data
from pymavlink import mavutil

global battery
global fix_type
global latitude
global longitude
global altitude
global GPS
global message
global velocity

mavlink = mavutil.mavlink_connection('tcp:localhost:5762')
mavlink.wait_heartbeat()


fix_types = {0: "NO GPS", 1: "NO FIX", 2: "2DFIX", 3: "3DFIX", 4: "DGPS", 5: "RTKF",
            6: "RTX FIX", 7: "STATIC", 8: "PPP"}


def mesajiste():

    mavlink.mav.command_long_send(mavlink.target_system, mavlink.target_component,
                                  mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
                                  24, 1, 0, 0, 0, 0, 0)
    # 24 message ı GPS_RAW_INT ID number
    mavlink.mav.command_long_send(mavlink.target_system, mavlink.target_component,
                                  mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
                                  0, mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS, 1, 0, 0, 0, 0, 0)
    # system status informations
    mavlink.mav.command_long_send(mavlink.target_system, mavlink.target_component,
                                  mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
                                  0, mavutil.mavlink.MAVLINK_MSG_ID_STATUSTEXT, 1, 0, 0, 0, 0, 0)
    # mesaj informations

def mesajlar():

    global battery
    global fix_type
    global latitude
    global longitude
    global altitude
    global GPS
    global message
    global velocity

    msg = mavlink.recv_msg()
    if msg:
        #print(msg)

        if msg.get_type() == 'SYS_STATUS':
            battery = msg.to_dict()["voltage_battery"]
            #print(battery)

        if msg.get_type() == 'GPS_RAW_INT':
            fix_type = fix_types[msg.to_dict()["fix_type"]]
            latitude = msg.to_dict()["lat"]
            longitude= msg.to_dict()["lon"]
            altitude = msg.to_dict()["alt"]
            velocity = msg.to_dict()["vel"]
            GPS      = msg.to_dict()["satellites_visible"]
        if msg.get_type() == 'STATUSTEXT':
            message = msg.to_dict()["text"]

def moddegis(mod: int):

    mavlink.mav.set_mode_send(mavlink.target_system,
                            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, mod)

def arm():
    mavlink.mav.command_long_send(mavlink.target_system, mavlink.target_component,
                                mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

def disarm():

    mavlink.mav.command_long_send(mavlink.target_system, mavlink.target_component,
                                  mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0)

def manualConrtol(x:int,y:int,z:int):
    #X axis takes min -1000 max 1000 value
    #Y axis takes min -1000 max 1000 value
    # When the z axis is at 500, it hovers in the air.Below 500 goes down and goes up
    mavlink.mav.manual_control_send(
        mavlink.target_system,
        x,
        y,
        z,
        0,
        0)

def Takeoff(h:int):

    mavlink.mav.command_long_send(mavlink.target_system, mavlink.target_component,
                                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, h)


