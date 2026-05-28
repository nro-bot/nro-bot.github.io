Title: 6.832: Inertia Wheel Inverted Pendulum
Starred: true
Date: 2019-05-01 12:00
Category: Computer Science
Slug: Inertia-Wheel-Pendulum
Summary: Using a flywheel to balance an inverted pendulum. LQR and region-of-attraction analysis in simulation; swingup and stabilization on real hardware using PD and bang-bang control. MIT Underactuated Robotics.
Featured_Image: pendulum.jpg
Card_Video: underactuated.mp4
Card_Video_Autoplay: false

*Nancy Ouyang, Ashwin Krishna — MIT 6.832 Underactuated Robotics*

<video controls muted loop playsinline style="width:100%;border-radius:6px;">
  <source src="/Inertia-Wheel-Pendulum/underactuated.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

A flywheel (inertia wheel) mounted at the tip of a pendulum can generate torque to keep the pendulum balanced upright — even without a motor at the pivot. In simulation, we derived the equations of motion and applied LQR control and region-of-attraction analysis. We also built a complete hardware system from scratch and implemented swingup and stabilization using PD and bang-bang control.

I led the analysis and controls design and co-built the hardware system.
