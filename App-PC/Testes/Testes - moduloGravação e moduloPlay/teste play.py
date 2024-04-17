import json

ficheiro = open('teste.txt', 'r')
pose_now = ficheiro.readline()
pose_now = json.loads(pose_now)
print(len(pose_now))
pose_now = pose_now[0]
print(pose_now)
ficheiro.close()
