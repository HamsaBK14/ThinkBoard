# 🧠 ThinkBoard: AI-Powered Drawing Board for Everyone

ThinkBoard is an inclusive, gesture-friendly, AI-assisted drawing web app built for **accessibility, creativity, and real-time interaction**. It supports voice notes, smart suggestions, color picking, and even gesture-based controls — making it ideal for everyone, including differently-abled users.

---

## ✨ Features

- 🎨 Multiple brush types: Pencil, Marker, Glow, Spray
- 🌈 Color picker and brush size control
- 🧽 Eraser, Undo, Clear, and Save tools
- 🧠 Smart Suggestion (AI-powered region highlight)
- 🗒️ Add sticky notes (typed and voice-based)
- 🎥 Timelapse playback of your drawing process
- 📷 Real-world color detection via camera
- 🔄 Canvas capture for future AI integration

---

## 🌐 Live Demo

👉 [Click here to open ThinkBoard](https://hamsabk.github.io/ThinkBoard/)  
Hosted via GitHub Pages

---

## 💻 Technologies Used

- **HTML5 Canvas API** for drawing
- **JavaScript** for interactivity
- **Web Speech API** for voice notes
- **WebRTC + MediaDevices** for real-world color picker
- **Python + OpenCV + MediaPipe** for AI gesture detection (backend)

---

## 🤖 AI Gesture Module

We’ve added a gesture recognition backend powered by Python and MediaPipe!

### 🔍 Files:
- [`ai-gesture/air_canvas_hand_test.py`](./ai-gesture/air_canvas_hand_test.py):  
  Uses OpenCV + MediaPipe to track hand gestures in real-time and map them to drawing commands.

- [`ai-gesture/style.cc`](./ai-gesture/style.cc):  
  Native C++ style module (part of MediaPipe or OpenCV backend).

### 🧠 Future Plan:
We'll integrate this with the browser-based ThinkBoard so users can:
- Change brush with hand gestures ✋
- Undo, clear, or save without touching the screen 🖐️
- Enable drawing for users with limited mobility 🧍‍♂️

➡️ This brings the power of **AI + Accessibility** to the drawing experience.

---

## 🚀 Roadmap

- [ ] Gesture-to-command integration (real-time AI triggers)
- [ ] Auto-save and restore previous drawing
- [ ] Mobile-responsive UI
- [ ] Export to PDF and video
- [ ] Full voice-controlled navigation

---

## 🙌 Author

**Hamsa B K**  
Passionate about building inclusive tools that merge creativity and AI.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
