# Script to download youtube video at url and trim it to the specified length

import argparse
import os
import subprocess
from arrow.parser import ParserError
import arrow

def get_time(time):
	formats = [
	'HH:mm:ss',
	'H:mm:ss',
	'mm:ss',
	'm:ss',
	'ss',
	's'
	]

	for format in formats:
		try:
			print(format)
			time = arrow.get(time, format)
			break
		except ParserError:
			continue
	return time
	

def cut_video(startTime, endTime, filename, audio_only=False):
	# only support mp3 audio output
	if (audio_only):
		outfile = 'out_' + os.path.splitext(filename)[0] + '.mp3'
	else:
		outfile = 'out_' + filename
	
	os.system('ffmpeg -i %s -ss %s -to %s -async 1 %s' % (filename, startTime, endTime, outfile))

def download_video(url):
	cmd = ['youtube-dl', url, '--get-filename', '--restrict-filenames']
	output = subprocess.Popen(cmd, stdout = subprocess.PIPE).stdout.read()
	output = output.decode('utf-8')
	

	output = output.split('\r\n')
	assert(len(output) == 1)
	filename = output[0]
	filename = filename.strip()
	#output = subprocess.Popen('youtube-dl %s --get-filename' % url, stdout = subprocess.PIPE).stdout.read()
	
	print(output)

	if (not os.path.isfile(filename)):
		cmd = ['youtube-dl', url, '--restrict-filenames']
		output = subprocess.Popen(cmd, stdout = subprocess.PIPE).stdout.read()
	
	return filename


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('url', help='The video url for downloading')
	parser.add_argument('st', help='The start time')
	parser.add_argument('et', help='The end time')
	parser.add_argument('--audio', action='store_true', default=False, help='Audio only in mp3 format')
	args = parser.parse_args()

	startTime = args.st
	startTime = get_time(startTime)
	endTime = args.et
	endTime = get_time(endTime)
	audioOnly = args.audio

	print ('Start = %s, end = %s' % (startTime, endTime))

	assert(endTime > startTime)

	#duration = endTime - startTime
	#print(duration)

	startTime = startTime.datetime.strftime('%H:%M:%S')
	endTime = endTime.datetime.strftime('%H:%M:%S')
	print ('Start = %s, end = %s' % (startTime, endTime))

	filename = download_video(args.url)
	cut_video(startTime, endTime, filename, audioOnly)


