package main

func main() {
	mac := &Mac{}
	client := &Client{}

	client.InsertLightingConnectorIntoComputer(mac)

	windowsMachine := Windows{}
	windowsMachineAdapter := &WindowAdapter{
		windowMachine: &windowsMachine,
	}

	client.InsertLightingConnectorIntoComputer(windowsMachineAdapter)
}
