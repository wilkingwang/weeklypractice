package main

import "fmt"

type Client struct {
}

func (c *Client) InsertLightingConnectorIntoComputer(com Computer) {
	fmt.Println("Client inserts Lighting connector into computer.")
	com.InsertIntoLightningPort()
}
