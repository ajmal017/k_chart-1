# -*- coding: utf-8 -*-
"""
Created on Fri May 10 15:40:39 2019

@author: w
"""
import os
import sys
package_path = os.getcwd()
if package_path not in sys.path:
    sys.path.append(package_path)
from Strategy.risk_parity_matrix import structure_weights_matrix

structure_weights_matrix(40, 4)