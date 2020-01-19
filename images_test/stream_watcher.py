import face_recognition
import cv2
import numpy as np
import time
import sys
import os
import knn


# This will be where the faces from the video get passed to the ML algorithm

video_capture = cv2.VideoCapture(0)
#addr = "http://169.233.122.23:8081/"
#video_capture = cv2.VideoCapture(addr)
#
#while True:
#    ret, frame = cap.read()
#    cv2.imshow('Video', frame)

<<<<<<< HEAD
image_first = face_recognition.load_image_file("aaron.jpg")
image_first_encoding = face_recognition.face_encodings(image_first)[0]

# Load a second sample picture and learn how to recognize it.
image_second = face_recognition.load_image_file("tim.jpeg")
image_second_encoding = face_recognition.face_encodings(image_second)[0]

image_third = face_recognition.load_image_file("eric1.jpg")
image_third_encoding = face_recognition.face_encodings(image_third)[0]

#image_fourth = face_recognition.load_image_file("mav_white.jpg")
#print(len(face_recognition.face_encodings(image_fourth)))
#image_fourth_encoding = face_recognition.face_encodings(image_fourth)[0]

image_fifth = face_recognition.load_image_file("robert.jpg")
image_fifth_encoding = face_recognition.face_encodings(image_fifth)[0]

image_sixth = face_recognition.load_image_file("tomas.jpg")
image_sixth_encoding = face_recognition.face_encodings(image_sixth)[0]


# Create arrays of known face encodings and their names
known_face_encodings = [
    image_first_encoding,
    image_second_encoding,
    image_third_encoding,
#    image_fourth_encoding,
    image_fifth_encoding,
    image_sixth_encoding
]
    
known_face_names = [
    "Aaron",
    "Tim",
    "Eric",
#    "Maverick",
    "Robert",
    "Tomas"
    
]
=======
try:
    directory = sys.argv[1]
except IndexError:
    print('Input directory of input images')
    exit(0)

known_face_encodings = []
known_face_names = []

for FILE in os.listdir(directory):
    if FILE[-4:] != '.jpg' and FILE[-5:] != '.jpeg':
        print('Wrong extension!')
        continue
        
    curr_image = face_recognition.load_image_file(directory+ "/" + FILE)
    print("Importing image file: " + FILE)
    curr_encoding = face_recognition.face_encodings(curr_image)[0]
    known_face_encodings.append(curr_encoding)
    known_face_names.append(FILE)
>>>>>>> 00dd620948dbd71441dc6c96a505127e1c541489

output_dict = {}

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

last_seen_face = None

face_flag = False
face_start = None

picture_timer = time.perf_counter()

process_this_frame = True
i  = 0
didDishes = False
while True:
    # Grab a single frame of video
    save_frame = True
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
#        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        
        if len(face_encodings) < 1:
            if face_flag == True:
                print("Last Seen Face: " + last_seen_face)
                face_flag = False

                
                if timer_end > 30:
                    output_dict[last_seen_face]['wash_bool'] = True
                output_dict[last_seen_face]['sink_time'] = timer_end
#                face_start = None
                face_start = None
                
                if didDishes == True:
                    print(name + " did dishes!")
                    didDishes = False
                else:
                    output_dict[name]['wash_bool'] = False
                    print(name + " didn't do dishes!")
            else:
                print("No faces right now")
        
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                        
                name = known_face_names[best_match_index]
                if name not in output_dict:
                    output_dict[name] = {}

                if face_flag == False:
                    face_flag = True
                    face_start = time.perf_counter()
                    last_seen_face = name
                    
                if face_flag == True:
                    if 'picture' not in output_dict:
                        pic_name = name + "_" + str(time.time()) + ".png"
                        cv2.imwrite(pic_name,frame)
                        output_dict[name]['picture'] = pic_name

                
                save_frame = True
            else:
                save_frame = False
                
            face_names.append(name)

#        if (i % 5 == 0):
#            process_this_frame = True
#        else:
#            process_this_frame = False
#        i = i + 1 
#    print("i = " + str(i), file=open("output.txt", "a"))
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

#     Display the resulting image
    cv2.imshow('Video', frame)
    ts = str(time.time())
    #image file is saved with timestamp 
#    if process_this_frame and save_frame:
##        print(time.perf_counter() - picture_timer)
#        if time.perf_counter() - picture_timer >= 5:
##            print("Take picture!!")
#            cv2.imwrite(ts + ".png",frame)
#            picture_timer = time.perf_counter()
            
#     Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print('Printing output dic: ')
print(output_dict)
for key in output_dict:
    if(output_dict[key]["wash_bool"]):
        print(key + " did dishes!")
    else:
        print(key + " didn't do dishes! Fuck this guy!")
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

print(output_dict)
