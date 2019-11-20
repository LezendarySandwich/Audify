

"""
Brute force method which uses the sliding window approach to compare the input target zone with all songs in the database
Extremely slow!
	def brute_force_compare_filtered(self, song1, song2):
		#Assuming x has more time slices than y (x is original, y is input)
		#Both have structure: x[time_slice] = [freq1, freq2, etc.]
		
		if song1.time_res != song2.time_res:
			print("Time resolution of both songs is unequal. Sliding window yet to be implmeneted")
			# exit(0)
			return (0,0)

		try:
			x = song1.filtered
			print("Found filtered for",song1.name,"in pickle dump")
		except:
			x = song1.fft_and_mask()
			song1.dump()
		try:
			y = song2.filtered
			print("Found filtered for",song2.name,"in pickle dump")
		except:
			y = song2.fft_and_mask()
			song2.dump()

		print("\nBrute-Force comparison between",song1.name, "and",song2.name," \n")
		if len(x) < len(y):
			x,y = y,x

		lx, ly = len(x), len(y)

		overlap = {}
		for start in range(lx-ly+1):
			matches, total = 0, 0
			for i in range(ly):
				if start+i not in x.keys() or i not in y.keys():
					continue
				x_cur, y_cur = x[start+i], y[i]
				total += len(x_cur) + len(y_cur)
				for x_freq in x_cur:
					for y_freq in y_cur:
						if abs(x_freq-y_freq) < self.delta:
							matches += 2
			if total == 0:
				overlap[start] = -1
			else:	
				overlap[start] = matches/total

		# plt.scatter(np.array(list(overlap.keys()))*song1.time_res, overlap.values())
		idx = np.argmax(list(overlap.values()))
		print("Most probable overlap between",song1.name,"and",song2.name,"is at time t = ",idx*song1.time_res,'with strength = ',overlap[idx])
		# plt.show()
		return (idx*song1.time_res, overlap[idx])


	def brute_search(self, target_song):

		base_pth = self.audio_path

		comparisons = {}

		target = Song(base_pth+target_song, self.window_size, keep_coeff = self.keep_coeff, sampling_freq=self.sampling_freq)
		maximum = -1
		name = '.'
		best_time = 0

		for song_name in os.listdir(base_pth):
			
			if song_name != target_song and song_name != '.DS_Store':

				current = Song(base_pth+song_name, self.window_size, keep_coeff = self.keep_coeff, sampling_freq=self.sampling_freq)
				time, strength = self.brute_force_compare_filtered(current, target)
				comparisons[song_name] = (time, strength)
				if strength > maximum:
					maximum = strength
					name = song_name
					best_time = time

		print("BEST MATCH:",name,"at time t = ",best_time)
		print('\n',comparisons)
"""