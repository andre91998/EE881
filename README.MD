# EE881 Final Project
## Digital FSK Modulation
FSK (*frequency-shift keying*) modulation is a form of Passband modulation in witch digital information is transmitted through frequency changes of a carrier signal. The simplest FSK is binary FSK (BFSK). BFSK uses a pair of discrete frequencies to transmit binary (0s and 1s) information. With this scheme, the "1" is called the mark frequency and the "0" is called the space frequency.

Esta modulação normalmente é adotada em transmissões na banda de RF, no entanto ela permite utilizarmos frequências baixas para a portadora com uma perda tolerável de eficiência. Essa capacidade faz com que seja possível uma transmissão digital por canais normalmente utilizados para transmitir voz (telefone, rádio-difusão, alto-falantes, etc) e fornece um protocolo versátil de comunicação onde não há possibilidade de se transmitir por ondas de rádio ou fibra óptica. 
![FSK Modulation](FSK.png)

## Syncronism
A mensagem a ser transimitida é assíncrona, ou seja, não há uma combinação prévia do horário em que ela será transmitida, então o detector desenvolvido deverá ser capaz de identificar corretamente o início e o fim de cada transmissão de dados. Para isso toda mensagem se iniciará com uma sequência pré-definida de bits. O cabeçaho não entra na conta da taxa de erro, então não é necessário que o decodificador o identifique totalmente, mas é fundamental que o momento da transição entre o cabeçalho e a mensagem seja definido com precisão. O cabeçalho utilizado se encontra no arquivo *header.txt*. Essa sequência foi gerada utilizando um algoritmo chamado "*maximum length sequence*" e aumenta a resolução do pico de auto-correlação, facilitando a identificação do cabeçalho.

## Data Format
Os dados transmitidos podem ser de diferentes fontes (áudio, texto, imagem, etc), e de tamanhos variados. O programa deve ser capaz de detectar os bits e fornecê-los **sem o cabeçalho** para a função *app_decoder* fornecida neste repositório (app_decoder.m ou app_decoder.py, a depender da linguagem escolhida). A função aceita um array **numérico** binário e retorna a quantidade de bits perdidos no processo de detecção. Preste atenção no tipo dos dados fornecido para a função (deve ser um array de inteiros) e no formato em que eles serão fornacidos (um bit por posição). É especialmente crítico que o momento to início da mensagem seja identificado corretamente, pois um erro de sincronismo levará ao erro de grande parte dos bits da mensagem e consequentemente ao fracasso da transmissão. 

## Types of Signals to be Processed
Serão testadas duas modulações diferentes. Uma 2-FSK e uma 4-FSK. O detector deverá permitir escolher uma das duas modulações no momento de iniciar a recepção. O protocolo de transmissão será o seguinte:

- 2-FSK
    - 800 Hz - 0
    - 1200 Hz - 1

- 4-FSK
    - 600 Hz - 00
    - 800 Hz - 01
    - 1000 Hz - 11
    - 1200 Hz - 10

Não há restrições quanto à estratégia de detecção, apesar de ser recomendado o emprego de um filtro casado. Para quem tiver curiosidade, as funções que fazem a transmissão se encontram no arquivo TX_script.py.

## Symbol Rate
A taxa de síbolos utilizada será definida no momento da transmissão. O detector deverá fornecer a opção de definir a taxa ao início do processo de decodificação.

## Test File
No repositório, encontram-se dois arquivos de teste: *teste_2fsk.wav* e *teste_4fsk.wav*. Estes arquivos foram gerados com uma taxa de 20 símbolos por segundo e podem ser utilizados para auxiliar o desenvolvimento do projeto. O arquivo *teste.txt* contem a respectiva sequência de bits com o cabeçalho. A função fornecida também identifica os áudios de teste e fornece o numero de bits incorretos. Eles são os arquivos gerados, sem ruído, para testar a imunidade ao ruído vocês podem utilizar o microfone e gravar uma reprodução dos áudios.

## Symbol Aquisition
Para a apresentação, será necessário adquirir o sinal transmitido para fazer a decodificação. Desta forma, vocês poderão gravar através do windows e importar o arquivo para o modem ou implementar um passo de gravação de áudio usando as biliotecas de Python ou MATLAB. Acredito que a dificuldade seja equivalente nos dois casos. É possível implementar um processamento em tempo real, mas é muito mais difícil e já foge do escopo da disciplina.

Como existe a possibilidde de fazer em diferentes linguagens, o procedimento para gravar áudio é diferente. Aqui vão algumas referências úteis para ajudar com este passo:
- Importar um arquivo WAV:
    - https://www.mathworks.com/help/matlab/ref/audioread.html
    - https://pysoundfile.readthedocs.io/en/0.9.0/#module-soundfile
- Gravar através do microfone do computador:
    - https://www.mathworks.com/help/matlab/import_export/record-and-play-audio.html
    - https://realpython.com/playing-and-recording-sound-python/
