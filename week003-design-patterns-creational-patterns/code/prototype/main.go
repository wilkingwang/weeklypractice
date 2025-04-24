package main

func main() {
	file1 := &File{name: "file1"}
	file2 := &File{name: "file2"}
	file3 := &File{name: "file3"}

	folder1 := &Folder{
		name:     "folder1",
		children: []Inode{file1},
	}

	folder2 := &Folder{
		name:     "folder2",
		children: []Inode{folder1, file2, file3},
	}

	folder2.Print(" ")

	cloneFolder := folder2.Clone()
	cloneFolder.Print(" ")
}
