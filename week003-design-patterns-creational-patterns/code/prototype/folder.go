package main

import "fmt"

type Folder struct {
	children []Inode
	name     string
}

func (f *Folder) Print(indentation string) {
	fmt.Println(indentation + f.name)

	for _, i := range f.children {
		i.Print(indentation + indentation)
	}
}

func (f *Folder) Clone() Inode {
	cloneFolder := &Folder{name: f.name + "_clone"}

	var tmpChildren []Inode
	for _, i := range f.children {
		item := i.Clone()
		tmpChildren = append(tmpChildren, item)
	}

	cloneFolder.children = tmpChildren
	return cloneFolder
}
