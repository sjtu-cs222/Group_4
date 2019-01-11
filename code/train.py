import tensorflow as tf
import inference
import read
import os

BATCH_SIZE = 1

LEARNING_RATE_BASE = 0.1

LEARNING_RATE_DECAY = 0.99

REGULARIZATION_RATE = 0.0001

TRAINING_STEPS = 50000

MOVING_AVERAGE_DECAY = 0.99

MODEL_SAVE_PATH = "KOG_model/"

MODEL_NAME = "kog_model.ckpt"


def train(data):

    x = tf.placeholder(tf.float32, [None, 50], name='x-input')
    y_ = tf.placeholder(tf.float32, [None, 2], name='y-input')

    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)

    y = inference.inference(x, regularizer)

    global_step = tf.Variable(0, trainable=False)

    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)

    variables_averages_op = variable_averages.apply(tf.trainable_variables())

    # cross_entropy_mean = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))
    mse = tf.reduce_mean(tf.square(y_-y))
    loss = mse + tf.add_n(tf.get_collection('losses'))

    learning_rate = tf.train.exponential_decay(

        LEARNING_RATE_BASE,

        global_step,

        len(data[1]) / BATCH_SIZE, LEARNING_RATE_DECAY,

        staircase=True)

    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

    with tf.control_dependencies([train_step, variables_averages_op]):

        train_op = tf.no_op(name='train')

    saver = tf.train.Saver()

    with tf.Session() as sess:
        saver.restore(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME))
        sess.run(global_step.initializer)
        #tf.global_variables_initializer().run()
        for i in range(TRAINING_STEPS):

            xs = [data[0][i % len(data[1])]]
            ys = [data[1][i % len(data[1])]]

            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: xs, y_: ys})

            if i % 1000 == 0:
                print("After %d training step(s), loss on training batch is %g." % (step, loss_value))
                # saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)
        saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME))


def main(argv=None):
    #data = read.read_train_linup_attr('train.xlsx')
    data = read.read
    train(data)


if __name__ == '__main__':
    tf.app.run()