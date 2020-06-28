from gui import main
from threading import Thread
from multiprocessing import Process
from pitch_detection import TunerStream
from time import sleep

if __name__ == "__main__":
    #main()
    stream = TunerStream(44100)
    reader_thread = Thread(target = lambda: stream.mainloop(), daemon=True)
    reader_thread.start()
    stream.resume()
    while True:
        print(stream.peek())
        sleep(0.5)
