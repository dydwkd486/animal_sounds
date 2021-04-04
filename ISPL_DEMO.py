import os
#os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import numpy as np
import h5py
import scipy.io as sio
import matplotlib as mpl
import matplotlib.pylab as plt
#from tensorflow.python.ops import spectral_ops
import librosa
from tensorflow.python.ops import array_ops

from multiprocessing import Process
import math
import threading
import time
import queue

Learnings='FIRST'
#import tensorflow_io as tfio

os.environ["CUDA_VISIBLE_DEVICES"]='0'
#tf.set_random_seed(777)

# Parameters
nClass = 115
GClass = 3
learning_rate = 0.0001
decay = .1
batch_size = 12

max_epoch = 50
ALPHA=0.5

PD=5

ALPHA=0.5

nBlock = 1      # matlab parameter
nChannel = 1    # matlab par ameter

gg=0
global g
g=batch_size
print(gg)
# Cross-Validation
TstFold = ['A']

#TstFold = [ 'A']
SNR=[15]

filterLength=160
head=4
dims=int(160/head)

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e)


def Resnet18P(self,w,inputs,name1):
    conv = tf.nn.conv2d(inputs, w["wc1"], strides=[1, 2, 2, 1], padding="SAME")
    conv = tf.nn.relu(tf.layers.batch_normalization(conv, training=self.phase_train,reuse=tf.AUTO_REUSE, name=name1))
    conv = tf.nn.max_pool(conv, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding="SAME")
    return conv

def Resnet18F(self,w,inputs,strid,name1,name2,name4):
    conv = tf.nn.conv2d(inputs, w["wc1"], strides=[1, strid, strid, 1], padding="SAME")
    conv = tf.nn.relu(tf.layers.batch_normalization(conv, training=self.phase_train,reuse=tf.AUTO_REUSE,name=name1))
    # 2nd convolutional layer
    conv = tf.nn.conv2d(conv, w["wc2"], strides=[1, 1, 1, 1], padding="SAME")
    conv = tf.nn.relu(tf.layers.batch_normalization(conv, training=self.phase_train,reuse=tf.AUTO_REUSE, name=name2))

    convr = tf.nn.conv2d(inputs, w["wc3"], strides=[1, strid, strid, 1], padding="SAME")
    convr = tf.nn.relu(tf.layers.batch_normalization(convr, training=self.phase_train,reuse=tf.AUTO_REUSE, name=name4))

    return tf.add(conv,convr)


def Resnet18B(self,w,inputs,name1,name2):
    conv = tf.nn.conv2d(inputs, w["wc1"], strides=[1, 1, 1, 1], padding="SAME")
    conv = tf.nn.relu(tf.layers.batch_normalization(conv, training=self.phase_train,reuse=tf.AUTO_REUSE,name=name1))
    # 2nd convolutional layer
    conv = tf.nn.conv2d(conv, w["wc2"], strides=[1, 1, 1, 1], padding="SAME")
    conv = tf.nn.relu(tf.layers.batch_normalization(conv, training=self.phase_train,reuse=tf.AUTO_REUSE, name=name2))

    return tf.add(conv,inputs)
def prenet(w,inputs):
    inputs=tf.nn.relu(inputs/tf.reduce_max(inputs,[1,2,3],keep_dims=True))
    conv = (tf.nn.conv2d(inputs, w["wc1"],dilations=[1,7,7,1], strides=[1, 1, 1, 1], padding="SAME"))
    conv = tf.sigmoid(conv[:,:,:,0:32])*conv[:,:,:,32:]
    conv = (tf.nn.conv2d(conv, w["wc2"],dilations=[1,5,5,1], strides=[1, 1, 1, 1], padding="SAME"))
    conv = tf.sigmoid(conv[:, :, :, 0:64]) * conv[:, :, :, 64:]
    conv = tf.nn.relu(tf.nn.conv2d(conv, w["wc3"],dilations=[1,3,3,1], strides=[1, 1, 1, 1], padding="SAME"))
    conv = tf.sigmoid(conv[:, :, :, 0:128]) * conv[:, :, :, 128:]
    conv = tf.nn.relu(tf.nn.conv2d(conv, w["wc4"],dilations=[1,1,1,1], strides=[1, 1, 1, 1], padding="SAME"))

    mean, vars = tf.nn.moments(conv, [1,2], keep_dims=True)
    norm2 = tf.nn.batch_normalization(conv, mean, vars, w["a"],w["b"], 0.001)
    mask = tf.sigmoid(tf.nn.conv2d(norm2, w["wc5"], dilations=[1, 1, 1, 1], strides=[1, 1, 1, 1], padding="SAME"))
    return mask

class Model:
    def __init__(self, name):
        with tf.variable_scope(name):
            # Place holders
            self.X = tf.placeholder(tf.float32, [None,None], name='X')
            self.Y = tf.placeholder(tf.float32, [None,nClass], name='Y')
            self.Z = tf.placeholder(tf.float32, [None,None], name='Z')
            self.phase_train = tf.placeholder(tf.bool,name='phase_train')

            self.weights0 = {
                "wc1": tf.Variable(tf.truncated_normal([3, 3, 1, 64], stddev=0.01), name="wc10"),
                "wc2": tf.Variable(tf.truncated_normal([3, 3, 32, 128], stddev=0.01), name="wc20"),
                "wc3": tf.Variable(tf.truncated_normal([3, 3, 64, 256], stddev=0.01), name="wc30"),
                "wc4": tf.Variable(tf.truncated_normal([3, 3, 128, 256], stddev=0.01), name="wc40"),
                "wc5": tf.Variable(tf.truncated_normal([1, 1, 256, 1], stddev=0.01), name="wc50"),
                "a": tf.Variable(tf.truncated_normal([1, 1, 1, 256], stddev=0.01), name="a0"),
                "b": tf.Variable(tf.truncated_normal([1, 1, 1, 256], stddev=0.01), name="b0"),
            }



            self.centroids = tf.Variable(tf.truncated_normal([nClass, 64], stddev=0.01), name="cen")
            self.centroids_delta = tf.Variable(tf.truncated_normal([nClass, 64], stddev=0.01), name="cen_del")

            self.weights1 = {
                "wc1": tf.Variable(tf.truncated_normal([7, 7, 1, 64], stddev=0.01), name="wc11",trainable=False)

            }
            self.weights21 = {
                # filter_hight, filter_width, input channels , numfilter
                "wc1": tf.Variable(tf.truncated_normal([3, 3, 64, 64], stddev=0.01), name="wc1",trainable=False),
                "wc2": tf.Variable(tf.truncated_normal([3, 3, 64, 64], stddev=0.01), name="wc2",trainable=False),
                "wc3": tf.Variable(tf.truncated_normal([1, 1, 64, 64], stddev=0.01), name="wc3",trainable=False),
            }

            self.weights22 = {
                # filter_hight, filter_width, input channels , numfilter
                "wc1": tf.Variable(tf.truncated_normal([3, 3, 64, 64], stddev=0.01), name="wc1",trainable=False),
                "wc2": tf.Variable(tf.truncated_normal([3, 3, 64, 64], stddev=0.01), name="wc2",trainable=False),
            }

            self.weights31 = {
                # filter_hight, filter_width, input channels , numfilter
                "wc1": tf.Variable(tf.truncated_normal([3, 3, 64, 128], stddev=0.01), name="wc1",trainable=False),
                "wc2": tf.Variable(tf.truncated_normal([3, 3, 128, 128], stddev=0.01), name="wc2",trainable=False),
                "wc3": tf.Variable(tf.truncated_normal([1, 1, 64, 128], stddev=0.01), name="wc3",trainable=False)
            }

            self.weights32 = {
                # filter_hight, filter_width, input channels , numfilter
                "wc1": tf.Variable(tf.truncated_normal([3, 3, 128, 128], stddev=0.01), name="wc1",trainable=False),
                "wc2": tf.Variable(tf.truncated_normal([3, 3, 128, 128], stddev=0.01), name="wc2",trainable=False)
            }

            self.weights41 = {
                # filter_hight, filter_width, input channels , numfilter
                "wc1": tf.Variable(tf.truncated_normal([3, 3, 128, 256], stddev=0.01), name="wc1",trainable=False),
                "wc2": tf.Variable(tf.truncated_normal([3, 3, 256, 256], stddev=0.01), name="wc2",trainable=False),
                "wc3": tf.Variable(tf.truncated_normal([1, 1, 128, 256], stddev=0.01), name="wc3",trainable=False)
            }

            self.weights42 = {
                # filter_hight, filter_width, input channels , numfilter
                "wc1": tf.Variable(tf.truncated_normal([3, 3, 256, 256], stddev=0.01), name="wc1",trainable=False),
                "wc2": tf.Variable(tf.truncated_normal([3, 3, 256, 256], stddev=0.01), name="wc2",trainable=False)
            }

            self.weights51 = {
                # filter_hight, filter_width, input channels , numfilter
                "wc1": tf.Variable(tf.truncated_normal([3, 3, 256, 512], stddev=0.01), name="wc1",trainable=False),
                "wc2": tf.Variable(tf.truncated_normal([3, 3, 512, 512], stddev=0.01), name="wc2",trainable=False),
                "wc3": tf.Variable(tf.truncated_normal([1, 1, 256, 512], stddev=0.01), name="wc3",trainable=False)
            }

            self.weights52 = {
                # filter_hight, filter_width, input channels , numfilter
                "wc1": tf.Variable(tf.truncated_normal([3, 3, 512, 512], stddev=0.01), name="wc1",trainable=False),
                "wc2": tf.Variable(tf.truncated_normal([3, 3, 512, 512], stddev=0.01), name="wc2",trainable=False)
            }

            self.FC = {
                "wc1": tf.Variable(tf.truncated_normal([512, 64], stddev=0.01), name="wc1",trainable=False),
                "wc2": tf.Variable(tf.truncated_normal([64, nClass], stddev=0.01), name="wc2",trainable=False),
            }
            self.biases = {
                "bf1": tf.Variable(tf.constant(1.0, shape=[64]), name="bf1",trainable=False),
                "bf2": tf.Variable(tf.constant(1.0, shape=[nClass]), name="bf2",trainable=False),
            }
            self.FC1 = {
                "wc1": tf.Variable(tf.truncated_normal([1, 1, 256, 1], stddev=0.01), name="wc1",trainable=False)
            }




            spec = self.X


            spec = tf.contrib.signal.stft(signals=spec, frame_length=512, frame_step=256, fft_length=512,
                                           window_fn=tf.contrib.signal.hamming_window)

            spec = tf.abs(spec)

            mask=tf.squeeze(prenet(self.weights0,tf.expand_dims(spec,3)),3)
            spec=spec*mask


            #spec=(spec-tf.reduce_min(spec,[1,2],keep_dims=True))/(tf.reduce_max(spec,[1,2],keep_dims=True)-tf.reduce_min(spec,[1,2],keep_dims=True))

            mel_weithf = tf.contrib.signal.linear_to_mel_weight_matrix(128, 257, 22050, 50, 11025, tf.float32)##
            t=tf.shape(spec)
            mel_weithf=tf.expand_dims(mel_weithf,0)
            mel_weithf=tf.tile(mel_weithf,[t[0],1,1])

            spec = tf.matmul(spec, mel_weithf)

            mean,vars=tf.nn.moments(spec,[1],keep_dims=True)

            spec=tf.nn.batch_normalization(spec,mean,vars,0,1,0.001)



            spec1 = self.Z

            spec1 = tf.contrib.signal.stft(signals=spec1, frame_length=512, frame_step=256, fft_length=512,
                                           window_fn=tf.contrib.signal.hamming_window)

            spec1 = tf.abs(spec1)

            mask=tf.squeeze(prenet(self.weights0,tf.expand_dims(spec1,3)),3)
            spec1=spec1*mask




            spec1 = tf.matmul(spec1, mel_weithf)
            mean,vars=tf.nn.moments(spec1,[1],keep_dims=True)

            spec1=tf.nn.batch_normalization(spec1,mean,vars,0,1,0.001)
            #spec=(tf.log(spec+0.001))



            spec2=tf.concat([tf.expand_dims(spec,3),tf.expand_dims(spec1,3)],0)
            x0 = Resnet18P(self, self.weights1, spec2, "cov11")
            # x0 = tf.nn.dropout(x0, 0.5)
            x1 = Resnet18F(self, self.weights21, x0, 1, "cov21", "cov22", "SK1")
            x2 = Resnet18B(self, self.weights22, x1, "cov24", "cov25")

            x3 = Resnet18F(self, self.weights31, x2, 2, "cov31", "cov32", "SK2")
            x4 = Resnet18B(self, self.weights32, x3, "cov34", "cov35")

            x5 = Resnet18F(self, self.weights41, x4, 2, "cov41", "cov42", "SK3")
            x6 = Resnet18B(self, self.weights42, x5, "cov44", "cov45")

            x7 = Resnet18F(self, self.weights51, x6, 2, "cov51", "cov52", "SK4")
            x8 = Resnet18B(self, self.weights52, x7, "cov54", "cov55")
            #x8 = tf.nn.dropout(x8, 0.5)

            #means, vars = tf.nn.moments(x8, [1, 2])
            #Feat = tf.concat([means, tf.sqrt(vars + 0.000001)], 1)
            Feat=tf.reduce_mean(x8,[1,2])

            Feat_shap=tf.shape(Feat)
            Feat_known=Feat[0:tf.cast(Feat_shap[0]/2,dtype=tf.int32),:]


            #Feat_shap=tf.shape(Feat)
            #Feat_known=Feat[0:tf.cast(Feat_shap[0]/2,dtype=tf.int32),:]



            x8=x8[:,:,:,0:256]*tf.sigmoid(x8[:,:,:,256:])
            conv = tf.nn.conv2d(x8, self.FC1["wc1"], strides=[1, 1, 1, 1], padding="SAME")
            conv = tf.sigmoid(conv)*conv
            self.conv = (tf.reduce_mean(conv,[1,2,3]))

            self.conv2=tf.sigmoid(self.conv)




            fc1 = (tf.nn.xw_plus_b(Feat_known, self.FC["wc1"], self.biases["bf1"], name="fc1"))
            self.fc1= tf.sigmoid(fc1)*fc1
            fc2 = (tf.nn.xw_plus_b(self.fc1, self.FC["wc2"], self.biases["bf2"], name="fc2"))
            self.slogits = fc2
            self.pr=tf.reduce_max(tf.nn.softmax(self.slogits))

            self.slabel = tf.argmax(self.slogits, 1)


class Solver:
    def __init__(self,sess,model):
        self.model = model
        self.sess = sess


    def evaluate_dev(self,X):
        feed = {
            self.model.X: X,
            self.model.Z: X,
            self.model.phase_train: False
        }
        scorrect_prediction = self.model.slabel
        tcorrect_prediction = self.model.conv2
        pre=self.model.pr
        return self.sess.run([scorrect_prediction,tcorrect_prediction,pre], feed_dict=feed)

def Animal_log(audio_path,Check_point_path,thread_unknown=0.5,thread_class=0.5):
    with tf.Session() as sess:

        model_A = Model('A')
        model_A_solver = Solver(sess, model_A)
        sess.run(tf.global_variables_initializer())
        ii=1;

        saver = tf.train.Saver(max_to_keep=1, var_list=tf.global_variables())
        saver.restore(sess,tf.train.latest_checkpoint(Check_point_path))
        # if Learnings != 'FIRST':
        #    saver_re = tf.train.import_meta_graph(CKT_re_path)
        logPath = './Animal.log'
        log_fp = open(logPath, 'w')
        #Frogdemo
        #Birddemo
        myrecording, sr = librosa.load(audio_path,sr=22050)
        audio_length=len(myrecording)
        #sf.write(paths, myrecording, 44100)
        class_list = open("./list_115.txt", 'r')
        myrecording=np.expand_dims(myrecording,0)
        lists = []
        for i6 in range(nClass):
            classes = class_list.readline()
            lists.append(classes)
        lists = np.block(lists)
        lists = list(map(lambda s: s.strip(), lists))
        #duration=8
        a=time.time()
        temps=np.mod(audio_length,22050)
        myrecording=np.concatenate([myrecording,np.zeros([1,22050-temps])],1)
        tt=np.shape(myrecording)
        Nchunk=np.floor(tt[1]/22050)
        file_size = Nchunk * 2 - 1
        outputs=[]
        file_size = np.asarray(file_size, dtype=np.int32)

        for i in range(file_size):
            inputs=myrecording[:, i * 11025:((i) * 11025+22050)]
            out,reg,pre= model_A_solver.evaluate_dev(inputs)

            print('Time: ,{0:0.6f}',time.time()-a)
            Sc=np.asarray(out,dtype=np.int32)
            Sc=Sc[0]

            #Sc=np.squeeze(Sc-np.mean(Sc)/(np.var(Sc)+0.001))
            print(reg[0])
            if reg[0]<thread_unknown:
                state='blank'
                print(state)
            else:
                if pre<thread_class:
                    state = 'blank'
                else:
                    print(pre)
                    temp=lists[Sc]
                    state=str(temp)
                    print(state)
            outputs.append(state)
            log = '[Step {0:2d}] ,Time: {1:.4f} Sec ,Target: {2:s}\n'.format((i + 1), (i + 1) * 0.5, state)
            print(log)
            log_fp.write(log)
    return outputs




