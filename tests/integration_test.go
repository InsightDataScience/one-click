package test

import (
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"runtime"
	"testing"

	"github.com/gruntwork-io/terratest/modules/ssh"
	"github.com/gruntwork-io/terratest/modules/terraform"
	test_structure "github.com/gruntwork-io/terratest/modules/test-structure"
)

func TestGithub(t *testing.T) {

	terraformDirectory := "../one_click/terraform"
	tempdirName := "deployment_directory"

	defer test_structure.RunTestStage(t, "teardown", func() {
		terraformOptions := test_structure.LoadTerraformOptions(t, terraformDirectory)
		terraform.Destroy(t, terraformOptions)

		dir := filepath.Join(os.TempDir(), tempdirName)
		os.Remove(dir)
	})

	test_structure.RunTestStage(t, "setup", func() {

		instanceNameBase := "terratest - flask-server"

		dir, err := ioutil.TempDir("", tempdirName)
		if err != nil {
			log.Fatal(err)
		}

		privatePath := filepath.Join(dir, "id_rsa")
		publicPath := filepath.Join(dir, "id_rsa.pub")
		privateF, _ := os.Create(privatePath)
		publicF, _ := os.Create(publicPath)

		keyPair := ssh.GenerateRSAKeyPair(t, 1096)
		privateF.WriteString(keyPair.PrivateKey)
		publicF.WriteString(keyPair.PublicKey)

		_, callerPath, _, _ := runtime.Caller(0)
		baseDirectory := filepath.Join(callerPath, "../../one_click")

		terraformOptions := &terraform.Options{
			TerraformDir: terraformDirectory,

			// Variables to pass to our Terraform code using -var options
			Vars: map[string]interface{}{
				"instance_name_base":   instanceNameBase,
				"base_directory":       baseDirectory,
				"instance_type":        "t2.micro",
				"image_version":        "tiangolo/uwsgi-nginx-flask:python3.6",
				"project_link_or_path": "https://github.com/gusostow/EXAMPLE-hosteldirt.git",
				"path_to_public_key":   publicPath,
				"path_to_private_key":  privatePath,
				"use_github":           "1",
				"use_local":            "0",
			},
		}

		test_structure.SaveTerraformOptions(t, terraformDirectory, terraformOptions)

		terraform.InitAndApply(t, terraformOptions)

	})

	test_structure.RunTestStage(t, "validate", func() {
		t.Log("Validating stage")
	})

}
