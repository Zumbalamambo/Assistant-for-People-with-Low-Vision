from PIL import Image
import pytesseract

filepath = "/home/richard/Desktop/menu_recognition/test.jpg"

class ReadText:

   def __init__(self):
      pass

   def read(self, filepath):
	response = pytesseract.image_to_string(Image.open(filepath),lang='eng')
	print response
      # for testing
      #text_file = open("text.txt", "w") 
      #text_file.write(response)
	return response

#reader = ReadText()
#reader.read(filepath)

#input_image=args[0]

#print "Input image =" + filepath




#import os
#import sys
#import subprocess
#import pdb
#from langdetect import detect_langs

#call tesseract from terminal
#subprocess.call("tesseract "+input_image+" kor_out -l kor", shell=True)
'''subprocess.call("tesseract "+input_image+" eng_out -l eng", shell=True)

#read contect to the file where it outputs
#kor_out_file = open("kor_out.txt","r")
eng_out_file = open("eng_out.txt","r")

#kor_out_text = kor_out_file.read()
#eng_out_text = eng_out_file.read()
#kor_out_text_list = [line.decode('utf-8').strip() for line in kor_out_file.readlines()]
eng_out_text_list = [line.decode('utf-8').strip() for line in eng_out_file.readlines()]

#kor_out_text =  ' '.join(kor_out_text_list)
eng_out_text =  ' '.join(eng_out_text_list)

#kor_out_text = u' '.join(kor_out_text_list).encode('utf-8').strip()
#eng_out_text = u' '.join(eng_out_text_list).encode('utf-8').strip()


#kor_out_file.close()
eng_out_file.close()'''

#check probability to belong to english
#pdb.set_trace()
#try:
#   prob_kor = detect_langs(kor_out_text)
#except:
#   print "Language was not detected"
#   response = "Text was not detected"

#try:
#   prob_eng = detect_langs(eng_out_text)
#except:
#   print "Language was not detected"
#   response = "Text was not detected"

#if response == "Text was not detected":
#   text_file.write(response)
#   text_file.close()
#   print response
#
#else:
   #check probability to belong to korean
#   lang1_name = str(prob_kor[0]).split(':')[0]
#   lang1_prob = float(str(prob_kor[0]).split(':')[1])

#   lang2_name = str(prob_eng[0]).split(':')[0]
#   lang2_prob = float(str(prob_eng[0]).split(':')[1])

   #pdb.set_trace()
#   if (lang1_name==lang2_name):
#      print lang1_name
#      if (lang1_prob>lang2_prob):
#         response= (u"ko "+kor_out_text).encode('utf-8')
#      else:
#         response= (u"eng "+eng_out_text).encode('utf-8')
#   elif (lang1_prob>lang2_prob and lang1_name=='ko' and lang1_prob>0.95):
#      print "Korean"
#      response= (u"ko "+kor_out_text).encode('utf-8')
#   elif (lang1_prob<lang2_prob and lang2_name=='en' and lang2_prob>0.95):
#      print "English"
#      response= (u"eng "+eng_out_text).encode('utf-8')
#   else: 
#      response = "Not detected"

   #response= (u"Detected language is English \n"+eng_out_text).encode('utf-8')
   ##pdb.set_trace()
   #text_file.write(response)
   #text_file.close()
#
   #print response




#reader = ReadText()
#reader.read(filepath)