import tkinter as tk
import multiprocessing, time, sys, signal
from pyghthouse.ph import Pyghthouse
from local_display import DisplayProcess
from stopwatch import Stopwatch
from color_functions import interpolate, cycle
from os import getenv
from animations.a_bounce import BounceAnimation

class AnimationController():   
    def __init__(self, time_per_anim, gui = False, remote = True, user=None, token=None, fps=60, animation=None) -> None:
        self.keep_going = True
        self.fps = fps if fps > 0 else 60
        self.update_interval = 1/(self.fps)
        self.name = "JhController"
        signal.signal(signal.SIGINT, self._handle_sigint)
        self.remote_enabled = remote
        self.ph = None
        self.gui_enabled = gui
        self.displayprocess = None
        self.displayqueue = None
        self.user = user
        self.token = token
        self.anim_timer = Stopwatch()
        self.frame_timer = Stopwatch() 
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
        
    def fade_opacity(self):
        elapsed = self.anim_timer.elapsed()
        remaining = self.anim_timer.remaining()
        if elapsed < 1:
            return elapsed
        elif remaining < 1:
            return remaining
        else:
            return 1.0
        
    def run_animation(self, anim: BounceAnimation, timeout=3000):
        # Initialize animation timer with timeout
        self.anim_timer.set(timeout)
        # Initialize frame timer with 100 ms
        self.frame_timer.set(0.1)
        while self.keep_going and not self.anim_timer.has_elapsed():  
                # Get image from animation
                frame = anim.get_frame()
                time.sleep(self.frame_timer.remaining()*0.5)
                # Send image at a fixed time after sleep to avoid stuttering
                if frame:
                    self.send_frame(frame, self.fade_opacity()) 
                    self.frame_timer.set(self.update_interval)
                else:
                    print("No image!")
                    break
                if self.frame_timer.has_elapsed():
                    print("Stutter detected: Frametimer ran out!")
                print(self.frame_timer.remaining())
                time.sleep(self.frame_timer.remaining())
                    
        
        
    ##### RUN METHOD #####
    def run(self, time_per_anim):
        
        if self.remote_enabled:
            self.read_auth()
            if not self.username or not self.token:
                exit(1)
            self.ph = Pyghthouse(self.username, self.token)
            self.ph.start()
            
        animations = [
                    BounceAnimation()
                    ]
    
        n = 0
        if self.gui_enabled:
            self.displayqueue = multiprocessing.Queue()
            self.displayprocess = DisplayProcess(self.displayqueue,self.fps)
            self.displayprocess.start()
            
        while self.keep_going:
            anim = animations[n].get_instance(28, 27, fps=self.fps)
            print(f"Starting animation '{anim.name}' for {time_per_anim} seconds.")
            self.run_animation(anim)
            n = (n+1) % len(animations)
            
        if self.displayprocess:
            self.displayprocess.stop()
            self.displayprocess.join(timeout = 2)
            self.displayprocess.kill()
        exit(0)
        
    
if __name__ == "__main__":
    AnimationController(300, True, True, None, None, 60, None)
    exit(0)
    if len(sys.argv) > 1:
        time_per_anim = int(sys.argv[1])
        gui = False
        remote = True
        fps = 60
        username = None
        token = None
        animation = None
        for argument in sys.argv:
            if '--local' in argument:
                gui = True
                remote = True
            elif  '--gui' in argument:
                gui = True
            elif '--fps=' in argument and len(argument) > 6 and argument.split('=')[1].isnumeric():
                fps = int(argument.split('=')[1])
            elif '--env' in argument:
                username = getenv('LIGHTHOUSE_USER')
                token = getenv('LIGHTHOUSE_TOKEN')
            elif '--animation=' in argument and len(argument) > 12 and argument.split('=')[1].isnumeric():
                animation = int(argument.split('=')[1])
        AnimationController(time_per_anim, gui, remote, username, token, fps, animation)
    else:
        print(f"Usage:\n{sys.argv[0]} [TIME] [OPTIONS]")
        print("Whereas [TIME] = time in seconds and possible options are:")
        print("--local\tRuns with local GUI only\n--gui\tRuns with both local GUI and remove connection")
        print("--env\tRead 'username' and 'token' from environment variable (instead of file) as")
        print("\tLIGHTHOUSE_USER | LIGHTHOUSE_TOKEN\n--fps=x\tRuns with x fps (default=60)")