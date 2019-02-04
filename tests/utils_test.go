package test

import (
	"fmt"
	"net/http"
	"time"
)

// GetWithRetryE tests if url responds with 200 after n_retries
func GetWithRetryE(url string, nRetries int) (response *http.Response, e error) {
	for i := 0; i < nRetries; i++ {
		response, e := http.Get(url)
		if e == nil {
			return response, e
		}
		time.Sleep(time.Second)
	}

	return nil, fmt.Errorf("Failed to receive a response after %d retries", nRetries)
}
