# nero_net
This is just simpe nero-net generator.

It consists three programs: 
1) universal mode for training of neural networks 
(nero_net_v2.py, that accept two parametrs from argv: 'studying' and start weights:
for example: python3.6 ./nero_net_v2.py studying 2 
//this command in your command line start to train nero_net with 0.2 start weghts)
This is alpha version of my code, that's why your must change 41 string in your code to select your own teaching set. 
All fine-tuning of your net you can make if config.json file.
2) nero using mode 
(nero_using.py, that accept two parametrs from argv: name of file wiht weights, which generate nero_net_v2 program and our input values
for example: python3.6 ./nero_using.py new_list_of_weights_t1526194990_w0.7.txt 101010
//we enter '101010' because this current net has 6 inputs.)
3) natural selection program
(diff_weights.py, this program help us to save our time and strengths efforts. It makes several threads in which the network are trained. This progran can be configured with 36 (weight limit) and 38 strings (lifetime of all current networks))

---------------------

Also I want to add example teaching set 'teaching_set.txt'
Finaly, this version is not final and there are many things that I want to fix :)
