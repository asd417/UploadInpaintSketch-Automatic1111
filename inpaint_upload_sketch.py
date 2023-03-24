import modules.scripts as scripts
import gradio as gr
import numpy as np
import tempfile

from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageChops
from modules.processing import Processed, process_images
from modules.shared import opts, cmd_opts, state

class Script(scripts.Script):
    
    def __init__(self):
        self.active = False

    def title(self):
        return "Upload Inpaint Sketch"

    def ui(self, is_img2img):
        info = gr.HTML("<p style=\"color:white\">Must be in Inpaint Upload Mode. Mask Alpha Channel Multiplier adjusts the transparency of the diffusion mask. Mask Image Alpha Multiplier adjusts the blending transparency of the mask image onto the image. 0.5 = 50% transparency</p>")
        
        with gr.Row():
            with gr.Column(min_width = 50, scale=1):
                active = gr.Checkbox(value = False,label="Active",interactive =True,elem_id="SU_active")
                file_mask = gr.File(label="Upload Sketch", type='file', elem_id=self.elem_id("file"))
                alpha_multiply_mask = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, value=1.0, label="Mask Alpha Channel Multiplier", elem_id=self.elem_id("alpha_multiply_mask"))
                alpha_multiply_mask_image = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, value=1.0, label="Mask Image Alpha Multiplier", elem_id=self.elem_id("alpha_multiply_mask_image"))
        return [info, active, file_mask,alpha_multiply_mask,alpha_multiply_mask_image]

    def run(self, p, _, active, file_mask, alpha_multiply_mask,alpha_multiply_mask_image):
        if not active:
            # print("MASK P TYPE= " + str(type(p.image_mask)))
            return process_images(p)

        file_mask_image = Image.open(file_mask)
        # image from p.image_mask does not have alpha channel
        # file_mask_image = p.image_mask
        image = p.init_images[0]
        mask = None
        if not (image.mode is 'RGBA'):
                alpha = Image.new("L", image.size, 255)
                image.putalpha(alpha)

        if 'A' in file_mask_image.getbands():
            print("Input Mask Image has alpha channel")
            r,g,b,a = file_mask_image.split()

            # applies Mask Alpha Channel Multiplier using existing alpha
            a_modified = ImageChops.multiply(a, Image.new('L', a.size, int(255*alpha_multiply_mask)))
            mask = a_modified

            # applies Mask Image Alpha Multiplier using existing alpha
            a_image = ImageChops.multiply(a, Image.new('L', a.size, int(255*alpha_multiply_mask_image)))
            file_mask_image.putalpha(a_image)

        else:
            print("\nInput Mask Image has no alpha channel\n")
            alpha = Image.new("L", image.size, 255)
            
            # applies Mask Image Alpha Multiplier
            file_mask_image.putalpha(Image.new('L', a.size, int(255*alpha_multiply_mask_image)))
            mask = Image.new('RGB', (image.size[0], image.size[1]), color='white')

        # merges mask image onto image using alpha channel
        image = Image.alpha_composite(image,file_mask_image)
        file_mask_image.close()
        image = image.convert("RGB")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
                mask.save(temp.name)
        
        p.init_images[0] = image
        p.image_mask = mask
        return process_images(p)
        
        