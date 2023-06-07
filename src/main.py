import pygame
from game import Game
import constants
import neat
import sys
import math
import pickle
import os

from spaceship import Spaceship

gen = 0

def eval_genomes(genomes, config):
    global gen
    gen += 1

    nets = []
    games = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        games.append(Game())
        ge.append(genome)

    pygame.init()
    size = (constants.WIDTH, constants.HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Asteroids")
    for i, game in enumerate(games):
        while game.running:
            screen.fill(constants.BLACK)
            game.spawn_asteroids()
            closest_asteroids = sorted(
                    game.asteroids,
                    key=lambda asteroid: math.sqrt((asteroid.position[0] - game.spaceship.center[0]) ** 2 + (asteroid.position[1] - game.spaceship.center[1]) ** 2)
                    )[:constants.CLOSEST_ASTEROIDS]
            asteroids_input = []
            in_min_distance = 0
            for asteroid in closest_asteroids:
                distance = math.sqrt((asteroid.position[0] - game.spaceship.center[0]) ** 2 + (asteroid.position[1] - game.spaceship.center[1]) ** 2)
                if distance <= constants.MIN_DISTANCE:
                    in_min_distance += 1
                asteroids_input.append(asteroid.position[0])
                asteroids_input.append(asteroid.position[1])
                asteroids_input.append(asteroid.vector[0])
                asteroids_input.append(asteroid.vector[1])
                asteroids_input.append(constants.ASTEROID_POSSIBLE_RADIUS[asteroid.radius_type])
                asteroids_input.append(game.spaceship.angle_asteroid(asteroid.vector))
                asteroids_input.append(distance)
            output = nets[i].activate(tuple(
                [
                game.spaceship.angle,
                game.spaceship.center[0],
                game.spaceship.center[1],
                game.spaceship.vertices[0][0],
                game.spaceship.vertices[0][1]
                ] + asteroids_input
                ))
            fitness_score = game.update(closest_asteroids)
            game.move(output, gen)
            if in_min_distance <= 0:
                fitness_score += 0.01
            ge[i].fitness += fitness_score
            game.display(screen)
            font = pygame.font.Font(None, 40)
            text = font.render('Generation: ' + str(gen), 1, constants.WHITE)
            screen.blit(text, (10, 40))
            font = pygame.font.Font(None, 40)
            text = font.render('Current game: ' + str(i), 1, constants.WHITE)
            screen.blit(text, (10, 70))
            font = pygame.font.Font(None, 40)
            text = font.render('Fitness: ' + str(round(ge[i].fitness, 2)), 1, constants.WHITE)
            screen.blit(text, (10, 100))
            pygame.event.get()
            pygame.display.update()

def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, constants.NUM_GENS)

    with open(constants.WINNER_FILE, 'wb') as f:
        pickle.dump(winner, f)
        f.close()

    print('\nBest genome:\n{!s}'.format(winner))

def main(argv):
    run(argv[0])

def replay_genome(config_path, genome_path="winner.pkl"):
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    print(genome)
    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    eval_genomes(genomes, config)

if __name__ == "__main__":
    #Set config file
    local_dir = os.path.dirname(__file__)
    config_path = "./config/neat_config.txt"
    if len(sys.argv) == 1:
        run(config_path)
    else:
        for genome in sys.argv[1:]:
            replay_genome(config_path, genome)
