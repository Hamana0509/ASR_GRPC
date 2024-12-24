# python3 client_grpc.py --uri asr.kiki.laban.vn:443 --file test.wav
# python3 client_grpc.py --uri 103.141.140.202:55555 --rate 8000 --chunk 2000
from __future__ import print_function

import pyaudio
import time

import grpc
import streaming_voice_pb2
import streaming_voice_pb2_grpc

import argparse
import time
import json
import urllib
import sys

CHUNK = None
CHANNELS = None
RATE = None

FORMAT = None
URI = None
FILE = None
SINGLE_SENTENCE = None

SILENCE_TIMEOUT = 10
SPEECH_TIMEOUT = 0.5
SPEECH_MAX = 30

def record_block():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    while True:
        block = stream.read(CHUNK)
        block_audio = streaming_voice_pb2.VoiceRequest(byte_buff=block)
        yield block_audio

def read_block():
    with open(FILE, 'rb') as rd:  
        rd.read(44)
        while True:
            block = rd.read(CHUNK)   
            if len(block) == 0:
                break
            block_audio = streaming_voice_pb2.VoiceRequest(byte_buff=block)
            yield block_audio
            time.sleep(0.1)

def write_transcript(sentence, is_final=False):
    with open("transcript.txt", "a", encoding="utf-8") as f:
        if is_final:
            f.write(sentence)
            f.write("\n")
        else:
            f.write(sentence)
 
def run():
    start_time = time.time()
    metadata = [('channels', str(CHANNELS)), ('rate', str(RATE)), ('format', FORMAT), ('single-sentence', str(SINGLE_SENTENCE)), ('token', 'test_token'), ('id', 'test_id_{}'.format(int(start_time))), ('silence_timeout', str(SILENCE_TIMEOUT)), ('speech_timeout', str(SPEECH_TIMEOUT)), ('speech_max', str(SPEECH_MAX))]
    #credentials = grpc.ssl_channel_credentials()
    #channel = grpc.secure_channel(URI, credentials)
    channel = grpc.insecure_channel(URI)
    stub = streaming_voice_pb2_grpc.StreamVoiceStub(channel)

    sys.stdout.write('-------- Start ---------\n'); sys.stdout.flush()
    if 1==1:
        if FILE != '':
            responses = stub.SendVoice(read_block(), metadata=metadata)
        else:
            responses = stub.SendVoice(record_block(), metadata=metadata)
        for response in responses:
            #print(response)
            if response.status == 0:
                sentence = response.result.hypotheses[0].transcript
                # print("RESULTS: ", sentence)
                if response.result.final:
                    print("final true")
                    #print(res)
                    #print("PROCESS TIME: {}".format(time.time() - start_time))
                    #pass
                    write_transcript(sentence, is_final=True)
                    sys.stdout.write("\rHuman: {} - {}\n".format(sentence, response.result.hypotheses[0].confidence)); sys.stdout.flush()
                    #print(response)
                else:
                    print(response)
                    if len(sentence) > 100:
                        sentence = "..." + sentence[-100:]
                    sys.stdout.write("\r-----: {}".format(sentence)); sys.stdout.flush()
            else:
                print(response.msg)
                
    #except:
    #    pass

if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description='Command line client for ASR gRPC Server')
    parser.add_argument('--uri', help="Uri of gRPC ASR Server", required=True)
    parser.add_argument('--rate', help="Samplerate of audio", type=int, default=8000)
    parser.add_argument('--chunk', help="Size of each block audio on sent event", type=int, default=2000)
    parser.add_argument('--channels', help="Number of audio channels", type=int, default=1)
    parser.add_argument('--format', help="Audio encoded type", choices=['S8', 'S16LE', 'S16BE', 'F32LE', 'F32BE', 'F64LE', 'F64BE'], default='S16LE')
    parser.add_argument('--file', help="File to recognize", default='')
    parser.add_argument('--single_sentence', help="True if recognize single sentence audio", choices=['True', 'False'], default='False')
    args = parser.parse_args()
    CHUNK = args.chunk
    CHANNELS = args.channels
    RATE = args.rate
    FORMAT = args.format
    URI = args.uri
    FILE = args.file
    SINGLE_SENTENCE = args.single_sentence

    run()

