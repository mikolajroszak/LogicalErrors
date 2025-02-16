import tensorflow as tf
import numpy as np
import json

def predict():
	#-------------------------------------------------------------------------------------------------------------------------------------#

	#-----------------------------------------------STEP 1. PREPARE THE TEST SETS---------------------------------------------------------#

	#-------------------------------------------------------------------------------------------------------------------------------------#

	test_input = []
	test_output = []

	# 1.1 Read the text file and load it as list of lists.

	with open("InputSequence.txt") as fp:
		for line in fp:
			sequence = json.loads(line)
			length = len(sequence)						
			for i in range(length-1):					 
				test_input.append(sequence[:i+1])	
				test_output.append(sequence[i+1])	

	# 1.2 Convert the input data from list of lists of fixed size
	maxlength = len(test_input[0])
	for i in test_input:
		l = len(i)
		if maxlength<l:
			maxlength = l
	for i in test_input:
		l = len(i)
		i+=([0,]*(maxlength-l))

	length = len(test_input)
	print("Length of the test cases = ", length)
	assert(length == len(test_output))

	# 1.3 Convert the input list into 2D numpy array
	test = np.asarray(test_input)

	#-------------------------------------------------------------------------------------------------------------------------------------#

	#-----------------------------------------------STEP 2. CONFIGURE THE RNN-------------------------------------------------------------#

	#-------------------------------------------------------------------------------------------------------------------------------------#
	with tf.name_scope("inputs"):
		data = tf.placeholder(tf.float32, [None, maxlength, 1], name="training_x")
		target = tf.placeholder(tf.float32, [None, 47], name="training_y")
	num_hidden = 1

	cell = tf.nn.rnn_cell.LSTMCell(num_hidden, state_is_tuple=True)
	val, state = tf.nn.dynamic_rnn(cell, data, dtype=tf.float32)
	val = tf.transpose(val, [1, 0, 2])
	last = tf.gather(val, int(val.get_shape()[0])-1)
	with tf.name_scope("layers"):
		weights = tf.Variable(tf.truncated_normal([num_hidden, int(target.get_shape()[1])]), name="weights")
		biases = tf.Variable(tf.constant(0.1, shape=[target.get_shape()[1]]), name="biases")

	prediction = tf.nn.softmax(tf.matmul(last, weights)+biases, name="predict")
	saver = tf.train.Saver()
	sess = tf.Session()
	writer = tf.train.SummaryWriter("logs/",sess.graph)
	saver.restore(sess, "variables.ckpt")
	test = np.reshape(test, (length, maxlength, 1))
	result=sess.run(prediction, {data: test})
	assert(length == len(result))
	total=0;
	correct=0;
	predicted=[]
	result_file = open("result_file.txt", "w")
	for i in range(0, length):
		result_file.write("Case "+str(i)+":\n")
		json.dump(result[i].tolist(), result_file)
		result_file.write("\n")
		maxi = max(result[i])
		result_file.write("Max probability is: "+str(maxi)+"\n")
		sublength = len(result[i])
		assert(sublength==47)
		temp=[]
		for j in range(0, sublength):
			if(result[i][j]==maxi):
				temp.append(j)
		result_file.write("Classes with max probability: ")
		json.dump(temp, result_file)
		result_file.write("\n")
		predicted.append(temp)

	assert(len(predicted)==length)
	for i in range(0, length):
		if(test_output[i] in predicted[i]):
			correct+=1
		result_file.write(str(predicted[i])+" "+str(test_output[i])+"\n")

	accuracy = float(correct/length) * 100
	result_file.write("\nAccuracy is: "+str(accuracy))
