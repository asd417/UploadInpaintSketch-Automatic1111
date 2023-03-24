# UploadInpaintSketch-Automatic1111

Inpaint Upload but for Sketch

Sick and tired of the built-in painting feature in inpaint sketch so I wrote this to edit the mask externally.


Installation

scripts/inpaint_upload_sketch.py


Usage:

1. Switch to Inpaint Upload Tab in img2img

2. Put Base image

3. Leave the default mask file input empty (You can put anything here but it will be overwritten by the script)

4. Enable 'Upload Inpaint Sketch' script

5. Check Enable checkbox and upload your transparent mask here.


Note:

Your 'Mask Mode' option will apply normally.

Your 'Mask Blur' option will not apply. The intention of this script is to use external program to finetune your mask including the blur effect. May add this feature later.


Example:
Base Image:

![base_image](https://user-images.githubusercontent.com/33945246/227451084-9b5468e1-57e3-45f8-98ac-316365097f65.png)

Mask Image:

![transparent image](https://user-images.githubusercontent.com/33945246/227451093-cc5d0819-1634-4e63-9b00-ae6ae2c1eab1.png)


Results:

Mask Mode: Inpaint Masked

![00052-1062298568](https://user-images.githubusercontent.com/33945246/227451037-05e932ed-2fb3-401a-917a-5dc8e413f91c.png)

Mask Mode: Inpaint not Masked

![00053-498094752](https://user-images.githubusercontent.com/33945246/227452909-d7cec86c-6de6-4c23-a4a8-6156ddd57103.png)
