# Team 22 Backend Python Webserver
This repository handles python backend. It is proxied from NGINX to the Python script so that we can handle requests via python. This python request handler handles any request sent from `https://demand.team22.sweispring21.tk/api/v1/[reuqest-name-here]`.


# Installation
*Before you install, make sure you have Python 3.8.5 on your system.*

First off, clone the repository using:
```git clone https://bitbucket.org/swe-spring-2021-team-22/team22-backend.git"```

After that, `cd` in`team22-backend` and run ```python3 -m venv backend``` and you should have an environment created.


# Usage
In our system, all you have to do is go to your directory, else go to your cloned repository:
```cd /home/team22/team22-backend/```

Once you're in the directory, all you have to do is type:
```source backend/bin/activate```
And you should be able to see a paranthesis on the left that says `(backend)`, meaning you are in they python environment for that file.

Once you're done, you type `deactivate` in terminal to exit.
