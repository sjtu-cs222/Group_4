import tensorflow as tf
from itertools import combinations

def get_weight_variable(shape, name, regularizer):

    weights = tf.get_variable(name, shape, initializer=tf.truncated_normal_initializer(stddev=0.1))

    if regularizer != None: tf.add_to_collection('losses', regularizer(weights))

    return weights


def inference(input_tensor, regularizer):

    with tf.variable_scope('layer1'):
        # n * 10
        layer1_weights = get_weight_variable([5, 1], 'layer1_weights', regularizer)
        biases = tf.get_variable("biases", [1], initializer=tf.constant_initializer(0.0))
        hero_array = tf.split(input_tensor, 10, 1)
        hero_power = tf.matmul(hero_array[0], layer1_weights) + biases
        for i in range(1, 10):
            raw_hero_power = tf.matmul(hero_array[i], layer1_weights) + biases
            hero_power = tf.concat([hero_power, raw_hero_power], 1)
        layer1 = tf.sigmoid(hero_power)

    with tf.variable_scope('layer2'):
        # n * 2
        weight0 = get_weight_variable([1, 1], 'weight0', regularizer)
        weight1 = get_weight_variable([1, 1], 'weight1', regularizer)
        weight2 = get_weight_variable([1, 1], 'weight2', regularizer)
        weight3 = get_weight_variable([1, 1], 'weight3', regularizer)
        layer2_weights = tf.concat([weight0, weight1, weight2, weight2, weight3], 0)
        biases = tf.get_variable("biases", [1], initializer=tf.constant_initializer(0.0))
        team_array = tf.split(layer1, 2, 1)
        team_power0 = tf.matmul(team_array[0], layer2_weights) + biases
        team_power1 = tf.matmul(team_array[1], layer2_weights) + biases
        team_power = tf.concat([team_power0, team_power1], 1)
        layer2 = tf.nn.softmax(team_power)

    return layer2


'''
    with tf.variable_scope('layer3'):
        # n*20
        hero_array = tf.split(layer1, 10, 1)
        for i in range(2):
            single_team_hero_array = hero_array[i*5: (i+1)*5]
            for j in combinations(single_team_hero_array, 2):
                if j[0].name[-1] == str(i*5+2) and j[1].name[-1] == str(i*5+3):

'''
