import live_streaming

i = 0
while i < 10 :
    reponse = live_streaming.main()
    confidence = live_streaming.get_confidence(response)
    speech = live_streaing.get_string(response)
    print(speech)
    i = i+1
