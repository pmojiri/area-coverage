#!/usr/bin/python
import cv2

class read_map:
  #def __init__(self):

  def read_file(self, filename):
      # read map file
      return cv2.imread(filename) # Read an image
    
  # Converts an RGB image to grayscale, where each pixel
  # now represents the intensity of the original image.
  ##
  def rgb_to_gray(self, image):
      return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

  ##
  # Converts an image into a binary image at the specified threshold.
  # All pixels with a value <= threshold become 0, while
  # pixels > threshold become 1
  def do_threshold(self, image, threshold):
      (thresh, im_bw) = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
      return (thresh, im_bw)

  def convert_to_binary(self, filename):
      #read map file
      self.img = self.read_file(filename)
      
      # If you have captured a frame from your camera like in the template program above,
      # you can create a bitmap from it as follows:
      self.img_gray = self.rgb_to_gray(self.img) # Convert img from RGB to Grayscale

      # Converts grayscale image to a binary image with a threshold value of 220. Any pixel with an
      # intensity of <= 220 will be black, while any pixel with an intensity > 220 will be white:
      (self.thresh, self.img_threshold) = self.do_threshold(self.img_gray, 220)

      cv2.imwrite("Grayscale_map.jpg", self.img_gray)
      cv2.imwrite("Threshold_map.jpg", self.img_threshold)
      return self.img_threshold
