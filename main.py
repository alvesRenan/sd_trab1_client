from Client import Client


client = Client()
while True:
  client.show_table()
  
  # Get the action from the user
  user_input = input("action: ")
  
  # Checks to see if the action exists
  # And receives the name of the method to call
  option = client.get_action(user_input)

  if not option:
    print("Invalid option \'{}\'.".format(user_input))
  
  else:
    # Gets the reference to the method
    method = getattr(client, option)
  
    # Invokes the method
    method()
