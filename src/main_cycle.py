import tkinter as tk
import multiprocessing, time, sys, signal
from pyghthouse.ph import Pyghthouse
from local_display import LocalDisplay, start_local_display
from mp_firework import Fireworks
from mp_bouncers import BounceAnimation as Bouncers
from mp_lavablob import Lavablobs
from mp_rgbtest import RgbTest
from mp_rain import RainAnimation
from mp_rebound import ReboundAnimation
from mp_diffraction import DiffAnimation
from mp_conway import GameOfLife
from stopwatch import Stopwatch
from color_functions import interpolate, cycle

class AnimationController():   
    def __init__(self, time_per_anim, local = False, remote = True) -> None:
        self.keep_going = True
        self.displayqueue = None
        self.name = "JhController"
        signal.signal(signal.SIGINT, self._handle_sigint)
        self.run(time_per_anim)
        self.local = local
        self.remote = local

    @staticmethod     
    def read_auth(filename="auth.txt"):
        with open(filename) as src:
            username, token = None, None
            lines = src.readlines()
            for line in lines:
                line = line.split(":")
                if len(line) == 2:
                    match line[0].strip().lower():
                        case 'name':
                            username = line[1].strip()
                            print(f"Username read from file: {username}")
                        case 'username':
                            username = line[1].strip()
                            print(f"Username read from file: {username}")
                        case 'token':
                            token = line[1].strip()
                            print(f"Token read from file: {token}")
                        case _:
                            print(f"Unrecognized Key: '{line[0]}'")
            if not username or not token:
                print(f"Error: File {filename} is incomplete!")
            return username, token
        
    def send_frame(self, ph: Pyghthouse, image: list, factor: float):
        img = ph.empty_image()
        if self.remote:
            for x in range(min(len(img), len(image[0]))):
                for y in range(min(len(img[0]), len(image))):
                    img[x][y] = interpolate(image[y][x], img[x][y], factor) if factor < 1.0 else image[y][x]
            ph.set_image(img)
        if self.local and self.displayqueue:
            self.displayqueue.put_nowait(img)
        
    def _handle_sigint(self, signum, frame):
        print("Ctrl+C detected. Stopping animations...")
        self.keep_going = False
        
    ##### RUN METHOD #####
    def run(self, time_per_anim):
        
        if self.remote:
            username, token = self.read_auth()
            if not username or not token:
                exit(1)
            ph = Pyghthouse(username, token)
            ph.start()
            
        animations = [
                    GameOfLife(),
                    Fireworks(), 
                    Lavablobs(),
                    #RgbTest(), 
                    RainAnimation(), 
                    ReboundAnimation(), 
                    DiffAnimation(), 
                    Bouncers()]
        
        fps = 60
        
        
        anim_timer = Stopwatch()
        frametimer = Stopwatch() 
        update_interval = 1/(fps)
        n = 0
        if self.local:
            self.displayqueue = multiprocessing.Queue()
            display_process = multiprocessing.Process(target=start_local_display, args=(self.displayqueue,fps))
            display_process.start()
        while self.keep_going:
            framequeue = multiprocessing.Queue()
            commandqueue = multiprocessing.Queue()
            anim_timer.set(time_per_anim)
            anim = animations[n].get_instance(28, 27, framequeue, commandqueue, fps=fps)
            print(f"Starting animation '{anim.name}' for {time_per_anim} seconds.")
            #anim.params(28, 27, framequeue, commandqueue, fps=fps)
            anim.start()
            
            image = Pyghthouse.empty_image()
            opacity = 0
            while not anim_timer.has_elapsed() and self.keep_going:   
                frametimer.set(update_interval)
                while not framequeue.empty(): 
                    image = framequeue.get_nowait()
                if opacity < 255:
                    self.send_frame(ph, image, opacity/256)
                    opacity += 4
                else:
                    self.send_frame(ph, image, 1.0)
                commandqueue.put("keep_running")
                time.sleep(frametimer.remaining())
                
            for i in range(256, 0, -4):
                frametimer.set(update_interval)
                while not framequeue.empty(): 
                    image = framequeue.get_nowait()
                self.send_frame(ph, image, i/256)
                commandqueue.put("keep_running")
                time.sleep(frametimer.remaining())
                    
            #Fireworks().terminate()
            print("Attempting to terminate process...")
            anim.stop()
            anim.join(timeout = 2)
            print("Child process terminated.")
            n = (n+1) % len(animations)
    
if __name__ == "__main__":
    time_per_anim=30
    if len(sys.argv) > 1:
        int(sys.argv[1])
        local = '--local' in sys.argv or '--gui' in sys.argv
        remote = not '--local' in sys.argv
    AnimationController(time_per_anim, local, remote)