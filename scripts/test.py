import pyglet
import scipy.io.wavfile as wavfile
import numpy

def to_16bit_wav(filepath):
  sr, data = wavfile.read(filepath)
  wavfile.write(str(16) + filepath, sr, numpy.int16(data))

to_16bit_wav("snare.wav")

window = pyglet.window.Window()
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')
def audio_callback(dt):
    print('-- audio_callback')
    #f = 'res/sounds/letters/k.wav'
    f = '16snare.wav'
    if 1:
        player = pyglet.media.Player()
        sound = pyglet.media.load(f)#, streaming=False)
        player.queue(sound)
        player.play()
    else:
        music = pyglet.resource.media(f)
        music.play()


@window.event
def on_draw():
    window.clear()
    label.draw()

if __name__ == '__main__':
    pyglet.clock.schedule_interval(audio_callback, 2.0)
    pyglet.app.run()