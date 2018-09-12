import numpy as np
import tensorflow as tf

def add_layer(inputs,in_size,out_size,activation_funcition=None):
    with tf.name_scope("layer"):
        with tf.name_scope("weights"):
            Weights=tf.Variable(tf.random_normal([in_size,out_size]))
        with tf.name_scope("bias"):
            biases=tf.Variable(tf.zeros([1,out_size]+0.1))
        Wx_plus_b=tf.add(tf.matmul(inputs,Weights),biases)
        if activation_funcition is None:
            outputs=Wx_plus_b
        else:
            outputs=activation_funcition(Wx_plus_b)
        return outputs
with tf.name_scope("inputs"):
    xs=tf.placeholder(tf.float32,[None,1],name="x_input")
    ys=tf.placeholder(tf.float32,[None,1],name="y_input")

l1=add_layer(xs,1,10,activation_funcition=tf.nn.relu)
prediction=add_layer(l1,10,1,activation_funcition=None)

loss=tf.reduce_mean(tf.reduce_sum(tf.square(ys-prediction)),reduction_indices=[1])
train_step=tf.train.GradientDescentOptimizer(0.1).minimize(loss)

sess=tf.Session()
writer=tf.train.SummaryWriter("logs/",sess.graph)
sess.run(tf.initialize_all_variables())