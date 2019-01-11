import tensorflow as tf
import read
import os

MODEL_SAVE_PATH = "KOG_model/"

MODEL_NAME = "kog_model.ckpt"


def get_weight_variable(shape, name):

    weights = tf.get_variable(name, shape, initializer=tf.truncated_normal_initializer(stddev=0.1))

    return weights


def predict(input_tensor):

    with tf.variable_scope('layer1'):

        layer1_weights = get_weight_variable([5, 1], 'layer1_weights')
        biases = tf.get_variable("biases", [1], initializer=tf.constant_initializer(0.0))
        hero_array = tf.split(input_tensor, 10, 1)
        hero_power = tf.matmul(hero_array[0], layer1_weights) + biases
        for i in range(1, 10):
            raw_hero_power = tf.matmul(hero_array[i], layer1_weights) + biases
            hero_power = tf.concat([hero_power, raw_hero_power], 1)
        layer1 = tf.nn.sigmoid(hero_power)

    with tf.variable_scope('layer2'):

        weight0 = get_weight_variable([1, 1], 'weight0')
        weight1 = get_weight_variable([1, 1], 'weight1')
        weight2 = get_weight_variable([1, 1], 'weight2')
        weight3 = get_weight_variable([1, 1], 'weight3')
        layer2_weights = tf.concat([weight0, weight1, weight2, weight2, weight3], 0)
        biases = tf.get_variable("biases", [1], initializer=tf.constant_initializer(0.0))
        team_array = tf.split(layer1, 2, 1)
        team_power0 = tf.matmul(team_array[0], layer2_weights) + biases
        team_power1 = tf.matmul(team_array[1], layer2_weights) + biases
        team_power = tf.concat([team_power0, team_power1], 1)
        layer2 = tf.nn.softmax(team_power)

    saver = tf.train.Saver()

    with tf.Session() as sess:
        saver.restore(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME))
        b = sess.run(layer2)
        # print(sess.run(layer1_weights), sess.run(layer2_weights))
        for i in range(len(b)):
            print(i+1, b[i])


def get_winning_rate(lineup):
    #x, y = read.read_train_linup_attr('train.xlsx')
    #lineup = {'Red': ['ÀÏ·ò×Ó', '½ª×ÓÑÀ', 'Ëïë÷', 'Ñîê¯', 'ÓÝ¼§'], 'Blue': ['Ë¾ÂíÜ²', 'Ëï²ß', 'ÕÅ·É', 'Áõ°î', 'ËïÎò¿Õ']}
    x = read.get_input_tensor(lineup)
    predict(x)



