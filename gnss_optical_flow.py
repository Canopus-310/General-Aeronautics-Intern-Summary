

# fusing inputs from GNSS, NRA24 AND OPTICAL FLOW SENSOR, BAROMETER, IMU into an EKF

# EVERY 100 MILISEC. - CONDUCT CHECKS for the signals below:- 
  # 3 signals - to be cross checked 
    # 1. IF gnss alt vs NRA24 ? 1.5 - FLAG
    # 2. IF GNSS vs IMU > 2 m/s for 10 cycles - FLAG
    # 3. IF gnss signal quality below threshold - FLAG
   
    # IF ANY 2 FLAGGINGS OUT OF 3 - TRIGGER GNSS FAILSAFE:
        # START LOGGING DATA
        # cut-off spraying immediately

        # Velocity calculations now primarily done by - Optical Flow meter

        # Altitude calculations now primary calculated by - NRA24
            # if height < 3 metres: 
                #climb to 5 metres AGL at the speed of 2 m/s using baro and IMU
            #ELSE: 
                #continue ahead
        # opt_qua quality check 
        # if opt_qua > 100:
            # use RTL dead reckoning with the help of optical flow
                # when near - descend at 0.5 m/s or the given descension velocity speed
        # else:
            # climb to 20 m AGL with the help of IMU + BARO at 2 m/s and hold
            # check for GNSS and optical flow: - 
                # if GNSS works:
                    # GPS RTL standard mode:- 
                # elif Only optical flow:
                    # dead reckoning through optical flow
                # else: 
                    # keep hovering and trigger alarm for manual intervention
        # log the data into GA hub and mission planner
        #return

            




            



