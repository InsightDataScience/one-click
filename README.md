# one-click
One-click deployment for Machine Learning Flask apps

## Quick-start Guide

Consult the [app compatibility guidelines](#app-compatibility) before deploying for the first time. You may have to restructure your project before it will work with one-click.

### Deploy Instructions

1. Install terraform `brew install terraform` / `apt-get install terraform`
1. Clone the repo
2. Install the one-click package (from inside the cloned repo) `pip install -e .`
3. If you do not have local key pair files on your computer, generate public and private rsa keys so a new key pair can automatically be imported to aws by using the default values with `ssh-keygen`. **_Careful_: This will overwrite any existing keys that that are named `id_rsa` and `id_rsa.pub`, so only generate them with default arguments if don't have any in `~/.ssh`**
4. Ensure that you have valid aws credentials in either your `~/.aws/credentials` file (as set up by the [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)) or in environment variables (`AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY`)
5. Make a new directory to track the state of your deployment. It can be anywhere.
6. Deploy your project! Inside the deployment directory you just created, run
```
one-click deploy https://github.com/gusostow/EXAMPLE-localtype_site --public_key_path=~/.ssh/id_rsa.pub --private_key_path=~/.ssh/id_rsa
```
Your app should now be publicly available from the `public_dns` output in your console.

### Destroy Instructions

1. Navigate to your deployment directory, which is where the terraform state is located.
2. Run `one-click destroy`

### Updating your App

As of now one-click does not provision automatic CI/CD support to keep your deployment up to date with pushes to your app's repo. To make updates:
1. Push your changes to github
2. Make sure you are inside the directory used for deployment, then destroy and re-deploy your project:
```
one-click destroy
one-click deploy <github-link-to-your-app>
```

## App Compatibility

One-click has several strict requirements for apps it can deploy. Rigid specifications keeps the tool easy to use. Check out some example [one-click compatible projects](#example-apps) that are compliant.

### Directory Structure 

- There must be a python file called `run.py in the root of your project directory that will run your app. _**The name and the location are non-negotiable.**_ The file might looks something like:
```python
from your_project import app

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
```
- As of now, run your app in `run.py` on `host='0.0.0.0'` and `port=80`

### Requirements File

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

## Troubleshooting your Deployment

A lot can go wrong with a one size fits all automatic deployment. Most issues will be visible with some detective work.

### Problems with Provisioning the Server and Building your App Environment

Build logs for installations on the server and building the docker environment are piped to console. Here you can see if there's an issue with making the ssh connection to remotely execute commands, cloning your repo to the server, or installing your requirements. If your url is completely unaccessable, then the error can likely be diagnosed here.

### Problems with Running your Code

However, once the environment is set up, the server logs won't be directly visible in your console. If you get a 403 error when you visit your webpage url, then that means there is an error in your code, which probably has something to do with porting it a docker environment.

You need to ssh into the server to view get visibility in those logs:
1. Get shell access to the server. `ssh ubuntu@<outputed-dns-address>`. You don't need to specify the path to a key file because you already did that in the deploy phase.
2. `cd app`
3. View the logs. `sudo docker-compose logs`

Here you will find the python errors you are accustomed to diagnosing when developing your app.

## Example Apps 

- [Localtype](https://github.com/gusostow/EXAMPLE-localtype_site)
- [Hosteldirt](https://github.com/gusostow/EXAMPLE-hosteldirt)

