import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_DEVICES"] = '-1'

import time
import librosa
import numpy as np
import tensorflow as tf
from datetime import datetime
from modules.models import Model, Solver, nClass, Feature_class, cos_sim


def time_string():
    return datetime.now().strftime('%Y/%m/%d-%H:%M:%S')


def main():
    fs = 44100
    inp_wav = os.path.join('./test1.wav')
    out_txt = os.path.join('./animal.log')
    prev_state = None
    with open("./class_name.txt", "r", encoding='UTF8') as f:
        labels = f.readlines()
    labels = np.block(labels)
    labels = list(map(lambda s: s.strip(), labels))

    with tf.Session() as sess:
        model_A = Model('A')
        model_A_solver = Solver(sess, model_A)

        # while True:
        curr_state = os.path.getatime(inp_wav)
        if curr_state != prev_state:
            print(time_string(), end=' ')
            print("New recorded file arrived!")
            prev_state = curr_state

            wav, _ = librosa.load(inp_wav, sr=fs)
            duration = len(wav) // fs
            wav = wav[np.newaxis, :]

            hop_size = fs // 2
            total_steps = duration * 2 - 1

            for i in range(total_steps):
                inp = wav[:, i * hop_size:(i + 1) * hop_size + hop_size]
                Sc = model_A_solver.evaluate(inp)
                Sc = np.asarray(Sc, dtype=np.float32)[0]
                # print(Sc)
                rres = list()
                for ii in range(nClass):
                    rres.append(cos_sim(Sc, Feature_class[ii]))
                rres = np.transpose(np.block(np.transpose(rres)))
                classs = np.where(rres > 0.92)[0]

                if not classs:
                    print('No animal sound detected')
                else:
                    curr_time = time.gmtime(curr_state + (i * .5))
                    with open(out_txt, 'a', encoding='UTF8') as f:
                        f.write(str(labels[classs.item()]) + ' sound detected at '
                                + time.strftime('%Y/%m/%d-%H:%M:%S', curr_time) + '\n')
                    print(time_string(), end=' ')
                    print(str(labels[classs.item()]) + ' sound detected')
main()