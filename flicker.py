# import the necessary packages
import numpy as np
import argparse
import cv2
import random
import resource

resource.setrlimit(resource.RLIMIT_AS, (6442450944,6442450944))

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
orig = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

minSize = 0
maxSize = 15
thresholdValue = 25
rounds = 20
fps = 10
outputFilename = 'tests/sky.mp4'

th, threshed = cv2.threshold(gray, thresholdValue, 255,
          cv2.THRESH_BINARY)#|cv2.THRESH_OTSU)
contours = cv2.findContours(threshed, cv2.RETR_LIST,
                    cv2.CHAIN_APPROX_SIMPLE)[-2]

sized_contours = []

for contour in contours:
    if minSize < cv2.contourArea(contour) < maxSize:
        sized_contours.append(contour)

frames = []
for x in range(rounds):
		output = orig.copy()
		not_reversed_frames = []
		reversed_frames = []

		sizedContoursUpdatedList = random.sample(sized_contours, random.randrange(len(sized_contours)//random.randint(16,32)))
		for y in sizedContoursUpdatedList:
			color = list(np.random.random(size=3) * 256)
			output = cv2.drawContours(output, y, -1, color, 1)

			#N = random.randint(1,3)
			#i = 0
			#while i < N:
			not_reversed_frames.append(output)
			#	i +=1

		#N = random.randint(1,5)
		#i = 0
		#while i < N:
		#	not_reversed_frames.append(output)
		#	i +=1

		frames += not_reversed_frames
		reversed_frames = not_reversed_frames[::-1]
		frames += reversed_frames

		not_reversed_frames = []
		reversed_frames = []

		output = None

height, width, layers = orig.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(outputFilename, fourcc, fps, (width,height))

for frame in frames:
	video.write(frame)

cv2.destroyAllWindows()
video.release()

cv2.waitKey(0)
