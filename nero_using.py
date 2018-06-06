#!/usr/bin/env python3.6
import sys
from sys import argv
import math
import random

name_file, nero_list_of_weights, input_answers = argv

# //////////////////////////////////////////////////////////////////////


def nero_using(nero_list_of_weights, input_answers):
    nero_list_of_weights = open(nero_list_of_weights)
    amount_of_hide_layers = int(nero_list_of_weights.readline())
    amount_of_neurons_in_layer = []
    amount_of_neurons_in_layer.append(int(nero_list_of_weights.readline()))
    for i in range(amount_of_hide_layers):
        amount_of_neurons_in_layer.append(int(nero_list_of_weights.readline()))
    amount_of_neurons_in_layer.append(int(nero_list_of_weights.readline()))
    input_parametrs = []

    for i in range(amount_of_neurons_in_layer[0]):
        input_parametrs.append(int(input_answers[i]))
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
    print(f"{number_of_maximum_output}")
    for i in range(amount_of_neurons_in_layer[
        len(amount_of_neurons_in_layer)-1
    ]):
        if layer_outputs[len(layer_outputs)-1][i] > layer_outputs[
            len(layer_outputs)-1
        ][number_of_maximum_output]:
            number_of_maximum_output = i

# /////////////////////////////////////////////////////////////

    nero_list_of_weights.close()
    print(f"{number_of_maximum_output}")
    return (number_of_maximum_output)


# __main__/////////////////////////////////
exit(nero_using(nero_list_of_weights, input_answers))
# ////////////////////////////////////////
