from get_next_train import get_next_train
from gpiozero import Button
from signal import pause

id = 'place-unsqu'

button = Button(17)

button.when_pressed = lambda: get_next_train(id)

pause()