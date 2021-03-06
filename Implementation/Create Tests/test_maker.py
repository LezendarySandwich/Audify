#Generates a random batch of audio clips from a directory fo songs for testing

import subprocess
import numpy as np
import os, shutil
import matplotlib.pyplot as plt
import time
import sys
sys.path.insert(1,'./../TrimSongs')
sys.path.insert(2,'./../Recognize Song')
from trimSongs import trimSong
from Findit import Findit
#from Shazam import Shazam
from Song import Song

path_Images = './../Images/'
path_audio = './../audio/'
path_test = './../test/'
path_database = './../database'
path_SOX = './../Recognize Song/sox'

def trim_s(song_pth, target_folder, start, duration):

	#new clip has the following name: <name>_start_duration.wav
	new_name = song_pth.split('.')[0].split('/')[-1]+'_'+str(start)+'_'+str(duration)+'.wav'
	#use soX to clip the file
	trimSong(song_pth, new_name, target_folder, start, duration)
	#print(song_pth,new_name)
	#subprocess.call(['./sox', song_pth, song_pth, 'trim', str(start), str(duration)])
"""
creates batch of clips to test on
songs_path is the directory which contains the original songs
target_path is the folder where the clips are to be dumped
"""

def create_clips(num_clips, songs_path=path_audio, target_path=path_test):

	#parameters which define the lower and upper bounds for the clips
	lower_length, upper_length = 2, 12
	#maximum starting point to clip the audio. Should be lesser than min(duration_of_songs)-upper-length
	start_max = 7
	songs_dir = [x for x in os.listdir(songs_path) if x != '.DS_Store']
	total_clips = len(songs_dir)
	#random batch of start points and the lengths of the clips
	start = np.random.randint(0, high=start_max, size=num_clips)
	lengths = np.random.randint(lower_length, high=upper_length, size=num_clips)

	chosen_songs = np.random.choice(total_clips, num_clips)
	#clip and save the audio files
	for i in range(num_clips):
		trim_s(songs_path+songs_dir[chosen_songs[i]], target_path, start[i], lengths[i])

"""
Do the actual testing by calling the Shazam model on each clip and store the results
Each prediction is classified into 3 categories:
1. correct with time: if the songs is correctly idenitifed along with the point in time at which the clip was trimmed
2. correct: song is correctly identified but the time is wrong
3. wrong: incorrect prediction about the song
set fresh start = True if the directory of clips needs to be cleaned before generating a new batch 
"""
def batch_testing(fresh_start=True, songs_path=path_audio, data_path=path_database, clips_path=path_test):
	
	#clip files have structure: <name-of-song>_start_dur.wav
	num_clips = 20
	#parameters for the Shazam app
	window_size = 1024
	downsample_factor = 2
	#maximum tolerance for identifying if the point in time at which the clip was trimmed is correct
	time_delta = 1

	#delete existing clips and make a new folder
	if fresh_start:
		shutil.rmtree(clips_path)
		os.mkdir(clips_path)

	#create clips to test
	create_clips(num_clips)
	app = Findit(audio_path=path_audio, data_path=path_database)
	#initialise the app
	#app = Shazam(songs_path, data_path)
    
	#store results
	stats = {}
	#to track time
	start_time = time.time()
	#total duration of clips. Used for tracking perofromance of the app
	clips_dur = 0

	for song in os.listdir(clips_path):

		if song == '.DS_Store':
			continue

		#identify song, duration and starting point
		song_name = '_'.join(song.split('_')[:-2])
		start, duration = int(song.split('_')[-2]), int(song.split('_')[-1].split('.')[0])
		#update the total duration of clips
		clips_dur += duration
		print(clips_path+song)

		#for each duration, store a dictionary of the 3 aforementioned categories 
		if duration not in stats.keys():
			stats[duration] = {'correct_time':0, 'correct':0, 'wrong':0}

		#test
		to_test = app.create_song(clips_path+song, try_dumped=True, is_target=True)
		print("Testing on", song_name)
		song_pred, time_pred = app.compare_song(to_test, check = True)
		
		#update statistics
		if song_pred == song_name and abs(time_pred-start) < time_delta:
			stats[duration]['correct_time'] += 1
		elif song_pred == song_name:
			stats[duration]['correct'] += 1
		else:
			stats[duration]['wrong'] += 1

	#marks end of prediction phase
	time_taken = time.time() - start_time

	#plot the stastics
	#green - correct with time, blue - correct, orange - wrong
	print(stats, time_taken)
	fig, ax = plt.subplots()
	ct, c, w = 0,0,0

	for dur, vals in stats.items():
		egs = sum(vals.values())
		for t_, num in vals.items():
			percent = 100*num/egs
			#if num == 0 :
    		#		continue
			if t_ == 'correct_time':
				ax.scatter(dur, percent, c='g')
				ct += num
			elif t_ == 'correct':
				ax.scatter(dur, percent, c='b')
				c += num
			else:
				ax.scatter(dur, percent, c='C1')
				w += num

	title = "time_taken: " + str(round(time_taken,4)) + "; len_clips: " + str(clips_dur) + 's'
	des = "Correct_time:"+str(ct)+" Correct:"+str(c)+" Wrong:"+str(w)
	plt.title(title+'\n'+des)
	plt.xlabel("Time duration in s")
	plt.ylabel("Percent success")
	plt.grid(True)
	plt.savefig(path_Images)
	shutil.rmtree(clips_path)
	os.mkdir(clips_path)

if __name__ == '__main__':
	batch_testing()