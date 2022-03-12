# https://www.youtube.com/watch?v=e05Hkz-W_aQ&list=PL7yh-TELLS1F3KytMVZRFO-xIo_S2_Jg1&index=3

import threading


def hello_world():
    print("Hello world")


t_helloworld = threading.Thread(target=hello_world())
t_helloworld.run() #Starter funksjon i thread

def function1():
    for i in range(100):
        print("one")

def function2():
    for i in range(100):
        print("two")

function1()
function2()

t1 = threading.Thread(target=function1())
t2 = threading.Thread(target=function2())

t1.start() # Start runs t1 & t2 in parallel
t2.start()

t1.join() # Wait for t1 to finnish before running print("Another text")

print("Another text")