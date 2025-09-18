import os
import cv2
import face_recognition
import pickle
import time 
from datetime import datetime
import numpy as np
import streamlit as st
import pandas as pd

ATTENDANCE_LOG = "attendance_log.csv"
USER_DATA_DIR = "user_data"
THRESHOLD = 0.5  


def load_user_data():
    """Loads all user data from the user_data directory."""
    user_data = {}
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)
        return user_data
    
    for user_id in os.listdir(USER_DATA_DIR):
        user_dir = os.path.join(USER_DATA_DIR, user_id)
        data_file = os.path.join(user_dir, f"{user_id}_data.pkl")
        
        if os.path.exists(data_file):
            with open(data_file, 'rb') as f:
                user_data[user_id] = pickle.load(f)
    return user_data

def log_attendance(user_data, action):
    """Logs the attendance action to the CSV file silently."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ATTENDANCE_LOG, 'a') as f:
        f.write(f"{timestamp},{user_data['user_id']},{user_data['user_name']},{user_data['department']},{action}\n")

def initialize_attendance_log():
    """Creates the attendance log file with headers if it doesn't exist."""
    if not os.path.exists(ATTENDANCE_LOG):
        with open(ATTENDANCE_LOG, 'w') as f:
            f.write("timestamp,user_id,user_name,department,action\n")


st.set_page_config(page_title="Face Recognition Attendance", layout="wide")
# title
st.title("Face Recognition Attendance System")

if 'page' not in st.session_state:
    st.session_state.page = "Home"

with st.sidebar:
    st.header("Face recognition attendance system")
    if st.button("Home", use_container_width=True):
        st.session_state.page = "Home"
    if st.button("Add New User", use_container_width=True):
        st.session_state.page = "Add User"
    if st.button("View Attendance", use_container_width=True):
        st.session_state.page = "View Attendance"

initialize_attendance_log()

# --- Page: Home (Attendance) ---
if st.session_state.page == "Home":
    # --- Initializations and Feedback Display ---
    if 'camera_active' not in st.session_state:
        st.session_state.camera_active = False
    if 'action' not in st.session_state:
        st.session_state.action = None
    if 'feedback_message' not in st.session_state:
        st.session_state.feedback_message = None

    if st.session_state.feedback_message:
        message_type = st.session_state.feedback_message["type"]
        message_text = st.session_state.feedback_message["text"]
        if message_type == "success":
            st.success(message_text, icon="✅")
        elif message_type == "error":
            st.error(message_text, icon="❌")
        st.session_state.feedback_message = None

    # --- Main Logic using if/else for clear UI separation ---
    
    # STATE 1: If the camera is active, show the video feed and "Stop Camera" button
    if st.session_state.camera_active:
        st.info(f"Camera is active for {st.session_state.action}. Please position your face in the frame.")
        
        if st.button("Stop Camera", key="stop_cam_home"):
            st.session_state.camera_active = False
            st.rerun()

        frame_placeholder = st.empty()
        video_capture = cv2.VideoCapture(0)

        known_users = load_user_data()
        known_encodings = [enc for data in known_users.values() for enc in data['face_encodings']]
        known_ids = [uid for uid, data in known_users.items() for _ in data['face_encodings']]

        while st.session_state.camera_active:
            ret, frame = video_capture.read()
            if not ret:
                st.error("Error: Could not read frame from camera.")
                st.session_state.camera_active = False
                break
            
            # Process and annotate the frame
            # (The camera logic from the previous step goes here without change)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            if not face_locations:
                cv2.putText(frame, "Please look at the camera", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif len(face_locations) > 1:
                cv2.putText(frame, "Multiple faces detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                top, right, bottom, left = face_locations[0]
                matches = face_recognition.compare_faces(known_encodings, face_encodings[0], THRESHOLD)
                name = "Unknown"
                color = (0, 0, 255)

                if True in matches:
                    first_match_index = matches.index(True)
                    user_id = known_ids[first_match_index]
                    user_data = known_users[user_id]
                    name = user_data['user_name']
                    color = (0, 255, 0)

                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

                    frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
                    log_attendance(user_data, st.session_state.action)
                    st.session_state.feedback_message = {"type": "success", "text": f"{st.session_state.action} confirmed for {name}."}
                    time.sleep(2)
                    st.session_state.camera_active = False
                    break
                
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

        video_capture.release()
        if not st.session_state.camera_active:
            st.rerun()

    # STATE 2: If the camera is NOT active, show the tiles menu
    else:
        st.header("Mark Your Attendance")
        st.markdown("---")

        col1, col2 = st.columns(2)

        # Tile 1: Check In
        with col1:
            with st.container(border=True):
                st.markdown("<h1 style='text-align: center; color: #28a745;'>✔️</h1>", unsafe_allow_html=True)
                st.markdown("<h4 style='text-align: center;'>Check In</h4>", unsafe_allow_html=True)
                
                if st.button("Start Camera", key="check_in_btn", use_container_width=True, type="primary"):
                    known_users = load_user_data()
                    if not known_users:
                        st.error("No users registered. Please add a user first.")
                    else:
                        st.session_state.camera_active = True
                        st.session_state.action = "Check In"
                        st.rerun()

        # Tile 2: Check Out
        with col2:
            with st.container(border=True):
                st.markdown("<h1 style='text-align: center; color: #dc3545;'>✖️</h1>", unsafe_allow_html=True)
                st.markdown("<h4 style='text-align: center;'>Check Out</h4>", unsafe_allow_html=True)

                if st.button("Start Camera", key="check_out_btn", use_container_width=True):
                    known_users = load_user_data()
                    if not known_users:
                        st.error("No users registered. Please add a user first.")
                    else:
                        st.session_state.camera_active = True
                        st.session_state.action = "Check Out"
                        st.rerun()

elif st.session_state.page == "Add User":
    st.header("Register a New User")

    with st.form("new_user_form"):
        user_id = st.text_input("Enter User ID (e.g., 'U001')")
        user_name = st.text_input("Enter User Name")
        user_department = st.text_input("Enter Department")
        submit_button = st.form_submit_button("Start Face Registration")

    if submit_button:
        if not all([user_id, user_name, user_department]):
            st.error("Please fill in all the details.")
        else:
            st.info("Starting camera for face registration. Please look at the camera and move your head slightly.")
            
            video_capture = cv2.VideoCapture(0)
            frame_placeholder = st.empty()
            
            face_encodings = []
            images_captured = 0
            max_images = 10
            
            progress_bar = st.progress(0)
            
            user_dir = os.path.join(USER_DATA_DIR, user_id)
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)

            while images_captured < max_images:
                ret, frame = video_capture.read()
                if not ret:
                    st.error("Failed to capture image from camera.")
                    break
                
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                
                if len(face_locations) == 1:
                    face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                    face_encodings.append(face_encoding)
                    
                    images_captured += 1
                    progress_bar.progress(images_captured / max_images)
                    
                    cv2.waitKey(500) 
                
                frame_placeholder.image(rgb_frame, channels="RGB", caption=f"Captured {images_captured}/{max_images} images")

            video_capture.release()
            cv2.destroyAllWindows()
            
            if len(face_encodings) == max_images:
                user_data = {
                    "user_id": user_id, "user_name": user_name,
                    "department": user_department, "face_encodings": face_encodings,
                    "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                data_file = os.path.join(user_dir, f"{user_id}_data.pkl")
                with open(data_file, 'wb') as f:
                    pickle.dump(user_data, f)
                st.success(f"User '{user_name}' registered successfully!")
            else:
                st.error("Registration failed. Could not capture enough face samples. Please try again.")

elif st.session_state.page == "View Attendance":
    st.header("Attendance Log")

    if os.path.exists(ATTENDANCE_LOG):
        try:
            df = pd.read_csv(ATTENDANCE_LOG)

            def style_attendance(row):
                action = row['action']
                if action == 'Check In':
                    return ['background-color: #D4EDDA; color: #155724'] * len(row)
                elif action == 'Check Out':
                    return ['background-color: #F8D7DA; color: #721C24'] * len(row)
                else:
                    return [''] * len(row)

            if df.empty:
                st.warning("The attendance log is empty.")
            else:
                st.dataframe(df.style.apply(style_attendance, axis=1), use_container_width=True)
            
        except Exception as e:
            st.error(f"Could not read the attendance log. Error: {e}")
    else:
        st.info("No attendance has been recorded yet.")