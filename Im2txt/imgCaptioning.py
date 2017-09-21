import math
import os


import tensorflow as tf

from im2txt import configuration
from im2txt import inference_wrapper
from im2txt.inference_utils import caption_generator
from im2txt.inference_utils import vocabulary

# Directory containing model checkpoints.
CHECKPOINT_DIR="/home/oleg/Desktop/ImageCaptioning/im2txt/model"

# Vocabulary file generated by the preprocessing script.
VOCAB_FILE="/home/oleg/Desktop/ImageCaptioning/im2txt/im2txt/data/word_counts.txt"

# JPEG image file to caption. NOT USED
IMAGE_FILE="/home/oleg/Desktop/ImageCaptioning/im2txt/im2txt/data/images1.jpeg"

class imgCap(object):
	def __init__(self):
		g = tf.Graph()
		with g.as_default():
			model = inference_wrapper.InferenceWrapper()
			restore_fn = model.build_graph_from_config(configuration.ModelConfig(), CHECKPOINT_DIR)
	    	
		g.finalize()

		# Create the vocabulary.
		self.vocab = vocabulary.Vocabulary(VOCAB_FILE)
		gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.25, visible_device_list="0")
		#config=tf.ConfigProto(gpu_options=gpu_options, device_count = {'GPU': 2})
		#config.gpu_options.allow_growth = False

		config=tf.ConfigProto(gpu_options=gpu_options)
	                
		self.sess = tf.Session(graph=g, config = config)
		restore_fn(self.sess)
		self.generator = caption_generator.CaptionGenerator(model, self.vocab)

	def feed_image(self, path):
		fileGlob = tf.gfile.Glob(path)
		f = tf.gfile.GFile(fileGlob[0], "r")
		image = f.read()
		f.close()
		captions = self.generator.beam_search(self.sess, image)

		answers = []
		for i, caption in enumerate(captions):
			# Ignore begin and end words.
			sentence = [self.vocab.id_to_word(w) for w in caption.sentence[1:-1]]
			sentence = " ".join(sentence)
			answers.append(sentence)
			print("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)))

		return answers[0]

