# one-click
One-click deployment for Machine Learning apps

## Deploy instructions
1. Install terraform `brew install terraform`
1. Clone the repo
2. Install the package (from inside the cloned repo) `pip install -e .`
3. If you do not have local key pair files on your computer, generate public and private rsa keys so a new key pair can automatically be imported to aws by using the default values with `ssh-keygen`. **_Careful_: This will overwrite any existing keys that that are named `id_rsa` and `id_rsa.pub`, so only generate them with default arguments if don't have any in `~/.ssh`**
4. Ensure that you have valid aws credentials in either your `~/.aws/credentials` file (as set up by the aws cli) or in environment variables (`AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY`)
5. Make a new directory to track the state of your deployment. It can be anywhere.
5. Deploy your project! Inside the deployment directory you just created, run
```
one-click https://github.com/gusostow/EXAMPLE-localtype_site --public_key_path=~/.ssh/id_rsa.pub --private_key_path=~/.ssh/id_rsa
```

### Tear down instructions
1. Navigate to your deployment directory, which is where the terraform state is located.
2. Run `one-click destroy`
