package main

import "fmt"

func main() {
	nginxServer := newNginxServer()
	appStatusUrl := "/app/status"
	createUserUrl := "/create/user"

	httpCode, body := nginxServer.handleRequest(appStatusUrl, "GET")
	fmt.Printf("URL: %s\n\tHttpCode: %d\n\tBody: %s\n", appStatusUrl, httpCode, body)

	httpCode, body = nginxServer.handleRequest(appStatusUrl, "GET")
	fmt.Printf("URL: %s\n\tHttpCode: %d\n\tBody: %s\n", appStatusUrl, httpCode, body)

	httpCode, body = nginxServer.handleRequest(appStatusUrl, "GET")
	fmt.Printf("URL: %s\n\tHttpCode: %d\n\tBody: %s\n", appStatusUrl, httpCode, body)

	httpCode, body = nginxServer.handleRequest(createUserUrl, "POST")
	fmt.Printf("URL: %s\n\tHttpCode: %d\n\tBody: %s\n", createUserUrl, httpCode, body)

	httpCode, body = nginxServer.handleRequest(createUserUrl, "GET")
	fmt.Printf("URL: %s\n\tHttpCode: %d\n\tBody: %s\n", createUserUrl, httpCode, body)
}
