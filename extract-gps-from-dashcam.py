import re
import subprocess
from subprocess import PIPE

FFMPEG_PATH = 'ffmpeg'
INTERMEDIATE = 'intermediate.txt'


def analyze(video):
    cmd = [FFMPEG_PATH, '-i', video, '-an', '-vn', '-bsf:s', 'mov2textsub', '-c:s', 'copy', '-f', 'rawvideo', INTERMEDIATE]
    try:
        subprocess.check_call(cmd, stdout=None)
    except subprocess.CalledProcessError:
        return []
    
    with open(INTERMEDIATE, 'r') as f:
        text = f.read()
    
    data = []
    parts = text.split(',')[:-1]
    pattern = r'.*EXTD\/\d\/(\d+)\.(\d+)\/(\d+)\.(\d+)\/\w+\/\w+\/\w+\/\w+'
    for part in parts:
        m = re.match(pattern, part)
        matches = m.groups()
        longitude = float('{}.{}'.format(matches[0], matches[1]))
        latitude = float('{}.{}'.format(matches[2], matches[3]))
        data.append([latitude, longitude])

    return data


if __name__ == '__main__':
    output_filename = 'output.csv'
    input_filename = 'test.MP4'
    headers = ['latitude', 'longitude']

    gps = analyze(input_filename)

    with open(output_filename, 'w+') as f:
        f.write(','.join(headers))
        f.write('\n')
        for data in gps:
            f.write(','.join(map(str, data)))
            f.write('\n')