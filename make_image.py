import math
from tqdm import tqdm
from pydub import AudioSegment
from PIL import Image, ImageDraw


def generate_waveform_image(audio_path, width, height, audio_slice=None, mirror=True):
    audio = AudioSegment.from_wav(audio_path)
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    if audio_slice:
        audio_length = len(audio[audio_slice])  # in milliseconds
    else:
        audio_length = len(audio)
    volumes = list(
        audio[slice((pixel * audio_length) / width, ((pixel + 1) * audio_length) / width)].rms
        for pixel in range(width))
    max_volume = int(max(volumes))
    volume_image_heights = list(volume * height / max_volume for volume in volumes)
    draw = ImageDraw.Draw(image)
    if mirror:
        for pixel, pixel_height in tqdm(enumerate(volume_image_heights)):
            draw.line(
                [(pixel, (height - pixel_height)/2), (pixel, (height + pixel_height)/2)],
                width=1,
                fill=(255, 255, 255)
            )
    else:
        for pixel, pixel_height in tqdm(enumerate(volume_image_heights)):
            draw.line(
                [(pixel, height), (pixel, height - pixel_height)],
                width=1,
                fill=(255, 255, 255)
            )

    return image


def save_waveform_image(output_path, audio_path, width, height, audio_slice=None, mirror=True):
    image = generate_waveform_image(audio_path, width, height, audio_slice, mirror)
    image.save(output_path)


def save_waveform_image_default(output_path, audio_path):
    audio = AudioSegment.from_wav(audio_path)
    time_for_full_screen_scroll_in_s = 20
    time_for_full_screen_scroll_in_ms = time_for_full_screen_scroll_in_s * 1000
    video_width_in_px = 1920
    waveform_width_in_px = math.ceil(len(audio) * video_width_in_px / time_for_full_screen_scroll_in_ms)

    save_waveform_image(output_path, audio_path, waveform_width_in_px, 500, None, True)
