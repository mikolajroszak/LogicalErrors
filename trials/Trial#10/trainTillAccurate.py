import os
import datetime
import tensorflow as tf
import numpy as np
import json

def train():
	#-------------------------------------------------------------------------------------------------------------------------------------#

	#--------------------------------------STEP 1. PREPARE THE TRAINING AND TEST SETS-----------------------------------------------------#

	#-------------------------------------------------------------------------------------------------------------------------------------#

	input_data_list = []
	output_data_list = []

	# 1.1 Read the text file and load it as list of lists.

	with open('Sequence.txt') as fp:				#----> Open the file containing the sequence of numbers for all the training programs.
		for line in fp:								#----> Every line contains the sequence for one program.
			sequence = json.loads(line)				#----> Convert the text into list data type.
			length = len(sequence)						
			for i in range(length-1):				#----> The sequence [1, 2, 3, 4, 5] is split into the sequences [1] o/p 2, [1, 2] o/p 
				input_data_list.append(sequence[:i+1])	#----> 3, [1, 2, 3] o/p 4 and [1, 2, 3, 4] o/p 5.
				output_data_list.append(sequence[i+1])	

	# 1.2 Convert the input data from list of lists to 2D numpy array of fixed size
	maxlength = len(input_data_list[0])
	for i in input_data_list:
		l = len(i)
		if maxlength<l:
			maxlength = l

	
	# 1.3 Convert the output data from integer list to binary list of list

	output_binary_list = []
	for i in output_data_list:							#----> The number 5 is converted to [0, 0, 0, 0, 0, 1, 0, 0, .... , 0] (68 classes)
		temp_list = [0]*68
		temp_list[i] = 1
		output_binary_list.append(temp_list)

	output_data_array = np.asarray(output_binary_list)	#----> List is converted to array

	

	
	
	#------------------------------------------------------------------------------------------------------------------------------------#
	
	#------------------------------------------STEP 2. PREPARE TEST SETS-----------------------------------------------------------------#
	
	#------------------------------------------------------------------------------------------------------------------------------------#
	
	test_input = []
	test_output = []
	
	# 2.1 Load the sequences into lists
	with open("InputSequence.txt") as fp:
		for line in fp:
			sequence = json.loads(line)
			test_length = len(sequence)						
			for i in range(test_length-1):					 
				test_input.append(sequence[:i+1])	
				test_output.append(sequence[i+1])
	
	for i in test_input:
		l = len(i)
		if maxlength<l:
			maxlength = l

	for i in test_input:
		l = len(i)
		i+=([0,]*(maxlength-l))
	
	for i in input_data_list:
		l = len(i)
		i+=([0,]*(maxlength-l))							#----> For all sequences other than the longest, fill zeroes at the end

	input_data_array = np.asarray(input_data_list)		#----> Convert into numpy array
	length = len(input_data_array)
	assert(length == len(output_data_array))
	dataset = np.reshape(input_data_array, (len(input_data_array), maxlength, 1))

	test_length = len(test_input)
	assert(test_length == len(test_output))
	test = np.reshape(test_input, (len(test_input), maxlength, 1))
	

	#-------------------------------------------------------------------------------------------------------------------------------------#

	#-----------------------------------------------STEP 3. DESIGN THE RNN----------------------------------------------------------------#

	#-------------------------------------------------------------------------------------------------------------------------------------#

	# 3.1 Configure training data characteristics

	with tf.name_scope("inputs"):
		data = tf.placeholder(tf.float32, [None, maxlength, 1], name="training_x")	
		target = tf.placeholder(tf.float32, [None, 68], name="training_y")	#---> 1 - no. of dimensions, 68 - number of classes

	num_hidden = 600														#----> Number of hidden cells/hidden layers

	# 3.2 Configure the LSTM cell

	cell = tf.nn.rnn_cell.LSTMCell(num_hidden, state_is_tuple=True)			#---> tf.nn.rnn_cell.LSTMCell.__init__(num_units, input_size=None, use_peepholes=False, cell_clip=None, initializer=None, num_proj=None, num_unit_shards=1, num_proj_shards=1, forget_bias=1.0, state_is_tuple=False, activation=tanh)

	# 3.3 Configure the RNN for the LSTM

	val, state = tf.nn.dynamic_rnn(cell, data, dtype=tf.float32)			#---> tf.nn.dynamic_rnn(cell, inputs, sequence_length=None, initial_state=None, dtype=None, parallel_iterations=None, swap_memory=False, time_major=False, scope=None)

	# 3.4 Convert the result to desired form

	val = tf.transpose(val, [1, 0, 2])
	last = tf.gather(val, int(val.get_shape()[0])-1)

	# 3.5 Allocate space for weights and biases

	with tf.name_scope("layers"):	
		weights = tf.Variable(tf.truncated_normal([num_hidden, int(target.get_shape()[1])]), name="weights")	
		#---> truncated_normal is used to generate random numbers with normal distribution, to a vector of size num_hidden * number of classes
	
		biases = tf.Variable(tf.constant(0.1, shape=[target.get_shape()[1]]), name="biases")

	# 3.6 Configure the Prediction function

	prediction = tf.nn.softmax(tf.matmul(last, weights)+biases, name="prediction")	#---> tf.nn.softmax(logits, dim=-1, name=None)

	# 3.7 Calculate cross entropy

	cross_entropy = -tf.reduce_sum(target * tf.log(prediction), name="cross_entropy")	#---> tf.reduce_sum(input_tensor, axis=None, keep_dims=False, name=None, reduction_indices=None) Calculates the sum of the tensor, Adding the log term helps in penalizing the model more if it is terribly wrong and very little when the prediction is close to the target

	# 3.8 Configure the Optimizer

	with tf.name_scope("optimizer"):
		optimizer = tf.train.AdamOptimizer(learning_rate=0.0001)				#---> tf.train.AdamOptimizer.__init__(learning_rate=0.001, 
		minimize = optimizer.minimize(cross_entropy)		#---> beta1=0.9, beta2=0.999, epsilon=1e-08, use_locking=False, name='Adam')
	
	mistakes = tf.not_equal(tf.argmax(output_data_array, 1), tf.argmax(prediction, 1))
	error = tf.reduce_mean(tf.cast(mistakes, tf.float32))

	# 3.9 Configure the initialize all variables function

	init_op = tf.initialize_all_variables()

	#-------------------------------------------------------------------------------------------------------------------------------------#

	#------------------------------------------------STEP 4. EXECUTION--------------------------------------------------------------------#

	#-------------------------------------------------------------------------------------------------------------------------------------#

	# 4.1 Create a tensor flow session
	sess = tf.Session()

	# 4.2 Create the graph summary writer
	writer = tf.train.SummaryWriter("logs/",sess.graph)

	# 4.3 Run init_op function
	sess.run(init_op)
	if(os.path.isfile("weights.txt")):
		weights=[]
		WeightsFile = open("weights.txt", "r")
		for line in WeightsFile:
			weights.append(np.asarray(json.loads(line)))
		i=0
		for v in tf.trainable_variables():
			sess.run(v.assign(weights[i]))		#------> Assign the weights from file to the trainable variables
			i=i+1
		WeightsFile.close()
	batch_size = len(dataset)
	no_of_batches = int(len(dataset) / batch_size)
	start_time = datetime.datetime.now()
	print("Execution starts at "+str(start_time))
	print("Prepared number of batches: "+str(no_of_batches))
	temp_file = open("record.txt", "w");
	epoch=0
	accuracy=0
	enough = False
	TrainedCount = 0
	incorrect=100
	while((incorrect*100)>=float(2)):
		towrite = "Running epoch "+str(epoch)+"..."
		print(towrite)
		temp_file.write(towrite+"\n")
		ptr = 0
		for j in range(no_of_batches):
			inp, out = dataset[ptr:ptr+batch_size], output_data_array[ptr:ptr+batch_size]
			ptr+=batch_size
			sess.run(minimize,{data: inp, target: out})
		
		print("Minimization over")
		result=sess.run(prediction, {data: test})
		total=0;
		correct=0;
		predicted=[]
		for i in range(0, test_length):
			sublength = len(result[i])
			assert(sublength==68)
			copy_list = list(result[i])
			copy_list.sort()
			temp = []
			j=len(copy_list)-1
			count=0
			while(count<=2 and j>=0):
				indices = [k for k, x in enumerate(result[i]) if x==copy_list[j]]
				temp+=indices
				j = j-1
				count=count+1
			predicted.append(temp)
		# Calculate accuracy
		assert(len(predicted)==test_length)
		for i in range(0, test_length):
			if(test_output[i] in predicted[i]):
				correct+=1
		accuracy = float(correct/test_length) * 100
		if(accuracy==float(100)):
			TrainedCount=TrainedCount+1
		if(TrainedCount>5):
			enough = True
		print(str(accuracy))
		temp_file.write(str(accuracy)+"\n")
		#print(str(accuracy))
		
		incorrect = sess.run(error,{data: dataset, target: output_data_array})
		print(str(incorrect*100))
		current = datetime.datetime.now()
		timelapse = current-start_time
		print(timelapse)
		epoch=epoch+1

	WeightsFile = open("weights.txt", "w")
	trainable_variables = [v.name for v in tf.trainable_variables()]
	values = sess.run(trainable_variables)
	WeightsFile.flush()
	for k,v in zip(trainable_variables, values):
		temp = v.tolist()			#------> Numpy array is not json serializable. Hence, convert it into list.
		json.dump(temp, WeightsFile)
		WeightsFile.write("\n")
	WeightsFile.close()
