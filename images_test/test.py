#import face_recognition
import cv2
import numpy as np
import time
import argparse, os, sys

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.


# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

def main():
    #### Given a directory, loop through all the images in that directory
    try:
        directory = sys.argv[1]
    except IndexError:
        print('Input directory of input images')
        exit(0)

    known_face_encodings = []
    known_face_names = []
    for FILE in os.listdir(directory):
        if FILE[-4:] != '.jpg':
            print('Wrong extension!')
            continue
        
        curr_image = face_recognition.load_image_file(FILE)
        curr_encoding = face_recognition.face_encodings(curr_image)[0]
        known_face_encodings.append(curr_encoding)
        known_face_names.append(FILE)


    #Test.py sees if it recognizes the face based on the two images provided here (pic1.jpg, tim.jpeg pictures of eric and tim )
    #It saves images on 2 second intervals if it sees a recognized face ... only saves for first frame rn for some reason
    video_capture = cv2.VideoCapture(0)

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    i  = 0
    while True:
        # Grab a single frame of video
        save_frame = False
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    save_frame = True
                    name = known_face_names[best_match_index]
                else:
                    save_frame = False

                face_names.append(name)
        if (i % 5 == 0):
            process_this_frame = True
        else:
            process_this_frame = False
        i = i + 1 
        print("i = " + str(i), file=open("output.txt", "a"))
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        ts = str(time.time())
        #image file is saved with timestamp 
        if process_this_frame and save_frame:
            cv2.imwrite(ts + ".png",frame)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()