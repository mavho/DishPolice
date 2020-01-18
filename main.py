'''
main:
    Setup directory and saved formats.

    Setup connection to pi
        requests urllib3

    wrapper: take in stream from pi server
    something mbytes

    machine learning stuff
'''
import sys
from stream import Stream

def main():
    #### We have requests set up here
    addr = "http://169.233.122.23:8081"
    cap = cv2.VideoCapture(addr)

    ###
    ### Establish a connection to the
    ### stream server on the rasberry pi
    ### Take in the bytes of the stream and return a 
    ### number of bytes decoded
    ###
    while True:
        ret, frame = cap.read()
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) == 27:
            exit(0)

if __name__ == "__main__":
    main()