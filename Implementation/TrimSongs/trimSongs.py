from pydub import AudioSegment

def trimSong(song_pth , new_name, target_folder, startSec, duration):
    files_path = './../audio/'
    
    endSec = startSec + duration

    # Time to miliseconds
    startTime = startSec*1000
    endTime = endSec*1000

    # Opening file and extracting segment
    song = AudioSegment.from_file( song_pth  )
    extract = song[startTime:endTime]

    # Saving
    extract.export( target_folder + new_name , format="wav")
