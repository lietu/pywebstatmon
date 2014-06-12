# PyWebStatMon

PyWebStatMon is a simple website status monitor, written in Python.

The main goals for this small tool are:

 - Have a simple configuration for defining URLs, and their monitoring requirements
 - Make periodic requests to all configured pages to confirm their status
 - Verifies that the response matches the requirements (e.g. a specified string is found)
 - Measures the response times for the web pages
 - Writes everything in a log
 - Provides the status information on a simple web interface
 

## Installation

Just get the code, and run "pip install -r requirements.txt".
Simple enough, should work on pretty much any platform, let me know if it doesn't.
The tool has been confirmed to work with Windows and Linux.

I recommend you set up a Python [virtualenv](http://virtualenv.readthedocs.org/en/latest/) for
PyWebStatMon to avoid conflicts with your global Python environment.

Example installation:
```Shell
git clone https://github.com/lietu/pywebstatmon
cd pywebstatmon
pip install -r requirements.txt
```


## Configuration

The configuration file, ```config.yaml```, uses a simple YAML syntax, it should be pretty self-explanatory, but
if you need more information on the YAML syntax, please visit [http://www.yaml.org/](http://www.yaml.org/).

Check out config.example.yaml for a full example.

### Monitoring

The syntax for the config is as follows:
```YAML
monitors:
    url:
        poll_seconds: 60
        content:
            - Some text that must be found on the page
            - Some other text. 
```

Please note that the "-" and the ":" -characters have a special meaning on YAML and need to be there.
The example above e.g. searches for "Some other text." and not "- Some other text." on the page.

So for example, to validate that "http://www.example.com/login" has the text "Please login.", you could 
use the following configuration:
```YAML
monitors:
    http://www.example.com/login:
        poll_seconds: 60
        content:
            - Please login.
```

You can define the interval between checks with "poll_seconds". Just set it to the number of seconds 
between checks. The "content" -section is completely optional.


### Other

You can define the port the web server listens to with the "http_port" -option. If not set, no web interface will be provided.
Log will be written to the file defined with "log_file", if set. If not set, no logging will be done.

The log will ALWAYS be written to STDOUT, if you do not like this, redirect it to /dev/null.


## Usage

First of all, make sure you edit the configuration file as instructed above.

Then, in the directory with the code, run:
```Shell
python pywebstatmon.py
```

You can of course run this with [supervisor](http://supervisord.org/) or similar, when
you have finished testing out the configuration.


### Command line options

If you want to override the polling period globally for temporary testing purposes, you can use
the argument "--poll_seconds=X" where X is the number of seconds you want to set it to.

For more help, try ```python pywebstatmon.py --help```.


## Contributing to the project

Getting started with testing the system is fairly easy.
 
 1. Install [Vagrant](http://vagrantup.com) and [VirtualBox](https://www.virtualbox.org/)
 2. Make sure you have a clone of the repository
 3. In the repository root, run ```vagrant up``` and wait for the machine to be up and running.
 4. Run ```vagrant ssh``` to get into your new virtual development environment (or ```vagrant ssh-config``` to show SSH settings)
    The user and pass are both "vagrant" btw.
 5. The source code should be in /src
 6. Make sure your changes pass the tests before trying to send a pull request: ```python -m nose```
 7. Make sure your code conforms to [PEP-8](http://legacy.python.org/dev/peps/pep-0008/) and PyFlakes doesn't complain of anything.

Hint, try out [Flake8](https://flake8.readthedocs.org/en/2.1.0/) or my 
[small script](http://lietu.net/2013/07/pyquality-python-code-quality-monitoring.html) for monitoring PEP-8 and pyflakes compliancy

It will also open up the port 8000 on your workstation and forward it to the VM's port 8000.


## Interesting Tech

The project uses Flask to provide the simple web interface.
The frontend uses Twitter Bootstrap, jQuery, EJS and some other things from Initializr. 


## Notes

Be aware that this project relies completely on the Flask web server that shouldn't really be used as the only web server
if you expect more than just a little traffic on the site. It should do for most basic uses, but the application
really isn't made for big installations in it's current form.


## License

The code is distributed with the very free new BSD and MIT licenses. More information in LICENSE.md -file.

The included libraries and dependencies have their own licenses.
