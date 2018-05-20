from __future__ import print_function

import sys
import numpy as np
import tensorflow as tf
from config import Config as conf

from capsNet.model import CapsNet


def main(_):
    # Construct Graph
    capsNet = CapsNet(is_training=True)
    print('[+] Graph is constructed')

    # Start session
    sv = tf.train.Supervisor(graph=capsNet.graph,
                             logdir=conf.logdir,
                             summary_op=capsNet.summary,
                             save_summaries_secs=100,
                             save_model_secs=0)
    with sv.managed_session() as sess:
        print('[+] Trainable variables')
        for tvar in capsNet.train_vars: print(tvar)

        print('[+] Model specification')
    	param_stats = tf.contrib.tfprof.model_analyzer.print_model_analysis(
			capsNet.graph,
        		tfprof_options=tf.contrib.tfprof.model_analyzer.
        		TRAINABLE_VARS_PARAMS_STAT_OPTIONS)
    	sys.stdout.write('total_params: %d\n' % param_stats.total_parameters)

        print('[+] Training start')
        for epoch in range(conf.num_epochs):
            if sv.should_stop(): break
            losses = []

            # from tqdm import tqdm
            # for step in tqdm(range(capsNet.num_batch), total=capsNet.num_batch, ncols=70, leave=False, unit='b'):
            for step in range(capsNet.num_batch):
                _, loss = sess.run([capsNet.train_op, capsNet.loss])
                losses.append(loss)
                if step % 100 == 0:
                    print(loss)
            print(('[+] EPOCH %d : ' % epoch) + str(np.mean(losses)))
            gs = sess.run(capsNet.global_step)
            sv.saver.save(sess, conf.logdir + '/model_epoch_%02d_gs_%d' % (epoch, gs))

    print("[+] Training is Completed")
    return

if __name__ == "__main__":
    tf.app.run()
