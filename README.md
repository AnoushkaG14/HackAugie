Inspiration

We were inspired by the challenges faced by visually impaired individuals in navigating everyday environments safely. Existing smart canes are often expensive, limiting accessibility. Our goal was to design a low-cost, practical alternative that delivers essential safety features without compromising usability.

What it does

The Adaptive Assistive Cane (AAC) is a smart navigation aid that detects obstacles in real time using an ultrasonic sensor and provides multi-level audio and visual feedback. It also uses motion sensing to detect sudden impacts or falls, alerting the user instantly. The system adapts feedback intensity based on proximity, improving situational awareness.

How we built it

We built the system using a Raspberry Pi Pico W, an ultrasonic sensor for distance detection, and an MPU6050 accelerometer for motion sensing. LEDs (green, yellow, red) indicate distance zones, while a buzzer provides audio feedback. The logic was programmed in MicroPython, integrating sensor data to trigger appropriate responses.

Challenges we ran into

We faced challenges in calibrating sensor sensitivity, especially distinguishing normal cane movement from sudden shocks. Stabilizing sensor readings and avoiding false triggers required multiple iterations. We also worked through hardware connection issues and optimized distance detection accuracy.

Accomplishments that we're proud of?

We successfully developed a fully functional, low-cost smart cane prototype that integrates distance sensing, motion detection, and adaptive feedback. Achieving reliable performance while keeping the cost under $50 is a key accomplishment.

What we learned

We gained hands-on experience with embedded systems, sensor integration, and real-time data processing. We also learned how to troubleshoot hardware-software interactions and refine system sensitivity for real-world usability.

What's next for Adaptive Assistive Cane (AAC)

Future improvements include adding vibration feedback, GPS integration for navigation, and a mobile app interface. We also aim to refine the design for durability and explore scalable production to make the device widely accessible.
