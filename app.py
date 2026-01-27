# import flask object and request method (req method allows to store data that is imported)
from flask import Flask, request
# import os allows for python to talk to my personal mac (like where files are stored)
import os
# import base 64 allows for the conversion of binary to actual text (image to json transfer for api)
import base64

# set up for flask object, name part is just telling flask object its location on the computer?
fl = Flask(__name__)

# creating a folder to store the images in; caps indicate the variable is a constant
FOLDER_NAME = "image_uploads"
# check if the folder exists, and if not, make it (need .path, but logically if it doesn't exist then a path wouldn't exist either)
if not os.path.exists(FOLDER_NAME) : 
    os.makedirs(FOLDER_NAME)

# decorator 
# route checks the url, if it ends in image and a post request, then call the decorator; i choose the /image part to whatever i want (just used to point to which method to call)
@fl.route("/image", methods = ["POST"])
# python function we want to be called when decorator works
def process_image() :

    # even if we uploaded the http thing for an image, need to actually check we have an image file, and even if we do we need to check if there is actually an image there

    # checking the right "form" of upload is an image
    # request.files holds all the files uploaded as a dictionary, with the type as the key and the acutal file as the value (make sure its an image box and not a video box)
    if "image" not in request.files : 
        return "did not upload correct file type"
    
    # check to make sure something was actually uploaded, even if the category of image was right (make sure image box isnt empty)
    # get the value of the stored files at image key, then get its name and ensure its not empty (empty would mean nothing uploaded)
    img = request.files["image"]
    if img.filename == "" : 
        return "did not actually upload an image"
    
    # read the img file as binary bits
    img_binary = img.read()
    # convert the binary to base 64 text
    # first we convert to bytes of base 64 (encode), which then go to the ascii table and map to text (decode)
    # this now has base 64 long string of title, dimensions, rgb values for each pixel etc
    img_base64 = base64.b64encode(img_binary).decode("utf-8")

    # use os import to store the file path from our destination to the image we recieved
    # actually store the image (not its name) to my computer using this filepath
    path = os.path.join(FOLDER_NAME, img.filename)
    request.files["image"].save(path)

    # printing confirmation to python console
    print(f"binary: {img_binary}")
    print(f"base64: {img_base64}")

    # returning message to go to apple terminal
    return "success. image uploaded and parsed."

# main method
# name is a variable assigned to the file and how it is being used
# if i run a python file, its name is main; if i import it, its name is the file name, not main
# thus, this main method only gets ran (server only set up) when running this file, not importing it
if __name__ == "__main__" : 
    # start server, and restart the server every time I refresh
    fl.run(debug = True)