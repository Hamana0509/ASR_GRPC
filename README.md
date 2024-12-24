# Streaming Voice gRPC Guide

## 1. Generate Code for `streaming_voice` gRPC from Proto

To generate the gRPC Python files, run the following command:

```bash
python3 -m grpc_tools.protoc -Iprotos --python_out=. --grpc_python_out=. protos/streaming_voice.proto
```

If successful, two files will be created:
- `streaming_voice_pb2.py`
- `streaming_voice_pb2_grpc.py`

---

## 2. Client Streaming Instructions

### Running the Streaming Client

Use the following command to run the client:

```bash
python3 client_grpc.py
```

### Configurable Parameters

You can specify values for various parameters while running the client. If not specified, default values will be used:

| Parameter         | Description                                        | Default Value      |
|--------------------|----------------------------------------------------|--------------------|
| `--uri`           | Server gRPC URI                                    | `localhost:50055`  |
| `--rate`          | Audio recording size in bytes per second           | `8000`             |
| `--chunk`         | Size of each audio block sent to the server (bytes)| `2000`             |
| `--channels`      | Number of audio channels                           | `1`                |
| `--format`        | Audio format                                       | `S16LE`            |
| `--file`          | Path to the audio file to send (optional)          | (record from mic)  |
| `--single_sentence` | Streaming mode (`True` for single sentence, `False` for multi-sentence) | `True` |

### Examples

1. **Streaming directly from the microphone**:  
    ```bash
    python3 client_grpc.py --uri 103.146.21.41:9001
    ```

2. **Streaming an audio file to the server**:  
    ```bash
    python3 client_grpc.py --uri 103.146.21.41:9001 --file test.wav
    ```

---

### Metadata Sent to Server

When a connection is established, the following metadata is sent from the client to the server:
- `channels`
- `rate`
- `format`
- `single_sentence`

---

### Streaming Response Format

The server responds with data in the following structure:

```protobuf
message TextReply {
    int32 status;
    string msg;
    int32 segment;
    string id;

    message Result {
        message Hypothese {
            string transcript;
            string transcript_normed;
            string transcript_urlencoded;
            string transcript_normed_urlencoded;
            float confidence;
            float likelihood;
        }
        repeated Hypothese hypotheses;
        bool final;
    }
    Result result;

    float segment_start;
    float segment_length;
    float total_length;
}
```

### Key Response Fields:
- **status**: Status code of the response.
- **msg**: Message describing the status.
- **segment**: The current audio segment being processed.
- **id**: Identifier for the response.
- **result**:
  - **hypotheses**: List of recognition hypotheses.
    - `transcript`: Raw transcription.
    - `transcript_normed`: Normalized transcription.
    - `transcript_urlencoded`: URL-encoded transcription.
    - `transcript_normed_urlencoded`: URL-encoded normalized transcription.
    - `confidence`: Confidence score of the transcription.
    - `likelihood`: Likelihood of the transcription.
  - `final`: Indicates if this is the final result for the segment.
- **segment_start**: Start time of the segment in seconds.
- **segment_length**: Duration of the segment in seconds.
- **total_length**: Total length of the streamed audio in seconds.
