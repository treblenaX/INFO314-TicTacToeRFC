import threading

event = threading.Event()

def myfunction():
    print("Waiting for event to trigger")

    # this will make the function wait until the Event triggered
    event.wait()
    # after triggered
    print("Performing action XYZ now...")

t1 = threading.Thread(target=myfunction)
t1.start()

x = input("Do you want to trigger the event? (y/n)\n")
if x == "y":
    event.set() # trigger the event
