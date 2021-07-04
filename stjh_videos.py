import math
import numpy as np
import moviepy.editor as mpy
from pydub import AudioSegment
from PIL import Image, ImageDraw


def draw_waveform_in_image(audio, image, left, top, width, height, audio_slice=None, mirror=True):
    if audio_slice:
        audio_length = len(audio[audio_slice])  # in milliseconds
    else:
        audio_length = len(audio)
    volumes = list(
        audio[slice((pixel * audio_length) / width, ((pixel + 1) * audio_length) / width)].rms
        for pixel in range(width))
    volume_image_heights = list(volume * height / max(volumes) for volume in volumes)
    draw = ImageDraw.Draw(image)
    if mirror:
        for pixel, pixel_height in enumerate(volume_image_heights):
            draw.line(
                [(left + pixel, top + (height - pixel_height)/2), (left + pixel, top + (height + pixel_height)/2)],
                width=1,
                fill=(255, 255, 255)
            )
    else:
        for pixel, pixel_height in enumerate(volume_image_heights):
            draw.line(
                [(left + pixel, top + height), (left + pixel, top + height - pixel_height)],
                width=1,
                fill=(255, 255, 255)
            )


time_for_full_screen_scroll_in_s = 10
time_for_full_screen_scroll_in_ms = time_for_full_screen_scroll_in_s * 1000
video_width_in_px = 1400
excerpt = AudioSegment.from_wav("test/Excerpt.wav")
waveform_width_in_px = math.ceil(len(excerpt) * video_width_in_px / time_for_full_screen_scroll_in_ms)


def make_frame(t):
    frame_image = Image.open("test/Instagram video background.png")
    draw_waveform_in_image(
        excerpt,
        frame_image,
        video_width_in_px - t * video_width_in_px / time_for_full_screen_scroll_in_s,
        900,
        waveform_width_in_px,
        500
    )
    return np.array(frame_image)[:, :, :3]


clip = mpy.VideoClip(make_frame, duration=len(excerpt)/1000)
clip.write_videofile("test/export.mp4", fps=60)
