package test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/gruntwork-io/terratest/modules/random"

	"github.com/gruntwork-io/terratest/modules/aws"
	"github.com/gruntwork-io/terratest/modules/terraform"
	test_structure "github.com/gruntwork-io/terratest/modules/test-structure"
)

func TestGithub(t *testing.T) {

	terraformDirectory := "../one_click/terraform"

	defer test_structure.RunTestStage(t, "teardown", func() {
		terraformOptions := test_structure.LoadTerraformOptions(t, terraformDirectory)
		keyPair := test_structure.LoadEc2KeyPair(t, terraformDirectory)

		terraform.Destroy(t, terraformOptions)
		aws.DeleteEC2KeyPair(t, keyPair)

		testFile := filepath.Join(terraformDirectory, "public-ip")
		if _, err := os.Stat(testFile); err == nil {
			os.Remove(testFile)
		}
	})

	test_structure.RunTestStage(t, "setup", func() {

		uniqueID := random.UniqueId()

	})

}
