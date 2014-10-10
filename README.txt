###################
# Francesco Cervigni - s111436
# Fundamental of Embedded Systems 2012
# DTU, Lyngby
###################


Software : 
- rta.py
- dtu_tabu.py
- dtu_lcf.py

Usage rta.py:

  > python rta.py <.graphml>


Usage dtu_lfc.py:

  > python dtu_lcf.py  -m 5 -n 5  <.graphml>

  Example : 

  python dtu_lcf.py -m 5 -n 5 application.graphml

  The <.graphml> has to contain edges, use application.graphml as example.


Usage dtu_tabu.py:

  > python dtu_tabu.py -m 5 -n 5 --size_tabu 10 --global_loops 1000 --num_candidates 4 application.graphml>

  Example : 

  python dtu_tabu.py -m 5 -n 5 --size_tabu 10 --global_loops 1000 --num_candidates 4 application.graphml 


  The <.graphml> has to contain edges, use application.graphml as example.


FOR ALL :
- Use the option -h to discover the usage


