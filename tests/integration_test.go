// Integration test that deploys github flask project to real infrastructure
package test

import (
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"runtime"
	"testing"
	"time"

	"github.com/gruntwork-io/terratest/modules/ssh"
	"github.com/gruntwork-io/terratest/modules/terraform"
	test_structure "github.com/gruntwork-io/terratest/modules/test-structure"
)

func TestGithub(t *testing.T) {
	terraformDirectory := "../one_click/terraform"
	tempdirName := "deployment_directory"
	dnsFileName := "public_dns"

	// Destroy infrastructure and temporary files at the end of the test
	defer test_structure.RunTestStage(t, "teardown", func() {
		terraformOptions := test_structure.LoadTerraformOptions(t, terraformDirectory)
		terraform.Destroy(t, terraformOptions)

		dir := filepath.Join(os.TempDir(), tempdirName)
		os.Remove(dir)

		// remove dns file if it exists
		dnsFilePath := filepath.Join(terraformDirectory, dnsFileName) + ".json"
		if _, e := os.Stat(dnsFilePath); e == nil {
			os.Remove(dnsFilePath)
		}
	})

	test_structure.RunTestStage(t, "setup", func() {
		// Give distinct "namespace" for test resources
		instanceNameBase := "terratest - flask-server"

		dir, e := ioutil.TempDir("", tempdirName)
		if e != nil {
			log.Fatal(e)
		}

		privatePath := filepath.Join(dir, "id_rsa")
		publicPath := filepath.Join(dir, "id_rsa.pub")
		privateF, _ := os.Create(privatePath)
		publicF, _ := os.Create(publicPath)

		// Create temporary keys
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

		// Save this information for the validation stage
		publicDNS := terraform.Output(t, terraformOptions, "public_dns")
		test_structure.SaveString(t, terraformDirectory, dnsFileName, publicDNS)
	})

	test_structure.RunTestStage(t, "validate", func() {
		// Load address of test webserver
		publicDNS := test_structure.LoadString(t, terraformDirectory, dnsFileName)

		time.Sleep(time.Second * 30)
		// Check if webserver is responding to requests
		publicDNSFullURL := "http://" + publicDNS
		response, e := GetWithRetryE(publicDNSFullURL, 30)

		if e != nil {
			t.Error(e)
		} else if response.StatusCode != 200 {
			t.Error("Test failed: Got status code", response.StatusCode)
		} else {
			log.Print("Successfully received response from", publicDNS)
		}
	})
}
