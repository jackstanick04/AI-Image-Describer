## IMPORT STATEMENTS

# import flask object and request method (req method allows to store data that is imported), and jsonify (to send the return in the right format)
from flask import Flask, request, jsonify
# import CORS which allows for flask to talk to the react port
from flask_cors import CORS
# import os allows for python to talk to my personal mac (like where files are stored), but this is entirely optional for the project
import os
# import to get access to the .env
from dotenv import load_dotenv
# import for gemini api
from google import genai
# import types (makes container for the image to be passed through (packages it)
from google.genai import types

## API, FLASK, AND FILE STORING DECLARATIONS

# load the dotenv variables, then get the key and store it
load_dotenv()
api = os.getenv("GEMINI_KEY")
# set up gemini client (my connection to the gemini api)
gem_client = genai.Client(api_key = api)
# set up for flask object, name part is just telling flask object its location on the computer?
fl = Flask(__name__)
# CORS allows it to read from other ports
CORS(fl)
# creating a folder to store the images in; caps indicate the variable is a constant
FOLDER_NAME = "image_uploads"
# check if the folder exists, and if not, make it (need .path, but logically if it doesn't exist then a path wouldn't exist either)
if not os.path.exists(FOLDER_NAME) : 
    os.makedirs(FOLDER_NAME)

## MAIN PROGRAM DECLARATION

# decorator 
# route checks the url, if it ends in image (can be any word) and a post request, then call decorator
@fl.route("/upload", methods = ["POST"])
# python function we want to be called when decorator works (main program)
def process_image() :

    # INPUT CHECKING FOR IMAGE UPLOAD

    # checking the right "form" of upload is an image
    # request.files holds all the files uploaded as a dictionary, with the type as the key and the acutal file as the value (make sure its an image box and not a video box)
    if "image" not in request.files : 
        return "did not upload correct file type"
    # check to make sure something was actually uploaded, even if the category of image was right (make sure image box isnt empty)
    # get the value of the stored files at image key, then get its name and ensure its not empty (empty would mean nothing uploaded)
    img = request.files["image"]
    if img.filename == "" : 
        return "did not actually upload an image"
    
    ## LOADING THE IMAGE, MOVING IT TO THIS MAC, AND PROCESSING THE IMAGE INTO PART OBJECT

    # read the img file as binary bits
    img_binary = img.read()
    # reset the pointer back to beginning of the image so the filepath can be saved
    img.seek(0)
    # use os import to store the file path from our destination to the image we recieved
    # actually store the image (not its name) to my computer using this filepath
    path = os.path.join(FOLDER_NAME, img.filename)
    request.files["image"].save(path)

    # package the binary image data to be sent using types
    # sends the mime type (image here) and the actual image binary to be used
    proc_image = types.Part.from_bytes(
        data = img_binary,
        # file content type always gives the right type of image
        mime_type = img.content_type
    )

    ## INSTANCIATING MODEL AND GETTING TEXT RESPONSE

    # call the model we want with the prompt we want and the image data
    # it takes a list of "arguments" (the model type and then contents--prompts are the processed image and prompt)
    # prompt engineering and system instructions above are big area for improvement!!!!!!
    full_resp = gem_client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents = [
            "Please describe what you see in this image.",
            proc_image
        ]
    )
    # response includes multiple things, we just want to store the text
    gem_text = full_resp.text

    ## OUTPUT FOR CLARIFICATION

    # printing confirmation to python console
    print(gem_text)
    # returning json package with the response to react (description is what react is looking for)
    return jsonify({"description" : gem_text})

## MAIN METHOD

# name is a variable assigned to the file and how it is being used
# if i run a python file, its name is main; if i import it, its name is the file name, not main
# thus, this main method only gets ran (server only set up) when running this file, not importing it
if __name__ == "__main__" : 
    # start server, and restart the server every time I refresh
    # need empty server of 5001
    fl.run(debug = True, port = 5001)