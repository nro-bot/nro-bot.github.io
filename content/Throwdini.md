Title: Throwdini: Throwing with Orientation
Starred: true
Date: 2020-01-01 12:00
Category: Hardware/Mechatronics
Slug: Throwdini
Summary: A robotic arm throwing setup built on a UR5. The plan was a reinforcement-learning residual model on top of ballistic physics, but under time constraints the throw was hardcoded. Unpublished work with Ondrej Biza.
Featured_Image: throwdini.jpg
Card_Video: throwdini_realtime.mp4

*Nancy Ouyang, Ondrej Biza (unpublished)*

<video controls muted loop playsinline style="width:100%;border-radius:6px;">
  <source src="/Throwdini/throwdini_realtime.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

The goal was a robotic arm that could throw objects with controlled orientation — for example, throwing a marker so it lands point-first. The intended approach was a learned residual model: a simple ballistics model to set the initial throw parameters (release angle, velocity), plus a reinforcement-learning residual term trained on real throws to correct for grasp-position variation and the ballistic model's errors.

In practice, time constraints meant the reinforcement-learning piece never got built — the throw trajectory ended up hardcoded instead. An automatic knife-return was built using 80-20 and a sliding board. Skills learned included diagnosing torque safety limits and learning the UR command syntax.

This was unpublished coursework / exploratory research.
