# ---- Flask Hello World ---- #

# import the Flask class from the flash module
from flask import Flask, render_template
import Image
import glob
import os
from mutagen.easyid3 import EasyID3
from mutagen import File

# create the application object
app = Flask(__name__)

app.config["DEBUG"] = True

directory = "C:\Users\Mike\Music\.hopesfall\The Satellite Years"

# use decorators to link the function to a url
@app.route("/")
def get_tags():
	mp3_list = []  		# empty list to store all tags details
	imagefound = False			
	for file in glob.glob(directory+"\*.mp3"):
		mp3info = EasyID3(file)			# returns set of basic tags
		mp3_list.append(mp3info)		# add to list to pass to template
		if(imagefound == False):
			mp3file = File(file)
			artwork = mp3file.tags['APIC:'].data	#get image from tags
			art_filename = 'static/img/'+mp3info["artist"][0]+' - '+mp3info["album"][0]+'.jpg' # save as Artist - Album in static images
			with open(art_filename, 'wb') as img:
				img.write(artwork) 
				pil_image = Image.open(art_filename)	# open image with PIL to check size
				image_size = pil_image.size
				imagefound = True
	return render_template('main.html', mp3_list=mp3_list, art_filename=art_filename, image_size=image_size)

# start the development server using the run() method
if __name__ == "__main__":
	app.run()
	