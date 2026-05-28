Title: Interactive UR5 Demo: Hand Tracking
Starred: true
Date: 2026-05-04 12:00
Category: Computer Science
Slug: UR5-Hand-Tracking
Summary: A UR5 robot arm that mirrors hand movements in real time using MediaPipe hand tracking. Built in ~6 hours; uses servoL (velocity mode) for smooth following. Next goal: make it fist-bump.
Featured_Image: ur5_hand_tracking.jpg
Card_Video: ur5_hand_tracking.mp4
Card_Video_Loop: false
Website: https://orangenarwhals.com/2026/05/ur5-hand-tracking-demo/

*May 2026*

<video controls muted playsinline style="width:100%;border-radius:6px;">
  <source src="/UR5-Hand-Tracking/ur5_hand_tracking.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

A live demo where a **UR5 robot arm** mirrors hand movements captured by a camera in real time. The key insight was switching from position-mode (`moveL`) to velocity-mode (`servoL`), which made the motion dramatically smoother and faster to implement.

About 6 hours of work: 2 hrs configuring a safety plane in the UR5, 2 hrs on the hand-coordinate to robot-coordinate transform code, and 2 hrs taking videos and showing friends.

**Stack:** MediaPipe hand tracking, Python UR5 driver over URScript/serial, safety plane constraints.

**Next steps being considered:** accepting Z-axis input (currently limited to XY plane for safety), adding derivative control to prevent runaway oscillation when hands move too fast, making the robot high-five or fist-bump, and eventually — making it build sandwiches.
