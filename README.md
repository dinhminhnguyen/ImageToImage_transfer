# ImageToImage_transfer
#Deploy water classifier using flask on heroku


A web app to predict whether image is winter or summer using fastai library.And transfer into another season.

#Demo:

Getting started
Fork and clone this repo on to your system
Customization
Put your model inside path/models folder
Place your trained `.pth` or `.h5` file under path/models/ directory.
Change the class and path name
Open "app.py" and search for a variable called classes and change that with your own classes

If your path name is different that `seasontrainer.pth`, then change the learn.load("with_your_file_name.pth") in "app.py"

#UI Change
Modify files in templates and static directory.

index.html for the UI and main.js for all the behaviors

Note: If App is showing Application error then refresh the browser,It will work fine.
