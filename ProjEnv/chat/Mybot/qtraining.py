import numpy as np
import json

# loading file
with open('C:/React Course/DjangoJS/ProjEnv/chat/htmlTemplate/intents.json', 'r') as file:
    data = json.load(file)
data = data['intents']


# Define the set of questions and possible answers
questions = [q['question'] for q in data]
answers = [q['answer'] for q in data]

# Define  Q-table
num_questions = len(questions)
num_answers = len(answers)
Q = np.zeros((num_questions, num_answers))  


alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.7  # Epsilon-greedy exploration parameter

# Train the agent using Q-learning
num_episodes = 400
for episode in range(num_episodes):
    # Randomly select a question
    state = np.random.randint(num_questions)
    
    # Epsilon-greedy action selection
    n = np.random.rand()
    # print("n : ", n)
    if n < epsilon:
        action = np.random.randint(num_answers)  # Random action
    else:
        action = np.argmax(Q[state])  # Greedy action
    
    # Getting reward for the answer it took
    reward = int(input(f'Question: {questions[state]}\nAnswer: {answers[action]}\nWas the answer correct? (1 for yes, 0 for no): '))
    
    # Update Q-value 
    Q[state, action] += alpha * (reward + gamma * np.max(Q[state]) - Q[state, action])
    # print(Q)

print(Q)

# # Test the trained agent
# def select_best_answer(question):
#     state = questions.index(question)
#     action = np.argmax(Q[state])
#     return answers[action]

# # Example usage
# test_question = 'What is your name?'
# print(select_best_answer(test_question))
