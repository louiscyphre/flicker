import numpy as np
import argparse
import cv2
import random as rnd
import resource

resource.setrlimit(resource.RLIMIT_AS, (8589934592,8589934592))

def add_same_frame(queue, frame, minBound=1, maxBound=5):
	N = rnd.randint(minBound, maxBound)
	i = 0
	while i < N:
		queue.append(frame)
		i +=1

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
orig = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

minSize = 0
maxSize = 3
thresholdValue = 25
rounds = 500
subsetRatio = 40
fps = 30
outputFilename = 'sky.mp4'

height, width, layers = orig.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(outputFilename, fourcc, fps, (width,height))

th, threshed = cv2.threshold(gray, thresholdValue, 255,
		  cv2.THRESH_BINARY)#|cv2.THRESH_OTSU)
contours = cv2.findContours(threshed, cv2.RETR_LIST,
				    cv2.CHAIN_APPROX_SIMPLE)[-2]

sizedContours = []

for contour in contours:
	if minSize < cv2.contourArea(contour) < maxSize:
		sizedContours.append(contour)

frames = []
for x in range(rounds):
	output = orig.copy()

	subsetSize = rnd.randrange(len(sizedContours)//
								   rnd.randint(width//subsetRatio,
											   (width//subsetRatio)*2))
	sizedContoursSubset = rnd.sample(sizedContours, subsetSize)
	print("Subset has: ", {len(sizedContoursSubset)}, " elements")
	for n in sizedContoursSubset:

		color = list(np.random.random(size=3) * 256)

		outputCopy = output.copy()

		cv2.drawContours(outputCopy, n, -1, color, 1)
		frames.append(outputCopy)

		output = outputCopy.copy()

	for frame in frames:
		video.write(frame)

	frames = frames[::-1]

	for frame in frames:
		video.write(frame)

	frames = []

cv2.destroyAllWindows()
video.release()

cv2.waitKey(0)
