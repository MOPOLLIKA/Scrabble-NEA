import matplotlib.pyplot as plt

# Poll data and responses
poll_data = {
    "Do you know the classic Scrabble game?": ["Yes", "No", "I've heard of it, but not very familiar"],
    "Do you play Scrabble sometimes?": ["Yes", "No"],
    "Would you change the classic rules if you could?": ["I would make some changes", "I wouldn't change the rules", "Not sure"],
    "Would you particularly change the rule allowing plurals?": ["Yes", "No"],
    "Would you like additional interface?": ["It's better to have some interface", "Straight into the game!"],
    "Do you think calculating score during making a move would be useful?": ["Yes", "No"],
    "Would you prefer a simplistic design, or a detailed one?": ["Detailed", "Simplistic"],
    "How much time would be acceptable for you to wait against a bot?": ["1-5 sec", "5-15 sec", "15-30 sec", "30-60 sec"],
    "Would you like to be able to change the difficulty of the bot?": ["Yes", "No"],
    "Would you want to be able to have a player name?": ["Yes", "No"],
    "Would you like to access game rules handbook during the game?": ["Yes", "No"]
}

poll_responses = {
    "Do you know the classic Scrabble game?": [18, 5, 7],
    "Do you play Scrabble sometimes?": [12, 18],
    "Would you change the classic rules if you could?": [13, 10, 7],
    "Would you particularly change the rule allowing plural word forms?": [9, 21],
    "Would you like additional interface?": [16, 14],
    "Do you think calculating score during making a move would be useful?": [20, 10],
    "Would you prefer a simplistic design, or a detailed one?": [14, 16],
    "How much time would be acceptable for you to wait against a bot?": [8, 12, 7, 3],
    "Would you like to be able to change the difficulty of the bot?": [22, 8],
    "Would you want to be able to have a player name?": [24, 6],
    "Would you like to access game rules handbook during the game?": [21, 9]
}

# Create a 4x3 grid of subplots
fig, axs = plt.subplots(4, 3, figsize=(18, 16))
fig.suptitle("Simulated Poll Results for Scrabble Game Survey", fontsize=20)
axs = axs.flatten()

# Plot each question and its responses
for i, (question, options) in enumerate(poll_data.items()):
    responses = poll_responses[question]
    axs[i].bar(options, responses, color='skyblue', edgecolor='black')
    axs[i].set_title(question, fontsize=14)
    axs[i].tick_params(axis='x', rotation=45, labelsize=10)
    axs[i].set_ylabel("Number of Responses")
    axs[i].set_ylim(0, max(responses) + 5)

# Remove any empty subplots
for j in range(len(poll_data), len(axs)):
    fig.delaxes(axs[j])

plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save as a PNG file
plt.savefig("simulated_poll_results.png")
plt.show()
