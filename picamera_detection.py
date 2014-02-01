import io
import time
import picamera
from PIL import Image

def checkForDifference(image1,buffer1,image2,buffer2):
    threshold = 10
    sensitivity = 20    
    # Count changed pixels
    changedPixels = 0
    for x in xrange(0, 100):
        for y in xrange(0, 75):
            # Just check green channel as it's the highest quality channel
            pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
            if pixdiff > threshold:
                changedPixels += 1

            # Save an image if pixels changed
    if changedPixels > sensitivity:
	print "Motion detected"
            # Swap comparison buffers
    image1 = image2
    buffer1 = buffer2

def getImage():
	stream = io.BytesIO()
	with picamera.PiCamera() as camera:
    		# The following is equivalent
		camera.resolution = camera.MAX_IMAGE_RESOLUTION
		camera.start_preview()
		time.sleep(2)
		camera.capture(stream,format="jpeg")
	stream.seek(0)
	image = Image.open(stream)
	buff = image.load()
	stream.close()
	return image, buff

def main():
	oldIm, oldBuf = getImage()
	print "Running..."
	newIm, newBuf = getImage()
	checkForDifference(oldIm,oldBuf,newIm,newBuf)
	oldIm, oldBuf = newIm, newBuf

if __name__ == "__main__":
	main()
