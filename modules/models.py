import tensorflow as tf
import numpy as np
import h5py


# Parameters
nClass = 26
GClass = 3

dataPath1 = './par_save_26class/conv1.mat'
batPath1 = './par_save_26class/batch1.mat'
batPath2 = './par_save_26class/batch2.mat'
batPath3 = './par_save_26class/batch3.mat'
batPath4 = './par_save_26class/batch4.mat'
batPath5 = './par_save_26class/batch5.mat'
class_feature = './par_save_26class/Class_features.mat'

with h5py.File(class_feature) as cc:
    Feature_class = np.transpose(np.squeeze(np.array(cc['Feature_class'].value, dtype='float32')))

with h5py.File(dataPath1) as conv:
    wc1 = np.array(conv['conv1'].value, dtype='float32')
    wc2 = np.array(conv['conv2'].value, dtype='float32')
    wc3 = np.array(conv['conv3'].value, dtype='float32')
    wc4 = np.array(conv['conv4'].value, dtype='float32')
    wc5 = np.array(conv['conv5'].value, dtype='float32')
    wc1 = np.transpose(wc1, [3, 2, 1, 0])
    wc2 = np.transpose(wc2, [3, 2, 1, 0])
    wc3 = np.transpose(wc3, [3, 2, 1, 0])
    wc4 = np.transpose(wc4, [3, 2, 1, 0])
    wc5 = np.transpose(wc5, [3, 2, 1, 0])

with h5py.File(batPath1) as batch1:
    batch1_mean = tf.squeeze(np.array(batch1['mean'].value, dtype='float32'))
    batch1_gamma = tf.squeeze(np.array(batch1['gamma'].value, dtype='float32'))
    batch1_var = tf.squeeze(np.array(batch1['variance'].value, dtype='float32'))
    batch1_beta = tf.squeeze(np.array(batch1['beta'].value, dtype='float32'))

with h5py.File(batPath2) as batch2:
    batch2_mean = tf.squeeze(np.array(batch2['mean'].value, dtype='float32'))
    batch2_gamma = tf.squeeze(np.array(batch2['gamma'].value, dtype='float32'))
    batch2_var = tf.squeeze(np.array(batch2['variance'].value, dtype='float32'))
    batch2_beta = tf.squeeze(np.array(batch2['beta'].value, dtype='float32'))

with h5py.File(batPath3) as batch3:
    batch3_mean = tf.squeeze(np.array(batch3['mean'].value, dtype='float32'))
    batch3_gamma = tf.squeeze(np.array(batch3['gamma'].value, dtype='float32'))
    batch3_var = tf.squeeze(np.array(batch3['variance'].value, dtype='float32'))
    batch3_beta = tf.squeeze(np.array(batch3['beta'].value, dtype='float32'))


with h5py.File(batPath4) as batch4:
    batch4_mean = tf.squeeze(np.array(batch4['mean'].value, dtype='float32'))
    batch4_gamma = tf.squeeze(np.array(batch4['gamma'].value, dtype='float32'))
    batch4_var = tf.squeeze(np.array(batch4['variance'].value, dtype='float32'))
    batch4_beta = tf.squeeze(np.array(batch4['beta'].value, dtype='float32'))

with h5py.File(batPath5) as batch5:
    batch5_mean = tf.squeeze(np.array(batch5['mean'].value, dtype='float32'))
    batch5_gamma = tf.squeeze(np.array(batch5['gamma'].value, dtype='float32'))
    batch5_var = tf.squeeze(np.array(batch5['variance'].value, dtype='float32'))
    batch5_beta = tf.squeeze(np.array(batch5['beta'].value, dtype='float32'))


def cos_sim(A, B):
    return (np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B)+0.001))


def AE_extraction(self, input):
    AE1 = tf.nn.conv2d(input, self.AE["wc1"], strides=[1, 1, 1, 1], padding="SAME", dilations=[1, 1, 1, 1], name="AE1")
    AE1 = tf.nn.relu(tf.layers.batch_normalization(AE1, training=self.phase_train,name="bat1"))
    AE1 = tf.nn.max_pool(AE1, ksize=[1, 4, 4, 1], strides=[1, 3, 3, 1], padding="SAME")
    # 2nd convolutional layer
    AE2 = tf.nn.conv2d(AE1, self.AE["wc2"], strides=[1, 1, 1, 1], padding="SAME", dilations=[1, 1, 1, 1], name="AE2")
    AE2 = tf.nn.relu(tf.layers.batch_normalization(AE2, training=self.phase_train,name="bat2"))
    AE2 = tf.nn.max_pool(AE2, ksize=[1, 4, 4, 1], strides=[1, 3, 3, 1], padding="SAME")
    # 3rd convolutional layer
    AE3 = tf.nn.conv2d(AE2, self.AE["wc3"], strides=[1, 1, 1, 1], padding="SAME", dilations=[1, 1, 1, 1], name="AE3")
    AE3 = tf.nn.relu(tf.layers.batch_normalization(AE3, training=self.phase_train,name="bat3"))
    AE3 = tf.nn.max_pool(AE3, ksize=[1, 4, 4, 1], strides=[1, 3, 3, 1], padding="SAME")

    AE0_size = tf.shape(input)
    AE1_size = tf.shape(AE1)
    AE2_size = tf.shape(AE2)

    AE4 = tf.nn.conv2d_transpose(AE3, self.AE["wc4"], output_shape=[AE2_size[0], 31, 18, 128],strides=[1, 3, 3, 1], padding="SAME",name="U1")
    AE4 = tf.nn.relu(tf.layers.batch_normalization(AE4, training=self.phase_train,name="bat4"))
    AE5 = tf.nn.conv2d_transpose(AE4, self.AE["wc5"], output_shape=[AE1_size[0], 92, 54, 64],strides=[1, 3, 3, 1], padding="SAME",name="U2")
    AE5 = tf.nn.relu(tf.layers.batch_normalization(AE5, training=self.phase_train,name="bat5"))
    AE6 = tf.nn.conv2d_transpose(AE5, self.AE["wc6"], output_shape=[AE0_size[0], 274, 161, 1],strides=[1, 3, 3, 1], padding="SAME",name="U3")
    AE6 = tf.nn.relu(tf.layers.batch_normalization(AE6, training=self.phase_train,name="bat6"))
    Recon_loss = tf.nn.l2_loss(tf.subtract(input, AE6)) / tf.cast(AE0_size[0], dtype=tf.float32)

    Specific_features = AE3[:, :, :, 0:180]
    group_features = AE3[:, :, :, 180:240]
    junk_features = AE3[:, :, :, 240:]

    return AE3, Specific_features, group_features, junk_features, Recon_loss


def GC_shared(self, input):
    gC1 = tf.nn.conv2d(input, self.GC_shared["wc1"], strides=[1, 1, 1, 1], padding="SAME",
                       dilations=[1, 1, 1, 1], name="GC1")
    gC1 = tf.nn.relu(tf.layers.batch_normalization(gC1, training=self.phase_train,name="Gbatch1"))

    # 5th convolutional layer
    gC2 = tf.nn.conv2d(gC1, self.GC_shared["wc2"], strides=[1, 1, 1, 1], padding="SAME", name="GC2")
    gC2 = tf.nn.relu(tf.layers.batch_normalization(gC2, training=self.phase_train,name="Gbatch2"))
    gC2 = tf.nn.max_pool(gC2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

    gC3 = tf.nn.conv2d(gC2, self.GC_shared["wc3"], strides=[1, 1, 1, 1], padding="SAME",
                       dilations=[1, 1, 1, 1], name="GC3")
    gC3 = tf.nn.relu(tf.layers.batch_normalization(gC3, training=self.phase_train,name="Gbatch3"))

    # 5th convolutional layer
    gC4 = tf.nn.conv2d(gC3, self.GC_shared["wc4"], strides=[1, 1, 1, 1], padding="SAME", name="GC4")
    gC4 = tf.nn.relu(tf.layers.batch_normalization(gC4, training=self.phase_train,name="Gbatch4"))
    gC4 = tf.nn.max_pool(gC4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
    return gC4


def SC_shared(self, input):
    SC1 = tf.nn.conv2d(input, self.SC_shared["wc1"], strides=[1, 1, 1, 1], padding="SAME",
                       dilations=[1, 1, 1, 1], name="SC1")
    SC1 = tf.nn.relu(tf.layers.batch_normalization(SC1, training=self.phase_train,name="Sbatch1"))

    # 5th convolutional layer
    SC2 = tf.nn.conv2d(SC1, self.SC_shared["wc2"], strides=[1, 1, 1, 1], padding="SAME", name="SC2")
    SC2 = tf.nn.relu(tf.layers.batch_normalization(SC2, training=self.phase_train,name="Sbatch2"))
    SC2 = tf.nn.max_pool(SC2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

    SC3 = tf.nn.conv2d(SC2, self.SC_shared["wc3"], strides=[1, 1, 1, 1], padding="SAME",
                       dilations=[1, 1, 1, 1], name="SC3")
    SC3 = tf.nn.relu(tf.layers.batch_normalization(SC3, training=self.phase_train,name="Sbatch3"))

    # 5th convolutional layer
    SC4 = tf.nn.conv2d(SC3, self.SC_shared["wc4"], strides=[1, 1, 1, 1], padding="SAME", name="SC4")
    SC4 = tf.nn.relu(tf.layers.batch_normalization(SC4, training=self.phase_train,name="Sbatch4"))
    SC4 = tf.nn.max_pool(SC4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
    return SC4


def SC_spec(intput, weights, batch8_mean, batch8_var, batch8_beta, batch8_gamma):
    temps=[]
    for i in range(nClass):
     names='Feaus'+str(i)

     feature = (tf.nn.conv2d(intput[:,:,:,i*15:(i+1)*15],weights[:,:,15*(i):15*(i+1),:] , strides=[1, 1, 1, 1], padding="SAME", name=names))
     feature = tf.nn.relu(tf.nn.batch_normalization(feature, batch8_mean[i*2:(i+1)*2], batch8_var[i*2:(i+1)*2], batch8_beta[i*2:(i+1)*2], batch8_gamma[i*2:(i+1)*2], 0.001))
     feature = tf.nn.max_pool(feature, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
     #feature = tf.nn.max_pool(feature, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
     temps.append(feature)
    temps=tf.transpose(tf.stack(temps),[1,2,3,0,4])

    return tf.reduce_sum(temps,[1,2])


def GC_spec(intput, weights):
    temps=[]
    for i in range(GClass):
        names='Feau'+str(i)
        ww=weights[:, :, 15 * (i):15 * (i + 1), :]
        feature = tf.nn.relu(tf.nn.conv2d(intput[:,:,:,i*15:(i+1)*15],np.expand_dims(ww,[0]) , strides=[1, 1, 1, 1], padding="SAME", name=names))
        feature = tf.nn.max_pool(feature, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
        temps.append(feature)
    temps=tf.transpose(tf.stack(temps),[1,2,3,0,4])
    return tf.reduce_mean(temps,[1,2])


class Model:
    def __init__(self, name):
        with tf.variable_scope(name):
            # Place holders
            self.X = tf.placeholder(tf.float32, [1,None], name='X')
            self.phase_train = tf.placeholder(tf.bool,name='phase_train')

            # Xavier initializer
            initializer = tf.contrib.layers.xavier_initializer_conv2d()
            # Store layers weight & bias

            self.spec1 = tf.abs(tf.contrib.signal.stft(signals=self.X, frame_length=512, frame_step=256, fft_length=512,window_fn=tf.contrib.signal.hamming_window))

            max_arr=tf.reduce_max(self.spec1,axis=[1,2],keep_dims=True)

            min_arr = tf.reduce_min(self.spec1,axis=[1,2],keep_dims=True)

            self.spec1 = tf.multiply(tf.add(self.spec1, -min_arr), 1.0 / (tf.add(max_arr, -min_arr)))

            mel_weithf = tf.contrib.signal.linear_to_mel_weight_matrix(96, 257, 44100, 50, 22050, tf.float32)



            mel_weithf=tf.expand_dims(mel_weithf,0)

            spec1 = tf.expand_dims(tf.matmul(self.spec1, mel_weithf),3)
            conv1 = tf.nn.conv2d(tf.nn.relu(spec1), wc1, strides=[1, 1, 1, 1], padding="SAME", name="conv1")
            # conv1 = tf.nn.relu(tf.layers.batch_normalization(conv1, training=self.phase_train))

            conv1 = tf.nn.relu(tf.nn.batch_normalization(conv1, batch1_mean, batch1_var,batch1_beta, batch1_gamma, 0.001))
            conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
            # 2nd convolutional layer
            conv2 = tf.nn.conv2d(conv1, wc2, strides=[1, 1, 1, 1], padding="SAME", name="conv2")
            conv2 = tf.nn.relu(tf.nn.batch_normalization(conv2, batch2_mean, batch2_var,batch2_beta, batch2_gamma, 0.001))
            conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

            # 3rd convolutional layer
            conv3 = tf.nn.conv2d(conv2, wc3, strides=[1, 1, 1, 1], padding="SAME", name="conv3")
            conv3 = tf.nn.relu(tf.nn.batch_normalization(conv3, batch3_mean, batch3_var,batch3_beta, batch3_gamma, 0.001))
            # 4th convolutional layer
            conv4 = tf.nn.conv2d(conv3, wc4, strides=[1, 1, 1, 1], padding="SAME", name="conv4")
            conv4 = tf.nn.relu(tf.nn.batch_normalization(conv4, batch4_mean, batch4_var,batch4_beta, batch4_gamma, 0.001))
            conv4 = tf.nn.max_pool(conv4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

            # 5th convolutional layer
            conv5 = tf.nn.conv2d(conv4, wc5, strides=[1, 1, 1, 1], padding="SAME", name="conv5")
            self.conv5 = tf.reduce_mean(tf.nn.relu(tf.nn.batch_normalization(conv5, batch5_mean, batch5_var,batch5_beta, batch5_gamma, 0.001)),[1,2])


class Solver:
    def __init__(self,sess,model):
        self.model = model
        self.sess = sess

    def evaluate(self,X):
        feed = {
            self.model.X: X,
            self.model.phase_train: False,
        }
        correct_predictions_SC = self.model.conv5
        return self.sess.run([correct_predictions_SC], feed_dict=feed)
