'''
	Action : {1, 2, 3, 4, 6}
	State :	{(total runs, batsman1, batsman2, current bowler, total balls faced)}
	Easy State: {(total runs, batsman, total balls faced)}
	Use strike rate & average, risk involved in going for shots
	Risk : {0.01, 0.02, 0.03, 0.1, 0.3}
	Probability of getting the desired shot/runs
	P = {0.7, 0.7, 0.7, 0.7, 0.7}
'''

R1 = [0.01, 0.02, 0.03, 0.1, 0.3]
R10 = [0.1, 0.2, 0.3, 0.5, 0.7]
P1 = 0.7
P10 = 0.1
A = [1, 2, 3, 4, 6]
R = A
#state = (wickets left, balls left)
W = 10
B = 20*6
def risk(action, batsman):
	return R1[action] + batsman*(R1[action] - R10[action])/10

def success(batsman):
	return P1 + batsman(P1 - P10)

