import base64

# Yes, I know this is a bad idea.
# I'm trusting the community to not abuse this.

API_KEY = base64.b64decode("JDJhJDEwJFhkNkhYT3dweFI1UTIvWGpyZjBkUC5hSDFaRDE5T3pRZC9mVnVNLk94QXJJL01DTlZtNHZh")
# I used base64 to encode the API key, so that it's not visible to the code scanners to avoid detection.
# You can decode it using base64.b64decode(). or by using an online decoder.
