#!/usr/bin/python
# -*- coding: utf-8 -*-

# pip install sox

import json

from multiprocessing import Pool
import logging
import os
import sys
import subprocess
import shlex
import re
from subprocess import call
from pathlib import Path
import sox

try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk


class Flac2Wav:

    logger = ''

    def __init__(self):
        global logger

        # create logger

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # create a file handler
        # handler = logging.FileHandler('converter.log')

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        # create a logging format

        formatter = \
            logging.Formatter('''
%(asctime)s - %(levelname)s - %(message)s 
''')
        handler.setFormatter(formatter)

        # add the handlers to the logger

        logger.addHandler(handler)

    def convert(self, src_dir, out_dir):
        global logger
        file_queue = []

        ext = ['.flac', '.wav']

        # collect files to be converted
        src_list = list(filter(Path.is_file, Path(src_dir).glob('**/*')))
        src_list = list(filter(lambda x: x.suffixes[0] == '.flac',src_list ))
        #src_list = list(filter(lambda x: re.match(r'.*mic1',str(x.name)),src_list ))
        trg_list = list(map(lambda x: re.sub(flac_folder,wav_folder, str(x)),src_list))
        trg_list = list(map(lambda x: re.sub(r'flac$','wav', x),trg_list))
        #trg_list = list(map(lambda x: re.sub(r'_mic\d','', x),trg_list))
        file_queue = list(map(lambda x,y:{
            'dir':str(x.parent),
            'path':str(x),
            'filename':str(Path(y).name),
            'dest':str(Path(y).parent)
            }
        ,src_list,trg_list))
        logger.info('Start converting:  %s files', str(len(file_queue)))

        with Pool(1) as p:
            p.map(self.process, file_queue)

    def cleanWhiteSpace(self, value):
        return value.replace(' ', '_').replace('/', '_').replace('|', '_').replace('"', '').replace('(', '').replace(')', '')

    def cleanDirectoryName(self, value):
        return value.replace('/', '_').replace('|', '_').replace('"', '')

    def probe_file(self, filename):
        cmnd = [
            'ffprobe',
            '-loglevel',
            'quiet',
            '-show_format',
            '-show_streams',
            '-select_streams',
            'a',
            '-print_format',
            'json',
            filename,
        ]
        p = subprocess.Popen(cmnd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        if err:
            print(err)
        else:
            return (out)

    def process(self, queue):

        while True:
            global logger

            filename = queue['filename']

            isWav = filename.index('wav') > -1

            info = self.probe_file(queue['path'])

            if info:
                data = json.loads(info.decode('utf-8'))
                format = data['format']
                stream = data['streams'][0]

                if 'bits_per_raw_sample' in stream:
                    bits = stream['bits_per_raw_sample']
                else:
                    bits = stream['bits_per_sample']

                bits_per_sample = int(bits)
                sample_rate = int(stream['sample_rate'])

                if 'tags' in format and 'ARTIST' in format['tags']:

                    print(format['tags'])
                    print(filename)

                    tags = format['tags']
                    artist = tags['ARTIST']
                    title = tags['TITLE']
                    album = tags.get('ALBUM', '')

                    directory = os.path.join(queue['dest'], artist,
                                             self.cleanDirectoryName(album))

                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    filename = os.path.join(directory,
                                            '{0}-{1}-{2}.wav'.format(self.cleanWhiteSpace(artist),
                                                                     self.cleanWhiteSpace(
                                                                         title),
                                                                     self.cleanWhiteSpace(album)))
                else:
                    if not os.path.exists(queue['dest']):
                        os.makedirs(queue['dest'])
                    filename = os.path.join(queue['dest'],
                                            queue['filename'])

                tfm = sox.Transformer()

                if bits_per_sample != 16 or sample_rate > 48000:
                    # check for 24bit or higher sample rates than 48k but don't
                    # convert anything less than 48k
                    new_sample_rate = sample_rate

                    if sample_rate > 48000:
                        new_sample_rate = 48000

                    logger.info('Converting From bit_depth: {0} sample_rate: {1}'.format(bits_per_sample,
                                                                                         sample_rate))
                    tfm.convert(new_sample_rate, 2, 16)

                logger.info('Converting {0} to {1} '.format(queue['filename'
                                                                  ], filename))

                tfm.build(queue['path'], filename)

                return True


converter = Flac2Wav()

#converter.convert("..//mnt/d/RekordBox/queue/", "/mnt/d/RekordBox/ElectroSet/")
#flac_folder = '/home/alvin/git_repository/cei_voice_converter/data1'
#flac_folder = '/home/alvin/git_repository/cei_voice_converter/.data/wav48_silence_trimmed/p225'
flac_folder = '/home/alvin/git_repository/cei_voice_converter/data1'
wav_folder = '/home/alvin/git_repository/cei_voice_converter/data2'
converter.convert(flac_folder,wav_folder)