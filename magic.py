import pygame

grey = pygame.Color(200, 200, 200)
lightgrey = pygame.Color(125, 125, 125)
darkred = pygame.Color(80, 0, 0)
lightred = pygame.Color(250, 100, 100)
lightgreen = pygame.Color(100, 250, 100)
lightblue = pygame.Color(100, 100, 250)
red = pygame.Color('red')
black = pygame.Color('black')

spell_elements = ['neutral', 'water', 'fire', 'wind']

element_colors = {}
element_colors['neutral'] = lightgrey
element_colors['water'] = lightblue
element_colors['fire'] = lightred
element_colors['wind'] = lightgreen

magic_combos = {}
for e in spell_elements:
	magic_combos[e] = {}

# EE - attack, EN - buff, NE - shield

magic_combos['neutral']['fire'] = 'inner flame'
magic_combos['fire']['neutral'] = 'burn souls'
magic_combos['fire']['fire'] = 'soul flare'

magic_combos['neutral']['wind'] = 'refresh jump'
magic_combos['wind']['neutral'] = 'tornado'
magic_combos['wind']['wind'] = 'air pistol'

class Player:
	def __init__(self):
		self.max_mana = 6
		self.curr_mana = self.max_mana

		self.time_between_recover_mana = 0.8
		self.time_until_recover_mana = 3.0
		self.time_remaining_to_recover = self.time_until_recover_mana

		# spell chain breaks when mana begins recovering
		self.max_spells_saved = self.max_mana
		self.spells_used = [] 
		self.spells_used_len = 0

def player_update(player):
	# thirty frames per second => 33 ms per frame
	if (player.curr_mana < player.max_mana):
		player.time_remaining_to_recover -= 1.0/30.0
		if (player.time_remaining_to_recover < 0.0):
			player.spells_used = []
			player.spells_used_len = 0
			if (player.time_remaining_to_recover < -player.time_between_recover_mana):
				player.time_remaining_to_recover = 0.0
				player.curr_mana += 1
				return '+'

def use_element(player, e):
	if player.curr_mana > 0:
		last_element = None
		if player.spells_used_len > 0:
			last_element = player.spells_used[player.spells_used_len-1]

		player.spells_used.append(e)
		player.spells_used_len += 1
		while (player.spells_used_len > player.max_spells_saved):
			player.spells_used.pop(0)
			player.spells_used_len -= 1

		player.curr_mana -= 1
		player.time_remaining_to_recover = player.time_until_recover_mana

		if not last_element is None and e in magic_combos[last_element]:
			return magic_combos[last_element][e]
		else:
			#return e
			pass
		
	else:
		return 'out of mana'

def main():
	pygame.init()

	# Set the width and height of the screen (width, height).
	screendim = (1050, 750)
	midscreen = (screendim[0]//2, screendim[1]//2)
	screen = pygame.display.set_mode(screendim)
	pygame.display.set_caption("B4J prototype")

	done = False
	clock = pygame.time.Clock()
	FPS = 30

	# input stuff
	pygame.joystick.init()

	# player stuff
	player = Player()

	# input stuff
	prev_input = []
	curr_input = [] # int list

	equipped_element_Q = 'neutral'
	equipped_element_W = 'fire'
	equipped_element_E = 'wind'

	while not done:
		clock.tick(FPS)

		output = []

		# poll input, put in curr_input and prev_input
		prev_input = curr_input[:]
		for event in pygame.event.get(): # User did something.
			if event.type == pygame.QUIT: # If user clicked close.
				done = True # Flag that we are done so we exit this loop.
			elif event.type == pygame.JOYBUTTONDOWN:
				print("Joystick button pressed.")
			elif event.type == pygame.KEYDOWN:
				curr_input.append(event.key)
			elif event.type == pygame.KEYUP:
				if event.key in curr_input:
					curr_input.remove(event.key)

		# keypad handle input
		moveinput_dir = [0, 0]
		if pygame.K_ESCAPE in curr_input:
			done = True
		if pygame.K_SPACE in curr_input:
			pass

		if pygame.K_q in curr_input and len(prev_input) == 0:
			output.append(use_element(player, equipped_element_Q))
		elif pygame.K_w in curr_input and len(prev_input) == 0:
			output.append(use_element(player, equipped_element_W))
		elif pygame.K_e in curr_input and len(prev_input) == 0:
			output.append(use_element(player, equipped_element_E))

		# update mana and shit
		output.append(player_update(player))

		# start drawing
		screen.fill(grey)

		for line in output:
			if (not line is None):
				print(line)

		#pygame.draw.circle(screen, lightgrey, (i, j), 1, 1)

		pygame.display.flip()

	pygame.quit()

if __name__=='__main__':
	main()