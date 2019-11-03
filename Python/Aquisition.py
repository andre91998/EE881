# -*- coding: utf-8 -*-
""""
%-----------------------------------------------------------------------------%
%Author: André Barros de Medeiros
%Date:10/31/2019
%Copyright: free to use, copy, and modify
%Description: Signal Aquisition and decodification for FSK modulation
%-----------------------------------------------------------------------------%
"""

#Algorithm:
    #1. Choose 2/4 FSK and Baud Rate
    #2. Record transimission
    #3. Apply matched filters for the 2/4 frequencies (filters with sin/cossin decomposition)
    #4. From the outputs of the matched filters, obtain bit sequence which was transmitted  
    #5. Sweep using Min. dist.Varredura or correlate to identify end of header and start of message
    #6. Remove header to obtain binary message
    #7. Decode message with app_decoder



import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import sounddevice as sd
from scipy.io.wavfile import write
import app_decoder

#Header to be removed from aquired signal (from Header.txt, see repository)

header = [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]

""" from intital test
#before working with recorded signal, using array from teste.txt concatenated with header from Header.txt, see repository
teste = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0]
signal = np.concatenate([header,teste],axis=0)
"""

#choose 2-FSK or 4-FSK
mode = int(input("For 2-FSK type '2' or for 4-FSK type '4': "))
if mode == 2:
    print("2-FSK selected")
if mode == 4:
    print("4-FSK selected")

#choose baud rate (bit/sec)
baud_rate = int(input("Choose Baud Rate: "))
print("Baud Rate = "+str(baud_rate)+" bit/sec")

#record  the transmission
"""
fs = int(input("Recording Sample Rate: ")) # Sample rate, usually 24000
seconds = 70  # Duration of recording
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
write('output.wav', fs, myrecording)  # Save as WAV file
"""

data, Fs = sf.read('output.wav') #comment above to use test files

#Process the recorded transmission (with noise)
print("Signal Received")

if mode == 2: #2-FSK
    
    F1=800 #0
    F2=1200 #1
    
    t_wave=np.arange(0,1/baud_rate,1/Fs)
    wave1=np.cos(2*np.pi*F1*t_wave)
    wave2=np.cos(2*np.pi*F2*t_wave)
    
    wave1_sin=np.sin(2*np.pi*F1*t_wave+np.pi/2)
    wave1_cos=np.cos(2*np.pi*F1*t_wave+np.pi/2)
    wave2_sin=np.sin(2*np.pi*F2*t_wave+np.pi/2)
    wave2_cos=np.cos(2*np.pi*F2*t_wave+np.pi/2)
    
    #Apply matched filters for the 2 frequencies (filters with sin/cossin decomposition)
    casado_1=np.power(np.convolve(data,np.flip(wave1_sin)),2)+np.power(np.convolve(data,np.flip(wave1_cos)),2)
    casado_2=np.power(np.convolve(data,np.flip(wave2_sin)),2)+np.power(np.convolve(data,np.flip(wave2_cos)),2)
    
    step=int(Fs/baud_rate)
    t=np.arange(0,len(data)/Fs,1/Fs)
    amostra_casado1=casado_1[step::step]
    amostra_casado2=casado_2[step::step]
    t_amostra=np.arange(step/Fs,t[-1]+step/Fs,step/Fs)
    
    #example plot to verify above code
    fig, axs = plt.subplots(2)
    fig.suptitle('Saída dos filtros casados + decomposição em seno e cosseno- Erro de 90°')
    axs[0].plot(t,casado_1[0:len(t)])
    axs[0].plot(t_amostra,amostra_casado1[0:len(t_amostra)],'or')
    axs[1].plot(t,casado_2[0:len(t)])
    axs[1].plot(t_amostra,amostra_casado2[0:len(t_amostra)],'or')
    plt.show()
    
    #From the outputs of the matched filters, obtain bit sequence which was transmitted 
    transmission_float1 = amostra_casado1[0:len(t_amostra)]
    transmission_float2 = amostra_casado2[0:len(t_amostra)] #from step above
    max_value=max(transmission_float2)
    min_value=min(transmission_float2)
    mean_value= (max_value-min_value)/2
    transmission = np.zeros((len(t_amostra),), dtype=int)
    
    for i in range(0,len(t_amostra),1): #transform transmission vector to pure binary
        if transmission_float1[i] < mean_value and transmission_float2[i] > mean_value:
            transmission[i]=1    
        elif transmission_float1[i] > mean_value and transmission_float2[i] < mean_value:
            transmission[i]=0 
        elif transmission_float2[i]>transmission_float1[i]:
            transmission[i]=1
        elif transmission_float2[i]<transmission_float1[i]:
            transmission[i]=0
            
            
#------------- End 2-FSK "if" section -----------------#
    
    
if mode == 4: #4-FSK
    F1=600 #00 
    F2=800 #01
    F3=1000 #11
    F4=1200 #10
    
    t_wave=np.arange(0,1/baud_rate,1/Fs)
    wave1=np.cos(2*np.pi*F1*t_wave)
    wave2=np.cos(2*np.pi*F2*t_wave)
    wave3=np.cos(2*np.pi*F3*t_wave)
    wave4=np.cos(2*np.pi*F4*t_wave)
    
    wave1_sin=np.sin(2*np.pi*F1*t_wave+np.pi/2)
    wave1_cos=np.cos(2*np.pi*F1*t_wave+np.pi/2)
    wave2_sin=np.sin(2*np.pi*F2*t_wave+np.pi/2)
    wave2_cos=np.cos(2*np.pi*F2*t_wave+np.pi/2)
    wave3_sin=np.sin(2*np.pi*F3*t_wave+np.pi/2)
    wave3_cos=np.cos(2*np.pi*F3*t_wave+np.pi/2)
    wave4_sin=np.sin(2*np.pi*F4*t_wave+np.pi/2)
    wave4_cos=np.cos(2*np.pi*F4*t_wave+np.pi/2)
    
    # Apply matched filters for the 4 frequencies (filters with sin/cossin decomposition)
    casado_1=np.power(np.convolve(data,np.flip(wave1_sin)),2)+np.power(np.convolve(data,np.flip(wave1_cos)),2)
    casado_2=np.power(np.convolve(data,np.flip(wave2_sin)),2)+np.power(np.convolve(data,np.flip(wave2_cos)),2)
    casado_3=np.power(np.convolve(data,np.flip(wave3_sin)),2)+np.power(np.convolve(data,np.flip(wave3_cos)),2)
    casado_4=np.power(np.convolve(data,np.flip(wave4_sin)),2)+np.power(np.convolve(data,np.flip(wave4_cos)),2)
    
    
    step=int(Fs/baud_rate)
    t=np.arange(0,len(data)/Fs,1/Fs)
    amostra_casado1=casado_1[step::step]
    amostra_casado2=casado_2[step::step]
    amostra_casado3=casado_3[step::step]
    amostra_casado4=casado_4[step::step]
    t_amostra=np.arange(step/Fs,t[-1]+step/Fs,step/Fs)
    
    
    #example plot to verify above code
    fig, axs = plt.subplots(4)
    fig.suptitle('Saída dos filtros casados + decomposição em seno e cosseno- Erro de 90°')
    axs[0].plot(t,casado_1[0:len(t)])
    axs[0].plot(t_amostra,amostra_casado1[0:len(t_amostra)],'or')
    axs[1].plot(t,casado_2[0:len(t)])
    axs[1].plot(t_amostra,amostra_casado2[0:len(t_amostra)],'or')
    axs[2].plot(t,casado_3[0:len(t)])
    axs[2].plot(t_amostra,amostra_casado3[0:len(t_amostra)],'or')
    axs[3].plot(t,casado_4[0:len(t)])
    axs[3].plot(t_amostra,amostra_casado4[0:len(t_amostra)],'or')
    plt.show()
    
    
     #From the outputs of the matched filters, obtain bit sequence which was transmitted 
    transmission_float1 = amostra_casado1[0:len(t_amostra)] #from step above
    transmission_float2 = amostra_casado2[0:len(t_amostra)]
    transmission_float3 = amostra_casado3[0:len(t_amostra)]
    transmission_float4 = amostra_casado4[0:len(t_amostra)]
    
    #check something
    check_vector=np.zeros(len(amostra_casado1))
    for i in range(0,len(amostra_casado1),1):
        check_vector[i]=transmission_float1[i]+transmission_float2[i]+transmission_float3[i]+transmission_float4[i]
    
    max_value = max(transmission_float1)
    min_value = min(transmission_float1)
    mean_value = (max_value + min_value)/2
    
    transmission = np.zeros((2*len(t_amostra)), dtype=int)
        
    #Method 1
    for i in range(0,2*len(t_amostra),2): #transform transmission vector to pure binary
        if transmission_float1[int(i/2)] > mean_value:
            transmission[i]=0
            transmission[i+1]=0
        elif transmission_float2[int(i/2)] > mean_value:
            transmission[i]=0
            transmission[i+1]=1
        elif transmission_float4[int(i/2)] > mean_value:
            transmission[i]=1
            transmission[i+1]=0
        elif transmission_float3[int(i/2)] > mean_value:
            transmission[i]=1
            transmission[i+1]=1

        
    """
    #Method 2    
    signal=np.empty((0,2*len(t_amostra)),dtype=int)
    for i in range(0,len(t_amostra),1):
        count=0
        if transmission_float1[i] > mean_value: 
            if i==0:
                signal=[0,0]
            else:
                signal.append(0) 
                signal.append(0)
        if transmission_float2[i] > mean_value:
            if i==0:
                signal=[0,1]
            else:
                signal.append(0)
                signal.append(1)
        if transmission_float4[i] > mean_value: 
            if i==0:
                signal=[1,0]
            else:
                signal.append(1) 
                signal.append(0)
        if transmission_float3[i] > mean_value: 
            if i==0:
                signal=[1,1]
            else:
                signal.append(1)
                signal.append(1)
    """

#------------- End 4-FSK "if" section -----------------#
    



#sweep signal with header array to find position that starts the transmission
header_size = len(header)
print("Header size: " + str(header_size))
transmission_size = len(transmission)
print("Signal size: " + str(transmission_size))

check=0
start_pos=0
best_check=header_size

for i in range(0, (transmission_size - (header_size-1)), 1):  #MaxI is the number of times the header fits in the signal in one sweep
    
    for j in range(i, header_size, 1):  #Store in Var check the "distance" between the header and current position in Var signal. Will slice at MinDist position
        #print(j)
        check = check + (abs(transmission[j]-header[j])^2)
        #print(check)
        
    if check < best_check:
        #print("New best starting position found")
        best_check = check
        start_pos = i   #starting position for array slice (removing header)
        #("New Min Dist: " + str(check))
        #print("New Optimal Starting Position: " + str(start_pos))
    
    check=0

print("Start Position Found: " + str(start_pos))
print("Slicing Received Message")
message = transmission[(start_pos):] #Here we slice the received signal and remove the header and everything before the header
print("Message Array Sliced")
print("Message Received: " + str(message))   

#print(message==[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0])

#app_decoder.app_decoder(message) #decode message received
