from flair_api import make_client



client = make_client(client_id, client_secret, 'https://api.flair.co/')

# retrieve a list of structures available to this account
structures = client.get('structures')

# get a single room by id
room = client.get('rooms', id="1")

# fetch vents in a room
vents = room.get_rel('vents')

# delete a room
room.delete()

# update a room
room.update(attributes={'name': 'Master Bedroom'}, relationships=dict(structure=structures[0], vents=vents))

# create a vent
vent = c.create('vents', attributes={'name': 'North Vent'}, relationships=dict(room=room))

# Add a vent to a room
room.add_rel(vents=vent)

# Update vent relationship for a room
room.update_rel(vents=[vent])

# Delete a vent relationship for a room
room.delete_rel(vents=vent)