import random
import sys

def ExtractCouples(couples_file_name):
	couples = []
	file_handler = open(couples_file_name, 'r')
	for line in file_handler:
		line = line.strip()
		couples.append(line)
	file_handler.close()
	return couples

def ShuffleCouples(couples):
	print " ## INFO: Shuffling couples..."
	shuffled_couples = {}

	while True:
		shuffled_couples.clear()
		for couple in couples:
			# you cannot gift yourself
			single_couple = [couple]

			# you cannot give to whoever is giving to you
			cannot_give_to = []
			if couple in shuffled_couples.values():
				shuffled_couples_inverted = dict(zip(shuffled_couples.values(), shuffled_couples.keys()))
				cannot_give_to.append(shuffled_couples_inverted[couple])

			# list of people to give to  # all people        # yourself           # already receiveing a gift      # whos giving to you
			available_ungifted_couples = list(set(couples) - set(single_couple) - set(shuffled_couples.values()) - set(cannot_give_to))
			if len(available_ungifted_couples) == 0:
				print " ### WARNING: Random sequence resulted in circular gifting ... recomputing"
				break
			if len(available_ungifted_couples) == 1:
				random_index = 0
			else:
				random_index = random.randint(0, len(available_ungifted_couples)-1)
			shuffled_couples[couple] = available_ungifted_couples[random_index]
		if len(shuffled_couples) == len(couples):
			break
	print " ## INFO: Couples shuffled."
	return shuffled_couples

def ExtractIndividuals(individual_filename):
	file_handler = open(individual_filename, 'r')
	names = []
	for line in file_handler:
		line = line.strip()
		names.append(line)
	file_handler.close()
	return names

def SeparateFamilies(names):
	families = {}

	for name in names:
		print name
		last_name = name.split(" ")[1]
		if last_name not in families.keys():
			families[last_name] = []
		families[last_name].append(name)

	return families

def ShuffleIndividuals(individuals):
	print " ## INFO: Shuffling individuals..."
	shuffled_individuals = {}
	families = SeparateFamilies(individuals)

	while True:
		shuffled_individuals.clear()
		for individual in individuals:

			# you cannot gift yourself
			single_individual = [individual]

			# you cannot give to whoever is giving to you
			cannot_give_to = []
			if individual in shuffled_individuals.values():
				shuffled_individuals_inverted = dict(zip(shuffled_individuals.values(), shuffled_individuals.keys()))
				cannot_give_to.append(shuffled_individuals_inverted[individual])

			# list of people to give to      # all people            # yourself               # already receiveing a gift          # whos giving to you   # your family
			available_ungifted_individuals = list(set(individuals) - set(single_individual) - set(shuffled_individuals.values()) - set(cannot_give_to) - set(families[individual.split(" ")[1]]))
			if len(available_ungifted_individuals) == 0:
				print " ### WARNING: Random sequence resulted in circular gifting ... recomputing"
				break
			if len(available_ungifted_individuals) == 1:
				random_index = 0
			else:
				random_index = random.randint(0, len(available_ungifted_individuals)-1)
			shuffled_individuals[individual] = available_ungifted_individuals[random_index]

		if len(shuffled_individuals) == len(individuals):
			break

	print " ## INFO: Individuals shuffled."
	return shuffled_individuals

def GenerateListOfAvailableCousins(grandkid, families, last_names, already_receiving_a_gift):
	available_cousins_to_give_to = []
	current_last_name = grandkid[1]
	for last_name in last_names:
		if last_name == current_last_name:
			continue
		for child in families[last_name]:
			if (child, last_name) not in already_receiving_a_gift:
				available_cousins_to_give_to.append((child, last_name))
	return available_cousins_to_give_to

def OutputFile(file_name, shuffled_couples, shuffled_individuals):
	print " ## INFO: Writing output to", file_name
	output_html_file_handler = open(file_name, 'w')
	output_html_file_handler.write("**********************************************\n")
	for gifter in shuffled_couples:
		output_html_file_handler.write("%s give to %s\n" % (gifter, shuffled_couples[gifter]))
	output_html_file_handler.write("**********************************************\n")
	for gifter in shuffled_individuals:
		output_html_file_handler.write("%s gives to %s\n" % (gifter, shuffled_individuals[gifter]))
	output_html_file_handler.write("**********************************************\n")
	#output_html_file_handler.write("<img src=\"callChristmasListGenerator.pl\" border=0 height=0 width=0><br>\n")
	output_html_file_handler.close()
	print " ## %s written" % file_name

def main():
	expected_command_line_arguments = 4
	if(len(sys.argv) != expected_command_line_arguments):
		print "##### ERROR: Expected %d command line arguments but received %d: %s" % (expected_command_line_arguments, len(sys.argv), sys.argv)
		print "    Example: python generate-christmas-list.py couples.txt individuals.txt out.txt"
		return 1
	random.seed()

	couples_filename = sys.argv[1]
	individuals_filename = sys.argv[2]
	output_filename = sys.argv[3]

	couples = ExtractCouples(couples_filename)
	shuffled_couples = ShuffleCouples(couples)

	individuals = ExtractIndividuals(individuals_filename)
	shuffled_individuals = ShuffleIndividuals(individuals)

	OutputFile(output_filename, shuffled_couples, shuffled_individuals)

if __name__ == "__main__":
	main()
