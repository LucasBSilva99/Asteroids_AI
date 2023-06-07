# Asteroids_AI

É necessário instalar as seguintes dependências:
pip install neat-python
pip install pygame
pip install numpy

Para correr o projeto de forma a realizar o treino dos indivíduos, 
é necessário alterar nos files neat_config.txt e no constants.py caso 
queira alterar número de asteróides no jogo, e os parâmetros de input das redes neuronais

o comando é o seguinte: 
python ./src/main.py

Caso tenha modelos que já foram treinados e salvos na pasta do models o comando é o seguinte
python ./src/main.py "./models/filename"