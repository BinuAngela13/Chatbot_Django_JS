from django.shortcuts import render
import json, numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
from difflib import get_close_matches
# Create your views here.



def botIcon(request):
    return render(request, "botIcon.html")


def botOpen(request):
    return render(request, "messageBox.html")

@api_view(['GET'])
def load_json(request):
    with open('htmlTemplate/intents.json', 'r') as file:
        data = json.load(file)
    return Response(data['intents'])

notAnsQue = []
notAnsAns = []
notAnswered = True #answered or notAns Flag

Q = [[1.04661746, 0.07783448, 0.04410896, 0.06952978, 0.04410896, 0.04410896, 0.,         0.,         0.1261128,  0.06952978, 0.04410896, 0.04410896, 0.08605613, 0.06952978, 0.13389363],
    [0.,          0.01,         0.,         0.,         0.,         0.,         0.,         0.,         0.,         0.,         0.,         0.,         0.,         0.,         0.        ],
    [0.009,       0.,         0.58519851, 0.01791,    0.04356359, 0.02601,    0.02601,    0.,         0.02601,    0.,         0.02601,    0.0990922,  0.,         0.01791,    0.        ],
    [0.,          0. ,        0. ,        0.1,        0.,         0.,         0.,         0. ,        0.,         0.009,      0.  ,       0.,         0.,         0. ,        0.        ],
    [0.,          0. ,        0.,         0.,         0.068 ,     0.,         0.,         0. ,        0. ,        0.,         0. ,        0.,         0.,         0. ,        0.        ],
    [0.11068308,  0. ,        0.07028475, 0. ,        0.07028475, 1.14420933, 0.03624953, 0. ,        0.26001986, 0.03624953, 0.1685819 , 0.11120648, 0.16491255, 0.09492812, 0.11806597],
    [0.,          0.  ,       0.0421209,  0.,         0.05266787, 0.0428499,  0.67934652, 0.0348309,  0.0668114,  0.0267309,  0.,         0.,         0.0267309,  0.0267309,  0.0267309 ],
    [0.07653119,  0.06114119, 0.,         0.05220896, 0. ,        0.,         0.,         0.67934652, 0.11583227, 0.05266787, 0.,         0.06114119, 0.01791 ,   0.05266787, 0.        ],
    [0.,          0.  ,       0.,         0.01791 ,   0.034029,   0.,         0.,         0.  ,       0.29701 ,   0.01791,    0.0267309,  0.,         0.0267309,  0.  ,       0.034029  ],
    [0.01791,     0.009,      0.,         0.0267309,  0.03546359, 0.04410896, 0.01791,    0.,         0.06529581, 0.4900995,  0.,         0.,         0. ,        0.06529581, 0.009     ],
    [0.05266787,  0.14788551, 0. ,        0.07783448, 0.07783448, 0.23602325, 0. ,        0.14041127, 0. ,        0.13368801, 1.73831376, 0.,         0.,         0.21902504, 0.1881798 ],
    [0.,          0.30970038, 0.11023108, 0.11023108, 0.,         0.11023108, 0.29079233, 0.09419557, 0.09419557, 0.11023108, 0.14041127, 1.31254187, 0.,         0.,         0.2451673 ],
    [0.,          0. ,        0.,         0.01791,    0.009 ,     0.,         0.,         0. ,        0. ,        0.01791,    0.009 ,     0.,         0.3940399,  0.03546359, 0. ,      ],
    [0.,          0.009,      0.07726019, 0.,         0.04410896, 0.09176729, 0. ,        0.    ,     0.04410896, 0.009,      0.01791 ,   0.05266787, 0.05266787, 0.67934652, 0.        ],
    [0.,          0.,         0.06114119, 0.09419557, 0.04410896, 0.,         0.,         0. ,        0.07783448, 0.16483041, 0.,         0.12422085, 0.04410896, 0.,         1.13615128]]

@api_view(['GET','POST'])
def get_answer(request):
    global botResp
    notAnswered = False         #answered or notAns Flag

    with open('htmlTemplate/intents.json', 'r') as file:
        data = json.load(file)

    data = data['intents']
    questions = [q["question"] for q in data]
    answers   = [q["answer"] for q in data]

    botResp = "Sorry, I don't have answer for this question."
    state=-1
    action=-1
    if (request.method == 'POST'):
        reqbody = json.loads(request.body)
        msg  = reqbody.get('msg', '')
        

        state = get_close_matches(msg, questions, n=1, cutoff=0.5)

        # if match found, response will be taken from the q table
        if state:
            state = questions.index(state[0])
            action = np.argmax(Q[state])
            botResp = answers[action]
    
    
    return Response([botResp, state, action])
       
    #     if notAnswered:
    #         notAnsAns.append(str(msg))
    #         notAnswered = False
    #         return "Thank you for your reply!"
    #     else:
    #         if msg != "":
    #             match = get_close_matches(msg, questions, n=1,cutoff=0.5)

    #         answer = ["Sorry, I'm not trained to answer this question"]
    #         if (match):
    #             for que in data:
    #                 if match[0] == que["question"]:
    #                     answer[0] = que["answer"]

    #     # if answer not found
    #     sorryMsg = "Sorry"
    #     if (sorryMsg in answer[0]):
    #         notAnswered = True
    #         notAnsQue.append(str(msg))

    #  return Response([answer[0], notAnsQue, notAnsAns])