package main

type Inode interface {
	Print(string)
	Clone() Inode
}
