
1. Lệnh tạo code tự động cho streaming_voice grpc từ proto 

- python3 -m grpc_tools.protoc -Iprotos --python_out=. --grpc_python_out=. protos/streaming_voice.proto
Khi thành công, sẽ có 2 file code được tạo ra: streaming_voice_pb2.py và streaming_voice_ppb2_grpc.py

2. Streaming từ phía client
* Chạy streaming
	python3 client_grpc.py

* Có thể gán giá trị cho các tham số khi streaming, tham số không được gán sẽ nhận giá trị mặc định
 --uri : Server GRPC URI, default = 'localhost:50055'
 --rate : kích thước của audio ghi âm theo bytes/giây, default = 8000
 --chunk : kích thước của mỗi block audio gửi lên server theo bytes, default = 2000
 --channels : channel của audio, default = 1
 --format: định dạnh, default = 'S16LE'
 --file : đườnng dẫn đến file audio muốn gửi lên server, thay cho việc ghi âm
 --single_sentence : streaming mode, default=True, nếu = True: chỉ gửi lên server 1 câu, ngược lại = False: muốn gửi nhiều câu lên server

Ví dụ:
    + python3 client_grpc.py --uri 103.146.21.41:9001
    Streaming trực tiếp từ microphone để nhận diện

    + python3 client_grpc.py --uri 103.146.21.41:9001 --file test.wav
    Nhận diện file test.wav bằng cách giả lập streaming gửi lên server

* Khi mở kết nối với server, thì metadata từ phía client sẽ được gửi lên server bao gồm: 
	+ channels
	+ rate
	+ format
	+ single_sentence
* Khi streaming, mỗi respond có dạng

    TextReply {
        int32 status;
        string msg;
        int32 segment;
        string id;

        Result {
            Hypothese {
                string transcript;
                string transcript_normed;
                string transcript_urlencoded;
                string transcript_normed_urlencoded;
                float confidence;
                float likelihood;
            }
            Hypothese hypotheses[];
            bool final;
        }
        Result result;

        float segment_start;
        float segment_length;
        float total_length;
    }


