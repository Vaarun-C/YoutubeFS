import struct
import numpy as np
from PIL import Image

class readFiles():
    def __init__(self, path) -> None:
        self.path = path
        self.color_code_size = 6
        self.width = 3840
        self.height = 2160
        self.pixel_data = np.zeros((self.height, self.width, 3), dtype=np.uint8)

    def get_txt_bytestream(self) -> str:
        with open(self.path, "rb") as file:
            byte_stream = file.read()
            print(byte_stream)
            return(byte_stream.hex())

    def get_colors(self, byte_stream) -> list[str]:
        block_24_stream = [byte_stream[i:i+self.color_code_size] for i in range(0,len(byte_stream),self.color_code_size)]
        last_code = block_24_stream[-1]
        last_code_length = len(last_code)

        if(last_code_length != self.color_code_size):
            last_code = last_code + (self.color_code_size - last_code_length)*'0'

        block_24_stream[-1] = last_code
        return block_24_stream
    
    def hex_to_rgb(self, hex_color_code) -> list[int]:
        red = int(hex_color_code[0], 16)*16 + int(hex_color_code[1], 16)
        green = int(hex_color_code[2], 16)*16 + int(hex_color_code[3], 16)
        blue = int(hex_color_code[4], 16)*16 + int(hex_color_code[5], 16)
        return [red, green, blue]
    
    def insert_pixels(self, pixel_colours) -> None:
        x = 0
        y = 0
        for colour in pixel_colours:
            color_code = self.hex_to_rgb(colour)
            self.pixel_data[y, x] = color_code
            x += 1
            if(x>= self.width):
                x=0
                y+=1
            # print(colour, x, y)

    def print_image(self) -> None:
        image = Image.fromarray(self.pixel_data)
        image.save('output_image.png')

if __name__ == "__main__":
    rf = readFiles("./OS Unit 1.pdf")
    colours = (rf.get_colors(rf.get_txt_bytestream()))
    rf.insert_pixels(colours)
    rf.print_image()
