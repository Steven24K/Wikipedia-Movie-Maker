from gtts import gTTS
from moviepy.editor import *
import math
import urllib




def render_movie(subject = 'justin bieber'):
    celeb = subject
    language = 'en'
    frame_duration = 2
    paragraphs = 5
    
    print('Get wiki info')
    textInfo = celebFinder.getWikiInfo(celeb, paragraphs, language)
    
    print('Create text-to-speech')
    myobj = gTTS(text=textInfo, lang=language, slow=False)
    
    soundFile = 'voice-overs/{}.mp3'.format(celeb)
    print('Save sound file :: ' + soundFile)
    myobj.save(soundFile)
    
    print('Create audio clip')
    audioclip = AudioFileClip(soundFile)
    
    print('Get giphys')
    gifs = celebFinder.getGifImage(celeb, limit=math.ceil(audioclip.duration/frame_duration))

    cnt = 0
    gif_paths = []
    print('Save gifs :: ' + str(len(gifs)))
    for gif in gifs: 
        gif_path = 'content/' + str(cnt) + '.gif'
        gif_paths.append(gif_path)
        urllib.request.urlretrieve(gif, gif_path)
        cnt += 1
        print('Saved giph ' + gif_path)



    print('Render final product')

    background = ImageClip('background.png', duration=audioclip.duration)

    def MakeVideoClip(path, duration):
        try: 
            return VideoFileClip(path, target_resolution = background.size).set_duration(duration)
        except: 
            return ImageClip('no-img.png').set_duration(duration)

    #clips = map(lambda path: VideoFileClip(path).set_duration(frame_duration), gif_paths)
    clips = map(lambda path: MakeVideoClip(path, frame_duration), gif_paths)

    final_clip = concatenate_videoclips(list(clips), method='compose')
    final_clip = final_clip.set_audio(audioclip)

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([background, final_clip], use_bgclip=True, bg_color='white')
    video = video.set_duration(audioclip.duration)

    # Write the result to a file (many options available !)
    video.write_videofile("videos/{}.mp4".format(celeb), fps=24)


