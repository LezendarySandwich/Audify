#Convert music files to .wav format and store in the same folder
#changes in Songs.py os.remove changed to os.rename for test 


from pydub import AudioSegment
import os

#directory of input songs
 

#file formats to convert into wav
file_formats = ['m4a', 'mp3']

def convert(music_dir):
	for file in os.listdir(music_dir):
		if file.split('.')[-1] in file_formats:
			print("Working on file", file)
			new_name = ''.join(file.split('.')[:-1])+'.wav'
			file=music_dir+file
			new_name=music_dir+new_name
			print(file,new_name)
			AudioSegment.from_file(file).export(new_name, format="wav")
			os.remove(file)
	