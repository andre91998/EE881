# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 12:29:09 2019

@author: Andre
"""
import sys  
import numpy as np
import array


def find_arrays(A1,A2):

  sum1 = sum(A1,0)
  sum2 = sum(A2,0)
  dif = abs(sum1-sum2)
  
  if sum1 > sum2 :
    dif1 = -1000
    pos=5000
    check=0
    for i in range(0,len(A1)):
      if (A1[i]-dif/2) < 0 and A1[i] > check:
        check = A1[i]
        pos = i
    if pos == 5000:
      return dif
    else:
      A2.append(A1[pos])
      A1.remove(A1[pos])
      find_arrays(A1,A2)
    
      
  if sum2 > sum1 :
    dif2 = -1000
    pos = 5000
    check = 0
    for i in range(0,len(A2)):
      if (A2[i]-dif/2) < 0 and A2[i] > check:
        check = A2[i]
        pos = i
    if pos==5000:
      return dif
    else:
      A1.append(A2[pos])
      A2.remove(A2[pos])
      find_arrays(A1,A2)
      
  else: return 0  
  
      
def solution(A):  # A not necessarily sorted and may have repeated elements
  """     My Solution    
  sum = 0
  for i in range(0,len(A)): # works for arrays without repeated elements
    sum = sum + A[i]
  if sum%2 == 0 :
    Best_solution = sum/2
    return 0
  else : 
    Best_solution = float(sum)/2 + 0.5
    return 1
    End My Solution """
  
  mid = len(A)/2
  A1=A[0:int(mid)]
  A2=A[int(mid):]
  out = find_arrays(A1,A2)
  return out
  pass























































import sys

def solution(A):
  """    My Solution       """
  RowCounter = 1   # We will always have at least one row
  for i in range(1,len(A)):    # Here we sweep the array comparing the pair A[i] and A[i-1]
    if A[i] < A[i-1] :
      RowCounter = RowCounter  # Next element is smaller, no new row
    elif A[i] > A[i-1] :
      RowCounter = RowCounter + 1  #Next element is larger, new row
      """print("new row " + str(RowCounter))"""
  return RowCounter  #return total number of rows
  """ End My Solution """
  pass


def main():
  """Read from stdin, solve the problem, write answer to stdout."""
  input = sys.stdin.readline().split()
  A = [int(x) for x in input[0].split(",")]
  sys.stdout.write(str(solution(A)))


if __name__ == "__main__":
  main()
