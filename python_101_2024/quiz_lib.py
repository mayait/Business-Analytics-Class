import json
import urllib.request
import random
import ipywidgets as widgets
from IPython.display import display

class Quiz:
    def __init__(self, filename):
        questions_file = f"https://raw.githubusercontent.com/mayait/Business-Analytics-Class/main/python_101_2024/{filename}.json"
        self.questions = self.load_questions(questions_file)
        random.shuffle(self.questions)  # Mezclar las preguntas aleatoriamente
        self.current_question_index = 0
        self.score = 0
        self.create_widgets()

    def load_questions(self, questions_file):
        with urllib.request.urlopen(questions_file) as url:
            questions = json.loads(url.read().decode())
        return questions

    def create_widgets(self):
        self.question_label = widgets.Label(value="")
        self.options = widgets.RadioButtons(
            options=[], 
            value=None, 
            description='Opciones:', 
            layout={'width': '800px'},  # Ajustar el ancho
            style={'description_width': 'initial'}
        )
        self.submit_button = widgets.Button(description="Enviar")
        self.submit_button.on_click(self.check_answer)
        self.feedback_label = widgets.Label(value="")
        self.next_button = widgets.Button(description="Siguiente pregunta")
        self.next_button.on_click(self.next_question)
        self.next_button.disabled = True

    def display_question(self):
        question_data = self.questions[self.current_question_index]
        self.question_label.value = question_data['question']
        self.options.options = question_data['options']
        self.options.value = None
        self.feedback_label.value = ""
        self.next_button.disabled = True

    def check_answer(self, b):
        selected_option = self.options.value
        if selected_option is None:
            self.feedback_label.value = "Por favor, selecciona una opción. ❌"
            return

        correct_option = self.questions[self.current_question_index]['answer']
        if selected_option == correct_option:
            self.feedback_label.value = "¡Correcto! 🎉"
            self.score += 1
        else:
            self.feedback_label.value = "Incorrecto. ❌"

        self.next_button.disabled = False

    def next_question(self, b):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            self.show_final_score()

    def show_final_score(self):
        self.question_label.value = f"Has completado el quiz. Tu puntuación final es: {self.score}/{len(self.questions)} 🎓"
        self.options.options = []
        self.submit_button.disabled = True
        self.next_button.disabled = True

    def start_quiz(self):
        self.display_question()
        display(self.question_label, self.options, self.submit_button, self.feedback_label, self.next_button)

# Example of how to use the Quiz class
# quiz = Quiz('questions')
# quiz.start_quiz()
