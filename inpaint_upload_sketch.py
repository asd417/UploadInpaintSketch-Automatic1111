import modules.scripts as scripts
import gradio as gr
import numpy as np
import tempfile

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from modules.processing import Processed, process_images
from modules.shared import opts, cmd_opts, state

class Script(scripts.Script):
    
    def __init__(self):
        self.active = False

    def title(self):
        return "Upload Inpaint Sketch"

    def ui(self, is_img2img):
        info = gr.HTML("<p style=\"margin-bottom:0.75em; color:white\">Must be in Inpaint Upload Mode!</p>")
        
        with gr.Row():
            with gr.Column(min_width = 50, scale=1):
                active = gr.Checkbox(value = False,label="Active",interactive =True,elem_id="SU_active")
                file_mask = gr.File(label="Upload Sketch", type='file', elem_id=self.elem_id("file"))
        return [info, active, file_mask]

    def run(self, p, _, active, file_mask):
        if not active:
            print("MASK P TYPE= " + str(type(p.image_mask)))
            return process_images(p)
        
        file_mask_image = Image.open(file_mask)
        print("MASK FILE TYPE= " + str(type(file_mask_image)))
        image = p.init_images[0]
        
        if 'A' in file_mask_image.getbands():
            r,g,b,a = file_mask_image.split()
            mask = a
        else:
            file_mask_image = Image.fromarray()
            mask = Image.new('RGB', (image.size[0], image.size[1]), color='white')

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
            mask.save(temp.name)

        if not (image.mode is 'RGBA'):
            alpha = Image.new("L", image.size, 255)
            image.putalpha(alpha)      

        print("MODE IS "+ file_mask_image.mode)
        print("MODE IS "+ image.mode)
        image = Image.alpha_composite(image,file_mask_image)
        image = image.convert("RGB")

        p.init_images[0] = image
        p.image_mask = mask
        return process_images(p)
        
        