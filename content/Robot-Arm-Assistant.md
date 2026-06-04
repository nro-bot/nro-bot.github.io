Title: Robot Arm Assistant: Voice + Vision Cube Pickup
Starred: false
Date: 2022-01-01 12:00
Category: Robotics
Slug: Robot-Arm-Assistant
Summary: A 6-DoF robot arm assistant that picks up cubes using ArUco tag detection and color thresholding in OpenCV, with voice interaction via Mozilla TTS and Vosk speech recognition.
Featured_Image: robot_arm_assistant.jpg
Website: https://orangenarwhals.com/2022/01/smart-e-robot-arm-assistant-helps-you-pick-up-cubes-wip-post-1-voice-interaction-with-mozilla-tts-and-vosk-lewansoul-6dof-arm-python-library-arucotags-opencv/

*2022*

A LewanSoul 6-DoF robot arm that can find and pick up cubes on command. The pipeline combines:

- **OpenCV** ArUco tag detection + color thresholding to locate cubes
- **Vosk** offline speech recognition for voice commands
- **Mozilla TTS** for spoken responses
- Python library for LewanSoul arm control

The arm listens for a command, locates the target cube visually, and picks it up.
