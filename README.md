# Team 22 Demand Python Backend
This is the Team 22 backend for demand. This repository deals with `demand` back end.

## REST API
You can view working REST API for supply using [Postman]()

## Structure
```
team22-supply-backend
├── docs                            # Documentation Directory
├── unittest                        # Unit Test Directory to test Object classes                     
│   └── customer_test_case.py       # Test cases for `customer.py` class
│   └── order_test_case.py          # Test cases for `order.py` class
├── customer.py                     # Customer class object
├── order.py                        # Order class object
├── server.py                       # The main Python endpoints server for supply cloud
├── requirements.txt                # Python Dependencies to run `server.py`
├── bitbucket-pipelines.yml         # This is our bitbucket pipeline which does continous integrations test
└── README.md                       # Documentation about this repo
```

> Use short lowercase names for files and folders except for
> `README.md`

# Modifying This Repo
### Cloning repository
***Before you star you must have Python 3.8 installed in your system***  
If you would like to contribute to this repository, you first must clone this repository by running:  
```git clone https://bitbucket.org/swe-spring-2021-team-22/team22-demand-backend.git```  
  
### Setting Up Environment
After doing so, go to the `team22-demand-backend` directory using command line or PyCharm Terminal and we will install the `env` environment for your setup by running:  
`python3 -m venv env`  
  
### Activating Environment
Now that you have the environment, in order to be in the environment you type:  
`source env/bin/activate`  
  
### Installing/Uninstalling Dependencies
Make sure you install dependencies. You do so by running `python3 -m pip install -r requirements.txt`. If you added more or removed dependencies and need to generate a new `requirements.txt`, you do so by running:  

`pip freeze > requirements.txt`.
  
### Deactivating Environment
Now you should be in the `env` environment. To get out of the environment you type `deactivate` in command line.