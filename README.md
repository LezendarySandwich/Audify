# Audify
- AUDify aims at identifying a song by analyzing its recorded audio segment, which would most likely be distorted due background noise and compressed, owing to the fact that the recording would be done using a tiny in-built microphone on a mobile phone. 
<br/>
- Moreover, the algorithm targets to perform the recognition as fast as possible with a low number of false positives, that is, with the minimum scope of error in detection. 
# Steps Involved
- Sampling
- Quantization
- Discrete Fourier Transform using Fast Fourier Transform technique(Cooley-Tukey algorithm)
- Matching Audio Fingerprints, which are extracted hash tokens from the audio samples, with the fingerprints of the songs present in our database and then the result was computed. 
# Results
Spectrogram (Song - Neovaii - I remember)<br/>
<img src="https://drive.google.com/uc?export=view&id=1O1di5OuZ3aZeUvIh3CcSyRHmS2Xx0GDz" alt="alt text"
width="500" height="400">

Filtered Spectrogram (Song - Neovaii - I remember)<br/>
<img src="https://drive.google.com/uc?export=view&id=1d3-il8002h2VQthx_lCbdGKDJzot4nT4" alt="alt text"
width="550" height="400">
<img src="https://drive.google.com/uc?export=view&id=19fzFwK2hWXR8ZGEMbGFOallgfAb2LTuo" alt="alt text" width="500" height="400">

Blue: Correctly recognized
<br/>
Green: Correctly recognized with correct starting time
<br/>
Orange: Incorrectly matched
<br/>
# Accuracy
Batch size: 172
<br/>
Correct matches: 162
<br/>
Time taken: 30 minutes
<br/>
Percentage accuracy: 94.18%
# References
[http://coding-geek.com/how-shazam-works/](http://coding-geek.com/how-shazam-works/)
<br/>
Wang, Avery. (2003). An Industrial-Strength Audio Search Algorithm.