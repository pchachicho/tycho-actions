# Tycho

[![Build Status](https://travis-ci.org/stevencox/tycho.svg?branch=master)](https://travis-ci.org/stevencox/tycho)

Tycho is an API and abstraction layer for the lifecycle management of Kubernetes applications.

While the Kubernetes API is extensive and well documented, it's also large and complex. We've chosen not to extend the full weight of that complexity to clients that need to instantiate applications in a cluster.

### Install - Development Environment

* Install python 3.7.x or greater.
* Create a virtual environment.
* Install the requirements.
* Start the server.

```
python3 -m venv environmentName
source environmentName/bin/activate
pip install -r requirements.txt
python api.py
```

#### Usage - Development Environment Next to Minikube

Run minikube:
```
minikbue start
```
Run the minikube dashboard:
```
minikube dashboard
```
Run the Tycho API:
```
cd tycho
PYTHONPATH=$PWD/.. python api.py
```

Launch the Swagger interface `http://localhost:5000/apidocs/`.
![image](https://user-images.githubusercontent.com/306971/53313133-f1337d00-3885-11e9-8aea-83ab4a92807e.png)

Use the Tycho client to launch the Jupyter data-science notebook. It is given the name jupyter-data-science-3425 and exposes port 8888.
```
(tycho) [scox@mac~/dev/tycho/tycho]$ PYTHONPATH=$PWD/.. python client.py --up -n jupyter-data-science-3425 -c jupyter/datascience-notebook -p 8888
200
{
  "status": "success",
  "result": {
    "container_map": {
      "jupyter-data-science-3425-c": {
        "port": 32188
      }
    }
  },
  "message": "Started system jupyter-data-science-3425"
}
http://192.168.99.111:32188
```

Request data from the newly created service.
```
(tycho) [scox@mac~/dev/tycho/tycho]$ wget --quiet -O- http://192.168.99.111:32188 | grep -i /title
    <title>Jupyter Notebook</title>
```
Shut down the service. This will delete all created artifacts (deployment, replica_sets, pods, services).
```
(tycho) [scox@mac~/dev/tycho/tycho]$ PYTHONPATH=$PWD/.. python client.py --down -n jupyter-data-science-3425
200
{
  "status": "success",
  "result": null,
  "message": "Deleted system jupyter-data-science-3425"
}
```
Verify the servie is no longer running.
```
(tycho) [scox@mac~/dev/tycho/tycho]$ wget --quiet -O- http://192.168.99.111:32188 | grep -i /title
(tycho) [scox@mac~/dev/tycho/tycho]$ ```
```



