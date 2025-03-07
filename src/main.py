import tkinter as tk
import multiprocessing, time, sys, signal
from pyghthouse.ph import Pyghthouse
from local_display import DisplayProcess
from stopwatch import Stopwatch
from color_functions import interpolate, cycle
from os import getenv
from mp_firework import Fireworks
from mp_bouncers import BounceAnimation as Bouncers
from mp_lavablob import Lavablobs
from mp_rgbtest import RgbTest
from mp_rain import RainAnimation
from mp_rebound import ReboundAnimation
from mp_diffraction import DiffAnimation
from mp_conway import GameOfLife
from mp_scrolltext import ScrollText
from mp_dots import Dots
from mp_child_prot_symbol import ChildProtSymbol

class AnimationController():   
    def __init__(self, time_per_anim, gui = False, remote = True, user=None, token=None, fps=60, animations=[], perf=True) -> None:
        self.keep_going = True
        self.displayqueue = None
        self.animations = animations
        self.perf = perf
        self.name = "JhController"
        signal.signal(signal.SIGINT, self._handle_sigint)
        self.gui_enabled = gui
        self.remote_enabled = remote
        self.ph = None
        self.displayprocess = None
        self.username = user
        self.token = token
        self.fps = fps
        self.run(time_per_anim)

    def read_auth(self, filename="auth.txt"):
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
            else:
                self.username = username
                self.token = token
                return True
        return False
        
    def send_frame(self, image: list, factor: float):
        img = Pyghthouse.empty_image()
        for x in range(min(len(img), len(image[0]))):
            for y in range(min(len(img[0]), len(image))):
                img[x][y] = interpolate(image[y][x], img[x][y], factor) if factor < 1.0 else image[y][x]
        if self.ph:
            self.ph.set_image(img)
        if self.displayqueue:
            self.displayqueue.put_nowait(img)
        
    def _handle_sigint(self, signum, frame):
        print("Ctrl+C detected. Stopping animations...")
        self.keep_going = False
        
    def perf_wait(self, timer: Stopwatch):
        if self.perf:
            while True:
                if timer.has_elapsed(): break
        else:
            time.sleep(timer.remaining())
        
    ##### RUN METHOD #####
    def run(self, time_per_anim):
        
        if self.remote_enabled:
            if not self.username or not self.token:
                self.read_auth()
            if not self.username or not self.token:
                exit(1)
            self.ph = Pyghthouse(self.username, self.token)
            self.ph.start()
            
        
        animations = self.animations
        anim_timer = Stopwatch()
        frametimer = Stopwatch() 
        update_interval = 1/(self.fps)
        n = 0
        if self.gui_enabled:
            self.displayqueue = multiprocessing.Queue()
            self.displayprocess = DisplayProcess(self.displayqueue,fps)
            self.displayprocess.start()
        while self.keep_going:
            framequeue = multiprocessing.Queue()
            commandqueue = multiprocessing.Queue()
            anim_timer.set(time_per_anim)
            anim = animations[n].get_instance(28, 27, framequeue, commandqueue, fps=fps)
            print(f"Starting animation '{anim.name}'" + "." if len(animations)==1 else f" for {time_per_anim} seconds.")
            #anim.params(28, 27, framequeue, commandqueue, fps=fps)
            anim.start()
            
            image = Pyghthouse.empty_image()
            opacity = 0
            while (len(animations)==1 or not anim_timer.has_elapsed()) and self.keep_going:   
                frametimer.set(update_interval)
                while not framequeue.empty(): 
                    image = framequeue.get_nowait()
                if opacity < 255:
                    self.send_frame(image, opacity/256)
                    opacity += 4
                else:
                    self.send_frame(image, 1.0)
                commandqueue.put("keep_running")
                time.sleep(frametimer.remaining())
                
            for i in range(256, 0, -4):
                frametimer.set(update_interval)
                while not framequeue.empty(): 
                    image = framequeue.get_nowait()
                self.send_frame(image, i/256)
                commandqueue.put("keep_running")
                self.perf_wait(frametimer)
                    
            #Fireworks().terminate()
            anim.stop()
            anim.join(timeout = 2)
            print("Animation terminated.")
            n = (n+1) % len(animations)
        if self.displayprocess:
            print("Attempting to terminate subprocesses...")
            self.displayprocess.stop()
            self.displayprocess.join(timeout = 2)
            if self.displayprocess.is_alive():
                self.displayprocess.terminate()
                self.displayprocess.join()  
            else:
                print("Display terminated successfully.")
        exit(0)
        
    
if __name__ == "__main__":
    animations = [
                    #ScrollText(),
                    GameOfLife(),
                    ChildProtSymbol(),
                    ScrollText(),
                    RainAnimation(), 
                    #Dots(),
                    Fireworks(), 
                    ChildProtSymbol(),
                    Lavablobs(),
                    #RgbTest(), 
                    #ReboundAnimation(), 
                    #DiffAnimation(), 
                    Bouncers(),]
    if len(sys.argv) > 1:
        time_per_anim = int(sys.argv[1])
        gui = False
        remote = True
        fps = 60
        username = None
        token = None
        animations_enabled = animations
        perf_mode = False
        for argument in sys.argv:
            if '--local' in argument:
                gui = True
                remote = False
            elif  '--gui' in argument:
                gui = True
            elif '--fps=' in argument and len(argument) > 6 and argument.split('=')[1].isnumeric():
                fps = int(argument.split('=')[1])
            elif '--env' in argument:
                username = getenv('LIGHTHOUSE_USER')
                token = getenv('LIGHTHOUSE_TOKEN')
            elif '--animation=' in argument and len(argument) > 12 and argument.split('=')[1].isnumeric():
                animation = int(argument.split('=')[1])
            elif '--perf' in argument:
                perf_mode = True
            elif '--anim=' in argument:
                for entry in animations:
                    if argument.split('=')[1] in entry.name:
                        animations_enabled = [entry]
        AnimationController(time_per_anim, gui, remote, username, token, fps, animations_enabled, perf_mode)
    else:
        print(f"Usage:\n{sys.argv[0]} [TIME] [OPTIONS]")
        print("Whereas [TIME] = time in seconds and possible options are:")
        print("--local\tRuns with local GUI only\n--gui\tRuns with both local GUI and remove connection")
        print("--env\tRead 'username' and 'token' from environment variable (instead of file) as")
        print("\tLIGHTHOUSE_USER | LIGHTHOUSE_TOKEN\n--fps=x\tRuns with x fps (default=60)")
        print("--perf\tUse active polling loop instead of 'wait' in frametimer for better performance on low end devices.")
        print(f"--anim=\tOnly show a certain animation. Available animations:\n\t{' '.join([anim.name for anim in animations])}")