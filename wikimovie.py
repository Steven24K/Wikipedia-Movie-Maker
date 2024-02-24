import argparse
import getInfo
from gtts import gTTS
import datetime
from moviepy.editor import *
import math
import urllib
import config
import os

def main():
    SOUND_FOLDER = 'voice-overs'
    IMAGE_FOLDER = 'giffs'
    VIDEO_OUTPUT = 'videos'


    default_background = 'defaults/background.png'
    default_img_fallback = 'defaults/no-image.png'

    parser = argparse.ArgumentParser(prog='Wikipedia Movie Maker',
                                     description='Make movies from Wikipedia articles, combined with Giffs!',
                                     usage='Example: wikimovie.py Justin Bieber --language en',
                                     )
    parser.add_argument('subject', help='The subject of your movie.')
    parser.add_argument('--language', default='en', required=False,
                        help='You can provide any language, this will be the language of the Google speech API and the language of the Wikipedia article')
    parser.add_argument('--paragraphs', required=False, default=3, help='The amount paragraphs taken from the Wikipredia article.')
    parser.add_argument('--gif_interval', default=2, help='The time a gif is show in the image', required=False)
    parser.add_argument('--background', default=default_background, help='Provide a custom background for your video.', required=False)
    parser.add_argument('--fallback', default=default_img_fallback, help='Provide a custom fallback when the image doen not load', required=False)
    parser.add_argument('--audio_dir', default=SOUND_FOLDER ,required=False)
    parser.add_argument('--image_dir', default=IMAGE_FOLDER ,required=False)
    parser.add_argument('--o', default=VIDEO_OUTPUT ,required=False)

    args = parser.parse_args()
    print(args)

    subject = args.subject
    language = args.language
    paragraphs = args.paragraphs 
    interval = args.gif_interval
    background_img = args.background
    img_fallback = args.fallback
    snd_dir = args.audio_dir
    img_dir = args.image_dir
    out = args.o

    subject_without_space = subject.replace(' ', '_')

    try: 
        os.mkdir(snd_dir)
    except: 
        print('Sound folder allready exists')
    try:
        os.mkdirs(img_dir)
    except: 
        print('Image folder allready exists')
    try:
        os.makedirs(img_dir + '/{}'.format(subject_without_space))
    except: 
        print('Subject image {} folder allready exists'.format(subject_without_space))
    try:
        os.mkdir(out)
    except: 
        print('Video output folder allready exists')

    text = getInfo.getWikiInfo(subject, int(paragraphs), language)
    print(text)

    print('Create text-to-speech')
    soundObj = gTTS(text=text, lang=language, slow=False)
    soundFile = snd_dir + '/generated_voice_{}_{}.mp3'.format(subject_without_space, datetime.date.today())
    print('Save sound file: ' + soundFile)
    soundObj.save(soundFile)

    print('Create audio clip')
    audioClip = AudioFileClip(soundFile)

    print('Get images')
    gifs = getInfo.getGifImages(config.GIPHY_API_KEY, subject, limit=math.ceil(audioClip.duration/interval), offset=0, rating='g', lang=language)

    cnt = 0
    gif_paths = []
    print('Save gifs: ' + str(len(gifs)))
    for gif in gifs: 
        gif_path = img_dir + '/{}/image_{}.gif'.format(subject_without_space, str(cnt))
        gif_paths.append(gif_path)
        urllib.request.urlretrieve(gif, gif_path)
        cnt += 1
        print('Saved giph ' + gif_path)

    print('Render final product')
    background = ImageClip(background_img, duration=audioClip.duration)

    def MakeVideoClip(path, duration):
        try: 
            return VideoFileClip(path, target_resolution = background.size).set_duration(duration)
        except: 
            return ImageClip(img_fallback).set_duration(duration)


    clips = map(lambda path: MakeVideoClip(path, interval), gif_paths)

    final_clip = concatenate_videoclips(list(clips), method='compose')
    final_clip = final_clip.set_audio(audioClip)
    final_clip = final_clip.set_position(('center', 'top'))

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([background, final_clip], use_bgclip=True, bg_color='white')
    video = video.set_duration(audioClip.duration)

    # Write the result to a file (many options available !)
    video.write_videofile("{}/{}.mp4".format(out, subject_without_space), fps=24)

    print('Done...')


if __name__ == '__main__':
    main()
