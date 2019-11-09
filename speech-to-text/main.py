import live_streaming

def main():
    answer = live_streaming.main()
    speech = live_streaming.get_string(answer)
    confidence = live_streaming.get_confidence(answer)
    print(speech)
if __name__ == '__main__':
    main()
