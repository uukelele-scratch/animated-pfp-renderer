# Scratch PFP Renderer (supports animated images)

## How this project works:

client: scratch project
host: python script

Firstly, the client asks the user for the Scratch username, and sends it to the host. The host then responds with whether the image is a GIF or not. The client saves this as a variable so that the renderer knows which type of data to expect.

The client then makes another request, this time with the same argument(s) but different response. This is where the data is received.

Then, the client renders the data in the appropriate format.
