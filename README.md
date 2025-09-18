-----

# Face Recognition Attendance System 📸

This project is a complete attendance management system that uses facial recognition to log check-ins and check-outs. It features a user-friendly web interface built with Streamlit, allowing for easy user registration, real-time attendance marking, and log viewing.

-----

## Features ✨

  * **Real-time Face Recognition**: Marks attendance instantly by recognizing faces from a live camera feed.
  * **Web-Based UI**: A simple and interactive interface built with Streamlit for all operations.
  * **User Registration**: Easily add new users by capturing multiple face samples through the webcam.
  * **Check-In / Check-Out Tiles**: Visually appealing, large-format buttons for clocking in and out.
  * **Attendance Log**: View the complete attendance history in a clean, color-coded table that distinguishes between actions.
  * **Persistent Storage**: User data and attendance logs are saved locally for persistent records.

-----

## Technology Stack 🛠️

  * **Language**: **Python**
  * **Web Framework**: **Streamlit**
  * **Core Libraries**:
      * **OpenCV** for camera access and image processing.
      * **face\_recognition** for the core facial detection and recognition logic.
      * **Pandas** for managing and displaying the attendance log.
      * **NumPy** for numerical operations.

-----

## Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

  * Python 3.8+ and Pip
  * Git for cloning the repository.
  * A webcam connected to your computer.

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/face-recognition-attendance.git
cd face-recognition-attendance
```

### 3. Create a Virtual Environment

It is highly recommended to use a virtual environment.

  * **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
  * **On Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### 4. Install Dependencies

Create a `requirements.txt` file in the project's root directory with the following content:

```txt
streamlit
opencv-python
face_recognition
numpy
pandas
```

Now, install the required packages using pip:

```bash
pip install -r requirements.txt
```

**Note**: The `dlib` library (a dependency of `face_recognition`) might require you to have CMake and a C++ compiler installed on your system.

-----

## How to Run the Application 🚀

With your virtual environment activated, run the following command in your terminal:

```bash
streamlit run app.py
```

The application will open in a new tab in your web browser.

-----

## File Structure 📂

The project is organized as follows:

```
face-recognition-attendance/
├── app.py              # Main Streamlit application script
├── attendance_log.csv  # CSV file where attendance is recorded
├── requirements.txt    # Python dependencies
└── user_data/          # Directory to store registered user data
    └── U001/
        ├── U001_data.pkl
        └── ...
```

-----

## Contributing 🤝

Contributions are welcome\! If you have suggestions for improvements or want to add new features, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Commit your changes (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/YourFeature`).
5.  Open a new Pull Request.

-----

## Author
Seetaram Prajapat - [GitHub Profile](https://github.com/Srprajapat)

## Contact

For any questions or suggestions, reach out to me at [**seetaram.22jics083@jietjodhpur.ac.in**](mailto\:seetaram.22jics083@jietjodhpur.ac.in) or connect on [LinkedIn](https://www.linkedin.com/in/seetaram-prajapat).

## License 📜

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.
