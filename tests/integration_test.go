package test

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"testing"

	"github.com/gruntwork-io/terratest/modules/random"
	"github.com/gruntwork-io/terratest/modules/ssh"
	"github.com/gruntwork-io/terratest/modules/terraform"
	test_structure "github.com/gruntwork-io/terratest/modules/test-structure"
)

func SetUp() {

}

func TestGithub(t *testing.T) {

	terraformDirectory := "../one_click/terraform"

	defer test_structure.RunTestStage(t, "teardown", func() {
		terraformOptions := test_structure.LoadTerraformOptions(t, terraformDirectory)
		terraform.Destroy(t, terraformOptions)

		os.RemoveAll(dir)
	})

	test_structure.RunTestStage(t, "setup", func() {

		uniqueID := random.UniqueId()
		instanceNameBase := "terratest - flask-server"

		dir, err := ioutil.TempDir("", "deployment_directory")
		if err != nil {
			log.Fatal(err)
		}

		keyPair := ssh.GenerateRSAKeyPair(t, 1096)
		fmt.Printf(keyPair.PublicKey)

	})

}
