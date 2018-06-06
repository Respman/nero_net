#!/usr/bin/env python3.6
import sys
from sys import argv
import math
import random
import json
import time
import subprocess

random.seed()
name_file, key, w_input = argv


def nero_studying(amount_of, alpha, n, part_from_teaching_set, weight_input):

    amount_of_iterations_for_one_exercise = 1
    # this is a typical list of weights for my net:
    # number of input neurons
    # number of hiden neurons
    # number of output neurons
    # [weights of inputs neurons]
    # [weights of hiden neurons]
    # [weights of output neurons]

    nero_list_of_weights = []
    for i in range(1, len(amount_of)):
        weights = []
        for j in range((amount_of[i-1]+1)*amount_of[i]):
            weights.append(random.uniform(-weight_input, weight_input))
        nero_list_of_weights.append(weights)

    delta_nero_list_of_weights = []
    for i in nero_list_of_weights:
        delta_weights = []
        for j in range(len(i)):
            delta_weights.append(0)
        delta_nero_list_of_weights.append(delta_weights)


# nero_teaching_set = open(input("Enter name of your teaching set: "))
    nero_teaching_set = open("./teaching_set.txt")

    data_teaching = nero_teaching_set.readlines()
    amount_of_teaching_set = len(data_teaching)
    nero_teaching_set.seek(0)
    amount_of_successful_attempts = 0
# demonstrate_results_in_concole = 0
    current_number_of_exercise = 0
    data_teaching_modified = []
    for i in data_teaching:
        new_layer = []
        for x in i.split(' ')[0]:
            new_layer.append(float(x))
        target = i.split(' ')[1]
        for j in range(amount_of[-1]):
            new_layer.append(1.0 if j == int(target) else 0.0)
        data_teaching_modified.append(new_layer)

    print(data_teaching_modified)
    last_example = 0
    while (amount_of_successful_attempts <
            amount_of_iterations_for_one_exercise *
            part_from_teaching_set * amount_of_teaching_set):

        if (current_number_of_exercise %
           (amount_of_iterations_for_one_exercise+1)) == 0:
            input_parametrs = data_teaching_modified[
                last_example % len(data_teaching_modified)
            ]
            last_example += 1
            current_number_of_exercise = 0
        current_number_of_exercise += 1

# everyone of neurons has ordinal number on his layer:
        ordinal_weight = 0
        layer_outputs = []
        layer_outputs.append(input_parametrs[:(amount_of[0])])
# apply input_parametrs
        for i in range(1, len(amount_of)):
            current_layer_outputs = []
            for k in range(amount_of[i]):
                summ = 1*nero_list_of_weights[i-1][k*(amount_of[i-1]+1)]
                for j in range(amount_of[i-1]):
                    ordinal_weight = nero_list_of_weights[i-1][
                        k*(amount_of[i-1]+1)+1+j
                    ]
                    summ += layer_outputs[i-1][j]*ordinal_weight
                current_layer_outputs.append(1/(1+math.exp(-2*summ)))
            layer_outputs.append(current_layer_outputs)

        output_correction = []
        correct_answers = []

        for i in range(amount_of[0], amount_of[0]+amount_of[len(amount_of)-1]):
            correct_answers.append(float(input_parametrs[i]))

        for i in range(amount_of[len(amount_of)-1]):
            b = layer_outputs[len(layer_outputs)-1][i]
            output_correction.append(b*(1-b)*(correct_answers[i]-b))

        layer_correction = []
        layer_correction.append(output_correction)

        for k in range(len(amount_of)-2):
            # amount of hide layer
            hide_correction = []
            for i in range(amount_of[len(amount_of)-k-2]):
                # amount of neurons in current hide layer
                shildren_summ = 0
                for j in range(amount_of[len(amount_of)-k-1]):
                    # amount of neurons in previous layer
                    paste1 = (len(nero_list_of_weights)-1)-k
                    paste2 = j*(amount_of[len(amount_of)-k-2]+1) + (i+1)
                    paste3 = nero_list_of_weights[paste1][paste2]
                    shildren_summ += layer_correction[k][j] * paste3
                paste1 = (len(layer_outputs)-1) - (k+1)
                paste2 = (1-layer_outputs[paste1][i]) * (shildren_summ)
                paste3 = layer_outputs[paste1][i] * paste2
                hide_correction.append(paste3)
            layer_correction.append(hide_correction)
            # making delta_nero_list_of_weight according to wikipedia
        layer_correction.reverse()
        for k in range(1, len(amount_of)):
            # number of layer
            for i in range(amount_of[k]):
                for j in range(len(delta_nero_list_of_weights[k-1])):
                    paste1 = delta_nero_list_of_weights[k-1][j]
                    paste2 = layer_correction[k-1][i]*layer_outputs[k][i]
                    paste1 = alpha * paste1 + (1-alpha) * n * paste2
                    delta_nero_list_of_weights[k-1][j] = paste1

        for i in range(len(nero_list_of_weights)):
            for j in range(len(nero_list_of_weights[i])):
                nero_list_of_weights[i][j] += delta_nero_list_of_weights[i][j]

        print("\033c")
        # console cleaner
        # print(f"hide parametrs is: {hide_parametrs}")
        print(f"input parametrs is {input_parametrs}")
        print(f"output parametrs is: {layer_outputs[len(layer_outputs)-1]}")
        print(f"correct outputs is: {correct_answers}")
        paste = f"{layer_correction[len(layer_correction)-1]}"
        write = "output correction is:" + paste
        print(write)
        # test for stopping studing:

        number_of_maximum_output = 0
        number_of_maximum_correct_output = 0
        for i in range(amount_of[len(amount_of)-1]):
            paste1 = len(layer_outputs)-1
            paste2 = layer_outputs[paste1][number_of_maximum_output]
            if layer_outputs[len(layer_outputs)-1][i] > paste2:
                number_of_maximum_output = i
            paste1 = correct_answers[number_of_maximum_correct_output]
            if correct_answers[i] > paste1:
                number_of_maximum_correct_output = i

        if number_of_maximum_output == number_of_maximum_correct_output:
            amount_of_successful_attempts += 1
        else:
            amount_of_successful_attempts = 0

        paste1 = f"{amount_of_successful_attempts}"
        write = "amount of successful attempts: " + paste1
        print(write)

    paste1 = f"{math.floor(time.time())}_w{round(weight_input, 1)}.txt"
    name = "./new_list_of_weights_t" + paste1
    new_nero_list_of_weights = open(name, 'w')

    new_nero_list_of_weights.write(str(len(amount_of)-2) + "\n")
    for i in amount_of:
        new_nero_list_of_weights.write(str(i) + "\n")

    for i in range(len(nero_list_of_weights)):
        for j in nero_list_of_weights[i]:
            new_nero_list_of_weights.write(str(j) + "\n")
    new_nero_list_of_weights.close()

    print(f"nero_list_of_weights is: {nero_list_of_weights}")
    nero_teaching_set.close()


# //////////////////////////////////////////////////////////////////////

def nero_using(nero_list_of_weights):
    nero_list_of_weights = open(nero_list_of_weights)

    amount_of_hide_layers = int(nero_list_of_weights.readline())
    amount_of_neurons_in_layer = []
    amount_of_neurons_in_layer.append(int(nero_list_of_weights.readline()))
    for i in range(amount_of_hide_layers):
        amount_of_neurons_in_layer.append(int(nero_list_of_weights.readline()))
    amount_of_neurons_in_layer.append(int(nero_list_of_weights.readline()))
    input_parametrs = []

    for i in range(amount_of_neurons_in_layer[0]):
        input_parametrs.append(input(f" input {i+1}-t input's parametrs: "))

    # /////////////////////////////////////////////////////////

    ordinal_weight = 0
    layer_outputs = []

    layer_outputs.append(input_parametrs)
    # apply input_parametrs

    for i in range(1, len(amount_of_neurons_in_layer)):
        current_layer_outputs = []
        for k in range(amount_of_neurons_in_layer[i]):
            summ = 1*(float(nero_list_of_weights.readline()))
            for j in range(amount_of_neurons_in_layer[i-1]):
                ordinal_weight = (float(nero_list_of_weights.readline()))
                summ += (float(layer_outputs[i-1][j]))*ordinal_weight
            current_layer_outputs.append(1/(1+math.exp(-2*summ)))
            layer_outputs.append(current_layer_outputs)
    number_of_maximum_output = 0
    for i in range(amount_of_neurons_in_layer[
        len(amount_of_neurons_in_layer)-1
    ]):
        if layer_outputs[len(layer_outputs)-1][i] > layer_outputs[
            len(layer_outputs)-1
        ][number_of_maximum_output]:
            number_of_maximum_output = i
    # /////////////////////////////////////////////////////////////

    print(f"The number of maximum output is {number_of_maximum_output + 1}")
    nero_list_of_weights.close()
    return (layer_outputs[len(layer_outputs)-1])


if key == "studying":

    studying = json.loads(open("config.json").read())
    momentum = studying['momentum']
    amount_of_input_neurons = studying['amount of input neurons']
    amount_of_output_neurons = studying['amount of output neurons']
    part_from_teaching_set = studying['part from teaching set']
# part of teaching set sufficient to pass the exam
    amount_of = []
    amount_of.append(amount_of_input_neurons)
    for x in studying['amount of hide neurons']:
        amount_of.append(x)
    amount_of.append(amount_of_output_neurons)
    speed = studying['speed']
# beta = studying['coeff. sigmoid']

    nero_studying(amount_of, momentum, speed, part_from_teaching_set,
                  0.1*int(w_input))


if key == "using":
    nero_list_of_weights = "./new_list_of_weights.txt"
# nero_list_of_weights = input("enter directory of weight list: ")
    print(f"{nero_using(nero_list_of_weights)}")
