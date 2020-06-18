from subprocess import Popen, PIPE
from time import sleep
from bridge.PitchDetector import PitchDetector 
import sys
import asyncio
from time import time, sleep

async def main():
    notes = []
    async def read_all():
        proc = await asyncio.create_subprocess_exec("./PitchDetection/PitchDetection", stdout=PIPE)
        while not proc.stdout.at_eof():
            notes.append((await proc.stdout.readline(),time()))
    async def display_pitch():
        while True:
            #sys.stdout.write("\b"*8)
            #sys.stdout.flush()
            if len(notes) == 0:
                print("empty   ")
            elif time() - notes[-1][1] <= 1:
                print("note: %s" % notes[-1][0][0:2])
            else:
                print("no note ")

            await asyncio.sleep(0.1)
    try:
        await asyncio.wait({display_pitch(), read_all()}, return_when=asyncio.FIRST_EXCEPTION)
    except KeyboardInterrupt:
        print()
        return
    #p = PitchDetector()
    #p.start()
    #print("after start")
    #sleep(2)
    #print("after sleep")
    #p.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()
