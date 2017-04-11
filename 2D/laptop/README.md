![Screenshot | center](./assets/screenshot.png)

# What this is
The last two-dimensional (inter-subject) project of our freshman year at SUTD. Basically, we need to build a controlled system for culturing algae, where the temperature must be kept at a constant ideal. 

We made a water cooling system, the code to make it work, and a monitoring / config GUI.

# Features
- GUI for monitoring system + changing target temperature (works both with simulation and in real life)
- Pulls real-time UV index, air temperature and wind velocity from data.gov.sg to give a realistic simulation environment


# Installation
1. Add the database URL and secrets to your environment variables (ask me for them. We don't want random people messing with our DB!). Alternatively, get the `setup.py` files from me. Putting these in the right place will auto-add the necessary environment variables.
2. Install the graph widget from kivy garden (in terminal, enter `garden install graph`)
3. Tuh-duh

