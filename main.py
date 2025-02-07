import sys
import os
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,
                             QStackedWidget, QMessageBox)
from gtts import gTTS
import pygame  # For playing audio

class SpeakEasyKids(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpeakEasy Kids - Speech Therapy App")
        self.setGeometry(100, 100, 600, 400)
        
        # Dictionary with words for each activity
        self.exercise_words = {
            "Articulation Practice": ["Sun", "Snake", "Sand", "Kids", "Kite"],
            "Vocabulary Building": ["Apple", "Ball", "Cat", "Dog", "Elephant"],
            "Listening Exercises": ["Park", "Playground", "Picnic", "Dog", "Swing"],
            "Communication Skills": ["Hello", "Please", "Thank you", "Sorry", "Goodbye"]
        }
        self.current_word_index = 0
        self.current_activity = ""

        self.stack = QStackedWidget()
        self.home_screen = self.create_home_screen()
        self.stack.addWidget(self.home_screen)
        self.setCentralWidget(self.stack)
    
    def create_home_screen(self):
        layout = QVBoxLayout()
        self.welcome_label = QLabel("Welcome to SpeakEasy Kids!", self)
        self.welcome_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.welcome_label)
        
        buttons = [
            ("Articulation Practice", self.show_articulation),
            ("Vocabulary Building", self.show_vocabulary),
            ("Listening Exercises", self.show_listening),
            ("Communication Skills", self.show_communication)
        ]
        
        for text, callback in buttons:
            button = QPushButton(text, self)
            button.clicked.connect(callback)
            layout.addWidget(button)
        
        container = QWidget()
        container.setLayout(layout)
        return container

    def create_activity_screen(self, title):
        layout = QVBoxLayout()
        label = QLabel(f"{title} - Interactive Exercises")
        layout.addWidget(label)
        
        start_button = QPushButton("Start Exercise", self)
        start_button.clicked.connect(lambda: self.start_interaction(title))
        layout.addWidget(start_button)
        
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.show_home)
        layout.addWidget(back_button)

        container = QWidget()
        container.setLayout(layout)
        return container
    
    def show_home(self):
        self.stack.setCurrentWidget(self.home_screen)
    
    def show_articulation(self):
        self.show_activity("Articulation Practice")

    def show_vocabulary(self):
        self.show_activity("Vocabulary Building")

    def show_listening(self):
        self.show_activity("Listening Exercises")

    def show_communication(self):
        self.show_activity("Communication Skills")

    def show_activity(self, activity_name):
        """Creates and displays the activity screen dynamically."""
        self.activity_widget = self.create_activity_screen(activity_name)
        self.stack.addWidget(self.activity_widget)
        self.stack.setCurrentWidget(self.activity_widget)

    def start_interaction(self, activity_name):
        """Starts the exercise by showing words one by one with pronunciation."""
        if activity_name not in self.exercise_words:
            QMessageBox.information(self, "No Words", f"No words defined for {activity_name}.")
            return
        self.current_activity = activity_name
        self.current_word_index = 0
        self.show_word_exercise()

    def show_word_exercise(self):
        """Creates a new widget to display words one by one."""
        self.exercise_widget = QWidget()
        layout = QVBoxLayout()
        
        self.word_label = QLabel("", self.exercise_widget)
        layout.addWidget(self.word_label)
        
        self.pronounce_button = QPushButton("🔊 Pronounce", self.exercise_widget)
        self.pronounce_button.clicked.connect(self.pronounce_word)
        layout.addWidget(self.pronounce_button)

        self.next_button = QPushButton("Next Word", self.exercise_widget)
        self.next_button.clicked.connect(self.next_word)
        layout.addWidget(self.next_button)

        back_button = QPushButton("Back", self.exercise_widget)
        back_button.clicked.connect(self.show_home)
        layout.addWidget(back_button)
        
        self.exercise_widget.setLayout(layout)
        self.stack.addWidget(self.exercise_widget)
        self.show_word()
        self.stack.setCurrentWidget(self.exercise_widget)

    def show_word(self):
        """Displays the current word and pronounces it."""
        words = self.exercise_words[self.current_activity]
        if self.current_word_index < len(words):
            self.word_label.setText(f"Word: {words[self.current_word_index]}")
            self.pronounce_word()
        else:
            self.word_label.setText("Exercise Completed!")
            self.next_button.setEnabled(False)
            self.pronounce_button.setEnabled(False)

    def next_word(self):
        """Moves to the next word and pronounces it."""
        self.current_word_index += 1
        self.show_word()

    def pronounce_word(self):
        """Uses gTTS to pronounce the current word and plays it."""
        if self.current_word_index >= len(self.exercise_words[self.current_activity]):
            return

        word = self.exercise_words[self.current_activity][self.current_word_index]
        audio_file = f"temp_audio_{int(time.time())}.mp3"  # Unique filename

        try:
            # Generate and save the speech
            tts = gTTS(word, lang="en")
            tts.save(audio_file)

            # Initialize pygame mixer and play the audio
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            # Wait for the audio to finish playing, then delete the file
            while pygame.mixer.music.get_busy():
                time.sleep(0.5)

            pygame.mixer.quit()  # Ensure pygame releases the file
            os.remove(audio_file)  # Delete after playing
        except Exception as e:
            QMessageBox.warning(self, "Audio Error", f"Could not play audio: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeakEasyKids()
    window.show()
    sys.exit(app.exec_())
