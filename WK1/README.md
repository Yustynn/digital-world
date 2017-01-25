# Homework 1

## General
1. Run `pip install -r requirements.txt` to get all the dependencies I used
1. If you're using the `automate-tutor-submission` script, make sure you've got [geckodriver](https://github.com/mozilla/geckodriver/releases) in your `PATH`.

## `evil-exec.py`
This prints out the answers to entire exercises in batch
Run this with the exercise name as a command line argument (e.g. `python
evil-exec.py ex1`)
This only works for ex1, ex2, ex4

## `automate-tutor-submission` _INCOMPLETE_
This auto-submits the answers to tutor.
Currently, it just logs in and goes to week 1. Uses firefox (geckodriver).

Ensure that you have your credentials as `TUTOR_USERNAME` and `TUTOR_PASSWORD` in your environment (your `.bashrc` or whatever)
