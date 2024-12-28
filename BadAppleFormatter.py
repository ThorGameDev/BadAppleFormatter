import cv2
import os
import numpy as np
import time
import subprocess

class RenderSystem():
    def __init__(self, video: str) -> None:
        text = ""
        for num in range(100):
            text += "0000000000"
        self.output_queue = text
        self.current_frame = 0
        self.video = cv2.VideoCapture(video)
        self.video_length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT)) - 1


    def getChars(self, num: int) -> str:
        chars = self.output_queue[:num]
        #self.output_queue = self.output_queue[num:]
        return(chars)


    def blip(self, frame: np.ndarray):
        for row in range(frame.shape[0]):
            row_text = ""
            for col in range(frame.shape[1]):
                if(frame[row, col][0] > 127):
                    row_text += self.getChars(1)
                else:
                    row_text += " "
            print(row_text)

    def get_next_frame(self):
        ret, frame = self.video.read()
        if not ret:
            return
        self.current_frame += 1
        if self.current_frame > (self.video_length-1):
            self.video.release()
        return frame
    def skip_next_frame(self):
        ret, frame = self.video.read()
        if not ret:
            return
        self.current_frame += 1
        if self.current_frame > (self.video_length-1):
            self.video.release()

    def render(self):
        if self.current_frame + 1 >= self.video_length:
            return
        term = os.get_terminal_size()
        if len(self.output_queue) > term.columns * term.lines:
            os.system("clear")
            frame = self.get_next_frame()
            down_width = term.columns
            down_height = term.lines -1
            down_points = (down_width, down_height)
            resized_down = cv2.resize(frame, down_points, interpolation= cv2.INTER_LINEAR)
            self.blip(resized_down)
        else:
            self.skip_next_frame()

command = subprocess.Popen(['ls','-l'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
renderer = RenderSystem("./TouhouBadApple.mp4")
while True:
    renderer.render()
    renderer.output_queue += str(command.stdout.read())
    time.sleep(1/60)
