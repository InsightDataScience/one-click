# one-click
One-click deployment for Machine Learning Flask apps

## Before you Can Deploy

The deploy might be one click ... installing dependencies, making your AWS account, and ensuring your project is compatible with one-click is not. If you've already setup your machine and your project skip to the [quick-start guide](#quick-start-guide)

### AWS Setup

1. Create a [AWS account](aws.amazon.com) (or use an existing one).
2. Create an [IAM admin user and group](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html). AWS credentialling is confusing. This instruction creates a new sub-user that will be safer to use than the root account you just created in step 1.
3. Get the access key and secret access key from the IAM administrator user you just created. 
  - Go to the [IAM console](https://console.aws.amazon.com/iam/home?#home)
  - Choose **Users**
  - Select the **Security Credentials** tab and then hit **Create Access Key**
  - Choose **Show**
  - We need to export these as enviornment variables in your `~/.bash_profile`. You should add something that looks like this to the bootom of it using your favorite text editor:
  ```bash
  export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
  export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
  ```
  Now your laptop will be fully authorized to create resources on AWS!
  
### Create RSA Key Pair

1. Check to see if you already have keys with default names: `ls ~/.ssh`. If you have two files with names `id_rsa` and `id_rsa.pub` then you are all set to skip this section, if not then continue on to creating the key pair.
2. `rsa-keygen`
3. Continue by pressing enter repeatedly (you don't need to enter anything in the text boxes) until you see something like this 
```
+--[ RSA 2048]----+
|       o=.       |
|    o  o++E      |
|   + . Ooo.      |
|    + O B..      |
|     = *S.       |
|      o          |
|                 |
|                 |
|                 |
+-----------------+
```

### Software Requirements

- You need terraform installed.
  - MacOs: `brew install terraform`
  - linux: `apt-get install terraform`

### App Compatibility

One-click has several strict requirements for apps it can deploy. Rigid specifications keeps the tool easy to use. Check out some example [one-click compatible projects](#example-apps) that are compliant.

#### Directory Structure 

- There must be a python file called `run.py` in the root of your project directory that will run your app. _**The name and the location are non-negotiable.**_ The file might looks something like:
```python
from views import app

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
```
- As of now, run your app in `run.py` on `host='0.0.0.0'` and `port=80`
- Your directory structure **must be flat**. That means your `templates`, `static`, and file where you first create your flask app (`app = Flask(__name__)`) need to be **in the root for your project**. Otherwise things will break.

#### Requirements File

One-click builds a fresh python environment in ubuntu for every deployment. You need to clearly specify which python requirements your app depends on.

- Put the name (and potentially the version number) of every requirement in a file `requirements.txt` in the root of your project. Once again, _**The name and the location of `requirements.txt` are non-negotiable.**_ 

- If you haven't been keeping track of your requirements you could:
  - Use a tool like [pigar](https://github.com/damnever/pigar) to automatically generate it based on searching your project.
  - If you've been using a conda environment or a virtualenv for the project you can run `pip freeze > requirements.txt`

- **HINT:** A good way to test if your `requirements.txt` file is comprehensive is to create a fresh conda or virtual enviornment and try to run your app after installing from the file.
```bash
conda create -n test_env python=3.6
source activate test_env
pip install -r requirements.txt
python run.py
```

## Quick-start Guide

Consult the [app compatibility guidelines](#app-compatibility) before deploying for the first time. You may have to restructure your project before it will work with one-click.

### Deploy Instructions

1. Clone the repo
2. Install the one-click package (from inside the cloned repo) `pip install .`
3. Make a new directory to track the state of your deployment. It can be anywhere. This new *deployment directory* has nothing to do with your project directory that has your code. It will hold the backend state files for the deployment. Any time you want to reference this specific deployment you must be using one-click from its deployment directory.
4. Deploy your project! Inside the deployment directory you just created, run for github deployment (**NOTE:** if you didn't use the default names when you generated your RSA keys, or if you're on windows, then you will have to specify the paths with the `--private_key_path` and `--public_key_path`command line options)
```
one-click deploy-github https://github.com/gusostow/EXAMPLE-localtype_site
```
or for local deployment
```
one-click deploy-local ~/path/to/your/flask/project/folder
```

Your app should now be publicly available from the `public_dns` output in your console. If you want to ssh into the instance this can be done with `ssh ubuntu@<public-dns>`

### Destroy Instructions

1. Navigate to your deployment directory, which is where the terraform state is located.
2. Run `one-click destroy`

### Updating your App

As of now one-click does not provision automatic CI/CD support to keep your deployment up to date with pushes to your app's repo. To make updates:
1. Push your changes to github
2. Make sure you are inside the directory used for deployment, then destroy and re-deploy your project:
```
one-click destroy
one-click deploy-github <github-link-to-your-app>
```

## Troubleshooting your Deployment

A lot can go wrong with a one size fits all automatic deployment. Most issues will be visible with some detective work.

### Problems with Provisioning the Server and Building your App Environment

Build logs for installations on the server and building the docker environment are piped to console. Here you can see if there's an issue with making the ssh connection to remotely execute commands, cloning your repo to the server, or installing your requirements. If your url is completely unaccessable, then the error can likely be diagnosed here.

### Problems with Running your Code

However, once the environment is set up, the server logs won't be directly visible in your console. If you get a 403 error when you visit your webpage url, then that means there is an error in your code, which probably has something to do with porting it a docker environment.

You need to ssh into the server to view get visibility in those logs:
1. Get shell access to the server. `ssh ubuntu@<outputed-dns-address>`. You don't need to specify the path to a key file because you already did that in the deploy phase.
2. `cd app`
3. View the logs. `docker-compose logs`

Here you will find the python errors you are accustomed to diagnosing when developing your app.

### Other Fixes to Common Problems

#### Broken Paths
- **Problem:** Absolute paths to files like datasets or models will break. The path `~/gusostow/python/myproject/data/data.csv` might work fine on your laptop, it won't in the docker container built for your app, which has a different directory structure.
- **Solution:** Switch to referencing paths relatively to the python file that uses them, so they will be invariant to where the script is run. The `__file__` variable has that information.

## Example Apps 

- [Localtype](https://github.com/gusostow/EXAMPLE-localtype_site)
- [Hosteldirt](https://github.com/gusostow/EXAMPLE-hosteldirt)

