from xgolib import XGO
import time
dog = XGO("xgomini")
time.sleep(2)
dog.reset()
def arm_dance():
    try:
        for i in range(5):
            dog.leg(1, [0, -25, 75])
            dog.leg(2, [0, -25, 75])
            dog.leg(3, [0, -20, 70])
            dog.leg(4, [0, -20, 70])
            time.sleep(0.3)
            dog.leg(1, [0, 5, 95])
            dog.leg(2, [0, 5, 95])
            dog.leg(3, [0, 5, 95])
            dog.leg(4, [0, 5, 95])
            time.sleep(0.3)
            dog.reset()

        for _ in range(8):
            dog.leg(1, [30, 0, 90])
            dog.leg(2, [30, 0, 90])
            time.sleep(0.4)
            dog.leg(1, [-20, 0, 90])
            dog.leg(2, [-20, 0, 90])
            time.sleep(0.4)

        for _ in range(8):
            dog.leg(1, [0, 0, 110])
            dog.leg(2, [0, 0, 110])
            time.sleep(0.4)
            dog.leg(1, [0, 0, 75])
            dog.leg(2, [0, 0, 75])
            time.sleep(0.4)
            
        for _ in range(6):
            dog.leg(1, [0, -20, 90])
            dog.leg(2, [0, 20, 90])
            time.sleep(0.5)
            dog.leg(1, [0, 20, 90])
            dog.leg(2, [0, -20, 90])
            time.sleep(0.5)

        for _ in range(6):
            dog.leg(1, [35, 0, 100])
            dog.leg(2, [0, 0, 90])
            time.sleep(0.5)
            dog.leg(1, [0, 0, 90])
            dog.leg(2, [35, 0, 100])
            time.sleep(0.5)

        dog.leg(1, [20, -15, 90])  
        dog.leg(2, [20, -15, 90])  
        time.sleep(1)
        
        for _ in range(3):
            dog.leg(1, [0, 0, 80])
            dog.leg(2, [0, 0, 80])
            dog.leg(3, [0, 0, 80])
            dog.leg(4, [0, 0, 80])
            time.sleep(0.3)
            dog.leg(1, [0, 0, 100])
            dog.leg(2, [0, 0, 100])
            dog.leg(3, [0, 0, 100])
            dog.leg(4, [0, 0, 100])
            time.sleep(0.3)
        dog.reset()
        time.sleep(1)

        dog.leg(1, [20, 10, 80])
        dog.leg(2, [20, -10, 80])
        time.sleep(2)

        dog.reset()


    except Exception as e:
        print(f"Error:{e}")
    finally:
        dog.reset()

if __name__ == "__main__":
    arm_dance()