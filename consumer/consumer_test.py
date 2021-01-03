from consumer import Consumer

def test_consumer():
    consumer = Consumer()
    consumer.run()

if __name__=="__main__":
    test_consumer()
    print("All good")