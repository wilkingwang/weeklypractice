import threading

def main():
    lock = threading.Lock()

    if lock.acquire():
        try:
            file = open('./data.dat', 'r')
        except Exception as e:
            print("open file failed, err: ", str(e))

        lock.release()
        print("done")

if __name__ == "__main__":
    main()