# File-observer Docker image

This image is tended to be use for watching into file system directories changes.

## Download

You can download this image by executing the code below:

	docker pull maekind/file-observer:latest
    
## Usage

File-observer docker image launches a python script that is executed forever. It watches for changes into a directory passed as argument.

### Arguments

	- -p, --path: Full path to watch for changes.
	- -r, --recursive: Set to True for recursive watching. Otherwise, set to False. (Default is True)
	- -e, --enable-webservice: Set to True to send events to webservice. (Default is False)
	- -a, --address: Webservice host address or FQDN. Mandatory if enable-webservice set to True.
	- -o, --port: Webservice port. Mandatory if enable-webservice set to True.

### Running the docker - Printing changes to the standard output

In order to watch to a system folder, it has to be mapped with "-v" docker option.

Here-below there is an example that maps "/srv/folder" local folder to "/srv/folder" running image folder to watch for changes recursively.
This execution print events at the standard output.

	$> docker run -ti -v /srv/folder:/srv/folder maekind/file-observer:latest -p /srv/folder -r True

### Running the docker - Sending events to a webservice

If you want to send events to a webservice, you can run the docker image as follows:

	$> docker run -ti -v /srv/folder:/srv/folder maekind/file-observer:latest -p /srv/folder -r True -e True -a "http://<your_ip_address_or_fqdn>" -o <port>

I asume that you have a webserver that is listening at \<your_ip_address_or_fqdn>:\<port> for the events "created" and "deleted". 
For instance, you can create a Flask server to test the docker image as follows:

	from flask import Flask
	
	app = Flask(__name__)

	@app.route('/')
	def hello_message():
		return 'Webservice for handling system file changes'

	@app.route('/created/<path:file>')
	def create_file(file):
		message = f'Create {file}'
		# TODO: Do the related work ...
		return message 

	@app.route('/deleted/<path:file>')
	def delete_file(file):
		message = f'Delete {file}'
		# TODO: Do the related work ...
		return message 

You can run the Flask server by typing the following command:

	$> python3 -m flask run --host=<your_ip_address_or_fqdn> --port=<port>

## Credits

2021 Copyright to Marco Espinosa. 

Say hello!: [hi@marcoespinosa.es](mailto:hi@marcoespinosa.es)
