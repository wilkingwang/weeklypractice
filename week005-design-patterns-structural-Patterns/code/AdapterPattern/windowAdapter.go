package main

import "fmt"

type WindowAdapter struct {
	windowMachine *Windows
}

func (w *WindowAdapter) InsertIntoLightningPort() {
	fmt.Println("Adapter converts  lighting signal to usb")
}
