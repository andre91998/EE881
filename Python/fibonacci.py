# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 17:04:16 2019

@author: Andre
"""

FibArray = [0,1] 
  
def fibonacci(n): 
    if n<0: 
        print("Incorrect input") 
    elif n<=len(FibArray): 
        return FibArray[n-1] 
    else: 
        temp_fib = fibonacci(n-1)+fibonacci(n-2) 
        FibArray.append(temp_fib) 
    return temp_fib



def Fibonacci2(n): 
    if n<0: 
        print("Incorrect input") 
    # First Fibonacci number is 0 
    elif n==1: 
        return 0
    # Second Fibonacci number is 1 
    elif n==2: 
        return 1
    else: 
        return Fibonacci2(n-1)+Fibonacci2(n-2) 
  
# Driver Program 
  
print(fibonacci(71)) 