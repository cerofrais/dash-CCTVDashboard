import random
import time
for i in range(50):
    file=open('realtime.txt','a')
    file.write(str(random.randint(0,10))+','+str(random.randint(0,10))+','+str(random.randint(0,10))+','+str(random.randint(0,10))+'\n')
    file.close()
    time.sleep(1)
