import pandas as pd

# Create a sample dataframe
#data = {'sad_words':["sad","depressed","unhappy","angry","miserable","depressing"]}
data = {'starter_encouragements':["Cheer up!","Hang in there","You are a great person"]}
df = pd.DataFrame(data)

# Save the dataframe to a CSV file
df.to_csv('Storage/'+ df.keys()[0] +'.csv', index=False)